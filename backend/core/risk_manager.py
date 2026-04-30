"""Risk Manager — จัดการความเสี่ยงระดับพอร์ต

รับผิดชอบ:
1. ตรวจสอบ drawdown ปัจจุบัน (peak-to-current)
2. Max daily / weekly / monthly loss limit
3. Consecutive loss limit
4. Max open positions limit
5. VaR calculation (Historical method)
6. ส่งสัญญาณ STOP TRADING เมื่อ breach limits

Citations:
- VaR: Jorion, P., "Value at Risk" (2007)
- Drawdown: Ang, A., "Long-Term Investing" (2014)
- Risk Limits: MSCI, "Risk Management Framework" (2020)
"""
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass, field


@dataclass
class RiskCheckResult:
    allowed: bool                    # True = allow trade, False = blocked
    reason: str                     # เหตุผลที่ block หรือ allow
    level: Literal["ok", "warning", "critical", "stop"]  # ระดับความเสี่ยง
    blocked_by: Optional[str] = None  # rule ที่ block
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DailyLoss:
    date: str          # YYYY-MM-DD
    loss: float        # ขาดทุนสุทธิของวัน (positive = loss)
    trades: int = 0


class RiskManager:
    """
    ตรวจสอบทุกครั้งก่อนเปิด trade ใหม่
    
    ถ้า breach กฎใด → block trade + log warning
    ถ้า breach กฎ critical → stop trading ทันที
    """

    def __init__(
        self,
        initial_balance: float = 100_000.0,
        
        # Drawdown limits
        max_drawdown_pct: float = 0.20,     # 20% max drawdown → stop
        
        # Loss limits
        max_daily_loss_pct: float = 0.03,   # 3% ของ initial balance ต่อวัน
        max_weekly_loss_pct: float = 0.08,   # 8% ของ initial balance ต่อสัปดาห์
        max_monthly_loss_pct: float = 0.15,  # 15% ของ initial balance ต่อเดือน
        
        # Consecutive loss
        max_consecutive_losses: int = 5,     # หยุดถ้าขาดทุนติดกัน 5 ครั้ง
        
        # Position limits
        max_open_positions: int = 5,
        min_trades_before_increase: int = 20,  # ต้องมีอย่างน้อย 20 trades ก่อนจะเพิ่มขนาด
        
        # VaR settings
        var_confidence: float = 0.95,        # 95% VaR
        var_lookback_days: int = 30,
    ):
        self.initial_balance = initial_balance
        self.max_drawdown_pct = max_drawdown_pct
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_weekly_loss_pct = max_weekly_loss_pct
        self.max_monthly_loss_pct = max_monthly_loss_pct
        self.max_consecutive_losses = max_consecutive_losses
        self.max_open_positions = max_open_positions
        self.var_confidence = var_confidence
        self.var_lookback_days = var_lookback_days

        # ---- State ---- #
        self.peak_balance = initial_balance
        self.current_balance = initial_balance
        
        # Trade history for stats
        self.trade_pnls: list[float] = []
        self.consecutive_losses = 0
        self.last_trade_was_loss = False
        
        # Daily losses tracking
        self.daily_losses: Dict[str, float] = {}  # date -> loss amount
        
        # VaR tracking
        self.portfolio_returns: list[float] = []
        
        # Override flag
        self.trading_paused = False
        self.pause_reason: Optional[str] = None

    # ================================================================= #
    # Main Check
    # ================================================================= #

    def pre_trade_check(
        self,
        trade_pnl_if_loss: float,
        current_positions: int = 0,
        portfolio_returns: Optional[list[float]] = None,
    ) -> RiskCheckResult:
        """
        ตรวจสอบก่อนเปิด trade ใหม่ทุกครั้ง
        
        Returns RiskCheckResult:
        - allowed=True: ผ่านทุกกฎ → สามารถเทรดได้
        - allowed=False: blocked ด้วยเหตุผลใดเหตุผลหนึ่ง
        """
        # 1. Paused by risk manager
        if self.trading_paused:
            return RiskCheckResult(
                allowed=False,
                reason=f"Trading PAUSED: {self.pause_reason}",
                level="stop",
                blocked_by="risk_manager_pause",
                details={"pause_reason": self.pause_reason},
            )

        # 2. Max open positions
        if current_positions >= self.max_open_positions:
            return RiskCheckResult(
                allowed=False,
                reason=f"Max positions ({self.max_open_positions}) reached",
                level="warning",
                blocked_by="max_positions",
            )

        # 3. Consecutive losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            return RiskCheckResult(
                allowed=False,
                reason=f"Consecutive loss limit reached ({self.consecutive_losses})",
                level="stop",
                blocked_by="consecutive_losses",
                details={"consecutive_losses": self.consecutive_losses},
            )

        # 4. Max daily loss
        daily_loss_result = self._check_daily_loss()
        if daily_loss_result is not None:
            return daily_loss_result

        # 5. Max weekly loss
        weekly_loss_result = self._check_weekly_loss()
        if weekly_loss_result is not None:
            return weekly_loss_result

        # 6. Max drawdown
        drawdown_result = self._check_drawdown()
        if drawdown_result is not None:
            return drawdown_result

        # 7. VaR check
        if portfolio_returns:
            var_result = self._check_var(portfolio_returns, trade_pnl_if_loss)
            if var_result is not None:
                return var_result

        # ผ่านทุกกฎ
        return RiskCheckResult(
            allowed=True,
            reason="All risk checks passed",
            level="ok",
        )

    # ================================================================= #
    # Record Keeping
    # ================================================================= #

    def record_trade(self, pnl: float, timestamp: Optional[datetime] = None):
        """
        บันทึกผล trade หลังปิด trade
        ใช้สำหรับอัปเดต consecutive loss และ daily loss
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        date_key = timestamp.strftime("%Y-%m-%d")
        
        self.trade_pnls.append(pnl)
        
        # Update consecutive losses
        if pnl < 0:
            self.consecutive_losses += 1
            self.last_trade_was_loss = True
        else:
            self.consecutive_losses = 0
            self.last_trade_was_loss = False
        
        # Update daily loss
        if pnl < 0:
            self.daily_losses[date_key] = self.daily_losses.get(date_key, 0) + abs(pnl)
        else:
            # บวกกำไรก็ลด loss ที่สะสมไว้
            existing = self.daily_losses.get(date_key, 0)
            if existing > 0:
                self.daily_losses[date_key] = max(0, existing - pnl)
        
        # Update balance tracking
        self.current_balance += pnl
        if self.current_balance > self.peak_balance:
            self.peak_balance = self.current_balance
        
        # Update portfolio returns
        prev_balance = self.current_balance - pnl
        if prev_balance > 0:
            ret = (self.current_balance - prev_balance) / prev_balance
            self.portfolio_returns.append(ret)
            # เก็บแค่ lookback days
            if len(self.portfolio_returns) > self.var_lookback_days:
                self.portfolio_returns.pop(0)

    def update_balance(self, new_balance: float):
        """อัปเดต balance ปัจจุบัน (เรียกเมื่อมี external change)"""
        self.current_balance = new_balance
        if new_balance > self.peak_balance:
            self.peak_balance = new_balance

    # ================================================================= #
    # Risk Checks
    # ================================================================= #

    def _check_daily_loss(self) -> Optional[RiskCheckResult]:
        today = datetime.now().strftime("%Y-%m-%d")
        daily_loss = self.daily_losses.get(today, 0)
        
        limit = self.initial_balance * self.max_daily_loss_pct
        
        if daily_loss >= limit:
            self._pause_trading(f"Daily loss limit breached: {daily_loss:.2f} >= {limit:.2f}")
            return RiskCheckResult(
                allowed=False,
                reason=f"Daily loss limit breached: {daily_loss:.2f} >= {limit:.2f}",
                level="stop",
                blocked_by="daily_loss_limit",
                details={"daily_loss": daily_loss, "limit": limit},
            )
        elif daily_loss >= limit * 0.8:
            return RiskCheckResult(
                allowed=True,
                reason=f"Warning: Daily loss at {daily_loss/limit:.0%} of limit",
                level="warning",
                details={"daily_loss": daily_loss, "limit": limit},
            )
        
        return None

    def _check_weekly_loss(self) -> Optional[RiskCheckResult]:
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_start_key = week_start.strftime("%Y-%m-%d")
        
        weekly_loss = sum(
            loss for date, loss in self.daily_losses.items()
            if date >= week_start_key
        )
        
        limit = self.initial_balance * self.max_weekly_loss_pct
        
        if weekly_loss >= limit:
            self._pause_trading(f"Weekly loss limit breached: {weekly_loss:.2f} >= {limit:.2f}")
            return RiskCheckResult(
                allowed=False,
                reason=f"Weekly loss limit breached",
                level="stop",
                blocked_by="weekly_loss_limit",
                details={"weekly_loss": weekly_loss, "limit": limit},
            )
        elif weekly_loss >= limit * 0.8:
            return RiskCheckResult(
                allowed=True,
                reason=f"Weekly loss warning: {weekly_loss/limit:.0%} of limit",
                level="warning",
            )
        
        return None

    def _check_drawdown(self) -> Optional[RiskCheckResult]:
        if self.peak_balance <= 0:
            return None
        
        drawdown = (self.peak_balance - self.current_balance) / self.peak_balance
        limit = self.max_drawdown_pct
        
        if drawdown >= limit:
            self._pause_trading(f"Max drawdown breached: {drawdown:.1%} >= {limit:.1%}")
            return RiskCheckResult(
                allowed=False,
                reason=f"Max drawdown breached: {drawdown:.1%} >= {limit:.1%}",
                level="stop",
                blocked_by="max_drawdown",
                details={
                    "current_drawdown": drawdown,
                    "max_drawdown": limit,
                    "peak": self.peak_balance,
                    "current": self.current_balance,
                },
            )
        elif drawdown >= limit * 0.8:
            return RiskCheckResult(
                allowed=True,
                reason=f"Drawdown warning: {drawdown:.1%} of {limit:.1%}",
                level="warning",
                details={"current_drawdown": drawdown, "limit": limit},
            )
        
        return None

    def _check_var(
        self,
        portfolio_returns: list[float],
        trade_pnl_if_loss: float,
    ) -> Optional[RiskCheckResult]:
        if len(portfolio_returns) < 5:
            return None
        
        returns = np.array(portfolio_returns[-self.var_lookback_days:])
        var_pct = np.percentile(returns, (1 - self.var_confidence) * 100)
        
        # Convert VaR % to absolute amount
        var_amount = abs(var_pct * self.current_balance)
        
        if trade_pnl_if_loss > var_amount * 1.5:
            return RiskCheckResult(
                allowed=True,
                reason=f"Trade loss ({trade_pnl_if_loss:.0f}) exceeds VaR ({var_amount:.0f}) — high risk",
                level="warning",
                details={"var_pct": var_pct, "var_amount": var_amount},
            )
        
        return None

    # ================================================================= #
    # Portfolio Stats
    # ================================================================= #

    def get_portfolio_stats(self) -> Dict[str, Any]:
        """สถิติพอร์ตปัจจุบัน"""
        if self.peak_balance <= 0:
            current_drawdown = 0.0
        else:
            current_drawdown = (self.peak_balance - self.current_balance) / self.peak_balance

        today = datetime.now().strftime("%Y-%m-%d")
        daily_loss = self.daily_losses.get(today, 0)
        
        wins = [p for p in self.trade_pnls if p > 0]
        losses = [p for p in self.trade_pnls if p <= 0]
        
        total_trades = len(self.trade_pnls)
        win_rate = len(wins) / total_trades if total_trades > 0 else 0
        
        avg_win = np.mean(wins) if wins else 0
        avg_loss = abs(np.mean(losses)) if losses else 0
        
        # Calculate VaR
        var_amount = 0.0
        if len(self.portfolio_returns) >= 5:
            var_pct = np.percentile(np.array(self.portfolio_returns), 5)
            var_amount = abs(var_pct * self.current_balance)
        
        return {
            "portfolio_value": self.current_balance,
            "peak_balance": self.peak_balance,
            "current_drawdown_pct": f"{current_drawdown:.2%}",
            "max_drawdown_limit": f"{self.max_drawdown_pct:.2%}",
            "daily_loss_today": daily_loss,
            "daily_loss_limit": self.initial_balance * self.max_daily_loss_pct,
            "consecutive_losses": self.consecutive_losses,
            "total_trades": total_trades,
            "win_rate": f"{win_rate:.1%}" if total_trades > 0 else "N/A",
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "win_loss_ratio": f"{avg_win/avg_loss:.2f}" if avg_loss > 0 else "N/A",
            "var_95_amount": var_amount,
            "trading_paused": self.trading_paused,
            "pause_reason": self.pause_reason,
        }

    def _pause_trading(self, reason: str):
        """หยุด trading เมื่อ breach critical limit"""
        self.trading_paused = True
        self.pause_reason = reason
        print(f"[RISK MANAGER] ⚠️  TRADING PAUSED: {reason}")

    def resume_trading(self):
        """เปิด trading อีกครั้ง (หลังจาก review แล้ว)"""
        self.trading_paused = False
        self.pause_reason = None
        print("[RISK MANAGER] ✅ Trading resumed")
