---
title: Trading Psychology & Behavioral Finance
type: concept
tags: [trading-psychology, behavioral-finance, cognitive-bias, backtesting-pitfalls, trade-journal, mental-models]
sources: [docs/portfolio-position-sizing-research.md]
created: 2026-05-01
updated: 2026-05-01
---

## Overview

"The markets are a device for transferring money from the impatient to the patient." — Warren Buffett

Trading psychology is often the difference between traders who understand a strategy and traders who profit from it. Most strategy failures come from psychological issues, not flawed systems.

---

## 1. Cognitive Biases in Trading

### Loss Aversion (Kahneman & Tversky, 1979)
**The bias**: Losses feel twice as painful as equivalent gains feel good.

**In trading**: Holding a losing position too long because closing it "locks in" the loss; taking profits too early to avoid the pain of giving back gains.

**Example**:
```
Loss of $100:  Emotional pain = -2x (experienced as -$200)
Gain of $100:  Emotional pleasure = +1x ($100)

Result: People hold losing positions 2x longer than winning ones
```

**Counter-strategy**:
- Use mechanical stop-losses (never discretionary)
- Pre-commit to exit rules before entering
- Track emotional decisions separately from mechanical ones

---

### Confirmation Bias
**The bias**: Seeking information that confirms existing beliefs; ignoring contradictory evidence.

**In trading**: Only reading bullish articles when holding long; dismissing bearish signals as "noise."

**Counter-strategy**:
- Keep a "devil's advocate" journal: write the Bear case for every Bull trade
- Follow analysts with opposing views
- Set rules that require confirmation of BOTH bullish AND bearish signals

---

### Anchoring Bias
**The bias**: Fixating on a specific reference point (anchor) even when it's irrelevant.

**In trading**:
- "BTC is cheap at $60K because I bought at $70K" (irrelevant to future price)
- Entry price becomes psychological barrier ("I won't sell until I break even")
- Resistance levels become anchors even after fundamentals change

**Counter-strategy**:
- Always evaluate current price vs fair value, not vs your entry
- Use percentage-based stops, not price-based ("stop at -10%", not "stop at $58K")
- Review each position as if you don't already own it

---

### Availability Bias
**The bias**: Overweighting recent or memorable events when assessing probability.

**In trading**:
- "Markets always crash after halving" (only happened twice in BTC history)
- Fear of "another FTX" causing over-caution after exchange collapses
- Recency: judging 2025 performance by just the last 3 months

**Counter-strategy**:
- Use long-term data, not just recent history
- Maintain statistical perspective: require 100+ samples before drawing conclusions
- Keep a long-term performance log, not just recent trades

---

### Recency Bias
**The bias**: Believing the future will resemble the very recent past.

**In trading**: After a 5-day winning streak, feeling "I'm on a hot streak" and increasing size. After 5 losses, feeling "I can't do anything right" and quitting.

