"""Position Sizer — คำนวณขนาดสถานะที่เหมาะสมตามทฤษฎี

รองรับ 4 วิธี:
- fixed_fractional: เปอร์เซ็นต์คงที่ของพอร์ต
- kelly: Kelly Criterion (full / half / quarter)
- risk_parity: กระจายความเสี่ยงเท่ากัน
- volatility_adjusted: ปรับตามความผันผวนของสินทรัพย์

Citations:
- Kelly Criterion: J.L. Kelly Jr., "A New Interpretation of Information Rate" (1956)
- Risk Parity: Edesess, M. et al., "The Real Lessons from the 2008 Crisis" (2009)
- Volatility Targeting: Morearno, J. et al., "Volatility-Based Risk Management" (2015)
"""
import numpy as np
from typing import Dict, Any, Optional, Literal
from dataclasses import dataclass


@dataclass
class PositionSizeResult:
    size: float              # ขนาดสถานะที่คำนวณได้
    method: str              # วิธีที่ใช้
    kelly_pct: Optional[float] = None    # Kelly fraction ที่คำนวณได้
    risk_amount: Optional[float] = None   # จำนวนเงินที่เสี่ยง
    max_size: Optional[float] = None      # ขนาดสูงสุดที่ allow
    reason: str = ""                       # เหตุผลที่ปรับลด/เพิ่ม


