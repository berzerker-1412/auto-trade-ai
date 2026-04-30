# MyMoney — Architecture

## สรุปสั้นๆ

MyMoney ใช้ clean 4-layer architecture แบบ classic — UI → State → Business Logic → Data ไม่มี circular dependency สะอาดมาก state ทำด้วย Provider pattern (ChangeNotifier) แยก 6 domain

---

## สิ่งที่น่าสนใจ / จุดสำคัญ

### 4 Layers ชัดเจน

```
Screens (UI)
    ↓
Providers (State — ChangeNotifier)
    ↓
Services (Business Logic)
    ↓
Models + SQLite (Data)
```

กฎเดียว: แต่ละ layer depend ได้แค่ layer ข้างล่าง ห้ามข้ามขั้น ห้าม circular

### Directory Layout

```
lib/
├── core/        — constants, themes, formatters (Thai date/currency)
├── models/      — data classes + SQLite serialization
├── providers/   — 6 ChangeNotifier state domains
├── services/    — database, OCR, prediction, Google Sheets, notifications
└── screens/     — UI organized by feature
```

### 6 Providers — แต่ละตัวดูแล 1 domain

| Provider | ดูแลอะไร |
| --- | --- |
| TransactionProvider | list transaction, monthly summary (income/expense/balance), auto-detect flag |
| CategoryProvider | category list, keyword matching สำหรับ AI predict |
| DebtProvider | หนี้ทั้งหมด, filter "due soon", utilization rate |
| SubscriptionProvider | subscription list, monthly cost รวม, next billing date |
| AccountReceivableProvider | ลูกหนี้, detect overdue, partial payment |
| SettingsProvider | theme, Google Sheet ID, toggle sync/notification (SharedPreferences) |

**Pattern ทุก provider เหมือนกัน:**
1. `init()` — โหลดจาก SQLite ตอน bootstrap
2. `notifyListeners()` — trigger UI rebuild เมื่อข้อมูลเปลี่ยน

### App Bootstrap Flow

```
main()
  → initialize DatabaseService (SQLite)
  → initialize NotificationService (EventChannel)
  → MultiProvider wrap (6 providers)
  → each provider.init() โหลดจาก SQLite
  → MaterialApp render
```

ลำดับสำคัญ — DatabaseService ต้อง ready ก่อน provider ทุกตัว init

---

## เชื่อมกับอะไร

- [MyMoney Data Models](mymoney-data-models.md) — structure ของแต่ละ model
- [MyMoney Services](mymoney-services.md) — business logic แต่ละ service
- [MyMoney](mymoney.md) — overview ภาพรวมทั้งแอป

---

## คำถามที่ยังค้างอยู่

- ถ้าต้องเพิ่ม feature ใหม่ที่ต้องการ provider ใหม่ — pattern ไหนดีสุด? แยก provider ใหม่หรือ extend ของเดิม?
- SettingsProvider ใช้ SharedPreferences ไม่ใช่ SQLite — มี edge case ไหมที่ settings หายตอน SQLite migrate?
