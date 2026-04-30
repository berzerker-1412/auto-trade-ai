"""AI-powered trading signal generator — ใช้ MiniMax เป็น AI provider"""

import os
import json
from typing import Dict, Any, Optional, List

from .minimax_client import MiniMaxChatClient
from ..core.models import TradeSignal, AssetType, TradeDirection


class AISignalGenerator:
    """Generate trading signals using MiniMax AI"""

    # Thai system prompt — AI ตอบเป็นภาษาไทยให้อ่านง่าย
    SYSTEM_PROMPT = """คุณคือนักวิเคราะห์การเทรดมืออาชีพ
วิเคราะห์ข้อมูลตลาด + sentiment ข่าว แล้วสร้างสัญญาณ BUY หรือ SELL ที่ชัดเจน
ตอบเป็น JSON ที่มี: direction, entry_price, quantity, stop_loss, take_profit, confidence (0-1), reasoning"""

    def __init__(
        self,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        confidence_threshold: float = 0.70,
    ):
        self.model = model or os.getenv("MINIMAX_MODEL_NAME", "MiniMax-Text-01")
        self.confidence_threshold = confidence_threshold

        try:
            self.client = MiniMaxChatClient(
                api_key=api_key or os.getenv("MINIMAX_API_KEY", ""),
                base_url=base_url or os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1"),
                model=self.model,
            )
        except ValueError as e:
            self.client = None
            print(f"[AI] MiniMax not available: {e}, using fallback signal generation")

    def generate_signal(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        analysis: str = "",
        news_signal: Optional[Dict[str, Any]] = None,
    ) -> Optional[TradeSignal]:
        """
        Generate a trading signal based on market data + news sentiment

        Args:
            news_signal: dict from get_trade_signal() — contains:
                - bias: "bullish" | "bearish" | "neutral"
                - score: float (-1 to 1)
                - signal: trade direction/hints from news
                - impacted_assets: list of asset tags
        """
        if self.client:
            return self._generate_with_minimax(symbol, asset_type, market_data, analysis, news_signal)
        else:
            return self._generate_fallback(symbol, asset_type, market_data, news_signal)

    def _generate_with_minimax(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        analysis: str,
        news_signal: Optional[Dict[str, Any]] = None,
    ) -> Optional[TradeSignal]:
        """Generate signal using MiniMax with news intelligence"""
        prompt = self._build_prompt(symbol, asset_type, market_data, analysis, news_signal)

        try:
            response = self.client.chat.completions_create(
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=512,
                response_format={"type": "json_object"},
            )

            content = response["choices"][0]["message"]["content"]

            # Parse JSON — handle potential markdown code blocks
            content = content.strip()
            if content.startswith("```"):
                # Strip markdown code block wrapper
                lines = content.split("\n")
                content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

            data = json.loads(content)

            if data.get("confidence", 0) >= self.confidence_threshold:
                return TradeSignal(
                    asset_type=asset_type,
                    symbol=symbol,
                    direction=TradeDirection.BUY if str(data["direction"]).upper() == "BUY"
                               else TradeDirection.SELL,
                    entry_price=float(data["entry_price"]),
                    quantity=float(data["quantity"]),
                    stop_loss=float(data.get("stop_loss", 0)),
                    take_profit=float(data.get("take_profit", 0)),
                    confidence=float(data["confidence"]),
                    reasoning=data.get("reasoning", ""),
                )

        except json.JSONDecodeError as e:
            print(f"[AI] JSON parse error: {e} — content: {content[:200]}")
        except Exception as e:
            print(f"[AI] Error generating signal: {e}")

        return None

    def _build_prompt(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        analysis: str,
        news_signal: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build prompt for AI — รวม news sentiment ด้วย"""
        news_section = ""
        if news_signal:
            bias = news_signal.get("bias", "unknown")
            score = news_signal.get("score", 0)
            impacted = news_signal.get("impacted_assets", [])
            category_breakdown = news_signal.get("category_breakdown", {})
            risk_level = news_signal.get("risk_level", "unknown")

            news_section = f"""
News Intelligence:
- Overall Bias: {bias.upper()} (score: {score:+.2f})
- Risk Level: {risk_level.upper()}
- Impacted Assets: {', '.join(impacted) if impacted else 'None'}
- Category Breakdown: {', '.join(f"{k}({v})" for k, v in category_breakdown.items()) if category_breakdown else 'N/A'}
"""
            if news_signal.get("signal"):
                sig = news_signal["signal"]
                news_section += f"- Suggested Direction: {sig.get('direction', 'N/A').upper()} (confidence: {sig.get('confidence', 0):.0%})\n"
                if sig.get("reason"):
                    news_section += f"- Reason: {sig['reason']}\n"

        return f"""วิเคราะห์ {symbol} ({asset_type.value}) แล้วสร้างสัญญาณเทรด

Market Data:
- Current Price: {market_data.get('price', 'N/A')}
- 24h High: {market_data.get('high', 'N/A')}
- 24h Low: {market_data.get('low', 'N/A')}
- Volume: {market_data.get('volume', 'N/A')}

Technical Analysis:
{analysis if analysis else '(None provided)'}
{news_section}
ตอบเป็น JSON ที่มี:
- direction: "BUY" หรือ "SELL"
- entry_price: ราคาเข้าเทรด
- quantity: จำนวนที่จะเทรด
- stop_loss: ราคาตั้ง stop loss (ถ้ามี)
- take_profit: ราคาตั้ง take profit (ถ้ามี)
- confidence: ความมั่นใจ 0-1
- reasoning: คำอธิบายสั้นๆ
"""

    def _generate_fallback(
        self,
        symbol: str,
        asset_type: AssetType,
        market_data: Dict[str, Any],
        news_signal: Optional[Dict[str, Any]] = None,
    ) -> Optional[TradeSignal]:
        """
        Fallback signal generation using simple heuristics
        ปรับ direction ตาม news sentiment ถ้ามีข้อมูลข่าว
        """
        import random

        price = market_data.get("price", 0)
        if price == 0:
            return None

        # ถ้ามี news signal ให้ใช้เป็น bias หลัก
        if news_signal:
            bias = news_signal.get("bias", "neutral")
            score = news_signal.get("score", 0)
            impacted = news_signal.get("impacted_assets", [])

            # ตรวจสอบว่า symbol ที่กำลังดูกระทบกับข่าวไหม
            symbol_lower = symbol.lower()
            is_impacted = any(
                tag.lower() in symbol_lower or symbol_lower in tag.lower()
                for tag in impacted
            )

            if is_impacted:
                # มีข่าวกระทบ symbol นี้โดยตรง
                if bias == "bullish" and score > 0.2:
                    direction = TradeDirection.BUY
                    confidence = min(0.6 + abs(score) * 0.3, 0.95)
                    reasoning = f"News bullish ({score:+.2f}) for {symbol}"
                elif bias == "bearish" and score < -0.2:
                    direction = TradeDirection.SELL
                    confidence = min(0.6 + abs(score) * 0.3, 0.95)
                    reasoning = f"News bearish ({score:+.2f}) for {symbol}"
                else:
                    direction = random.choice([TradeDirection.BUY, TradeDirection.SELL])
                    confidence = 0.55
                    reasoning = "No strong news bias, random direction"
            else:
                # ไม่กระทบโดยตรง ใช้ random
                direction = random.choice([TradeDirection.BUY, TradeDirection.SELL])
                confidence = 0.55
                reasoning = "Symbol not directly impacted by current news"
        else:
            # ไม่มี news signal — ใช้ random
            direction = random.choice([TradeDirection.BUY, TradeDirection.SELL])
            confidence = random.uniform(0.6, 0.9)
            reasoning = "Fallback signal — configure MiniMax for better signals"

        if confidence < self.confidence_threshold:
            return None

        return TradeSignal(
            asset_type=asset_type,
            symbol=symbol,
            direction=direction,
            entry_price=price,
            quantity=0.1,
            stop_loss=price * 0.98 if direction == TradeDirection.BUY else price * 1.02,
            take_profit=price * 1.05 if direction == TradeDirection.BUY else price * 0.95,
            confidence=confidence,
            reasoning=reasoning,
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
