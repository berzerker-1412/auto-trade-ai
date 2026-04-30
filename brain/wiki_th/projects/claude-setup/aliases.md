# Claude Code Setup — Shell Aliases

## สรุปสั้นๆ

Shell aliases ใน `~/.zshrc` สำหรับ navigate และเปิด Claude Code ใน project ต่างๆ อย่างรวดเร็ว ไม่ต้องพิมพ์ path ยาว

---

## สิ่งที่น่าสนใจ / จุดสำคัญ

### Aliases ที่ตั้งไว้

```bash
# Navigate to project
alias mymoney='cd /Users/chinnawat/projects/mymoney'
alias banktest='cd /Users/chinnawat/projects/bank_noti_tester'
alias brain='cd /Users/chinnawat/Desktop/Brain/2nd\ Brain'

# Open Claude Code ใน project นั้นเลย
alias cc-mymoney='cd /Users/chinnawat/projects/mymoney && claude'
alias cc-brain='cd /Users/chinnawat/Desktop/Brain/2nd\ Brain && claude'
alias cc-banktest='cd /Users/chinnawat/projects/bank_noti_tester && claude'
```

เพิ่มใน `~/.zshrc` แล้วรัน `source ~/.zshrc`

### `--add-dir` สำหรับ multi-project context

```bash
claude --add-dir /Users/chinnawat/projects/bank_noti_tester
```

ใช้เมื่อต้องการให้ Claude เห็น context จาก 2 project พร้อมกัน เช่น debug notification pipeline ที่ MyMoney อ่าน event จาก Bank Noti Tester

### CLAUDE.md ต่อ Project — "soul" ของ Claude

แต่ละ project ควรมี `CLAUDE.md` ที่ root เพื่อบอก Claude ว่า project นี้คืออะไร stack คืออะไร convention คืออะไร

| Project | มี CLAUDE.md ไหม |
| --- | --- |
| 2nd Brain | มี — schema + workflow |
| mymoney | ยังไม่มี (แนะนำให้สร้าง) |
| bank_noti_tester | ยังไม่มี (project เล็กอาจไม่จำเป็น) |

**ตัวอย่าง CLAUDE.md สำหรับ mymoney:**

```markdown
# MyMoney — Claude Instructions

Flutter personal finance app.

## Stack
- Flutter 3.x / Dart 3.2+, Provider, SQLite, ML Kit

## Conventions
- State: ChangeNotifier providers in lib/providers/
- DB: DatabaseService singleton (lib/services/database_service.dart)
- All models have toMap()/fromMap() for SQLite

## Before coding
1. Read lib/models/ — understand data structure
2. Read the relevant provider before touching UI
```

---

## เชื่อมกับอะไร

- [Claude Code Setup](claude-setup.md) — overview ทั้งหมด
- [Claude Setup Hooks](claude-setup-hooks.md) — auto-translate hook
- [MyMoney Architecture](mymoney-architecture.md) — context ที่ alias `cc-mymoney` เปิดไป

---

## คำถามที่ยังค้างอยู่

- ถ้าต้องทำงาน 3 project พร้อมกัน `--add-dir` ใส่ได้หลายครั้งไหม?
- CLAUDE.md ของ mymoney ควรมี section อะไรบ้าง? ถึงเวลาสร้างแล้ว?
