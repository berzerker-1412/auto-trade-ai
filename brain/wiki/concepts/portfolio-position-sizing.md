---
title: Portfolio Construction & Position Sizing
type: concept
tags: [kelly-criterion, risk-parity, position-sizing, drawdown, portfolio-risk, optimal-f]
sources: [docs/portfolio-position-sizing-research.md]
created: 2026-05-01
updated: 2026-05-01
---

## Overview

Position sizing is the most impactful risk management decision a trader makes. A study by Thomas Stridsman found that position sizing accounts for more of a trader's P&L than entry/exit timing. This page covers mathematically rigorous approaches to sizing positions within a portfolio.

---

## 1. Kelly Criterion

### The Formula

**Original Kelly (gambling):**
```
f* = (bp - q) / b

f* = fraction of bankroll to bet
b = odds received on the bet (profit / loss)
p = probability of winning
q = probability of losing = 1 - p
```

**Kelly for Trading (simplified):**
```
Kelly % = W - (1 - W) / R

W = Win rate (fraction of winning trades)
R = Win/Loss Ratio = Average Win / Average Loss
```

### Worked Example

```
W = 0.40  (40% win rate)
Average Win = $100
Average Loss = $50
R = 100/50 = 2

Kelly % = 0.40 - (0.60 / 2) = 0.40 - 0.30 = 0.10 = 10%

Interpretation: Risk 10% of portfolio per trade
```

### Kelly Variants

| Variant | Multiplier | Description |
|---------|-----------|-------------|
| Full Kelly | 1x | Maximum growth; extremely volatile |
| Half-Kelly | 0.5x | Most popular; halves both risk and reward |
| Quarter-Kelly | 0.25x | For risk-averse traders |

### Practical Implementation
```python
# คำนวณ Kelly และ variants
def kelly_fraction(win_rate, avg_win, avg_loss):
    if avg_loss == 0:
        return 0
    r = avg_win / abs(avg_loss)
    kelly = win_rate - (1 - win_rate) / r
    return {
        'full_kelly': max(0, kelly),
        'half_kelly': max(0, kelly * 0.5),
        'quarter_kelly': max(0, kelly * 0.25),
    }
```

### Kelly Limitations
1. Requires accurate win rate and R estimates
2. Full Kelly is extremely volatile - a 20% losing streak devastates the account
3. Ignores correlation between positions
4. Assumes infinite capital

---

## 2. Risk Parity

### Core Philosophy
Allocate risk, not capital. Each position should contribute equally to portfolio volatility.

### Formula
```
Asset Weight = (Target Portfolio Risk / N) / Asset Volatility
```

### Worked Example
```
Target portfolio risk: 15%
3 assets: BTC (vol=60%), ETH (vol=80%), Gold (vol=12%)

Equal risk contribution = 15% / 3 = 5%

Weight_BTC  = 5% / 60% = 8.3%
Weight_ETH  = 5% / 80% = 6.3%
Weight_GOLD = 5% / 12% = 41.7%
```

---

## 3. Fixed Ratio (Ryan Jones)

### Formula
```
Position Size = Delta x (1 + 2 x Accumulated Profit / Delta)^0.5

Delta = profit per unit needed to increase position by 1 unit
```

### Worked Example
```
Delta = $1,000 per contract

Accumulated Profit = $0    -> Size = 1,000 x 1.0 = 1 contract
Accumulated Profit = $5,000 -> Size = 1,000 x sqrt(11) = 3.3 -> 3 contracts
Accumulated Profit = $10,000 -> Size = 1,000 x sqrt(21) = 4.6 -> 4 contracts
```

### Python Implementation
```python
import numpy as np

def fixed_ratio_position(delta, accumulated_profit):
    multiplier = 1 + 2 * accumulated_profit / delta
    if multiplier <= 0:
        return 1
    size = delta * np.sqrt(multiplier)
    return max(1, int(size))
```

---

## 4. Optimal F (Ralph Vince)

### TWR Formula
```
TWR = product of (1 + f x H_i) for all trades i

H_i = return of trade i (as fraction)
f = fraction being tested
```

### Python Search for Optimal F
```python
import numpy as np

def find_optimal_f(trades, precision=0.01):
    best_f, best_twr = 0, 0
    for f in np.arange(0.01, 2.0, precision):
        twr = np.prod([1 + f * h for h in trades])
        if twr > best_twr:
            best_twr = twr
            best_f = f
    return best_f, best_twr
```

---

## 5. Correlated Position Sizing

### Portfolio Variance
```
sigma_squared_p = sum_i sum_j w_i w_j sigma_i sigma_j rho_ij
```

### Correlation-Adjusted Kelly
```python
import numpy as np

def correlation_adjusted_kelly(weights, vols, correlations):
    # weights: Kelly fractions for each position
    # vols: individual asset volatilities
    # correlations: NxN correlation matrix
    vol_matrix = np.outer(vols, vols) * correlations
    weight_array = np.array(weights)
    portfolio_variance = np.dot(weight_array, np.dot(vol_matrix, weight_array))
    portfolio_vol = np.sqrt(portfolio_variance)
    raw_total = np.sum(weights)
    adjustment = min(1.0, raw_total / (len(weights) * 0.2))
    return [w * adjustment for w in weights]
```

---

## 6. Drawdown Management

### Recovery Return Formula
```python
def recovery_return(drawdown_pct):
    # drawdown_pct: e.g., 0.20 for 20% drawdown
    # Return needed to break even
    return drawdown_pct / (1 - drawdown_pct)

# 10% -> 11.1%,  20% -> 25%,  50% -> 100%,  90% -> 900%
```

### Drawdown Limits

| Max DD | Recovery Needed | Action |
|--------|----------------|--------|
| 10% | 11% | Acceptable |
| 20% | 25% | Normal |
| 30% | 43% | Review strategy |
| 50% | 100% | Career risk |

### Drawdown Limiting Rules
1. Hard Stop-Out: portfolio drawdown > X% -> exit all positions
2. Volatility-Based Stops: reduce size when market volatility spikes
3. Consecutive Loss Limit: stop after N consecutive losses

---

## 7. Portfolio Risk Limits

### Value at Risk (VaR)

```python
import numpy as np

def historical_var(returns, confidence=0.95):
    sorted_returns = np.sort(returns)
    index = int((1 - confidence) * len(sorted_returns))
    return abs(sorted_returns[index])
```

### Risk Limit Table

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Daily VaR | > 1% | > 2% | Cut 50% |
| Max Drawdown | > 10% | > 20% | Stop trading |
| Portfolio Beta | > 1.5 | > 2.0 | Hedge |
| Volatility ratio | > 2x avg | > 3x avg | Reduce size |

### Position-Level Risk Rules
```
1. Max 1 position = 5% portfolio risk
2. Max 3 positions = 10% total risk
3. Max daily loss = 3% -> stop for the day
4. Max weekly loss = 8% -> reduce size 50%
```

---

## Related Concepts

- [[risk-management]] - Stop-loss, position sizing basics
- [[trading-strategies]] - Entry/exit rules that define win rate and R
- [[advanced-quantitative-strategies]] - Stat arb pairs trading sizing
