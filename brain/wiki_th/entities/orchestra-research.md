# Orchestra Research — ห้องสมุด AI Research Skills

## สรุปสั้นๆ

Orchestra Research คือองค์กรวิจัย AI ที่สร้าง open-source library ชื่อ "AI Research Skills Library" รวม 87 skills ที่ให้ AI agent ทำ ML research แบบ end-to-end ได้เองตั้งแต่ต้นจนจบ จุดเด่นคือ install ครั้งเดียวได้เลย ใช้กับ coding agent หลักๆ ทุกตัว

## สิ่งที่น่าสนใจ / จุดสำคัญ

- **87 skills** ครอบคลุม ML research pipeline ครบ — ตั้งแต่ idea จนถึง paper
- **ติดตั้งง่ายมาก:** `npm install @orchestra-research/ai-research-skills` แล้ว sync skills เข้า project
- รองรับ coding agents หลัก: Claude Code, Gemini CLI, Cursor, OpenCode, Hermes Agent
- sync ผ่าน `orchestra-research.com` — เลือก skill ที่ต้องการ add ได้ทีละตัว

**ทำไมน่าสนใจ?** แนวคิดนี้ตรงกับ pattern ที่ดีมากของ AI workflow: แทนที่จะให้ agent รู้ทุกอย่าง ให้มี specialized skills ที่โหลดเฉพาะเมื่อต้องการ คล้ายกับ MCP tools แต่ packaging เป็น skill library สำหรับ research โดยเฉพาะ

## เชื่อมกับอะไร

- [AI Research Skills Library](ai-research-skills.md) — รายละเอียดของ library
- [Claude Code Setup](../projects/claude-setup.md) — pattern ของ skills ใน Claude Code workflow
- [SOUL.md](soul-md.md) / [DESIGN.md](design-md.md) — concept ที่คล้ายกัน: ให้ AI มีบริบทที่ถูกต้องผ่านไฟล์ที่เตรียมไว้ล่วงหน้า

## คำถามที่ยังค้างอยู่

- 87 skills ครอบคลุม research pipeline ไหนบ้าง — มี taxonomy ไหม
- quality ของ skills ดีแค่ไหน — community-contributed หรือ curated
- ต่างจาก MCP tools ยังไงในทางปฏิบัติ
