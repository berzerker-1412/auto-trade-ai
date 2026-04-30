# Candlestick Patterns — แท่งเทียน

## สรุปสั้นๆ

แท่งเทียน = ภาษาของตลาด แต่ละแท่งบอกว่าคนซื้อ vs คนขาย ใครชinsะ ตอนไหน

**หลักการตัวเดียว:** รูปแบบแท่งเทียนต้องดู context — อยู่ตรงไหนของ trend สำคัญกว่าตัวแท่งเอง

## สิ่งที่ wow

- **Doji** — แค่เห็นว่า Open ≈ Close = ตลาดลังเล แต่ต้องรอแท่งถัดไปบอกทาง
- **Hammer** — ไส้ล่างยาวๆ + ตัวแท่งอยู่บน = buyers ปฏิเสธราคาต่ำ มีโอกาสกลับขึ้น (แต่ต้องหลัง downtrend)
- **Engulfing** — แท่ง 2 กลืนแท่ง 1 = สัญญาณกลับตัวที่แรงมาก (ต้องดู volume ด้วย)
- **Marubozu** — ไม่มีไส้เลย = ฝ่ายใดฝ่ายหนึ่งควบคุมตลาดสนิท หาดูยาก

## จำง่ายๆ

```
Single patterns:
  Doji      = ลังเล (ต้องรอ)
  Hammer    = กลับขึ้น (หลังลง)
  Shooting  = กลัวลง (หลังขึ้น)
  Spinning  = งง (ลังเลสูง)
  Marubozu  = กล้า (ฝ่ายใดฝ่ายหนึ่งครอง)

Multi patterns:
  Engulfing = กลืน = reversal แรง
  Morning/Evening Star = ดาว 3 แท่ง = reversal แรงกว่า engulfing
  Three White Soldiers  = ทหารขาว 3 ตัว = trend ต่อเนื่องแรงมาก
```

## ในโปรเจกต์

`signal_generator.py` ตรวจจับ Hammer, Doji, Engulfing patterns เป็นสัญญาณเข้า

## เชื่อมกับ

- [[chart-patterns]] — รูปแบบใหญ่กว่า (หลายแท่งรวมกัน)
- [[technical-indicators]] — RSI ช่วยยืนยัน overbought/oversold
- [[risk-management]] — stop วางใต้ hammer low
