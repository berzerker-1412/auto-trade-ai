"""
scraper/sentiment.py — Sentiment Analysis สำหรับข่าวการเงิน
ใช้ lexicon-based approach ออกแบบมาสำหรับข่าวการเงินโดยเฉพาะ
"""
from typing import Dict, List, Tuple
import re


# ── Lexicon สำหรับข่าวการเงิน/สงคราม ────────────────────────────

HIGH_IMPACT_PAIRS = {
    # คริปโตเฉพาะ
    ("bitcoin", "etf"): 0.8, ("bitcoin", "approval"): 0.9, ("bitcoin", "spot"): 0.9,
    ("sec", "bitcoin"): 0.8, ("binance", " lawsuit"): -0.8, ("coinbase", "sec"): -0.7,
    ("crypto", "regulation"): -0.5, ("fed", "rate"): -0.4, ("federal", "reserve"): -0.3,
    ("rate", "hike"): -0.6, ("rate", "cut"): 0.6, ("inflation", "hot"): -0.7,
    ("inflation", "cool"): 0.5, ("cpi", "higher"): -0.6, ("cpi", "lower"): 0.5,
    ("treasury", "yield"): -0.4, ("dollar", "strong"): -0.5, ("dollar", "weak"): 0.5,
    ("china", "economy"): -0.4, ("china", "stimulus"): 0.6,
    ("spot", "etf"): 0.8, ("institutional", "buy"): 0.7,
    # ทองเฉพาะ
    ("gold", "record"): 0.8, ("gold", "high"): 0.7, ("gold", "surge"): 0.7,
    ("xauusd", "high"): 0.7, ("safe haven",): 0.6, ("central bank", "gold"): 0.7,
    ("geopolitical", "risk"): 0.5, ("tension", "middle east"): -0.5,
    ("oil", "spike"): -0.4, ("energy", "crisis"): -0.4,
}

POSITIVE_WORDS = {
    # การเงิน/ตลาด
    "bullish": 0.6, "rally": 0.5, "surge": 0.6, "soar": 0.7, "jump": 0.4,
    "gain": 0.4, "rise": 0.4, "climb": 0.4, "advance": 0.4, "growth": 0.5,
    "profit": 0.5, "profitability": 0.5, "beat": 0.4, "exceed": 0.4,
    "optimism": 0.5, "recovery": 0.5, "recover": 0.5, "rebound": 0.5,
    "upgrade": 0.4, "upbeat": 0.5, "strong": 0.3, "strength": 0.3,
    "breakthrough": 0.5, "boom": 0.6, "boom": 0.6, "historic": 0.4,
    "record high": 0.7, "all-time high": 0.7, "peak": 0.5,
    "positive": 0.4, "improving": 0.4, "expansion": 0.5,
    "investor confidence": 0.5, " inflows": 0.4, "bull run": 0.6,

    # สงคราม/การเมือง (negative สำหรับ risk)
    "ceasefire": 0.6, "peace": 0.7, "talks": 0.2, "diplomacy": 0.4,
    "agreement": 0.3, "deal": 0.3, "truce": 0.5,

    # คริปโต
    "bull market": 0.7, "accumulation": 0.4, "hodl": 0.3, "uptrend": 0.5,
    "all-time high": 0.7, "new high": 0.6, "moon": 0.7, "pump": 0.5,
}

NEGATIVE_WORDS = {
    # การเงิน/ตลาด
    "bearish": -0.6, "crash": -0.8, "plunge": -0.7, "tumble": -0.6,
    "slump": -0.6, "drop": -0.4, "fall": -0.4, "decline": -0.4,
    "loss": -0.5, "losses": -0.5, "miss": -0.4, "missed": -0.4,
    "downgrade": -0.5, "pessimism": -0.5, "recession": -0.7,
    "recession fears": -0.7, "contraction": -0.5, "slowdown": -0.5,
    "weak": -0.3, "weakness": -0.4, "crisis": -0.7, "crash": -0.8,
    "bailout": -0.6, "default": -0.8, "bankruptcy": -0.8,
    "bubble": -0.4, "burst": -0.5, "collapse": -0.8,
    "selloff": -0.6, " outflows": -0.5, "liquidation": -0.7,
    "bank run": -0.8, " contagion": -0.7, "crackdown": -0.5,

    # สงคราม/ความขัดแย้ง
    "war": -0.8, "invasion": -0.9, "attack": -0.7, "conflict": -0.7,
    "military": -0.4, "missile": -0.5, "bomb": -0.7, "terror": -0.8,
    "sanctions": -0.4, "escalation": -0.7, "escalate": -0.7,
    "casualties": -0.7, "death": -0.7, "killed": -0.7, "wounded": -0.6,
    "occupation": -0.7, "atrocity": -0.9, "massacre": -0.9,
    "nuclear threat": -0.9, "terrorism": -0.9, "hostage": -0.7,

    # คริปโต
    "bear market": -0.7, "dump": -0.6, "crash": -0.8, "liquidation": -0.7,
    "hack": -0.7, "scam": -0.8, "rug pull": -0.8, "depeg": -0.7,
    " FTX": -0.8, "bankruptcy": -0.7, "all-time low": -0.7,
    "new low": -0.6, "capitulation": -0.7, "death cross": -0.6,
}

