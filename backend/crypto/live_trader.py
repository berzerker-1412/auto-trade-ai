"""Live Exchange Trader — real trading via CCXT"""

from datetime import datetime
from typing import Optional, Dict, Any

from ..core.models import Trade, TradeSignal, TradeStatus, TradeDirection, AssetType, WalletType
from ..core.trader import Trader
from ..core.wallet_manager import WalletManager
from .exchange import CryptoExchange


class LiveExchangeTrader(Trader):
    """
    Live Trader — เทรดเงินจริงผ่าน exchange (Binance)

    สำหรับ LIVE wallet เท่านั้น:
    - ดึงยอดจริงจาก exchange
    - วาง order จริง
    - ปิด position จริง
    """

    def __init__(
        self,
        wallet_manager: WalletManager,
        exchange: CryptoExchange,
        db_path: str = "data/trades.db",
    ):
        super().__init__(
            wallet_manager=wallet_manager,
            db_path=db_path,
            wallet_type=WalletType.LIVE,
        )
        self.exchange = exchange
        self._exchange_order_ids: Dict[str, str] = {}  # symbol -> exchange_order_id

    def refresh_live_balance(self) -> float:
        """ดึงยอด USDT จริงจาก exchange แล้วอัปเดต wallet"""
        balance = self.exchange.get_balance("USDT")
        self.wallet_manager.update_balance(WalletType.LIVE, balance)
        return balance

    def execute_signal(self, signal: TradeSignal) -> Optional[Trade]:
        """Execute signal — PLACE REAL ORDER on exchange"""
        signal.wallet_type = WalletType.LIVE

        # Refresh live balance before trading
        self.refresh_live_balance()

        required = signal.entry_price * signal.quantity
        if signal.direction == TradeDirection.BUY and self.wallet.balance < required:
            print(f"[LIVE] Insufficient balance: {self.wallet.balance} < {required}")
            return None

        # Create trade record
        trade = Trade(
            symbol=signal.symbol,
            asset_type=signal.asset_type,
            wallet_type=WalletType.LIVE,
            direction=signal.direction,
            entry_price=signal.entry_price,
            quantity=signal.quantity,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            status=TradeStatus.OPEN,
            entry_time=datetime.now(),
            trade_number=self.logger.get_next_trade_number(
                signal.symbol, WalletType.LIVE
            ),
        )

        # Place real order on exchange
        order_result = self._place_live_order(trade)
        if "error" in order_result:
            print(f"[LIVE] Order failed: {order_result['error']}")
            return None

        # Deduct from live wallet (best-effort — actual balance tracked by exchange)
        if trade.direction == TradeDirection.BUY:
            self.wallet.balance -= required

        # Store exchange order ID for tracking
        self._exchange_order_ids[signal.symbol] = order_result.get("id", "")

        # Log trade
        trade.id = self.logger.log_trade(trade)
        self.active_trades[signal.symbol] = trade

        print(f"[LIVE] Opened {trade.direction.value.upper()} {trade.symbol} "
              f"#{trade.trade_number}: {trade.quantity} @ {trade.entry_price} "
              f"| Order ID: {order_result.get('id')}")

        return trade

    def _place_live_order(self, trade: Trade) -> Dict[str, Any]:
        """Place real order on exchange"""
        side = "buy" if trade.direction == TradeDirection.BUY else "sell"
        
        # Place market order for immediate execution
        result = self.exchange.place_order(
            symbol=trade.symbol,
            amount=trade.quantity,
            side=side,
            order_type="market",
        )
        return result

    def _close_live_position(
        self,
        trade: Trade,
        exit_price: float
    ):
        """Close real position on exchange"""
        side = "sell" if trade.direction == TradeDirection.BUY else "buy"
        self.exchange.place_order(
            symbol=trade.symbol,
            amount=trade.quantity,
            side=side,
            order_type="market",
        )

    def close_trade(
        self,
        symbol: str,
        exit_price: Optional[float] = None,
        reason: str = "signal"
    ) -> Optional[Trade]:
        """Close trade — close real position on exchange if LIVE"""
        if symbol not in self.active_trades:
            print(f"[LIVE] No active trade for {symbol}")
            return None

        trade = self.active_trades[symbol]

        # Get current price if not provided
        if exit_price is None:
            ticker = self.exchange.get_ticker(symbol)
            exit_price = ticker.get("last") or trade.entry_price

        trade.exit_price = exit_price
        trade.exit_time = datetime.now()
        trade.status = TradeStatus.CLOSED

        # Calculate P&L
        pnl = trade.pnl

        # Close real position on exchange
        self._close_live_position(trade, exit_price)

        # Update wallet balance (refresh from exchange)
        self.refresh_live_balance()

        # Log trade
        self.logger.update_trade(trade)

        print(f"[LIVE] Closed {symbol} #{trade.trade_number}: "
              f"Exit @ {exit_price} | P&L: {pnl:.2f} | "
              f"Exchange Balance: {self.wallet.balance:.2f}")

        del self.active_trades[symbol]
        if symbol in self._exchange_order_ids:
            del self._exchange_order_ids[symbol]

        return trade

    def check_stop_loss_take_profit(
        self,
        symbol: str,
        current_price: Optional[float] = None
    ):
        """Check SL/TP against current price from exchange"""
        if symbol not in self.active_trades:
            return None

        if current_price is None:
            ticker = self.exchange.get_ticker(symbol)
            current_price = ticker.get("last")

        if current_price is None:
            return None

        return super().check_stop_loss_take_profit(symbol, current_price)
