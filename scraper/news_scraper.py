"""
scraper/news_scraper.py — Main News Scraper
รวม scrapers ทั้งหมด + sentiment analysis + SQLite storage
"""
import logging
import sqlite3
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
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
    content_th TEXT,          -- เนื้อหาแปลไทยแล้ว
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

-- Archive table: เก็บข่าวเก่าเกิน retention period
CREATE TABLE IF NOT EXISTS articles_archive (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    source TEXT NOT NULL,
    category TEXT NOT NULL,
    published_at TEXT,
    summary TEXT,
    content TEXT,
    content_th TEXT,
    sentiment_score REAL DEFAULT 0.0,
    sentiment_keywords TEXT,
    impact_tags TEXT,
    raw_data TEXT,
    scraped_at TEXT,
    is_read INTEGER DEFAULT 0,
    archived_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_archive_scraped ON articles_archive(scraped_at);
CREATE INDEX IF NOT EXISTS idx_archive_source ON articles_archive(source);

CREATE TABLE IF NOT EXISTS scrape_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scraped_at TEXT DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    articles_count INTEGER,
    status TEXT,
    error TEXT
);

-- Archive policy metadata
CREATE TABLE IF NOT EXISTS archive_policy (
    id INTEGER PRIMARY KEY,
    retention_days INTEGER DEFAULT 7,      -- เก็บข่าวใน main table กี่วัน
    last_archived_at TEXT
);
INSERT OR IGNORE INTO archive_policy (id, retention_days) VALUES (1, 7);
"""


@contextmanager
def get_db():
    """เชื่อมต่อ DB"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    # migrate เพิ่ม column ถ้ายังไม่มี
    migrate_add_content_th(conn)
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


def migrate_add_content_th(conn):
    """เพิ่ม column content_th สำหรับ DB เก่า"""
    try:
        conn.execute("ALTER TABLE articles ADD COLUMN content_th TEXT")
        print("[DB Migration] Added content_th column")
    except sqlite3.OperationalError:
        pass  # column already exists


# ── Archival System ──────────────────────────────────────────

def get_archive_policy(conn) -> Dict:
    """ดึง archive policy"""
    row = conn.execute("SELECT * FROM archive_policy WHERE id = 1").fetchone()
    if not row:
        return {"retention_days": 7, "last_archived_at": None}
    return dict(row)


def set_archive_retention(days: int) -> Dict:
    """ตั้ง retention period"""
    with get_db() as conn:
        conn.execute(
            "UPDATE archive_policy SET retention_days = ? WHERE id = 1",
            (days,)
        )
    return {"retention_days": days}


