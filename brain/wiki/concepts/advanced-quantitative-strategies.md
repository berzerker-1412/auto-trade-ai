---
title: Advanced Quantitative Strategies
type: concept
tags: [stat-arb, pairs-trading, market-making, cointegration, orderbook, vwap, twap, hft]
sources: [docs/quantitative-systematic-trading.md]
created: 2026-05-01
updated: 2026-05-01
---

## Overview

Advanced quantitative strategies go beyond simple rule-based indicators. They use statistical models, mathematical frameworks, and execution algorithms to find and exploit market inefficiencies systematically.

---

## 1. Statistical Arbitrage (Stat Arb)

### Core Philosophy
Use statistical models to find price inefficiencies that are expected to revert to mean. Profit from the statistical edge, not directional bets.

### Key Principles
- **Mean Reversion**: Prices that deviate from historical average tend to revert
- **Central Limit Theorem**: Returns of many assets approximate normal distribution
- **Law of Large Numbers**: Repeating many trades converges to expected outcome

### Strategy Types

**1. Mean Reversion Stat Arb**
- Buy assets priced below their average; sell when price returns
- Uses Z-Score to identify deviations

**2. Cross-Sectional Stat Arb**
- Compare assets in the same category
- Long the "cheap" one, short the "expensive" one
- Example: Long COIN, Short GBTC (same BTC exposure, different premiums)

**3. ETF Arbitrage**
- Exploit price-NAV discrepancies of ETFs
- Buy NAV when ETF trades at discount; sell when at premium

### Z-Score Entry/Exit Rules

```
Spread = Price_A − β × Price_B
Z-Score = (Spread − Moving_Avg_Spread) / Moving_Std_Spread

Entry: |Z-Score| > 2.0  →  Short the spread
Exit:  |Z-Score| < 0.5  →  Close position
```

### Risks
- Execution risk: price changes between order and fill
- Model risk: model fails in changing market regimes
- Liquidity risk: cannot exit position immediately
- Regime change: market shifts from mean-reverting to trending

---

## 2. Pairs Trading & Cointegration

### What is Pairs Trading?
Find two assets with a historical relationship, then trade the price difference (spread) when the relationship breaks down.

### Pairs Trading vs Plain Correlation

| Metric | Correlation | Cointegration |
|--------|-------------|---------------|
| Measures | Direction of relationship | Long-run equilibrium |
| Volatility | High | Low |
| Stability | Unstable | Stable |
| Use case | Short-term | Long-term |

### Cointegration — Engle-Granger Two-Step Method

**Step 1: Regression**
```
Y_t = α + β × X_t + ε_t
```

**Step 2: ADF Test on Residuals**
```
Δε_t = γ × ε_{t-1} + Σδ_i × Δε_{t-i} + u_t
```
- H0: Series has unit root (NOT stationary)
- H1: Series is stationary / mean-reverting
- p-value < 0.05 → Reject H0 → Cointegrated pair

### Common Crypto Pairs
- BTC/USD — ETH/USD (high correlation ~0.85)
- COIN — GBTC (same underlying, different premium/discount)
- Binance BTC — Coinbase BTC (exchange arbitrage)

### Z-Score Calculation
```
β = Cov(R_A, R_B) / Var(R_B)
Spread = R_A − β × R_B
Z-Score = (Spread − μ_spread) / σ_spread
```

### Entry/Exit Parameters
- Lookback period: 60–120 days
- Entry threshold: Z-Score > 2.0 or < −2.0
- Exit threshold: Z-Score approaches 0
- Half-life of spread: T = −ln(2) / λ (from Ornstein-Uhlenbeck equation)

