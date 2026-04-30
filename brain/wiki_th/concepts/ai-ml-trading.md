# AI/ML สำหรับ Trading

## สรุปสั้นๆ

AI/ML ใน trading แบ่งเป็นสอง paradigm: **supervised learning** (predict target variable) และ **reinforcement learning** (learn optimal policy ผ่าน interaction) ทั้งสอง relevant สำหรับ auto-trade-ai

**Core tension:** ตลาดไม่ stationary — pattern ที่เคยใช้ได้อาจไม่ work ต่อไป (non-stationarity problem) ทำให้ ML for trading ยากจริงๆ

## สิ่งที่น่าสนใจ

### Supervised Learning

**LSTM (Long Short-Term Memory)**
- เหมาะกับ sequential data ที่มี long-range dependencies
- Input: `[N × T × F]` — N=samples, T=timesteps, F=features
- Features: OHLCV, indicators (RSI, MACD, Bollinger), macro data
- Output: next-period price หรือ direction (UP/DOWN/HOLD)

**สิ่งสำคัญ:**
- Normalize features ต่อ asset
- Train/test split ต้อง respect time (ไม่มี look-ahead bias)
- ใช้ walk-forward validation สำหรับ realistic performance estimates

**Sentiment Analysis**
```
News/Social Media → Scraping → NLP → Sentiment Score → Trading Signal
```
- Lexicon-based: VADER, TextBlob → score −1 ถึง +1
- Fine-tuned transformer: FinBERT → directional sentiment
- **Challenge:** แยก signal จาก noise — financial social media noisy, news structured กว่า

**Feature Engineering** (ส่วนสำคัญที่สุด)
```python
features = {
    # Price-based
    "returns_1d": (price - price.shift(1)) / price.shift(1),
    "returns_7d": (price - price.shift(7)) / price.shift(7),
    
    # Technical indicators
    "rsi_14": calculate_rsi(close, period=14),
    "macd_signal": calculate_macd(close)["signal"],
    "bb_position": (close - bb_lower) / (bb_upper - bb_lower),
    
    # Volume
    "volume_ratio": volume / volume.rolling(20).mean(),
    "obv_slope": obv.diff(10) / obv.shift(10),
    
    # Cross-asset / macro
    "btc_correlation_7d": close.rolling(7).corr(btc_close),
    "fear_greed_index": fetch_fear_greed(),
    
    # Time-based
    "hour_of_day": timestamp.hour,
    "day_of_week": timestamp.dayofweek,
}
```

### Reinforcement Learning

**Core Framework:**
```
Environment: Market (price data feed)
Agent: Trading strategy
State: Current portfolio + price features
Action: {−1 (short), 0 (hold), +1 (long)}
Reward: Portfolio return หรือ Sharpe ratio
```

**Algorithms ที่นิยม:**
| Algorithm | Characteristics |
|-----------|----------------|
| DQN | Off-policy, ดีสำหรับ discrete actions |
| PPO | On-policy, รองรับ continuous action spaces |
| SAC | Off-policy, maximum entropy, ดีสำหรับ exploration |
| A2C/A3C | Actor-critic, parallel environments |

**Key Risks:**
- **Overfitting** — strategy หา pattern ใน noise
- **Survivorship bias** — train บน assets ที่ยังมีอยู่
- **Reward hacking** — agent หาทางลัด (เช่น ถือ positions เล็กๆ เพื่อลด risk)
- **Non-stationarity** — market regime เปลี่ยนทำลาย learned policy

**Walk-Forward Testing (จำเป็นสำหรับ RL):**
```
For each rolling window:
  1. Train on [t−train_period, t−1]
  2. Validate on [t−1, t]
  3. Record out-of-sample performance
```

### Architecture สำหรับ auto-trade-ai

```
┌─────────────────────────────────────────────────────┐
│                    Input Features                     │
│  OHLCV · Indicators · Macro · On-chain · Sentiment  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│              Feature Engineering Layer               │
│  Normalization · Lag features · Cross-asset feats    │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│                   Model Ensemble                      │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐   │
│  │ LSTM        │  │ XGBoost     │  │ RL Agent   │   │
│  │ (sequence)  │  │ (tabular)   │  │ (policy)   │   │
│  └─────────────┘  └─────────────┘  └────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│               Signal Generation Layer                 │
│  Confidence score (0–1) · Direction (BUY/SELL/HOLD)  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│              Risk Management Layer                     │
│  Position sizing · Stop-loss · Max drawdown check    │
└──────────────────────────────────────────────────────┘
```

### Current Status ใน auto-trade-ai

ปัจจุบัน `signal_generator.py` เป็น **rule-based placeholder** — generate signals จาก candlestick patterns และ indicators ไม่ใช่ ML

**แผนการพัฒนา:**
- Phase 1 (ปัจจุบัน): Rule-based signal generation
- Phase 2: LSTM price prediction ด้วย walk-forward validation
- Phase 3: Sentiment analysis จาก crypto news
- Phase 4: RL agent สำหรับ portfolio-level decision making

## เชื่อมกับอะไร

- [[technical-indicators]] — indicator values เป็น primary ML features
- [[risk-management]] — RL reward function ต้อง include risk (Sharpe, max drawdown)
- [[trading-strategies]] — strategies define action space สำหรับ RL agents
- [[candlestick-patterns]] — pattern signals เป็น features สำหรับ classification

## คำถามที่ยังค้าง

- Phase 2 LSTM ควร predict price หรือ direction ดีกว่า?
- จะ handle non-stationarity อย่างไร — retrain frequency เท่าไหร่ดี?
- Sentiment data source ไหน reliable สำหรับ crypto?
