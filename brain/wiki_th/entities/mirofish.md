# MiroFish และ Multi-Agent Simulation

## สรุปสั้นๆ

MiroFish คือ engine ที่สร้าง "โลกจำลองดิจิทัล" ด้วย agent หลายพันตัว แต่ละตัวมีบุคลิก, ความจำ, และตรรกะของตัวเอง แล้วปล่อยให้ interact กัน เพื่อดูว่า "อนาคตจะเป็นยังไง" โดยไม่ได้ถามโมเดลโดยตรง แต่สังเกต emergent outcome แทน

## สิ่งที่น่าสนใจ

- แนวคิดเหมือนฝูงปลา (ชื่อก็มาจากนี่) — ปลาแต่ละตัวฉลาดแค่ระดับหนึ่ง แต่ทั้งฝูงทำสิ่งที่ซับซ้อนกว่าได้มาก
- inject ตัวแปรระหว่าง simulation ได้ — "ถ้าเกิดเหตุการณ์ X จะเป็นยังไง?" counterfactual testing
- ใช้ OASIS (จาก CAMEL-AI), Zep Cloud สำหรับ memory ของ agent, GraphRAG สร้าง relationship graph

## เชื่อมกับอะไร

- SOUL.md — agent ที่มี identity ชัดเจนน่าจะให้ simulation ที่ realistic กว่า
- PredictionService ใน MyMoney ก็เป็น prediction แบบง่าย — MiroFish คือ prediction แบบ heavy-weight

## คำถามที่ยังค้างอยู่

- scale ได้แค่ไหน? agent พัน ตัว × หลายรอบ = compute เท่าไหร่?
- คุณภาพ persona design ส่งผลแค่ไหนต่อผล simulation?
- ในงาน serious (นโยบาย, การเงิน) เชื่อถือได้แค่ไหน?
