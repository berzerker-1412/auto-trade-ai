# Technical Indicators (ตัวชี้วัดทางเทคนิค)

## สรุปสั้นๆ

Technical indicators คือการ transform ทางคณิตศาสตร์ของ price, volume, หรือ open interest มี 3 จุดประสงค์: **ยืนยัน trend**, **ระบุ overbought/oversold**, และ **วัด volatility**

**หลักการสำคัญ:** ไม่มี indicator �ตัวเดียวเพียงพอ ใช้ 2-3 ตัวที่เสริมกันจากหมวดต่างๆ

## สิ่งที่น่าสนใจ

### Trend Indicators

**Moving Averages**
- SMA: ค่าเฉลี่ยธรรมดา (laggy)
- EMA: ให้น้ำหนักกับราคาล่าสุดมากกว่า (responsive)
- **Crossover signals:** SMA 50 > SMA 200 = Golden Cross (bullish), กลับกัน = Death Cross (bearish)

**MACD**
- `MACD = EMA(12) - EMA(26)`, Signal = EMA(9) ของ MACD
- Crossover + histogram ขยาย = สัญญาณแรง
- **Divergence:** ราคาสูงใหม่แต่ MACD ไม่สูง → เตือน reversal

**ADX**
- วัด **trend strength** ไม่ใช่ direction
- ADX < 20 = ranging (อย่าใช้ trend indicators)
- ADX > 25 = trending

### Momentum Oscillators

**RSI**
- `RSI = 100 - (100 / (1 + RS))`
- Overbought > 70, Oversold < 30
- **Divergence คือสัญญาณที่แรงที่สุด:** ราคาต่ำสุดต่ำกว่า แต่ RSI สูงสุดต่ำสูงกว่า → กลับขึ้น

**Stochastic**
- `%K = (Close - Lowest Low) / (Highest High - Lowest Low) × 100`
- Overbought > 80, Oversold < 20
- %K cross above %D in oversold zone → buy signal

### Volatility Indicators

**Bollinger Bands**
- `Middle = SMA(20)`, `Upper = Middle + 2×StdDev`, `Lower = Middle - 2×StdDev`
- Band squeeze = volatility ต่ำสุด → breakout จะมา
- Price touches upper band = overextended, touches lower = oversold

**ATR**
- วัดค่าเฉลี่ยของ True Range
- **ใช้หลักๆ:** ตั้ง stop-loss distance ที่ปรับตัวตาม volatility
- `Stop = 1.5 × ATR(14)` สำหรับตลาด volatile, `0.5 × ATR(14)` สำหรับ quiet

### Volume Indicators

**OBV**
- บวก volume เมื่อราคาขึ้น, ลบเมื่อลง
- OBV divergence จากราคา = เตือน reversal

**VWAP**
- ราคาเฉลี่ยถ่วงน้ำหนักด้วย volume
- สถาบันใช้เป็น reference: ราคาสูงกว่า VWAP = buy bias

### การเลือก Indicators

| เป้าหมาย | Indicators |
|----------|-----------|
| หา trend direction | SMA 50/200, EMA 21, ADX |
| จังหวะ entry | RSI, Stochastic, MACD crossover |
| ตั้ง stop-loss | ATR, Bollinger lower |
| ยืนยัน breakout | Volume, OBV |
| วัด volatility | ATR, Bollinger width |

## เชื่อมกับอะไร

- [[candlestick-patterns]] — pattern signals ช่วยยืนยัน indicator readings
- [[chart-patterns]] — patterns ระดับโครงสร้าง, indicators ระดับคณิตศาสตร์
- [[risk-management]] — ATR ใช้ sizing stop-loss; volatility ใช้ position sizing
- [[ai-ml-trading]] — indicator values เป็น features หลักสำหรับ ML models

## คำถามที่ยังค้าง

- threshold ของแต่ละ indicator ควรปรับตาม asset หรือไม่?
- จะ combine หลาย indicators อย่างไรให้ไม่เกิด analysis paralysis?