NEUTRAL_WORDS = {
    "unchanged": 0.0, "stable": 0.0, "steady": 0.0, "flat": 0.0,
    "unchanged": 0.0, "hold": 0.0, "maintain": 0.0, "monitor": 0.0,
    "wait": 0.0, "uncertain": 0.0, "uncertainty": -0.1,
}


def analyze_sentiment(text: str) -> Tuple[float, List[str]]:
    """
    วิเคราะห์ sentiment ของข้อความข่าว

    Returns:
        (score, keywords) — score -1.0 ถึง 1.0, keywords ที่เจอ
    """
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)

    score = 0.0
    matches = []

    # 1. Check high-impact keyword pairs ก่อน (ให้ weight สูงสุด)
    for kw_pair, weight in HIGH_IMPACT_PAIRS.items():
        kw1, kw2 = kw_pair if len(kw_pair) == 2 else (kw_pair[0], None)
        if kw1 in text_lower and (kw2 is None or kw2 in text_lower):
            score += weight
            matches.append(f"pair:{kw1}")

    # 2. Single-word scoring
    for word in words:
        if word in POSITIVE_WORDS:
            score += POSITIVE_WORDS[word]
            matches.append(f"+{word}")
        elif word in NEGATIVE_WORDS:
            score += NEGATIVE_WORDS[word]
            matches.append(f"-{word}")

    # Normalize: หารด้วย sqrt(word_count) แทน — รักษา sentiment strength ไว้
    # แต่ละ keyword มี weight สูงอยู่แล้ว (0.3-0.9) ไม่ต้องลดทอนมาก
    # Amp factor 3 เพื่อให้คะแนนจริงอยู่ในช่วง -1 ถึง 1
    score = max(-1.0, min(1.0, score / max(1, len(words) ** 0.5) * 3))

    return score, matches


# แหล่งข่าวที่เป็นการเงิน/ตลาด (ใช้สำหรับ sentiment)
FINANCIAL_SOURCES = {"Reuters", "Bloomberg", "BBC", "CNBC", "Investing.com", "CoinDesk", "The Block", "CoinTelegraph"}

# แหล่งข่าวไทย (ไม่ใช้สำหรับ sentiment เพราะ lexicon เป็น English)
THAI_SOURCES = {"Thairath", "Naewna", "Matichon", "Bangkok Post", "The Nation", "Thai News"}


