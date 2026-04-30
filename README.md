# Auto Trade AI

AI-driven Auto Trade & Paper Trade System สำหรับ Crypto และ Gold — ครบวงจรการลงทุน

## Features

### Trading Modes
- **Auto Trade**: ระบบเทรดอัตโนมัติด้วย AI
- **Paper Trade**: ทดลองเทรดโดยไม่ใช้เงินจริง พร้อมระบบติดตามผล

### Asset Classes
- **Crypto**: Bitcoin, Ethereum และคริปโตอื่นๆ ผ่าน CCXT
- **Gold**: ราคาทองคำและการเทรดทอง

### Core Features
- ระบบเข้า/ออกออร์เดอร์ชัดเจน (Entry/Exit tracking)
- ติดตามผลกำไร/ขาดทุน (P&L tracking)
- รายงานสรุปผลการเทรด
- AI-driven signal generation

## Project Structure

```
auto-trade-ai/
├── CLAUDE.md          ← schema & workflows (read every session)
├── README.md          ← this file
├── skills/            → ~/.hermes/skills/ (symlink)
│
├── backend/           ← trading system source code
│   ├── ai/            # AI signal generation (GPT-4o)
│   ├── core/          # models, paper_trader, trade_logger
│   ├── crypto/        # CCXT Binance integration
│   └── gold/          # XAUUSD price feed
│
├── brain/             ← second brain (Obsidian vault)
│   ├── wiki/          ← English knowledge base
│   └── wiki_th/       ← Thai notes
│
├── frontend/          ← Next.js dashboard
├── api/               ← API server
├── config/            ← settings.yaml
├── data/              ← trading data & logs
├── docs/              ← documentation
├── scraper/           ← web scraper
└── tests/             ← unit tests
```

## Installation

```bash
git clone https://github.com/berzerker-1412/auto-trade-ai.git
cd auto-trade-ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

```yaml
# config/settings.yaml
exchange:
  name: binance
  api_key: YOUR_API_KEY
  api_secret: YOUR_API_SECRET
  testnet: true  # Paper trade mode

paper_trade:
  enabled: true
  initial_balance: 100000  # THB or USD

crypto:
  symbols:
    - BTC/USDT
    - ETH/USDT
  trading_pair: USDT

gold:
  source: alpha_vantage
  symbol: XAUUSD

ai:
  model: gpt-4
  confidence_threshold: 0.75
```

## Usage

```bash
# Paper trade mode (recommended for start)
python -m backend.core.paper_trader --mode paper --asset crypto

# Auto trade mode
python -m backend.core.auto_trader --mode live --asset crypto

# View P&L
python -m backend.core.report --show-pnl
```

## Tech Stack

- **Python 3.10+** — backend
- **CCXT** — crypto exchange connection
- **LangChain/OpenAI** — AI signal generation
- **Pandas** — data analysis
- **SQLite** — trade logging
- **Next.js** — frontend dashboard

## Brain / Knowledge Base

The project includes a **second brain** for knowledge management. See `CLAUDE.md` at project root for how it works.

```bash
# Open brain as Obsidian vault
obsidian "/Users/chinnawat/auto-trade-ai/brain"
```

---

**⚠️ Disclaimer**: ระบบนี้เป็นเครื่องมือช่วยเทรด ผู้ใช้ต้องศึกษาและเข้าใจความเสี่ยงก่อนใช้งาน ผู้ใช้รับผิดชอบต่อการซื้อขายของตัวเอง
