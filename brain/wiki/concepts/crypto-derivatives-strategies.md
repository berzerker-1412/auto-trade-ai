---
title: Crypto Derivatives Strategies
type: concept
tags: [derivatives, options, perpetual-futures, funding-rate, basis-trading, gamma, theta, volatility-surface]
sources: [docs/crypto-derivatives-strategies.md]
created: 2026-05-01
updated: 2026-05-01
---

## Overview

Crypto derivatives are financial instruments whose value is derived from underlying assets (BTC, ETH). This page covers strategies using perpetual futures, options, and funding rate mechanisms — essential knowledge for systematic crypto trading.

---

## 1. Options Strategies for BTC/ETH

### Options Fundamentals

| Term | Definition |
|------|------------|
| Call Option | Right to BUY at strike price |
| Put Option | Right to SELL at strike price |
| Strike Price | Price at which option can be exercised |
| Premium | Cost paid for the option |
| Expiry | When option expires worthless if OTM |

### Basic Strategies

**1. Covered Call** (Income-generating for BTC holders)
```
Setup: Hold BTC + Sell OTM Call (e.g., Strike = +15% above current)
Profit: Keep premium; limited upside above strike
Risk: BTC upside capped at strike + premium
Best for: Sideways or slightly bullish markets
```

**2. Protective Put** (Insurance for BTC position)
```
Setup: Hold BTC + Buy OTM Put (e.g., Strike = −10% below current)
Profit: Unlimited upside; loss capped at strike
Risk: Premium paid (cost of insurance)
Best for: Bear market protection, high-volatility periods
```

**3. Cash-Secured Put** (Structured "buy the dip")
```
Setup: Hold cash + Sell OTM Put (willing to buy at strike)
Profit: Earn premium; buy BTC at discount if assigned
Risk: BTC drops below strike (but you wanted to buy anyway)
Best for: Accumulating BTC at lower prices systematically
```

**4. Bull/Bear Spreads** (Defined-risk directional bets)
```
Bull Call Spread: Buy Call (lower strike) + Sell Call (higher strike)
- Max profit = spread width − net premium paid
- Max loss = net premium paid
- Risk/reward capped

Bear Put Spread: Buy Put (higher strike) + Sell Put (lower strike)
- Max profit = spread width − net premium paid
- Max loss = net premium paid
```

### Advanced Strategies

**5. Straddle** (Volatility trade — direction-agnostic)
```
Setup: Buy Call + Buy Put at same strike (usually ATM)
Profit if: BTC moves significantly in EITHER direction
Max loss: Both premiums paid
Break-even: Strike ± (Call Premium + Put Premium)
Best for: Pre-announcement trades (ETF approvals, halving)
```

**6. Strangle** (Cheaper volatility trade)
```
Setup: Buy OTM Call + Buy OTM Put (different strikes)
- Cheaper than straddle (further from money)
- Requires larger move to profit
- Best for: Cheap volatility plays before major events
```

**7. Iron Condor** (Premium collection in range-bound markets)
```
Setup: Bull Put Spread + Bear Call Spread
- Sell OTM Put (lower) + Buy further OTM Put (protection)
- Sell OTM Call (higher) + Buy further OTM Call (protection)
Profit: Net premium received if price stays within sold strikes
Risk: Width of spreads − net premium
Best for: Low-volatility periods; BTC in tight range
```

---

## 2. Perpetual Futures & Funding Rate Arbitrage

### What are Perpetual Futures ("Perps")?
Perpetual futures are futures contracts that never expire. They mimic spot price through a funding rate mechanism.

### How Funding Rate Works

```
When Perp Price > Spot Price → Funding Rate positive (long pays short)
When Perp Price < Spot Price → Funding Rate negative (short pays long)

Funding Rate = (Mark Price − Index Price) / Index Price × 8 (per 8 hours)
Typical BTC funding: −0.01% to +0.04% every 8 hours
```

### Funding Rate Arbitrage Strategy

**Method 1: Spot-Perp Arbitrage (Risk-free in theory)**
```python
# ขั้นตอน:
# 1. ซื้อสินทรัพย์ใน spot market
# 2. Short perpetual futures at higher price
# 3. เก็บ funding rate ทุก 8 ชั่วโมง
# 4. เมื่อ funding rate กลับสู่ปกติ → ปิดทั้งสองข้าง

# ตัวอย่าง:
# Buy BTC spot @ $60,000
# Short BTC-PERP @ $60,150 (premium 0.25%)
# Funding rate = +0.01% per 8 hours
# Daily earning = 3 × 0.01% × $60,000 = $18/day
# Monthly = ~$540 from funding alone (plus any basis收敛)
```

**Method 2: Cross-Exchange Arbitrage**
```python
# เมื่อ funding rate ต่างกันมากระหว่าง exchanges
# Binance: +0.02% per 8h
# Bybit:  −0.01% per 8h
# Strategy: Long ที่ Bybit, Short ที่ Binance → รับ funding ทั้งสองข้าง
```

