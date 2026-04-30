---
title: Technical Indicators
type: concept
tags: [technical-indicators, trading, RSI, MACD, Bollinger, ATR, oscillators]
sources: 1
created: 2026-04-30
updated: 2026-04-30
---

## Overview

Technical indicators are mathematical transformations of price, volume, or open interest data. They serve three broad purposes: **confirm trends**, **identify overbought/oversold extremes**, and **measure volatility**.

**Key principle:** No single indicator is sufficient. Use 2–3 complementary indicators across categories.

---

## Categories

### Trend Indicators

**Moving Averages (MA)**

| Type | Formula | Characteristics |
|------|---------|----------------|
| SMA (Simple) | Mean of last N prices | Equal weight, laggy |
| EMA (Exponential) | Exponential decay weighting | More responsive to recent price |
| WMA (Weighted) | Linear weighting | Between SMA and EMA |

**Crossover signals:**
- Short MA > Long MA → Golden Cross (bullish)
- Short MA < Long MA → Death Cross (bearish)
- Common pairs: SMA 50/200 (daily), EMA 12/26 (daily)

**MACD (Moving Average Convergence Divergence)**

```
MACD Line = EMA(12) − EMA(26)
Signal Line = EMA(9) of MACD Line
Histogram = MACD − Signal
```

| Signal | Condition |
|--------|-----------|
| Bullish | MACD crosses above Signal |
| Bearish | MACD crosses below Signal |
| Strong bullish | MACD > 0 and histogram expanding |
| Divergence | Price makes new high but MACD doesn't → reversal warning |

**ADX (Average Directional Index)**

Measures **trend strength**, not direction:

| ADX Value | Interpretation |
|-----------|--------------|
| 0–20 | Market is ranging (no trend) |
| 20–25 | Emerging trend |
| 25–50 | Strong trend |
| 50–75 | Very strong trend |
| 75–100 | Extreme strength (rare) |

**Rule:** Don't use trend-following indicators when ADX < 20 (market is sideways).

---

## Momentum Oscillators

**RSI (Relative Strength Index)**

```
RS = Average Gain / Average Loss over N periods
RSI = 100 − (100 / (1 + RS))
```

| Zone | Range | Interpretation |
|------|-------|---------------|
| Overbought | > 70 | Extended — potential reversal or continuation |
| Oversold | < 30 | Depressed — potential bounce |
| Neutral | 30–70 | No extreme signal |

**Divergence (most powerful RSI signal):**
- **Bullish divergence:** Price makes lower low, RSI makes higher low → upward reversal likely
- **Bearish divergence:** Price makes higher high, RSI makes lower high → downward reversal likely

**Stochastic Oscillator**

```
%K = (Current Close − Lowest Low over N) / (Highest High − Lowest Low) × 100
%D = SMA(%K, 3)
```

| Zone | Range |
|------|-------|
| Overbought | > 80 |
| Oversold | < 20 |

**Crossover signal:** %K crosses above %D in oversold zone → buy signal (and vice versa).

---

## Volatility Indicators

**Bollinger Bands**

```
Middle Band = SMA(20)
Upper Band = SMA(20) + 2 × StdDev(20)
Lower Band = SMA(20) − 2 × StdDev(20)
```

| Pattern | Interpretation |
|---------|---------------|
| Band squeeze | Volatility at minimum — breakout imminent |
| Price touches upper band | Potentially overextended |
| Price touches lower band | Potentially oversold |
| Price walks the bands | Strong trend continuation |

**Band Width:** Narrow bands (low volatility) precede high-volatility breakouts.

**ATR (Average True Range)**

```
TR = max(High−Low, |High−PrevClose|, |Low−PrevClose|)
ATR = SMA(TR, 14)
```

**Primary use:** Setting stop-loss distances. ATR-based stops adapt to current volatility.

```
Stop Distance = 1.5 × ATR(14)  # for volatile markets
             = 0.5 × ATR(14)  # for quiet markets
```

---

## Volume Indicators

**OBV (On-Balance Volume)**

```
If Close > Prev Close: OBV += Volume
If Close < Prev Close: OBV -= Volume
If Close == Prev Close: OBV unchanged
```

