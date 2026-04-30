---
title: MyMoney — Data Models
type: project
tags: [flutter, sqlite, data-model]
created: 2026-04-12
updated: 2026-04-13
---

See overview at [[mymoney/index|MyMoney]].

All models use UUID as primary key (TEXT), serialized with `toMap()`/`fromMap()` for SQLite.

---

## AppTransaction

Income/expense record.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT (UUID) | PK |
| amount | REAL | amount |
| type | TEXT | `income` / `expense` |
| categoryId | TEXT | FK → AppCategory.id |
| title | TEXT | transaction name |
| note | TEXT | notes |
| date | TEXT | ISO 8601 |
| bankName | TEXT | bank name |
| fromSlip | INTEGER | 1 = created from OCR scan |
| isAutoDetected | INTEGER | 1 = created from bank notification |

---

## AppCategory

Transaction category with keywords for AI prediction.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT (UUID) | PK |
| name | TEXT | category name |
| icon | TEXT | emoji or symbol |
| color | INTEGER | ARGB color value |
| type | TEXT | `income` / `expense` |
| keywords | TEXT | comma-separated — matched against title/note |
| isCustom | INTEGER | 0 = predefined, 1 = user-created |

---

## Debt

Liabilities — credit cards, loans.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT (UUID) | PK |
| name | TEXT | card/loan name |
| debtType | TEXT | `creditCard` / `loan` / `other` |
| creditLimit | REAL | total credit limit |
| currentBalance | REAL | outstanding balance |
| minimumPayment | REAL | minimum payment amount |
| statementDay | INTEGER | billing cycle day |
| dueDateDay | INTEGER | payment due day |
| interestRate | REAL | interest rate |
| bankName | TEXT | bank name |
| lastFourDigits | TEXT | last 4 digits |

**Computed fields:**

- `utilizationRate` = currentBalance / creditLimit
- `availableCredit` = creditLimit - currentBalance
- `nextDueDate` — calculated from dueDateDay

---

## Subscription

Recurring subscription entries.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT (UUID) | PK |
| name | TEXT | service name |
| icon | TEXT | emoji |
| amount | REAL | amount per cycle |
| billingCycle | TEXT | `monthly` / `yearly` / `weekly` |
| billingDay | INTEGER | billing day |
| categoryId | TEXT | FK → AppCategory.id |
| isActive | INTEGER | enabled/disabled |
| color | INTEGER | display color |
| startDate | TEXT | start date |

**Computed fields:**

- `monthlyAmount` — normalize yearly → monthly
- `nextBillingDate` — calculated from billingCycle + billingDay
- `daysUntilBilling` — days until next cycle

**Presets included:** Netflix, Spotify, YouTube Premium, Apple Music, Disney+, HBO Max, Amazon Prime, iCloud, Google One, LINE TV, True ID, AIS Play, and others — 15 total.

---

## AccountReceivable

Money lent to others.

| Field | Type | Notes |
| --- | --- | --- |
| id | TEXT (UUID) | PK |
| personName | TEXT | debtor name |
| totalAmount | REAL | total amount lent |
| paidAmount | REAL | amount paid so far |
| dueDate | TEXT | due date |
| status | TEXT | `pending` / `partiallyPaid` / `paid` / `overdue` |
| note | TEXT | notes |

**Nested:** `ARPayment[]` — individual payment records (partial payments).

**Computed fields:**

- `remainingAmount` = totalAmount - paidAmount
- `isOverdue` — compared against current date
- `computedStatus` — derived automatically from payment state
