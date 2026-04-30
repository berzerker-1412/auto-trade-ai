"""Paper Trader - Simulated trading without real money"""

import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

from .models import Trade, TradeSignal, TradeStatus, TradeDirection, AssetType
from .trade_logger import TradeLogger


class PaperTrader:
    """Paper trading system - simulates trades without real money"""
    
    def __init__(
        self,
        initial_balance: float = 100000.0,
        balance_currency: str = "USDT",
        db_path: str = "data/trades.db"
    ):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.balance_currency = balance_currency
        self.logger = TradeLogger(db_path)
        self.active_trades: Dict[str, Trade] = {}
    
    def execute_signal(self, signal: TradeSignal) -> Optional[Trade]:
        """Execute a trade signal in paper trade mode"""
        # Check balance
        required = signal.entry_price * signal.quantity
        if signal.direction == TradeDirection.BUY and self.balance < required:
            print(f"[PAPER] Insufficient balance: {self.balance} < {required}")
            return None
        
        # Create trade
        trade = Trade(
            symbol=signal.symbol,
            asset_type=signal.asset_type,
            direction=signal.direction,
            entry_price=signal.entry_price,
            quantity=signal.quantity,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            status=TradeStatus.OPEN,
            entry_time=datetime.now(),
            trade_number=self.logger.get_next_trade_number(signal.symbol)
        )
        
        # Deduct balance for buy orders
        if trade.direction == TradeDirection.BUY:
            self.balance -= required
        
        # Log trade
        trade.id = self.logger.log_trade(trade)
        self.active_trades[signal.symbol] = trade
        
        print(f"[PAPER] Opened {trade.direction.value.upper()} {trade.symbol} "
              f"#{trade.trade_number}: {trade.quantity} @ {trade.entry_price}")
        
        return trade
    
    def close_trade(
        self, 
        symbol: str, 
        exit_price: float,
        reason: str = "signal"
    ) -> Optional[Trade]:
        """Close a trade at current price"""
        if symbol not in self.active_trades:
            print(f"[PAPER] No active trade for {symbol}")
            return None
        
        trade = self.active_trades[symbol]
        trade.exit_price = exit_price
        trade.exit_time = datetime.now()
        trade.status = TradeStatus.CLOSED
        
        # Calculate P&L and update balance
        pnl = trade.pnl
        if pnl:
            self.balance += abs(pnl) if pnl > 0 else 0
        
        # Update in database
        self.logger.update_trade(trade)
        
        print(f"[PAPER] Closed {symbol} #{trade.trade_number}: "
              f"Exit @ {exit_price} | P&L: {pnl:.2f} | "
              f"Balance: {self.balance:.2f} {self.balance_currency}")
        
        del self.active_trades[symbol]
        return trade
    
    def check_stop_loss_take_profit(
        self, 
        symbol: str, 
        current_price: float
    ) -> Optional[Trade]:
        """Check and execute stop loss / take profit"""
        if symbol not in self.active_trades:
            return None
        
        trade = self.active_trades[symbol]
        
        # Check stop loss (for long positions)
        if trade.direction == TradeDirection.BUY:
            if trade.stop_loss and current_price <= trade.stop_loss:
                return self.close_trade(symbol, current_price, "stop_loss")
            if trade.take_profit and current_price >= trade.take_profit:
                return self.close_trade(symbol, current_price, "take_profit")
        
        # Check stop loss (for short positions)
        if trade.direction == TradeDirection.SELL:
            if trade.stop_loss and current_price >= trade.stop_loss:
                return self.close_trade(symbol, current_price, "stop_loss")
            if trade.take_profit and current_price <= trade.take_profit:
                return self.close_trade(symbol, current_price, "take_profit")
        
        return None
    
    def get_balance(self) -> Dict[str, Any]:
        """Get current paper trading balance"""
        return {
            "balance": self.balance,
            "currency": self.balance_currency,
            "initial_balance": self.initial_balance,
            "total_pnl": self.balance - self.initial_balance,
            "active_trades": len(self.active_trades)
        }
    
    def get_stats(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get trading statistics"""
        stats = self.logger.get_trade_stats(symbol)
        return {
            "total_trades": stats.total_trades,
            "winning_trades": stats.winning_trades,
            "losing_trades": stats.losing_trades,
            "win_rate": f"{stats.win_rate:.1f}%",
            "total_pnl": stats.total_pnl,
            "current_balance": self.balance
        }
