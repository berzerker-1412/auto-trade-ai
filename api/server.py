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
    wallet_type: str = Field(default="paper", description="paper หรือ live — กระเป๋าตังที่จะใช้")

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
    wallet_type: str = Field(default="paper", description="paper หรือ live")

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
                wallet_type TEXT NOT NULL DEFAULT 'paper',
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
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_trades_wallet_type 
            ON trades(wallet_type)
        """)
        # wallet_transactions: ประวัติ deposit/withdraw
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wallet_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                wallet_type TEXT NOT NULL DEFAULT 'paper',
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                note TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_wallet_tx_type
            ON wallet_transactions(wallet_type, type)
        """)
        # default settings
        defaults = {
            "max_position_size": "0.1",
            "stop_loss_percent": "2.0",
            "take_profit_percent": "5.0",
            "max_concurrent_trades": "3",
            "paper_initial_balance": "100000.0",
        }
        for k, v in defaults.items():
            conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
        conn.commit()
    logger.info(f"Trades DB initialized at {TRADES_DB}")

# ── Wallet Persistence ───────────────────────────────────────
def _get_setting(key: str, default: str = None) -> Optional[str]:
    """ดึงค่า setting จาก DB"""
    with get_db() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        return row[0] if row else default

def _set_setting(key: str, value: str):
    """บันทึกค่า setting ลง DB"""
    with get_db() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, str(value)))
        conn.commit()

def get_wallet_balance(wallet_type: str = "paper") -> float:
    """ดึง balance ปัจจุบัน = initial + deposits - withdrawals + total_pnl"""
    initial = float(_get_setting(f"{wallet_type}_initial_balance", "100000.0"))
    with get_db() as conn:
        rows = conn.execute("""
            SELECT type, SUM(amount) as total
            FROM wallet_transactions
            WHERE wallet_type = ?
            GROUP BY type
        """, (wallet_type,)).fetchall()
        tx = {r[0]: r[1] for r in rows}

        deposits = tx.get("deposit", 0.0)
        withdrawals = tx.get("withdraw", 0.0)

        # รวม P&L จาก trades ที่ปิดแล้ว
        pnl_row = conn.execute("""
            SELECT COALESCE(SUM(pnl), 0) FROM trades
            WHERE wallet_type = ? AND status = 'closed' AND pnl IS NOT NULL
        """, (wallet_type,)).fetchone()
        total_pnl = pnl_row[0] if pnl_row else 0.0

    return initial + deposits - withdrawals + total_pnl

def add_wallet_transaction(
    wallet_type: str,
    tx_type: str,
    amount: float,
    note: str = None
) -> int:
    """บันทึก deposit หรือ withdraw ลง DB คืนค่า transaction id"""
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO wallet_transactions (wallet_type, type, amount, note, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (wallet_type, tx_type, amount, note, datetime.now().isoformat()))
        conn.commit()
        return cursor.lastrowid

