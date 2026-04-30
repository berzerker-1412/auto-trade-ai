---
title: Candlestick Patterns
type: concept
tags: [candlestick, technical-analysis, price-action, patterns]
sources: 1
created: 2026-04-30
updated: 2026-04-30
---

## Overview

Candlestick patterns are the most fundamental price action signals. They encode the battle between buyers and sellers in a single time period. The body shows Open→Close, and wicks show the High→Low range.

**Key principle:** A pattern's signal is only meaningful in context — where it appears in the trend matters as much as the pattern itself.

## Single Candlestick Patterns

### Doji (โดจิ)

**Formula:** `Open ≈ Close` (body nearly absent)

```
        High
         ▲
    ─────┴─────  ← Open ≈ Close
         │
         │
    ─────┴─────
         ▼
       Low
```

| Type | Shape | Interpretation |
|------|-------|----------------|
| Gravestone | Long upper wick | Sellers dominated after push up |
| Dragonfly | Long lower wick | Buyers dominated after push down |
| Long-legged | Long both wicks | Maximum market indecision |

**Signal:** Indecision — **requires confirmation from next candle**
- At resistance (top) → potential bearish reversal
- At support (bottom) → potential bullish reversal

### Hammer

**Formula:** `Lower Wick ≥ 2 × Body` AND `Body in upper zone`

```
         High
          │
    ──────┴─────  Upper Wick (short)
    │           │
    │   Body    │  ← near top of candle
    │           │
    └───────────┘
          │
          └────────  Lower Wick (long ≥ 2× body)
          ▼
        Low
```

**Context:** Must appear after a **downtrend**
**Signal:** Bullish reversal — buyers rejected lower prices
**Confirmation:** Next candle is green, volume above average

### Shooting Star

**Formula:** `Upper Wick ≥ 2 × Body` AND `Body in lower zone`

**Context:** Must appear after an **uptrend**
**Signal:** Bearish reversal — sellers rejected higher prices

### Spinning Top

**Formula:** Small body, long upper and lower wicks

**Signal:** High uncertainty — neither buyers nor sellers in control. Wait for next candle.

### Marubozu

**Formula:** No wicks (or negligible)

- **Bullish Marubozu** — Open = High, Close = Low → complete bullish control
- **Bearish Marubozu** — Open = Low, Close = High → complete bearish control

**Signal:** Strong directional conviction. The entire session was one-directional.

---

## Multi-Candlestick Patterns

### Engulfing Pattern

**Structure:** Body of candle 2 fully covers body of candle 1 (wicks ignored)

| Type | Condition | Signal |
|------|-----------|--------|
| Bullish Engulfing | Candle 1 bearish, candle 2 bullish + larger body | Bullish reversal |
| Bearish Engulfing | Candle 1 bullish, candle 2 bearish + larger body | Bearish reversal |

**Key:** Volume on candle 2 should exceed volume on candle 1

### Morning Star / Evening Star

**Structure:** 3 candles
1. Large directional candle (continues trend)
2. Small body (star/doji) — indecision
3. Large candle opposite direction — **closes into candle 1 body**

**Signal:** Strong reversal (stronger than engulfing due to the middle indecision candle)

### Three White Soldiers / Three Black Crows

**Structure:** 3 consecutive large directional candles, each closing above/within prior body

**Signal:** Strong trend continuation — most powerful of all reversal patterns

### Tweezer Top / Bottom

**Structure:** Two candles with matching or near-matching High/Low (wicks only, bodies can differ)

**Signal:** Confirmation of reversal — buyers/sellers rejected at same price level twice

---

## Recognition Algorithm (Python)

```python
# ตรวจจับ Hammer (bullish reversal candlestick)
def is_hammer(candle: dict) -> bool:
    """
    candle = {open, high, low, close}
    Hammer: lower_wick >= 2*body AND body in upper half
    """
    body = abs(candle["close"] - candle["open"])
    upper_wick = candle["high"] - max(candle["open"], candle["close"])
    lower_wick = min(candle["open"], candle["close"]) - candle["low"]
    body_top = max(candle["open"], candle["close"])

    # เงื่อนไข: ไส้ล่างยาว และตัวแท่งอยู่ในครึ่งบนของแท่ง
    return lower_wick >= 2 * body and body_top >= candle["low"] + lower_wick / 2

# ตรวจจับ Engulfing Pattern
def is_bullish_engulfing(candle1: dict, candle2: dict) -> bool:
    """
    candle1 = bearish (close < open)
    candle2 = bullish (close > open) และ body ครอบ candle1
    """
    c1_bearish = candle1["close"] < candle1["open"]
    c2_bullish = candle2["close"] > candle2["open"]

    if not (c1_bearish and c2_bullish):
        return False

    body1_top = max(candle1["open"], candle1["close"])
    body1_bot = min(candle1["open"], candle1["close"])
    body2_top = max(candle2["open"], candle2["close"])
    body2_bot = min(candle2["open"], candle2["close"])

    # body ของ candle2 ครอบทั้ง body ของ candle1
    return body2_bot <= body1_bot and body2_top >= body1_top
```

## Relationship to Other Concepts

- **[[chart-patterns]]** — multi-candle patterns at a higher structural level
- **[[technical-indicators]]** — RSI/Stochastic measure overbought/oversold, complementing candle signals
- **[[risk-management]]** — stop-loss placed below hammer low for bullish setups

## In auto-trade-ai

Implemented in `backend/ai/signal_generator.py` as pattern recognition rules. The TA document has full code examples for candlestick pattern detection and signal generation.
