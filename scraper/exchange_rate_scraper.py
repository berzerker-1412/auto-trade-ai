"""
scraper/exchange_rate_scraper.py
────────────────────────────────
Web scraper สำหรับเก็บอัตราแลกเปลี่ยนเงินตราทุกวัน
ใช้ requests + BeautifulSoup ดึงข้อมูลจาก Google Finance, Exchange Rates API

ข้อมูลที่ดึง:
  - THB/USD (บาทต่อดอลลาร์)
  - USD/THB (ดอลลาร์ต่อบาท)
  - EUR/THB, JPY/THB, GBP/THB
  - Crypto prices (BTC, ETH) ใน THB

วิธีใช้:
  python -m scraper.exchange_rate_scraper

วางไว้ใน cron รันทุกวัน:
  0 0 * * * cd /path/to/auto-trade-ai && python -m scraper.exchange_rate_scraper >> logs/exchange.log 2>&1
"""

import requests
import sqlite3
import json
import logging
import time
from datetime import datetime, date
from pathlib import Path

# Setup logging
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "exchange.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ── Database ────────────────────────────────────────────────
DB_PATH = Path(__file__).parent.parent / "data" / "exchange_rates.db"


def init_db():
    """สร้างตาราง exchange_rates ถ้ายังไม่มี"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                base_currency TEXT NOT NULL,
                quote_currency TEXT NOT NULL,
                rate REAL NOT NULL,
                source TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, base_currency, quote_currency)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                symbol TEXT NOT NULL,
                price_usd REAL NOT NULL,
                price_thb REAL,
                market_cap REAL,
                source TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, symbol)
            )
        """)
        conn.commit()
    logger.info(f"Database initialized at {DB_PATH}")


# ── Exchange Rates API ──────────────────────────────────────
def get_exchange_rate_api() -> dict:
    """
    ดึงอัตราแลกเปลี่ยนจาก exchangerate-api.com (ฟรี)
    Free tier: 1500 requests/month
    """
    try:
        # ดึง THB ทั้งหมดเทียบ USD
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        rates = {}
        for currency in ["THB", "EUR", "JPY", "GBP", "CNY", "SGD", "AUD", "KRW"]:
            if currency in data["rates"]:
                rates[f"USD/{currency}"] = data["rates"][currency]
                rates[f"{currency}/USD"] = 1 / data["rates"][currency]

        rates["THB/USD"] = 1 / rates.get("USD/THB", 35.0)  # THB per USD
        rates["timestamp"] = data.get("time_last_updated", int(time.time()))

        logger.info(f"Fetched exchange rates: {len(rates)} currencies")
        return rates
    except Exception as e:
        logger.error(f"Exchange rate API failed: {e}")
        return {}


def get_thai_bank_rate() -> dict:
    """
    ดึงอัตราซื้อขายเงินบาทจาก bank-of-thailand หรือทดสอบ alternative
    ถ้าไม่ได้จะ fallback ไปใช้ API ข้างบน
    """
    try:
        # Bank of Thailand API
        url = "https://www.bot.or.th/English/STATISTICS/ECONOMICANDFINANCIAL/DataAndChart/CashFlow/Daily/_download.html?download=ERAll"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            logger.info("Got THB rate from Bank of Thailand")
            # Parse CSV/text response...
    except Exception as e:
        logger.warning(f"Bank of Thailand API failed: {e}")

    return {}


def scrape_google_finance() -> dict:
    """
    Scrape อัตราแลกเปลี่ยนจาก Google Finance
    Fallback ถ้า API ไม่ได้
    """
    symbols = {
        "THB=X": "USD/THB",
        "THBUSD=X": "THB/USD",
        "EURTHB=X": "EUR/THB",
        "JPYTHB=X": "JPY/THB",
    }

    rates = {}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    for symbol, name in symbols.items():
        try:
            url = f"https://www.google.com/finance/quote/{symbol}"
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                # Simple extraction from text
                import re
                match = re.search(r'(\d+\.\d+)\s*THB', resp.text)
                if match:
                    rate = float(match.group(1))
                    rates[name] = rate
                    logger.info(f"Scraped {name}: {rate}")
        except Exception as e:
            logger.warning(f"Google Finance {symbol} failed: {e}")
        time.sleep(1)  # Be polite

    return rates


def save_exchange_rates(rates: dict, source: str = "exchangerate-api"):
    """บันทึกอัตราแลกเปลี่ยนลง SQLite"""
    if not rates or "timestamp" in rates:
        return

    today = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        for pair, rate in rates.items():
            if pair == "timestamp" or "/" not in pair:
                continue
            base, quote = pair.split("/")
            try:
                conn.execute("""
                    INSERT OR REPLACE INTO exchange_rates
                    (date, base_currency, quote_currency, rate, source)
                    VALUES (?, ?, ?, ?, ?)
                """, (today, base, quote, rate, source))
            except Exception as e:
                logger.error(f"DB insert error: {e}")
        conn.commit()
    logger.info(f"Saved {len(rates)-1} exchange rates to DB")


