"""
scraper/sources/reuters.py — Reuters News Scraper
ดึงข่าวจาก Reuters เน้นการเงิน เศรษฐกิจ และ commodities
"""
from typing import List, Optional
from datetime import datetime
import logging
import re

from .base import BaseScraper, NewsArticle

logger = logging.getLogger(__name__)


class ReutersScraper(BaseScraper):
    """Scraper สำหรับ Reuters"""

    source_name = "Reuters"
    base_url = "https://www.reuters.com"
    categories = ["finance", "economy", "crypto", "commodities"]

    # RSS feeds ของ Reuters
    RSS_URLS = {
        "markets": "https://feeds.reuters.com/reuters/businessNews",
        "world": "https://feeds.reuters.com/reuters/worldNews",
        "technology": "https://feeds.reuters.com/reuters/technologyNews",
    }

    def get_article_urls(self) -> List[str]:
        """ดึง URLs ล่าสุดจาก RSS feeds"""
        import feedparser

        urls = []
        for name, url in self.RSS_URLS.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:  # ล่าสุด 10 ข่าวต่อ feed
                    if hasattr(entry, "link"):
                        urls.append(entry.link)
            except Exception as e:
                logger.warning(f"[Reuters] RSS feed error ({name}): {e}")
        return urls

    def parse_article(self, url: str) -> Optional[NewsArticle]:
        """ดึงรายละเอียดข่าวจาก Reuters"""
        html = self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)

        # ดึง title
        title = ""
        title_elem = soup.select_one("h1") or soup.select_one("[data-testid='Heading']")
        if title_elem:
            title = title_elem.get_text(strip=True)

        # ดึง published time
        published_at = None
        time_elem = soup.select_one("time")
        if time_elem and time_elem.get("datetime"):
            try:
                published_at = datetime.fromisoformat(time_elem["datetime"].replace("Z", "+00:00"))
            except Exception:
                pass

        # ดึง summary (lede แรกๆ)
        summary = ""
        lede = soup.select_one("[data-testid='article-lede']") or soup.select_one(".article-body") or soup.select_one("article")
        if lede:
            paras = lede.select("p")[:3]
            summary = " ".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
            summary = summary[:300] + "..." if len(summary) > 300 else summary

        # ดึง content เต็ม — ทุก paragraph ใน article body
        content = ""
        article_body = (
            soup.select_one("[data-testid='article-body']")
            or soup.select_one(".article-body")
            or soup.select_one("article")
            or soup.select_one("div[data-element='story-body']")
        )
        if article_body:
            # เอาทุก paragraph ที่มี text
            paras = article_body.select("p")
            content_parts = []
            for p in paras:
                text = p.get_text(strip=True)
                # ข้าม tiny paragraphs (likely captions, credits)
                if text and len(text) > 30:
                    content_parts.append(text)
            content = "\n\n".join(content_parts)

        # ถ้าได้ content น้อยกว่า threshold ใช้ Playwright ดึงใหม่
        if not content or len(content) < self.MIN_CONTENT_LENGTH:
            full_text = self.extract_full_article(url)
            if full_text and len(full_text) > len(content):
                content = full_text

        # ถ้าไม่มี content ใช้ summary เป็น fallback
        if not content:
            content = summary

        # ตรวจหา impact tags
        impact_tags = self._detect_impact_tags(title + " " + summary)

        return NewsArticle(
            title=title,
            url=url,
            source=self.source_name,
            category=self._categorize(title, summary),
            published_at=published_at,
            summary=summary,
            content=content,  # ตอนนี้มี full content แล้ว
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _categorize(self, title: str, text: str) -> str:
        combined = (title + " " + text).lower()
        if any(w in combined for w in ["war", "military", "conflict", "attack", "ukraine", "russia", "israel", "gaza", "iran"]):
            return "war"
        if any(w in combined for w in ["bitcoin", "crypto", "ethereum", "binance", "defi", "token", "blockchain"]):
            return "crypto"
        if any(w in combined for w in ["gold", "silver", "oil", "crude", "commodity", "opec", "xau"]):
            return "commodities"
        if any(w in combined for w in ["fed", "rate", "inflation", "cpi", "gdp", "treasury", "bond", "dollar", "usd"]):
            return "economy"
        return "finance"

    def _detect_impact_tags(self, text: str) -> List[str]:
        """ตรวจหา asset tags ที่ข่าวนี้กระทบ"""
        text_lower = text.lower()
        tags = []

        CRYPTO_TAGS = ["bitcoin", "btc", "ethereum", "eth", "solana", "sol", "bnb", "xrp", "cardano", "ada"]
        COMMODITY_TAGS = ["gold", "xauusd", "silver", "xagusd", "oil", "crude", "wti", "brent"]
        FOREX_TAGS = ["usd", "dollar", "yen", "jpy", "euro", "eur", "gbp", "baht", "thb", "yuan", "cny"]
        INDEX_TAGS = ["s&p", "spx", "nasdaq", "dow", "ftse", "nikkei", "set", "set50"]

        for tag in CRYPTO_TAGS:
            if tag in text_lower:
                tags.append("CRYPTO")
                break
        for tag in COMMODITY_TAGS:
            if tag in text_lower:
                tags.append("XAUUSD" if "gold" in tag or "xau" in tag else "COMMODITY")
                break
        for tag in FOREX_TAGS:
            if tag in text_lower:
                tags.append("FOREX")
                break
        for tag in INDEX_TAGS:
            if tag in text_lower:
                tags.append("INDEX")
                break

        return list(set(tags)) if tags else ["GENERAL"]