**Method 3: Future Curve Arbitrage**
```
Contango (futures > spot): Sell expensive futures, buy spot
Backwardation (futures < spot): Buy cheap futures, short spot
```

### Risks of Funding Rate Arbitrage
- **Execution risk**: Cannot close both positions simultaneously
- **Liquidity risk**: Thin books on some exchanges
- **Counterparty risk**: Exchange insolvency (FTX lesson)
- **Margin call risk**: Price moves against you on the leveraged side
- **Liquidation risk**: Under extreme volatility, leveraged position liquidated

---

## 3. Basis Trading

### What is Basis?
```
Basis = Futures Price − Spot Price

Contango: Basis > 0 (futures priced above spot)
Backwardation: Basis < 0 (futures priced below spot)
```

### Cash and Carry Arbitrage (Contango)
```python
# หาก basis ใหญ่เกินไป (contango มาก):
# 1. ซื้อสินทรัพย์ใน spot
# 2. Short futures ที่ futures price สูงกว่า
# 3. ถือจน futures expire → basis收敛 → ปิดทั้งสองข้าง

# ต้องคำนวณ:
# - Cost of carry (บันทึก opportunity cost)
# - Storage cost (สำหรับ physical commodities)
# - Financing cost (borrow rate)
# Net basis = Gross basis − Cost of carry
```

### Basis Mean Reversion
```python
# basis มักจะ mean-revert เมื่อ:
# 1. ถึง expiry date (futures converge to spot)
# 2. เมื่อ funding rate สูงมาก → arbitrageurs ทำให้ basis ลดลง

# Strategy: Short basis when basis > historical 90th percentile
# Exit when basis < historical 50th percentile
```

---

## 4. Greeks & Options Strategies

### The Four Key Greeks

| Greek | Measures | Positive When |
|-------|----------|---------------|
| **Delta** | Price sensitivity of option | ATM ≈ 0.5 |
| **Gamma** | Rate of Delta change | ATM options |
| **Theta** | Time decay per day | Always negative for long options |
| **Vega** | Volatility sensitivity | Higher for longer-dated options |

### Delta in Practice
```python
# การใช้ Delta สำหรับ direction trading:
# Position Delta = Option Delta × Quantity

# Long 1 BTC Call (delta ≈ 0.50)
# Effective BTC exposure = 0.50 BTC

# Long 1 BTC Put (delta ≈ −0.50)
# Effective short BTC exposure = −0.50 BTC
```

### Gamma Scalping
```
Gamma scalping: ปรับ position อย่างต่อเนื่องเพื่อ capture theta
- เมื่อ price ขยับ → delta เปลี่ยน → ต้อง rebalance
- ในสภาวะ high gamma → rebalance บ่อย = capture more theta

สูตรง่าย: P/L = 0.5 × Gamma × (ΔS)² − Theta × Δt
```

### Theta Harvesting Strategies

**The Wheel Strategy** (Systematic theta collection)
```
1. Sell OTM Put (collect premium)
2. If assigned → sell OTM Call (covered)
3. If not assigned → repeat step 1
4. ทำซ้ำจนกว่าจะได้สินทรัพย์ที่ strike ที่ต้องการ
```

**Short Strangle** (High-probability income)
```
Sell OTM Call + Sell OTM Put (same expiry)
- Higher premium than covered call
- Requires wider stop-out zone
- Probability of profit = probability price stays in range
```

---

## 5. Volatility Surface Trading

### What is the Volatility Surface?
An implied volatility surface plots IV across different strikes and expirations. In crypto, it reveals market expectations of future uncertainty.

### Key Surface Features

**Volatility Smile/Skew**
```
BTC typical skew: OTM puts more expensive than OTM calls
- Fear of crash → higher IV on puts
- Called "reverse smile" or "skew"

Trading the skew:
- Buy cheap OTM calls (tail risk on upside)
- Sell expensive OTM puts (income + high premium)
```

**Term Structure**
```
Near-term IV > Long-term IV: "Backwardation"
- Market expects near-term volatility
- Common before major events (halving, ETF decisions)

Near-term IV < Long-term IV: "Contango"
- Market expects future volatility to increase
- Common post-crash recovery
```

### Volatility Trading Rules
```
1. When IV > HV (historical vol) significantly → options expensive → sell them
2. When IV < HV significantly → options cheap → buy them
3. IV Rank: current IV vs 30-day IV range (0–100%)
   - IV Rank > 70 → IV is high → favor selling strategies
   - IV Rank < 30 → IV is low → favor buying strategies
```

---

## Related Concepts

- [[trading-strategies]] — Basic strategies (trend-following, breakout, mean reversion)
- [[advanced-quantitative-strategies]] — Stat arb, pairs trading, market making
- [[risk-management]] — Position sizing, Greeks, portfolio risk
