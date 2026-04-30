# Multi-Agent Simulation — กลไกการจำลองสังคม

## สรุปสั้นๆ

Multi-agent simulation คือเทคนิคจำลองระบบที่ประกอบด้วย agent อิสระหลายตัว แต่ละตัวมี state, กฎพฤติกรรม และความสามารถ interact กับ agent อื่น ใน context ของ AI ปัจจุบัน นี่คือวิธีสร้าง "สังคมจำลอง" ที่ให้ผลลัพธ์แบบ emergent ซึ่ง single model ทำไม่ได้

## สิ่งที่น่าสนใจ / จุดสำคัญ

**ส่วนประกอบของ agent แต่ละตัว** (ใน MiroFish / OASIS framework)

- **Personality** — traits, attitudes, beliefs
- **Long-term memory** — ประวัติ interaction สะสม (ผ่าน Zep Cloud)
- **Behavioral logic** — กฎตัดสินใจ
- **Social relationships** — ความสัมพันธ์กับ agent อื่น (สร้างผ่าน GraphRAG)

**Simulation Workflow**

1. Generate personas จาก seed materials
2. สร้าง relationship graph (GraphRAG)
3. ปล่อย agent interact ตาม temporal loops
4. สังเกต emergent patterns ที่เกิดขึ้น
5. สรุปผ่าน ReportAgent

**จุดแข็ง**
- จับ nonlinear และ emergent behavior ที่โมเดลเดี่ยวทำไม่ได้
- Inject counterfactual variable กลางการ simulation ได้
- ผลลัพธ์ scale ตามจำนวน agent และรอบ simulation

**ข้อจำกัดที่ต้องรู้**
- ผล quality ขึ้นกับ persona design และ seed เป็นหลัก
- Token/compute cost สูงมาก — แนะนำ test ด้วย < 40 rounds ก่อน
- ไม่ใช่ ground truth — เป็นการ explore possibility space ไม่ใช่ทำนายแน่นอน

**ความแตกต่างที่สำคัญ:** Multi-agent simulation ไม่ใช่แค่รัน LLM หลายตัวพร้อมกัน — agent แต่ละตัวต้องมี memory ที่ persist ข้าม loop และ relationship graph ที่กำหนด pattern ของ interaction สิ่งที่ make it work คือ memory + social graph ไม่ใช่แค่จำนวน agent

## เชื่อมกับอะไร

- [Swarm Intelligence](swarm-intelligence.md) — theoretical foundation
- [MiroFish และ Multi-Agent Simulation](mirofish.md) — primary implementation
- OASIS — underlying simulation framework (ยังไม่มีโน้ตแยก)

## คำถามที่ยังค้างอยู่

- Temporal loops ที่เหมาะสมคือกี่ rounds — trade-off ระหว่าง quality กับ cost
- GraphRAG สำหรับ social relationship — ใช้ graph DB อะไร, scale ยังไงกับ agent หลายพัน
- Seed quality กำหนดผล — มี methodology ที่ดีสำหรับ persona generation ไหม