**Counter-strategy**:
- Treat each trade independently (the coin doesn't remember previous flips)
- Size based on Kelly/fixed rules, not "feelings"
- Review decisions based on process, not outcomes

---

### Overconfidence Bias
**The bias**: Overestimating one's ability to predict and control outcomes.

**In trading**:
- "I can time the market" (evidence: short-term, no)
- Position sizes too large relative to edge
- Underestimating tail risk

**Counter-strategy**:
- Keep a "confidence calibration" log: record predicted outcomes vs actual
- Use Half-Kelly (less confident in edge estimates)
- Stress test: ask "What if I'm completely wrong?" for every trade

---

## 2. Backtesting Pitfalls

### Overfitting (The Biggest Killer)

**What it is**: Tuning a strategy too precisely to historical data, capturing noise instead of signal.

**The tell-tale sign**:
- Strategy has 20+ parameters
- Works on 2018–2023 but fails on 2024
- Different parameter sets give wildly different results

**Overfit diagnosis**:
```python
# Walk-forward analysis: test strategy on data AFTER the period used to optimize
# If OOS (out-of-sample) performance is much worse -> overfitted

# 1. Divide data: 70% train, 30% test
# 2. Optimize on train only -> get parameter set
# 3. Test on test data WITHOUT re-optimizing
# 4. If test performance < 50% of train -> overfitted

def walk_forward_analysis(prices, train_ratio=0.7):
    split = int(len(prices) * train_ratio)
    train_prices = prices[:split]
    test_prices = prices[split:]
    
    # Optimize only on train data
    best_params = optimize(train_prices)
    
    # Test on unseen data
    train_performance = backtest(train_prices, best_params)
    test_performance = backtest(test_prices, best_params)
    
    overfit_ratio = test_performance / train_performance
    return best_params, overfit_ratio
```

**Prevention rules**:
- Maximum 5 parameters for any strategy
- Use 3x more data points than parameters
- Require IS/OOS ratio > 0.5 to accept strategy

---

### Look-Ahead Bias

**What it is**: Accidentally using future data in the present calculation.

**Common sources**:
- Non-adjusted close price (dividends, splits not accounted for)
- Forward-filled data when backfilling fundamental data
- Using "high" and "low" that include intraday extremes not known until end of day

**Example**:
```python
# WRONG: using same-bar data for signal
if high > bollinger_upper and close < bollinger_upper:
    # close was below band at bar close, but high (same bar) already broke it
    # This is look-ahead: you can't know the high until the bar closes

# RIGHT: only use previous bar data or current bar close
if close > bollinger_upper and open < bollinger_upper:
    # broke out on close using only known information
```

---

### Survival Bias

**What it is**: Only studying assets that "survived," ignoring those that were delisted/bankrupted.

**In crypto**: Studying BTC and ETH performance while ignoring all failed coins.
- Of 25,000+ coins created, > 90% are dead
- An index of all crypto would have terrible performance
- BTC looks amazing partly because we only see survivors

**Counter-strategy**:
- Include delisted/crashed assets in backtest
- Test on equal-weight index of all assets, not just survivors
- Use index proxies when possible

---

### Transaction Cost Neglect

**What it is**: Forgetting that every trade has cost, making marginal strategies unprofitable.

**Key costs**:
```
- Exchange fees: 0.1% per side (maker/taker)
- Slippage: 0.05–0.5% depending on order size
- Funding rate (perpetuals): 0.01–0.04% per 8 hours
- Overnight funding (margin): 0.01–0.05% per day
- Network fee (withdrawals): $1–$50 per transaction
```

**The math that kills strategies**:
```python
# Strategy trades 20 times per month
# Fees (round trip) = 0.2% x 20 = 4% per month in fees alone
# At 12% monthly target: 8% net after fees
# Most "profitable" backtests ignore this
```

---

### Data Snooping (Multiple Testing)

**What it is**: Testing many variations of a strategy and reporting only the best.

**The statistics**: If you test 100 strategies randomly, the best one will look great even if all are noise. This is the "false discovery rate."

**Solution**: Use separate in-sample and out-of-sample datasets, or use the Sharpe ratio with a "sharpe of 1.0 or higher only" rule.

---

## 3. Trade Journaling

### What to Record Per Trade

```python
trade_log_entry = {
    # Pre-trade (before entering)
    "pre_trade_plan": "Why am I taking this?",
    "entry_rule_triggered": "Which rule from my system?",
    "max_loss_accepted": "$X or X%",
    "time_horizon": "Intraday / Swing / Position",
    
    # During trade
    "emotions_during": "Calm / Anxious / FOMO / Revenge",
    "did_I_deviate": True / False,
    
    # Post-trade
    "outcome": "Win / Loss / Breakeven",
    "pnl": 0.0,
    "outcome_vs_plan": "Better / Worse / As Expected",
    "lessons_learned": "What would I do differently?",
    "rule_violated": "None / Stop-loss / Entry rule / Size rule",
}
```

### Key Metrics to Track

| Metric | Formula | Good |
|--------|---------|------|
| Win Rate | Wins / Total | > 40% (for R > 1.5) |
| Avg Win / Avg Loss | mean(win$) / mean(loss$) | > 1.5 |
| Sharpe Ratio | Mean Return / Std | > 1.0 |
| Max Drawdown | Peak - Trough | < 20% |
| Expectancy | W x R - (1-W) | > 0 |
| Risk/Reward | Potential gain / Potential loss | > 2:1 |

---

## 4. Mental Models for Traders

### First Principles Thinking
```
Belief: "BTC always bounces after a 30% drop"
First principles: "BTC is an asset with no cash flows, driven by adoption and sentiment. 30% drops in 2014, 2018, and 2022 all recovered, but for different reasons. Is this time different?"

Better question: "What would make this recovery fail? What is the probability of that?"
```

### Inversion (Münchhausen Trilemma approach)
```
Instead of asking "How do I make money?"
Ask: "What would make me lose all my money?"

List: Blow up on leverage / Exchange hack / Black swan / Drawdown > 50%
-> Then build rules specifically to prevent each
```

### Circle of Competence
```
Know the difference between:
- What you think you know
- What you actually know
- What you don't know you don't know

For crypto: Understand the specific risks (smart contract, regulatory, liquidity)
before using leverage or exotic strategies.
```

### Probabilistic Thinking
```
Never say "BTC will go up" -> Say "BTC has a 65% probability of going up"

Revise probabilities as new information arrives:
- New regulation announced -> -10% to bullish probability
- ETF approved -> +20% to bullish probability
- Whale wallets moving -> -5% to bullish probability
```

### Margin of Safety (Seth Klarman)
```
Only buy when price is significantly below your estimate of fair value.
If fair value = $70K, only buy below $55K (20% margin of safety).

For trading: Only enter when reward/risk is > 3:1 AND confidence > 70%.
```

### Second-Order Thinking
```
First order: "Rate hikes are bad for BTC -> short BTC"
Second order: "Rate hikes hurt risky assets, but also cause liquidity crises
              that lead to Fed pivoting -> long BTC mid-crisis"
Third order: "If everyone thinks the same, who is on the other side?"
```

### Hanlon's Razor (applied to markets)
```
"Never attribute to malice that which is adequately explained by liquidity."

BTC dropped 5% suddenly? Probably not "institutional selling conspiracy."
Probably: large liquidation cascade + thin weekend liquidity.
```

---

## Related Concepts

- [[trading-strategies]] - Entry/exit rules that define process
- [[portfolio-position-sizing]] - Mathematically rigorous sizing
- [[risk-management]] - Stop-loss and position risk rules
- [[advanced-quantitative-strategies]] - Stat arb and quantitative approaches
