---
title: Claude Code Setup — Hooks
type: project
tags: [claude, hooks, gemini, automation]
created: 2026-04-12
updated: 2026-04-13
---

See overview at [[claude-setup/index|Claude Code Setup]].

Hooks are shell scripts that run automatically when events occur in Claude Code. Configured in `settings.json`.

---

## Hook: Auto-Translate Prompt

**File:** `.claude/hooks/gemini-translate-prompt.sh` (project-local)
**Event:** `UserPromptSubmit` — fires on every prompt submission

### How It Works

```text
User types a prompt (in Thai)
    ↓
Hook receives JSON input from stdin
    ↓
Extracts user_prompt field
    ↓
Sends to Gemini 2.5 Flash: "Translate to English"
    ↓
Returns systemMessage:
  "[Prompt Translation by Gemini]
   Original: <original text>
   English: <translation>"
    ↓
Claude sees both languages simultaneously
```

### Effect

Claude better understands the intent of Thai prompts because the context includes both the original and an English translation.

### Edge Cases

- If translation fails → skip (hook exits 0, no systemMessage)
- If translation matches original (prompt already in English) → skip
- Timeout: 30 seconds

### Config in settings.json

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "'/Users/chinnawat/Desktop/Brain/2nd Brain/.claude/hooks/gemini-translate-prompt.sh'",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```
