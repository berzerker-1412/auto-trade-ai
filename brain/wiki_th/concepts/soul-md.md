# SOUL.md — ให้ตัวตนกับ AI agent

## สรุปสั้นๆ

SOUL.md คือไฟล์ข้อความที่ inject เข้า agent ทุก session อัตโนมัติ เหมือนกับว่า agent มี "ตัวตน" ถาวรที่จำได้ข้ามทุก conversation โดยไม่ต้องแตะ code

มาจาก OpenClaw — personal AI assistant ที่รันบนเครื่องตัวเอง

## สิ่งที่น่าสนใจ

- แยก identity ออกจาก code — แก้ personality ของ agent แค่แก้ไฟล์ข้อความ ไม่ต้อง deploy ใหม่
- version control ได้ด้วย git — ย้อนดูได้ว่า agent "เป็นใคร" ณ เวลานั้น
- CLAUDE.md ของ project นี้ทำหน้าที่เดียวกันเป๊ะ — มันคือ SOUL.md ของ wiki นี้

## เชื่อมกับอะไร

- **CLAUDE.md** — เราใช้ pattern นี้อยู่แล้วโดยไม่รู้ตัว ตอนนี้รู้ที่มาแล้ว
- **Multi-agent simulation** — agent ที่มี SOUL.md ที่ดีกว่า น่าจะให้ผล simulation ที่ realistic กว่า
- **MiroFish** — ใช้ swarm agent หลายพัน ตัว — ถ้า agent แต่ละตัวมี soul ที่ชัด ผลลัพธ์น่าจะต่างกันมาก

## คำถามที่ยังค้างอยู่

- SOUL.md ที่ดีควรมีอะไรบ้าง? แค่ personality หรือรวม constraints และ values ด้วย?
- ใน multi-agent sim ที่มี agent พัน ตัว จะ generate SOUL.md แต่ละตัวยังไงให้ diverse แต่ consistent?
