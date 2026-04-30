# Claude Code Setup

## สรุปสั้นๆ

config และ tools ที่ติดตั้งไว้ใน `~/.claude/` สำหรับ Claude Code CLI มี hook, skills, และ alias ที่ช่วยให้ทำงานได้เร็วขึ้น

## Skills ที่มี

- `/gemini` — ส่งงาน token-heavy ไปให้ Gemini CLI ทำแทน เช่น summarize ไฟล์ยาว หรือ research topic
- `/review` — spawn reviewer agent แยก session ไม่ bias จาก context ปัจจุบัน ประเมิน 6 มิติ
- `/translate` — แปล Thai↔English ผ่าน Gemini 2.5 Flash เหมาะสำหรับข้อความยาว
- `/playwright-research` — research หัวข้อหรือ URL จากเว็บ โดย fallback ไป Playwright อัตโนมัติถ้า WebFetch ได้ content น้อย (JS-rendered pages)

## Hook ที่ใช้งานอยู่

UserPromptSubmit hook auto-translate prompt ไทย → อังกฤษ ผ่าน Gemini ก่อนส่งให้ Claude เห็น ทำให้ Claude เข้าใจ intent ดีขึ้น hook อยู่ที่ project-local `.claude/hooks/` ไม่ใช่ global

## เชื่อมกับอะไร

- wiki นี้ใช้ hook นี้ทุก session
- CLAUDE.md ของ project คือ "soul" ของ Claude ในแต่ละ project — เหมือน SOUL.md pattern ของ OpenClaw

## คำถามที่ยังค้างอยู่

- FileChanged hook ยังไม่ทำงาน — ยังต้อง debug อยู่
- global hook ใน `~/.claude/settings.json` ยังมีอยู่ซ้ำกับ project-local — ควรลบ global ออก