def get_wallet_transactions(
    wallet_type: str = "paper",
    limit: int = 50
) -> list:
    """ดึงประวัติ deposit/withdraw"""
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT id, wallet_type, type, amount, note, created_at
            FROM wallet_transactions
            WHERE wallet_type = ?
            ORDER BY id DESC
            LIMIT ?
        """, (wallet_type, limit)).fetchall()
        return [_row_to_dict(r) for r in rows]

def _row_to_dict(row) -> dict:
    """Convert sqlite3.Row to dict with string keys"""
    if row is None:
        return None
    if hasattr(row, "keys"):
        return dict(zip(row.keys(), row))
    return dict(row)

def get_wallet_summary(wallet_type: str = "paper") -> dict:
    """สรุปยอดกระเป๋า: balance, initial, deposits, withdrawals, pnl"""
    initial = float(_get_setting(f"{wallet_type}_initial_balance", "100000.0"))
    with get_db() as conn:
        rows = conn.execute("""
            SELECT type, SUM(amount) as total
            FROM wallet_transactions
            WHERE wallet_type = ?
            GROUP BY type
        """, (wallet_type,)).fetchall()
        tx = {r[0]: r[1] for r in rows}

        deposits = tx.get("deposit", 0.0)
        withdrawals = tx.get("withdraw", 0.0)

        pnl_row = conn.execute("""
            SELECT COALESCE(SUM(pnl), 0), COUNT(*)
            FROM trades
            WHERE wallet_type = ? AND status = 'closed' AND pnl IS NOT NULL
        """, (wallet_type,)).fetchone()
        total_pnl = pnl_row[0] if pnl_row else 0.0
        closed_trades = pnl_row[1] if pnl_row else 0

    current_balance = initial + deposits - withdrawals + total_pnl

    return {
        "wallet_type": wallet_type,
        "current_balance": round(current_balance, 2),
        "initial_balance": round(initial, 2),
        "total_deposits": round(deposits, 2),
        "total_withdrawals": round(withdrawals, 2),
        "total_pnl": round(total_pnl, 2),
        "closed_trades": closed_trades,
        "currency": "THB",
    }

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

        wallet_type = "paper" if mode == "paper" else "live"
        # โหลด balance จาก DB (รวม deposits/withdrawals/P&L ที่เก็บไว้)
        computed = get_wallet_balance(wallet_type)
        # balance ที่โหลดได้ = ยอดจริงในกระเป๋า
        # ถ้า computed == initial (100k มาตรฐาน) แสดงว่าเริ่มใหม่ — ใช้ balance ที่ใส่มาเป็น initial
        self.initial_balance = computed
        self.balance = computed
        # บันทึก initial_balance ลง DB เฉพาะครั้งแรกเท่านั้น (ไม่เขียนทับหลัง deposit/withdraw)
        existing = _get_setting(f"{wallet_type}_initial_balance")
        if existing is None:
            _set_setting(f"{wallet_type}_initial_balance", str(computed))

        self.running = True
        self.stop_event.clear()

        # เริ่ม trader loop ใน background thread
        self.process = threading.Thread(target=self._run_loop, daemon=True)
        self.process.start()
        logger.info(f"Trader started: mode={mode}, asset={asset}, balance={computed}")

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
        from backend.core.trader import Trader
        from backend.core.wallet_manager import WalletManager
        from backend.core.models import WalletType
        from backend.crypto.exchange import CryptoExchange
        from backend.gold.price_feed import GoldPriceFeed
        from backend.ai.signal_generator import AISignalGenerator
        from backend.core.models import AssetType

        is_live = self.mode == "live"

        # สร้าง WalletManager แยกกระเป๋าตัง
        wm = WalletManager(paper_initial=self.balance)
        wallet_type = WalletType.LIVE if is_live else WalletType.PAPER

        # Paper mode: ใช้ real Binance public API สำหรับราคา (paper trade จริงไม่ execute)
        # Live mode: ใช้ real API พร้อม API key
        exchange = CryptoExchange(testnet=False)

        # Gold ใช้ real API เสมอ (demo เฉพาะถ้า API key ไม่มีจริง)
        gold = GoldPriceFeed()

        # สร้าง Trader ตาม wallet type
        trader = Trader(
            wallet_manager=wm,
            db_path=str(TRADES_DB),
            wallet_type=wallet_type,
        )
        ai = AISignalGenerator()

        symbols_to_trade = self.symbols
        news_signal_cache = None  # เก็บ news signal ไว้ใช้รอบนึง
        last_news_fetch = 0  # timestamp ล่าสุดที่ fetch news

        while not self.stop_event.is_set():
            # ── ดึง news signal ทุก 5 นาที ──────────────────────
            try:
                if time.time() - last_news_fetch > 300:  # 5 นาที
                    from scraper.news_scraper import get_articles
                    from scraper.sentiment import get_trade_signal
                    articles = get_articles(limit=100)
                    news_signal_cache = get_trade_signal(articles)
                    last_news_fetch = time.time()
                    logger.info(f"[News] Fetched signal: bias={news_signal_cache.get('bias')}, score={news_signal_cache.get('score')}")
            except Exception as e:
                logger.warning(f"[News] Failed to fetch news signal: {e}")
                news_signal_cache = None

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

                    # ── สร้าง signal โดยส่ง news sentiment ด้วย ───────
                    signal = ai.generate_signal(
                        symbol=symbol,
                        asset_type=AssetType.GOLD if "XAU" in symbol else AssetType.CRYPTO,
                        market_data=price_data,
                        news_signal=news_signal_cache,
                    )

                    if signal:
                        # ตรวจสอบว่ามี position อยู่แล้วหรือยัง
                        existing = trader.active_trades.get(symbol)
                        
                        # DB check: ป้องกัน race condition เมื่อ position เพิ่งถูกปิด
                        with get_db() as conn:
                            conn.row_factory = sqlite3.Row
                            db_open = conn.execute(
                                "SELECT 1 FROM trades WHERE symbol=? AND status='open' LIMIT 1",
                                (symbol,)).fetchone()
                        
                        if signal.direction.value == "buy":
                            # ซื้อได้เฉพาะเมื่อยังไม่มี position เปิดอยู่ (memory หรือ DB)
                            if existing is None and db_open is None:
                                result = trader.execute_signal(signal)
                                logger.info(f"SIGNAL BUY [{signal.reasoning}]: {symbol} @ {signal.entry_price}, qty={signal.quantity}")
                            else:
                                logger.info(f"[SKIP] {symbol} already has open position, skipping BUY signal")
                        elif signal.direction.value == "sell":
                            # ขายได้เฉพาะเมื่อมี position เปิดอยู่
                            if existing:
                                result = trader.close_trade(symbol, price_data.get("price"), "signal_sell")
                                logger.info(f"SIGNAL SELL [{signal.reasoning}]: {symbol} @ {price_data.get('price')}")
                            else:
                                logger.info(f"[SKIP] {symbol} no open position to sell")
                        
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
        # ดึง balance จาก DB เพื่อความถูกต้องเสมอ
        wtype = "paper" if self.mode == "paper" else "live"
        db_balance = get_wallet_balance(wtype)
        return {
            "running": self.running,
            "mode": self.mode,
            "asset": self.asset,
            "symbols": self.symbols,
            "balance": db_balance,
            "initial_balance": self.initial_balance,
        }

    def get_stats(self) -> dict:
        wtype = "paper" if self.mode == "paper" else "live"
        db_balance = get_wallet_balance(wtype)
        return {
            "current_balance": db_balance,
            "initial_balance": self.initial_balance,
            "total_pnl": db_balance - self.initial_balance,
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
class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0, description="จำนวนเงินที่เติม")
    note: Optional[str] = Field(default=None, description="หมายเหตุ")

class WithdrawRequest(BaseModel):
    amount: float = Field(..., gt=0, description="จำนวนเงินที่ถอน")
    note: Optional[str] = Field(default=None, description="หมายเหตุ")

@app.get("/api/balance")
async def get_balance(wallet_type: str = "paper"):
    """ดึงยอดกระเป๋าตัง — คำนวณจาก DB: initial + deposits - withdrawals + P&L"""
    return get_wallet_summary(wallet_type)

@app.get("/api/wallets")
async def get_all_wallets():
    """ดึงยอดทั้งสองกระเป๋าตัง (PAPER + LIVE)"""
    return {
        "paper": get_wallet_summary("paper"),
        "live": get_wallet_summary("live"),
    }

@app.post("/api/wallet/deposit")
async def deposit(req: DepositRequest, wallet_type: str = "paper"):
    """เติมเงินเข้ากระเป๋า — บันทึกลง DB แล้วอัปเดต balance"""
    if wallet_type not in ("paper", "live"):
        raise HTTPException(status_code=400, detail="wallet_type must be 'paper' or 'live'")

    tx_id = add_wallet_transaction(wallet_type, "deposit", req.amount, req.note)
    # อัปเดต in-memory balance
    trader_state.balance = get_wallet_balance(wallet_type)
    summary = get_wallet_summary(wallet_type)
    logger.info(f"[WALLET] Deposit {req.amount} to {wallet_type}: tx_id={tx_id}, new_balance={summary['current_balance']}")
    return {
        "success": True,
        "tx_id": tx_id,
        "new_balance": summary["current_balance"],
        "summary": summary,
    }

@app.post("/api/wallet/withdraw")
async def withdraw(req: WithdrawRequest, wallet_type: str = "paper"):
    """ถอนเงินออกจากกระเป๋า — บันทึกลง DB แล้วอัปเดต balance"""
    if wallet_type not in ("paper", "live"):
        raise HTTPException(status_code=400, detail="wallet_type must be 'paper' or 'live'")

    current = get_wallet_balance(wallet_type)
    if current < req.amount:
        raise HTTPException(status_code=400, detail=f"ไม่มีเงินเพียงพอ: มี {current:.2f} บาท")

    tx_id = add_wallet_transaction(wallet_type, "withdraw", req.amount, req.note)
    # อัปเดต in-memory balance
    trader_state.balance = get_wallet_balance(wallet_type)
    summary = get_wallet_summary(wallet_type)
    logger.info(f"[WALLET] Withdraw {req.amount} from {wallet_type}: tx_id={tx_id}, new_balance={summary['current_balance']}")
    return {
        "success": True,
        "tx_id": tx_id,
        "new_balance": summary["current_balance"],
        "summary": summary,
    }

@app.get("/api/wallet/transactions")
async def list_wallet_transactions(wallet_type: str = "paper", limit: int = 50):
    """ดูประวัติ deposit/withdraw"""
    return {
        "wallet_type": wallet_type,
        "transactions": get_wallet_transactions(wallet_type, limit),
    }

@app.get("/api/wallet/summary")
async def wallet_summary(wallet_type: str = "paper"):
    """สรุปยอดกระเป๋า: balance, initial, deposits, withdrawals, pnl"""
    return get_wallet_summary(wallet_type)

def _count_open_trades() -> int:
    with get_db() as conn:
        cur = conn.execute("SELECT COUNT(*) FROM trades WHERE status = 'open'")
        return cur.fetchone()[0]

# ── Stats ──────────────────────────────────────────────────
@app.get("/api/stats")
async def get_stats(wallet_type: str = None):
    """ดึงสถิติ trades — เลือก wallet_type ได้ (paper, live, หรือ None ทั้งหมด)"""
    from backend.core.trade_logger import TradeLogger
    from backend.core.models import WalletType

    wtype = WalletType(wallet_type) if wallet_type in ("paper", "live") else None

    logger = TradeLogger(str(TRADES_DB))
    stats = logger.get_trade_stats(wallet_type=wtype)

    return {
        "wallet_type": wtype.value if wtype else "all",
        "total_trades": stats.total_trades,
        "winning_trades": stats.winning_trades,
        "losing_trades": stats.losing_trades,
        "win_rate": f"{stats.win_rate:.1f}%",
        "total_pnl": stats.total_pnl,
    }

# ── Trades ─────────────────────────────────────────────────
@app.get("/api/trades")
async def get_trades(limit: int = 50, wallet_type: str = None):
    wallet_filter = ""
    params = [limit]
    if wallet_type in ("paper", "live"):
        wallet_filter = " AND wallet_type = ?"
        params.insert(0, wallet_type)

    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f"""
            SELECT * FROM trades
            WHERE 1=1{wallet_filter}
            ORDER BY id DESC
            LIMIT ?
        """, params).fetchall()
        return [_row_to_trade(r) for r in rows]

@app.get("/api/trades/open")
async def get_open_trades(wallet_type: str = None):
    wallet_filter = ""
    params = []
    if wallet_type in ("paper", "live"):
        wallet_filter = " AND wallet_type = ?"
        params.append(wallet_type)

    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(f"""
            SELECT * FROM trades WHERE status = 'open'{wallet_filter}
        """, params).fetchall()
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

        # อัปเดต trader state balance — โหลดจาก DB เพื่อความถูกต้อง
        trader_state.balance = get_wallet_balance(trade.get("wallet_type", "paper"))

        return _row_to_trade(trade)

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
        gold = GoldPriceFeed()
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

        wallet_type = signal.get("wallet_type", "paper")
        conn.execute("""
            INSERT INTO trades (symbol, asset_type, wallet_type, direction, entry_price, quantity, status, entry_time, trade_number)
            VALUES (?, ?, ?, ?, ?, ?, 'open', ?, ?)
        """, (symbol, asset_type, wallet_type, direction, price, quantity, datetime.now().isoformat(), trade_num))
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
        gold = GoldPriceFeed()
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

        wallet_type = req.wallet_type
        conn.execute("""
            INSERT INTO trades (symbol, asset_type, wallet_type, direction, entry_price, quantity, stop_loss, take_profit, status, entry_time, trade_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', ?, ?)
        """, (
            symbol, asset_type, wallet_type, req.direction,
            entry_price, req.quantity,
            req.stop_loss, req.take_profit,
            datetime.now().isoformat(), trade_num,
        ))
        conn.commit()

        row = conn.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 1").fetchone()
        return _row_to_trade(row)

def _row_to_trade(row) -> dict:
    """Convert sqlite3.Row or dict to trade dict with string keys."""
    if row is None:
        return None
    # sqlite3.Row: dict(row) gives {0:val, 1:val,...} — need column names
    if hasattr(row, "keys"):
        r = dict(zip(row.keys(), row))
    else:
        r = dict(row)
    return {
        "id": r.get("id"),
        "symbol": r.get("symbol"),
        "asset_type": r.get("asset_type"),
        "wallet_type": r.get("wallet_type", "paper"),
        "direction": r.get("direction"),
        "entry_price": r.get("entry_price"),
        "exit_price": r.get("exit_price"),
        "quantity": r.get("quantity"),
        "stop_loss": r.get("stop_loss"),
        "take_profit": r.get("take_profit"),
        "status": r.get("status"),
        "entry_time": r.get("entry_time"),
        "exit_time": r.get("exit_time"),
        "trade_number": r.get("trade_number"),
        "pnl": r.get("pnl"),
        "pnl_percent": r.get("pnl_percent"),
        "entry_reason": json.loads(r.get("entry_reason")) if r.get("entry_reason") else None,
        "exit_reason": json.loads(r.get("exit_reason")) if r.get("exit_reason") else None,
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

        # ใช้ real data — testnet ตาม mode ของ trader
        mode = trader_state.mode
        exchange = CryptoExchange(testnet=(mode == "paper"))
        gold = GoldPriceFeed()

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


# ── News / Intelligence Feed ────────────────────────────────
@app.get("/api/news/feed")
async def get_news_feed(limit: int = 50, category: str = None, source: str = None):
    """
    ดึงข่าวทั้งหมด + trade signal ที่สร้างจาก sentiment analysis

    Query params:
    - limit: จำนวนข่าว (default 50)
    - category: filter เช่น war, finance, crypto (optional)
    - source: filter เช่น Reuters, Bloomberg (optional)
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import get_articles, get_trade_signal
    except ImportError as e:
        logger.warning(f"Could not import news scraper: {e}")
        return {"articles": [], "trade_signal": None, "total": 0, "generated_at": datetime.now().isoformat()}

    try:
        articles = get_articles(limit=limit, category=category, source=source)
        trade_signal = get_trade_signal(articles)

        for art in articles:
            score = art.get("sentiment_score", 0)
            art["sentiment_label"] = (
                "positive" if score > 0.2
                else "negative" if score < -0.2
                else "neutral"
            )

        return {
            "articles": articles,
            "trade_signal": trade_signal,
            "total": len(articles),
            "generated_at": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Error getting news feed: {e}")
        raise HTTPException(status_code=500, detail=f"News feed error: {e}")


@app.get("/api/news/article/{article_id}")
async def get_news_article(article_id: int):
    """
    ดึงข่าวเดียว by ID พร้อมเนื้อหาเต็ม (แปลไทยแล้ว)
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import get_article_by_id
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    try:
        article = get_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        return article
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting article {article_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/news/scrape")
async def trigger_scrape():
    """
    สั่ง scrape ข่าวใหม่จากทุกแหล่ง
    ควรเรียกผ่าน cron job หรือปุ่ม manual scrape
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import NewsScraper
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    try:
        scraper = NewsScraper()
        result = scraper.scrape_all()
        return {
            "status": "ok",
            "total_saved": result["total_saved"],
            "sources_scraped": result["sources_scraped"],
            "errors": result.get("errors", []),
        }
    except Exception as e:
        logger.error(f"Scrape error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/signal")
async def get_trade_signal_endpoint():
    """
    ดึงเฉพาะ trade signal ที่สร้างจากข่าว
    ใช้สำหรับ AI signal generator ประกอบการตัดสินใจ
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import get_articles
        from scraper.sentiment import get_trade_signal
    except ImportError as e:
        return {"bias": "neutral", "score": 0.0, "signal": None}

    articles = get_articles(limit=100)
    signal = get_trade_signal(articles)
    return signal


# ── Archive Endpoints ────────────────────────────────────────

@app.post("/api/news/archive")
async def run_archive(retention_days: int = 7):
    """
    รัน archival process —ย้ายข่าวเก่าไป archive table
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import archive_old_articles
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    result = archive_old_articles(retention_days=retention_days)
    return result


@app.get("/api/news/archive")
async def get_archive(
    limit: int = 50,
    category: str = None,
    source: str = None,
):
    """
    ดึงข่าวจาก archive
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import get_archived_articles
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    articles = get_archived_articles(limit=limit, category=category, source=source)
    return {"articles": articles, "total": len(articles)}


@app.get("/api/news/archive/stats")
async def get_archive_stats():
    """
    ดึง archive stats
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import get_archive_stats
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    return get_archive_stats()


@app.patch("/api/news/archive/policy")
async def update_archive_policy(retention_days: int = 7):
    """
    ตั้ง retention period (จำนวนวันที่เก็บข่าวใน main table)
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import set_archive_retention
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    return set_archive_retention(days=retention_days)


# ── AI Translation & Impact Analysis ─────────────────────────────

@app.post("/api/news/process-pending")
async def process_pending_articles(threshold_hours: int = 24):
    """
    หาข่าวที่ยังไม่ได้แปลหรือยังไม่ได้วิเคราะห์ impact
    แล้ว process (translate + impact reasoning) ทั้งหมด
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import translate_and_analyze_pending
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    try:
        results = translate_and_analyze_pending(threshold_hours=threshold_hours)
        return {
            "status": "ok",
            "processed": len(results),
            "results": results,
        }
    except Exception as e:
        logger.error(f"Process pending error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/news/article/{article_id}/translate")
async def translate_article(article_id: int):
    """
    แปลข่าวเดียวเป็นภาษาไทย + วิเคราะห์ impact
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import process_article_with_ai
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    try:
        result = process_article_with_ai(article_id)
        if "error" in result and result["error"] == "Article not found":
            raise HTTPException(status_code=404, detail="Article not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/news/article/{article_id}/impact")
async def get_article_impact(article_id: int):
    """
    ดึง impact reasoning ของข่าวเดียว
    """
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from scraper.news_scraper import get_article_by_id
    except ImportError as e:
        raise HTTPException(status_code=500, detail=f"Import error: {e}")

    article = get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    return {
        "id": article["id"],
        "title": article["title"],
        "source": article["source"],
        "impact_reasoning": article.get("impact_reasoning"),
        "impact_sentiment": article.get("impact_sentiment", "neutral"),
        "impact_risk": article.get("impact_risk", "low"),
        "impact_tags": article.get("impact_tags", []),
        "content_th": article.get("content_th", "")[:500] if article.get("content_th") else None,
        "has_translation": bool(article.get("content_th")),
        "has_impact_analysis": bool(article.get("impact_reasoning")),
    }


# ── Run Server ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
