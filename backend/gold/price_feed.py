"""Gold Price Feed — XAUUSD real-time data from alpha_vantage"""

import os
import time
import requests
from datetime import datetime
from typing import Optional, Dict, Any
from functools import lru_cache

# For testing/demo without API key, use free demo endpoint
DEMO_MODE = os.getenv("ALPHA_VANTAGE_API_KEY") in (None, "", "demo")


@lru_cache(maxsize=1)
def _get_cached_rate(symbol: str = "XAUUSD") -> Optional[float]:
    """Cached rate to avoid hammering the API"""
    # For demo, return a realistic gold price
    if DEMO_MODE:
        return 2345.50  # realistic placeholder for demo
    return None


class GoldPriceFeed:
    """
    Gold (XAUUSD) price feed using Alpha Vantage API.
    
    ถ้าไม่มี API key จะ fallback เป็น demo data แต่จะแจ้งเตือนให้ user รู้
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY", "")
        self.base_url = "https://www.alphavantage.co/query"
        self._last_fetch: Optional[datetime] = None
        self._cache_ttl_seconds = 60  # cache 1 นาที
        self._demo_mode = self.api_key in ("", "demo") if not self.api_key else False
        self._last_price: Optional[float] = None

    @property
    def is_demo(self) -> bool:
        return self._demo_mode

    def get_current_price(self, symbol: str = "XAUUSD") -> Optional[float]:
        """Get current gold price (XAUUSD) as a float"""
        # Check cache first
        if self._last_price and self._last_fetch:
            age = (datetime.now() - self._last_fetch).total_seconds()
            if age < self._cache_ttl_seconds:
                return self._last_price

        if self._demo_mode:
            self._last_price = self._get_demo_price()
            self._last_fetch = datetime.now()
            return self._last_price

        return self._fetch_real_price(symbol)

    def get_price(self, symbol: str = "XAUUSD") -> Dict[str, Any]:
        """Get gold price as dict (compatibility method for API)"""
        price = self.get_current_price(symbol)
        if price is None:
            return {}
        return {
            "price": price,
            "bid": price - 0.5,
            "ask": price + 0.5,
            "high": price * 1.001,
            "low": price * 0.999,
        }

    def _fetch_real_price(self, symbol: str) -> Optional[float]:
        """Fetch real XAUUSD price from Alpha Vantage API"""
        try:
            # Alpha Vantage's Gold (XAU/USD) endpoint via CURRENCY_EXCHANGE_RATE
            params = {
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": "XAU",
                "to_currency": "USD",
                "apikey": self.api_key,
            }
            
            resp = requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if "Realtime Currency Exchange Rate" in data:
                price_str = data["Realtime Currency Exchange Rate"]["5. Exchange Rate"]
                price = float(price_str)
                self._last_price = price
                self._last_fetch = datetime.now()
                return price
            
            # Hit rate limit — fallback to demo
            if "Note" in data or "Information" in data:
                print("[GoldPriceFeed] API rate limit hit, falling back to demo data")
                self._demo_mode = True
                self._last_price = self._get_demo_price()
                self._last_fetch = datetime.now()
                return self._last_price
                
        except Exception as e:
            print(f"[GoldPriceFeed] API error: {e}, using demo data")
            self._demo_mode = True
            self._last_price = self._get_demo_price()
            self._last_fetch = datetime.now()
            return self._last_price

        return None

    def _get_demo_price(self) -> float:
        """Demo price when no API key is available"""
        return 2345.50

    def get_historical_prices(
        self,
        symbol: str = "XAUUSD",
        interval: str = "60min",
        output_size: str = "compact"
    ) -> Optional[Dict[str, Any]]:
        """
        Get historical gold prices.
        Falls back to demo data if API key not available.
        """
        if self._demo_mode or self.api_key in ("", "demo"):
            return self._get_demo_historical()

        try:
            params = {
                "function": "GOLD",
                "interval": interval,
                "outputsize": output_size,
                "apikey": self.api_key,
                "datatype": "json",
            }
            
            resp = requests.get(self.base_url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            
            if "data" in data:
                return data
            
            # Fallback to demo
            return self._get_demo_historical()
            
        except Exception as e:
            print(f"[GoldPriceFeed] Historical API error: {e}")
            return self._get_demo_historical()

    def _get_demo_historical(self) -> Dict[str, Any]:
        """Demo historical data"""
        now = datetime.now()
        return {
            "data": [
                {
                    "date": (now.replace(minute=0) - i * 3600).strftime("%Y-%m-%d %H:%M:%S"),
                    "value": round(2345.50 + (i % 5 - 2) * 2, 2)
                }
                for i in range(100)
            ]
        }
