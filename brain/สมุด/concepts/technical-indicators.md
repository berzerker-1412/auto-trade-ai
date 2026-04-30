# Technical Indicators — ตัวชี้วัดทางเทคนิค

## สรุปสั้นๆ

Indicators = คณิตศาสตร์ที่ใส่ราคา/volume เพื่อให้เห็น pattern ชัดขึ้น
แบ่งเป็น 4 กลุ่ม: Trend, Momentum, Volatility, Volume

**หลัก:** ใช้ 2-3 ตัวจากคนละกลุ่ม อย่างเดียวไม่พอ

## สิ่งที่ wow

### RSI — ของง่ายแต่ทรงพลัง
- >70 = overbought (อาจลง)
- <30 = oversold (อายขึ้น)
- **Divergence สำคัญที่สุด:** ราคาขึ้นต่อแต่ RSI ไม่ขึ้น = เตือนกลับ

### MACD — trend + momentum
- MACD > Signal = bullish
- Histogram ใหญ่ขึ้น = momentum แข็งขึ้น
- Divergence = warning sign

### Bollinger Bands — บอก volatility
- แถบแคบ = volatility ต่ำ → breakout จะมา
- ราคาแตะแถบบน = overbought, แตะแถบล่าง = oversold

### ADX — บอกว่ามี trend ไหม
- <20 = ranging (อย่าใช้ trend indicators)
- >25 = trending (ใช้ trend-following strategies)

## ตัวที่ใช้ในโปรเจกต์

`signal_generator.py` ใช้ RSI, MACD, Bollinger Bands สำหรับสัญญาณ

## Python code สำคัญ

มีใน [[../wiki/concepts/technical-indicators]] พร้อม code ครบ

## จำง่ายๆ

```
Trend:     MA, MACD, ADX     → บอกทิศ
Momentum:  RSI, Stochastic   → บอกแรง
Volatility: Bollinger, ATR   → บอนกว้างแค่ไหน
Volume:    OBV, VWAP         → บอกว่ามีคนเข้าออกเท่าไหร่
```

## เชื่อมกับ

- [[candlestick-patterns]] — indicators ยืนยันสัญญาณจาก candlestick
- [[chart-patterns]] — indicators ช่วย validate breakout
- [[risk-management]] — ATR ใช้ตั้ง stop-loss
- [[ai-ml-trading]] — indicator values เป็น features สำหรับ ML model