### Half-Life Formula
```python
# Ornstein-Uhlenbeck half-life estimation
# ในกรณีที่ spread เบี่ยงเบนไป ค่า half-life บอกว่ากี่วัน spread จะกลับสู่ mean
import numpy as np
from scipy import stats

def half_life(spread):
    # Lag the spread and run regression: spread_t = λ * spread_{t-1} + error
    lagged = spread[:-1]
    current = spread[1:]
    slope, intercept, r_value, p_value, std_err = stats.linregress(lagged, current)
    lambda_param = slope - 1  # ค่า λ จาก OU process
    if lambda_param >= 0:
        return -1  # ไม่ mean-reverting
    return -np.log(2) / lambda_param  # จำนวน periods ที่ spread กลับคืนครึ่งหนึ่ง
```

---

## 3. Market Making

### What is a Market Maker?
A market maker continuously posts both bid and ask orders, profiting from the spread while providing liquidity to the market.

### Revenue Sources
1. **Spread profit**: Buy at bid, sell at ask
2. **Inventory gains**: Price movement in favor of held inventory
3. ** Adverse selection avoidance**: Avoiding trading with informed traders

### Avellaneda-Stoikov Model (2008)

The seminal academic market-making model:

```
Setup:
- σ = asset volatility
- T = time until trading session ends
- γ = risk aversion parameter
- κ = order arrival rate parameter

Optimal bid-ask spread (simplified):
Δ = γ × σ² × (T − t) + (1/γ) × ln(1 + γ/κ)

Reservation price (fair value):
r = s − σ² × (T − t) × γ / 2
```

### Key Parameters
- **Spread width**: Wider when volatility is high, when inventory is skewed
- **Inventory management**: Keep inventory balanced; avoid one-sided exposure
- **Adverse selection**: Thin out orders when informed trading detected (large order flow imbalance)

### Inventory Risk Formula
```python
# คำนวณ inventory risk — ถ้าถือ position นานเกินไป
# inventory risk จะเพิ่มขึ้นตาม variance ของ price movement
inventory_risk = position_size * price_volatility * np.sqrt(time_held)
```

---

## 4. Momentum vs Mean Reversion in Crypto

### The Debate
- **Momentum**: Assets that have gone up tend to continue going up (trend-following)
- **Mean Reversion**: Assets that are extended tend to pull back

### Crypto-Specific Evidence

| Market Condition | Better Strategy | Evidence |
|-----------------|-----------------|----------|
| Strong trend (ADX > 40) | Momentum | Trend continuation 60–70% in BTC |
| Ranging / low vol | Mean Reversion | RSI extremes work 55–60% |
| Post-crash recovery | Mean Reversion | Sharp bounce after -20% days |
| Post-rally pause | Momentum | Continuation 3–5 days after +10% |

### Combined Approach (Regime Detection)
```python
# ตรวจจับ regime ด้วย ADX + Volatility
import numpy as np

def detect_regime(prices, adx_period=14):
    # คำนวณ ADX แบบง่าย (ใช้ std แทน True Range)
    returns = np.diff(prices) / prices[:-1]
    plus_dm = np.maximum(returns, 0)
    minus_dm = np.maximum(-returns, 0)
    
    # Simplified ADX
    adx = abs(plus_dm.mean() - minus_dm.mean()) / (abs(plus_dm.mean()) + abs(minus_dm.mean()))
    
    if adx > 0.3:
        return "TRENDING"  # → momentum
    elif adx < 0.15:
        return "RANGING"  # → mean reversion
    else:
        return "NEUTRAL"  # → combined signals
```

---

## 5. Cross-Asset Correlations

### Key Crypto Correlations

| Pair | 30-day Corr | 90-day Corr | Notes |
|------|------------|-------------|-------|
| BTC — ETH | 0.85 | 0.80 | High, stable |
| BTC — Gold | 0.15 | 0.25 | Low, conditional |
| BTC — SPX | −0.10 | 0.05 | Near zero; "digital gold" narrative |
| BTC — DXY | −0.30 | −0.20 | Weak negative (USD up → BTC down) |
| ETH — Gold | 0.10 | 0.15 | Very low |
| BTC — USDC | −0.05 | −0.08 | Near zero |

