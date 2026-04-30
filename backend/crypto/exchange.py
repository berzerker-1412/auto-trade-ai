"""CCXT Exchange Wrapper for Crypto Trading"""

import ccxt
from typing import Dict, Any, Optional, List
from datetime import datetime


class CryptoExchange:
    """Unified interface for crypto exchanges via CCXT"""
    
    def __init__(
        self,
        exchange_id: str = "binance",
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        testnet: bool = True
    ):
        self.exchange_id = exchange_id
        self.testnet = testnet
        self._exchange = self._init_exchange(api_key, api_secret)
    
    def _init_exchange(
        self, 
        api_key: Optional[str], 
        api_secret: Optional[str]
    ) -> ccxt.Exchange:
        """Initialize CCXT exchange instance"""
        exchange_class = getattr(ccxt, self.exchange_id)
        
        config: Dict[str, Any] = {
            "enableRateLimit": True,
            "options": {"defaultType": "spot"}
        }
        
        if api_key and api_secret:
            config["apiKey"] = api_key
            config["secret"] = api_secret
        
        if self.testnet:
            # Binance testnet
            config["urls"] = {
                "api": "https://testnet.binance.vision/api"
            }
        
        return exchange_class(config)
    
    def get_balance(self, currency: str = "USDT") -> float:
        """Get balance for a specific currency"""
        try:
            balance = self._exchange.fetch_balance()
            return float(balance.get(currency, {}).get("free", 0))
        except Exception as e:
            print(f"[EXCHANGE] Error fetching balance: {e}")
            return 0.0
    
    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """Get current ticker data for a symbol"""
        try:
            ticker = self._exchange.fetch_ticker(symbol)
            return {
                "symbol": symbol,
                "bid": ticker["bid"],
                "ask": ticker["ask"],
                "last": ticker["last"],
                "high": ticker["high"],
                "low": ticker["low"],
                "volume": ticker["baseVolume"],
                "timestamp": datetime.fromtimestamp(ticker["timestamp"] / 1000)
            }
        except Exception as e:
            print(f"[EXCHANGE] Error fetching ticker {symbol}: {e}")
            return {}
    
    def get_ohlcv(
        self, 
        symbol: str, 
        timeframe: str = "1h", 
        limit: int = 100
    ) -> List[List[float]]:
        """Get OHLCV (candlestick) data"""
        try:
            return self._exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        except Exception as e:
            print(f"[EXCHANGE] Error fetching OHLCV {symbol}: {e}")
            return []
    
    def place_order(
        self,
        symbol: str,
        amount: float,
        side: str = "buy",
        order_type: str = "limit",
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Place a trading order"""
        try:
            if order_type == "limit" and price:
                order = self._exchange.create_order(
                    symbol, order_type, side, amount, price
                )
            else:
                order = self._exchange.create_order(
                    symbol, "market", side, amount
                )
            
            return {
                "id": order["id"],
                "symbol": order["symbol"],
                "type": order["type"],
                "side": order["side"],
                "amount": order["amount"],
                "price": order.get("price"),
                "status": order["status"],
                "filled": order.get("filled", 0),
                "remaining": order.get("remaining", amount)
            }
        except Exception as e:
            print(f"[EXCHANGE] Error placing order: {e}")
            return {"error": str(e)}
    
    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """Cancel an order"""
        try:
            self._exchange.cancel_order(order_id, symbol)
            return True
        except Exception as e:
            print(f"[EXCHANGE] Error cancelling order: {e}")
            return False
    
    def get_open_orders(self, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all open orders"""
        try:
            orders = self._exchange.fetch_open_orders(symbol) if symbol \
                     else self._exchange.fetch_open_orders()
            return [
                {
                    "id": o["id"],
                    "symbol": o["symbol"],
                    "type": o["type"],
                    "side": o["side"],
                    "amount": o["amount"],
                    "price": o.get("price"),
                    "filled": o.get("filled", 0),
                    "timestamp": datetime.fromtimestamp(o["timestamp"] / 1000)
                }
                for o in orders
            ]
        except Exception as e:
            print(f"[EXCHANGE] Error fetching open orders: {e}")
            return []
    
    @staticmethod
    def get_available_exchanges() -> List[str]:
        """List all exchanges supported by CCXT"""
        return list(ccxt.exchanges)
    
    def get_supported_symbols(self) -> List[str]:
        """Get list of trading pairs on the exchange"""
        try:
            markets = self._exchange.load_markets()
            return list(markets.keys())
        except Exception as e:
            print(f"[EXCHANGE] Error loading markets: {e}")
            return []
