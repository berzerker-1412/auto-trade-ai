# Market Theories (ทฤษฎีตลาด)

## สรุปสั้นๆ

Market theories ให้กรอบความคิดสำหรับเข้าใจ *ทำไม* ราคาถึงเคลื่อนที่แบบนั้น — ไม่ใช่แค่ pattern ที่จะ trade แต่เป็น underlying dynamics สามกรอบที่ relevant ที่สุดสำหรับ systematic trading: Dow Theory, Elliott Wave, และ Wyckoff

## สิ่งที่น่าสนใจ

### Dow Theory

**Core:** ตลาดมี trend อยู่ 3 ระดับ และยืนยันด้วย volume

**สามระดับของ Trend:**
| ระดับ | คำอธิบาย | ระยะเวลา |
|-------|---------|----------|
| Primary | Major bull/bear cycles | เดือน - ปี |
| Secondary | Corrections 30-70% ของ primary | สัปดาห์ - เดือน |
| Minor | ความผันผวนรายวัน | ชั่วโมง - วัน |

**สามขั้นของ Bull Market:**
1. **Accumulation** — smart money เข้าเงียบๆ
2. **Public Participation** — trend ยืนยัน, momentum สร้าง
3. **Distribution** — smart money ออก, ราคาขึ้นสุดก่อนล่วง

**หลักการ:**
- ราคา discounts ทุกอย่าง (ข้อมูลอยู่ในราคาหมดแล้ว)
- Trend ยังคงอยู่จนกว่าจะมี reversal signal ชัดเจน
- Volume ยืนยัน trend

### Elliott Wave Theory

**Core:** ตลาดเคลื่อนที่เป็น 5-wave impulse ตามด้วย 3-wave correction, fractally ทุก timeframe

**โครงสร้าง:**
```
Impulse (5 waves):
  Wave 1: การผลักแรก
  Wave 2: Pullback (ไม่ลงต่ำกว่าจุดเริ่มต้น wave 1)
  Wave 3: волныสูงสุด (ไม่เคยสั้นที่สุด)
  Wave 4: Pullback (ไม่ overlap wave 1)
  Wave 5: การผลักสุดท้าย

Correction (3 waves):
  Wave A: ขยับสวน trend แรก
  Wave B: การ bounce
  Wave C: ขยับสุดท้ายในทิศ correction
```

**Fibonacci Ratios:**
| Wave Relationship | Ratio |
|------------------|-------|
| Wave 2 retraces Wave 1 | 50-78.6% |
| Wave 3 vs Wave 1 | 161.8% หรือ 261.8% |
| Wave 4 retraces Wave 3 | 23.6-38.2% |

### Wyckoff Method

**Core:** ราคาเคลื่อนที่จาก institutional ("smart money") accumulation และ distribution

**สี่ขั้น:**
```
Phase 1: Accumulation — ซื้อสะสมที่ support
Phase 2: Markup — breakout จาก range, trend เริ่ม
Phase 3: Distribution — ขายให้ public
Phase 4: Markdown — ราคาลง
```

**Spring และ Upthrust:**
- **Spring:** ราคาลงต่ำกว่า support แล้วกลับเร็ว → smart money ดูดซื้อ → markup จะมา
- **Upthrust:** ราคาขึ้นเหนือ resistance แล้วกลับ → smart money เทขาย → markdown จะมา

**เปรียบเทียบเชิงปฏิบัติ:**

| ด้าน | Dow Theory | Elliott Wave | Wyckoff |
|------|-----------|-------------|---------|
| Timeframe | Daily+ | ทุก timeframe | Daily+ |
| Focus | Trend confirmation | Wave counting | Smart money |
| Entry signal | Trend breakout | Wave 3 start | Spring/Upthrust |
| Stop-loss | Below prior low | Below Wave 1/2 | Outside range |
| Complexity | ต่ำ | สูง | กลาง |

## เชื่อมกับอะไร

- [[chart-patterns]] — Wyckoff phases map ไป chart patterns (accumulation → base, markup → breakout)
- [[technical-indicators]] — Volume indicators (OBV) ช่วยระบุ Wyckoff phases
- [[risk-management]] — stop-loss placement consistent ทุกกรอบทฤษฎี
- [[ai-ml-trading]] — institutional flow detection เป็น ML feature

## คำถามที่ยังค้าง

- Wyckoff ดูเหมาะที่สุดสำหรับ auto-trade-ai เพราะใช้ volume data ได้ตรงๆ — จะ automate อย่างไร?
- Elliott wave counting ใช้ในระดับ systematic ได้ไหม หรือต้อง subjective?
