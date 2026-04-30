# Technical Analysis Deep Dive (Source Summary)

## สรุปสั้นๆ

สรุปจาก `docs/technical-analysis-deep-dive.md` — คู่มือภาษาไทยที่ครอบคลุมสำหรับ technical analysis ในการเทรด crypto และ gold ครอบคลุม 9 หัวข้อหลักพร้อมตัวอย่าง Python code

## สิ่งที่น่าสนใจ

### 1. Candlestick Basics
- Body length แสดง conviction ของ buyers/sellers — ยาว = strong conviction
- Wick length แสดงว่า control เปลี่ยนตรงไหนใน session
- Bullish candle = Close > Open; Bearish = Close < Open

### 2. Candlestick Patterns (23+ patterns)

**Single Candlestick:**
- Doji — Open ≈ Close → market indecision (ต้องรอยืนยัน)
- Hammer — ไส้ล่าง ≥ 2× body, body ในครึ่งบน → bullish reversal หลัง downtrend
- Shooting Star — ไส้บน ≥ 2× body, body ในครึ่งล่าง → bearish reversal หลัง uptrend
- Spinning Top — body เล็ก, ไส้ยาว → high uncertainty
- Marubozu — ไม่มีไส้ → ฝ่ายใดฝ่ายหนึ่งควบคุมเต็มที่

**Multi-Candlestick:**
- Engulfing — body 2 ครอบ body 1 → strong reversal signal
- Morning/Evening Star — 3 แท่ง star + engulfing → strong reversal
- Three White Soldiers / Three Black Crows — 3 แท่ง strong ติดต่อกัน → strong trend continuation

### 3. Chart Patterns

**Reversal:**
- Head & Shoulders → bearish เมื่อ neckline ทะลุ; target = 2×Neckline − Head
- Double Top / Double Bottom → reversal ที่ระดับเท่ากัน (±5% tolerance)
- Triple Top/Bottom → แรงกว่า double
- Rounding Bottom → gradual sentiment shift

**Continuation:**
- Triangles (Ascending/Descending/Symmetric) → price compresses ก่อน breakout
- Flags & Pennants → brief consolidation → usually continues
- Wedges → คล้าย triangles แต่ sloped boundaries
- Rectangles → sideways consolidation channel

**การวัด:** `Target = Reference point ± Height of pattern`; breakout ต้องด้วย volume สูงกว่าค่าเฉลี่ย

### 4. Technical Indicators

**Trend:**
- MAs (SMA, EMA) — directional filters
- MACD — momentum + trend; signal line crossover = entry trigger
- ADX — trend strength (0-100); >25 = trending, <20 = ranging

**Momentum:**
- RSI — overbought >70, oversold <30; divergences signal reversals
- Stochastic — %K/%D crossover; overbought >80, oversold <20

**Volatility:**
- Bollinger Bands — band squeeze = volatility breakout มา
- ATR — stop-loss placement

**Volume:**
- OBV — divergence จากราคา = warning sign
- VWAP — institutional reference point

### 5. Market Theories

- **Dow Theory** — trends confirmed by volume; 3 phases: accumulation, public participation, distribution
- **Elliott Wave** — 5-wave impulse + 3-wave correction; fractals at all timeframes
- **Wyckoff Method** — 4 phases: accumulation → markup → distribution → markdown; volume analysis to identify smart money

### 6. Risk Management

- **Position Sizing:** `Account × Risk% / ATR`
- **Stop-Loss Types:** Fixed %, ATR-based, support/resistance based
- **Kelly Criterion:** `f = W - (1-W)/R`
- **Key Rules:** Risk ≤ 1-2% per trade; reward-to-risk ≥ 2:1; win rate >40%

### 7. Trading Strategies

- **Breakout Trading** — enter when price breaks consolidation with volume surge
- **Trend Following (MA Cross)** — SMA 50/200 crossover
- **Mean Reversion** — price reverts to MA; overbought/oversold as entry
- **Multi-Timeframe** — higher TF for direction, lower TF for entry
- **Paradox Strategy** — trade against crowd at extremes

### 8. AI/ML for Trading

- **LSTM** — time series forecasting; sequential data, long-term dependencies
- **Sentiment Analysis** — news/chat → sentiment score → directional bias
- **Reinforcement Learning** — agent learns optimal policy through reward signals
- **Feature Engineering** — technical indicators + on-chain + macro as model input

### 9. Project Implementation

- **Language:** Python (backend), TypeScript/Next.js (frontend)
- **Libraries:** CCXT (crypto), pandas, numpy, ta-lib/ta
- **Frontend:** Next.js, Tailwind CSS, lightweight-charts v5, recharts
- **DB:** SQLite

## เชื่อมกับอะไร

- [[candlestick-patterns]] — 23+ patterns พร้อมรายละเอียด
- [[chart-patterns]] — reversal และ continuation patterns
- [[technical-indicators]] — ทุกหมวด indicators
- [[market-theories]] — Dow, Elliott Wave, Wyckoff
- [[risk-management]] — position sizing, stop-loss, Kelly Criterion
- [[ai-ml-trading]] — LSTM, RL, sentiment analysis
- [[trading-strategies]] — breakout, trend-following, mean reversion

## คำถามที่ยังค้าง

- TA deep dive นี้เป็น source หลักหรือแค่ summary? ถ้าเป็น summary ควรดู original ที่ไหน?
- มี content เกี่ยวกับ crypto-specific TA หรือไม่? (เช่น funding rates, open interest)
- มี backtesting results หรือ performance metrics สำหรับ strategies ที่แนะนำหรือไม่?
