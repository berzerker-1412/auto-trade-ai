---
title: Trading Strategy
type: concept
tags: [trading, AI, signals, GPT-4o, prompt]
created: 2026-04-30
updated: 2026-04-30
sources: 0
---

## Overview

AI generates BUY/SELL signals using GPT-4o with a structured prompt containing market data.

## Prompt Structure

System role:
```
You are a professional trading signal generator.
Analyze market data and generate clear BUY or SELL signals.
Return JSON format with: direction, entry_price, quantity,
stop_loss, take_profit, confidence (0-1), reasoning.
```

User prompt includes:
- Current price, 24h high/low, volume
- Technical/news analysis text
- Required output format

## Signal Criteria

- `confidence >= 0.75` → execute trade
- `confidence < 0.75` → no trade

## Open Questions

- Should technical indicators (RSI, MACD) be added to prompt?
- News sentiment analysis integration?
- Custom prompt tuning per asset class?
- How to handle low-confidence high-conviction setups?
