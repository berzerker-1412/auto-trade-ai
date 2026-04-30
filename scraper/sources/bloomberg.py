"""
scraper/sources/bloomberg.py — Bloomberg News Scraper
ดึงข่าวจาก Bloomberg เน้นตลาดการเงิน และเศรษฐกิจโลก
"""
from typing import List, Optional
from datetime import datetime
import logging

from .base import BaseScraper, NewsArticle

logger = logging.getLogger(__name__)


class BloombergScraper(BaseScraper):
    """Scraper สำหรับ Bloomberg"""

    source_name = "Bloomberg"
    base_url = "https://www.bloomberg.com"
    categories = ["finance", "economy", "markets", "crypto"]

    # Bloomberg RSS feeds
    RSS_URLS = {
        "markets": "https://feeds.bloomberg.com/markets/news.rss",
        "top": "https://feeds.bloomberg.com/top/news.rss",
        "economy": "https://feeds.bloomberg.com/economics/news.rss",
        "crypto": "https://feeds.bloomberg.com/technology/news.rss",
    }

    def get_article_urls(self) -> List[str]:
        """ดึง URLs ล่าสุดจาก RSS feeds"""
        import feedparser

        urls = []
        for name, url in self.RSS_URLS.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:
                    if hasattr(entry, "link"):
                        urls.append(entry.link)
            except Exception as e:
                logger.warning(f"[Bloomberg] RSS feed error ({name}): {e}")
        return urls

    def parse_article(self, url: str) -> Optional[NewsArticle]:
        """ดึงรายละเอียดข่าวจาก Bloomberg article"""
        html = self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)

        # Title
        title = ""
        title_elem = (
            soup.select_one("h1")
            or soup.select_one("[data-component='headline']")
            or soup.select_one(".headline")
        )
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Published time
        published_at = None
        time_elem = (
            soup.select_one("time")
            or soup.select_one("[data-component='timestamp']")
            or soup.select_one(".published-at")
        )
        if time_elem:
            dt = time_elem.get("datetime") or time_elem.get_text(strip=True)
            try:
                published_at = datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except Exception:
                pass

        # Summary (lede แรกๆ)
        summary = ""
        lede = (
            soup.select_one("[data-component='article-body']")
            or soup.select_one(".article-body")
            or soup.select_one("article")
        )
        if lede:
            paras = lede.select("p")[:3]
            summary = " ".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
            summary = summary[:300] + "..." if len(summary) > 300 else summary

        # ดึง content เต็ม
        content = ""
        article_body = (
            soup.select_one("[data-component='article-body']")
            or soup.select_one(".article-body")
            or soup.select_one("article")
        )
        if article_body:
            paras = article_body.select("p")
            content_parts = []
            for p in paras:
                text = p.get_text(strip=True)
                if text and len(text) > 30:
                    content_parts.append(text)
            content = "\n\n".join(content_parts)

        # ถ้าได้ content น้อยกว่า threshold ใช้ Playwright ดึงใหม่
        if not content or len(content) < self.MIN_CONTENT_LENGTH:
            full_text = self.extract_full_article(url)
            if full_text and len(full_text) > len(content):
                content = full_text

        if not content:
            content = summary

        impact_tags = self._detect_impact_tags(title + " " + summary)

        return NewsArticle(
            title=title,
            url=url,
            source=self.source_name,
            category=self._categorize(title, summary),
            published_at=published_at,
            summary=summary,
            content=content,
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _categorize(self, title: str, text: str) -> str:
        combined = (title + " " + text).lower()
        if any(w in combined for w in ["bitcoin", "crypto", "ethereum", "blockchain", "defi"]):
            return "crypto"
        if any(w in combined for w in ["fed", "rate", "inflation", "cpi", "gdp", "ecb", "boe"]):
            return "economy"
        if any(w in combined for w in ["stock", "market", "shares", "equity", "trading", "s&p", "nasdaq"]):
            return "markets"
        return "finance"

    def _detect_impact_tags(self, text: str) -> List[str]:
        text_lower = text.lower()
        tags = []
        if any(w in text_lower for w in ["bitcoin", "btc", "ethereum", "eth", "crypto"]):
            tags.append("CRYPTO")
        if any(w in text_lower for w in ["gold", "xau", "silver", "oil", "commodity"]):
            tags.append("XAUUSD")
        if any(w in text_lower for w in ["fed", "rate", "dollar", "usd"]):
            tags.append("FOREX")
        if any(w in text_lower for w in ["stock", "market", "s&p", "nasdaq", "dow"]):
            tags.append("INDEX")
        return list(set(tags)) if tags else ["GENERAL"]
