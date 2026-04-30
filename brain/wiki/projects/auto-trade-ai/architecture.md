---
title: auto-trade-ai: Architecture
type: project
tags: [architecture, system-design, layers]
created: 2026-04-30
updated: 2026-05-01
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
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              WalletManager                               │  │
│  │  ┌──────────────────┐    ┌──────────────────┐          │  │
│  │  │  PAPER Wallet    │    │  LIVE Wallet     │          │  │
│  │  │  initial: 100K  │    │  balance: จาก    │          │  │
│  │  │  USDT (sim)     │    │  exchange API   │          │  │
│  │  └──────────────────┘    └──────────────────┘          │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────┐    ┌────────────────────────────────┐  │
│  │  AI Signal Gen   │    │     Trader                     │  │
│  │  (GPT-4o)       │───▶│  - PAPER: simulate only        │  │
│  │                  │    │  - LIVE: real exchange orders   │  │
│  └──────────────────┘    └──────────────┬─────────────────┘  │
│                                         │                     │
│  ┌──────────────────────────────────────▼─────────────────┐  │
│  │              TradeLogger (SQLite)                         │  │
│  │  trades table: id, symbol, asset_type, wallet_type,     │  │
│  │  direction, entry/exit, quantity, SL/TP, P&L           │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│   Crypto        │     │   Gold          │
│   (CCXT)        │     │   (Alpha Vantage)│
│   Binance       │     │   Real XAUUSD   │
│   real spot     │     │   API fallback  │
└─────────────────┘     └─────────────────┘
```

---

## Wallet Separation (PAPER vs LIVE)

**Two completely separate wallets:**

| | PAPER | LIVE |
|---|---|---|
| Balance source | `WalletManager.paper_wallet` | Exchange API (`exchange.get_balance()`) |
| Orders | Simulated only | Real orders via CCXT |
| SL/TP execution | Simulated | Real stop-loss/take-profit |
| DB tracking | `wallet_type='paper'` | `wallet_type='live'` |
| Risk | None (simulated) | Real money |

**Key principle:** PAPER wallet สำหรับทดสอบระบบก่อน — LIVE wallet สำหรับเงินจริงหลังจาก proven แล้ว

---

## Key Modules

### `backend/core/wallet_manager.py`

**Class:** `WalletManager`

จัดการกระเป๋าสองใบแยกจากกัน:

```python
wm = WalletManager(paper_initial=100000)
wm.paper_wallet   # กระเป๋าจำลอง
wm.live_wallet    # กระเป๋าจริง (balance จาก exchange API)
wm.get_wallet(WalletType.PAPER)
wm.reset_paper_wallet()  # รีเซ็ตกระเป๋าจำลอง
wm.get_summary()  # {"paper": {...}, "live": {...}}
```

---

### `backend/core/trader.py`

**Classes:** `Trader` (base), `PaperTrader` (backward compat), `LiveExchangeTrader`

Trader ทำงานได้ทั้ง PAPER และ LIVE ตาม `wallet_type`:

```python
trader = Trader(wallet_manager=wm, wallet_type=WalletType.PAPER)
trader.execute_signal(signal)      # เปิด trade
trader.close_trade(symbol, price)  # ปิด trade
trader.check_stop_loss_take_profit(symbol, current_price)  # เช็ค SL/TP
trader.get_stats()                 # สถิติ
```

**For LIVE trades:** ใช้ `LiveExchangeTrader` (subclass) ที่ integrate กับ CCXT โดยตรง

---

### `backend/crypto/live_trader.py`

**Class:** `LiveExchangeTrader`

```python
trader = LiveExchangeTrader(wallet_manager=wm, exchange=exchange)
trader.refresh_live_balance()   # ดึงยอดจริงจาก exchange
trader.execute_signal(signal)    # PLACE REAL ORDER บน Binance
trader.close_trade(symbol)      # ปิด position จริง
```

---

### `backend/ai/signal_generator.py`

**Class:** `AISignalGenerator` — **ใช้ MiniMax เป็น AI provider**

```
Input: symbol, asset_type, market_data, analysis_text
  ↓
Build prompt (Thai system prompt)
  ↓
MiniMax Chat Completions API (OpenAI-compatible)
  ↓
Parse JSON response
  ↓
If confidence >= threshold → return TradeSignal
Else → return None (no trade)
```

**Prompt:** ภาษาไทย — รวม market data + news sentiment + technical analysis

**Fallback mode:** When MiniMax unavailable, generates BUY/SELL with confidence 0.6–0.9 and simple SL/TP at ±2% / ±5%

**MiniMax Client:** `backend/ai/minimax_client.py` — OpenAI-compatible wrapper สำหรับ `https://api.minimax.io/v1`

