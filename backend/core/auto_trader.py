"""AutoTrader — ระบบเทรดอัตโนมัติที่รวมทุก component เข้าด้วยกัน

การทำงาน:
1. Regime Detection → เลือก strategy ที่เหมาะสม
2. AI Signal Generation → สร้างสัญญาณจาก MiniMax
3. Risk Check → RiskManager ตรวจก่อนเทรด
4. Position Sizing → PositionSizer คำนวณขนาด
5. Execute → Trader เปิดสถานะ + บันทึกเหตุผล (TradeReasoner)
6. Monitor → TrailingStop ติดตาม + PortfolioMonitor วิเคราะห์
7. Record → บันทึกผลเข้า RiskManager + PositionSizer
"""
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

from .models import TradeSignal, Trade, TradeStatus, TradeDirection, AssetType, WalletType
from .trader import Trader
from .wallet_manager import WalletManager
from .position_sizer import PositionSizer, PositionSizeResult
from .risk_manager import RiskManager, RiskCheckResult
from .trailing_stop import TrailingStop
from .regime_detector import RegimeDetector, MarketRegime
from .portfolio_monitor import PortfolioMonitor, PortfolioRiskReport
from .trade_reasoner import TradeReasoner, TradeReasonLog


@dataclass
class AutoTraderConfig:
    """Configuration for AutoTrader"""
    sizing_method: str = "kelly"
    kelly_variant: str = "half"
    max_risk_per_trade: float = 0.02
    max_position_pct: float = 0.10
    
    max_drawdown_pct: float = 0.20
    max_daily_loss_pct: float = 0.03
    max_weekly_loss_pct: float = 0.08
    max_consecutive_losses: int = 5
    
    trailing_method: str = "percentage"
    trailing_pct: float = 0.02
    trailing_activation_pct: float = 0.01
    
    regime_detection_enabled: bool = True
    loop_interval_seconds: int = 60
    confidence_threshold: float = 0.70


@dataclass
class TradeWithExtras:
    """Trade ที่มี trailing stop + metadata"""
    trade: Trade
    trailing_stop: Optional[TrailingStop] = None
    regime_at_entry: Optional[MarketRegime] = None
    sizing_result: Optional[PositionSizeResult] = None
    news_signal: Optional[Dict[str, Any]] = None
    indicators: Optional[Dict[str, float]] = None


