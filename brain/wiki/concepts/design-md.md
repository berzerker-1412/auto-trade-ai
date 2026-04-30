---
title: DESIGN.md
type: concept
tags: [design-systems, ai-agents, ui-generation, context-injection, prompt-engineering]
sources: 1
created: 2026-04-14 00:00
updated: 2026-04-14 00:00
---

A plain-text design system document structured for AI agents to read. Introduced by [[google-stitch|Google Stitch]]. Drop one into a project root and any AI coding agent generates UI consistent with the defined visual language — no Figma exports, no JSON schemas, no tooling required.

## How It Works

The file lives at the project root alongside `AGENTS.md` and `CLAUDE.md`. The agent reads it before generating any UI.

| File | Reader | Domain |
| --- | --- | --- |
| `AGENTS.md` | Coding agents | Build process, conventions |
| `CLAUDE.md` | Claude Code | Behavior within the project |
| `SOUL.md` | Agent identity systems | Personality, values |
| `DESIGN.md` | Design agents | Visual language, UI patterns |

## Standard Sections (Stitch format)

| # | Section | What it captures |
| --- | --- | --- |
| 1 | Visual Theme & Atmosphere | Mood, density, design philosophy |
| 2 | Color Palette & Roles | Semantic name + hex + functional role |
| 3 | Typography Rules | Font families, full hierarchy table |
| 4 | Component Stylings | Buttons, cards, inputs, nav with states |
| 5 | Layout Principles | Spacing scale, grid, whitespace philosophy |
| 6 | Depth & Elevation | Shadow system, surface hierarchy |
| 7 | Do's and Don'ts | Design guardrails and anti-patterns |
| 8 | Responsive Behavior | Breakpoints, touch targets, collapsing strategy |
| 9 | Agent Prompt Guide | Quick color reference, ready-to-use prompts |

Section 9 (Agent Prompt Guide) is notable — the file ships with pre-written prompts for common UI generation tasks, essentially bootstrapping the human↔agent conversation.

## Relation to [[soul-md|SOUL.md]] Pattern

DESIGN.md is the UI-domain instance of the broader **plain-text context injection** pattern:

- Separates design intent from code — change the visual system by editing a markdown file, not component source.
- Version-controllable and diff-readable.
- Portable: any agent that can read markdown can use it.
- Human-readable: designers can review and edit without engineering tools.

The pattern is: *give the agent a persistent, domain-specific context file in markdown, and the agent internalizes it without prompt engineering on every request.*

## Practical Use

The [[awesome-design-md]] repo provides 50+ ready-to-use DESIGN.md files extracted from real websites (Vercel, Linear, Notion, Stripe, Apple, etc.).

Usage:

1. Copy a site's `DESIGN.md` into project root.
2. Tell the agent: "Build a page that matches this design system."

Each file in the repo also ships with `preview.html` and `preview-dark.html` — visual catalogs showing color swatches, type scales, button states, and card components.
