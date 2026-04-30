"""
api/server.py — FastAPI Server สำหรับ Auto Trade AI
======================================================
เป็น REST API layer เชื่อมระหว่าง Frontend (Next.js) กับ Backend (Python trading engine)

รัน: uvicorn api.server:app --reload --port 8000

Endpoints:
  GET  /api/health               — health check
  GET  /api/trader/status        — trader running status
  POST /api/trader/start         — start auto-trader
  POST /api/trader/stop          — stop auto-trader
  GET  /api/trader/stats         — real-time trading stats
  GET  /api/balance              — current balance
  GET  /api/stats                — trade statistics
  GET  /api/trades               — trade history
  GET  /api/trades/open          — open positions
  POST /api/trades/close         — close a position
  POST /api/trade/execute        — execute a signal manually
  GET  /api/tickers              — all asset prices
  GET  /api/ticker/{symbol}      — single asset price
  GET  /api/exchange-rates       — THB exchange rates
  GET  /api/settings              — get settings
  POST /api/settings             — update settings
  POST /api/trades               — create a manual trade
"""

import asyncio
import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import sys
import sqlite3

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# ── Logging ────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── FastAPI App ─────────────────────────────────────────────
app = FastAPI(
    title="Auto Trade AI API",
    description="REST API สำหรับควบคุม Auto Trade AI trading system",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ใน production ควรจำกัดเฉพาะ frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Models ─────────────────────────────────────────
class TraderStartRequest(BaseModel):
    mode: str = Field(default="paper", description="paper หรือ live")
    asset: str = Field(default="both", description="crypto, gold, หรือ both")
    symbols: list[str] = Field(default=["BTC/USDT", "ETH/USDT", "XAUUSD"])
    balance: float = Field(default=100000, description="initial balance สำหรับ paper mode")

class TradeCloseRequest(BaseModel):
    symbol: str
    exit_price: float

class ManualTradeRequest(BaseModel):
    symbol: str
    direction: str = Field(description="buy หรือ sell")
    quantity: float
    entry_price: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None

class SettingsUpdateRequest(BaseModel):
    max_position_size: Optional[float] = None
    stop_loss_percent: Optional[float] = None
    take_profit_percent: Optional[float] = None
    max_concurrent_trades: Optional[int] = None

# ── Database ───────────────────────────────────────────────
DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)
TRADES_DB = DATA_DIR / "trades.db"
EXCHANGE_DB = DATA_DIR / "exchange_rates.db"

