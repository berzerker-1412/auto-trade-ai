---
title: MyMoney
type: project
tags: [flutter, dart, mobile, personal-finance, thai, sqlite, google-sheets, ocr]
created: 2026-04-12
updated: 2026-04-13
---

Personal finance app for Thai users, built with Flutter. Supports iOS and Android. Offline-first with optional Google Sheets sync.

**Source:** `/Users/chinnawat/projects/mymoney`

---

## Purpose

- Record income and expenses with AI-powered automatic category prediction
- Scan bank slips via OCR (Google ML Kit)
- Auto-capture transactions from bank notifications
- Manage subscriptions, debts, and accounts receivable
- Sync data to Google Sheets for further analysis

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Framework | Flutter 3.x / Dart 3.2+ |
| State Management | Provider 6.1.1 (ChangeNotifier) |
| Database | SQLite via sqflite 2.3.2 |
| OCR | google_mlkit_text_recognition 0.13.1 |
| Cloud | Google Sign-In 6.2.1 + googleapis 13.2.0 |
| Charts | fl_chart 0.68.0 |
| Notifications | flutter_local_notifications 17.1.2 |
| Font | Sarabun (Thai) |

---

## Key Features

- **Offline-first** — works without internet; Google Sheets sync is optional
- **Thai-optimized** — Sarabun font, Thai dates, Thai bank slip parsing, Thai numeral OCR
- **Semi-auto transactions** — bank notification → transaction without manual entry
- **Multi-entity** — transactions, debts, AR, and subscriptions in one ecosystem

---

## Knowledge Pages

- [[mymoney/architecture|Architecture]] — layered architecture, providers, directory layout
- [[mymoney/data-models|Data Models]] — AppTransaction, AppCategory, Debt, Subscription, AccountReceivable
- [[mymoney/services|Services & Screens]] — DatabaseService, OcrService, PredictionService, GoogleSheets, Notifications, Screens

---

## Related Projects

- [[bank-noti-tester/index|Bank Noti Tester]] — dev tool that simulates notifications for testing this app
