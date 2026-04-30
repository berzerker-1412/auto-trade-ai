# AI Research Skills Library

## สรุปสั้นๆ

Orchestra Research สร้าง library รวม 87 skills สำหรับ AI agent ทำ ML research แบบ end-to-end — ตั้งแต่คิด idea, survey literature, รัน experiment, จนถึงเขียน paper เอง ติดตั้งได้ด้วย command เดียว: `npx @orchestra-research/ai-research-skills`

## สิ่งที่น่าสนใจ

- **Autoresearch skill** คือ meta-skill ที่ใช้ two-loop architecture — inner loop optimize, outer loop synthesize แล้ว route ไปยัง domain skills ที่เหมาะสมเอง เหมือนมี research director ที่รู้จักทุก tool แล้วเลือกใช้ให้เอง
- **Format เดียวกับที่เราเคยเจอ** — SKILL.md (50-150 lines quick ref) + references/ folder (300KB+ deep docs) นี่คือ progressive disclosure pattern เดียวกับ playwright-skill ที่เจอก่อนหน้า ecosystem กำลัง converge มาที่ format นี้
- **Demo ที่น่าตกใจ**: agent ไม่แค่รัน experiment — มัน refute hypothesis ตัวเองแล้ว pivot ไปหา finding ที่ดีกว่า (norm heterogeneity r=-0.99 ทำนาย LoRA brittleness ได้) นี่คือ research autonomy จริงๆ ไม่ใช่แค่ task execution
- **รองรับ Claude Code /loop** — autoresearch skill ทำงานกับ /loop ได้เลย คือรัน continuous research loop ได้โดยไม่ต้อง babysit

## เชื่อมกับอะไร

เป็น instance ขนาดใหญ่ของ pattern เดิมที่เราเห็นมาตลอด — **plain-text context injection** (SOUL.md, DESIGN.md, CLAUDE.md, SKILL.md) แต่ครั้งนี้มี 87 files และมี routing layer ที่เลือก context ที่จะ inject ตาม stage ของงาน

เชื่อมกับ OpenClaw ด้วย — autoresearch รองรับ OpenClaw heartbeat สำหรับ continuous operation

## คำถามที่ยังค้างอยู่

- Autoresearch skill handle context window limit ยังไงเวลา research loop ยาวมาก?
- มีใครใช้กับ non-ML research domain ได้ไหม? (เช่น software engineering research)
- Quality ของ paper ที่ agent เขียน — peer review ผ่านไหม หรือแค่ preprint?
