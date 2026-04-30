---
title: auto-trade-ai: Risk Management
type: project
tags: [risk-management, trading, stop-loss, position-sizing]
created: 2026-04-30
updated: 2026-04-30
---

## Risk Management Rules

Defined in `config/settings.yaml`:

```yaml
risk_management:
  max_position_size: 0.1        # Max 10% of balance per trade
  stop_loss_percent: 2.0         # 2% stop loss
  take_profit_percent: 5.0      # 5% take profit
  max_concurrent_trades: 3
```

---

## Position Sizing

The most important risk control lever:

```python
def calculate_position_size(account_balance: float,
                            risk_per_trade: float,
                            stop_distance_pct: float) -> float:
    """
    คำนวณขนาด position ที่เหมาะสม
    account_balance = มูลค่าพอร์ตทั้งหมด
    risk_per_trade  = % ที่ยอมเสียต่อ trade (เช่น 0.01 = 1%)
    stop_distance   = ระยะห่างราคาถึง stop-loss (% จากราคาเข้า)
    """
    risk_amount = account_balance * risk_per_trade
    position_size = risk_amount / stop_distance_pct
    return position_size
```

**Example:** $100,000 account, 1% risk per trade, 2% stop distance
```
Position Size = $100,000 × 0.01 / 0.02 = $5,000
```

---

## ATR-Based Position Sizing

Adapts to current volatility:

```python
def calculate_atr_position(account_balance: float,
                           risk_per_trade: float,
                           atr: float,
                           stop_atr_multiplier: float = 2.0) -> float:
    """
    ใช้ ATR กำหนดระยะ stop-loss (ผันผวนตามตลาด)
    stop_atr_multiplier = จำนวน ATR ที่ใช้เป็น stop (2 = 2×ATR)
    """
    stop_distance = atr * stop_atr_multiplier
    stop_distance_pct = stop_distance  # ATR เป็น absolute price
    risk_amount = account_balance * risk_per_trade
    return risk_amount / stop_distance_pct
```

---

## Kelly Criterion

Mathematically optimal bet sizing based on win rate and reward-to-risk ratio:

```
f* = W − (1−W)/R

โดย:
  f* = สัดส่วน capital ที่ควรเดิมพัน
  W  = win rate (เช่น 0.55 = 55% ชนะ)
  R  = reward-to-risk ratio (เช่น 2.0 = ได้ 2 ต่อ 1)
```

**Example:** 55% win rate, 2:1 reward-to-risk
```
f* = 0.55 − (0.45 / 2.0) = 0.55 − 0.225 = 0.325 = 32.5%
```

**Practical constraint:** Use fractional Kelly (25–50% of f*) to reduce volatility.

---

## Stop-Loss Strategies

| Type | Rule | Best For |
|------|------|----------|
| **Fixed %** | Stop = Entry × (1 − stop%) | Simple systems |
| **ATR-based** | Stop = Entry − k × ATR | Volatile markets |
| **Support/Resistance** | Stop below nearest S/R | Pattern trades |
| **Time-based** | Exit after N periods | Short-term trades |

**Never move a stop-loss further away from entry** — this violates risk management principles.

---

## Risk Management Key Rules

1. **Risk ≤ 1–2% per trade** — even 10 consecutive losses = still have 80%+ capital
2. **Reward-to-risk ≥ 2:1** — cut losers quickly, let winners run
3. **Win rate ≥ 40%** for 2:1 R:R to be profitable
4. **Max drawdown limit** — pause trading if drawdown exceeds threshold (e.g., −10%)
5. **Diversify** — don't concentrate in one asset or direction
6. **Never average down on a losing position**

---

## Related Concepts

- [[technical-indicators]] — ATR is the primary input for adaptive stops
- [[trading-strategies]] — each strategy has different optimal position sizing
- [[ai-ml-trading]] — RL reward functions should incorporate risk-adjusted returns
- [[market-theories]] — Wyckoff risk management at accumulation/distribution boundaries

## Sources

See [[ta-deep-dive]] Section 6: Risk Management for detailed Thai-language coverage.

```yaml
ai:
  confidence_threshold: 0.75      # Minimum confidence to execute
  max_trades_per_day: 5
```

---

## Position Sizing

```
max_position_value = balance × max_position_size
                 = 100,000 × 0.1
                 = 10,000 USDT per trade

quantity = max_position_value / entry_price
         = 10,000 / 62,500
         = 0.16 BTC
```

This ensures no single trade can lose more than 2% of portfolio (since SL = 2%).

---

## Stop-Loss & Take-Profit

### For BUY (Long) Positions

```
Entry: 62,500 USDT
Stop-Loss: 62,500 × (1 - 0.02) = 61,250 USDT  (-2%)
Take-Profit: 62,500 × (1 + 0.05) = 65,625 USDT (+5%)
```

### For SELL (Short) Positions

```
Entry: 62,500 USDT
Stop-Loss: 62,500 × (1 + 0.02) = 63,750 USDT  (+2%)
Take-Profit: 62,500 × (1 - 0.05) = 59,375 USDT (-5%)
```

---

## Why These Numbers?

| Rule | Value | Rationale |
| --- | --- | --- |
| Max position | 10% | Diversify across at least 10 positions |
| Stop-loss | 2% | Cut losses quickly, survive losing streaks |
| Take-profit | 5% | Reward-to-risk ratio = 2.5:1 (decent edge) |
| Confidence | 0.75 | Only trade high-conviction signals |
| Max concurrent | 3 | Avoid overtrading, manage capacity |
| Max daily trades | 5 | Prevent overtrading in volatile markets |

---

## Risk-of-Ruin Calculation

With 2% max loss per trade and 10% max position:

```
Worst case per trade: 2% of portfolio
Worst case with 3 concurrent: 6% of portfolio

To blow up 50% of portfolio (ruin):
- Need 25 consecutive max losses (25 × 2% = 50%)
- With win rate ~50%, probability of 25 losses in a row ≈ 1 in 33M

→ System is robust to losing streaks
```

---

## P&L Tracking

### Balance Update Logic

```python
# BUY trade closed at profit
if pnl > 0:
    balance += pnl           # Add profit

# BUY trade closed at loss
if pnl < 0:
    balance += 0             # Loss already deducted at entry
    # Loss absorbed, no further action
```

Note: For BUY orders, balance is deducted at entry time. For SELL orders, no deduction until close.

---

## Key Metrics

| Metric | Formula |
| --- | --- |
| Win Rate | winning_trades / total_trades × 100 |
| Avg Win | total_pnl / winning_trades |
| Avg Loss | abs(total_pnl) / losing_trades |
| Risk-Reward | avg_win / avg_loss |

**Target:** Win rate ≥ 40% with R:R ≥ 2:1 → profitable system

---

## Open Questions

- How to dynamically adjust position size based on confidence?
- Should stop-loss be tighter in high-volatility periods?
- Any trailing stop mechanism planned?
- How to handle news events / market regime changes?
