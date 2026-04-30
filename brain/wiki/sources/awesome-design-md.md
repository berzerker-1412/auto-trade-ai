---
title: "awesome-design-md — Curated Collection of DESIGN.md Files"
type: source
tags: [design-systems, ai-agents, design-md, ui-generation, context-injection]
sources: 1
created: 2026-04-14 00:00
updated: 2026-04-14 00:00
---

A [[voltagent|VoltAgent]]-maintained repo of 50+ [[design-md|DESIGN.md]] files — each extracted from a real website's design system. Drop one into a project root and any AI coding agent generates UI that matches the target brand.

## Key Claims

- [[design-md|DESIGN.md]] is a format introduced by [[google-stitch|Google Stitch]]. It is a plain-text design system document specifically structured for AI agents to read.
- Analogy table from the source:

| File | Who reads it | What it defines |
| --- | --- | --- |
| `AGENTS.md` | Coding agents | How to build the project |
| `DESIGN.md` | Design agents | How the project should look and feel |

- Each file follows the Stitch DESIGN.md format with 9 sections (see [[design-md|DESIGN.md]] concept page for section breakdown).
- Every site ships three files: `DESIGN.md` (agent-readable), `preview.html`, and `preview-dark.html` (visual catalogs of the design system).
- MIT license — tokens are extracted from publicly visible CSS values; no copyright claimed over visual identity.

## Collection Coverage

55+ sites across 8 categories:

| Category | Examples |
| --- | --- |
| AI & LLM Platforms | Claude, Mistral AI, Ollama, ElevenLabs, xAI |
| Developer Tools | Cursor, Vercel, Raycast, Warp, Lovable |
| Backend/DevOps | Supabase, Sentry, PostHog, MongoDB, Stripe |
| Productivity & SaaS | Linear, Notion, Mintlify, Cal.com, Resend |
| Design & Creative | Figma, Framer, Miro, Webflow |
| Fintech & Crypto | Stripe, Revolut, Coinbase, Kraken |
| E-commerce & Retail | Shopify, Nike, Airbnb |
| Media & Consumer | Apple, Spotify, SpaceX, NVIDIA, Tesla |

## Notable Quotes

> "Markdown is the format LLMs read best, so there's nothing to parse or configure."

> "Copy a DESIGN.md into your project, tell your AI agent 'build me a page that looks like this' and get pixel-perfect UI that actually matches."

## Connections

- [[design-md|DESIGN.md]] is structurally the same pattern as [[soul-md|SOUL.md]] — a plain-text markdown file that injects domain-specific context into an agent.
- Practical use case for [[mymoney/index|MyMoney]]: copy a DESIGN.md (e.g., Linear or Notion) into the project root to guide Claude when building new screens.
- Suggests a broader trend: `*.md` context files are becoming the standard interface between humans and coding agents across all domains.