# ── Crypto Prices in THB ────────────────────────────────────
def get_crypto_prices() -> dict:
    """
    ดึงราคา Crypto เป็น USD แล้วคำนวณเป็น THB
    ใช้ CoinGecko API (ฟรี, 10-30 calls/min)
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,solana",
            "vs_currencies": "usd,thb",
            "include_market_cap": "true",
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        result = {}
        for coin, info in data.items():
            result[coin.upper()] = {
                "price_usd": info.get("usd", 0),
                "price_thb": info.get("thb", 0),
                "market_cap": info.get("usd_market_cap", 0),
            }

        logger.info(f"Fetched crypto prices: {list(result.keys())}")
        return result
    except Exception as e:
        logger.error(f"CoinGecko API failed: {e}")
        return {}


def save_crypto_prices(crypto_prices: dict, source: str = "coingecko"):
    """บันทึกราคา Crypto ลง SQLite"""
    if not crypto_prices:
        return

    today = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        for symbol, info in crypto_prices.items():
            try:
                conn.execute("""
                    INSERT OR REPLACE INTO crypto_prices
                    (date, symbol, price_usd, price_thb, market_cap, source)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    today,
                    symbol,
                    info["price_usd"],
                    info.get("price_thb", 0),
                    info.get("market_cap", 0),
                    source,
                ))
            except Exception as e:
                logger.error(f"DB insert crypto error: {e}")
        conn.commit()
    logger.info(f"Saved crypto prices for {len(crypto_prices)} coins")


# ── Get Latest Rates (สำหรับให้ API endpoint เรียก) ───────
def get_latest_rates() -> dict:
    """ดึงอัตราแลกเปลี่ยนล่าสุดจาก DB"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT base_currency, quote_currency, rate, date
            FROM exchange_rates
            WHERE date = (SELECT MAX(date) FROM exchange_rates)
            ORDER BY base_currency, quote_currency
        """)
        rows = cursor.fetchall()

    result = {}
    for row in rows:
        key = f"{row['base_currency']}/{row['quote_currency']}"
        result[key] = row["rate"]

    return result


def get_latest_crypto() -> dict:
    """ดึงราคา Crypto ล่าสุดจาก DB"""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT symbol, price_usd, price_thb, market_cap, date
            FROM crypto_prices
            WHERE date = (SELECT MAX(date) FROM crypto_prices)
            ORDER BY symbol
        """)
        rows = cursor.fetchall()

    result = {}
    for row in rows:
        result[row["symbol"]] = {
            "price_usd": row["price_usd"],
            "price_thb": row["price_thb"],
            "market_cap": row["market_cap"],
        }

    return result


def convert_to_thb(amount_usd: float, rate: float = None) -> float:
    """แปลง USD เป็น THB"""
    if rate is None:
        rates = get_latest_rates()
        rate = rates.get("USD/THB", 35.0)  # Default fallback
    return amount_usd * rate


# ── Main: Scrape + Save ─────────────────────────────────────
def run_scrape():
    """รวบรวมทั้งหมดแล้วบันทึก"""
    logger.info("=" * 50)
    logger.info(f"Starting exchange rate scrape at {datetime.now()}")
    logger.info("=" * 50)

    # ตรวจสอบ/สร้าง DB
    init_db()

    # ดึงอัตราแลกเปลี่ยน
    rates = get_exchange_rate_api()
    if rates:
        save_exchange_rates(rates)
    else:
        # Fallback: scrape from Google Finance
        logger.info("Trying Google Finance fallback...")
        rates = scrape_google_finance()
        if rates:
            rates["timestamp"] = int(time.time())
            save_exchange_rates(rates, source="google-finance")

    # ดึงราคา Crypto
    crypto = get_crypto_prices()
    if crypto:
        save_crypto_prices(crypto)

    # แสดงผลล่าสุด
    latest = get_latest_rates()
    latest_crypto = get_latest_crypto()
    logger.info(f"Latest rates: {latest}")
    logger.info(f"Latest crypto: {latest_crypto}")

    return {
        "rates": latest,
        "crypto": latest_crypto,
        "scrape_time": datetime.now().isoformat(),
    }


# ── CLI ─────────────────────────────────────────────────────
if __name__ == "__main__":
    result = run_scrape()
    print(json.dumps(result, indent=2, default=str))
