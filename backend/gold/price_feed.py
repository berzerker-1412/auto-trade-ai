"""Gold price feed - fetches gold (XAU) prices from various sources"""

import requests
from typing import Dict, Any, Optional
from datetime import datetime


class GoldPriceFeed:
    """Fetch gold prices from various data sources"""
    
    def __init__(self, source: str = "demo"):
        self.source = source
        self.base_url = self._get_base_url()
    
    def _get_base_url(self) -> str:
        """Get API base URL based on source"""
        sources = {
            "alpha_vantage": "https://www.alphavantage.co/query",
            "goldapi": "https://www.goldapi.io/api",
            "demo": ""  # Will use simulated data
        }
        return sources.get(self.source, sources["demo"])
    
    def get_price(self, symbol: str = "XAUUSD") -> Optional[Dict[str, Any]]:
        """Get current gold price"""
        if self.source == "demo":
            return self._get_demo_price(symbol)
        
        if self.source == "alpha_vantage":
            return self._get_alpha_vantage_price(symbol)
        
        if self.source == "goldapi":
            return self._get_goldapi_price(symbol)
        
        return None
    
    def _get_demo_price(self, symbol: str) -> Dict[str, Any]:
        """Generate simulated gold price for testing"""
        # Base price around $2000 per troy ounce
        import random
        base_price = 2000.0
        variation = random.uniform(-50, 50)
        price = base_price + variation
        
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "bid": round(price - 0.5, 2),
            "ask": round(price + 0.5, 2),
            "currency": "USD",
            "unit": "oz",  # per troy ounce
            "timestamp": datetime.now()
        }
    
    def _get_alpha_vantage_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch from Alpha Vantage (requires API key)"""
        # Note: Requires FREE API key from alpha.vantage.co
        api_key = ""  # Set via config or environment variable
        
        if not api_key:
            print("[GOLD] Alpha Vantage API key not set, using demo data")
            return self._get_demo_price(symbol)
        
        try:
            response = requests.get(self.base_url, params={
                "function": "CURRENCY_EXCHANGE_RATE",
                "from_currency": "XAU",
                "to_currency": "USD",
                "apikey": api_key
            }, timeout=10)
            
            data = response.json()
            if "Realtime Currency Exchange Rate" in data:
                rate = data["Realtime Currency Exchange Rate"]
                return {
                    "symbol": symbol,
                    "price": float(rate["5. Exchange Rate"]),
                    "bid": float(rate["8. Bid Price"]),
                    "ask": float(rate["9. Ask Price"]),
                    "currency": "USD",
                    "timestamp": datetime.now()
                }
        except Exception as e:
            print(f"[GOLD] Error fetching price: {e}")
        
        return None
    
    def _get_goldapi_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch from GoldAPI.io (requires API key)"""
        api_key = ""  # Set via config or environment variable
        
        if not api_key:
            print("[GOLD] GoldAPI key not set, using demo data")
            return self._get_demo_price(symbol)
        
        try:
            headers = {"x-access-token": api_key}
            response = requests.get(
                f"{self.base_url}/{symbol.lower()}",
                headers=headers,
                timeout=10
            )
            
            data = response.json()
            return {
                "symbol": symbol,
                "price": data.get("price"),
                "bid": data.get("bid"),
                "ask": data.get("ask"),
                "currency": data.get("currency", "USD"),
                "timestamp": datetime.now()
            }
        except Exception as e:
            print(f"[GOLD] Error fetching price: {e}")
        
        return None
    
    def get_historical_prices(
        self, 
        days: int = 30
    ) -> list:
        """Get historical gold prices"""
        import random
        
        # Generate simulated historical data
        base_price = 2000.0
        prices = []
        
        for i in range(days):
            variation = random.uniform(-100, 100)
            price = base_price + variation
            prices.append({
                "date": datetime.now().timestamp() - (i * 86400),
                "price": round(price, 2)
            })
        
        return list(reversed(prices))
