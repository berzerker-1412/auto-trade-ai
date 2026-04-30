# Wiki Log

**Active log — latest 15 entries only.** Older entries → `wiki/logs/YYYY-MM.md`

Append-only chronological record of all operations on this knowledge base.
Format: `## [YYYY-MM-DD HH:MM] <operation> | <title>`

---

## [2026-05-01 00:20] restructure | Restructured project layout

**Moved:**
- `brain/CLAUDE.md` + `brain/README.md` → project root (deleted duplicates from brain/)
- `src/` → `backend/` (trading system code)
- Created `skills/` → `~/.hermes/skills/` symlink at project root

**Updated:**
- `CLAUDE.md` (root) — directory layout updated to reflect new structure
- `README.md` (root) — structure diagram + backend/ paths

Updated `wiki/projects/auto-trade-ai/` pages to reference `backend/` instead of `src/`.

## [2026-05-01 00:15] restore | Restored non-EzyHR files from original 2nd Brain

Restored 33 files from original brain at `/Users/chinnawat/Desktop/Brain/2nd Brain/`, excluding all EzyHR-related files (concepts/ezyhr.md, entities/ezyhr.md, sources/ezyhr-support-docs.md).

**Restored to wiki/ (English):**
- concepts/: design-md, graphrag, multi-agent-simulation, obsidian-setup, soul-md, swarm-intelligence
- entities/: camel-ai, google-stitch, mirofish, oasis, openclaw, orchestra-research, playwright, voltagent, zep-cloud
- sources/: ai-research-skills, awesome-design-md, mirofish, playwright-skill
- projects/: bank-noti-tester (1), claude-setup (4), mymoney (4)
- entertainment/: manga/soul-eater (5 files), movie, music, novel, cartoon

**Restored to wiki_th/ (Thai):**
- concepts/: obsidian-setup, multi-agent-simulation, swarm-intelligence, design-md, soul-md
- entities/: orchestra-research, mirofish
- sources/: ai-research-skills, playwright-skill
- projects/: mymoney (4), bank-noti-tester (1), claude-setup (4), 50-frontend-projects (3)
- entertainment/: same as wiki/

Updated wiki/index.md and wiki_th/index.md with full catalog of all restored pages.

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
