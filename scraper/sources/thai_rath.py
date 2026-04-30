"""
scraper/sources/thai_rath.py — Thai Rath News Scraper
ดึงข่าวจาก Thai Rath API เน้นเศรษฐกิจ การเงิน และข่าวในประเทศ

API: https://api.thairath.co.th/tr-api/v1.1/news/latested
"""
import logging
import requests
from datetime import datetime
from typing import List, Optional

from .base import BaseScraper, NewsArticle

logger = logging.getLogger(__name__)

# Topic sections ที่สนใจ (API path)
TOPIC_PATHS = {
    "economy": "news/economy",
    "finance": "news/finance",
    "national": "news",
    "world": "news/foreign",
    "business": "business",
}


class ThaiRathScraper(BaseScraper):
    """Scraper สำหรับ Thai Rath — ใช้ REST API"""

    source_name = "ไทยรัฐ"
    base_url = "https://www.thairath.co.th"
    categories = list(TOPIC_PATHS.keys())

    API_BASE = "https://api.thairath.co.th/tr-api/v1.1"

    def __init__(self):
        super().__init__()
        self.session.headers.update({
            "Accept": "application/json",
            "Referer": "https://www.thairath.co.th/",
            "Origin": "https://www.thairath.co.th",
        })

    def _api_get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """เรียก Thai Rath API อย่างปลอดภัย"""
        try:
            resp = self.session.get(
                f"{self.API_BASE}/{endpoint}",
                params=params or {},
                timeout=10,
            )
            if resp.status_code == 200:
                return resp.json()
            else:
                logger.warning(f"[ThaiRath] API {endpoint} → {resp.status_code}")
                return None
        except Exception as e:
            logger.warning(f"[ThaiRath] API error {endpoint}: {e}")
            return None

    def get_article_urls(self) -> List[str]:
        """ดึง URLs จาก API หลายหน้า"""
        all_urls = []
        seen = set()

        # ดึงหลายหน้าของ latest news
        for page in range(1, 6):  # 5 หน้า = ข่าวล่าสุด ~40 ข่าว
            data = self._api_get("news/latested", {"page": page})
            if not data:
                break

            items = data.get("items", [])
            if not items:
                break

            for item in items:
                url = item.get("canonical") or item.get("fullPath")
                if url and url not in seen:
                    if not url.startswith("http"):
                        url = f"https://www.thairath.co.th/{url.lstrip('/')}"
                    seen.add(url)
                    all_urls.append(url)

            logger.info(f"[ThaiRath] page {page}: {len(items)} items")

        # ดึงเพิ่มจาก section ต่างๆ
        section_seen = set(all_urls)
        for topic_key, topic_path in TOPIC_PATHS.items():
            # ดึง 2 หน้าแรกของแต่ละ section
            for page in range(1, 3):
                data = self._api_get(f"news/{topic_key}", {"page": page})
                if not data:
                    # fallback: ใช้ latest
                    data = self._api_get("news/latested", {"page": page})
                if not data:
                    break

                items = data.get("items", [])
                if not items:
                    break

                for item in items:
                    url = item.get("canonical") or item.get("fullPath")
                    if url and url not in section_seen:
                        if not url.startswith("http"):
                            url = f"https://www.thairath.co.th/{url.lstrip('/')}"
                        section_seen.add(url)
                        all_urls.append(url)

        logger.info(f"[ThaiRath] Total unique URLs: {len(all_urls)}")
        return all_urls

    def parse_article(self, url: str) -> Optional[NewsArticle]:
        """
        ดึง article content จาก URL
        ถ้าเป็น Thai Rath URL: ใช้ API ดึง content เต็ม
        """
        # ดึง ID จาก URL
        # URL format: https://www.thairath.co.th/news/foreign/2929993
        article_id = url.rstrip("/").split("/")[-1]
        topic = url.rstrip("/").split("/")[-2] if "/" in url else ""

        # เรียก API ดึง content
        data = self._api_get(f"news/content/{article_id}")
        if not data:
            # Fallback: ใช้ parse จาก page HTML
            return self._parse_html_article(url)

        item = data.get("data", {}) or data

        title = item.get("title", "")
        abstract = item.get("abstract", "")
        content = item.get("content", "") or abstract
        section = item.get("section", "")
        topic_name = item.get("topic", "")
        tags = item.get("tags", [])

        # Published time
        published_at = None
        pub_ts = item.get("publishTs")
        if pub_ts:
            try:
                published_at = datetime.fromtimestamp(pub_ts / 1000)
            except Exception:
                pass
        else:
            pub_time = item.get("publishTime")
            if pub_time:
                try:
                    published_at = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                except Exception:
                    pass

        combined = (title + " " + abstract).lower()
        impact_tags = self._detect_impact_tags(combined, tags)
        category = self._categorize(combined, topic, topic_name)

        summary = abstract[:300] + "..." if len(abstract) > 300 else abstract

        return NewsArticle(
            title=title,
            url=url,
            source=self.source_name,
            category=category,
            published_at=published_at,
            summary=summary,
            content=content,
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _parse_html_article(self, url: str) -> Optional[NewsArticle]:
        """Parse จาก HTML — ดึง data จาก __NEXT_DATA__ + Schema.org JSON-LD"""
        import json as json_lib

        html = self.fetch(url)
        if not html:
            return None

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")

        title = ""
        summary = ""
        published_at = None
        tags = []
        topic = ""
        topic_name = ""
        combined = ""

        # 1. ลอง __NEXT_DATA__ (Next.js SSR data)
        next_data = soup.find("script", {"id": "__NEXT_DATA__"})
        if next_data and next_data.string:
            try:
                nd = json_lib.loads(next_data.string)
                article_data = (
                    nd.get("props", {})
                    .get("initialState", {})
                    .get("common", {})
                    .get("data", {})
                )
                title = article_data.get("title", "")
                summary = article_data.get("description", "") or article_data.get("abstract", "")
                tags = article_data.get("tags", [])
                topic = article_data.get("sectionName", "")
                topic_name = article_data.get("topicName", "")
                pub_time = article_data.get("publishTime")
                if pub_time:
                    try:
                        published_at = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                    except Exception:
                        pass
                combined = (title + " " + summary).lower()
            except Exception:
                pass

        # 2. ถ้ายังไม่มี title ลอง Schema.org JSON-LD
        if not title:
            schema_scripts = soup.find_all("script", {"type": "application/ld+json"})
            for s in schema_scripts:
                try:
                    sd = json_lib.loads(s.string)
                    if sd.get("@type") == "NewsArticle":
                        title = sd.get("headline", "")
                        summary = sd.get("description", "")
                        pub_iso = sd.get("datePublished")
                        if pub_iso:
                            try:
                                published_at = datetime.fromisoformat(pub_iso.replace("Z", "+00:00"))
                            except Exception:
                                pass
                        combined = (title + " " + summary).lower()
                        break
                except Exception:
                    pass

        # 3. Fallback: basic HTML parse
        if not title:
            title_elem = soup.select_one("h1") or soup.select_one("title")
            if title_elem:
                title = title_elem.get_text(strip=True)
            time_elem = soup.select_one("time") or soup.select_one("[itemprop='datePublished']")
            if time_elem:
                dt = time_elem.get("datetime") or time_elem.get_text(strip=True)
                try:
                    published_at = datetime.fromisoformat(dt.replace("Z", "+00:00"))
                except Exception:
                    pass
            combined = title.lower()

        if not summary:
            article_body = soup.select_one("article") or soup.select_one(".article-content")
            if article_body:
                paras = article_body.select("p")[:4]
                summary = " ".join(p.get_text(strip=True) for p in paras if p.get_text(strip=True))

        summary = summary[:500] + "..." if len(summary) > 500 else summary
        impact_tags = self._detect_impact_tags(combined, tags)
        category = self._categorize(combined, topic, topic_name)

        return NewsArticle(
            title=title,
            url=url,
            source=self.source_name,
            category=category,
            published_at=published_at,
            summary=summary,
            content=summary,  # summary ก็คือ content ในที่นี้
            sentiment_score=0.0,
            impact_tags=impact_tags,
        )

    def _categorize(self, text: str, topic: str, topic_name: str) -> str:
        # ใช้ topic จาก API ก่อน
        topic_lower = (topic + " " + topic_name).lower()

        FINANCE_KEYWORDS = ["ตลาด", "หุ้น", "บาท", "ค่าเงิน", "ดอลลาร์", "บอนด์", "น้ำมัน", "ทองคำ", "คริปโต", "เศรษฐกิจ", "การเงิน", "ลงทุน", "ตลาดหุ้น"]
        WORLD_KEYWORDS = ["ต่างประเทศ", "foreign", "อเมริกา", "ยุโรป", "จีน", "รัสเซีย", "อิหร่าน", "สงคราม"]

        if any(w in topic_lower for w in ["foreign", "world", "ต่างประเทศ"]):
            return "world"
        if any(w in topic_lower for w in ["economy", "finance", "เศรษฐกิจ", "การเงิน"]):
            return "finance"
        if any(w in text for w in WORLD_KEYWORDS):
            return "world"
        if any(w in text for w in FINANCE_KEYWORDS):
            return "finance"
        return "national"

    def _detect_impact_tags(self, text: str, tags: List[str]) -> List[str]:
        tag_set = set()
        all_text = text + " " + " ".join(tags)

        if any(w in all_text for w in ["บาท", "thb", "ค่าเงินบาท", "THB", "เงินบาท"]):
            tag_set.add("THB")
        if any(w in all_text for w in ["ทองคำ", "gold", "xau", "ราคาทอง", "ทอง"]):
            tag_set.add("XAUUSD")
        if any(w in all_text for w in ["น้ำมัน", "oil", "crude", "ปิโตรเลียม"]):
            tag_set.add("OIL")
        if any(w in all_text for w in ["bitcoin", "คริปโต", "crypto", "บิตคอย", "cryptocurrency"]):
            tag_set.add("CRYPTO")
        if any(w in all_text for w in ["ดอลลาร์", "dollar", "usd", "ดอล", "สหรัฐ"]):
            tag_set.add("USD")
        if any(w in all_text for w in ["สงคราม", "war", "ukraine", "russia", "israel", "อิหร่าน", "ซีเรีย", "ความขัดแย้ง"]):
            tag_set.add("RISK_OFF")
        if any(w in all_text for w in ["ดอกเบี้ย", "fed", "กนง.", "ธปท.", "ธนาคารแห่งประเทศไทย"]):
            tag_set.add("THB")
        if any(w in all_text for w in ["หุ้น", "ตลาดหุ้น", " SET", "mai", "index"]):
            tag_set.add("SET")

        return list(tag_set) if tag_set else ["GENERAL"]
