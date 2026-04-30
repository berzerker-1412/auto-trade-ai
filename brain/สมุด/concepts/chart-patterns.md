# Chart Patterns — รูปแบบกราฟ

## สรุปสั้นๆ

กราฟ patterns = ภาพรวมของแท่งเทียนหลายๆ แท่งมาประกอบกัน บอกโครงสร้าง supply/demand

**แบ่งเป็น 2 กลุ่ม:**
- **Reversal** = กลับทิศ (trend change)
- **Continuation** = ต่อเนื่อง (แค่พัก)

## Reversal Patterns สำคัญ

### Head and Shoulders (หัวและไหล่)
```
     หัว
  ไหล่ซ้าย   ไหล่ขวา
───────────  Neckline
```
- หัวสูงสุด, ไหล่ทั้งสองต่ำกว่าและใกล้เคียงกัน
- **เป้าหมาย:** `2 × Neckline − Head`
- หลุด Neckline ลง = ขาลง

### Double Top / Double Bottom
- Top สองครั้งในระดับเดียวกัน = กลับลง
- Bottom สองครั้งในระดับเดียวกัน = กลับขึ้น

## Continuation Patterns สำคัญ

### Triangles
```
Ascending:     ─── flat resistance
               / rising support
Descending:    \ flat support
               ─── falling resistance
Symmetric:     /\ converging
```

- Ascending → มีโอกาสขึ้น (resistance ทดสอบหลายครั้งจนพัง)
- Symmetric → ไม่มี bias (รอ breakout)

### Flags & Pennants
- หลังขึ้น/ลงแรงๆ → พักตัวสั้นๆ → มักจะต่อเนื่อง
- "เสาธง" = ขาสั้น + ธง = สัญญาณต่อเนื่องที่ดี

## กฎทอง

> **Breakout ต้องมี volume สูงกว่าปกติ** — ไม่งั้นมีโอกาส false breakout สูงมาก

## จำง่ายๆ

```
Reversal:    H&S, Double Top/Bottom, Triple, Rounding = เปลี่ยนทิศ
Continuation: Triangles, Flags, Pennants, Wedges = พักแล้วต่อ
```

## ในโปรเจกต์

chart_patterns ยังไม่ได้ implement ใน signal_generator — เป็นโอกาสเพิ่มเติม

## เชื่อมกับ

- [[candlestick-patterns]] — candlestick เป็นส่วนประกอบของ chart patterns
- [[technical-indicators]] — OBV/volume ยืนยัน breakout
- [[risk-management]] — stop วางใต้ neckline
