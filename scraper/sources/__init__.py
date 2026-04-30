"""
scraper/sources/__init__.py — ตัวดึงข่าวจากแหล่งข่าวต่างๆ
"""
from .reuters import ReutersScraper
from .bloomberg import BloombergScraper
from .bbc import BBCScraper
from .cnbc import CnbcScraper
from .yahoo_finance import YahooFinanceScraper
from .thai_rath import ThaiRathScraper

# เรียงตามความสำคัญ: financial news ก่อน, general news หลัง
ALL_SCRAPERS = [
    CnbcScraper,
    YahooFinanceScraper,
    ReutersScraper,
    BBCScraper,
    ThaiRathScraper,
]
