# Bank Noti Tester

## สรุปสั้นๆ

Flutter app เล็กๆ ที่ทำขึ้นมาสำหรับ dev เท่านั้น — ส่ง notification จำลองที่หน้าตาเหมือน SMS ธนาคารไทยจริง เพื่อทดสอบ MyMoney โดยไม่ต้องรอ notification จากธนาคารจริง

## สิ่งที่น่าสนใจ

- code ทั้งหมด 284 บรรทัดในไฟล์เดียว — เป็นตัวอย่างที่ดีของ "ไม่ over-engineer สิ่งที่ไม่จำเป็น"
- มี template 6 แบบ: SCB/KBank/KTB/BBL ทั้ง incoming/outgoing — cover case ที่ใช้บ่อยครบ
- ทดสอบ edge case ได้ผ่าน custom builder กรอก title/body เองได้เลย

## เชื่อมกับอะไร

- MyMoney — รับ notification ผ่าน EventChannel แล้ว parse เป็น transaction อัตโนมัติ
- pipeline: Bank Noti Tester → Android OS → MyMoney NotificationService → TransactionProvider → SQLite
