# 50 Front-end Projects

## สรุปสั้นๆ

repo ของ Sudeep Acharjee ที่รวม 50 frontend projects ไว้ในที่เดียว แต่ละโปรเจกต์อยู่ใน folder ของตัวเอง เปิด `index.html` ในบราวเซอร์ได้เลย ไม่ต้อง build

clone ไว้ที่ `~/Desktop/50-frontend-projects/` แล้ว

## สิ่งที่น่าสนใจ

**แบ่งเป็น 5 กลุ่มหลัก:**

- **Landing Pages (8)** — Company Portfolio, Blog, E-commerce, Hotel ฯลฯ → ดูการจัด layout และ responsive design
- **Utility Tools (14)** — Password Gen, Weather App, Image Resizer, Dictionary → ดูการ call API และจัดการ DOM
- **Games (10)** — Chess, Snake, Car Racing, Tic-Tac-Toe → ส่วนใหญ่ใช้ Canvas API หรือ DOM manipulation
- **Media & Creative (8)** — Drawing App, Music Player, Piano, Photo Editor → ดูการใช้ Web APIs
- **UI Clones & Apps (10)** — Twitter Clone, Whatsapp Clone, Admin Dashboard → ดูการ implement layout ที่ซับซ้อน

**Pattern ที่น่าเก็บไว้อ้างอิง:**

- Canvas game loop → ดู Car Racing (#25), Snake (#37), Dragon Game (#49)
- LocalStorage CRUD → ดู Note App (#34), Todo List (#41)
- File API + Blob download → ดู File Downloader (#23), Text Saver (#35)
- `<audio>` control → ดู Music Player (#31)
- Fetch + external API → ดู Weather (#11), Dictionary (#36), Translator (#19)

## เชื่อมกับอะไร

- เป็น knowledge base สำหรับ frontend patterns พื้นฐาน — ถ้าจะทำ feature ไหน เช่น canvas drawing หรือ LocalStorage app มาดู implementation reference ได้เลย
- ต่างจาก MyMoney ที่เป็น Flutter app — อันนี้เป็น pure web, ไม่มี framework หนัก

## คำถามที่ยังค้างอยู่

- project ไหนที่ใช้ React จริงๆ บ้าง? (README บอกแค่ว่ามี React แต่ไม่ได้ระบุ project หมายเลขชัดเจน)
- Admin Dashboard (#44) น่าจะ React-based — ลองเปิดดู source ได้
