# Chart Patterns (รูปแบบกราฟ)

## สรุปสั้นๆ

Chart patterns คือรูปแบบที่เกิดจาก price action ข้ามหลายช่วงเวลา ต่างจาก single candlestick เพราะ encode พลวัต supply/demand เชิงโครงสร้าง แบ่งเป็น **reversal** (กลับทิศ) และ **continuation** (พักตัวก่อนไปต่อ)

**กฎทอง:** Breakout ต้องเกิดขึ้นด้วย volume สูงกว่าค่าเฉลี่ยถึงจะ valid

## สิ่งที่น่าสนใจ

### Reversal Patterns

**Head and Shoulders (H&S)**
- โครงสร้าง: ไหล่ซ้าย → หัว (สูงสุด) → ไหล่ขวา (ต่ำกว่าหัว) → neckline
- **สัญญาณ:** ราคาลงต่ำกว่า neckline → bearish reversal
- **เป้าหมาย:** `Target = 2 × Neckline − Head`
- Inverse H&S = mirror image → bullish reversal

**Double Top / Double Bottom**
- ยอด/đáy สองครั้งที่ระดับใกล้เคียงกัน (±5%)
- Volume ของยอด/đáy ครั้งที่สองควรต่ำกว่าครั้งแรก
- **เป้าหมาย:** คำนวณจากระยะห่างระหว่างยอด/đáyกับ neckline

**Triple Top / Triple Bottom**
- พยายามทดสอบ 3 ครั้งที่ระดับเดิม → สัญญาณแรงกว่า double

**Rounding Bottom (Saucer)**
- เปลี่ยนจากแรงขายเป็นแรงซื้ออย่างค่อยเป็นค่อยไป
- Volume ลดลงที่đáy เพิ่มขึ้นด้านขวา
- **เหมาะกับ weekly/monthly charts**

### Continuation Patterns

**Triangles**
- **Ascending:** แนวต้านแบน + แนวรับขาขึ้น → bullish bias
- **Descending:** แนวรับแบน + แนวต้านลง → bearish bias
- **Symmetric:** ทั้งสองด้านเข้าหากัน → neutral (รอ breakout บอกทิศ)

**Flags และ Pennants**
- เกิดหลัง move แรง (pole) → พักตัวสั้นๆ → มัก continue
- Flag: slope ตรงข้าม trend
- Pennant: converging lines
- **สำคัญ:** consolidation ควร shallow (flag at < 38.2% retracement ของ pole)

**Wedges**
- คล้าย triangle แต่ขอบทั้งสอง slope ไปทางเดียวกัน
- Rising Wedge → bearish (แรงซื้ออ่อน)
- Falling Wedge → bullish (แรงขายอ่อน)

**Rectangles**
- Sideways consolidation ระหว่าง support/resistance แนวนอน
- แทนการต่อสู้ระหว่าง buyers/sellers ที่ equilibrium
- Breakout มัก continue prior trend

### การวัดเป้าหมาย

```
Measured Move = Reference Point ± Pattern Height
```

| Pattern | Reference Point | Direction |
|---------|---------------|-----------|
| H&S | Neckline | ลงจาก neckline |
| Double Top | Neckline | ลงจาก neckline |
| Ascending Triangle | Resistance (breakout) | ขึ้นตามความสูง |
| Flag/Pennant | Start of pole | ต่อทิศ pole |

## เชื่อมกับอะไร

- [[candlestick-patterns]] — signals ที่ละเอียดกว่า
- [[technical-indicators]] — volume indicators (OBV) ช่วยยืนยัน breakout
- [[risk-management]] — stop-loss ใต้ neckline สำหรับ reversal trades
- [[trading-strategies]] — breakout trading ใช้ chart patterns เป็น signals

## คำถามที่ยังค้าง

- ทำ automated detection ของ chart patterns ยากกว่า candlesticks มาก — ควรใช้ approach ไหน?
- จะ combine chart patterns กับ ML ได้อย่างไรสำหรับ auto-trade-ai?
