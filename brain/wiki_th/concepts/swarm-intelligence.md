# Swarm Intelligence — สติปัญญาจากฝูงชน

## สรุปสั้นๆ

Swarm intelligence คือแนวคิดที่ว่า "ความฉลาดซับซ้อนสามารถ emerge จากการ interact กันของ agent เล็กๆ หลายตัว โดยไม่มีตัวควบคุมกลาง" ตัวอย่างธรรมชาติ: ฝูงปลา, นกกระจอกบินวนเป็นรูปแบบ (murmuration), อาณาจักรมด ในโลก AI ปัจจุบัน แนวคิดนี้ถูกนำมาใช้แบบจริงจังใน multi-agent simulation

## สิ่งที่น่าสนใจ / จุดสำคัญ

- ไม่มี central controller — แต่ผลลัพธ์รวมฉลาดกว่าแต่ละตัวมาก
- ใน AI context: ใช้ agent หลายพันตัวทำงานพร้อมกัน interact กัน → ดู emergent behavior ที่เกิดขึ้น

**เปรียบเทียบวิธีทำนาย**

| วิธี | แนวทาง | ข้อจำกัด |
| --- | --- | --- |
| Statistical model | Fit curve จากข้อมูลอดีต | พลาด nonlinear social dynamics |
| Single LLM | ถามโมเดลตรงๆ | ไม่มี emergent behavior, bias จาก training |
| Swarm simulation | ปล่อย agent หลายพัน interact | compute สูง, ผลขึ้นกับ persona design |

**ทำไม single LLM ไม่พอ?** LLM ตอบจาก training data — มันไม่ได้ "จำลอง" สังคม มันแค่ "จำ" patterns ที่เคยเห็น Swarm simulation บังคับให้เกิด interaction จริงๆ ระหว่าง agent → ผลที่ได้คือ emergent จริง ไม่ใช่แค่ pattern matching

**MiroFish** เป็นตัวอย่างการ apply concept นี้: สร้างสังคมจำลองหลายพัน agent เพื่อทำนาย social outcome แทนการถาม LLM โดยตรง

## เชื่อมกับอะไร

- [MiroFish และ Multi-Agent Simulation](mirofish.md) — implementation จริงของ concept นี้
- [Multi-Agent Simulation](multi-agent-simulation.md) — mechanics ว่า agent แต่ละตัวสร้างยังไง

## คำถามที่ยังค้างอยู่

- Compute cost เป็น bottleneck หลัก — มีวิธี optimize ไหมโดยไม่เสีย emergent quality
- ขนาด population ที่เหมาะสม — 1,000 vs 10,000 agent ให้ผลต่างกันแค่ไหน
