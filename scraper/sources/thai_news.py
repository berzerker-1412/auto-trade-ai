"""
scraper/sources/thai_news.py — Thai News Scraper
ดึงข่าวจากสำนักข่าวไทย เน้นเศรษฐกิจ การเงิน และข่าวต่างประเทศ
"""
from typing import List, Optional
from datetime import datetime
import logging

from .base import BaseScraper, NewsArticle

logger = logging.getLogger(__name__)


class ThaiNewsScraper(BaseScraper):
    """Scraper สำหรับสำนักข่าวไทย"""

    source_name = "Thai News"
    categories = ["finance", "economy", "war", "general"]

    SOURCES = {
        "bangkokpost": {
            "name": "Bangkok Post",
            "rss": [
                "https://www.bangkokpost.com/rss/business.xml",
                "https://www.bangkokpost.com/rss/world.xml",
                "https://www.bangkokpost.com/rss/economy.xml",
            ],
        },
        "thaipbs": {
            "name": "Thai PBS",
            "rss": [
                "https://www.thaipbs.or.th/rss/business.xml",
                "https://www.thaipbs.or.th/rss/world.xml",
            ],
        },
        "matter": {
            "name": "Matter",
            "rss": ["https://thematter.co/feed"],
        },
    }

    def get_article_urls(self) -> List[str]:
        import feedparser

        urls = []
        for src_key, src_info in self.SOURCES.items():
            for rss_url in src_info["rss"]:
                try:
                    feed = feedparser.parse(rss_url)
                    for entry in feed.entries[:8]:
                        if hasattr(entry, "link"):
                            urls.append(entry.link)
                except Exception as e:
                    logger.warning(f"[ThaiNews] RSS error ({src_key}): {e}")
        return urls

    def parse_article(self, url: str) -> Optional[NewsArticle]:
        html = self.fetch(url)
        if not html:
            return None

        soup = self.parse_html(html)

        # Title
        title = ""
        title_elem = (
            soup.select_one("h1")
            or soup.select_one(".article-title")
            or soup.select_one(".entry-title")
            or soup.select_one("title")
        )
        if title_elem:
            title = title_elem.get_text(strip=True)

        # Published time
        published_at = None
        time_elem = soup.select_one("time") or soup.select_one("[itemprop='datePublished']")
        if time_elem:
            dt = time_elem.get("datetime") or time_elem.get_text(strip=True)
            try:
                published_at = datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except Exception:
                pass

        # Summary
        summary = ""
        article_body = (
            soup.select_one("article")
            or soup.select_one(".article-content")
            or soup.select_one(".entry-content")
            or soup.select_one(".post-content")
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
            source=self._detect_source_name(url),
            category=self._categorize(combined),
            published_at=published_at,
            summary=summary,
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _detect_source_name(self, url: str) -> str:
        for src_key, src_info in self.SOURCES.items():
            if src_key in url:
                return src_info["name"]
        return "Thai News"

    def _categorize(self, text: str) -> str:
        WAR_KEYWORDS = ["สงคราม", "conflict", "ukraine", "russia", "israel", "gaza", "iran", "ทหาร", "รบ", "โจมตี", "ชนชาติ"]
        FINANCE_KEYWORDS = ["ตลาด", "หุ้น", "บาท", "บอนด์", "ดอลลาร์", "น้ำมัน", "ทองคำ", "คริปโต", "bitcoin", "เศรษฐกิจ"]

        if any(w in text for w in WAR_KEYWORDS):
            return "war"
        if any(w in text for w in FINANCE_KEYWORDS):
            return "finance"
        return "general"

    def _detect_impact_tags(self, text: str) -> List[str]:
        tags = []
        if any(w in text for w in ["บาท", "thb", "ค่าเงินบาท"]):
            tags.append("THB")
        if any(w in text for w in ["ทองคำ", "gold", "xau"]):
            tags.append("XAUUSD")
        if any(w in text for w in ["น้ำมัน", "oil", " crude"]):
            tags.append("OIL")
        if any(w in text for w in ["bitcoin", "คริปโต", "crypto", " ethereum"]):
            tags.append("CRYPTO")
        if any(w in text for w in ["ดอลลาร์", "dollar", "usd"]):
            tags.append("USD")
        if any(w in text for w in ["สงคราม", "war", "ukraine", "russia", "conflict", "israel"]):
            tags.append("RISK_OFF")
        return list(set(tags)) if tags else ["GENERAL"]
