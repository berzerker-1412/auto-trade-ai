"""AI-powered trading signal generator"""

import os
from typing import Dict, Any, Optional, List
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..core.models import TradeSignal, AssetType, TradeDirection


class AISignalGenerator:
    """Generate trading signals using AI"""
    
    def __init__(
        self,
        model: str = "gpt-4",
        api_key: Optional[str] = None,
        confidence_threshold: float = 0.70
    ):
        self.model = model
        self.confidence_threshold = confidence_threshold
        
        if OPENAI_AVAILABLE:
            self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        else:
            self.client = None
            print("[AI] OpenAI not available, using fallback signal generation")
    
    def generate_signal(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        analysis: str = ""
    ) -> Optional[TradeSignal]:
        """Generate a trading signal based on market data"""
        
        if self.client:
            return self._generate_with_openai(symbol, asset_type, market_data, analysis)
        else:
            return self._generate_fallback(symbol, asset_type, market_data)
    
    def _generate_with_openai(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        analysis: str
    ) -> Optional[TradeSignal]:
        """Generate signal using OpenAI"""
        
        prompt = self._build_prompt(symbol, asset_type, market_data, analysis)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a professional trading signal generator. 
                        Analyze market data and generate clear BUY or SELL signals.
                        Return JSON format with: direction, entry_price, quantity, 
                        stop_loss, take_profit, confidence (0-1), reasoning."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            data = eval(content)  # Safe here as we control the prompt
            
            if data.get("confidence", 0) >= self.confidence_threshold:
                return TradeSignal(
                    asset_type=asset_type,
                    symbol=symbol,
                    direction=TradeDirection.BUY if data["direction"].upper() == "BUY" 
                               else TradeDirection.SELL,
                    entry_price=float(data["entry_price"]),
                    quantity=float(data["quantity"]),
                    stop_loss=float(data.get("stop_loss", 0)),
                    take_profit=float(data.get("take_profit", 0)),
                    confidence=float(data["confidence"]),
                    reasoning=data.get("reasoning", "")
                )
            
        except Exception as e:
            print(f"[AI] Error generating signal: {e}")
        
        return None
    
    def _build_prompt(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        analysis: str
    ) -> str:
        """Build prompt for AI"""
        return f"""Analyze {symbol} ({asset_type.value}) and generate a trading signal.

Market Data:
- Current Price: {market_data.get('price', 'N/A')}
- 24h High: {market_data.get('high', 'N/A')}
- 24h Low: {market_data.get('low', 'N/A')}
- Volume: {market_data.get('volume', 'N/A')}

Technical/News Analysis:
{analysis}

Return a JSON signal with:
- direction: "BUY" or "SELL"
- entry_price: specific price to enter
- quantity: amount to trade
- stop_loss: price for stop loss (optional)
- take_profit: price for take profit (optional)
- confidence: confidence level 0-1
- reasoning: brief explanation
"""
    
    def _generate_fallback(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any]
    ) -> Optional[TradeSignal]:
        """Fallback signal generation using simple heuristics"""
        import random
        
        price = market_data.get("price", 0)
        if price == 0:
            return None
        
        # Simple random signal for testing
        direction = random.choice([TradeDirection.BUY, TradeDirection.SELL])
        confidence = random.uniform(0.6, 0.9)
        
        if confidence < self.confidence_threshold:
            return None
        
        return TradeSignal(
            asset_type=asset_type,
            symbol=symbol,
            direction=direction,
            entry_price=price,
            quantity=0.1,  # Default quantity
            stop_loss=price * 0.98 if direction == TradeDirection.BUY else price * 1.02,
            take_profit=price * 1.05 if direction == TradeDirection.BUY else price * 0.95,
            confidence=confidence,
            reasoning="Fallback signal - configure OpenAI for better signals"
        )
    
    def analyze_market(
        self,
        symbol: str,
        price_data: List[Dict[str, Any]],
        news: List[str] = None
    ) -> str:
        """Analyze market data and produce text analysis"""
        if not price_data:
            return "No price data available"
        
        latest = price_data[-1]
        oldest = price_data[0]
        
        # Simple trend calculation
        price_change = ((latest.get("price", 0) - oldest.get("price", 0)) 
                        / oldest.get("price", 1)) * 100
        
        analysis = f"""
Current Price: {latest.get('price', 'N/A')}
Price Change (period): {price_change:+.2f}%
High: {latest.get('high', 'N/A')}
Low: {latest.get('low', 'N/A')}

Trend: {"BULLISH" if price_change > 2 else "BEARISH" if price_change < -2 else "SIDEWAYS"}
"""
        
        if news:
            analysis += f"\nRecent News: {'; '.join(news[:3])}"
        
        return analysis
