---
title: MyMoney — Services & Screens
type: project
tags: [flutter, sqlite, ocr, google-sheets, notifications]
created: 2026-04-12
updated: 2026-04-13
---

See overview at [[mymoney/index|MyMoney]].

---

## Services

### DatabaseService

SQLite singleton for app-wide persistence.

- **Tables:** `categories`, `transactions`, `accounts_receivable`, `ar_payments`, `debts`, `subscriptions`
- **Primary keys:** UUID (TEXT)
- **Booleans:** INTEGER (0/1)
- **Dates:** ISO 8601 string
- **Methods:** `getTransactions(dateRange)`, `getMonthSummary()`, CRUD for every entity

---

### OcrService

Reads Thai bank slips using Google ML Kit.

**Input:** image from camera or gallery (quality 90%)

**Parse logic:**

- Amount: recognizes `฿`, comma format e.g. `1,500.00`
- Date: DD/MM/YYYY or Thai month + Buddhist Era year (converted to CE)
- Bank name: matched against Thai bank list
- Recipient/sender

**Output:** `SlipData` object → forwarded to create an AppTransaction

---

### PredictionService

AI categorization — automatic category prediction.

**Algorithm (scoring):**

| Condition | Score |
| --- | --- |
| keyword match in title/note | +10 |
| meal hours (7–9, 12–14, 18–20) | → food boost |
| late night (22–2) | → entertainment boost |
| amount < 100 | → food/transport |
| amount 500–3,000 | → shopping |
| amount > 5,000 | → housing/insurance |

Returns the category ID with the highest score, filtered by transaction type first.

---

### GoogleSheetsService

Syncs data to Google Sheets.

- **Auth:** OAuth 2.0 via google_sign_in
- **Sheets:** auto-creates 2 tabs
  - `Transaction List` — all transactions
  - `Monthly Summary` — monthly summary
- **Methods:** `signIn`, `signOut`, `trySilentSignIn`, `createSpreadsheet`, `syncTransactions`

---

### NotificationService

Receives bank notifications from native Android and dispatches reminders.

- **EventChannel:** `com.berzerker.mymoney/bank_notifications`
- **Flow:** native notification → EventChannel → parse → TransactionProvider → auto-create transaction
- **Reminders:** schedule subscription alert 7 days before billing
- **Permission:** requests `POST_NOTIFICATIONS` (Android 13+)

Tested with [[bank-noti-tester/index|Bank Noti Tester]].

---

### PermissionService

Manages runtime permissions:

- Camera — for slip scanner
- Storage — export/import files
- Notifications — bank notifications + reminders

---

## Screens

| Screen | Purpose |
| --- | --- |
| Home | Dashboard: month summary, recent transactions, alerts |
| Transactions | Full list, add/edit/delete, filter, search |
| Statistics | Pie chart (by category), bar chart (daily/monthly) |
| Slip Scanner | OCR scan slip → pre-fill transaction form |
| Accounts Receivable | Debtors, partial payment recording, overdue alerts |
| Debts | Credit cards/loans, utilization rate, due date countdown |
| Subscriptions | Recurring cost total, billing calendar, reminder toggle |
| Categories | Manage predefined + custom categories |
| Settings | Theme toggle, Google Sheets connect, notification prefs, export |