class AutoTrader:
    """
    AutoTrader — ระบบเทรดอัตโนมัติที่รวมทุก component
    
    Components:
    - Trader: execution engine
    - PositionSizer: คำนวณขนาดสถานะ
    - RiskManager: ตรวจสอบความเสี่ยงก่อนเทรด
    - TrailingStop: ติดตามและล็อกกำไร
    - RegimeDetector: ตรวจจับ market regime
    - PortfolioMonitor: วิเคราะห์ความเสี่ยงพอร์ต
    - TradeReasoner: บันทึกเหตุผลเปิด/ปิดทุก trade
    """

    def __init__(
        self,
        initial_balance: float = 100_000.0,
        config: Optional[AutoTraderConfig] = None,
        db_path: str = "data/trades.db",
    ):
        self.config = config or AutoTraderConfig()
        
        self.wallet_manager = WalletManager(
            paper_initial=initial_balance,
            paper_currency="USDT",
        )
        self.trader = Trader(
            wallet_manager=self.wallet_manager,
            db_path=db_path,
            wallet_type=WalletType.PAPER,
        )
        
        self.position_sizer = PositionSizer(
            method=self.config.sizing_method,
            kelly_variant=self.config.kelly_variant,
            portfolio_value=initial_balance,
            max_risk_per_trade=self.config.max_risk_per_trade,
            max_position_pct=self.config.max_position_pct,
        )
        
        self.risk_manager = RiskManager(
            initial_balance=initial_balance,
            max_drawdown_pct=self.config.max_drawdown_pct,
            max_daily_loss_pct=self.config.max_daily_loss_pct,
            max_weekly_loss_pct=self.config.max_weekly_loss_pct,
            max_consecutive_losses=self.config.max_consecutive_losses,
        )
        
        self.regime_detector = RegimeDetector()
        self.portfolio_monitor = PortfolioMonitor(portfolio_value=initial_balance)
        
        # ✅ TradeReasoner: บันทึกเหตุผลเปิด/ปิด
        self.reasoner = TradeReasoner()
        
        self.active_trades: Dict[str, TradeWithExtras] = {}
        self.initial_balance = initial_balance

    # ================================================================= #
    # Pre-Trade Pipeline
    # ================================================================= #

    def pre_trade_check(
        self,
        signal: TradeSignal,
        news_signal: Optional[Dict[str, Any]] = None,
    ) -> RiskCheckResult:
        """
        Pipeline ทั้งหมดก่อนเปิด trade:
        1. Position sizing
        2. Risk check
        """
        if signal.symbol in self.active_trades:
            return RiskCheckResult(
                allowed=False,
                reason=f"Position already exists for {signal.symbol}",
                level="warning",
                blocked_by="duplicate_position",
            )
        
        sizing = self.position_sizer.calculate(
            symbol=signal.symbol,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
            confidence=signal.confidence,
        )
        
        signal.quantity = sizing.size / signal.entry_price if signal.entry_price > 0 else sizing.size
        
        trade_value = signal.quantity * signal.entry_price
        loss_if_wrong = trade_value * self.config.max_risk_per_trade
        
        result = self.risk_manager.pre_trade_check(
            trade_pnl_if_loss=loss_if_wrong,
            current_positions=len(self.active_trades),
        )
        
        result.details["sizing"] = {
            "method": sizing.method,
            "size": sizing.size,
            "quantity": signal.quantity,
            "kelly_pct": sizing.kelly_pct,
            "reason": sizing.reason,
        }
        
        return result

    # ================================================================= #
    # Execute Trade
    # ================================================================= #

    def execute_trade(
        self,
        signal: TradeSignal,
        regime: Optional[MarketRegime] = None,
        news_signal: Optional[Dict[str, Any]] = None,
        indicators: Optional[Dict[str, float]] = None,
    ) -> Optional[Trade]:
        """
        Execute trade หลังจากผ่าน pre_trade_check แล้ว
        
        บันทึกเหตุผลการเปิด trade ด้วย TradeReasoner
        """
        # 1. ตรวจสอบ risk ก่อนเปิด trade
        risk_check = self.pre_trade_check(signal, news_signal)
        
        sizing = self.position_sizer.calculate(
            symbol=signal.symbol,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
            confidence=signal.confidence,
        )
        
        # 2. Block trade if risk check failed
        if not risk_check.allowed:
            print(f"[BLOCKED] Trade blocked: {risk_check.reason}")
            self.reasoner.log_entry(
                trade_id=f"blocked_{signal.symbol}",
                trade_number=-1,
                symbol=signal.symbol,
                direction="LONG" if signal.direction == TradeDirection.BUY else "SHORT",
                wallet_type=self.trader.wallet_type.value,
                entry_price=signal.entry_price,
                stop_loss=signal.stop_loss,
                take_profit=signal.take_profit,
                signal=signal,
                regime=regime,
                sizing_result=sizing,
                risk_check_result=risk_check,
                news_signal=news_signal,
                indicators=indicators,
            )
            return None
        
        signal.quantity = sizing.size / signal.entry_price if signal.entry_price > 0 else sizing.size
        
        trade = self.trader.execute_signal(signal)
        
        if trade is None:
            return None
        
        trailing = TrailingStop(
            method=self.config.trailing_method,
            trail_pct=self.config.trailing_pct,
            activation_pct=self.config.trailing_activation_pct,
        )
        direction = "LONG" if signal.direction == TradeDirection.BUY else "SHORT"
        trailing.activate(direction=direction, entry_price=signal.entry_price)
        
        self.active_trades[signal.symbol] = TradeWithExtras(
            trade=trade,
            trailing_stop=trailing,
            regime_at_entry=regime,
            sizing_result=sizing,
            news_signal=news_signal,
            indicators=indicators,
        )
        
        self.portfolio_monitor.add_position(
            symbol=signal.symbol,
            size=sizing.size,
            entry_price=signal.entry_price,
        )
        
        self.position_sizer.update_portfolio_value(self.trader.wallet.balance)
        
        # ✅ บันทึกเหตุผลเปิด trade
        self.reasoner.log_entry(
            trade_id=str(trade.id or trade.trade_number),
            trade_number=trade.trade_number,
            symbol=signal.symbol,
            direction=direction,
            wallet_type=self.trader.wallet_type.value,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            signal=signal,
            regime=regime,
            sizing_result=sizing,
            risk_check_result=risk_check,
            news_signal=news_signal,
            indicators=indicators,
        )
        
        # ✅ พิมพ์เหตุผลเปิด trade
        log = self.reasoner.get_trade_reason(str(trade.id or trade.trade_number))
        if log and log.entry:
            print()
            print(log.entry.summary)
        
        return trade

    # ================================================================= #
    # Monitor & Update
    # ================================================================= #

    def update_prices(
        self,
        price_updates: Dict[str, float],
        regime_updates: Optional[Dict[str, MarketRegime]] = None,
    ):
        """
        อัปเดตราคาปัจจุบัน + ตรวจ trailing stop + regime change
        
        เรียกทุก tick หรือทุก interval
        """
        closed = []
        
        for symbol, current_price in price_updates.items():
            if symbol not in self.active_trades:
                continue
            
            trade_extras = self.active_trades[symbol]
            trailing = trade_extras.trailing_stop
            trade = trade_extras.trade
            
            self.portfolio_monitor.update_position_price(symbol, current_price)
            
            # --- Trailing Stop ---
            if trailing:
                result = trailing.update(current_price)
                
                if result.triggered:
                    self._close_trade(
                        symbol,
                        exit_price=result.exit_price,
                        trigger="trailing_stop",
                        trigger_detail=result.reason,
                        trailing_info={
                            "high": result.highest_price,
                            "locked_pct": result.profit_locked_pct,
                        },
                    )
                    closed.append(symbol)
                    continue
            
            # --- Regime Change Check ---
            if regime_updates and symbol in regime_updates:
                new_regime = regime_updates[symbol]
                old_regime = trade_extras.regime_at_entry
                
                if old_regime and new_regime.name != old_regime.name:
                    # Regime เปลี่ยน — อาจต้องปิด
                    if new_regime.name in ("CRASH", "VOLATILE"):
                        self._close_trade(
                            symbol,
                            exit_price=current_price,
                            trigger="regime_change",
                            trigger_detail=f"Regime changed: {old_regime.name} → {new_regime.name}. {new_regime.reason}",
                        )
                        closed.append(symbol)
                        continue
            
            # --- SL/TP Check ---
            sl_result = self.trader.check_stop_loss_take_profit(symbol, current_price)
            if sl_result:
                trigger = "stop_loss" if "stop" in (sl_result.status.value or "").lower() else "take_profit"
                self._close_trade(
                    symbol,
                    exit_price=sl_result.exit_price,
                    trigger=trigger,
                    trigger_detail=f"Price reached {current_price:.2f}",
                )
                closed.append(symbol)

    def _close_trade(
        self,
        symbol: str,
        exit_price: float,
        trigger: str,
        trigger_detail: str,
        trailing_info: Optional[Dict[str, float]] = None,
    ):
        """Helper: ปิด trade + อัปเดตทุก component + บันทึกเหตุผล"""
        if symbol not in self.active_trades:
            return
        
        trade_extras = self.active_trades[symbol]
        trade = trade_extras.trade
        
        closed_trade = self.trader.close_trade(symbol, exit_price, trigger)
        
        if closed_trade:
            pnl = closed_trade.pnl
            pnl_pct = pnl / (closed_trade.quantity * closed_trade.entry_price) if closed_trade.quantity > 0 and closed_trade.entry_price > 0 else 0
            
            if closed_trade.quantity > 0 and closed_trade.entry_price > 0:
                return_pct = pnl / (closed_trade.quantity * closed_trade.entry_price)
                self.position_sizer.record_trade_result(return_pct)
            
            self.risk_manager.record_trade(pnl)
            self.portfolio_monitor.remove_position(symbol)
            self.position_sizer.update_portfolio_value(self.trader.wallet.balance)
            
            # ✅ บันทึกเหตุผลปิด trade
            self.reasoner.log_exit(
                trade_id=str(trade.id or trade.trade_number),
                trade_number=trade.trade_number,
                trigger=trigger,
                trigger_detail=trigger_detail,
                exit_price=exit_price,
                entry_price=trade.entry_price,
                pnl=pnl,
                pnl_pct=pnl_pct,
                trailing_info=trailing_info,
            )
            
            # ✅ พิมพ์เหตุผลปิด trade
            log = self.reasoner.get_trade_reason(str(trade.id or trade.trade_number))
            if log and log.exit:
                print()
                print(log.exit.summary)
        
        del self.active_trades[symbol]

    # ================================================================= #
    # Regime & Signal
    # ================================================================= #

    def detect_regime(
        self,
        prices: List[float],
        highs: Optional[List[float]] = None,
        lows: Optional[List[float]] = None,
    ) -> MarketRegime:
        """ตรวจจับ market regime"""
        return self.regime_detector.detect(prices, highs, lows)

    def get_adjusted_confidence(
        self,
        base_confidence: float,
        regime: MarketRegime,
    ) -> tuple[float, str]:
        """ปรับ confidence ตาม regime"""
        return self.regime_detector.get_strategy_for_regime(regime, base_confidence)

    # ================================================================= #
    # Reporting
    # ================================================================= #

    def get_full_status(self) -> Dict[str, Any]:
        """สถานะระบบทั้งหมด"""
        risk_stats = self.risk_manager.get_portfolio_stats()
        portfolio_report = self.portfolio_monitor.generate_report()
        
        active_positions = []
        for symbol, te in self.active_trades.items():
            trailing_status = te.trailing_stop.get_status() if te.trailing_stop else {}
            active_positions.append({
                "symbol": symbol,
                "direction": te.trade.direction.value,
                "entry_price": te.trade.entry_price,
                "quantity": te.trade.quantity,
                "unrealized_pnl": te.trade.pnl,
                "regime_at_entry": te.regime_at_entry.name if te.regime_at_entry else None,
                "trailing": trailing_status,
            })
        
        return {
            "wallet": self.trader.get_balance(),
            "stats": self.trader.get_stats(),
            "risk": risk_stats,
            "portfolio": {
                "var_95_daily": portfolio_report.var_95_daily,
                "var_95_monthly": portfolio_report.var_95_monthly,
                "cvar_95": portfolio_report.cvar_95_daily,
                "sharpe_ratio": portfolio_report.sharpe_ratio,
                "max_drawdown": f"{portfolio_report.max_drawdown:.2%}",
                "risk_level": portfolio_report.risk_level,
                "warnings": portfolio_report.warnings,
                "positions": [
                    {
                        "symbol": p.symbol,
                        "weight": f"{p.weight:.1%}",
                        "var_95": p.var_95,
                        "contribution_pct": f"{p.contribution_pct:.1%}",
                    }
                    for p in portfolio_report.positions
                ],
            },
            "active_trades": active_positions,
            "position_sizer": {
                "method": self.position_sizer.method,
                "kelly_variant": self.position_sizer.kelly_variant,
                "trade_history_count": len(self.position_sizer.trade_history),
            },
        }

    # ================================================================= #
    # Trade Reasoner Access
    # ================================================================= #

    def print_trade_reason(self, trade_id: str):
        """พิมพ์เหตุผลของ trade สวยงาม"""
        self.reasoner.print_trade_reason(trade_id)

    def get_trade_reason(self, trade_id: str) -> Optional[TradeReasonLog]:
        """ดึงเหตุผลของ trade"""
        return self.reasoner.get_trade_reason(trade_id)

    def get_all_trade_reasons(self) -> List[TradeReasonLog]:
        """ดึงเหตุผลทั้งหมด"""
        return self.reasoner.get_all_reasons()

    # ================================================================= #
    # Demo / Backtest
    # ================================================================= #

    def simulate_trade(
        self,
        symbol: str,
        direction: TradeDirection,
        entry_price: float,
        exit_price: float,
        quantity: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        regime: Optional[MarketRegime] = None,
        holding_bars: int = 10,
    ):
        """
        Simulate a trade for backtesting — ไม่ต้อง execute จริง
        
        ใช้สำหรับทดสอบ logic โดยไม่กระทบ wallet จริง
        """
        from .models import TradeSignal
        
        signal = TradeSignal(
            asset_type=AssetType.CRYPTO if "BTC" in symbol or "ETH" in symbol else AssetType.GOLD,
            symbol=symbol,
            direction=direction,
            entry_price=entry_price,
            quantity=quantity,
            stop_loss=stop_loss,
            take_profit=take_profit,
            confidence=0.75,
            reasoning=f"Simulated {direction.value} trade",
        )
        
        trade = self.execute_trade(signal, regime=regime)
        
        if trade:
            self._close_trade(
                symbol=symbol,
                exit_price=exit_price,
                trigger="backtest",
                trigger_detail=f"Backtest simulation — held {holding_bars} bars",
            )
        
        return trade
