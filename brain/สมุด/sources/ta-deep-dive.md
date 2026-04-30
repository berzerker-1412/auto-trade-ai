# Technical Analysis Deep Dive — สรุปความรู้

## ที่มา

`docs/technical-analysis-deep-dive.md` — คู่มือ TA ภาษาไทย 2,612 บรรทัด เขียนโดย Claude วิจัยจากหลายแหล่ง
Source page: [[../wiki/sources/ta-deep-dive]]

## สรุปสาระสำคัญ

### สิ่งที่ wow — ไฮไลท์จากการวิจัย

1. **ดอจิต้องยืนยัน** — ดอจิเป็นแค่เครื่องบอกว่าตลาดลังเล แต่ต้องรอแท่งถัดไปถึงรู้ทิศ
2. **Hammer + Engulfing = เซ็ตอัพแข็ง** — ถ้าเจอ Hammer ในโซนรองรับ แล้วตามด้วย Engulfing ขึ้น = สัญญาณซื้อที่ดี
3. **Wyckoff อธิบาย "เงินฉลาด"** — เรื่อง Accumulation/Distribution ช่วยให้เข้าใจว่าทำไมราคาถึงพักตัวก่อนขึ้น
4. **ADX < 20 = อย่าใช้ Trend indicator** — ปัญหาที่เทรดเดอร์มือใหม่ชอบเจอ: ใช้ MA crossover ตอนตลาด sideways = แพ้ทุกที
5. **หลักการเดียวกันใช้ได้ทั้ง Crypto และ Gold** — ทั้งสองเป็น volatile assets ที่ TA ทำงานได้ดี

### สิ่งที่น่าสนใจ

- **แท่งเทียน 23+ แบบ** พร้อมสูตรจำ — จำแค่ 5-6 แบบหลักก็เพียงพอแล้ว
- **รูปแบบกราฟ** มันเยอะมาก แต่จริงๆแล้วมีแค่ 2 กลุ่ม: Reversal กับ Continuation
- **Bollinger Band squeeze** บอกว่า volatility กำลังจะ burst — ใช้จังหวะได้ดีกับ breakout trading
- **ไม่มี indicator ตัวไหนเพียงพอ** — ต้องใช้หลายตัวคู่กัน

## เชื่อมกับอะไร

- **auto-trade-ai** — signal_generator.py ใช้หลักจาก TA ทั้งหมดนี้
- **การลงทุนจริง** — บทความนี้ช่วยให้เข้าใจว่าทำไมราคาถึงขึ้น/ลง
- **AI/ML** — features สำหรับ ML model มาจาก indicators ในบทความนี้ทั้งนั้น

## คำถามที่ยังค้าง

- จะเอาทฤษฎี Elliot Wave ไปใช้ใน auto-trade-ai ยังไง? (มัน subjective เกินไปสำหรับ systematic trading)
- LSTM สำหรับ predict price direction — ใช้ indicators อะไรเป็น features ดีที่สุด?
- Wyckoff volume analysis — มี library สำหรับ detect accumulation/distribution หรือต้องเขียนเอง?
