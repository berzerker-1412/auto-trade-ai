"""
scraper/ai_scraper.py — AI-powered scraper with self-healing selectors
ใช้ AI วิเคราะห์โครงสร้างเว็บ + health check ตัวตรวจสอบว่า selector ยังใช้ได้
"""
import logging
import time
import re
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# MiniMax client path
MINIMAX_PATH = "/Users/chinnawat/auto-trade-ai/backend/ai"


@dataclass
class SelectorResult:
    """ผลลัพธ์จาก AI ที่บอกว่าจะ extract จาก selector ไหน"""
    title_selector: str = "h1"
    title_attr: str = "text"  # "text" | "href" | "datetime"
    body_selector: str = "article"
    body_text_filter: str = "p"  # "p" | "div" | "*"
    published_selector: str = "time"
    published_attr: str = "datetime"
    site_name: str = ""
    notes: str = ""


@dataclass
class HealthCheckResult:
    """ผลตรวจ health check ของ scraper"""
    ok: bool
    url: str = ""
    title_found: bool = False
    body_found: bool = False
    body_length: int = 0
    error: str = ""
    checked_at: datetime = field(default_factory=datetime.now)


class AIAwareScraper:
    """
    Scraper ที่ใช้ AI วิเคราะห์โครงสร้างเว็บ
    มี health check + self-healing ถ้า selector เสีย
    """

    def __init__(self, url: str, source_name: str = ""):
        self.url = url
        self.source_name = source_name
        self.selectors: Optional[SelectorResult] = None
        self._html_cache: Optional[str] = None
        self._soup_cache: Optional[BeautifulSoup] = None

    # ─── MiniMax AI ────────────────────────────────────────────────

    def _call_ai(self, prompt: str, timeout: int = 30) -> str:
        """เรียก MiniMax AI สำหรับวิเคราะห์ HTML"""
        import subprocess
        import json as _json

        prompt_truncated = prompt[:4000]
        messages_arg = _json.dumps([{"role": "user", "content": prompt_truncated}])

        cmd = f"""python3 -c '
import os
from dotenv import load_dotenv
load_dotenv(os.path.expanduser("~/.hermes/.env"), override=False)

import sys
sys.path.insert(0, "{MINIMAX_PATH}")
from minimax_client import MiniMaxChatClient

client = MiniMaxChatClient()
messages = {messages_arg}
resp = client.create(messages)
content = resp.get("choices", [{{}}])[0].get("message", {{}}).get("content", "")
print(content, end="")
'"""

        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd="/Users/chinnawat/auto-trade-ai",
        )
        if result.returncode != 0:
            logger.error(f"[AI] MiniMax call failed: {result.stderr[:200]}")
            return ""
        return result.stdout.strip()

    # ─── Selector Discovery ────────────────────────────────────────

    def analyze_structure(self, html: str) -> SelectorResult:
        """
        ใช้ AI วิเคราะห์ HTML structure แล้วบอกว่าจะ extract จากไหน
        """
        prompt = f"""คุณคือ web scraping expert วิเคราะห์ HTML ของหน้าเว็บนี้แล้วตอบเป็น selector ที่ถูกต้อง

หน้าเว็บ: {self.url}

ดูโครงสร้าง HTML แล้วบอก:
1. selector สำหรับ title ของ article (h1 หรือ class อื่น)
2. selector สำหรับ body ของ article (ส่วนเนื้อหาหลัก)
3. selector สำหรับ published date (ถ้ามี)
4. ชื่อเว็บไซต์

ตอบเป็น JSON ที่มี format:
{{
  "title_selector": "h1.article-title",
  "body_selector": "article .body",
  "published_selector": "time",
  "site_name": "BBC News",
  "notes": "ใช้ data-testid attribute สำหรับ title"
}}

สำคัญ: ตอบเป็น JSON อย่างเดียว ไม่ต้องอธิบายเพิ่ม

--- HTML ส่วนต้นของหน้า (ไม่เกิน 8000 ตัวอักษร) ---
{html[:8000]}
"""
        response = self._call_ai(prompt)
        return self._parse_selector_response(response)

    def _parse_selector_response(self, response: str) -> SelectorResult:
        """แปลง JSON response จาก AI เป็น SelectorResult"""
        import json

        # หา JSON ใน response
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if not match:
            # Fallback: ใช้ default selectors
            return SelectorResult(
                title_selector="h1",
                body_selector="article",
                site_name=self.source_name,
                notes="Fallback — AI response parse failed",
            )

        try:
            data = json.loads(match.group())
            return SelectorResult(
                title_selector=data.get("title_selector", "h1"),
                title_attr=data.get("title_attr", "text"),
                body_selector=data.get("body_selector", "article"),
                body_text_filter=data.get("body_text_filter", "p"),
                published_selector=data.get("published_selector", "time"),
                published_attr=data.get("published_attr", "datetime"),
                site_name=data.get("site_name", self.source_name),
                notes=data.get("notes", ""),
            )
        except json.JSONDecodeError:
            return SelectorResult(
                title_selector="h1",
                body_selector="article",
                site_name=self.source_name,
                notes=f"Fallback — JSON parse failed: {response[:100]}",
            )

    # ─── HTML Fetch ────────────────────────────────────────────────

    def fetch(self, use_cache: bool = True) -> str:
        """ดึง HTML ของหน้าเว็บ"""
        if use_cache and self._html_cache:
            return self._html_cache

        import requests
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml",
        }
        resp = requests.get(self.url, headers=headers, timeout=15)
        resp.raise_for_status()
        self._html_cache = resp.text
        # invalidate soup cache when HTML changes
        self._soup_cache = None
        return self._html_cache

    def get_soup(self, html: str = "") -> BeautifulSoup:
        """Parse HTML เป็น BeautifulSoup"""
        if not html:
            html = self.fetch()
        if self._soup_cache is None:
            self._soup_cache = BeautifulSoup(html, "lxml")
        return self._soup_cache

    # ─── Health Check ──────────────────────────────────────────────

    def health_check(self, selectors: SelectorResult = None) -> HealthCheckResult:
        """
        ตรวจสอบว่า selectors ยังทำงานได้ปกติไหม
        ถ้า body สั้นผิดปกติ หรือไม่เจอ title → แจ้งว่ามีปัญหา
        """
        if selectors is None:
            selectors = self.selectors

        result = HealthCheckResult(ok=False, url=self.url)

        try:
            html = self.fetch()
            soup = self.get_soup(html)

            # Check title
            title_elem = soup.select_one(selectors.title_selector)
            result.title_found = title_elem is not None

            # Check body
            body_elem = soup.select_one(selectors.body_selector)
            if body_elem:
                # นับ text length
                text = body_elem.get_text(separator=" ", strip=True)
                result.body_length = len(text)
                result.body_found = len(text) > 100
            else:
                result.body_found = False
                result.error = f"Body selector '{selectors.body_selector}' ไม่เจอ element"

            result.ok = result.title_found and result.body_found

            # ถ้า body สั้นผิดปกติ
            if result.body_found and result.body_length < 100:
                result.ok = False
                result.error = f"Body content สั้นผิดปกติ ({result.body_length} chars)"

        except Exception as e:
            result.ok = False
            result.error = str(e)

        return result

    # ─── AI Self-Healing ──────────────────────────────────────────

    def diagnose_and_fix(self) -> SelectorResult:
        """
        เมื่อ health check ล้มเหลว → ใช้ AI วิเคราะห์ใหม่
        """
        logger.warning(f"[{self.source_name}] Health check failed — re-analyzing structure")

        html = self.fetch()
        soup = self.get_soup(html)

        # ดึง AI วิเคราะห์โครงสร้างใหม่
        new_selectors = self.analyze_structure(html)
        self.selectors = new_selectors

        # ตรวจสอบว่า selectors ใหม่ทำงานได้จริง
        check = self.health_check(new_selectors)
        if not check.ok:
            logger.warning(
                f"[{self.source_name}] AI-proposed selectors still failing: {check.error}"
            )
            # ลอง fallback selectors ที่เป็น universal
            fallback = self._get_universal_fallback_selectors()
            check2 = self.health_check(fallback)
            if check2.ok:
                new_selectors = fallback
                new_selectors.notes = "Universal fallback — AI selectors failed"
                logger.info(f"[{self.source_name}] Using universal fallback selectors")

        return new_selectors

    def _get_universal_fallback_selectors(self) -> SelectorResult:
        """Universal selectors ที่ใช้ได้กับหลายเว็บ"""
        return SelectorResult(
            title_selector="h1",
            body_selector="article, [role='main'], main, .article-body, .post-content",
            published_selector="time",
            site_name=self.source_name,
            notes="Universal fallback selectors",
        )

    # ─── Extract ─────────────────────────────────────────────────

    def extract(self, selectors: SelectorResult = None) -> Dict[str, Any]:
        """
        Extract article data ด้วย selectors
        ถ้า selectors ไม่ผ่าน health check → ลอง diagnose_and_fix ก่อน
        """
        if selectors is None:
            selectors = self.selectors

        if selectors is None:
            # ครั้งแรก → วิเคราะห์ด้วย AI
            html = self.fetch()
            selectors = self.analyze_structure(html)
            self.selectors = selectors

        # Health check
        check = self.health_check(selectors)
        if not check.ok:
            logger.warning(
                f"[{self.source_name}] Selector issue: {check.error} — running AI diagnosis"
            )
            selectors = self.diagnose_and_fix()

        soup = self.get_soup()

        # Extract title
        title_elem = soup.select_one(selectors.title_selector)
        title = title_elem.get_text(strip=True) if title_elem else ""

        # Extract published
        published_at = None
        time_elem = soup.select_one(selectors.published_selector)
        if time_elem:
            dt = time_elem.get(selectors.published_attr) or time_elem.get_text(strip=True)
            try:
                from dateutil.parser import parse
                published_at = parse(dt)
            except Exception:
                pass

        # Extract body
        body_elem = soup.select_one(selectors.body_selector)
        if body_elem:
            if selectors.body_text_filter == "p":
                paras = body_elem.select("p")
            elif selectors.body_text_filter == "div":
                paras = body_elem.select("div")
            else:
                paras = body_elem.find_all(string=True)

            content_parts = []
            for p in paras:
                text = p.get_text(strip=True) if hasattr(p, "get_text") else str(p).strip()
                if text and len(text) > 30:
                    content_parts.append(text)
            content = "\n\n".join(content_parts)
        else:
            content = ""

        # Extract summary (first 3 paragraphs)
        summary = ""
        if content:
            paras = content.split("\n\n")[:3]
            summary = " ".join(paras)
            if len(summary) > 300:
                summary = summary[:300] + "..."

        return {
            "title": title,
            "url": self.url,
            "source": selectors.site_name or self.source_name,
            "published_at": published_at.isoformat() if published_at else None,
            "summary": summary,
            "content": content,
            "content_length": len(content),
            "selectors_used": {
                "title": selectors.title_selector,
                "body": selectors.body_selector,
                "published": selectors.published_selector,
            },
            "ai_notes": selectors.notes,
            "health_ok": check.ok,
            "extracted_at": datetime.now().isoformat(),
        }


