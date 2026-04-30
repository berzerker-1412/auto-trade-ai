---
title: auto-trade-ai
type: project
tags: [python, AI, trading, crypto, gold, signals, ccxt, langchain]
created: 2026-04-30
updated: 2026-04-30
---

AI-powered trading system that generates BUY/SELL signals across crypto and gold markets with the **goal of making profit**.

**Source:** `/Users/chinnawat/auto-trade-ai`

---

## Core Objective

**"Make money, no matter what"** — maximize profit through AI-driven signal generation and risk-managed trade execution.

---

## How It Makes Profit

1. **AI Signal Generator** — analyzes market data → generates BUY or SELL signals with confidence score
2. **Paper Trader** — simulates trades with virtual balance (100,000 USDT default)
3. **Live Trader** — executes real orders when paper trading proves profitable
4. **Risk Management** — stop-loss, take-profit, position sizing to protect capital
5. **P&L Tracking** — win rate, total P&L, average win/loss metrics

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3.10+ |
| Exchange | CCXT (Binance, 100+ exchanges) |
| AI | OpenAI GPT-4o / LangChain |
| Data | Pandas, NumPy, TA (technical analysis) |
| Database | SQLite (trade logging) |
| Web | FastAPI + Next.js frontend |
| Technical Analysis | ta library |

---

## Directory Structure

```
auto-trade-ai/
├── backend/
│   ├── ai/
│   │   └── signal_generator.py     ← AI signal generation (GPT-4o)
│   ├── crypto/
│   │   └── exchange.py            ← CCXT wrapper for crypto exchanges
│   ├── gold/
│   │   └── price_feed.py          ← Gold price (XAUUSD) from multiple sources
│   └── core/
│       ├── models.py              ← TradeSignal, Trade, TradeResult dataclasses
│       ├── paper_trader.py        ← Paper trading engine
│       └── trade_logger.py        ← SQLite trade database
├── frontend/                       ← Next.js web UI
├── config/settings.yaml            ← All configuration
├── data/trades.db                  ← SQLite trade history
├── docs/
│   └── technical-analysis-deep-dive.md  ← Thai TA guide (candlesticks, patterns)
└── requirements.txt
```

---

## Trading Flow

```
Market Data (CCXT / Price Feed)
        ↓
AI Signal Generator (GPT-4o)
  - confidence ≥ 0.75 → Signal
  - < 0.75 → No trade
        ↓
Paper Trader / Live Trader
  - Check balance
  - Execute order
  - Monitor stop-loss / take-profit
        ↓
Trade Logger (SQLite)
  - Record trade
  - Calculate P&L
  - Update balance
```

---

## Risk Management Rules

| Parameter | Value |
| --- | --- |
| Max position size | 10% of balance |
| Stop-loss | 2% |
| Take-profit | 5% |
| Max concurrent trades | 3 |
| Max trades per day | 5 |
| Confidence threshold | 0.75 |

---

## AI Signal Generation

**Prompt输入:**
- Current price, 24h high/low, volume
- Technical analysis output
- Optional news

**Output:**
- `direction`: "BUY" or "SELL"
- `entry_price`: exact price to enter
- `quantity`: amount to trade
- `stop_loss`: price for stop loss
- `take_profit`: price for take profit
- `confidence`: 0.0–1.0
- `reasoning`: explanation

**Fallback:** If OpenAI unavailable → random signal with confidence 0.6–0.9 (for testing only)

---

## Asset Classes

### Crypto (via CCXT)
- Binance testnet by default
- Supports 100+ exchanges
- Symbols: BTC/USDT, ETH/USDT, SOL/USDT
- OHLCV data, ticker data, order execution

### Gold (XAU/USD)
- Demo mode (simulated ~$2000/oz)
- Alpha Vantage API (real data, needs API key)
- GoldAPI.io (real data, needs API key)

---

## Knowledge Pages

- [[auto-trade-ai/architecture|Architecture]] — system layers and data flow
- [[auto-trade-ai/data-models|Data Models]] — TradeSignal, Trade, TradeResult
- [[auto-trade-ai/risk-management|Risk Management]] — stop-loss, position sizing, drawdown
