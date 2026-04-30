# Trading Strategies (กลยุทธ์การเทรด)

## สรุปสั้นๆ

Trading strategy กำหนดกฎสำหรับ *เมื่อไหร่เข้า* และ *เมื่อไหร่ออก* จาก position ไม่มี strategy ไหนใช้ได้ใTất cả market conditions — สำคัญคือ match strategy กับ market regime

**กรอบหลัก:** Trend-following strategies เด่นใน trending markets; mean-reversion strategies เด่นใน ranging markets

## สิ่งที่น่าสนใจ

### 1. Trend Following (ดักเทรนด์)

**ปรัชญา:** "The trend is your friend" — เข้าเมื่อ trend ชัด, ออกเมื่อกลับทิศ

**Entry rules (MA Crossover):**
```
SMA 50 > SMA 200 → Golden Cross → BUY
SMA 50 < SMA 200 → Death Cross → SELL
```

**Stop-loss:** ใต้ swing low ล่าสุด หรือ `Entry - 2 × ATR(14)`

**จุดแข็ง:** จับ big moves ได้; ง่ายต่อการ sistematize
**จุดอ่อน:** Entry ช้า (confirm หลัง trend เริ่ม); เสียบ่อยใน choppy markets

### 2. Breakout Trading (เทรดสิ่งที่ตูม)

**ปรัชญา:** เทรดเมื่อราคาทะลุ consolidation range ด้วย force

**Entry rules:**
1. ระบุ consolidation: ราคาอยู่ใน range ≥ 5 แท่ง
2. รอ breakout: ปิดเหนือ resistance ด้วย volume > 1.5× average
3. Entry: เล็กน้อยเหนือจุด breakout (หลีกเลี่ยง false breakout)
4. Stop-loss: ใต้จุด breakout หรือใต้ range low

**จุดแข็ง:** จับ big moves แต่ early; มี risk ชัดเจน
**จุดอ่อน:** False breakouts บ่อย (ถึง 50%); ต้องมีวินัยตัดขาดทุน

### 3. Mean Reversion (กลับไปกลับมา)

**ปรัชญา:** "สิ่งที่ขึ้นไปสูงเกินไปต้องลงมา" — ราคาผันผวนรอบ fair value

**Entry rules (Bollinger Bands):**
```
RSI < 30 หรือ ราคาแตะ lower BB → BUY (oversold bounce)
RSI > 70 หรือ ราคาแตะ upper BB → SELL (overbought)
```

**VWAP rules:**
```
ราคา < VWAP มาก → BUY (สถาบันซื้อถูก)
ราคา > VWAP มาก → SELL
```

**จุดแข็ง:** Signals บ่อย; ดีใน ranging markets
**จุดอ่อน:** ใน strong trends, ราคา "walk the bands" ได้นาน → large losses

### 4. Multi-Timeframe Analysis (หลายกรอบเวลา)

**ปรัชญา:** timeframe สูงกว่าสำหรับ *what* (ทิศทาง), timeframe ต่ำกว่าสำหรับ *when* (จังหวะ entry)

**ขั้นตอน:**
```
1. Daily: ระบุ primary trend (SMA direction, ADX level)
2. 4H: หา key support/resistance, รอ pattern
3. 1H: entry timing แม่นยำด้วย indicators
```

**ตัวอย่าง:**
```
Daily: Uptrend (SMA 50 > 200, ADX > 25)
  ↓
4H: Pullback to support zone, สร้าง hammer
  ↓
1H: RSI oversold (<30), MACD bullish crossover
  ↓
Entry: BUY at 1H close above hammer high
Stop: Below 4H swing low
```

### 5. Paradox / Contrarian (เทรดสวนทาง)

**ปรัชญา:** "กลัวเมื่อคนอื่นโลภ, โลภเมื่อคนอื่นกลัว" — Warren Buffett

**Eldar's paradox principle:** ซื้อเมื่อมีเลือดในถนน (fear สุดขั้ว), ขายเมื่อ euphoria สุดขั้ว

**Tools:** Fear & Greed Index, RSI extreme zones, sentiment surveys, options flow

**จุดแข็ง:** Reward-to-risk สูงที่สุดเมื่อถูก
**จุดอ่อน:** Extremes ยืดเยื้อได้นานกว่าที่คาด; ต้องมี conviction ถือ

### Strategy Selection by Market Regime

| Market Regime | Strategy ที่ดีที่สุด | Indicators |
|---------------|---------------------|------------|
| Strong trend | Trend Following | ADX > 40, SMA crossover |
| Weak trend | Breakout | ADX 20-30, volume |
| Ranging/Choppy | Mean Reversion | RSI extremes, Bollinger |
| Extreme fear | Contrarian | Fear & Greed < 25 |
| Extreme euphoria | Contrarian | Fear & Greed > 75 |

## เชื่อมกับอะไร

- [[candlestick-patterns]] — entry signals จาก price action
- [[chart-patterns]] — breakout levels จาก structural analysis
- [[technical-indicators]] — RSI, ADX, Bollinger สำหรับ signal generation
- [[risk-management]] — position sizing, stop-loss, reward-to-risk
- [[market-theories]] — Wyckoff accumulation/distribution phases ช่วย detect regime

## คำถามที่ยังค้าง

- auto-trade-ai ควรใช้ strategy ไหนเป็นหลัก หรือใช้ทุกอันแล้วรวม confidence score?
- จะ detect market regime แบบ automatic ได้อย่างไร?