class PositionSizer:
    """
    คำนวณขนาดสถานะที่เหมาะสมสำหรับแต่ละ trade
    
    ใช้ได้ทั้ง crypto (BTC, ETH) และ gold (XAUUSD)
    โดยปรับความผันผวน (volatility) ตามสินทรัพย์นั้นๆ
    """

    def __init__(
        self,
        method: Literal["fixed_fractional", "kelly", "risk_parity", "volatility_adjusted"] = "kelly",
        kelly_variant: Literal["full", "half", "quarter"] = "half",
        portfolio_value: float = 100_000.0,
        max_risk_per_trade: float = 0.02,   # 2% ของพอร์ตต่อ trade
        max_position_pct: float = 0.10,      # 10% ของพอร์ตสูงสุดต่อสินทรัพย์
        asset_volatility: Optional[Dict[str, float]] = None,
    ):
        self.method = method
        self.kelly_variant = kelly_variant
        self.portfolio_value = portfolio_value
        self.max_risk_per_trade = max_risk_per_trade
        self.max_position_pct = max_position_pct
        
        # ความผันผวนรายปีของสินทรัพย์ (สำหรับ risk parity / volatility adjusted)
        # คำนวณจาก historical data หรือใช้ค่า approximate
        self.asset_volatility = asset_volatility or {
            "BTCUSDT": 0.70,    # 70% annual vol (crypto is volatile)
            "ETHUSDT": 0.85,
            "XAUUSD": 0.15,    # 15% annual vol (gold is stable)
            "BTC": 0.70,
            "ETH": 0.85,
            "XAU": 0.15,
            "default": 0.60,
        }
        
        # ประวัติ trades สำหรับคำนวณ Kelly
        self.trade_history: list[float] = []  # รายการ return ของแต่ละ trade

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def calculate(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: Optional[float] = None,
        confidence: float = 0.70,
        strategy_win_rate: Optional[float] = None,
        strategy_avg_win: Optional[float] = None,
        strategy_avg_loss: Optional[float] = None,
    ) -> PositionSizeResult:
        """
        คำนวณขนาดสถานะที่เหมาะสม
        
        Args:
            entry_price: ราคาเข้าเทรด
            stop_loss: ราคา stop loss (ถ้ามี)
            confidence: ความมั่นใจของ AI signal (0-1)
            strategy_win_rate: win rate ของระบบ (ถ้าทราบ)
            strategy_avg_win: กำไรเฉลี่ยต่อ trade (ถ้าทราบ)
            strategy_avg_loss: ขาดทุนเฉลี่ยต่อ trade (ถ้าทราบ)
        """
        # หา max position จาก max_position_pct
        max_by_pct = self.portfolio_value * self.max_position_pct
        
        # หา risk-based size จาก stop loss
        risk_amount = self.portfolio_value * self.max_risk_per_trade
        
        if self.method == "kelly":
            result = self._kelly_size(
                symbol, entry_price, stop_loss, risk_amount,
                confidence, strategy_win_rate, strategy_avg_win, strategy_avg_loss
            )
        elif self.method == "volatility_adjusted":
            result = self._volatility_adjusted_size(
                symbol, entry_price, stop_loss, risk_amount, confidence
            )
        elif self.method == "risk_parity":
            result = self._risk_parity_size(
                symbol, entry_price, stop_loss, risk_amount, confidence
            )
        else:
            result = self._fixed_fractional_size(
                symbol, entry_price, stop_loss, risk_amount, confidence
            )
        
        # Cap ด้วย max_position_pct
        if result.size > max_by_pct:
            result.size = max_by_pct
            result.reason += f" | Capped at {self.max_position_pct*100}% of portfolio"
        
        result.max_size = max_by_pct
        
        return result

    def update_portfolio_value(self, new_value: float):
        """อัปเดต portfolio value หลังจาก P&L เปลี่ยน"""
        self.portfolio_value = new_value

    def record_trade_result(self, return_pct: float):
        """
        บันทึกผล trade เพื่อใช้คำนวณ Kelly ครั้งต่อไป
        return_pct: ผลตอบแทนเป็น % เช่น 0.05 = +5%, -0.03 = -3%
        """
        self.trade_history.append(return_pct)
        # เก็บแค่ 100 trade ล่าสุด
        if len(self.trade_history) > 100:
            self.trade_history.pop(0)

    # ------------------------------------------------------------------ #
    # Method: Kelly Criterion
    # ------------------------------------------------------------------ #

    def _kelly_size(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: Optional[float],
        risk_amount: float,
        confidence: float,
        win_rate: Optional[float],
        avg_win: Optional[float],
        avg_loss: Optional[float],
    ) -> PositionSizeResult:
        """
        คำนวณขนาดสถานะด้วย Kelly Criterion
        
        Kelly % = W - (1-W) / R
        
        ปรับความเสี่ยงด้วย:
        - Kelly multiplier (full/half/quarter)
        - Confidence multiplier (confidence < 1 ลด size)
        """
        kelly_pct = None
        size = risk_amount  # fallback
        
        # วิธีที่ 1: ใช้ trade history
        if len(self.trade_history) >= 10 and win_rate is None:
            wins = [t for t in self.trade_history if t > 0]
            losses = [t for t in self.trade_history if t <= 0]
            
            if wins and losses:
                W = len(wins) / len(self.trade_history)
                avg_w = np.mean(wins)
                avg_l = abs(np.mean(losses))
                
                if avg_l > 0:
                    R = avg_w / avg_l
                    kelly_pct = W - (1 - W) / R
                    kelly_pct = max(0, kelly_pct)
        
        # วิธีที่ 2: ใช้ provided strategy stats
        elif win_rate is not None and avg_win is not None and avg_loss is not None:
            if avg_loss > 0:
                R = avg_win / avg_loss
                kelly_pct = win_rate - (1 - win_rate) / R
                kelly_pct = max(0, kelly_pct)
        
        # วิธีที่ 3: ใช้ confidence เป็น rough proxy
        if kelly_pct is None:
            # Conservative: ใช้ confidence เป็น rough win rate estimate
            # สมมติ R = 2 (risk/reward 2:1)
            R = 2.0
            W = confidence
            kelly_pct = max(0, W - (1 - W) / R)
        
        # Apply Kelly variant
        variant_multiplier = {
            "full": 1.0,
            "half": 0.5,
            "quarter": 0.25,
        }[self.kelly_variant]
        
        kelly_pct *= variant_multiplier
        
        # คำนวณ size จาก Kelly fraction
        if stop_loss and stop_loss != entry_price:
            risk_per_unit = abs(entry_price - stop_loss) / entry_price
            if risk_per_unit > 0:
                size = (kelly_pct * self.portfolio_value) / risk_per_unit
        else:
            # ไม่มี stop loss = ใช้ max_risk_per_trade
            size = kelly_pct * self.portfolio_value
        
        # Confidence adjustment: confidence ต่ำ = ลด size
        confidence_multiplier = max(0.3, confidence)  # สูงสุด = 1.0
        size *= confidence_multiplier
        
        reason = (
            f"Kelly {self.kelly_variant}={kelly_pct:.2%}"
            f" | conf={confidence:.0%}"
            f" | variant_mult={variant_multiplier}"
        )
        
        return PositionSizeResult(
            size=size,
            method="kelly",
            kelly_pct=kelly_pct,
            risk_amount=kelly_pct * self.portfolio_value,
            reason=reason,
        )

    # ------------------------------------------------------------------ #
    # Method: Volatility-Adjusted
    # ------------------------------------------------------------------ #

    def _volatility_adjusted_size(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: Optional[float],
        risk_amount: float,
        confidence: float,
    ) -> PositionSizeResult:
        """
        คำนวณขนาดสถานะโดยปรับตามความผันผวน
        
        หลักการ: สินทรัพย์ที่ผันผวนสูง = ขนาดเล็กลง
        สินทรัพย์ที่ผันผวนต่ำ = ขนาดใหญ่ขึ้น
        
        size = risk_amount / (volatility * 2)
        (คูณ 2 เพราะ daily vol ไม่ใช่ annual)
        """
        vol = self.asset_volatility.get(symbol, self.asset_volatility["default"])
        
        # แปลง annual vol เป็น daily (approx)
        daily_vol = vol / np.sqrt(365)
        
        # Base size
        base_size = risk_amount / max(daily_vol * 2, 0.001)
        
        # Confidence adjustment
        size = base_size * confidence
        
        reason = (
            f"vol_adj | vol={vol:.0%} (annual)"
            f" | daily_vol={daily_vol:.2%}"
            f" | conf={confidence:.0%}"
        )
        
        return PositionSizeResult(
            size=size,
            method="volatility_adjusted",
            risk_amount=risk_amount,
            reason=reason,
        )

    # ------------------------------------------------------------------ #
    # Method: Risk Parity
    # ------------------------------------------------------------------ #

    def _risk_parity_size(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: Optional[float],
        risk_amount: float,
        confidence: float,
    ) -> PositionSizeResult:
        """
        คำนวณขนาดสถานะให้ทุกสินทรัพย์มี risk contribution เท่ากัน
        
        Weight = (Target Risk / N) / Asset Volatility
        """
        vol = self.asset_volatility.get(symbol, self.asset_volatility["default"])
        
        # สมมติมี 3 สินทรัพย์
        n_assets = 3
        target_risk = 0.15  # 15% portfolio vol target
        
        equal_risk = target_risk / n_assets
        size = (equal_risk / vol) * self.portfolio_value * confidence
        
        reason = (
            f"risk_parity | vol={vol:.0%}"
            f" | equal_risk={equal_risk:.2%}"
            f" | conf={confidence:.0%}"
        )
        
        return PositionSizeResult(
            size=size,
            method="risk_parity",
            risk_amount=equal_risk * self.portfolio_value,
            reason=reason,
        )

    # ------------------------------------------------------------------ #
    # Method: Fixed Fractional
    # ------------------------------------------------------------------ #

    def _fixed_fractional_size(
        self,
        symbol: str,
        entry_price: float,
        stop_loss: Optional[float],
        risk_amount: float,
        confidence: float,
    ) -> PositionSizeResult:
        """
        คำนวณขนาดสถานะแบบ fixed fractional
        
        size = portfolio * max_risk_per_trade
        ปรับด้วย confidence
        """
        if stop_loss and stop_loss != entry_price:
            risk_per_unit = abs(entry_price - stop_loss) / entry_price
            if risk_per_unit > 0:
                size = risk_amount / risk_per_unit
                reason = f"fixed_frac | risk={risk_amount:.0f} | sl_risk={risk_per_unit:.2%}"
            else:
                size = risk_amount
                reason = f"fixed_frac | no SL, risk={risk_amount:.0f}"
        else:
            size = risk_amount
            reason = f"fixed_frac | no SL, risk={risk_amount:.0f}"
        
        size *= confidence
        
        return PositionSizeResult(
            size=size,
            method="fixed_fractional",
            risk_amount=risk_amount,
            reason=reason,
        )
