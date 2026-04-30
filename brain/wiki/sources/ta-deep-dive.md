---
title: "Technical Analysis Deep Dive"
type: source
tags: [technical-analysis, trading, crypto, gold, candlestick, indicators]
sources: 0
created: 2026-04-30
updated: 2026-04-30
---

## Source Summary

**File:** `docs/technical-analysis-deep-dive.md`
**Lines:** 2,612 | **Size:** ~95KB
**Language:** Thai (with English technical terms)
**Project:** [[auto-trade-ai/index]]

A comprehensive Thai-language guide to technical analysis for crypto and gold trading, covering 9 major topics with Python code examples.

## Key Claims & Findings

### 1. Candlestick Basics
- Body length indicates buyer/seller conviction — longer = stronger conviction
- Wick length shows where control shifted during the session
- Bullish candle = Close > Open; Bearish = Close < Open

### 2. Candlestick Patterns (23+ patterns documented)

**Single Candlestick:**
- Doji — Open ≈ Close → market indecision (requires confirmation)
- Hammer — lower wick ≥ 2× body, body in upper zone → bullish reversal after downtrend
- Inverted Hammer — upper wick ≥ 2× body → bullish reversal (needs confirmation)
- Shooting Star — upper wick ≥ 2× body, body in lower zone → bearish reversal after uptrend
- Spinning Top — small body, long wicks → high uncertainty
- Marubozu — no wicks → complete control by one side

**Multi-Candlestick:**
- Engulfing (Bullish/Bearish) — body 2 engulfs body 1 → strong reversal signal
- Tweezers (Top/Bottom) — same-high/low wicks → reversal confirmation
- Morning/Evening Star — 3-candle star + engulfing → strong reversal
- Three White Soldiers / Three Black Crows — 3 consecutive strong candles → strong trend continuation

### 3. Chart Patterns

**Reversal Patterns:**
- Head & Shoulders → bearish when neckline breaks; target = 2×Neckline − Head
- Inverse H&S → bullish equivalent
- Double Top / Double Bottom → classic reversal at equal levels (±5% tolerance)
- Triple Top/Bottom → stronger than double
- Rounding Bottom (Saucers) → gradual sentiment shift

**Continuation Patterns:**
- Triangles (Ascending/Descending/Symmetric) → price compresses before breakout
- Flags & Pennants → brief consolidation in strong trend → usually continues
- Wedges → similar to triangles but with sloped boundaries
- Rectangles → sideways consolidation channel

**Measurement:**
```
Target = Reference point ± Height of pattern
Breakout must be on above-average volume for validation
```

### 4. Technical Indicators

**Trend Indicators:**
- Moving Averages (SMA, EMA) — directional filters
- MACD — momentum + trend; signal line crossover = entry trigger
- ADX — measures trend strength (0–100); >25 = trending, <20 = ranging

**Momentum Oscillators:**
- RSI — overbought >70, oversold <30; divergences signal reversals
- Stochastic — %K/%D crossover; overbought >80, oversold <20

**Volatility:**
- Bollinger Bands — price within bands; band squeeze = volatility breakout coming
- ATR — true range average; used for stop-loss placement

**Volume:**
- OBV — cumulative volume flow; divergence from price = warning sign
- VWAP — volume-weighted average price; institutional reference point

### 5. Market Theories

- **Dow Theory** — trends confirmed by volume; 3 phases: accumulation, public participation, distribution
- **Elliott Wave** — 5-wave impulse + 3-wave correction; fractals at all timeframes
- **Wyckoff Method** — 4 phases: accumulation → markup → distribution → markdown; volume analysis to identify smart money

### 6. Risk Management

- **Position Sizing:** `Position Size = Account × Risk% / ATR` (or stop distance in %)
- **Stop-Loss Types:** Fixed %, ATR-based, support/resistance based
- **Kelly Criterion:** `f = W - (1-W)/R` (win rate, reward-to-risk ratio)
- **Key Rules:** Risk ≤ 1–2% per trade; reward-to-risk ≥ 2:1; maintain win rate >40%

### 7. Trading Strategies

- **Breakout Trading** — enter when price breaks consolidation with volume surge; stop below breakout level
- **Trend Following (MA Cross)** — SMA 50/200 crossover; golden cross = bullish, death cross = bearish
- **Mean Reversion** — price reverts to moving average; overbought/oversold as entry
- **Multi-Timeframe Analysis** — higher TF for direction, lower TF for entry timing
- **Paradox Strategy** — trade against crowd at extremes (Eldar: buy when there's blood in the streets)

### 8. AI/ML for Trading

- **LSTM** — time series forecasting; handles sequential data, captures long-term dependencies
- **Sentiment Analysis** — news/chat → sentiment score → directional bias
- **Reinforcement Learning** — agent learns optimal trading policy through reward signals
- **Feature Engineering** — technical indicators + on-chain data + macro features as model input

### 9. Project Implementation

- **Language:** Python (backend), TypeScript/Next.js (frontend)
- **Libraries:** CCXT (crypto), pandas, numpy, ta-lib/ta
- **Frontend:** Next.js, Tailwind CSS, lightweight-charts v5, recharts
- **DB:** SQLite (trades, exchange rates)

## Notable Quotes

> "Wick ยาวด้านบน = ฝ่ายขายพยายามกด แต่ฝ่ายซื้อยังควบคุม"
> (Long upper wick = sellers tried to push down but buyers retained control)

> "Doji ต้องรอยืนยันจากแท่งถัดไป"
> (Doji requires confirmation from the next candle)

## Related Wiki Pages

- [[candlestick-patterns]] — single and multi-candlestick patterns
- [[chart-patterns]] — reversal and continuation chart patterns
- [[technical-indicators]] — all indicator categories
- [[market-theories]] — Dow, Elliott Wave, Wyckoff
- [[risk-management]] — position sizing, stop-loss, Kelly Criterion
- [[ai-ml-trading]] — LSTM, RL, sentiment analysis
- [[trading-strategies]] — breakout, trend-following, mean reversion

## Related Raw Source

`brain/raw/technical-analysis-deep-dive.md`
