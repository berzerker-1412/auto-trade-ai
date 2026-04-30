---
title: AI/ML for Trading
type: concept
tags: [AI, machine-learning, LSTM, reinforcement-learning, sentiment, trading]
sources: 1
created: 2026-04-30
updated: 2026-04-30
---

## Overview

AI/ML in trading falls into two paradigms: **supervised learning** (predict a target variable) and **reinforcement learning** (learn an optimal policy through interaction). Both are relevant for auto-trade-ai.

**Core tension:** Markets are not stationary — patterns that worked historically may not persist (non-stationarity problem). This makes ML for trading genuinely hard.

---

## Supervised Learning Approaches

### Time Series Forecasting (LSTM)

**LSTM (Long Short-Term Memory)** networks handle sequential data with long-range dependencies — well-suited for price prediction.

```
Architecture for price prediction:
  Input: [N × T × F]  where N=samples, T=timesteps, F=features
  Features: OHLCV, technical indicators (RSI, MACD, Bollinger values), macro data
  Output: Next-period price or return direction (UP/DOWN/HOLD)
```

**Key considerations:**
- Normalize/standardize features per asset
- Train/test split must respect time (no look-ahead bias)
- Target: raw price, returns, or directional classification
- Use walk-forward validation for realistic performance estimates

**Typical performance:** LSTM models can capture some momentum patterns but struggle to consistently outperform simple baselines (e.g., random forest on features) due to market non-stationarity.

### Sentiment Analysis

**Pipeline:**
```
News / Social Media → Scraping → NLP → Sentiment Score → Trading Signal
```

| Approach | Tool | Output |
|----------|------|--------|
| Lexicon-based | VADER, TextBlob | Score (−1 to +1) |
| Fine-tuned transformer | FinBERT | Directional sentiment |
| Embeddings + classifier | Custom | Probabilistic signal |

**Key challenge:** Separating signal from noise. Financial social media is noisy. News is more structured.

### Feature Engineering

The most impactful part of ML for trading is feature design:

```python
# Feature categories for a crypto trading model
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
    "is_month_start": timestamp.is_month_start,
}

# Target: 1-day forward return direction
target = (price.shift(-1) - price) / price
```

---

## Reinforcement Learning

### Core Framework

An RL agent learns a **policy** π(a|s) — given state s, what action a to take (BUY/SELL/HOLD), by maximizing cumulative reward.

```
Environment: Market (price data feed)
Agent: Trading strategy
State: Current portfolio + price features
Action: {−1 (short), 0 (hold), +1 (long)}
Reward: Portfolio return or Sharpe ratio
```

### Common Algorithms

| Algorithm | Characteristics |
|-----------|----------------|
| **DQN** | Off-policy, good for discrete actions, stable |
| **PPO** | On-policy, handles continuous action spaces, widely used |
| **SAC** | Off-policy, maximum entropy, good for exploration |
| **A2C/A3C** | Actor-critic, parallel environments |

### Key Risks

- **Overfitting to historical data** — strategy finds patterns in noise
- **Survivorship bias** — trained on assets that still exist
- **Reward hacking** — agent finds exploits (e.g., holding tiny positions to reduce risk)
- **Non-stationarity** — market regime changes break learned policy

### Walk-Forward Testing

Essential for RL trading systems:

```
For each rolling window:
  1. Train on [t−train_period, t−1]
  2. Validate on [t−1, t]
  3. Record out-of-sample performance
Aggregate all out-of-sample results for true performance estimate
```

---

## Practical Architecture for auto-trade-ai

```
┌─────────────────────────────────────────────────────┐
│                    Input Features                    │
│  OHLCV · Indicators · Macro · On-chain · Sentiment  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│              Feature Engineering Layer               │
│  Normalization · Lag features · Cross-asset feats   │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│                   Model Ensemble                      │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │ LSTM         │  │ XGBoost     │  │ RL Agent    │  │
│  │ (sequence)   │  │ (tabular)   │  │ (policy)    │  │
│  └─────────────┘  └─────────────┘  └────────────┘  │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│               Signal Generation Layer                 │
│  Confidence score (0–1) · Direction (BUY/SELL/HOLD) │
└──────────────────────┬──────────────────────────────┘
                       ▼
┌──────────────────────────────────────────────────────┐
│              Risk Management Layer                    │
│  Position sizing · Stop-loss · Max drawdown check   │
└──────────────────────────────────────────────────────┘
```

---

## Current Status in auto-trade-ai

The current `signal_generator.py` is a **rule-based placeholder** — it generates signals from candlestick patterns and indicators, not ML. The AI/ML components are planned as future work:

- **Phase 1 (current):** Rule-based signal generation from technical indicators
- **Phase 2:** LSTM price prediction model with walk-forward validation
- **Phase 3:** Sentiment analysis from crypto news
- **Phase 4:** RL agent for portfolio-level decision making

---

## Libraries

| Task | Libraries |
|------|----------|
| Feature engineering | pandas, numpy, ta (technical analysis) |
| LSTM | PyTorch, TensorFlow, Keras |
| Tabular ML | XGBoost, LightGBM, scikit-learn |
| Reinforcement Learning | Stable-Baselines3, RLlib |
| NLP / Sentiment | transformers (FinBERT), VADER |

---

## Related Concepts

- [[technical-indicators]] — indicator values are primary ML features
- [[risk-management]] — RL reward function must incorporate risk (Sharpe, max drawdown)
- [[trading-strategies]] — strategies define the action space for RL agents
- [[candlestick-patterns]] — pattern signals as features for classification models