def get_trade_signal(articles: List[Dict]) -> Dict:
    """
    สร้าง trade signal จากข่าวทั้งหมดที่เก็บมา

    Logic:
    - Filter ข่าวที่มี |sentiment| < 0.05 ออก (noisy general news)
    - ถ้า sentiment เฉลี่ย > 0.15 = BUY bias
    - ถ้า sentiment เฉลี่ย < -0.15 = SELL bias
    - ถ้าเป็นข่าว war ที่กระทบ XAUUSD → พิจารณา long gold
    - ถ้าเป็นข่าว crypto ที่ positive → long crypto
    - ถ้าเป็นข่าว rate hike → กระทบ USD
    """
    if not articles:
        return {
            "bias": "neutral",
            "score": 0.0,
            "signal": None,
            "reason": "No news available",
            "impacted_assets": [],
            "risk_level": "low",
        }

    # Filter: เอาเฉพาะข่าวจาก financial sources ก่อน (ถ้ามี)
    financial_articles = [a for a in articles if a.get("source", "") in FINANCIAL_SOURCES]
    if financial_articles:
        use_articles = financial_articles
    else:
        # ไม่มี financial news → ใช้ทั้งหมดแต่ต้องมี sentiment ที่ดี
        use_articles = articles

    # Filter ข่าวที่ไม่มี sentiment ชัดเจน (|score| < 0.05 = noise)
    signal_articles = [a for a in use_articles if abs(a.get("sentiment_score", 0)) >= 0.05]

    # ถ้าข่าวที่มี signal มีน้อยกว่า 30% ของทั้งหมด → ใช้ทั้งหมดแต่ลด threshold
    use_articles = signal_articles if len(signal_articles) >= len(use_articles) * 0.3 else use_articles
    if not use_articles:
        use_articles = articles

    total_sentiment = sum(a.get("sentiment_score", 0) for a in use_articles)
    avg_sentiment = total_sentiment / len(use_articles)

    # ถ้าข่าวส่วนใหญ่เป็น high-impact ให้เพิ่ม weighting
    high_impact_count = sum(1 for a in use_articles if abs(a.get("sentiment_score", 0)) >= 0.3)
    if high_impact_count > 0:
        # Weighted average: ให้ high-impact มี influence มากขึ้น
        weighted_sum = sum(a.get("sentiment_score", 0) * (1 if abs(a.get("sentiment_score", 0)) < 0.3 else 2) for a in use_articles)
        total_weight = len(use_articles) + high_impact_count
        avg_sentiment = weighted_sum / total_weight

    # นับข่าวตาม category
    category_count: Dict[str, int] = {}
    asset_impact: Dict[str, List[float]] = {}

    for article in use_articles:
        cat = article.get("category", "general")
        category_count[cat] = category_count.get(cat, 0) + 1

        for tag in article.get("impact_tags", []):
            if tag not in asset_impact:
                asset_impact[tag] = []
            asset_impact[tag].append(article.get("sentiment_score", 0))

    # หา asset ที่กระทบมากที่สุด
    asset_scores = {
        asset: sum(scores) / len(scores)
        for asset, scores in asset_impact.items()
        if scores
    }

    # ระดับความเสี่ยง
    war_count = category_count.get("war", 0)
    high_impact_news_count = sum(1 for a in use_articles if abs(a.get("sentiment_score", 0)) >= 0.4)
    if war_count >= 3 or high_impact_news_count >= 5:
        risk_level = "high"
    elif war_count >= 1 or high_impact_news_count >= 2:
        risk_level = "medium"
    else:
        risk_level = "low"

    # ตัดสินใจ — threshold ลดลงเป็น ±0.10 (paper trade: ต้องการ signal บ่อยขึ้น)
    if avg_sentiment > 0.10:
        bias = "bullish"
        top_assets = sorted(asset_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        signal = {
            "direction": "buy",
            "top_assets": [a[0] for a in top_assets],
            "confidence": min(abs(avg_sentiment) * 3.0, 1.0),
        }
        reason = f"Positive sentiment ({avg_sentiment:.2f}) from {len(use_articles)} articles"
    elif avg_sentiment < -0.10:
        bias = "bearish"
        top_assets = sorted(asset_scores.items(), key=lambda x: x[1])[:3]
        signal = {
            "direction": "sell",
            "top_assets": [a[0] for a in top_assets],
            "confidence": min(abs(avg_sentiment) * 3.0, 1.0),
        }
        reason = f"Negative sentiment ({avg_sentiment:.2f}) from {len(use_articles)} articles"
    else:
        bias = "neutral"
        signal = None
        reason = f"Neutral sentiment ({avg_sentiment:.2f})"

    # War news เพิ่ม risk-off signal สำหรับ gold
    if war_count >= 2:
        if "XAUUSD" in asset_scores or "GOLD" in asset_scores:
            signal = signal or {"direction": "buy", "top_assets": ["XAUUSD"], "confidence": 0.5}
            signal["reason"] = f"War news ({war_count} articles) → Safe haven demand for gold"
            signal["top_assets"] = ["XAUUSD"] + (signal.get("top_assets") or [])

    return {
        "bias": bias,
        "score": round(avg_sentiment, 3),
        "signal": signal,
        "reason": reason,
        "impacted_assets": list(asset_scores.keys()),
        "asset_sentiments": {k: round(v, 3) for k, v in asset_scores.items()},
        "category_breakdown": category_count,
        "risk_level": risk_level,
        "article_count": len(use_articles),
        "high_impact_count": high_impact_count,
    }
