"""Trailing Stop — ราคาติดตามการเคลื่อนไหวของราคาเพื่อล็อกกำไร

รองรับ 3 วิธี:
- percentage: ใช้ % trail (เช่น 2% จาก high)
- atr: ใช้ ATR (Average True Range) ซึ่งปรับตัวตามความผันผวน
- fixed: ระยะห่างคงที่จาก high/low

Trailing stop จะเคลื่อนที่ขึ้นเรื่อยๆ สำหรับ LONG แต่ไม่เคลื่อนลง
เมื่อราคาวิ่งกลับมาแตะ trailing stop → ปิดสถานะ

Citations:
- Thomas Stridsman, "Trading Systems" (2000)
- Michael Choe, "A Practical Approach to Trailing Stops" (2015)
"""
from typing import Optional, Literal
from dataclasses import dataclass


@dataclass
class TrailingStopResult:
    triggered: bool
    exit_price: Optional[float]
    trailing_price: float        # ราคา stop ปัจจุบัน
    highest_price: float         # high ล่าสุด
    profit_locked_pct: float     # % กำไรที่ล็อกไว้
    reason: str = ""


class TrailingStop:
    """
    Trailing Stop สำหรับทั้ง LONG และ SHORT positions
    
    วิธีใช้:
        ts = TrailingStop(method="atr", atr_multiplier=2.0, atr_period=14)
        for price in price_series:
            result = ts.update(price)
            if result.triggered:
                close_position(result.exit_price)
    """

    def __init__(
        self,
        method: Literal["percentage", "atr", "fixed"] = "percentage",
        trail_pct: float = 0.02,       # 2% trailing distance
        atr_multiplier: float = 2.0,   # ATR multiplier (for ATR method)
        atr_period: int = 14,           # ATR lookback period
        fixed_distance: float = 0.005,  # Fixed distance (for fixed method)
        activation_pct: float = 0.01,  # เปิด trailing หลังราคาขยับ 1% เข้าทางที่ต้องการ
        min_locked_pct: float = 0.005, # ล็อกกำไรอย่างน้อย 0.5% ก่อนจะ trail
    ):
        self.method = method
        self.trail_pct = trail_pct
        self.atr_multiplier = atr_multiplier
        self.atr_period = atr_period
        self.fixed_distance = fixed_distance
        self.activation_pct = activation_pct
        self.min_locked_pct = min_locked_pct
        
        self.reset()

    def reset(self):
        """Reset trailing stop state"""
        self.direction: Optional[Literal["LONG", "SHORT"]] = None
        self.entry_price: float = 0.0
        self.trailing_price: float = 0.0
        self.breakeven_price: float = 0.0
        self.highest_price: float = 0.0
        self.lowest_price: float = 0.0
        self.activated: bool = False
        self.triggered: bool = False
        
        # ATR tracking
        self.trues: list[float] = []
        self.current_atr: float = 0.0
        
        # Profit tracking
        self.profit_locked_pct: float = 0.0

    def activate(self, direction: Literal["LONG", "SHORT"], entry_price: float):
        """
        เปิดใช้งาน trailing stop
        
        direction: LONG หรือ SHORT
        entry_price: ราคาเข้าเทรด
        """
        self.reset()
        self.direction = direction
        self.entry_price = entry_price
        
        if direction == "LONG":
            self.trailing_price = entry_price * (1 - self.trail_pct)
            self.breakeven_price = entry_price
        else:  # SHORT
            self.trailing_price = entry_price * (1 + self.trail_pct)
            self.breakeven_price = entry_price
        
        # Initialize ATR tracking
        self.highest_price = entry_price
        self.lowest_price = entry_price

    def update(self, current_price: float, high: float = None, low: float = None) -> TrailingStopResult:
        """
        อัปเดต trailing stop ทุกครั้งที่ได้ราคาใหม่
        
        Returns TrailingStopResult:
        - triggered=True: ถูก trailing stop แล้ว → ปิดสถานะ
        - triggered=False: ยังไม่ถูก → continue holding
        """
        if self.triggered or self.direction is None:
            return TrailingStopResult(
                triggered=self.triggered,
                exit_price=None,
                trailing_price=self.trailing_price,
                highest_price=self.highest_price,
                profit_locked_pct=self.profit_locked_pct,
                reason="Already triggered or not active",
            )
        
        # Update ATR if using that method
        if self.method == "atr":
            if high is not None and low is not None:
                self._update_atr(high, low)
        
        if self.direction == "LONG":
            return self._update_long(current_price, high or current_price)
        else:
            return self._update_short(current_price, low or current_price)

    def _update_long(self, current_price: float, high: float) -> TrailingStopResult:
        # Track highest price
        if high > self.highest_price:
            self.highest_price = high
        
        # Check if activation threshold met
        if not self.activated:
            gain_pct = (self.highest_price - self.entry_price) / self.entry_price
            if gain_pct >= self.activation_pct:
                self.activated = True
        
        if not self.activated:
            return TrailingStopResult(
                triggered=False,
                exit_price=None,
                trailing_price=self.trailing_price,
                highest_price=self.highest_price,
                profit_locked_pct=0.0,
                reason=f"Not activated yet: gain={((self.highest_price-self.entry_price)/self.entry_price):.2%}",
            )
        
        # Calculate new trailing price
        if self.method == "percentage":
            new_trailing = self.highest_price * (1 - self.trail_pct)
        elif self.method == "atr":
            new_trailing = self.highest_price - (self.current_atr * self.atr_multiplier)
        else:  # fixed
            new_trailing = self.highest_price - self.fixed_distance
        
        # Trailing stop moves UP only (never down)
        if new_trailing > self.trailing_price:
            self.trailing_price = new_trailing
        
        # Check breakeven
        self.breakeven_price = self.entry_price
        
        # Calculate locked profit
        self.profit_locked_pct = (self.trailing_price - self.entry_price) / self.entry_price
        
        # Check if price has pulled back to trailing stop
        if current_price <= self.trailing_price:
            self.triggered = True
            # Exit at trailing price (not at current price which might be lower)
            exit_price = self.trailing_price
            pnl_pct = (exit_price - self.entry_price) / self.entry_price
            return TrailingStopResult(
                triggered=True,
                exit_price=exit_price,
                trailing_price=self.trailing_price,
                highest_price=self.highest_price,
                profit_locked_pct=pnl_pct,
                reason=f"Trailing stop triggered @ {exit_price:.2f} (locked {pnl_pct:.2%})",
            )
        
        return TrailingStopResult(
            triggered=False,
            exit_price=None,
            trailing_price=self.trailing_price,
            highest_price=self.highest_price,
            profit_locked_pct=self.profit_locked_pct,
            reason=f"Trailing: {self.trailing_price:.2f} | High: {self.highest_price:.2f}",
        )

    def _update_short(self, current_price: float, low: float) -> TrailingStopResult:
        # Track lowest price
        if low < self.lowest_price:
            self.lowest_price = low
        
        if not self.activated:
            gain_pct = (self.entry_price - self.lowest_price) / self.entry_price
            if gain_pct >= self.activation_pct:
                self.activated = True
        
        if not self.activated:
            return TrailingStopResult(
                triggered=False,
                exit_price=None,
                trailing_price=self.trailing_price,
                highest_price=self.lowest_price,
                profit_locked_pct=0.0,
                reason=f"Not activated yet",
            )
        
        # Calculate new trailing price (for SHORT, it moves DOWN)
        if self.method == "percentage":
            new_trailing = self.lowest_price * (1 + self.trail_pct)
        elif self.method == "atr":
            new_trailing = self.lowest_price + (self.current_atr * self.atr_multiplier)
        else:  # fixed
            new_trailing = self.lowest_price + self.fixed_distance
        
        # Trailing stop moves DOWN only (never up) for SHORT
        if new_trailing < self.trailing_price:
            self.trailing_price = new_trailing
        
        self.breakeven_price = self.entry_price
        
        self.profit_locked_pct = (self.entry_price - self.trailing_price) / self.entry_price
        
        if current_price >= self.trailing_price:
            self.triggered = True
            exit_price = self.trailing_price
            pnl_pct = (self.entry_price - exit_price) / self.entry_price
            return TrailingStopResult(
                triggered=True,
                exit_price=exit_price,
                trailing_price=self.trailing_price,
                highest_price=self.lowest_price,
                profit_locked_pct=pnl_pct,
                reason=f"Trailing stop triggered @ {exit_price:.2f} (locked {pnl_pct:.2%})",
            )
        
        return TrailingStopResult(
            triggered=False,
            exit_price=None,
            trailing_price=self.trailing_price,
            highest_price=self.lowest_price,
            profit_locked_pct=self.profit_locked_pct,
            reason=f"Trailing: {self.trailing_price:.2f} | Low: {self.lowest_price:.2f}",
        )

    def _update_atr(self, high: float, low: float):
        """Update ATR using True Range calculation"""
        if self.current_atr == 0:
            # Initialize with first values
            self.current_atr = high - low
            self.trues = [high - low]
        else:
            tr = max(
                high - low,
                abs(high - (self.trues[-1] if self.trues else low)),
                abs(low - (self.trues[-1] if self.trues else high)),
            )
            self.trues.append(tr)
            if len(self.trues) > self.atr_period:
                self.trues.pop(0)
            self.current_atr = sum(self.trues) / len(self.trues)

    def get_status(self) -> dict:
        """สถานะปัจจุบันของ trailing stop"""
        return {
            "direction": self.direction,
            "entry_price": self.entry_price,
            "trailing_price": self.trailing_price,
            "highest_price": self.highest_price,
            "lowest_price": self.lowest_price,
            "activated": self.activated,
            "triggered": self.triggered,
            "profit_locked_pct": f"{self.profit_locked_pct:.2%}" if self.profit_locked_pct else "0.00%",
            "atr_current": self.current_atr,
            "method": self.method,
        }
