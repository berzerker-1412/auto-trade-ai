"""Regime Detector — ตรวจจับ market regime เพื่อเลือกกลยุทธ์ที่เหมาะสม

Market Regime:
- TRENDING: ราคาเคลื่อนไหวเป็นแนวโน้มชัดเจน → ใช้ momentum strategies
- RANGING: ราคาแกว่งในกรอบ → ใช้ mean reversion strategies
- VOLATILE: ความผันผวนสูงมาก → ลดขนาด หรือ ออก
- CRASH: ราคาร่วงแรง → risk-off, ไม่เปิด long

การใช้งาน:
    detector = RegimeDetector()
    
    # วิเคราะห์ทุกครั้งที่ได้ OHLCV data ใหม่
    regime = detector.detect(prices, volumes)
    
    if regime.name == "TRENDING":
        strategy = momentum_strategy  # trend-following
    elif regime.name == "RANGING":
        strategy = mean_reversion_strategy  # mean reversion
    else:
        strategy = None  # ไม่เทรดในช่วง volatile/crash

Indicators ใช้:
- ADX (Average Directional Index): วัดความแข็งแกร่งของ trend
- Bollinger Band Width: วัดความกว้างของ bands → volatility
- ATR: Average True Range → volatility
- Returns distribution: skewness → crash detection

Citations:
- ADX: J. Welles Wilder, "New Concepts in Technical Trading" (1978)
- Regime Switching: Ang & Timmermann, "Regime Changes and Financial Markets" (2012)
"""
import numpy as np
from typing import Optional, List, Literal
from dataclasses import dataclass


@dataclass
class MarketRegime:
    name: Literal["TRENDING", "RANGING", "VOLATILE", "CRASH", "UNKNOWN"]
    adx: float                          # 0-100, >25 = trending
    atr_pct: float                      # ATR as % of price
    bb_width: float                     # Bollinger bandwidth (volatility)
    trend_strength: float               # 0-1, normalized ADX
    confidence: float                   # 0-1, confidence in regime detection
    recommended_strategy: str           # "momentum" | "mean_reversion" | "none"
    reason: str                         # เหตุผลที่ตรวจจับได้


