---
title: MyMoney — Architecture
type: project
tags: [flutter, architecture, provider, state-management]
created: 2026-04-12
updated: 2026-04-13
---

See overview at [[mymoney/index|MyMoney]].

---

## Layered Architecture

The app uses a clean 4-layer architecture:

```text
Screens (UI)
    ↓
Providers (State — ChangeNotifier)
    ↓
Services (Business Logic)
    ↓
Models + SQLite (Data)
```

Each layer only depends on the layer below. No circular dependencies.

---

## Directory Layout

```text
lib/
├── core/        — constants, themes, formatters (Thai date/currency)
├── models/      — data classes + SQLite serialization
├── providers/   — 6 ChangeNotifier state domains
├── services/    — database, OCR, prediction, Google Sheets, notifications
└── screens/     — UI organized by feature
```

---

## Providers (State Domains)

App bootstraps with `MultiProvider` in `main.dart`, registering 6 providers:

| Provider | Responsibility |
| --- | --- |
| TransactionProvider | transaction list, monthly summary (income/expense/balance), auto-detection flag |
| CategoryProvider | category list, keyword matching for AI prediction |
| DebtProvider | debt list, "due soon" filter, utilization rate |
| SubscriptionProvider | subscription list, monthly cost total, next billing date |
| AccountReceivableProvider | AR list, overdue detection, partial payment tracking |
| SettingsProvider | theme, Google Sheet ID, sync/notification toggles (SharedPreferences) |

All providers follow the same pattern:

1. `init()` — load data from SQLite at bootstrap
2. `notifyListeners()` — trigger UI rebuild on data change

---

## App Bootstrap Flow

```text
main()
  → initialize DatabaseService (SQLite)
  → initialize NotificationService (EventChannel)
  → MultiProvider wrap (6 providers)
  → each provider.init() loads from SQLite
  → MaterialApp renders
```
