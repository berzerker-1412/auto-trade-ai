# MyMoney — Services & Screens

## สรุปสั้นๆ

Services คือ business logic ทั้งหมดของแอป มี 5 ตัวหลัก: DatabaseService (SQLite), OcrService (อ่าน slip), PredictionService (AI หมวดหมู่), GoogleSheetsService (sync), NotificationService (bank noti)

---

## สิ่งที่น่าสนใจ / จุดสำคัญ

### DatabaseService — แกนกลาง

SQLite singleton — ทุก provider ใช้ตัวเดียวกัน

Tables: `categories`, `transactions`, `accounts_receivable`, `ar_payments`, `debts`, `subscriptions`

Methods หลัก: `getTransactions(dateRange)`, `getMonthSummary()`, CRUD ทุก entity

### OcrService — อ่าน slip อัตโนมัติ

ใช้ **Google ML Kit** (on-device, ไม่ต้องส่ง internet)

**Parse logic:**
- Amount: จับ `฿` + comma format เช่น `1,500.00`
- Date: DD/MM/YYYY หรือ เดือนไทย + ปีพ.ศ. แล้วแปลงเป็น CE อัตโนมัติ
- Bank name: match กับ list ธนาคารไทย
- Recipient/Sender

Output → SlipData → สร้าง AppTransaction pre-filled ให้ user confirm

### PredictionService — AI แบบ rule-based scoring

ไม่ใช่ ML จริงๆ แต่ scoring แบบ weighted rules ที่ใช้ได้จริง:

| Condition | Score |
| --- | --- |
| keyword match ใน title/note | +10 |
| เวลา 7–9, 12–14, 18–20 | → boost หมวดอาหาร |
| เวลา 22–2 | → boost หมวดบันเทิง |
| amount < 100 | → food/transport |
| amount 500–3,000 | → shopping |
| amount > 5,000 | → housing/insurance |

Filter by transaction type (income/expense) ก่อน แล้วเลือก category ที่ score สูงสุด

ความฉลาดจริงๆ อยู่ที่ keywords ที่ user define per category — ยิ่ง train ดี ยิ่ง predict แม่น

### GoogleSheetsService — sync ไป Sheets

Auth: OAuth 2.0 via google_sign_in

Auto-create 2 tabs:
- `Transaction List` — transactions ทั้งหมด
- `Monthly Summary` — summary รายเดือน

Methods: signIn, signOut, trySilentSignIn, createSpreadsheet, syncTransactions

ไม่ใช่ real-time sync — user กด manual sync หรือตั้ง auto

### NotificationService — จับ bank notification

**EventChannel:** `com.berzerker.mymoney/bank_notifications` (Android เท่านั้น)

Flow:
```
notification จากแอปธนาคาร
  → EventChannel (native Android)
  → parse ยอดเงิน + ธนาคาร
  → TransactionProvider
  → auto-create transaction
```

**Reminders:** schedule alert 7 วันก่อน billing subscription

ทดสอบด้วย Bank Noti Tester แยกต่างหาก — ส่ง notification จำลองได้โดยไม่ต้องโอนเงินจริง

### PermissionService — จัดการ runtime permissions

- Camera — สำหรับ slip scanner
- Storage — export/import file
- Notifications — bank noti + subscription reminder

### Screens ทั้งหมด

| Screen | ทำอะไร |
| --- | --- |
| Home | Dashboard: month summary, recent transactions, alerts |
| Transactions | Full list, add/edit/delete, filter, search |
| Statistics | Pie chart (by category), bar chart (daily/monthly) |
| Slip Scanner | OCR scan → pre-fill transaction form |
| Accounts Receivable | ลูกหนี้, partial payment, overdue alerts |
| Debts | บัตรเครดิต/กู้, utilization rate, due date countdown |
| Subscriptions | Monthly cost total, billing calendar, reminder toggle |
| Categories | จัดการ predefined + custom categories |
| Settings | Theme, Google Sheets connect, notification prefs, export |

---

## เชื่อมกับอะไร

- [MyMoney Architecture](mymoney-architecture.md) — layered design
- [MyMoney Data Models](mymoney-data-models.md) — entity ทั้งหมด
- [MyMoney](mymoney.md) — overview
- Bank Noti Tester — dev tool คู่กัน

---

## คำถามที่ยังค้างอยู่

- OcrService ใช้ Google ML Kit on-device — accuracy บน handwriting หรือ thermal slip แย่ลงไหม?
- NotificationService รองรับแค่ Android — iOS notification permission ทำงานต่างกัน คิดจะรองรับไหม?
- PredictionService ยังเป็น rule-based — ถ้าจะอัปเกรดเป็น on-device ML (TensorFlow Lite) ต้อง collect training data ยังไง?
