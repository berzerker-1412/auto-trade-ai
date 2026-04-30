---
title: Trading Strategies
type: concept
tags: [trading-strategies, breakout, trend-following, mean-reversion, multi-timeframe]
sources: 1
created: 2026-04-30
updated: 2026-04-30
---

## Overview

A trading strategy defines the rules for *when to enter* and *when to exit* a position. No single strategy works in all market conditions — the key is matching strategy to market regime.

**Core framework:** Trend-following strategies dominate in trending markets; mean-reversion strategies dominate in ranging markets.

---

## Strategy Categories

### 1. Trend Following (ดักเทรนด์)

**Philosophy:** "The trend is your friend." Enter when a trend is established, exit when it reverses.

**Indicators:** SMA crossover, EMA crossover, ADX > 25

**Entry rules (MA Crossover):**
```
SMA 50 > SMA 200 → Golden Cross → BUY signal
SMA 50 < SMA 200 → Death Cross  → SELL signal
```

**Stop-loss:** Below recent swing low (for longs) — use ATR for adaptation:
```
Stop = Entry − 2 × ATR(14)
```

**Strengths:** Catches big moves; easy to systematize
**Weaknesses:** Lagging entry (confirms trend after it started); many small losses in choppy markets

### 2. Breakout Trading (เทรดสิ่งที่ตูม)

**Philosophy:** Trade when price breaks out of a consolidation range with force.

**Entry rules:**
1. Identify consolidation: price moving within a defined range for ≥ 5 candles
2. Wait for breakout: close above resistance (for BUY) with volume > 1.5× average
3. Entry: slightly above breakout level (to avoid false breakouts)
4. Stop-loss: below breakout level or below range low

**Key filters:**
- Volume confirmation is mandatory
- Breakout from a longer consolidation is stronger than brief ones
- Use ATR to set stop distance: `Stop = Breakout Level − 1.5 × ATR`

**Strengths:** Catches big moves early; defined risk upfront
**Weaknesses:** False breakouts are common (up to 50%); requires discipline to cut losses

### 3. Mean Reversion (กลับไปกลับมา)

**Philosophy:** "What goes up too far must come down." Price oscillates around a fair value.

**Indicators:** RSI, Bollinger Bands, VWAP

**Entry rules (Bollinger Bands):**
```
RSI < 30 OR price touches lower Bollinger Band → BUY (oversold bounce)
RSI > 70 OR price touches upper Bollinger Band → SELL (overbought)
```

**Entry rules (VWAP):**
```
Price < VWAP significantly → BUY (institutions buying at discount)
Price > VWAP significantly → SELL
```

**Stop-loss:** Bands or ATR-based; tighter than trend-following

**Strengths:** More frequent signals; good in ranging markets
**Weaknesses:** In strong trends, price can "walk the bands" for large losses

### 4. Multi-Timeframe Analysis (หลายกรอบเวลา)

**Philosophy:** Use higher timeframe for *what* to trade (direction), lower timeframe for *when* to enter.

**Procedure:**
```
1. Daily chart: identify primary trend (SMA direction, ADX level)
2. 4H chart: find key support/resistance levels, wait for pattern
3. 1H chart: precise entry timing with indicators
```

**Example:**
```
Daily: Uptrend (SMA 50 > SMA 200, ADX > 25)
  ↓
4H: Price pulls back to key support zone, forms hammer candlestick
  ↓
1H: RSI oversold (< 30), MACD bullish crossover
  ↓
Entry: BUY at 1H close above hammer high
Stop: Below 4H swing low
```

### 5. Paradox / Contrarian (เทรดสวนทาง)

**Philosophy:** "Be fearful when others are greedy, and greedy when others are fearful." — Warren Buffett

**Eldar's paradox principle:** Buy when there's blood in the streets (extreme fear), sell when euphoria peaks.

**Indicators:**
```
Fear & Greed Index < 20 → Extreme fear → BUY opportunity
Fear & Greed Index > 80 → Extreme greed → SELL opportunity
```

**Tools:** Fear & Greed Index, RSI extreme zones, sentiment surveys, options flow (put/call ratio)

**Strengths:** Highest reward-to-risk when extreme signals are correct
**Weaknesses:** Extremes can persist longer than expected; requires conviction to hold

---

## Strategy Selection by Market Regime

| Market Regime | Best Strategy | Indicators |
|---------------|--------------|------------|
| Strong trend | Trend Following | ADX > 40, SMA crossover |
| Weak trend | Breakout | ADX 20–30, volume confirmation |
| Ranging/Choppy | Mean Reversion | RSI extremes, Bollinger bands |
| Extreme fear | Contrarian | Fear & Greed < 25 |
| Extreme euphoria | Contrarian | Fear & Greed > 75 |

---

## Entry/Exit Checklist

```
Before entering any trade:
  [ ] Is the market regime favorable for this strategy?
  [ ] Is ADX > 20 (trend exists) if using trend-following?
  [ ] Is the signal confirmed by volume?
  [ ] Is stop-loss within risk parameters (≤ 2% portfolio)?
  [ ] Is reward-to-risk ≥ 2:1?

Before exiting:
  [ ] Has the original thesis changed (trend broken)?
  [ ] Has the stop-loss been hit?
  [ ] Is there a better opportunity elsewhere?
  [ ] Has a target been reached with signs of reversal?
```

---

## In auto-trade-ai

Current signal generator (`signal_generator.py`) implements rule-based versions of:
- Trend-following (MA crossover)
- Mean reversion (RSI extremes + Bollinger)
- Breakout (volume confirmation)
- Paradox signals (Fear & Greed)

These are combined into a composite confidence score (0–100) for each asset.

---

## Related Concepts

- [[candlestick-patterns]] — entry signals from price action
- [[chart-patterns]] — breakout levels from structural analysis
- [[technical-indicators]] — RSI, ADX, Bollinger Bands for signal generation
- [[risk-management]] — position sizing, stop-loss placement, reward-to-risk
- [[market-theories]] — Wyckoff accumulation/distribution phases inform regime detection
