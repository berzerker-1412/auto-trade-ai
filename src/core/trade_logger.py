"""Trade logging and database management"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

from .models import Trade, TradeStatus, TradeResult, AssetType, TradeDirection


class TradeLogger:
    """SQLite-based trade logger"""
    
    def __init__(self, db_path: str = "data/trades.db"):
        self.db_path = db_path
        self._init_db()
    
    @contextmanager
    def _get_conn(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _init_db(self):
        """Initialize database schema"""
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    asset_type TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    entry_price REAL NOT NULL,
                    exit_price REAL,
                    quantity REAL NOT NULL,
                    stop_loss REAL,
                    take_profit REAL,
                    status TEXT NOT NULL,
                    entry_time TEXT,
                    exit_time TEXT,
                    trade_number INTEGER NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_trades_symbol 
                ON trades(symbol)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_trades_status 
                ON trades(status)
            """)
    
    def log_trade(self, trade: Trade) -> int:
        """Log a new trade"""
        with self._get_conn() as conn:
            cursor = conn.execute("""
                INSERT INTO trades (
                    symbol, asset_type, direction, entry_price, exit_price,
                    quantity, stop_loss, take_profit, status,
                    entry_time, exit_time, trade_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade.symbol,
                trade.asset_type.value,
                trade.direction.value,
                trade.entry_price,
                trade.exit_price,
                trade.quantity,
                trade.stop_loss,
                trade.take_profit,
                trade.status.value,
                trade.entry_time.isoformat() if trade.entry_time else None,
                trade.exit_time.isoformat() if trade.exit_time else None,
                trade.trade_number
            ))
            return cursor.lastrowid
    
    def update_trade(self, trade: Trade):
        """Update existing trade"""
        with self._get_conn() as conn:
            conn.execute("""
                UPDATE trades SET
                    exit_price = ?,
                    status = ?,
                    exit_time = ?
                WHERE id = ?
            """, (
                trade.exit_price,
                trade.status.value,
                trade.exit_time.isoformat() if trade.exit_time else None,
                trade.id
            ))
    
    def get_open_trades(self, symbol: Optional[str] = None) -> List[Trade]:
        """Get all open trades"""
        query = "SELECT * FROM trades WHERE status = ?"
        params = [TradeStatus.OPEN.value]
        
        if symbol:
            query += " AND symbol = ?"
            params.append(symbol)
        
        return self._rows_to_trades(query, params)
    
    def get_trade_history(
        self, 
        symbol: Optional[str] = None,
        limit: int = 100
    ) -> List[Trade]:
        """Get trade history"""
        query = "SELECT * FROM trades ORDER BY created_at DESC LIMIT ?"
        params = [limit]
        
        if symbol:
            query = "SELECT * FROM trades WHERE symbol = ? ORDER BY created_at DESC LIMIT ?"
            params = [symbol, limit]
        
        return self._rows_to_trades(query, params)
    
    def get_trade_stats(self, symbol: Optional[str] = None) -> TradeResult:
        """Get trading statistics"""
        query = """
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN exit_price > entry_price AND direction = 'buy' THEN 1
                         WHEN exit_price < entry_price AND direction = 'sell' THEN 1
                         ELSE 0 END) as wins,
                SUM(CASE WHEN exit_price < entry_price AND direction = 'buy' THEN 1
                         WHEN exit_price > entry_price AND direction = 'sell' THEN 1
                         ELSE 0 END) as losses
            FROM trades
            WHERE status = 'closed'
        """
        params = []
        
        if symbol:
            query += " AND symbol = ?"
            params = [symbol]
        
        with self._get_conn() as conn:
            row = conn.execute(query, params).fetchone()
            
            result = TradeResult(
                total_trades=row["total"] or 0,
                winning_trades=row["wins"] or 0,
                losing_trades=row["losses"] or 0
            )
            result.calculate_metrics()
            return result
    
    def get_next_trade_number(self, symbol: str) -> int:
        """Get next trade number for a symbol (ไม้ที่เท่าไหร่)"""
        with self._get_conn() as conn:
            row = conn.execute(
                "SELECT MAX(trade_number) as last_num FROM trades WHERE symbol = ?",
                (symbol,)
            ).fetchone()
            return (row["last_num"] or 0) + 1
    
    def _rows_to_trades(self, query: str, params: list) -> List[Trade]:
        """Convert database rows to Trade objects"""
        with self._get_conn() as conn:
            rows = conn.execute(query, params).fetchall()
            trades = []
            for row in rows:
                trade = Trade(
                    id=row["id"],
                    symbol=row["symbol"],
                    asset_type=AssetType(row["asset_type"]),
                    direction=TradeDirection(row["direction"]),
                    entry_price=row["entry_price"],
                    exit_price=row["exit_price"],
                    quantity=row["quantity"],
                    stop_loss=row["stop_loss"],
                    take_profit=row["take_profit"],
                    status=TradeStatus(row["status"]),
                    entry_time=datetime.fromisoformat(row["entry_time"]) if row["entry_time"] else None,
                    exit_time=datetime.fromisoformat(row["exit_time"]) if row["exit_time"] else None,
                    trade_number=row["trade_number"]
                )
                trades.append(trade)
            return trades
