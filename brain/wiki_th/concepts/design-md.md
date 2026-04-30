# DESIGN.md — วาง design system ให้ AI อ่านแล้ว UI ออกมาตรงเลย

## สรุปสั้นๆ

DESIGN.md คือ markdown file ที่เก็บ design system ไว้ในรูปแบบที่ AI agent อ่านได้ — วาง file นี้ที่ root ของ project แล้วบอก Claude ว่า "build UI ตาม design system นี้" ได้เลย Google Stitch เป็นคนแนะนำ format นี้

## สิ่งที่น่าสนใจ

- **Pattern เดียวกับ SOUL.md** — นี่คือ instance ของ "plain-text context injection" pattern: ให้ agent ไฟล์ markdown ที่มี context ชัดเจน แล้วมันจะทำงานได้ตรงทิศทางโดยไม่ต้องอธิบายซ้ำทุกครั้ง
- **ไม่มี tooling พิเศษ** — แค่ markdown ธรรมดา ไม่ต้องมี Figma, ไม่ต้องมี JSON schema, ไม่ต้อง configure อะไร
- **Agent Prompt Guide** คือ section ที่ 9 ใน format — file จะมี prompt สำเร็จรูปไว้ให้ด้วย เช่น "สร้างหน้า dashboard ที่มี sidebar สีเข้ม" แบบ copy-paste ได้เลย
- **Google Stitch แนะนำ format นี้** — ถ้า big player adopt แบบนี้ มีโอกาสสูงที่จะ standardize เป็น convention ของ industry

## แหล่งข้อมูลพร้อมใช้

VoltAgent มี repo `awesome-design-md` ที่มี DESIGN.md จาก 55+ website จริงๆ เช่น:
- Vercel, Linear, Notion, Stripe (dev/SaaS)
- Apple, Spotify, Tesla (premium brand)
- Figma, Cursor (design/dev tool)
- Coinbase, Revolut (fintech)

แต่ละตัวมี `preview.html` ให้ดูด้วย ว่าหน้าตา design system จริงๆ เป็นยังไง

## เชื่อมกับอะไร

- **SOUL.md pattern** — ทั้งคู่คือ "ให้ agent ไฟล์ markdown domain-specific เพื่อ shape behavior"
- **MyMoney** — ถ้าอยากให้ Claude สร้าง UI ใหม่ให้ดูเหมือน Linear หรือ Notion แค่ copy DESIGN.md เข้ามาในโปรเจกต์แล้วบอก Claude ได้เลย ไม่ต้องอธิบาย design ยาวๆ

## คำถามที่ยังค้างอยู่

- Google Stitch ใช้งานได้จริงแล้วหรือยัง หรือยังเป็น preview?
- DESIGN.md กับ CLAUDE.md ถ้าขัดกัน agent จะเชื่ออันไหน?
- มีคนทำ DESIGN.md สำหรับ Material Design หรือ Ant Design ไหม — น่าจะมีประโยชน์มากถ้า design system เป็น open standard