# ─── Health Monitor ──────────────────────────────────────────────

class HealthMonitor:
    """
    ตรวจสอบ health ของ scrapers ทั้งหมดเป็นระยะ
    ถ้าเจอปัญหา → แจ้งและ re-analyze อัตโนมัติ
    """

    def __init__(self):
        self.domain_cache: Dict[str, AIAwareScraper] = {}
        self.last_check: Dict[str, datetime] = {}
        self.check_interval_seconds = 3600  # ทุกชั่วโมง

    def register(self, url: str, source_name: str = "") -> AIAwareScraper:
        """Register scraper URL"""
        domain = self._extract_domain(url)
        if domain not in self.domain_cache:
            scraper = AIAwareScraper(url, source_name)
            self.domain_cache[domain] = scraper
        return self.domain_cache[domain]

    def check_all(self, force: bool = False) -> Dict[str, HealthCheckResult]:
        """ตรวจสอบ health ของทุก registered scraper"""
        results = {}
        now = datetime.now()

        for domain, scraper in self.domain_cache.items():
            # Rate limit: ตรวจได้ทุก check_interval_seconds
            last = self.last_check.get(domain)
            if not force and last and (now - last).total_seconds() < self.check_interval_seconds:
                continue

            check = scraper.health_check()
            results[domain] = check
            self.last_check[domain] = now

            if not check.ok:
                logger.warning(
                    f"[HealthMonitor] {domain} failing: {check.error} — triggering self-heal"
                )
                # Self-heal
                new_selectors = scraper.diagnose_and_fix()
                check2 = scraper.health_check(new_selectors)
                results[domain] = check2
                self.last_check[domain] = now

        return results

    def _extract_domain(self, url: str) -> str:
        import re
        m = re.match(r"https?://([^/]+)", url)
        return m.group(1) if m else url


# Singleton health monitor
_monitor = HealthMonitor()


def get_monitor() -> HealthMonitor:
    return _monitor
