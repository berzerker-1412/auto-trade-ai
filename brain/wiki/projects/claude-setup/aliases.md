---
title: Claude Code Setup — Project Aliases
type: project
tags: [claude, alias, workflow, shell]
created: 2026-04-12
updated: 2026-04-13
---

See overview at [[claude-setup/index|Claude Code Setup]].

Shell aliases let you switch working directory and project context quickly without typing long paths.

---

## Setting Up Shell Aliases

Add to `~/.zshrc` (or `~/.bashrc`):

```bash
# Project aliases
alias mymoney='cd /Users/chinnawat/projects/mymoney'
alias banktest='cd /Users/chinnawat/projects/bank_noti_tester'
alias brain='cd /Users/chinnawat/Desktop/Brain/2nd\ Brain'

# Open Claude Code directly in that project
alias cc-mymoney='cd /Users/chinnawat/projects/mymoney && claude'
alias cc-brain='cd /Users/chinnawat/Desktop/Brain/2nd\ Brain && claude'
alias cc-banktest='cd /Users/chinnawat/projects/bank_noti_tester && claude'
```

Reload:

```bash
source ~/.zshrc
```

---

## Usage

```bash
# Navigate to project
mymoney        # → cd /Users/chinnawat/projects/mymoney

# Open Claude Code immediately in a project
cc-mymoney     # → cd ... && claude
cc-brain       # → open wiki session
```

---

## CLAUDE.md per Project

Each project should have a `CLAUDE.md` at its root so Claude knows the context when opening a new session.

| Project | CLAUDE.md |
| --- | --- |
| 2nd Brain | exists — schema + workflow instructions |
| mymoney | not yet — recommended to create |
| bank_noti_tester | not yet — may not be needed for such a small project |

### Sample CLAUDE.md for mymoney

```markdown
# MyMoney — Claude Instructions

Flutter personal finance app. Source at `/Users/chinnawat/projects/mymoney`.

## Stack
- Flutter 3.x / Dart 3.2+, Provider, SQLite, ML Kit

## Conventions
- State: ChangeNotifier providers in lib/providers/
- DB: DatabaseService singleton (lib/services/database_service.dart)
- All models have toMap()/fromMap() for SQLite

## Before coding
1. Read lib/models/ to understand data structure
2. Read the relevant provider before touching UI
```

---

## `--add-dir` (Multi-project Context)

Open Claude with references to multiple projects:

```bash
claude --add-dir /Users/chinnawat/projects/bank_noti_tester
```

Use when you need Claude to see `bank_noti_tester` while working in `mymoney` — e.g., when fixing the notification pipeline that requires context from both projects.
