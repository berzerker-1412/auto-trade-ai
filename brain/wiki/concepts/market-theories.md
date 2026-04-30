---
title: Market Theories
type: concept
tags: [market-theory, dow-theory, elliott-wave, wyckoff, trading-philosophy]
sources: 1
created: 2026-04-30
updated: 2026-04-30
---

## Overview

Market theories provide frameworks for understanding *why* price moves the way it does — not just what patterns to trade, but the underlying market dynamics. Three frameworks are most relevant for systematic trading:

---

## Dow Theory

**Core principle:** Market trends exist at three levels, confirmed by volume.

### Three Trends

| Level | Description | Duration |
|-------|-------------|----------|
| **Primary** | Major bull/bear market cycles | Months to years |
| **Secondary** | Corrections within primary (30–70% retracements) | Weeks to months |
| **Minor** | Day-to-day noise | Hours to days |

### Three Phases of a Bull Market

1. **Accumulation** — smart money enters quietly; price flat or slowly rising
2. **Public Participation** — trend confirmed; momentum builds; media coverage increases
3. **Distribution** — smart money exits; price makes final parabolic move before collapse

### Confirmation Rule

> "A trend must be confirmed by both indices" (Industrial + Transport)

In modern context: multiple timeframes or asset classes confirming the same direction.

### Key Tenets

- Price discounts everything (all known information is already in the price)
- Trends persist until a clear reversal signal appears
- Volume confirms the trend — rising prices with increasing volume = healthy

---

## Elliott Wave Theory

**Core principle:** Markets move in 5-wave impulse patterns followed by 3-wave corrections, fractally at all timeframes.

### Wave Structure

```
Impulse (5 waves, in direction of trend):
  Wave 1: First push
  Wave 2: Pullback (doesn't retrace below wave 1 start)
  Wave 3: Strongest wave (never the shortest)
  Wave 4: Pullback (doesn't overlap wave 1)
  Wave 5: Final push

Correction (3 waves, against trend):
  Wave A: First counter-trend move
  Wave B: Bounce (partial retrace of A)
  Wave C: Final move in correction direction
```

### Fibonacci Ratios

| Wave Relationship | Ratio |
|-------------------|-------|
| Wave 2 retraces Wave 1 | 50–78.6% |
| Wave 3 vs Wave 1 | 161.8% or 261.8% (extension) |
| Wave 4 retraces Wave 3 | 23.6–38.2% |
| Wave 5 vs Wave 3 | 61.8% or 100% |

**Key rules:**
- Wave 2 never fully retraces Wave 1
- Wave 3 is never the shortest impulse wave
- Wave 4 never overlaps Wave 1 territory (in a 5-wave impulse)

### Practical Use

- **Count waves on higher timeframes** to identify current position in cycle
- **Extensions** in Wave 3 or 5 often produce the best trade setups
- **Corrective waves** (A-B-C) offer counter-trend entry opportunities

---

## Wyckoff Method

**Core principle:** Price movements result from institutional ("smart money") accumulation and distribution. Individual traders can identify smart money activity through volume analysis and price behavior.

### Four Phases

```
Phase 1: Accumulation     — institutional buying at support, price range-bound
Phase 2: Markup          — price breaks out of range, trend established
Phase 3: Distribution    — institutions sell to public, price tops
Phase 4: Markdown         — price declines
```

### Wyckoff Composite Operator (C.C.O.)

Think of the market as being run by a single "composite operator." Their actions are visible through:

1. **Volume spread analysis** — how price moves relative to volume
2. **Price and volume behavior at supply/demand zones**
3. **Spring and Upthrust** — tests of support/resistance that fail (smart money trapping)

### Wyckoff Schematics

**Spring:** Price breaks below support, then quickly reverses — smart money absorbed selling, markup imminent.

**Upthrust:** Price breaks above resistance, then reverses — smart money distributing, markdown imminent.

### Practical Application

```
Accumulation识别:
  - Price in range (weeks to months)
  - Volume spikes on down-moves but price doesn't fall further
  - Price tests lows multiple times without breaking

Markup信号:
  - Volume confirmation on breakout
  - Price accelerates away from range
  - Pullbacks are shallow

Distribution识别:
  - Volume increases on rallies (smart money distributing)
  - Price fails at previous highs
  - Last point of supply (LPSY) appears before breakdown
```

---

## Practical Comparison

| Aspect | Dow Theory | Elliott Wave | Wyckoff |
|--------|-----------|-------------|---------|
| **Timeframe** | Daily+ | Any | Daily+ |
| **Focus** | Trend confirmation | Wave counting | Smart money |
| **Entry signal** | Trend breakout | Wave 3 start | Spring/Upthrust |
| **Stop-loss** | Below prior low | Below Wave 1/2 | Outside range |
| **Complexity** | Low | High | Medium |

**In auto-trade-ai context:** Wyckoff is most practical for detecting accumulation/distribution phases using volume data. Elliott wave counts could be automated but subjective at scale. Dow theory underpins the multi-timeframe approach.

---

## Related Concepts

- [[chart-patterns]] — Wyckoff phases map to chart patterns (accumulation → base, markup → breakout)
- [[technical-indicators]] — Volume indicators (OBV) help identify Wyckoff phases
- [[risk-management]] — stop-loss placement consistent across all three frameworks
- [[ai-ml-trading]] — institutional flow detection as ML feature
