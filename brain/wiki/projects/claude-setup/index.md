---
title: Claude Code Setup
type: project
tags: [claude, tools, hooks, skills, gemini, workflow]
created: 2026-04-12
updated: 2026-04-13
---

Configuration and tools installed under `~/.claude/` for the Claude Code CLI.

---

## Directory Layout

```text
~/.claude/
├── CLAUDE.md           — global instructions for all projects
├── settings.json       — model + hooks config
├── projects/           — conversation history per project
├── sessions/           — current session data
├── hooks/              — shell scripts triggered automatically
├── skills/             — custom skills (gemini, review, translate)
├── plans/              — plan files
└── memory/             — auto-memory across sessions
```

---

## Projects Claude Tracks

| Folder Key | Project |
| --- | --- |
| `-Users-chinnawat` | home directory |
| `-Users-chinnawat-Desktop-Brain-2nd-Brain` | this wiki |
| `-Users-chinnawat-gemini-web` | gemini web project |
| `-Users-chinnawat-projects-mymoney` | [[mymoney/index\|MyMoney app]] |

---

## Knowledge Pages

- [[claude-setup/skills|Skills]] — /gemini, /review, /translate
- [[claude-setup/hooks|Hooks]] — auto-translate prompt hook
- [[claude-setup/aliases|Aliases]] — shell aliases for quick project switching
