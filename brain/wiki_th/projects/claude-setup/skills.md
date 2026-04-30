# Claude Code Setup — Skills

## สรุปสั้นๆ

Skills คือ slash commands custom ที่อยู่ใน `~/.claude/skills/` เรียกใช้ด้วย `/skill-name`

## Skills ที่มี

### `/gemini` — Research & Summarize
ใช้ Gemini CLI แทน Claude สำหรับงานที่ output ยาวหรือ input ใหญ่ — ประหยัด token

| Command | ใช้ทำอะไร |
| --- | --- |
| `/gemini research <topic>` | research สรุป topic |
| `/gemini summarize <file>` | สรุปไฟล์ยาว |
| `/gemini read <file> <question>` | อ่านไฟล์แล้วตอบคำถาม |

### `/review` — Code Review
spawn reviewer agent แยก session — ได้ second opinion จริงๆ ไม่ใช่ตัวเดิม

### `/translate` — Thai ↔ English
ใช้ Gemini 2.5 Flash แปลข้อความยาว (500+ คำ) — สั้นกว่านั้นแปลตรงได้เลย

### `/playwright-research` — JS-rendered Pages
fallback อัตโนมัติไปใช้ Playwright เมื่อ WebFetch ได้ content น้อยกว่า 500 chars หรือเจอ `<script>` เยอะ

## เชื่อมกับอะไร

- hooks → `claude-setup/hooks`
- aliases → `claude-setup/aliases`
