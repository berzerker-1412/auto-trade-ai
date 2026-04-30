# Claude Code Setup — Hooks

## สรุปสั้นๆ

Hooks คือ shell script ที่รันอัตโนมัติเมื่อเกิด event ใน Claude Code ตั้งค่าผ่าน `settings.json` hook หลักที่ใช้อยู่: auto-translate prompt ไทย → อังกฤษ ผ่าน Gemini ก่อนส่งให้ Claude เห็น

---

## สิ่งที่น่าสนใจ / จุดสำคัญ

### Hook: Auto-Translate Prompt (UserPromptSubmit)

**File:** `.claude/hooks/gemini-translate-prompt.sh` (อยู่ใน project-local ของ 2nd Brain)

**Event:** `UserPromptSubmit` — ทำงานทุกครั้งที่ submit prompt

**Flow:**

```
User พิมพ์ prompt (ไทย)
  ↓
Hook รับ JSON จาก stdin
  ↓
ดึง user_prompt field
  ↓
ส่งให้ Gemini 2.5 Flash: "Translate to English"
  ↓
Return systemMessage:
  "[Prompt Translation by Gemini]
   Original: <ต้นฉบับ>
   English: <แปลแล้ว>"
  ↓
Claude เห็นทั้ง 2 ภาษาพร้อมกัน
```

**ทำไมถึงดี:**
Claude เข้าใจ intent ของ prompt ไทยได้ดีขึ้นเพราะเห็น translation คู่กัน ลดโอกาสตีความผิด

**Edge cases:**
- translate fail → hook exit 0 (skip silently)
- prompt เป็นอังกฤษอยู่แล้ว → skip (translation = original)
- timeout: 30 วินาที

### Config ใน settings.json

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

Hook นี้อยู่ใน **project-local settings** ของ 2nd Brain ไม่ใช่ global `~/.claude/settings.json`

### สถานะปัจจุบัน (อัปเดต)

- UserPromptSubmit hook: ทำงานแล้ว
- FileChanged hook: ยังไม่ทำงาน — ต้อง debug
- global hook ใน `~/.claude/settings.json`: ยังมีซ้ำกับ project-local — ควรลบ global ออก

---

## เชื่อมกับอะไร

- [Claude Code Setup](claude-setup.md) — overview
- [Claude Setup Aliases](claude-setup-aliases.md) — alias + CLAUDE.md per project
- [Claude Setup Skills](claude-setup.md) — skills `/gemini`, `/review`, `/translate`, `/playwright-research`

---

## คำถามที่ยังค้างอยู่

- FileChanged hook ไม่ทำงาน — event name ผิด หรือ format JSON ผิด?
- global hook กับ project-local hook ชนกัน — run ซ้ำไหม หรือ project-local override?
- สามารถเขียน hook หลายตัวใน UserPromptSubmit ได้ไหม? หรือต้อง chain ใน script เดียว?
