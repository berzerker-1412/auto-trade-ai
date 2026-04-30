---
title: auto-trade-ai: Architecture
type: project
tags: [architecture, system-design, layers]
created: 2026-04-30
updated: 2026-04-30
---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│           Web UI for monitoring, stats, controls               │
└─────────────────────┬─────────────────────────────────────────┘
                      │ HTTP / WebSocket
┌─────────────────────▼─────────────────────────────────────────┐
│                   FastAPI Backend (Python)                     │
│            Trade commands, P&L stats, signal triggers           │
└─────────────────────┬─────────────────────────────────────────┘
                      │
┌─────────────────────▼─────────────────────────────────────────┐
│                      Core Layer                                │
│  ┌──────────────────┐    ┌────────────────────────────────┐  │
│  │  AI Signal Gen   │    │     Paper Trader /             │  │
│  │  (GPT-4o)       │───▶│     Live Trader                │  │
│  │                  │    │  Balance tracking, SL/TP check  │  │
│  └──────────────────┘    └──────────────┬─────────────────┘  │
│                                          │                     │
│  ┌───────────────────────────────────────▼─────────────────┐  │
│  │              Trade Logger (SQLite)                         │  │
│  │   trades table: id, symbol, direction, entry/exit, P&L   │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Crypto        │     │   Gold          │
│   (CCXT)       │     │   (Price Feed)  │
│   Binance       │     │   Alpha Vantage  │
│   100+ exchanges│     │   GoldAPI       │
└─────────────────┘     └─────────────────┘
```

---

## Key Modules

### `backend/ai/signal_generator.py`

**Class:** `AISignalGenerator`

```
Input: symbol, asset_type, market_data, analysis_text
  ↓
Build prompt with system role: "professional trading signal generator"
  ↓
OpenAI GPT-4o chat completion (temperature=0.3, JSON mode)
  ↓
Parse JSON response
  ↓
If confidence >= threshold → return TradeSignal
Else → return None (no trade)
```

**Fallback mode:** When OpenAI unavailable, generates random BUY/SELL with confidence 0.6–0.9 and simple SL/TP at ±2% / ±5%

---

### `backend/crypto/exchange.py`

**Class:** `CryptoExchange`

CCXT wrapper providing:
- `get_balance(currency)` — fetch wallet balance
- `get_ticker(symbol)` — current price, bid/ask, volume
- `get_ohlcv(symbol, timeframe, limit)` — candlestick data
- `place_order(symbol, type, side, amount, price)` — execute trade
- `cancel_order(order_id, symbol)` — cancel pending order
- `get_open_orders(symbol)` — list active orders

**Testnet:** `https://testnet.binance.vision/api`

---

### `backend/gold/price_feed.py`

**Class:** `GoldPriceFeed`

Sources:
- `demo` — simulated ~$2000/oz with random variation (default)
- `alpha_vantage` — real XAUUSD via API (needs key)
- `goldapi` — real XAUUSD via API (needs key)

---

### `backend/core/paper_trader.py`

**Class:** `PaperTrader`

```
init: balance = 100,000 USDT
  ↓
execute_signal(signal):
  - Check balance >= required
  - Create Trade (OPEN)
  - Deduct balance (for BUY)
  - Log to SQLite
  ↓
check_stop_loss_take_profit(symbol, current_price):
  - BUY: SL if price <= stop_loss, TP if price >= take_profit
  - SELL: SL if price >= stop_loss, TP if price <= take_profit
  ↓
close_trade(symbol, exit_price, reason):
  - Calculate P&L
  - Update balance (add profit / subtract loss)
  - Update trade status → CLOSED
```

---

### `backend/core/trade_logger.py`

**Class:** `TradeLogger`

SQLite schema:
```sql
trades (
  id, symbol, asset_type, direction,
  entry_price, exit_price, quantity,
  stop_loss, take_profit,
  status, entry_time, exit_time,
  trade_number, created_at
)
```

Key queries:
- `log_trade()` — INSERT new trade
- `update_trade()` — UPDATE exit_price, status, exit_time
- `get_open_trades()` — WHERE status = 'open'
- `get_trade_stats()` — win rate, total P&L, avg win/loss
- `get_next_trade_number()` — "ไม้ที่เท่าไหร่"

---

## Data Flow: Signal → Trade → P&L

```
1. Cron/system triggers check
2. exchange.get_ticker("BTC/USDT") → market_data
3. ai.analyze_market(price_data) → analysis_text
4. ai.generate_signal("BTC/USDT", CRYPTO, market_data, analysis)
   → TradeSignal or None
5. If signal:
   paper_trader.execute_signal(signal)
   → Trade created, balance deducted
6. Loop: check_stop_loss_take_profit every tick
   → close_trade when SL/TP hit
7. P&L calculated, balance updated
```

---

## Frontend Architecture (Next.js)

```
frontend/
├── src/
│   ├── app/              ← Next.js App Router pages
│   ├── components/       ← React components
│   └── lib/             ← API client utilities
└── public/
```

Purpose:
- Dashboard: balance, open trades, P&L
- Trade history: past trades with stats
- Settings: API keys, thresholds, symbols
- Real-time updates via polling or WebSocket
