---
title: Quantitative Systematic Trading
type: source
description: Research on advanced quantitative trading strategies
url: docs/quantitative-systematic-trading.md
tags: [stat-arb, pairs-trading, market-making, cointegration, vwap, twap]
created: 2026-05-01
---

## Summary

Comprehensive research covering:
- Statistical arbitrage and mean reversion strategies
- Pairs trading and cointegration (Engle-Granger, ADF test)
- Market making and Avellaneda-Stoikov model
- Orderbook analysis (OBI, depth imbalance)
- VWAP and TWAP execution algorithms
- Cross-asset correlations (BTC-ETH, BTC-Gold, BTC-SPX)
- HFT concepts adapted for retail traders
- Z-Score calculation and entry/exit rules
- Cryptocurrency-specific market microstructure

## Key Findings

1. **Cointegration > Correlation**: For long-term pairs trading, cointegration tests (ADF) are more reliable than simple correlation
2. **OBI as intraday signal**: Order Flow Imbalance > 0.2 predicts short-term direction with ~55% accuracy
3. **Half-life of mean reversion**: BTC-ETH spread typically reverts within 2-5 days (statistically)
4. **Market making requires inventory management**: Avellaneda-Stoikov shows optimal spread widens with volatility and time-to-expiry
5. **VWAP benchmark**: Executing below VWAP = good for buys; above VWAP = good for sells

## Related Concepts

- [[advanced-quantitative-strategies]] — Full concept page
- [[pairs-trading]] — Pairs trading deep dive
- [[orderbook-analysis]] — Orderbook metrics

## File Location

`docs/quantitative-systematic-trading.md`
