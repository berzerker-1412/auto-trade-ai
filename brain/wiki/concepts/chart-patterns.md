---
title: Chart Patterns
type: concept
tags: [chart-patterns, technical-analysis, price-action, reversal, continuation]
sources: 1
created: 2026-04-30
updated: 2026-04-30
---

## Overview

Chart patterns are formations created by price action over multiple time periods. Unlike single candlesticks, they encode structural supply/demand dynamics and are classified as either **reversal** (trend change) or **continuation** (brief pause before resumption).

**Golden rule:** Breakout must occur on above-average volume to be valid.

---

## Reversal Patterns

### Head and Shoulders (H&S)

```
         ┌───┐
        /  H  \      H = Head (highest peak)
 ┌───┐ /     \ ┌───┐
 │ L ││       ││ R │  L = Left Shoulder, R = Right Shoulder
 └───┘│       │└───┘
 ─────┴───────┴──────  Neckline
```

**Identification:**
1. Left shoulder — first peak
2. Head — peak exceeding all others
3. Right shoulder — lower peak, roughly level with left shoulder
4. Neckline — horizontal line through the lows between shoulders

**Signal:** When price **breaks below neckline** → bearish reversal
**Price Target:**
```
Target = 2 × Neckline − Head
```
**Inverse H&S:** Mirror image → bullish reversal (neckline breakout upward)

**Failure Rate Context:** H&S is most reliable at market highs; inverse H&S performs better on weekly timeframes.

---

### Double Top / Double Bottom

```
Double Top:                    Double Bottom:
       ┌───┐                    ──────────────
      /     \                   \     1     /
     /   1   \                  2\         /2
    /         \                  \   1   /
   /     2     \                  \       /
  ───────────────  Neckline         \   /
       ▼                              └───┘
   (breakdown)                          ▲
                                    (breakout)
```

**Identification:**
- Two peaks/bottoms at roughly the same level (within ±5%)
- A clear trough/bump between them
- Volume on second peak/bottom should be lower than the first

**Price Target:**
```
Target = Neckline − (Peak − Neckline)    # Double Top
Target = Neckline + (Neckline − Bottom)  # Double Bottom
```

---

### Triple Top / Triple Bottom

Three attempts at the same level before breakdown/breakout. Stronger signal than double top/bottom — the market made three attempts and failed.

### Rounding Bottom (Saucer)

Gradual, smooth transition from selling pressure to buying pressure. Volume typically decreases at the bottom and increases on the right side. Often forms over weeks or months.

**Best detected on weekly/monthly charts.**

---

## Continuation Patterns

### Triangles

**Ascending Triangle:**
```
         ▲  flat resistance
        / \
       /   \  rising support
 ─────/─────\─────
```

- Horizontal resistance + rising support
- **Bullish bias** — resistance eventually breaks upward
- Measured move = height of triangle added to breakout point

**Descending Triangle:**
```
       /  flat support
      / \
 ────/───\─────  falling resistance
```

- Flat support + falling resistance
- **Bearish bias** — support eventually breaks downward

**Symmetric Triangle:**
```
       /\  falling resistance
      /  \
     /    \
    /      \  rising support
```

- Both sides converging
- **Neutral** — breakout direction determines direction
- Most common triangle type

### Flags and Pennants

```
Flag:                          Pennant:
    \  (slope opposite         /\  (converging
     \   to trend)             \/
      \                    ────/───
       ────────────            (short duration)
       (strong move before)
```

- Appear after a strong directional move ("the pole")
- Brief consolidation, then trend usually continues
- **Most reliable continuation pattern in strong trends**

**Key:** The consolidation should be shallow (flag at < 38.2% retracement of the pole is ideal).

### Wedges

Similar to triangles but both boundaries slope in the same direction:
- **Rising Wedge** — both lines slope up → **bearish** (buyers losing conviction)
- **Falling Wedge** — both lines slope down → **bullish** (sellers losing conviction)

### Rectangles

Sideways consolidation between parallel horizontal support and resistance levels. Represents a battle between buyers and sellers at equilibrium. Breakout usually continues the prior trend.

```
────────────────  Resistance
 │            │
 │            │  ← sideways range
 │            │
────────────────  Support
```

---

## Pattern Measurement Rule

```
Measured Move = Reference Point ± Pattern Height
```

| Pattern | Reference Point | Direction |
|---------|---------------|-----------|
| H&S | Neckline | Down from neckline |
| Double Top | Neckline | Down from neckline |
| Ascending Triangle | Resistance (breakout) | Up by triangle height |
| Flag/Pennant | Start of pole | Continuation of pole direction |

---

## Common Mistakes

1. **Trading patterns without volume confirmation** — most false signals lack volume
2. **Ignoring the trend context** — reversal patterns in a strong trend = countertrend bet
3. **Measuring targets as certainties** — targets are probabilities, not certainties
4. **Trading inside the pattern** — wait for breakout confirmation

---

## In auto-trade-ai

Chart patterns are harder to programmatically detect than candlesticks. The current `signal_generator.py` focuses on candlestick patterns and indicators. Chart pattern recognition could be added as a future module using contour detection or structural analysis of price series.

## Related Concepts

- [[candlestick-patterns]] — single and multi-candlestick signals (finer granularity)
- [[technical-indicators]] — volume indicators (OBV) help confirm breakouts
- [[risk-management]] — stop-loss placement below neckline for reversal trades
