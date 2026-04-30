# MyMoney

## สรุปสั้นๆ

แอป personal finance สำหรับคนไทย เขียนด้วย Flutter ทำงาน offline-first และ sync กับ Google Sheets ได้ เด่นตรงที่ดึง transaction จาก notification ธนาคารอัตโนมัติ ไม่ต้องกรอกมือ

## สิ่งที่น่าสนใจ

- OCR อ่าน slip ธนาคารไทยได้ — จับ ฿, เดือนไทย, ปีพ.ศ. แล้วแปลงให้อัตโนมัติ
- AI predict หมวดหมู่แบบ rule-based scoring ง่ายๆ แต่ใช้งานได้จริง — บวกคะแนนตาม keyword + เวลาของวัน + ยอดเงิน
- Architecture clean มาก — 4 layer ไม่มี circular dependency, provider แยก domain ชัดเจน 6 ตัว
- มี Bank Noti Tester แยกต่างหากสำหรับจำลอง notification ตอน dev

## เชื่อมกับอะไร

- Bank Noti Tester — dev tool คู่กัน ส่ง notification จำลองมาให้ MyMoney parse
- PredictionService ใช้ keyword matching แบบ เดียวกับที่ swarm agent simulation ก็ใช้ใน persona design

## คำถามที่ยังค้างอยู่

- PredictionService ยังเป็น rule-based — อัปเกรดเป็น on-device ML model ได้ไหม?
- Google Sheets sync เป็น optional ดีแล้ว แต่ถ้าอยากทำ analytics เพิ่ม ควรใช้ BigQuery หรือ Sheets ต่อไปดี?