def archive_old_articles(retention_days: int = 7) -> Dict:
    """
    ย้ายข่าวเก่ากว่า retention_days ไป archive table
    Returns: {moved_count, errors}
    """
    cutoff = (datetime.now() - timedelta(days=retention_days)).isoformat()

    with get_db() as conn:
        # ดึงข่าวที่จะ archive
        old_articles = conn.execute(
            "SELECT * FROM articles WHERE scraped_at < ?",
            (cutoff,)
        ).fetchall()

        moved_count = 0
        errors = []

        for row in old_articles:
            try:
                art = dict(row)
                # Insert ไป archive table
                conn.execute("""
                    INSERT OR REPLACE INTO articles_archive (
                        id, title, url, source, category, published_at,
                        summary, content, content_th, sentiment_score,
                        sentiment_keywords, impact_tags, raw_data,
                        scraped_at, is_read, archived_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    art["id"], art["title"], art["url"], art["source"],
                    art["category"], art.get("published_at"),
                    art.get("summary", ""), art.get("content", ""),
                    art.get("content_th", ""), art.get("sentiment_score", 0.0),
                    art.get("sentiment_keywords", "[]"), art.get("impact_tags", "[]"),
                    art.get("raw_data", "{}"), art.get("scraped_at"),
                    art.get("is_read", 0)
                ))

                # ลบออกจาก main table
                conn.execute("DELETE FROM articles WHERE id = ?", (art["id"],))
                moved_count += 1

            except Exception as e:
                errors.append(f"Article {row['id']}: {e}")

        # อัปเดต last_archived_at
        conn.execute(
            "UPDATE archive_policy SET last_archived_at = CURRENT_TIMESTAMP WHERE id = 1"
        )

        logger.info(f"[Archive] Moved {moved_count} articles to archive, {len(errors)} errors")

        return {
            "moved_count": moved_count,
            "retention_days": retention_days,
            "cutoff": cutoff,
            "errors": errors
        }


def get_archived_articles(
    limit: int = 50,
    category: Optional[str] = None,
    source: Optional[str] = None,
) -> List[Dict]:
    """ดึงข่าวจาก archive table"""
    import json

    query = "SELECT * FROM articles_archive WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)

    if source:
        query += " AND source = ?"
        params.append(source)

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

            score = art.get("sentiment_score", 0)
            art["sentiment_label"] = (
                "positive" if score > 0.2
                else "negative" if score < -0.2
                else "neutral"
            )
            articles.append(art)

        return articles


def get_archive_stats() -> Dict:
    """ดึง stats ของ archive"""
    with get_db() as conn:
        main_count = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        archive_count = conn.execute("SELECT COUNT(*) FROM articles_archive").fetchone()[0]
        policy = get_archive_policy(conn)

        return {
            "main_table_count": main_count,
            "archive_count": archive_count,
            "retention_days": policy["retention_days"],
            "last_archived_at": policy.get("last_archived_at"),
        }


def prune_archive(before_date: str) -> int:
    """ลบข่าวใน archive ก่อน before_date (YYYY-MM-DD)"""
    with get_db() as conn:
        result = conn.execute(
            "DELETE FROM articles_archive WHERE archived_at < ?",
            (before_date,)
        )
        logger.info(f"[Prune] Deleted {result.rowcount} archived articles before {before_date}")
        return result.rowcount


def get_article_by_id(article_id: int) -> Optional[Dict]:
    """ดึงข่าวเดียว by ID พร้อม translate content เป็นไทย"""
    import json

    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM articles WHERE id = ?", (article_id,)
        ).fetchone()

        if not row:
            return None

        art = dict(row)
        try:
            art["sentiment_keywords"] = json.loads(art.get("sentiment_keywords") or "[]")
            art["impact_tags"] = json.loads(art.get("impact_tags") or "[]")
        except Exception:
            pass

        # แปลง sentiment_label
        score = art.get("sentiment_score", 0)
        art["sentiment_label"] = (
            "positive" if score > 0.2
            else "negative" if score < -0.2
            else "neutral"
        )

        # แปล content เป็นไทยถ้ามี (ทำนอก context manager ก่อน)
        content = art.get("content", "")
        content_th = None
        if content and not art.get("content_th"):
            content_th = translate_content_to_thai(content)

        # บันทึก translation ลง DB
        if content_th:
            conn.execute(
                "UPDATE articles SET content_th = ? WHERE id = ?",
                (content_th, article_id)
            )
            art["content_th"] = content_th

        return art


def translate_content_to_thai(content: str) -> str:
    """แปล content ข่าวเป็นภาษาไทยด้วย MiniMax"""
    import os
    import sys
    from pathlib import Path
    from dotenv import load_dotenv

    if not content or len(content.strip()) < 10:
        return content

    # โหลด .env ก่อน (ระบุ path แบบ absolute)
    from pathlib import Path
    hermes_env = Path.home() / ".hermes" / ".env"
    load_dotenv(hermes_env)

    # เพิ่ม backend path เพื่อ import MiniMaxChatClient
    backend_path = Path(__file__).parent.parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    try:
        from backend.ai.minimax_client import MiniMaxChatClient

        client = MiniMaxChatClient(
            api_key=os.getenv("MINIMAX_API_KEY", ""),
            base_url=os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1"),
            model=os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5"),
        )

        messages = [
            {
                "role": "system",
                "content": "คุณคือนักแปลข่าวมืออาชีพ แปลเนื้อหาข่าวเป็นภาษาไทยที่เข้าใจง่าย รักษาความหมายเดิม ถ้าเป็นชื่อคน ชื่อองค์กร ให้ทับศัพท์"
            },
            {
                "role": "user",
                "content": f"แปลข่าวต่อไปนี้เป็นภาษาไทย:\n\n{content[:8000]}"
            }
        ]

        response = client.chat_completions_create(
            messages=messages,
            temperature=0.3,
            max_tokens=8192,
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.warning(f"Translation failed: {e}")
        return content  # fallback: return original


def analyze_market_impact(title: str, content: str, tags: List[str]) -> Dict[str, Any]:
    """
    ใช้ AI วิเคราะห์ว่าข่าวส่งผลกับตลาด/สินทรัพย์อะไรบ้าง
    Returns: {impact_instruments: [...], reasoning: str, sentiment: str, risk_level: str}
    """
    import os
    import sys
    from pathlib import Path
    from dotenv import load_dotenv

    if not title:
        return {
            "impact_instruments": [],
            "reasoning": "",
            "sentiment": "neutral",
            "risk_level": "low",
        }

    # โหลด .env ก่อน (ระบุ path แบบ absolute)
    from pathlib import Path
    hermes_env = Path.home() / ".hermes" / ".env"
    load_dotenv(hermes_env)

    # เพิ่ม backend path สำหรับ MiniMax client
    backend_path = Path(__file__).parent.parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))

    try:
        from backend.ai.minimax_client import MiniMaxChatClient

        client = MiniMaxChatClient(
            api_key=os.getenv("MINIMAX_API_KEY", ""),
            base_url=os.getenv("MINIMAX_BASE_URL", "https://api.minimax.io/v1"),
            model=os.getenv("MINIMAX_MODEL_NAME", "MiniMax-M2.5"),
        )

        prompt = f"""คุณคือนักวิเคราะห์ตลาดการเงิน ดูข่าวแล้วบอกว่าส่งผลกับสินทรัพย์/ตลาดอะไรบ้าง

หัวข้อข่าว: {title}
เนื้อหา (ถ้ามี): {content[:2000]}
Tags: {', '.join(tags)}

ตอบเป็น JSON ที่มี format ต่อไปนี้เท่านั้น (ไม่ต้องอธิบายเพิ่ม):
{{
  "impact_instruments": ["USD", "EUR", "XAUUSD", "OIL", "BTC", "SPX", "NDX", "THB", "JPY", "GBP", ...],
  "reasoning": "เหตุผลที่คิดว่าส่งผลตรงนี้ สั้นๆ 1-2 ประโยค",
  "sentiment": "bullish | bearish | neutral",
  "risk_level": "low | medium | high",
  "time_horizon": "short-term | medium-term | long-term",
  "affected_countries": ["US", "EU", "TH", "CN", ...]
}}

กฎ:
- ถ้าข่าวเศรษฐกิจสหรัฐ → USD, DXY, TREASURY, SPX
- ถ้าข่าวสงคราม/ความขัดแย้ง → GOLD, XAUUSD, OIL, USD (safe haven)
- ถ้าข่าวคริปโต → BTC, ETH
- ถ้าข่าวไทย → THB, SET Index
- ถ้าข่าวยุโรป → EUR, GBP
- ถ้าข่าวเงินเฟ้อ/Fed → USD, TREASURY, DXY
- ถ้าข่าว China → CNY, HSI, OIL, COPPER
"""

        messages = [
            {"role": "user", "content": prompt}
        ]

        response = client.chat_completions_create(
            messages=messages,
            temperature=0.2,
            max_tokens=1024,
        )

        raw = response["choices"][0]["message"]["content"].strip()

        # ดึง JSON จาก response
        import re
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            import json
            return json.loads(match.group())
        else:
            return {
                "impact_instruments": tags,
                "reasoning": raw[:200],
                "sentiment": "neutral",
                "risk_level": "low",
            }

    except Exception as e:
        logger.warning(f"Impact analysis failed: {e}")
        return {
            "impact_instruments": tags,
            "reasoning": f"Error: {e}",
            "sentiment": "neutral",
            "risk_level": "unknown",
        }


def process_article_with_ai(article_id: int) -> Dict[str, Any]:
    """
    ดึงข่าวจาก DB → แปลเป็นไทย → วิเคราะห์ผลกระทบตลาด
    แล้วบันทึก content_th + impact reasoning ลง DB
    """
    import json

    # ดึงข่าว
    with get_db() as conn:
        row = conn.execute(
            "SELECT id, title, content, content_th, impact_tags, summary FROM articles WHERE id = ?",
            (article_id,),
        ).fetchone()
    if not row:
        return {"error": "Article not found"}

    art = dict(row)
    art["impact_tags"] = json.loads(art["impact_tags"]) if art["impact_tags"] else []

    results = {}

    # 1. Translate to Thai
    content_th = art.get("content_th")  # None ถ้ายังไม่เคยแปล
    if not content_th and art.get("content"):
        logger.info(f"[AI] Translating article {article_id} to Thai")
        content_th = translate_content_to_thai(art["content"])
        with get_db() as conn:
            conn.execute(
                "UPDATE articles SET content_th = ? WHERE id = ?",
                (content_th, article_id),
            )
        results["translated"] = len(content_th)
    else:
        results["translated"] = 0

    # 2. Analyze market impact (ใช้ content_th ที่ได้จากขั้นตอนบน)
    if content_th:
        impact = analyze_market_impact(
            title=art["title"],
            content=content_th,  # ใช้ตัวแปร content_th โดยตรง ไม่ใช่ art dict
            tags=art["impact_tags"],
        )
        # บันทึก reasoning ลง impact_reasoning field
        with get_db() as conn:
            conn.execute(
                "UPDATE articles SET impact_reasoning = ?, impact_sentiment = ?, impact_risk = ? WHERE id = ?",
                (
                    impact.get("reasoning", ""),
                    impact.get("sentiment", "neutral"),
                    impact.get("risk_level", "low"),
                    article_id,
                ),
            )
        results["impact"] = impact
        results["instruments"] = impact.get("impact_instruments", [])
    else:
        results["impact"] = None

    return results


def translate_and_analyze_pending(threshold_hours: int = 24) -> List[Dict[str, Any]]:
    """
    หาข่าวที่ยังไม่ได้แปลหรือยังไม่ได้วิเคราะห์ impact ในช่วง X ชั่วโมงที่ผ่านมา
    แล้ว process ทั้งหมด
    """
    cutoff = (datetime.now() - timedelta(hours=threshold_hours)).isoformat()
    with get_db() as conn:
        rows = conn.execute(
            """SELECT id, title FROM articles
             WHERE scraped_at > ?
             AND (content_th IS NULL OR content_th = ''
                  OR impact_reasoning IS NULL OR impact_reasoning = '')
             ORDER BY scraped_at DESC
             LIMIT 10""",
            (cutoff,),
        ).fetchall()

    results = []
    for row in rows:
        art_id = row[0]
        title = row[1]
        try:
            result = process_article_with_ai(art_id)
            results.append({"id": art_id, "title": title[:60], **result})
        except Exception as e:
            logger.error(f"Failed to process article {art_id}: {e}")
            results.append({"id": art_id, "title": title[:60], "error": str(e)})

    return results


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