class RegimeDetector:
    """
    ตรวจจับ market regime จาก price/volume data
    
    ใช้ได้กับทั้ง crypto และ gold
    """

    def __init__(
        self,
        adx_period: int = 14,
        atr_period: int = 14,
        bb_period: int = 20,
        bb_std: float = 2.0,
        # Thresholds
        adx_trending_threshold: float = 25.0,
        adx_strong_threshold: float = 40.0,
        atr_volatile_threshold: float = 0.03,   # 3% daily ATR
        bb_volatile_threshold: float = 0.10,    # 10% BB width
        crash_threshold: float = -0.05,          # -5% intraday = potential crash
    ):
        self.adx_period = adx_period
        self.atr_period = atr_period
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.adx_trending_threshold = adx_trending_threshold
        self.adx_strong_threshold = adx_strong_threshold
        self.atr_volatile_threshold = atr_volatile_threshold
        self.bb_volatile_threshold = bb_volatile_threshold
        self.crash_threshold = crash_threshold
        
        self._cache: dict = {}

    def detect(
        self,
        prices: List[float],
        highs: Optional[List[float]] = None,
        lows: Optional[List[float]] = None,
        volumes: Optional[List[float]] = None,
    ) -> MarketRegime:
        """
        วิเคราะห์ price series แล้ว return market regime
        
        Args:
            prices: list of closing prices
            highs: list of high prices (optional)
            lows: list of low prices (optional)
            volumes: list of volume (optional)
        
        Returns:
            MarketRegime with name, indicators, and recommended strategy
        """
        if len(prices) < max(self.adx_period, self.bb_period, self.atr_period) + 1:
            return MarketRegime(
                name="UNKNOWN",
                adx=0, atr_pct=0, bb_width=0, trend_strength=0,
                confidence=0,
                recommended_strategy="none",
                reason="Insufficient data",
            )
        
        prices = np.array(prices)
        
        # Calculate indicators
        adx = self._calculate_adx(prices, highs, lows)
        atr_pct = self._calculate_atr_pct(prices, highs, lows)
        bb_width = self._calculate_bb_width(prices)
        
        # Normalize trend strength (0-1)
        trend_strength = min(adx / 60.0, 1.0)  # ADX 60 = max
        
        # Calculate crash signal
        returns = np.diff(prices) / prices[:-1]
        recent_return = returns[-1] if len(returns) > 0 else 0
        drawdown = self._calculate_drawdown(prices)
        
        # Determine regime
        if drawdown > 0.15 or recent_return < self.crash_threshold:
            # Either sharp drawdown or big intraday drop
            confidence = min(abs(drawdown) * 3, 1.0)
            regime = MarketRegime(
                name="CRASH",
                adx=adx,
                atr_pct=atr_pct,
                bb_width=bb_width,
                trend_strength=trend_strength,
                confidence=confidence,
                recommended_strategy="none",
                reason=f"Crash detected: drawdown={drawdown:.1%}, return={recent_return:.2%}",
            )
        
        elif atr_pct > self.atr_volatile_threshold or bb_width > self.bb_volatile_threshold:
            confidence = min(atr_pct / 0.06, 1.0)
            regime = MarketRegime(
                name="VOLATILE",
                adx=adx,
                atr_pct=atr_pct,
                bb_width=bb_width,
                trend_strength=trend_strength,
                confidence=confidence,
                recommended_strategy="none",
                reason=f"High volatility: ATR={atr_pct:.2%}, BB_width={bb_width:.2%}",
            )
        
        elif adx > self.adx_trending_threshold:
            if adx > self.adx_strong_threshold:
                confidence = min((adx - 25) / 35, 1.0)
                strategy = "momentum"
                reason = f"Strong trend: ADX={adx:.1f} > {self.adx_strong_threshold}"
            else:
                confidence = min((adx - 15) / 25, 1.0)
                strategy = "momentum"
                reason = f"Trending: ADX={adx:.1f} > {self.adx_trending_threshold}"
            
            regime = MarketRegime(
                name="TRENDING",
                adx=adx,
                atr_pct=atr_pct,
                bb_width=bb_width,
                trend_strength=trend_strength,
                confidence=confidence,
                recommended_strategy=strategy,
                reason=reason,
            )
        
        else:
            confidence = min((30 - adx) / 30, 1.0) if adx < 30 else 0.3
            regime = MarketRegime(
                name="RANGING",
                adx=adx,
                atr_pct=atr_pct,
                bb_width=bb_width,
                trend_strength=trend_strength,
                confidence=confidence,
                recommended_strategy="mean_reversion",
                reason=f"Ranging: ADX={adx:.1f} < {self.adx_trending_threshold}",
            )
        
        return regime

    def _calculate_adx(
        self,
        prices: np.ndarray,
        highs: Optional[List[float]],
        lows: Optional[List[float]],
    ) -> float:
        """
        คำนวณ ADX (Average Directional Index)
        
        ADX > 25 = trending
        ADX > 40 = strong trend
        ADX < 20 = ranging/sideways
        """
        if highs is None or lows is None:
            # Approximate from close prices
            returns = np.diff(prices) / prices[:-1]
            plus_dm = np.maximum(returns, 0)
            minus_dm = np.maximum(-returns, 0)
        else:
            highs = np.array(highs)
            lows = np.array(lows)
            high_diff = np.diff(highs)
            low_diff = np.diff(lows)
            
            plus_dm = np.maximum(high_diff - np.roll(low_diff, 1), 0)
            minus_dm = np.maximum(np.roll(low_diff, 1) - high_diff, 0)
        
        plus_dm = np.clip(plus_dm, 0, None)
        minus_dm = np.clip(minus_dm, 0, None)
        
        # Smooth with EMA
        period = self.adx_period
        if len(plus_dm) < period:
            return 25.0
        
        plus_di = self._ema(plus_dm[-period:], period)
        minus_di = self._ema(minus_dm[-period:], period)
        
        di_sum = plus_di + minus_di
        if di_sum == 0:
            return 25.0
        
        dx = 100 * abs(plus_di - minus_di) / di_sum
        
        # ADX = smoothed DX over period
        adx = self._ema(np.array([dx]), period)[-1] if isinstance(dx, (int, float)) else dx
        
        if np.isnan(adx):
            return 25.0
        
        return float(adx)

    def _calculate_atr_pct(
        self,
        prices: np.ndarray,
        highs: Optional[List[float]],
        lows: Optional[List[float]],
    ) -> float:
        """ATR เป็น % ของราคาปัจจุบัน"""
        period = min(self.atr_period, len(prices) - 1)
        if period < 1:
            return 0.0
        
        if highs is not None and lows is not None:
            highs = np.array(highs)
            lows = np.array(lows)
            prev_close = prices[-period-1:-1]
            tr = np.maximum(
                highs[-period:] - lows[-period:],
                np.maximum(
                    abs(highs[-period:] - prev_close),
                    abs(lows[-period:] - prev_close)
                )
            )
        else:
            # Simplified TR from close prices
            tr = np.abs(np.diff(prices[-period-1:]))
        
        atr = np.mean(tr)
        current_price = prices[-1]
        
        if current_price == 0:
            return 0.0
        
        return float(atr / current_price)

    def _calculate_bb_width(self, prices: np.ndarray) -> float:
        """
        Bollinger Band Width เป็น % ของราคา
        
        BB Width = (Upper Band - Lower Band) / Middle Band
        
        High BB width = high volatility
        Low BB width = low volatility / consolidation
        """
        period = min(self.bb_period, len(prices) - 1)
        if period < 5:
            return 0.0
        
        recent = prices[-period:]
        middle = np.mean(recent)
        std = np.std(recent)
        
        if middle == 0:
            return 0.0
        
        upper = middle + (self.bb_std * std)
        lower = middle - (self.bb_std * std)
        
        return float((upper - lower) / middle)

    def _calculate_drawdown(self, prices: np.ndarray) -> float:
        """คำนวณ current drawdown จาก peak"""
        peak = np.max(prices)
        current = prices[-1]
        if peak == 0:
            return 0.0
        return float((current - peak) / peak)

    def _ema(self, data: np.ndarray, period: int) -> float:
        """Exponential Moving Average"""
        if len(data) == 0:
            return 0.0
        alpha = 2.0 / (period + 1)
        ema = data[0]
        for val in data[1:]:
            ema = alpha * val + (1 - alpha) * ema
        return float(ema)

    def get_strategy_for_regime(
        self,
        regime: MarketRegime,
        base_signal_confidence: float,
    ) -> tuple[str, float]:
        """
        ปรับ signal confidence ตาม regime
        
        ถ้า regime ไม่เหมาะกับ strategy → confidence ลดลง
        
        Returns: (adjusted_confidence, reason)
        """
        if regime.recommended_strategy == "none":
            return 0.0, f"{regime.name} regime — no trading"
        
        if regime.name == "TRENDING" and regime.confidence > 0.6:
            # Momentum strategy works well in trending markets
            adjusted = base_signal_confidence * regime.confidence
            return adjusted, f"Momentum boost: {regime.name} with {regime.confidence:.0%} confidence"
        
        elif regime.name == "RANGING":
            # Mean reversion works in ranging markets
            adjusted = base_signal_confidence * regime.confidence * 0.9
            return adjusted, f"Mean reversion suited for {regime.name} market"
        
        elif regime.name == "VOLATILE":
            # Reduce confidence in volatile markets
            adjusted = base_signal_confidence * 0.5
            return adjusted, f"Volatile market — reduced confidence"
        
        return base_signal_confidence, "Default strategy"
