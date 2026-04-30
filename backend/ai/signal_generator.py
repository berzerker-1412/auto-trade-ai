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
        confidence_threshold: float = 0.55,
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

            price = float(data["entry_price"])
            raw_qty = float(data["quantity"])
            # Cap quantity ไม่ให้เกิน $100 ต่อ trade (10% ของ $1000)
            trade_notional = 100.0
            quantity = min(raw_qty, trade_notional / price) if price > 0 else raw_qty

            if data.get("confidence", 0) >= self.confidence_threshold:
                return TradeSignal(
                    asset_type=asset_type,
                    symbol=symbol,
                    direction=TradeDirection.BUY if str(data["direction"]).upper() == "BUY"
                               else TradeDirection.SELL,
                    entry_price=price,
                    quantity=quantity,
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
        Rules-based fallback signal generation — แทนที่จะ random
        ใช้ trend + RSI-like momentum + news bias รวมกัน
        """
        price = market_data.get("price", 0)
        high = market_data.get("high", 0)
        low = market_data.get("low", 0)
        volume = market_data.get("volume", 0)

        if price == 0:
            return None

        # ── 1. คำนวณ trend จาก high/low vs price ──────────────
        # ถ้าราคาอยู่ในครึ่งบนของ daily range → bullish bias
        daily_range = high - low if high > low else price * 0.02
        if daily_range > 0:
            price_position = (price - low) / daily_range  # 0 = ก้น, 1 = ยอด
        else:
            price_position = 0.5

        if price_position > 0.65:
            trend_score = 1  # ในครึ่งบน → uptrend
        elif price_position < 0.35:
            trend_score = -1  # ในครึ่งล่าง → downtrend
        else:
            trend_score = 0  # กลาง → sideways

        # ── 2. คำนวณ momentum (RSI-like) จาก price position ────
        # price_position ใกล้ 1 = overbought (RSI-like > 70) แต่เฉพาะเมื่อ trend ไม่ได้ bullish อยู่แล้ว
        # price_position ใกล้ 0 = oversold (RSI-like < 30) แต่เฉพาะเมื่อ trend ไม่ได้ bearish อยู่แล้ว
        rsi_approx = price_position * 100  # 0-100 scale
        if rsi_approx > 75 and trend_score <= 0:
            momentum_score = -1  # overbought → sell bias (เฉพาะถ้าไม่ได้อยู่ใน uptrend)
        elif rsi_approx < 25 and trend_score >= 0:
            momentum_score = 1  # oversold → buy bias (เฉพาะถ้าไม่ได้อยู่ใน downtrend)
        else:
            momentum_score = 0

        # ── 3. News bias ────────────────────────────────────────
        news_score = 0.0
        if news_signal:
            score = news_signal.get("score", 0)
            bias = news_signal.get("bias", "neutral")
            impacted = news_signal.get("impacted_assets", [])
            risk_level = news_signal.get("risk_level", "low")

            # ตรวจสอบว่า symbol กระทบกับข่าวไหม
            symbol_lower = symbol.lower()
            is_impacted = any(
                tag.lower() in symbol_lower or symbol_lower in tag.lower()
                for tag in impacted
            )

            if is_impacted or not impacted:
                if bias == "bullish" and abs(score) > 0.1:
                    news_score = min(score * 2, 1.0)
                elif bias == "bearish" and abs(score) > 0.1:
                    news_score = max(score * 2, -1.0)

            # Risk-off environment: ถ้า risk=high และเป็น gold ให้ buy bias
            if risk_level == "high" and "XAU" in symbol:
                news_score = max(news_score, 0.4)

        # ── 4. รวม scores ────────────────────────────────────────
        # trend: 30%, momentum: 30%, news: 40%
        combined = (trend_score * 0.3) + (momentum_score * 0.3) + (news_score * 0.4)

        # ถ้า combined ใกล้ 0 → skip ไม่ trade (sideways/no signal)
        if abs(combined) < 0.15:
            return None

        # ── 5. ตัดสินใจ direction + confidence ──────────────────
        if combined > 0.15:
            direction = TradeDirection.BUY
            confidence = min(0.60 + abs(combined) * 0.25, 0.85)
            reasoning_parts = []
            if trend_score > 0:
                reasoning_parts.append("price in upper range")
            if momentum_score > 0:
                reasoning_parts.append("oversold bounce")
            if news_score > 0:
                reasoning_parts.append(f"news bullish ({news_score:+.2f})")
            reasoning = "Fallback BUY: " + ", ".join(reasoning_parts) if reasoning_parts else "Fallback BUY: combined signal"
        else:
            direction = TradeDirection.SELL
            confidence = min(0.60 + abs(combined) * 0.25, 0.85)
            reasoning_parts = []
            if trend_score < 0:
                reasoning_parts.append("price in lower range")
            if momentum_score < 0:
                reasoning_parts.append("overbought reversal")
            if news_score < 0:
                reasoning_parts.append(f"news bearish ({news_score:+.2f})")
            reasoning = "Fallback SELL: " + ", ".join(reasoning_parts) if reasoning_parts else "Fallback SELL: combined signal"

        # ── 6. Stop loss / Take profit ──────────────────────────
        # Gold: tighter SL (0.8%), wider TP (2%)
        # Crypto: wider SL (1.5%), wider TP (4%)
        if asset_type == AssetType.GOLD:
            sl_pct = 0.008
            tp_pct = 0.020
        else:
            sl_pct = 0.015
            tp_pct = 0.040

        stop_loss = round(price * (1 - sl_pct), 2) if direction == TradeDirection.BUY else round(price * (1 + sl_pct), 2)
        take_profit = round(price * (1 + tp_pct), 2) if direction == TradeDirection.BUY else round(price * (1 - tp_pct), 2)

        # ── 7. Position sizing ───────────────────────────────────
        # 10% ของ balance ต่อ trade ($100 จาก $1000)
        trade_notional = 100.0
        quantity = round(trade_notional / price, 6) if price > 0 else 0.001

        if confidence < self.confidence_threshold:
            return None

        return TradeSignal(
            asset_type=asset_type,
            symbol=symbol,
            direction=direction,
            entry_price=price,
            quantity=quantity,
            stop_loss=stop_loss,
            take_profit=take_profit,
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
