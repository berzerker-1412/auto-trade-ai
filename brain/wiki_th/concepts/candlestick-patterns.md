# Candlestick Patterns (แท่งเทียน)

## สรุปสั้นๆ

แท่งเทียนเป็นสัญญาณ price action พื้นฐานที่สุด บอกการต่อสู้ระหว่างฝ่ายซื้อและฝ่ายขายในหนึ่งช่วงเวลา ตัวแท่ง (body) แสดง Open→Close และไส้เทียน (wick) แสดง High→Low

**หลักการสำคัญ:** สัญญาณจาก pattern มีความหมายต่อเมื่ออยู่ใน context ที่ถูกต้อง — ตำแหน่งใน trend สำคัญพอๆ กับรูปแบบตัวมันเอง

## สิ่งที่น่าสนใจ

### Single Candlestick Patterns

**Doji (โดจิ)**
- Open ≈ Close (ตัวแท่งเล็กมาก)
- 3 ประเภท: Gravestone (ไส้บนยาว), Dragonfly (ไส้ล่างยาว), Long-legged (ไส้ทั้งสองยาว)
- **สัญญาณ:** ความลังเลในตลาด — ต้องรอยืนยันจากแท่งถัดไป
- ที่แนวต้าน (top) → เบรกขึ้น, ที่แนวรับ (bottom) → เบรกลง

**Hammer (ค้อน)**
- ไส้ล่าง ≥ 2× ตัวแท่ง และตัวแท่งอยู่ครึ่งบน
- **ต้องอยู่หลัง downtrend**
- **สัญญาณ:** การกลับตัวขึ้น — ฝ่ายซื้อปฏิเสธราคาต่ำ

**Shooting Star**
- ไส้บน ≥ 2× ตัวแท่ง ตัวแท่งอยู่ครึ่งล่าง
- **ต้องอยู่หลัง uptrend**
- **สัญญาณ:** การกลับตัวลง — ฝ่ายขายปฏิเสธราคาสูง

**Spinning Top**
- ตัวแท่งเล็ก ไส้ยาวทั้งสองด้าน
- **สัญญาณ:** ความไม่แน่ใจสูง — รอแท่งถัดไป

**Marubozu**
- ไม่มีไส้ (หรือเล็กมาก)
- Bullish: Open=High, Close=Low → ฝ่ายซื้อควบคุมเต็มที่
- Bearish: Open=Low, Close=High → ฝ่ายขายควบคุมเต็มที่

### Multi-Candlestick Patterns

**Engulfing Pattern**
- แท่งที่ 2 ครอบ body ของแท่งที่ 1 ทั้งหมด
- Bullish: แท่ง 1 เป็นสีแดง, แท่ง 2 เป็นสีเขียว + body ใหญ่กว่า
- **สำคัญ:** volume แท่ง 2 ต้องมากกว่าแท่ง 1

**Morning Star / Evening Star**
- 3 แท่ง: แท่งใหญ่ต่อเนื่อง → แท่งเล็ก (doji/spinning top) → แท่งใหญ่กลับทิศ
- สัญญาณการกลับตัวที่แรงกว่า engulfing

**Three White Soldiers / Three Black Crows**
- 3 แท่งติดต่อกัน แต่ละแท่งปิดสูง/ต่ำกว่า body แท่งก่อน
- สัญญาณต่อเนื่อง trend ที่แรงที่สุด

**Tweezer Top / Bottom**
- 2 แท่งมี High/Low เท่ากัน (ดูที่ไส้)
- ยืนยันการกลับตัว — ฝ่ายซื้อ/ขายทดสอบราคาเดิมสองครั้ง

## เชื่อมกับอะไร

- [[chart-patterns]] — pattern หลายแท่งในระดับโครงสร้างสูงกว่า
- [[technical-indicators]] — RSI/Stochastic วัด overbought/oversolid ช่วยยืนยันสัญญาณ
- [[risk-management]] — stop-loss วางใต้ hammer low สำหรับ long

## คำถามที่ยังค้าง

- ควรให้ weight กับ pattern เท่าไหร่เมื่อเทียบกับ indicator signals?
- multi-timeframe confirmation ควรใช้อย่างไรกับ candlestick patterns?
