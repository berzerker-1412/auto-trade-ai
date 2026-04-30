---
title: "playwright-skill — Claude Code Skill for Playwright Browser Automation"
type: source
tags: [claude-code, playwright, browser-automation, skills, testing]
sources: 1
created: 2026-04-14 00:00
updated: 2026-04-14 00:00
---

A [[claude-setup/index|Claude Code]] skill by lackeyjb that lets Claude write and execute [[playwright|Playwright]] automation on the fly — no pre-built scripts, custom code for every request.

## Key Claims

- Claude autonomously decides when to invoke the skill based on the user's browser task description.
- Implements the open [agentskills.io](https://agentskills.io/) spec — compatible with other agent platforms, not just Claude Code.
- Default config: `headless: false`, 100ms slow-motion, 30s timeout, screenshots to `/tmp/`. Browser is intentionally visible so the user can watch automation happen in real time.
- `run.js` (universal executor) handles module resolution, eliminating the "module not found" errors that occur when Claude generates standalone Playwright scripts.
- `API_REFERENCE.md` covers selectors, network interception, auth, visual regression, mobile emulation, and performance testing — loaded only when Claude needs it.

## Progressive Disclosure Pattern

> The skill uses a minimal SKILL.md for day-to-day invocations and defers full API documentation to a separate file loaded on demand.

This keeps the skill's baseline context footprint small while retaining access to comprehensive docs. A pattern worth copying for any skill with a large reference surface.

## Install Modes

| Mode | Method |
| --- | --- |
| Plugin (recommended) | `/plugin marketplace add lackeyjb/playwright-skill` then `npm run setup` |
| Standalone global | Clone → copy `skills/playwright-skill/` to `~/.claude/skills/` → `npm run setup` |
| Standalone project | Same, but copy to `.claude/skills/` in project root |

The plugin format uses a nested `skills/` directory; standalone installation extracts only the inner skill folder.

## Connections

- Extends [[claude-setup/skills]] with a third-party browser automation capability.
- The Progressive Disclosure pattern is independently useful — applicable to any Claude skill with large reference docs.
- Visible-browser-by-default is an unusual but pragmatic default that prioritizes human observability over speed.
