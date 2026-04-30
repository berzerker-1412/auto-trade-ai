"""
scraper/sources/base.py — Base scraper class
"""
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


@dataclass
class NewsArticle:
    """โครงสร้างข้อมูลข่าว"""
    title: str
    url: str
    source: str          # ชื่อแหล่งข่าว เช่น "Reuters"
    category: str         # "finance" | "war" | "economy" | "crypto" | "general"
    published_at: Optional[datetime] = None
    summary: str = ""    # สรุปข่าว (ถ้ามี)
    content: str = ""    # เนื้อหาเต็ม (ถ้าดึงได้)
    sentiment_score: float = 0.0  # -1.0 ถึง 1.0
    impact_tags: List[str] = field(default_factory=list)  # ["BTC", "XAUUSD", "USD"]

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "summary": self.summary,
            "content": self.content[:500],  # เก็บแค่ 500 ตัวอักษรแรก
            "sentiment_score": self.sentiment_score,
            "impact_tags": self.impact_tags,
        }


class BaseScraper(ABC):
    """Base class สำหรับ news scraper ทุกตัว"""

    source_name: str = ""
    base_url: str = ""
    categories: List[str] = []  # categories ที่ scraper นี้ดูแล

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch(self, url: str, timeout: int = 10) -> Optional[str]:
        """ดึง HTML จาก URL"""
        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            logger.warning(f"[{self.source_name}] Failed to fetch {url}: {e}")
            return None

    def parse_html(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")

    @abstractmethod
    def get_article_urls(self) -> List[str]:
        """ดึง list ของ URL ข่าวล่าสุด"""
        pass

    @abstractmethod
    def parse_article(self, url: str) -> Optional[NewsArticle]:
        """ดึงรายละเอียดข่าวจาก URL"""
        pass

    def scrape(self) -> List[NewsArticle]:
        """ดึงข่าวทั้งหมดจากแหล่งนี้"""
        articles = []
        for url in self.get_article_urls():
            try:
                article = self.parse_article(url)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.warning(f"[{self.source_name}] Error parsing {url}: {e}")
        return articles

    def _safe_text(self, elem, selector: str, default: str = "") -> str:
        """ดึง text จาก element อย่างปลอดภัย"""
        if elem is None:
            return default
        el = elem.select_one(selector) if hasattr(elem, "select_one") else elem.find(selector)
        return el.get_text(strip=True) if el else default

    def _safe_attr(self, elem, attr: str, default: str = "") -> str:
        if elem is None:
            return default
        return elem.get(attr, default)
