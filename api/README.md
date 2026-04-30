# Auto Trade AI — API Server

REST API layer ที่เชื่อมระหว่าง **Frontend (Next.js)** กับ **Backend (Python trading engine)**

## Quick Start

```bash
# ติดตั้ง dependencies
pip install -r api/requirements.txt

# รัน API server
uvicorn api.server:app --reload --port 8000

# หรือใช้ startup script
chmod +x run.sh && ./run.sh
```

API จะรันที่ `http://localhost:8000`

---

## API Documentation

เปิด **Swagger UI** อัตโนมัติที่: `http://localhost:8000/docs`

## Endpoints

### Trader Control

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/trader/status` | สถานะ trader (running/stopped) |
| `POST` | `/api/trader/start` | เริ่ม auto-trader |
| `POST` | `/api/trader/stop` | หยุด auto-trader |
| `GET` | `/api/trader/stats` | สถิติ real-time |

**Start Trader Body:**
```json
{
  "mode": "paper",
  "asset": "both",
  "symbols": ["BTC/USDT", "ETH/USDT", "XAUUSD"],
  "balance": 100000
}
```

### Trading

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/trades` | ประวัติ trades |
| `GET` | `/api/trades/open` | positions ที่เปิดอยู่ |
| `POST` | `/api/trades/close` | ปิด position |
| `POST` | `/api/trades` | สร้าง trade ด้วยมือ |
| `POST` | `/api/trade/execute` | execute signal จาก AI |

### Market Data

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/tickers` | ราคาทั้งหมด |
| `GET` | `/api/ticker/{symbol}` | ราคาเฉพาะ asset |
| `GET` | `/api/exchange-rates` | อัตราแลกเปลี่ยน THB |

### Balance & Stats

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/balance` | balance + P&L |
| `GET` | `/api/stats` | สถิติ trading |

### Settings

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/settings` | ดู settings ปัจจุบัน |
| `POST` | `/api/settings` | อัปเดต settings |

---

## Architecture

```
┌─────────────────┐         ┌────────────────────┐
│  Next.js        │  HTTP   │   FastAPI Server   │
│  Frontend       │ ──────► │   (api/server.py)  │
│  :3000          │         │   :8000            │
└─────────────────┘         └────────┬───────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
           ┌────────────┐  ┌────────────────┐  ┌──────────┐
           │ CCXT       │  │ Gold Price     │  │ AI       │
           │ Exchange   │  │ Feed           │  │ Signal   │
           │ (Crypto)   │  │ (XAUUSD)      │  │ Generator│
           └────────────┘  └────────────────┘  └──────────┘
                    └────────────────┬────────────────┘
                                     ▼
                            ┌────────────────┐
                            │ PaperTrader    │
                            │ (SQLite logs)  │
                            └────────────────┘
```

## Frontend Connection

Frontend ตั้ง `USE_MOCK = false` ใน `frontend/src/lib/api.ts` แล้วตั้ง env:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

หรือรันทั้งสองพร้อมกัน:
```bash
./run.sh
```

## Database

ข้อมูลถูกเก็บใน SQLite:
- `data/trades.db` — trade history + settings
- `data/exchange_rates.db` — อัตราแลกเปลี่ยน (จาก scraper)

## CORS

API server อนุญาตทุก origin ใน development (`allow_origins=["*"]`) — ควรจำกัดใน production ให้เฉพาะ `http://localhost:3000`
