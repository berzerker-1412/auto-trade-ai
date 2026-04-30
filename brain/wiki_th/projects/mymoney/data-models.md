# MyMoney — Data Models

## สรุปสั้นๆ

Models ทั้งหมดใช้ UUID (TEXT) เป็น PK และ serialize ผ่าน `toMap()`/`fromMap()` สำหรับ SQLite มี 5 entities หลัก + 1 nested (ARPayment)

---

## สิ่งที่น่าสนใจ / จุดสำคัญ

### AppTransaction — รายรับรายจ่าย

Field หลัก: amount, type (income/expense), categoryId, title, note, date, bankName

Field พิเศษที่บอก source:
- `fromSlip = 1` — สร้างจาก OCR scan slip
- `isAutoDetected = 1` — สร้างจาก bank notification อัตโนมัติ

### AppCategory — หมวดหมู่

Field พิเศษ: `keywords` — comma-separated string ใช้ match กับ title/note สำหรับ AI predict

`isCustom = 0` คือ predefined, `1` คือ user สร้างเอง

### Debt — หนี้ (บัตรเครดิต/กู้ยืม)

Type: creditCard / loan / other

Computed fields ที่น่าสนใจ:
- `utilizationRate` = currentBalance / creditLimit (ถ้าเกิน 30% เริ่มกระทบ credit score)
- `availableCredit` = creditLimit - currentBalance
- `nextDueDate` — คำนวณจาก dueDateDay

### Subscription — subscription รายคาบ

Type: monthly / yearly / weekly

Computed fields:
- `monthlyAmount` — normalize yearly → monthly (ยอดรายเดือนเทียบได้)
- `nextBillingDate` — คำนวณจาก billingCycle + billingDay
- `daysUntilBilling` — เตือนล่วงหน้า

**Presets มา 15 ตัวพร้อมใช้:** Netflix, Spotify, YouTube Premium, Apple Music, Disney+, HBO Max, Amazon Prime, iCloud, Google One, LINE TV, True ID, AIS Play ฯลฯ

### AccountReceivable — เงินที่ให้คนอื่นยืม

Status: pending / partiallyPaid / paid / overdue

**Nested ARPayment** — เก็บ record การจ่ายแต่ละครั้ง (partial payment)

Computed: remainingAmount, isOverdue (เทียบ date ปัจจุบัน), computedStatus (derive อัตโนมัติจาก payment state)

### Pattern รวม

- ทุก model ใช้ UUID แทน integer auto-increment — ป้องกัน collision ตอน merge data จากหลาย device
- Boolean เก็บเป็น INTEGER 0/1 ใน SQLite
- Date เก็บเป็น ISO 8601 string

---

## เชื่อมกับอะไร

- [MyMoney Architecture](mymoney-architecture.md) — 4-layer design
- [MyMoney Services](mymoney-services.md) — DatabaseService จัดการ CRUD ทั้งหมด
- [MyMoney](mymoney.md) — overview

---

## คำถามที่ยังค้างอยู่

- UUID ดีกว่า integer PK สำหรับ sync — แต่ SQLite query UUID string ช้ากว่า integer ไหมในทางปฏิบัติ?
- AccountReceivable.computedStatus derive อัตโนมัติ — ถ้ามี partial payment แล้ว manually set status ได้ไหม หรือ always override?
