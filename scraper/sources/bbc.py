"""
scraper/sources/bbc.py — BBC News Scraper
ดึงข่าวจาก BBC เน้นข่าวระหว่างประเทศ สงคราม และเหตุการณ์สำคัญ
"""
from typing import List, Optional
from datetime import datetime
import logging

from .base import BaseScraper, NewsArticle

logger = logging.getLogger(__name__)


class BBCScraper(BaseScraper):
    """Scraper สำหรับ BBC News — ข่าวต่างประเทศและสงคราม"""

    source_name = "BBC News"
    base_url = "https://www.bbc.com"
    categories = ["war", "international", "politics", "economy"]

    RSS_URLS = {
        "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
        "uk": "https://feeds.bbci.co.uk/news/uk/rss.xml",
        "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
        "science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    }

    def get_article_urls(self) -> List[str]:
        import feedparser

        urls = []
        for name, url in self.RSS_URLS.items():
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries[:10]:
                    if hasattr(entry, "link"):
                        urls.append(entry.link)
            except Exception as e:
                logger.warning(f"[BBC] RSS feed error ({name}): {e}")
        return urls

    def parse_article(self, url: str) -> Optional[NewsArticle]:
        html = self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)

        # Title
        title = ""
        title_elem = soup.select_one("h1") or soup.select_one("[data-testid='heading']")
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
        article_body = (
            soup.select_one("[data-component='text-block']")
            or soup.select_one("article")
            or soup.select_one(".article-body")
        )
        if article_body:
            paras = article_body.select("p")[:4]
            summary = " ".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))
            summary = summary[:300] + "..." if len(summary) > 300 else summary

        combined = (title + " " + summary).lower()
        impact_tags = self._detect_impact_tags(combined)

        return NewsArticle(
            title=title,
            url=url,
            source=self.source_name,
            category=self._categorize(combined),
            published_at=published_at,
            summary=summary,
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _categorize(self, text: str) -> str:
        WAR_KEYWORDS = [
            "war", "military", "conflict", "attack", "invasion", "battle",
            "ukraine", "russia", "israel", "gaza", "iran", "nuclear",
            "missile", "drone", "troop", "ceasefire", "sanction", "nato",
            "hamas", "hezbollah", "taiwan", "china", "south china sea",
        ]
        ECONOMY_KEYWORDS = ["economy", "inflation", "recession", "trade", "tariff", "gdp", "growth"]

        if any(w in text for w in WAR_KEYWORDS):
            return "war"
        if any(w in text for w in ECONOMY_KEYWORDS):
            return "economy"
        return "international"

    def _detect_impact_tags(self, text: str) -> List[str]:
        tags = []

        # สงคราม/ความขัดแย้ง กระทบตลาด
        WAR_TAGS = {
            "ukraine": ["EUR", "NATURAL_GAS", "WHEAT", "RUB"],
            "russia": ["OIL", "NATURAL_GAS", "RUB", "EUR"],
            "israel": ["OIL", "GOLD", "XAUUSD"],
            "gaza": ["OIL", "GOLD", "XAUUSD"],
            "iran": ["OIL", "GOLD", "XAUUSD"],
            "taiwan": ["SEMICONDUCTOR", "TSMC", "NASDAQ"],
            "china": ["CNY", "CNH", "HSI", "OIL", "COPPER"],
        }

        for keyword, tag_list in WAR_TAGS.items():
            if keyword in text:
                tags.extend(tag_list)

        # ตลาดการเงิน
        if any(w in text for w in ["fed", "rate hike", "interest rate"]):
            tags.extend(["USD", "DXY", "TREASURY"])
        if any(w in text for w in ["stock market", "shares", "rally", "selloff"]):
            tags.extend(["SPX", "NDX", "INDEX"])
        if any(w in text for w in ["bitcoin", "crypto"]):
            tags.append("CRYPTO")
        if any(w in text for w in ["gold", "xau"]):
            tags.append("XAUUSD")
        if any(w in text for w in ["oil", "crude", "opec"]):
            tags.append("OIL")

        return list(set(tags)) if tags else ["GENERAL"]
