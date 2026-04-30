---
title: Overview
type: overview
tags: [trading, AI, crypto, gold, technical-analysis]
created: 2026-04-30
updated: 2026-04-30
---

This wiki documents the **auto-trade-ai** project — an AI-powered trading system covering crypto signals, gold trading, and stock analysis.

## Projects

- [[auto-trade-ai/index]] — main project page

## Knowledge Base Structure

```
Technical Analysis (9 sections in TA Deep Dive)
├── Candlestick Patterns       → [[candlestick-patterns]]
│   └── 23+ patterns: Doji, Hammer, Engulfing, Morning Star, etc.
├── Chart Patterns            → [[chart-patterns]]
│   ├── Reversal: Head & Shoulders, Double Top/Bottom, Rounding Bottom
│   └── Continuation: Triangles, Flags, Pennants, Wedges, Rectangles
├── Technical Indicators      → [[technical-indicators]]
│   ├── Trend: MA, MACD, ADX
│   ├── Momentum: RSI, Stochastic
│   ├── Volatility: Bollinger Bands, ATR
│   └── Volume: OBV, VWAP
├── Market Theories           → [[market-theories]]
│   ├── Dow Theory (3 trends, 3 phases)
│   ├── Elliott Wave (5-3 fractal structure)
│   └── Wyckoff Method (accumulation/distribution phases)
├── Risk Management          → [[risk-management]], [[auto-trade-ai/risk-management]]
│   ├── Position sizing (fixed %, ATR-based)
│   ├── Stop-loss strategies
│   └── Kelly Criterion
├── Trading Strategies       → [[trading-strategies]]
│   ├── Trend-following (MA crossover)
│   ├── Breakout trading
│   ├── Mean reversion
│   ├── Multi-timeframe analysis
│   └── Paradox / Contrarian
└── AI/ML for Trading       → [[ai-ml-trading]]
    ├── LSTM time series forecasting
    ├── Reinforcement Learning (PPO, SAC, DQN)
    ├── Sentiment analysis (FinBERT, VADER)
    └── Feature engineering pipeline
```

## Key Pages

[[auto-trade-ai/index]] · [[auto-trade-ai/architecture]] · [[auto-trade-ai/data-models]]
[[auto-trade-ai/risk-management]] · [[candlestick-patterns]] · [[technical-indicators]]

## Open Questions

- [x] What are the core trading strategies being implemented? → [[trading-strategies]]
- [x] What data sources power the AI signals? → [[ta-deep-dive]] + CoinGecko + Exchange Rate API
- [x] How is risk management handled? → [[auto-trade-ai/risk-management]]
- [ ] LSTM model: what features, what validation approach?
- [ ] When will Phase 2 (ML) be implemented?

## Recent Updates

- **2026-04-30:** Integrated full TA Deep Dive research into knowledge base — 7 concept pages + 1 source page created
