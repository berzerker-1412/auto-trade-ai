"""Trader — executes signals against a specific wallet type"""

import asyncio
from datetime import datetime
from typing import Optional, Dict, Any

from .models import Trade, TradeSignal, TradeStatus, TradeDirection, AssetType, WalletType
from .trade_logger import TradeLogger
from .wallet_manager import WalletManager


class Trader:
    """
    Trader ทำงานได้ทั้ง PAPER และ LIVE ขึ้นอยู่กับ wallet_type ที่ให้มา

    PAPER: ดึงยอดจาก WalletManager.paper_wallet
    LIVE:  ดึงยอดจาก exchange API ผ่าน WalletManager.live_wallet
    """

    def __init__(
        self,
        wallet_manager: WalletManager,
        db_path: str = "data/trades.db",
        wallet_type: WalletType = WalletType.PAPER,
    ):
        self.wallet_manager = wallet_manager
        self.wallet_type = wallet_type
        self.logger = TradeLogger(db_path)
        self.active_trades: Dict[str, Trade] = {}

    @property
    def wallet(self):
        return self.wallet_manager.get_wallet(self.wallet_type)

    def execute_signal(self, signal: TradeSignal) -> Optional[Trade]:
        """
        Execute a trade signal on the specified wallet.
        For LIVE trades, also places the order on the exchange.
        """
        # Override signal's wallet_type with this trader's wallet_type
        signal.wallet_type = self.wallet_type

        required = signal.entry_price * signal.quantity
        if signal.direction == TradeDirection.BUY and self.wallet.balance < required:
            tag = self.wallet_type.value.upper()
            print(f"[{tag}] Insufficient balance: {self.wallet.balance} < {required}")
            return None

        # Create trade
        trade = Trade(
            symbol=signal.symbol,
            asset_type=signal.asset_type,
            wallet_type=signal.wallet_type,
            direction=signal.direction,
            entry_price=signal.entry_price,
            quantity=signal.quantity,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            status=TradeStatus.OPEN,
            entry_time=datetime.now(),
            trade_number=self.logger.get_next_trade_number(signal.symbol, self.wallet_type),
        )

        # Deduct balance for BUY orders
        if trade.direction == TradeDirection.BUY:
            self.wallet.balance -= required

        # For LIVE trades, also place real order on exchange
        if self.wallet_type == WalletType.LIVE:
            self._place_live_order(trade)

        # Log trade
        trade.id = self.logger.log_trade(trade)
        self.active_trades[signal.symbol] = trade

        tag = self.wallet_type.value.upper()
        print(f"[{tag}] Opened {trade.direction.value.upper()} {trade.symbol} "
              f"#{trade.trade_number}: {trade.quantity} @ {trade.entry_price}")

        return trade

    def _place_live_order(self, trade: Trade):
        """Place real order on exchange (LIVE mode only)"""
        # TODO: integrate with exchange.py for real order placement
        pass

    def close_trade(
        self,
        symbol: str,
        exit_price: float,
        reason: str = "signal"
    ) -> Optional[Trade]:
        """Close a trade at current price"""
        if symbol not in self.active_trades:
            print(f"[{self.wallet_type.value.upper()}] No active trade for {symbol}")
            return None

        trade = self.active_trades[symbol]
        trade.exit_price = exit_price
        trade.exit_time = datetime.now()
        trade.status = TradeStatus.CLOSED

        # Calculate P&L and update wallet balance
        pnl = trade.pnl
        if pnl:
            if pnl > 0:
                self.wallet.balance += abs(pnl)
            # For LIVE trades, also close real position on exchange
            if self.wallet_type == WalletType.LIVE:
                self._close_live_position(trade, exit_price)

        # Update in database
        self.logger.update_trade(trade)

        tag = self.wallet_type.value.upper()
        print(f"[{tag}] Closed {symbol} #{trade.trade_number}: "
              f"Exit @ {exit_price} | P&L: {pnl:.2f} | "
              f"Balance: {self.wallet.balance:.2f} {self.wallet.currency}")

        del self.active_trades[symbol]
        return trade

    def _close_live_position(self, trade: Trade, exit_price: float):
        """Close real position on exchange (LIVE mode only)"""
        # TODO: integrate with exchange.py for real position closing
        pass

    def check_stop_loss_take_profit(
        self,
        symbol: str,
        current_price: float
    ) -> Optional[Trade]:
        """Check and execute stop loss / take profit"""
        if symbol not in self.active_trades:
            return None

        trade = self.active_trades[symbol]

        if trade.direction == TradeDirection.BUY:
            if trade.stop_loss and current_price <= trade.stop_loss:
                return self.close_trade(symbol, current_price, "stop_loss")
            if trade.take_profit and current_price >= trade.take_profit:
                return self.close_trade(symbol, current_price, "take_profit")

        if trade.direction == TradeDirection.SELL:
            if trade.stop_loss and current_price >= trade.stop_loss:
                return self.close_trade(symbol, current_price, "stop_loss")
            if trade.take_profit and current_price <= trade.take_profit:
                return self.close_trade(symbol, current_price, "take_profit")

        return None

    def get_balance(self) -> Dict[str, Any]:
        """Get current wallet balance"""
        return self.wallet.to_dict()

    def get_stats(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get trading statistics for this wallet type"""
        stats = self.logger.get_trade_stats(symbol, self.wallet_type)
        return {
            "wallet_type": self.wallet_type.value,
            "total_trades": stats.total_trades,
            "winning_trades": stats.winning_trades,
            "losing_trades": stats.losing_trades,
            "win_rate": f"{stats.win_rate:.1f}%",
            "total_pnl": stats.total_pnl,
            "current_balance": self.wallet.balance,
        }


# Backward compatibility alias
class PaperTrader(Trader):
    """PaperTrader — backward compatible, uses PAPER wallet only"""

    def __init__(
        self,
        initial_balance: float = 100000.0,
        balance_currency: str = "USDT",
        db_path: str = "data/trades.db"
    ):
        wm = WalletManager(
            paper_initial=initial_balance,
            paper_currency=balance_currency,
        )
        super().__init__(
            wallet_manager=wm,
            db_path=db_path,
            wallet_type=WalletType.PAPER,
        )
        self.initial_balance = initial_balance  # for backward compat
        self.balance = initial_balance  # for backward compat

    @property
    def balance(self) -> float:
        return self.wallet.balance

    @balance.setter
    def balance(self, value: float):
        self.wallet.balance = value
