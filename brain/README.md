# Auto Trade AI — Project Brain

Project knowledge base maintained with Claude Code. Thai-English bilingual — wiki in English, สมุด in Thai.

## Structure

```
brain/
├── raw/              ← source documents (immutable)
├── wiki/             ← Claude-maintained knowledge base (English)
│   ├── index.md      ← catalog of all pages
│   ├── log.md        ← append-only operation log
│   ├── overview.md   ← high-level synthesis
│   ├── entities/     ← people, orgs, products
│   ├── concepts/     ← ideas and topics
│   ├── sources/      ← one summary per ingested source
│   └── projects/     ← codebase and tool documentation
└── สมุด/             ← human notes in Thai
    ├── index.md
    ├── concepts/
    └── projects/
```

## Setup

```bash
# Open as Obsidian vault
obsidian "/Users/chinnawat/auto-trade-ai/brain"
```

## Workflow

Managed via `CLAUDE.md` — covers INGEST, PROJECT, QUERY, SYNC, and LINT workflows.

## Project

- **auto-trade-ai** — AI-powered trading system with crypto, gold, and stock modules
