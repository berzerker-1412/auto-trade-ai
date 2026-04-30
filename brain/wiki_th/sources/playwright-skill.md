# playwright-skill — ให้ Claude เขียนและรัน Playwright เอง

## สรุปสั้นๆ

playwright-skill คือ Claude Code Skill ที่ทำให้ Claude เขียน Playwright automation code แบบ on-the-fly ได้เลย ไม่ต้องเตรียม script ไว้ก่อน — บอกว่าอยากทำอะไร Claude เขียน code ให้แล้วรันเลย

## สิ่งที่น่าสนใจ

- **Visible browser by default** — `headless: false` เป็น default ตั้งใจให้เห็น automation ทำงานจริง ต่างจาก testing tool ทั่วไปที่ headless เป็น default เพราะ speed-first — ตรงนี้ priority ต่างกัน: developer experience > speed
- **Progressive Disclosure** — SKILL.md สั้น ๆ ไว้ for day-to-day, โหลด API_REFERENCE.md เต็มๆ เฉพาะตอนที่ต้องการ — pattern นี้ประหยัด context window ได้มาก เอาไปใช้กับ skill อื่นได้เลย
- **run.js (universal executor)** — แก้ปัญหา module resolution ที่ Claude มักเจอตอนสร้าง Playwright script แบบ standalone — เป็น solution ง่ายๆ แต่สำคัญมาก
- **Cross-platform via agentskills.io** — ไม่ได้ lock-in Claude เท่านั้น ใช้กับ agent platform อื่นได้ด้วย

## วิธีติดตั้ง (standalone global)

```bash
git clone https://github.com/lackeyjb/playwright-skill.git /tmp/playwright-skill-temp
cp -r /tmp/playwright-skill-temp/skills/playwright-skill ~/.claude/skills/
cd ~/.claude/skills/playwright-skill && npm run setup
rm -rf /tmp/playwright-skill-temp
```

## เชื่อมกับอะไร

- ต่อขยาย Claude Code skills ที่มีอยู่แล้ว (gemini, review, translate)
- Progressive Disclosure pattern เอาไปใช้กับ skill ตัวอื่นได้เลยถ้า skill นั้นมี reference docs ใหญ่

## คำถามที่ยังค้างอยู่

- plugin marketplace ของ Claude Code ทำงานยังไง ตอนนี้มี marketplace อื่นไหมนอกจาก lackeyjb
- agentskills.io spec ครอบคลุมอะไรบ้าง — น่าดูว่า skill ของ Claude Code compatible ได้จริงแค่ไหน
