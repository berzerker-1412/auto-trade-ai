"""AutoTrader — ระบบเทรดอัตโนมัติที่รวมทุก component เข้าด้วยกัน

การทำงาน:
1. Regime Detection → เลือก strategy ที่เหมาะสม
2. AI Signal Generation → สร้างสัญญาณจาก MiniMax
3. Risk Check → RiskManager ตรวจก่อนเทรด
4. Position Sizing → PositionSizer คำนวณขนาด
5. Execute → Trader เปิดสถานะ
6. Monitor → TrailingStop ติดตาม + PortfolioMonitor วิเคราะห์
7. Record → บันทึกผลเข้า RiskManager + PositionSizer

Usage:
    auto_trader = AutoTrader(initial_balance=100_000)
    auto_trader.run()  # รัน loop หลัก

    # หรือเรียกทีละ step:
    regime = auto_trader.detect_regime(prices)
    signal = auto_trader.generate_signal(symbol, market_data, regime)
    if auto_trader.pre_trade_check(signal):
        auto_trader.execute_trade(signal)
"""
import asyncio
from datetime import datetime
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field

from .models import TradeSignal, Trade, TradeStatus, TradeDirection, AssetType, WalletType
from .trader import Trader
from .wallet_manager import WalletManager
from .position_sizer import PositionSizer
from .risk_manager import RiskManager, RiskCheckResult
from .trailing_stop import TrailingStop
from .regime_detector import RegimeDetector, MarketRegime
from .portfolio_monitor import PortfolioMonitor, PortfolioRiskReport


@dataclass
class AutoTraderConfig:
    """Configuration for AutoTrader"""
    # Position sizing
    sizing_method: str = "kelly"              # kelly / volatility_adjusted / risk_parity / fixed_fractional
    kelly_variant: str = "half"              # full / half / quarter
    max_risk_per_trade: float = 0.02          # 2% per trade
    max_position_pct: float = 0.10            # 10% max per position
    
    # Risk limits
    max_drawdown_pct: float = 0.20            # 20% max drawdown
    max_daily_loss_pct: float = 0.03          # 3% daily loss limit
    max_weekly_loss_pct: float = 0.08         # 8% weekly loss limit
    max_consecutive_losses: int = 5            # Stop after 5 consecutive losses
    
    # Trailing stop
    trailing_method: str = "percentage"       # percentage / atr / fixed
    trailing_pct: float = 0.02                # 2% trailing
    trailing_activation_pct: float = 0.01     # Activate after 1% profit
    
    # Regime detection
    regime_detection_enabled: bool = True
    
    # Execution
    loop_interval_seconds: int = 60           # Main loop interval
    confidence_threshold: float = 0.70        # AI confidence threshold


@dataclass
class TradeWithExtras:
    """Trade ที่มี trailing stop + metadata"""
    trade: Trade
    trailing_stop: Optional[TrailingStop] = None
    regime_at_entry: Optional[MarketRegime] = None
    sizing_result: Optional[Any] = None


