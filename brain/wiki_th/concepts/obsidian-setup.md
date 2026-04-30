# Obsidian Vault Setup

## สรุปสั้นๆ

บันทึก config ของ vault นี้ (2nd Brain) — plugins ที่ใช้, Web Clipper workflow, และ vault structure

## Plugins ที่ enable อยู่

**Core (built-in):**
- Sync, File Recovery, Graph, Backlink, Properties, Daily Notes, Templates, Canvas, Bases

**Community:**
- **Kanban** — board แบบ kanban ใน markdown
- **Terminal** — เปิด terminal ใน sidebar ได้เลย

**ติดตั้งแต่ยังไม่ได้ enable:**
- Dataview (query notes เหมือน database)
- Excalidraw (วาดรูป whiteboard)
- Breadcrumbs (navigation แบบ hierarchy)

## Web Clipping ด้วย Obsidian Web Clipper

ใช้ browser extension ตัวเป็นทางการของ Obsidian

**Flow:**
1. เจอบทความน่าสนใจ → click extension
2. Clipper แปลงเป็น Markdown → save ลง `raw/`
3. อ่านแล้วเจอ insight → INGEST เข้า wiki

**Template ที่แนะนำ (ตั้งใน extension settings):**
```
---
title: {{title}}
url: {{url}}
clipped: {{date:YYYY-MM-DD}}
tags: [clipped]
---

{{content}}
```

**เคล็ดลับ:**
- Highlight ข้อความก่อน clip → ได้แค่ส่วนที่สำคัญ (ใช้ `{{highlights}}`)
- แก้ใน popup ก่อน save — ตัด nav/footer noise ออกได้
- File ไปลงที่ `raw/` → รอ INGEST เข้า wiki ภายหลัง

## Vault Structure

```
2nd Brain/
├── raw/       ← web clips + source docs มาลงที่นี่
├── สมุด/      ← โน้ตภาษาไทย (เราเขียนเอง)
└── wiki/      ← knowledge base ภาษาอังกฤษ (Claude maintain)
```

## คำถามที่ยังค้างอยู่

- Interpreter mode ของ Web Clipper ใช้กับ vault นี้ได้ไหม?
- Dataview ควร enable ไหม — มี use case ชัดๆ ยัง?
