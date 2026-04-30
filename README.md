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
├── src/
│   ├── core/           # Core trading engine
│   ├── crypto/          # Crypto trading modules (CCXT)
│   ├── gold/            # Gold trading modules
│   └── ai/              # AI signal generation
├── config/              # Configuration files
├── data/                # Trading data & logs
├── tests/                # Unit tests
├── docs/                 # Documentation
├── README.md
├── requirements.txt
└── LICENSE
```

## Installation

```bash
# Clone repository
git clone https://github.com/berzerker-1412/auto-trade-ai.git
cd auto-trade-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

ตั้งค่า API keys และ parameters ใน `config/`:

```yaml
# config/settings.yaml
exchange:
  name: binance
  api_key: YOUR_API_KEY
  api_secret: YOUR_API_SECRET
  testnet: true  # Paper trade mode

paper_trade:
  enabled: true
  initial_balance: 100000  # THB หรือ USD

crypto:
  symbols:
    - BTC/USDT
    - ETH/USDT
  trading_pair: USDT

gold:
  source: alpha_vantage  # หรือ data source อื่น
  symbol: XAUUSD

ai:
  model: gpt-4          # AI model for signals
  confidence_threshold: 0.75
```

## Usage

### Paper Trade Mode (แนะนำเริ่มต้น)

```bash
python -m src.core.paper_trader --mode paper --asset crypto
```

### Auto Trade Mode

```bash
python -m src.core.auto_trader --mode live --asset crypto
```

### ดูผลการเทรด

```bash
python -m src.core.report --show-pnl
```

## Tech Stack

- **Python 3.10+**
- **CCXT**: Crypto exchange connection
- **LangChain/OpenAI**: AI signal generation
- **Pandas**: Data analysis
- **SQLite**: Trade logging

## License

MIT License

---

**⚠️ Disclaimer**: ระบบนี้เป็นเครื่องมือช่วยเทรด ผู้ใช้ต้องศึกษาและเข้าใจความเสี่ยงก่อนใช้งาน ผู้ใช้รับผิดชอบต่อการซื้อขายของตัวเอง