### Practical Use
- BTC-ETH correlation spike (> 0.95) often precedes trend reversals
- Low BTC-Gold correlation breaks down during systemic crises (COVID 2020, FTX 2022)
- Negative BTC-DXY correlation used as USD strength signal

---

## 6. Orderbook Analysis & Execution

### Key Orderbook Metrics

**1. Bid-Ask Spread**
```
Spread = Ask_Price − Bid_Price
Spread (bps) = (Ask − Bid) / Mid_Price × 10,000
```
- Normal BTC: 1–10 bps; during volatility: 50–200 bps
- Wide spread = high transaction cost for market orders

**2. Order Flow Imbalance (OBI)**
```
OBI = (Bid_Volume − Ask_Volume) / (Bid_Volume + Ask_Volume)
```
- OBI > 0.2 → buying pressure → short-term bullish
- OBI < −0.2 → selling pressure → short-term bearish
- Useful for intraday direction signals

**3. Depth Imbalance**
```python
# คำนวณ depth imbalance ที่ระดับราคาต่างๆ
def depth_imbalance(orderbook, levels=10):
    bid_vol = sum(orderbook['bids'][:levels])
    ask_vol = sum(orderbook['asks'][:levels])
    return (bid_vol - ask_vol) / (bid_vol + ask_vol)
```

### VWAP (Volume Weighted Average Price)
```
VWAP = Σ(Price × Volume) / Σ(Volume)
```
- Used as execution benchmark: better than VWAP = good execution
- Strategy: buy below VWAP = institutional buying behavior

### TWAP (Time Weighted Average Price)
```
TWAP = Σ(Price_i) / N  (equally weighted over time slices)
```
- Used for large orders that would move the market
- Break large order into smaller chunks over time

### Execution Strategies

**1. VWAP Algorithm**
- Divide large order into time slices proportional to expected volume distribution
- Expected intraday volume pattern: U-shaped (high at open and close)

**2. Implementation Shortfall**
```
IS = (Execution_Price − Decision_Price) × Direction × Size
```
- Measures cost of delay between decision and execution
- IS = 0 if executed at decision price

**3. Liquidity-Seeking**
- Dark pools, midpoint orders
- Only execute when spread is tight

---

## 7. HFT Concepts for Retail

### What Retail Can Learn from HFT

**1. Co-location**: HFT firms place servers near exchange matching engines
- Retail equivalent: use VPS in same region as exchange API

**2. Latency Components (total round-trip)**
```
Total Latency = Network + Gateway + Matching + Release
             ≈ 0.1ms + 0.5ms + 0.1ms + 0.1ms = ~0.8ms (co-located)
             ≈ 50–200ms (retail via internet)
```

**3. Order Types for Retail**
- **IOC (Immediate or Cancel)**: Fill as much as possible, cancel rest
- **FOK (Fill or Kill)**: All-or-nothing execution
- **Post-only**: Only add liquidity, not take — avoids taker fees

**4. What Retail CANNOT Do**
- Pure latency arbitrage (requires < 1ms)
- Cross-exchange arbitrage at scale
- High-frequency market making (inventory risk too high at retail scale)

### Practical Retail HFT-Inspired Strategies
- Use **IOC orders** to minimize adverse selection
- Monitor **OBI** for intraday directional signals
- Provide liquidity via **post-only limit orders** to earn maker rebates
- Split large orders using **TWAP** to minimize market impact

---

## Related Concepts

- [[trading-strategies]] — Basic strategies (trend-following, breakout, mean reversion)
- [[technical-indicators]] — RSI, MACD, Bollinger Bands, ADX
- [[chart-patterns]] — Breakout levels, support/resistance
- [[risk-management]] — Position sizing, stop-loss
- [[ai-ml-trading]] — ML approaches to strategy discovery
