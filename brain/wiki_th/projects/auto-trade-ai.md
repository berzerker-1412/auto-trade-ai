# auto-trade-ai

## สรุปสั้นๆ
ระบบเทรดอัตโนมัติที่ใช้ AI วิเคราะห์ตลาดแล้วส่งสัญญาณ BUY/SELL เพื่อทำกำไร รองรับ crypto (ผ่าน Binance/CCXT) และทองคำ

**จุดประสงค์: ทำกำไร ไม่ว่าจะด้วยวิธีไหน**

---

## วิธีทำกำไร

```
ข้อมูลตลาด (ราคา, volume, OHLCV)
    ↓
AI Signal Generator (GPT-4o)
  → วิเคราะห์ → ส่งสัญญาณ BUY หรือ SELL
  → confidence >= 0.75 ถึงจะเทรด
    ↓
Paper Trader (ทดลองเทรดก่อน)
  → ถ้าผลดี → Live Trader (เทรดจริง)
    ↓
Risk Management
  → Stop-loss -2%, Take-profit +5%
  → Position size ไม่เกิน 10% ของ balance
    ↓
P&L Tracking
  → ดู win rate, กำไร/ขาดทุน
```

---

## โครงสร้าง codebase

| ไฟล์ | ทำหน้าที่ |
| --- | --- |
| `src/ai/signal_generator.py` | สร้างสัญญาณ BUY/SELL ด้วย GPT-4o |
| `src/crypto/exchange.py` | เชื่อมต่อ exchange ผ่าน CCXT (Binance) |
| `src/gold/price_feed.py` | ดึงราคาทอง (demo หรือ APIจริง) |
| `src/core/paper_trader.py` | จำลองเทรด ไม่ใช้เงินจริง |
| `src/core/trade_logger.py` | เก็บ log ลง SQLite |
| `src/core/models.py` | dataclass: TradeSignal, Trade, TradeResult |
| `config/settings.yaml` | ตั้งค่าทั้งหมด |

---

## Risk Management ที่ใช้

| กฎ | ค่า | หมายเหตุ |
| --- | --- | --- |
| Max position | 10% ของ balance | กระจายความเสี่ยง |
| Stop-loss | -2% | ตัดขาดทุนเร็ว |
| Take-profit | +5% | R:R = 2.5:1 |
| Confidence | ≥ 0.75 | เทรดเฉพาะ signal แข็ง |
| Max concurrent | 3 trades | ไม่เยอะเกินไป |
| Max daily | 5 trades | ป้องกัน overtrade |

---

## สิ่งที่น่าสนใจ

1. **Fallback mode** — ถ้าไม่มี OpenAI ระบบยังทำงานได้ (random signal) แต่ความแม่นยำต่ำ
2. **Paper trade ก่อน** — แนะนำทดลองก่อนใช้เงินจริง
3. **P&L คำนวณทันที** — balance อัปเดตเมื่อ trade ปิด
4. **ไม้ที่เท่าไหร่** — ระบบนับ trade number ต่อ symbol

## คำถามที่ค้าง

- AI prompt ปรับแต่งอย่างไรให้แม่นขึ้น?
- มี backtesting module ไหม?
- ถ้า confidence ต่ำกว่า 0.75 แล้ว market มันชัดมาก ควรทำไง?
- มี trailing stop ไหม?
- จะรับมือกับ news events / black swan ได้ไหม?
