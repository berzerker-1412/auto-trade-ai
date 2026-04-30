---
title: Bank Noti Tester
type: project
tags: [flutter, dart, mobile, testing, notifications, mymoney]
created: 2026-04-12
updated: 2026-04-13
---

Flutter utility app for simulating bank notifications to test [[mymoney/index|MyMoney]]. Not an end-user app.

**Source:** `/Users/chinnawat/projects/bank_noti_tester`

---

## Purpose

Used during MyMoney development to:

- Send simulated notifications formatted like real Thai bank messages
- Test the `NotificationService` logic in MyMoney that parses notification → transaction
- Test edge cases without waiting for real bank notifications

---

## Tech Stack

- Flutter / Dart 3.11.4+
- `flutter_local_notifications` v18.0.0 — sends system notifications
- Material Design 3

---

## Architecture

Small codebase — all logic lives in a single file:

```text
lib/
└── main.dart  (284 lines — UI + notification logic)
```

**How it works:**

1. `_initNotifications()` — creates Android notification channel `bank_test_channel` (high importance/priority)
2. `sendNotification()` — dispatches notification to the system
3. MyMoney receives it via EventChannel `com.berzerker.mymoney/bank_notifications` and parses it into a transaction

---

## Features

### Template Notifications

6 preset templates simulating real Thai banks:

| Bank | Direction |
| --- | --- |
| SCB | Incoming / Outgoing |
| KBank | Incoming / Outgoing |
| KTB | Outgoing |
| BBL | Outgoing |

Each template includes full data: amount, recipient/sender, Thai-language message format matching real SMS.

### Custom Notification Builder

Freely enter any title and body — for testing edge cases or formats not covered by templates.

---

## Integration Pipeline with MyMoney

```text
Bank Noti Tester
    ↓ sends system notification (bank_test_channel)
Android OS
    ↓ forwards to EventChannel
MyMoney: NotificationService
    ↓ parses title/body
MyMoney: TransactionProvider
    ↓ auto-creates transaction
SQLite (mymoney DB)
```
