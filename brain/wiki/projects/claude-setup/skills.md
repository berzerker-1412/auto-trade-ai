---
title: Claude Code Setup — Skills
type: project
tags: [claude, skills, gemini, review, translate, playwright]
created: 2026-04-12
updated: 2026-04-14
---

See overview at [[claude-setup/index|Claude Code Setup]].

Custom skills in `~/.claude/skills/`, invoked with `/skill-name`.

---

## `/gemini` — Gemini Research & Summarize

Uses the Gemini CLI to handle token-heavy tasks instead of Claude — saves tokens and is faster for long-output work.

**When to use:** output 500+ words, multiple input files, large logs.

| Command | Purpose |
| --- | --- |
| `/gemini research <topic>` | research and summarize a topic |
| `/gemini summarize <file>` | summarize long content |
| `/gemini read <file> <question>` | read a file and answer a question |
| `/gemini index <directory>` | create/update INDEX.md |
| `/gemini <any prompt>` | ad-hoc tasks |

**Wiki workflow use:** ingest long raw sources, fill in stub concept pages.

---

## `/review` — Code Review

Spawns a reviewer agent in a separate session — reviews code without bias from current context.

| Command | Purpose |
| --- | --- |
| `/review` | review current git diff (staged + unstaged) |
| `/review <file>` | review a specific file |
| `/review <file1> <file2>` | review multiple files |
| `/review pr` | review all commits on branch vs main |

**Evaluates 6 dimensions:** correctness, security, performance, readability, error handling, edge cases.

**Output:** APPROVE / REQUEST CHANGES / NEEDS DISCUSSION with file:line references.

**Use with:** [[mymoney/index|MyMoney]] before committing new features.

---

## `/translate` — Thai↔English via Gemini

Translates text using Gemini 2.5 Flash — suitable for 500+ word texts.
For short text, Claude translates directly without invoking the skill.

| Direction | Method |
| --- | --- |
| EN → TH | `~/.local/bin/translate-th` |
| TH → EN | `~/.local/bin/translate-en` |

**Wiki workflow use:** translate English raw sources before ingest.

---

## `/playwright-research` — Web Research with Playwright Fallback

Research any topic from the web. Uses `WebFetch` first — automatically falls back to Playwright to render JavaScript-heavy pages when WebFetch returns sparse or empty content.

**Location:** `~/.claude/skills/playwright-research/SKILL.md`

| Command | Purpose |
| --- | --- |
| `/playwright-research <topic>` | research a topic, auto-fallback for JS pages |
| `/playwright-research <url>` | fetch a specific URL with Playwright fallback |
| `/playwright-research <url> <question>` | fetch URL and answer a specific question |

**Flow:**

1. `WebSearch` to find relevant URLs (if topic, not URL)
2. `WebFetch` each URL
3. If content < ~500 chars or mostly `<script>` tags → fall back to Playwright
4. Playwright runs headless Chromium via `node -e "require('playwright')"` with `waitUntil: 'networkidle'` + 2s extra wait
5. Extracts `article/main/[role="main"]` before falling back to full `body.innerText`, truncated to 8000 chars

**Playwright dependency:** Uses `playwright` npm package. If not installed, skill installs to `/tmp/node_modules/playwright` automatically.

**Always reports** which method was used per source (WebFetch or Playwright).

---

## Notable Third-Party Skills

### `playwright-skill` — Browser Automation

Source: [[playwright-skill|playwright-skill source page]]

Claude writes and executes custom [[playwright|Playwright]] automation on the fly for any browser task — testing, screenshots, form interaction, broken link checks.

**Install (global standalone):**

```bash
git clone https://github.com/lackeyjb/playwright-skill.git /tmp/playwright-skill-temp
cp -r /tmp/playwright-skill-temp/skills/playwright-skill ~/.claude/skills/
cd ~/.claude/skills/playwright-skill && npm run setup
rm -rf /tmp/playwright-skill-temp
```

**Or via plugin marketplace:**

```text
/plugin marketplace add lackeyjb/playwright-skill
/plugin install playwright-skill@playwright-skill
```

**Key defaults:** headless: false (visible browser), 100ms slow-motion, 30s timeout.

**Pattern worth noting:** uses Progressive Disclosure — `SKILL.md` is concise, full `API_REFERENCE.md` loaded only when needed.
