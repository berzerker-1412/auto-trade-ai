---
title: SOUL.md
type: concept
tags: [agent, identity, prompt-engineering, context-injection]
sources: 3
created: 2026-04-13
updated: 2026-04-14
---

A pattern for giving an AI agent a persistent identity via a text file that is automatically injected into every conversation. More broadly, the **plain-text context injection** pattern — a domain-specific markdown file that shapes agent behavior without prompt engineering on every request.

## Concept

SOUL.md stores the agent's "self" — personality, values, working style, constraints — that the agent upholds across all sessions. Unlike a typical system prompt, it is a permanent, editable file that can be modified without touching code.

Originated in [[OpenClaw]], which injects this file set into the agent workspace:

- `AGENTS.md` — operational instructions
- **`SOUL.md`** — agent identity
- `TOOLS.md` — available tools

## The Broader Pattern

SOUL.md is one instance of a pattern appearing across the agent ecosystem: *give the agent a domain-specific context file in markdown, and the agent internalizes it persistently.*

| File | Reader | Domain |
| --- | --- | --- |
| `SOUL.md` (OpenClaw) | Agent runtime | Identity, personality, values |
| `CLAUDE.md` (Claude Code) | Claude | Behavior within a project |
| `SKILL.md` | Claude (on demand) | Domain knowledge for a skill |
| `AGENTS.md` | Coding agents | Build process, conventions |
| `DESIGN.md` | Design agents | Visual language, UI patterns |
| `SKILL.md` × 87 ([[ai-research-skills\|AI Research Skills Library]]) | Any coding agent | Full ML research lifecycle — training, eval, inference, RAG, etc. |

See [[design-md|DESIGN.md]] for the UI-domain instance of this pattern, introduced by [[google-stitch|Google Stitch]].

The `CLAUDE.md` of this project serves the same role as SOUL.md — it is the "soul" of this wiki that tells Claude how to operate.

## Benefits

- Separates domain context from code — change agent behavior by editing a text file.
- Persistent across all sessions without repetition.
- Version-controllable with git.
- Human-readable: any stakeholder can review and edit without engineering tools.
- Portable: any agent that reads markdown can consume it.
