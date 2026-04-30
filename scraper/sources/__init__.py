"""
scraper/sources/__init__.py — ตัวดึงข่าวจากแหล่งข่าวต่างๆ
"""
from .reuters import ReutersScraper
from .bloomberg import BloombergScraper
from .bbc import BBCScraper
from .thai_news import ThaiNewsScraper

ALL_SCRAPERS = [
    ReutersScraper,
    BloombergScraper,
    BBCScraper,
    ThaiNewsScraper,
]
