"""
scraper/sources/yahoo_finance.py — Yahoo Finance News Scraper
ดึงข่าวจาก Yahoo Finance RSS
"""
from typing import List, Optional
from datetime import datetime
import logging

from .base import BaseScraper, NewsArticle

logger = logging.getLogger(__name__)


class YahooFinanceScraper(BaseScraper):
    """Scraper สำหรับ Yahoo Finance News"""

    source_name = "Yahoo Finance"
    base_url = "https://finance.yahoo.com"
    categories = ["finance", "economy", "crypto", "markets"]

    RSS_URLS = {
        "news": "https://finance.yahoo.com/news/rssindex",
    }

    def get_article_urls(self) -> List[str]:
        import feedparser

        urls = []
        for name, url in self.RSS_URLS.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:15]:
                    if hasattr(entry, "link"):
                        urls.append(entry.link)
            except Exception as e:
                logger.warning(f"[YahooFinance] RSS feed error ({name}): {e}")
        return urls

    def parse_article(self, url: str) -> Optional[NewsArticle]:
        html = self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)

        # Title
        title = ""
        title_elem = soup.select_one("h1") or soup.select_one("h1.caas-title")
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Published time
        published_at = None
        time_elem = soup.select_one("time")
        if time_elem and time_elem.get("datetime"):
            try:
                published_at = datetime.fromisoformat(time_elem["datetime"].replace("Z", "+00:00"))
            except Exception:
                pass

        # Summary
        summary = ""
        summary_elem = soup.select_one(".caas-body") or soup.select_one(".article-summary")
        if summary_elem:
            summary = summary_elem.get_text(strip=True)[:300]

        # Content
        content = ""
        article_body = soup.select_one(".caas-body") or soup.select_one("article")
        if article_body:
            paras = article_body.select("p")
            content_parts = []
            for p in paras:
                text = p.get_text(strip=True)
                if text and len(text) > 30:
                    content_parts.append(text)
            content = "\n\n".join(content_parts)

        if not content:
            content = summary

        combined = (title + " " + summary).lower()
        impact_tags = self._detect_impact_tags(combined)

        return NewsArticle(
            title=title,
            url=url,
            source=self.source_name,
            category=self._categorize(combined),
            published_at=published_at,
            summary=summary,
            content=content,
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _categorize(self, text: str) -> str:
        if any(w in text for w in ["bitcoin", "crypto", "ethereum", "defi", "token", "blockchain"]):
            return "crypto"
        if any(w in text for w in ["fed", "rate", "inflation", "cpi", "gdp", "treasury", "bond", "dollar", "recession"]):
            return "economy"
        if any(w in text for w in ["stock", "market", "shares", "rally", "selloff", "nasdaq", "s&p", "dow"]):
            return "markets"
        return "finance"

    def _detect_impact_tags(self, text: str) -> List[str]:
        tags = []
        CRYPTO = ["bitcoin", "btc", "ethereum", "eth", "solana", "bnb", "xrp", "crypto"]
        COMMODITY = ["gold", "xauusd", "silver", "oil", "crude"]
        FOREX = ["usd", "dollar", "yen", "jpy", "euro", "gbp"]
        INDEX = ["s&p", "spx", "nasdaq", "dow", "ftse"]

        for tag in CRYPTO:
            if tag in text:
                tags.append("CRYPTO")
                break
        for tag in COMMODITY:
            if tag in text:
                tags.append("XAUUSD" if "gold" in tag else "COMMODITY")
                break
        for tag in FOREX:
            if tag in text:
                tags.append("FOREX")
                break
        for tag in INDEX:
            if tag in text:
                tags.append("INDEX")
                break

        return list(set(tags)) if tags else ["GENERAL"]