**Use:** OBV divergence from price warns of potential reversal. OBV making new highs confirms bullish trend.

**VWAP (Volume Weighted Average Price)**

```
VWAP = Sum(Price × Volume) / Sum(Volume)
```

**Use:** Institutional traders use VWAP as reference — price above VWAP = buy bias, below = sell bias.

---

## Python Implementation

```python
import pandas as pd
import numpy as np

# RSI calculation
def calculate_rsi(prices: list[float], period: int = 14) -> float:
    """คำนวณ RSI สำหรับ list ของราคาปิด"""
    deltas = pd.Series(prices).diff()
    gains = deltas.where(deltas > 0, 0.0)
    losses = -deltas.where(deltas < 0, 0.0)

    avg_gain = gains.rolling(window=period).mean()
    avg_loss = losses.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

# MACD calculation
def calculate_macd(prices: list[float],
                   fast: int = 12,
                   slow: int = 26,
                   signal: int = 9) -> dict:
    """คำนวณ MACD, Signal Line และ Histogram"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line

    return {
        "macd": macd_line.iloc[-1],
        "signal": signal_line.iloc[-1],
        "histogram": histogram.iloc[-1],
    }

# Bollinger Bands
def calculate_bollinger_bands(prices: list[float],
                               period: int = 20,
                               std_dev: float = 2.0) -> dict:
    """คำนวณ Bollinger Bands"""
    sma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()

    upper = sma + (std_dev * std)
    lower = sma - (std_dev * std)

    return {
        "upper": upper.iloc[-1],
        "middle": sma.iloc[-1],
        "lower": lower.iloc[-1],
    }

# ATR calculation
def calculate_atr(highs: list[float],
                  lows: list[float],
                  closes: list[float],
                  period: int = 14) -> float:
    """คำนวณ ATR (Average True Range)"""
    tr = []
    for i in range(1, len(highs)):
        h_l = highs[i] - lows[i]
        h_c = abs(highs[i] - closes[i-1])
        l_c = abs(lows[i] - closes[i-1])
        tr.append(max(h_l, h_c, l_c))

    return np.mean(tr[-period:])

# Combined signal check
def get_combined_signal(prices: list[float],
                        rsi_thresh: float = 30,
                        macd_fast: int = 12,
                        macd_slow: int = 26) -> str:
    """รวม RSI + MACD สำหรับสัญญาณ"""
    ps = pd.Series(prices)

    rsi = calculate_rsi(prices)
    macd = calculate_macd(ps, fast=macd_fast, slow=macd_slow)

    signals = []
    if rsi < rsi_thresh:
        signals.append("RSI_OVERSOLD")
    elif rsi > 70:
        signals.append("RSI_OVERBOUGHT")

    if macd["histogram"] > 0 and macd["macd"] > macd["signal"]:
        signals.append("MACD_BULLISH")
    elif macd["histogram"] < 0 and macd["macd"] < macd["signal"]:
        signals.append("MACD_BEARISH")

    return " + ".join(signals) if signals else "NEUTRAL"
```

## Indicator Selection Strategy

| Goal | Indicators |
|------|-----------|
| Identify trend direction | SMA 50/200, EMA 21, ADX |
| Find entry timing | RSI, Stochastic, MACD crossover |
| Set stop-loss | ATR, Bollinger Bands lower |
| Confirm breakout | Volume, OBV |
| Measure volatility | ATR, Bollinger Band width |

## Common Pitfalls

1. **Indicator overload** — using 5+ indicators leads to analysis paralysis
2. **Ignoring timeframes** — RSI overbought on 1H doesn't matter on daily
3. **Using lagging indicators in ranging markets** — MA and MACD give false signals when ADX < 20
4. **Divergence takes time** — divergence can persist for weeks before price reverses

## Related Concepts

- [[candlestick-patterns]] — pattern signals complement indicator readings
- [[chart-patterns]] — patterns at structural level, indicators at mathematical level
- [[risk-management]] — ATR for stop-loss sizing; position sizing based on volatility
- [[ai-ml-trading]] — ML models use indicator values as features