class AutoTrader:
    """
    AutoTrader — ระบบเทรดอัตโนมัติที่รวมทุก component
    
    Components ที่รวม:
    - Trader: execution engine
    - PositionSizer: คำนวณขนาดสถานะ
    - RiskManager: ตรวจสอบความเสี่ยงก่อนเทรด
    - TrailingStop: ติดตามและล็อกกำไร
    - RegimeDetector: ตรวจจับ market regime
    - PortfolioMonitor: วิเคราะห์ความเสี่ยงพอร์ต
    """

    def __init__(
        self,
        initial_balance: float = 100_000.0,
        config: Optional[AutoTraderConfig] = None,
        db_path: str = "data/trades.db",
    ):
        self.config = config or AutoTraderConfig()
        
        # Core components
        self.wallet_manager = WalletManager(
            paper_initial=initial_balance,
            paper_currency="USDT",
        )
        self.trader = Trader(
            wallet_manager=self.wallet_manager,
            db_path=db_path,
            wallet_type=WalletType.PAPER,
        )
        
        # Risk & sizing
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
        
        # Market analysis
        self.regime_detector = RegimeDetector()
        self.portfolio_monitor = PortfolioMonitor(portfolio_value=initial_balance)
        
        # Active trades with trailing stops
        self.active_trades: Dict[str, TradeWithExtras] = {}
        
        # Stats
        self.initial_balance = initial_balance

    # ================================================================= #
    # Pre-Trade Pipeline
    # ================================================================= #

    def pre_trade_check(self, signal: TradeSignal) -> RiskCheckResult:
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
        
        # Step 1: Calculate position size
        sizing = self.position_sizer.calculate(
            symbol=signal.symbol,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
            confidence=signal.confidence,
        )
        
        # Override signal quantity with calculated size
        # Convert from notional to quantity
        if signal.entry_price > 0:
            signal.quantity = sizing.size / signal.entry_price
        
        # Step 2: Risk check
        trade_value = signal.quantity * signal.entry_price
        loss_if_wrong = trade_value * self.config.max_risk_per_trade
        
        result = self.risk_manager.pre_trade_check(
            trade_pnl_if_loss=loss_if_wrong,
            current_positions=len(self.active_trades),
        )
        
        # Attach sizing result
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
    ) -> Optional[Trade]:
        """
        Execute trade หลังจากผ่าน pre_trade_check แล้ว
        """
        # Calculate sizing
        sizing = self.position_sizer.calculate(
            symbol=signal.symbol,
            entry_price=signal.entry_price,
            stop_loss=signal.stop_loss,
            confidence=signal.confidence,
        )
        
        # Override quantity
        signal.quantity = sizing.size / signal.entry_price if signal.entry_price > 0 else sizing.size
        
        # Execute via trader
        trade = self.trader.execute_signal(signal)
        
        if trade is None:
            return None
        
        # Setup trailing stop
        trailing = TrailingStop(
            method=self.config.trailing_method,
            trail_pct=self.config.trailing_pct,
            activation_pct=self.config.trailing_activation_pct,
        )
        direction = "LONG" if signal.direction == TradeDirection.BUY else "SHORT"
        trailing.activate(direction=direction, entry_price=signal.entry_price)
        
        # Track with extras
        self.active_trades[signal.symbol] = TradeWithExtras(
            trade=trade,
            trailing_stop=trailing,
            regime_at_entry=regime,
            sizing_result=sizing,
        )
        
        # Add to portfolio monitor
        self.portfolio_monitor.add_position(
            symbol=signal.symbol,
            size=sizing.size,
            entry_price=signal.entry_price,
        )
        
        # Update portfolio value in position sizer
        self.position_sizer.update_portfolio_value(self.trader.wallet.balance)
        
        return trade

    # ================================================================= #
    # Monitor & Update
    # ================================================================= #

    def update_prices(self, price_updates: Dict[str, float]):
        """
        อัปเดตราคาปัจจุบัน + ตรวจ trailing stop
        
        เรียกทุก tick หรือทุก interval
        """
        closed = []
        
        for symbol, current_price in price_updates.items():
            if symbol not in self.active_trades:
                continue
            
            trade_extras = self.active_trades[symbol]
            trailing = trade_extras.trailing_stop
            
            # Update portfolio monitor
            self.portfolio_monitor.update_position_price(symbol, current_price)
            
            # Check trailing stop
            if trailing:
                result = trailing.update(current_price)
                
                if result.triggered:
                    self._close_trade(symbol, result.exit_price, "trailing_stop")
                    closed.append(symbol)
                    continue
            
            # Check SL/TP via trader
            sl_result = self.trader.check_stop_loss_take_profit(symbol, current_price)
            if sl_result:
                self._close_trade(symbol, sl_result.exit_price, sl_result.status.value)
                closed.append(symbol)

    def _close_trade(
        self,
        symbol: str,
        exit_price: float,
        reason: str,
    ):
        """Helper: ปิด trade + อัปเดตทุก component"""
        if symbol not in self.active_trades:
            return
        
        trade_extras = self.active_trades[symbol]
        trade = trade_extras.trade
        
        # Close via trader
        closed_trade = self.trader.close_trade(symbol, exit_price, reason)
        
        if closed_trade:
            pnl = closed_trade.pnl
            
            # Record to position sizer (for Kelly)
            if closed_trade.quantity > 0 and closed_trade.entry_price > 0:
                return_pct = pnl / (closed_trade.quantity * closed_trade.entry_price)
                self.position_sizer.record_trade_result(return_pct)
            
            # Record to risk manager
            self.risk_manager.record_trade(pnl)
            
            # Update portfolio monitor
            self.portfolio_monitor.remove_position(symbol)
            
            # Update portfolio value
            self.position_sizer.update_portfolio_value(self.trader.wallet.balance)
        
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
        """สถานะระบบทั้งหมด = ready-to-display"""
        risk_stats = self.risk_manager.get_portfolio_stats()
        portfolio_report = self.portfolio_monitor.generate_report()
        
        # Active positions summary
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
    # Persistence / Serialization
    # ================================================================= #

    def save_state(self, path: str = "data/autotrader_state.json"):
        """บันทึกสถานะระบบ (optional)"""
        import json
        
        state = {
            "initial_balance": self.initial_balance,
            "current_balance": self.trader.wallet.balance,
            "config": {
                "sizing_method": self.config.sizing_method,
                "max_risk_per_trade": self.config.max_risk_per_trade,
                "max_position_pct": self.config.max_position_pct,
                "max_drawdown_pct": self.config.max_drawdown_pct,
            },
            "risk_paused": self.risk_manager.trading_paused,
            "consecutive_losses": self.risk_manager.consecutive_losses,
        }
        
        with open(path, "w") as f:
            json.dump(state, f, indent=2)
        
        return state
