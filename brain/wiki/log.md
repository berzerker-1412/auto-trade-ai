# Wiki Log

**Active log — latest 15 entries only.** Older entries → `wiki/logs/YYYY-MM.md`

Append-only chronological record of all operations on this knowledge base.
Format: `## [YYYY-MM-DD HH:MM] <operation> | <title>`

---

## [2026-04-30 23:35] project | auto-trade-ai — Full codebase documentation

Explored full codebase. Created 4 wiki pages:
- `wiki/projects/auto-trade-ai/index.md` — main project page with objective (make profit), tech stack, directory structure, trading flow, risk management rules
- `wiki/projects/auto-trade-ai/architecture.md` — system architecture diagram, all module breakdowns (AI Signal Generator, CCXT Crypto Exchange, Gold Price Feed, Paper Trader, Trade Logger), data flow signal→trade→P&L, frontend architecture
- `wiki/projects/auto-trade-ai/data-models.md` — all dataclasses (TradeSignal, Trade, TradeResult), enums, SQLite schema, P&L calculation, market data shapes
- `wiki/projects/auto-trade-ai/risk-management.md` — position sizing formula, SL/TP calculation for BUY/SELL, risk-of-ruin math, balance update logic, key metrics

## [2026-04-30 23:55] ingest | Technical Analysis Deep Dive — Knowledge base integration

Integrated `docs/technical-analysis-deep-dive.md` (2,612 lines, Thai) into brain knowledge base.

**Actions taken:**
1. Copied raw doc to `brain/raw/technical-analysis-deep-dive.md`
2. Created `wiki/sources/ta-deep-dive.md` — structured source summary page
3. Created 7 concept wiki pages:
   - `wiki/concepts/candlestick-patterns.md` — 23+ patterns, Python recognition code, context rules
   - `wiki/concepts/chart-patterns.md` — H&S, Double Top/Bottom, Triangles, Flags, Wedges, Rectangles
   - `wiki/concepts/technical-indicators.md` — RSI, MACD, Bollinger, ATR, ADX, Stochastic, OBV, VWAP with Python code
   - `wiki/concepts/market-theories.md` — Dow Theory, Elliott Wave, Wyckoff Method
   - `wiki/concepts/trading-strategies.md` — Trend-following, Breakout, Mean Reversion, Multi-TF, Paradox
   - `wiki/concepts/ai-ml-trading.md` — LSTM, RL, Sentiment Analysis, Feature Engineering
4. Updated `wiki/projects/auto-trade-ai/risk-management.md` — added position sizing, ATR sizing, Kelly Criterion, stop-loss strategies
5. Updated `wiki/index.md` — added all new concept and source pages
6. Updated `wiki/overview.md` — added knowledge base structure
7. Created 5 สมุด counterparts:
   - `สมุด/sources/ta-deep-dive.md` — Thai summary of TA Deep Dive
   - `สมุด/concepts/candlestick-patterns.md`
   - `สมุด/concepts/chart-patterns.md`
   - `สมุด/concepts/technical-indicators.md`
   - `สมุด/concepts/ai-ml-trading.md`
8. Updated `สมุด/index.md` — added all new pages
9. Appended to `wiki/log.md`

**Key findings from source:**
- 23+ candlestick patterns documented with ASCII diagrams
- Wyckoff Method particularly practical for institutional flow detection
- ADX < 20 = ranging market = don't use trend indicators
- ATR-based stops are the most adaptive risk management approach

## [2026-04-30 23:32] update | Brain initialized

Initialized 2nd Brain structure for auto-trade-ai project. Created directory layout: wiki/, wiki_th/, raw/assets/. Created CLAUDE.md, README.md, wiki/index.md, wiki/log.md, wiki/overview.md, wiki/projects/auto-trade-ai/index.md. Synced to wiki_th/ counterparts.
