"""
scraper/news_scraper.py — Main News Scraper
รวม scrapers ทั้งหมด + sentiment analysis + SQLite storage
"""
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from contextlib import contextmanager
from pathlib import Path

from .sources import ALL_SCRAPERS
from .sentiment import analyze_sentiment, get_trade_signal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "news.db"


# ── Database Schema ─────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    source TEXT NOT NULL,
    category TEXT NOT NULL,
    published_at TEXT,
    summary TEXT,
    content TEXT,
    sentiment_score REAL DEFAULT 0.0,
    sentiment_keywords TEXT,  -- JSON array of matched keywords
    impact_tags TEXT,          -- JSON array
    raw_data TEXT,             -- JSON full article data
    scraped_at TEXT DEFAULT CURRENT_TIMESTAMP,
    is_read INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_articles_source ON articles(source);
CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category);
CREATE INDEX IF NOT EXISTS idx_articles_scraped ON articles(scraped_at);
CREATE TABLE IF NOT EXISTS scrape_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scraped_at TEXT DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    articles_count INTEGER,
    status TEXT,
    error TEXT
);
"""


@contextmanager
def get_db():
    """เชื่อมต่อ DB"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def save_article(article: Dict) -> Optional[int]:
    """บันทึกข่าวลง DB (ถ้าซ้ำจะไม่บันทึก)"""
    import json

    with get_db() as conn:
        # ตรวจสอบซ้ำ
        exists = conn.execute(
            "SELECT id FROM articles WHERE url = ?", (article["url"],)
        ).fetchone()

        if exists:
            return exists["id"]

        cursor = conn.execute("""
            INSERT INTO articles (
                title, url, source, category, published_at,
                summary, content, sentiment_score, sentiment_keywords,
                impact_tags, raw_data
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            article["title"],
            article["url"],
            article["source"],
            article["category"],
            article.get("published_at"),
            article.get("summary", ""),
            article.get("content", ""),
            article.get("sentiment_score", 0.0),
            json.dumps(article.get("sentiment_keywords", [])),
            json.dumps(article.get("impact_tags", [])),
            json.dumps(article.get("raw_data", {})),
        ))
        return cursor.lastrowid


def get_articles(
    limit: int = 50,
    category: Optional[str] = None,
    source: Optional[str] = None,
    since_hours: Optional[int] = None,
) -> List[Dict]:
    """ดึงข่าวจาก DB"""
    import json

    query = "SELECT * FROM articles WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if source:
        query += " AND source = ?"
        params.append(source)

    if since_hours:
        cutoff = (datetime.now() - timedelta(hours=since_hours)).isoformat()
        query += " AND scraped_at > ?"
        params.append(cutoff)

    query += " ORDER BY scraped_at DESC LIMIT ?"
    params.append(limit)

    with get_db() as conn:
        rows = conn.execute(query, params).fetchall()
        articles = []
        for row in rows:
            art = dict(row)
            try:
                art["sentiment_keywords"] = json.loads(art.get("sentiment_keywords") or "[]")
                art["impact_tags"] = json.loads(art.get("impact_tags") or "[]")
            except Exception:
                pass
            articles.append(art)
        return articles


def get_news_feed(limit: int = 30) -> Dict:
    """ดึงข่าวทั้งหมด + trade signal"""
    articles = get_articles(limit=limit)
    trade_signal = get_trade_signal(articles)

    # แปลง sentiment score
    for art in articles:
        art["sentiment_label"] = (
            "positive" if art["sentiment_score"] > 0.2
            else "negative" if art["sentiment_score"] < -0.2
            else "neutral"
        )

    return {
        "articles": articles,
        "trade_signal": trade_signal,
        "total": len(articles),
        "generated_at": datetime.now().isoformat(),
    }


# ── Main Scraper Class ──────────────────────────────────────
class NewsScraper:
    """
    ดึงข่าวจากทุกแหล่ง + วิเคราะห์ sentiment + บันทึกลง DB

    Usage:
        scraper = NewsScraper()
        result = scraper.scrape_all()
        feed = get_news_feed(limit=50)
    """

    def __init__(self):
        self.scrapers = [cls() for cls in ALL_SCRAPERS]
        self.results = []

    def scrape_all(self, max_per_source: int = 20) -> Dict:
        """ดึงข่าวจากทุกแหล่ง"""
        total_articles = 0
        errors = []

        for scraper_cls in ALL_SCRAPERS:
            scraper = scraper_cls()
            source_name = scraper.source_name

            logger.info(f"[NewsScraper] Scraping {source_name}...")

            try:
                articles = scraper.scrape()

                saved_count = 0
                for article in articles[:max_per_source]:
                    try:
                        # วิเคราะห์ sentiment
                        text = article.title + " " + article.summary
                        score, keywords = analyze_sentiment(text)
                        article.sentiment_score = score

                        # บันทึกลง DB
                        art_dict = article.to_dict()
                        art_dict["sentiment_keywords"] = keywords
                        saved_id = save_article(art_dict)

                        if saved_id:
                            saved_count += 1
                            self.results.append(art_dict)

                    except Exception as e:
                        logger.warning(f"[{source_name}] Error saving article: {e}")

                total_articles += saved_count

                # Log
                with get_db() as conn:
                    conn.execute("""
                        INSERT INTO scrape_log (source, articles_count, status)
                        VALUES (?, ?, ?)
                    """, (source_name, saved_count, "success"))

                logger.info(f"[NewsScraper] {source_name}: saved {saved_count} articles")

            except Exception as e:
                error_msg = str(e)
                errors.append(f"{source_name}: {error_msg}")
                logger.error(f"[NewsScraper] {source_name} failed: {e}")

                with get_db() as conn:
                    conn.execute("""
                        INSERT INTO scrape_log (source, articles_count, status, error)
                        VALUES (?, ?, ?, ?)
                    """, (source_name, 0, "error", error_msg))

        return {
            "total_saved": total_articles,
            "sources_scraped": len(ALL_SCRAPERS),
            "errors": errors,
            "articles": self.results,
        }

    def get_feed(self, limit: int = 50) -> Dict:
        """ดึง feed �พร้อม trade signal"""
        return get_news_feed(limit=limit)