---

### `backend/crypto/exchange.py`

**Class:** `CryptoExchange`

CCXT wrapper providing:
- `get_balance(currency)` — fetch wallet balance from exchange
- `get_ticker(symbol)` — current price, bid/ask, volume
- `get_ohlcv(symbol, timeframe, limit)` — candlestick data
- `place_order(symbol, type, side, amount, price)` — execute real trade
- `cancel_order(order_id, symbol)` — cancel pending order
- `get_open_orders(symbol)` — list active orders

**Testnet:** `https://testnet.binance.vision/api` (used when `testnet=True`)

---

### `backend/gold/price_feed.py`

**Class:** `GoldPriceFeed`

Real-time gold (XAUUSD) price feed:

- **Default:** Alpha Vantage API — ดึงราคาจริง
- **Fallback:** Demo data ถ้าไม่มี API key หรือ API rate limit
- Cache 60 วินาที เพื่อไม่ hammering API

```python
gold = GoldPriceFeed()
gold.get_current_price()  # float: 2345.50
gold.get_price()          # dict: {"price": 2345.5, "bid": 2345.0, "ask": 2346.0}
gold.is_demo             # True if using demo data
```

---

### `backend/core/trade_logger.py`

**Class:** `TradeLogger`

SQLite schema:
```sql
trades (
  id, symbol, asset_type, wallet_type,
  direction, entry_price, exit_price, quantity,
  stop_loss, take_profit,
  status, entry_time, exit_time,
  trade_number, created_at
)
```

Key queries:
- `log_trade()` — INSERT new trade
- `update_trade()` — UPDATE exit_price, status, exit_time
- `get_open_trades(wallet_type)` — WHERE status = 'open' + filter by wallet
- `get_trade_stats(wallet_type)` — win rate, total P&L, filter by wallet
- `get_trade_history(wallet_type)` — ดึง history แยกตามกระเป๋า
- `get_next_trade_number(symbol, wallet_type)` — "ไม้ที่เท่าไหร่" + wallet type

---

## Data Flow: Signal → Trade → P&L

```
1. Cron/system triggers check
2. exchange.get_ticker("BTC/USDT") → market_data (real price)
3. ai.analyze_market(price_data) → analysis_text
4. ai.generate_signal("BTC/USDT", CRYPTO, market_data, analysis)
   → TradeSignal or None
5. If signal:
   trader.execute_signal(signal)
   → Trade created, balance deducted
6. Loop: check_stop_loss_take_profit every tick
   → close_trade when SL/TP hit
7. P&L calculated, balance updated
8. Stats tracked per wallet_type (PAPER or LIVE)
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
- Dashboard: balance (PAPER + LIVE), open trades, P&L
- Trade history: past trades with stats filtered by wallet
- Settings: API keys, thresholds, symbols
- Real-time updates via polling or WebSocket

---

## API Endpoints (FastAPI)

| Endpoint | Method | Description |
|---|---|---|
| `/api/trader/start` | POST | Start auto-trader (mode: paper/live) |
| `/api/trader/stop` | POST | Stop auto-trader |
| `/api/trader/stats` | GET | Trader running stats |
| `/api/wallets` | GET | **Both wallet balances (PAPER + LIVE)** |
| `/api/balance` | GET | Single wallet balance (query: ?wallet_type=paper\|live) |
| `/api/stats` | GET | Trade stats (query: ?wallet_type=paper\|live) |
| `/api/trades` | GET | Trade history (query: ?wallet_type=paper\|live) |
| `/api/trades/open` | GET | Open positions (query: ?wallet_type=paper\|live) |
| `/api/tickers` | GET | Real-time prices (no more mock data) |
| `/api/ticker/{symbol}` | GET | Single asset price |
| `/api/settings` | GET/PATCH | Trading settings |
| `/api/news/feed` | GET | News intelligence feed |

---

## Configuration

See `config/settings.yaml`:

```yaml
wallets:
  paper:
    initial_balance: 100000.0
    currency: "USDT"
  live:
    currency: "USDT"
    enabled: true

data:
  gold:
    provider: "alpha_vantage"
    api_key: "${ALPHA_VANTAGE_API_KEY}"
  crypto:
    provider: "binance"
    testnet: false

exchange:
  binance:
    api_key: "${BINANCE_API_KEY}"
    api_secret: "${BINANCE_API_SECRET}"
```

**Required env vars:**
- `ALPHA_VANTAGE_API_KEY` — gold real data
- `BINANCE_API_KEY` + `BINANCE_API_SECRET` — live crypto trading
- `OPENAI_API_KEY` — AI signal generation