def get_db():
    """สร้าง connection สำหรับ trades DB"""
    conn = sqlite3.connect(TRADES_DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_trades_db():
    """สร้างตาราง trades ถ้ายังไม่มี"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                direction TEXT NOT NULL,
                entry_price REAL,
                exit_price REAL,
                quantity REAL,
                stop_loss REAL,
                take_profit REAL,
                status TEXT DEFAULT 'open',
                entry_time TEXT,
                exit_time TEXT,
                trade_number INTEGER,
                pnl REAL,
                pnl_percent REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        # default settings
        defaults = {
            "max_position_size": "0.1",
            "stop_loss_percent": "2.0",
            "take_profit_percent": "5.0",
            "max_concurrent_trades": "3",
        }
        for k, v in defaults.items():
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
        conn.commit()
    logger.info(f"Trades DB initialized at {TRADES_DB}")

# ── Trader State (in-memory) ────────────────────────────────
class TraderState:
    """เก็บสถานะของ auto-trader process"""

    running: bool = False
    mode: str = "paper"
    asset: str = "both"
    symbols: list[str] = ["BTC/USDT", "ETH/USDT", "XAUUSD"]
    balance: float = 100000.0
    initial_balance: float = 100000.0
    process: Optional[threading.Thread] = None
    stop_event: threading.Event = threading.Event()

    # real-time stats
    total_trades: int = 0
    winning_trades: int = 0
    losing_trades: int = 0

    def start(self, mode: str, asset: str, symbols: list, balance: float):
        if self.running:
            raise RuntimeError("Trader is already running")
        self.mode = mode
        self.asset = asset
        self.symbols = symbols
        self.balance = balance
        self.initial_balance = balance
        self.running = True
        self.stop_event.clear()

        # เริ่ม trader loop ใน background thread
        self.process = threading.Thread(target=self._run_loop, daemon=True)
        self.process.start()
        logger.info(f"Trader started: mode={mode}, asset={asset}, balance=${balance}")

    def stop(self):
        if not self.running:
            return
        self.stop_event.set()
        self.running = False
        if self.process and self.process.is_alive():
            self.process.join(timeout=5)
        logger.info("Trader stopped")

    def _run_loop(self):
        """Background loop ที่ทำหน้าที่ auto-trader"""
        # Import ที่นี่เพื่อหลีกเลี่ยง circular import
        from backend.core.paper_trader import PaperTrader
        from backend.crypto.exchange import CryptoExchange
        from backend.gold.price_feed import GoldPriceFeed
        from backend.ai.signal_generator import AISignalGenerator
        from backend.core.models import AssetType

        trader = PaperTrader(initial_balance=self.balance)
        ai = AISignalGenerator()
        exchange = CryptoExchange(testnet=(self.mode == "paper"))
        gold = GoldPriceFeed(source="demo")

        symbols_to_trade = self.symbols

        while not self.stop_event.is_set():
            for symbol in symbols_to_trade:
                try:
                    if "XAU" in symbol:
                        # Gold
                        price_data = gold.get_price(symbol)
                    else:
                        # Crypto
                        ticker = exchange.get_ticker(symbol)
                        if not ticker:
                            continue
                        price_data = {
                            "price": ticker.get("last"),
                            "high": ticker.get("high"),
                            "low": ticker.get("low"),
                        }

                    signal = ai.generate_signal(
                        symbol=symbol,
                        asset_type=AssetType.GOLD if "XAU" in symbol else AssetType.CRYPTO,
                        market_data=price_data,
                    )

                    if signal:
                        # ประมวลผลสัญญาณผ่าน paper trader
                        if signal.direction.value == "buy":
                            result = trader.execute_signal(signal)
                            logger.info(f"SIGNAL BUY: {symbol} @ {signal.entry_price}, qty={signal.quantity}")
                        elif signal.direction.value == "sell":
                            result = trader.close_trade(symbol, price_data.get("price"))
                            logger.info(f"SIGNAL SELL: {symbol} @ {price_data.get('price')}")

                        # อัปเดต stats
                        self._refresh_stats(trader)

                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")

            # รอก่อนรอบถัดไป
            for _ in range(15):  # ทุก 15 วินาที
                if self.stop_event.is_set():
                    break
                time.sleep(1)

    def _refresh_stats(self, trader):
        stats = trader.get_stats()
        self.balance = stats.get("current_balance", self.balance)
        self.total_trades = stats.get("total_trades", self.total_trades)
        self.winning_trades = stats.get("winning_trades", self.winning_trades)
        self.losing_trades = stats.get("losing_trades", self.losing_trades)

    def get_status(self) -> dict:
        return {
            "running": self.running,
            "mode": self.mode,
            "asset": self.asset,
            "symbols": self.symbols,
            "balance": self.balance,
            "initial_balance": self.initial_balance,
        }

    def get_stats(self) -> dict:
        return {
            "current_balance": self.balance,
            "initial_balance": self.initial_balance,
            "total_pnl": self.balance - self.initial_balance,
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": f"{int(self.winning_trades / self.total_trades * 100)}%" if self.total_trades > 0 else "0%",
        }

# Global trader state
trader_state = TraderState()

# ── Initialize DB on startup ────────────────────────────────
init_trades_db()

# ── Health ──────────────────────────────────────────────────
@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# ── Trader Control ──────────────────────────────────────────
@app.get("/api/trader/status")
async def get_trader_status():
    return trader_state.get_status()

@app.post("/api/trader/start")
async def start_trader(req: TraderStartRequest):
    try:
        trader_state.start(
            mode=req.mode,
            asset=req.asset,
            symbols=req.symbols,
            balance=req.balance,
        )
        return {"success": True, "message": "Trader started", **trader_state.get_status()}
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/trader/stop")
async def stop_trader():
    trader_state.stop()
    return {"success": True, "message": "Trader stopped"}

@app.get("/api/trader/stats")
async def get_trader_stats():
    return trader_state.get_stats()

# ── Balance ────────────────────────────────────────────────
@app.get("/api/balance")
async def get_balance():
    status = trader_state.get_status()
    return {
        "balance": status["balance"],
        "currency": "USDT",
        "initial_balance": status["initial_balance"],
        "total_pnl": status["balance"] - status["initial_balance"],
        "active_trades": _count_open_trades(),
    }

def _count_open_trades() -> int:
    with get_db() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM trades WHERE status = 'open'")
        return cur.fetchone()[0]

# ── Stats ──────────────────────────────────────────────────
@app.get("/api/stats")
async def get_stats():
    with get_db() as conn:
        conn.row_factory = sqlite3.Row

        # Calculate P&L from exit_price - entry_price (direction-aware)
        row = conn.execute("""
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN (exit_price > entry_price AND direction = 'buy')
                         OR (exit_price < entry_price AND direction = 'sell') THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN (exit_price < entry_price AND direction = 'buy')
                         OR (exit_price > entry_price AND direction = 'sell') THEN 1 ELSE 0 END) as losses,
                SUM(CASE WHEN (exit_price > entry_price AND direction = 'buy')
                         OR (exit_price < entry_price AND direction = 'sell')
                         THEN exit_price - entry_price
                         ELSE entry_price - exit_price END) as total_pnl
            FROM trades WHERE status = 'closed'
        """).fetchone()

        total = row["total"] or 0
        wins = row["wins"] or 0
        losses = row["losses"] or 0
        total_pnl = row["total_pnl"] or 0

        status = trader_state.get_status()

        return {
            "total_trades": total,
            "winning_trades": wins,
            "losing_trades": losses,
            "win_rate": f"{int(wins / total * 100)}%" if total > 0 else "0%",
            "total_pnl": total_pnl,
            "current_balance": status["balance"],
        }

# ── Trades ─────────────────────────────────────────────────
@app.get("/api/trades")
async def get_trades(limit: int = 50):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT * FROM trades
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()
        return [_row_to_trade(r) for r in rows]

@app.get("/api/trades/open")
async def get_open_trades():
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM trades WHERE status = 'open'").fetchall()
        return [_row_to_trade(r) for r in rows]

@app.post("/api/trades/close")
async def close_trade(req: TradeCloseRequest):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        trade = conn.execute(
            "SELECT * FROM trades WHERE symbol = ? AND status = 'open' LIMIT 1",
            (req.symbol,),
        ).fetchone()

        if not trade:
            raise HTTPException(status_code=404, detail=f"No open trade for {req.symbol}")

        pnl = (req.exit_price - trade["entry_price"]) * trade["quantity"]
        pnl_pct = (req.exit_price - trade["entry_price"]) / trade["entry_price"] * 100

        conn.execute("""
            UPDATE trades
            SET status = 'closed',
                exit_price = ?,
                exit_time = ?,
                pnl = ?,
                pnl_percent = ?
            WHERE id = ?
        """, (req.exit_price, datetime.now().isoformat(), pnl, pnl_pct, trade["id"]))
        conn.commit()

        # อัปเดต trader state balance
        status = trader_state.get_status()
        trader_state.balance += pnl

        return _row_to_trade({**dict(trade), "exit_price": req.exit_price, "status": "closed", "pnl": pnl, "pnl_percent": pnl_pct})

@app.post("/api/trade/execute")
async def execute_trade(signal: dict):
    """รับ signal dict แล้วสร้าง trade ใหม่"""
    from backend.ai.signal_generator import AISignalGenerator
    from backend.core.models import AssetType, TradeDirection

    symbol = signal.get("symbol")
    direction = signal.get("direction", "buy")
    quantity = float(signal.get("quantity", 0.01))

    # ดึงราคาปัจจุบัน
    from backend.crypto.exchange import CryptoExchange
    from backend.gold.price_feed import GoldPriceFeed

    if "XAU" in symbol:
        gold = GoldPriceFeed(source="demo")
        price_data = gold.get_price(symbol)
        price = price_data.get("price")
        asset_type = "gold"
    else:
        exchange = CryptoExchange(testnet=True)
        ticker = exchange.get_ticker(symbol)
        price = ticker.get("last") if ticker else signal.get("entry_price", 0)
        asset_type = "crypto"

    with get_db() as conn:
        trade_num = conn.execute("SELECT COALESCE(MAX(trade_number), 0) + 1 as next_num FROM trades").fetchone()["next_num"]

        conn.execute("""
            INSERT INTO trades (symbol, asset_type, direction, entry_price, quantity, status, entry_time, trade_number)
            VALUES (?, ?, ?, ?, ?, 'open', ?, ?)
        """, (symbol, asset_type, direction, price, quantity, datetime.now().isoformat(), trade_num))
        conn.commit()

        row = conn.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 1").fetchone()
        return _row_to_trade(row)

@app.post("/api/trades")
async def create_manual_trade(req: ManualTradeRequest):
    """สร้าง trade ด้วยมือ (manual entry)"""
    from backend.gold.price_feed import GoldPriceFeed
    from backend.crypto.exchange import CryptoExchange

    symbol = req.symbol
    if "XAU" in symbol:
        gold = GoldPriceFeed(source="demo")
        price_data = gold.get_price(symbol)
        entry_price = req.entry_price or price_data.get("price")
        asset_type = "gold"
    else:
        exchange = CryptoExchange(testnet=True)
        ticker = exchange.get_ticker(symbol)
        entry_price = req.entry_price or ticker.get("last") if ticker else 0
        asset_type = "crypto"

    with get_db() as conn:
        trade_num = conn.execute("SELECT COALESCE(MAX(trade_number), 0) + 1 as next_num FROM trades").fetchone()["next_num"]

        conn.execute("""
            INSERT INTO trades (symbol, asset_type, direction, entry_price, quantity, stop_loss, take_profit, status, entry_time, trade_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'open', ?, ?)
        """, (
            symbol, asset_type, req.direction,
            entry_price, req.quantity,
            req.stop_loss, req.take_profit,
            datetime.now().isoformat(), trade_num,
        ))
        conn.commit()

        row = conn.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 1").fetchone()
        return _row_to_trade(row)

def _row_to_trade(row: dict) -> dict:
    return {
        "id": row["id"],
        "symbol": row["symbol"],
        "asset_type": row["asset_type"],
        "direction": row["direction"],
        "entry_price": row["entry_price"],
        "exit_price": row["exit_price"],
        "quantity": row["quantity"],
        "stop_loss": row["stop_loss"],
        "take_profit": row["take_profit"],
        "status": row["status"],
        "entry_time": row["entry_time"],
        "exit_time": row["exit_time"],
        "trade_number": row["trade_number"],
        "pnl": row["pnl"],
        "pnl_percent": row["pnl_percent"],
    }

# ── Tickers ────────────────────────────────────────────────
@app.get("/api/tickers")
async def get_tickers():
    # Mock fallback data — ใช้เมื่อ exchange APIs ไม่สามารถเชื่อมต่อได้
    MOCK_TICKERS = {
        "BTC/USDT": {"symbol": "BTC/USDT", "price": 68250, "bid": 68240, "ask": 68260, "high": 68800, "low": 67800, "volume": 25000},
        "ETH/USDT": {"symbol": "ETH/USDT", "price": 3480, "bid": 3478, "ask": 3482, "high": 3520, "low": 3430, "volume": 180000},
        "SOL/USDT": {"symbol": "SOL/USDT", "price": 96, "bid": 95.8, "ask": 96.2, "high": 99, "low": 94, "volume": 500000},
        "XAUUSD": {"symbol": "XAUUSD", "price": 2035, "bid": 2034.5, "ask": 2035.5, "high": 2040, "low": 2020, "volume": 0},
    }

    result = {}

    try:
        from backend.crypto.exchange import CryptoExchange
        from backend.gold.price_feed import GoldPriceFeed

        exchange = CryptoExchange(testnet=True)
        gold = GoldPriceFeed(source="demo")

        for symbol in ["BTC/USDT", "ETH/USDT", "SOL/USDT"]:
            try:
                ticker = exchange.get_ticker(symbol)
                if ticker:
                    result[symbol] = {
                        "symbol": symbol,
                        "price": ticker.get("last"),
                        "bid": ticker.get("bid"),
                        "ask": ticker.get("ask"),
                        "high": ticker.get("high"),
                        "low": ticker.get("low"),
                        "volume": ticker.get("base_volume"),
                    }
            except Exception:
                pass  # ไม่สน ข้ามไป

        try:
            gold_data = gold.get_price("XAUUSD")
            if gold_data:
                result["XAUUSD"] = {
                    "symbol": "XAUUSD",
                    "price": gold_data.get("price"),
                    "bid": gold_data.get("price") - 0.5,
                    "ask": gold_data.get("price") + 0.5,
                    "high": gold_data.get("high"),
                    "low": gold_data.get("low"),
                    "volume": 0,
                }
        except Exception:
            pass

    except Exception as e:
        logger.warning(f"Exchange init failed: {e}")

    # Fallback เป็น mock data หากไม่ได้ข้อมูลจริง
    if not result:
        result = MOCK_TICKERS

    return result

@app.get("/api/ticker/{symbol}")
async def get_ticker(symbol: str):
    tickers = await get_tickers()
    decoded = symbol.replace("%2F", "/")
    if decoded not in tickers:
        raise HTTPException(status_code=404, detail=f"Ticker {decoded} not found")
    return tickers[decoded]

# ── Exchange Rates ─────────────────────────────────────────
@app.get("/api/exchange-rates")
async def get_exchange_rates():
    """ดึงอัตราแลกเปลี่ยนจาก DB หรือ API"""
    try:
        import requests
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        rates = data.get("rates", {})
        result = {
            "USD/THB": rates.get("THB", 35.0),
            "EUR/THB": rates.get("EUR", 38.5) / rates.get("USD", 1) * rates.get("THB", 35.0),
            "GBP/THB": rates.get("GBP", 44.5) / rates.get("USD", 1) * rates.get("THB", 35.0),
            "JPY/THB": rates.get("JPY", 160) / rates.get("USD", 1) * rates.get("THB", 35.0),
            "lastUpdated": data.get("date"),
        }
        return result
    except Exception:
        # Fallback ไปดึงจาก DB
        try:
            import requests as req
            conn = sqlite3.connect(EXCHANGE_DB)
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT * FROM exchange_rates
                WHERE base_currency = 'USD' AND quote_currency = 'THB'
                ORDER BY date DESC LIMIT 1
            """).fetchone()
            conn.close()
            if row:
                return {"USD/THB": row["rate"], "lastUpdated": row["date"]}
        except:
            pass
        return {"USD/THB": 35.0, "EUR/THB": 38.5, "GBP/THB": 44.5, "JPY/THB": 0.235, "lastUpdated": None}

# ── Settings ────────────────────────────────────────────────
@app.get("/api/settings")
async def get_settings():
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM settings").fetchall()
        return {r["key"]: r["value"] for r in rows}

@app.post("/api/settings")
async def update_settings(req: SettingsUpdateRequest):
    with get_db() as conn:
        for key, value in req.model_dump(exclude_none=True).items():
            conn.execute(
                "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
                (key, str(value)),
            )
        conn.commit()
    return {"success": True, "message": "Settings updated"}

# ── Run Server ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
