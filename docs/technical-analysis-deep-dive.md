# คู่มือการวิเคราะห์ทางเทคนิค: การลงทุนครบวงจร
**Project: Auto Trade AI — Crypto & Gold Trading System**
**Updated: April 2026**

---

## สารบัญ
1. [พื้นฐานแท่งเทียน (Candlestick Basics)](#1-พื้นฐานแท่งเทียน-candlestick-basics)
2. [รูปแบบแท่งเทียน (Candlestick Patterns)](#2-รูปแบบแท่งเทียน-candlestick-patterns)
3. [รูปแบบกราฟ (Chart Patterns)](#3-รูปแบบกราฟ-chart-patterns)
4. [ตัวชี้วัดทางเทคนิค (Technical Indicators)](#4-ตัวชี้วัดทางเทคนิค-technical-indicators)
5. [ทฤษฎีตลาด (Market Theories)](#5-ทฤษฎีตลาด-market-theories)
6. [การบริหารความเสี่ยง (Risk Management)](#6-การบริหารความเสี่ยง-risk-management)
7. [กลยุทธ์การเทรด (Trading Strategies)](#7-กลยุทธ์การเทรด-trading-strategies)
8. [AI/ML สำหรับการเทรด](#8-aiml-สำหรับการเทรด)
9. [การนำไปใช้ในโปรเจกต์](#9-การนำไปใช้ในโปรเจกต์)

---

## 1. พื้นฐานแท่งเทียน (Candlestick Basics)

### โครงสร้างแท่งเทียน

```
        High
         ▲
         │  Upper Wick (ไส้เทียนบน)
         │
  Open ────┐
   │       │
   │       │  Body (ตัวแท่ง)
   │       │
  Close ───┘
         │
         │  Lower Wick (ไส้เทียนล่าง)
         ▼
       Low
```

### องค์ประกอบ

| ส่วน | ความหมาย |
|------|----------|
| **Body (ตัวแท่ง)** | ระหว่าง Open กับ Close |
| **Upper Wick** | High - max(Open, Close) |
| **Lower Wick** | min(Open, Close) - Low |
| **Bullish (สีเขียว/ขาว)** | Close > Open → ราคาขึ้น |
| **Bearish (สีแดง/ดำ)** | Close < Open → ราคาลง |

### หลักการอ่านแท่งเทียน

1. **ตัวแท่งยาว** = แรงซื้อ/ขายเยอะ (ความเชื่อมั่นสูง)
2. **ตัวแท่งสั้น** = ความลังเลของตลาด
3. **ไส้ยาวด้านบน** = ฝ่ายขายพยายามกด แต่ฝ่ายซื้อยังควบคุม
4. **ไส้ยาวด้านล่าง** = ฝ่ายซื้อพยายามยก แต่ฝ่ายขายยังควบคุม

---

## 2. รูปแบบแท่งเทียน (Candlestick Patterns)

### 2.1 Single Candlestick Patterns (รูปแบบแท่งเดียว)

#### Doji (โดจิ) — ความลังเล

```
        High
         ▲
    ─────┴─────  ← Open ≈ Close (almost same level)
         │
         │
    ─────┴─────
         ▼
       Low
```

**วิธีระบุ:** ราคาเปิดและปิดใกล้กันมาก (แท่งเล็กมาก)
**ประเภท:**
- **Gravestone Doji** — ไส้บนยาว, ไส้ล่างสั้น → ฝ่ายขายควบคุม
- **Dragonfly Doji** — ไส้ล่างยาว, ไส้บนสั้น → ฝ่ายซื้อควบคุม
- **Long-legged Doji** — ไส้ทั้งสองยาว → ความลังเลสูง

**สัญญาณ:**
- เกิดที่ยอด → เตือนการกลับตัวลง
- เกิดที่ก้น → เตือนการกลับตัวขึ้น
- **ต้องรอยืนยันจากแท่งถัดไป**

#### Hammer (ฮอมเมอร์) — กลับตัวขาขึ้น

```
         High
          │
    ──────┴─────  Upper Wick (สั้นมาก)
    │           │
    │   Body    │  ← อยู่ในช่วงบน
    │           │
    └───────────┘
          │
          └────────  Lower Wick (ยาว ≥ 2x Body)
          ▼
        Low
```

**สูตร:** `Lower Wick ≥ 2 × Body` และ `Body อยู่ในช่วงบน`
**เงื่อนไข:** ต้องเกิดหลังจาก **Downtrend**
**สัญญาณ:** ราคามีโอกาสกลับตัวขึ้น (Bullish Reversal)
**ยืนยัน:** แท่งถัดไปเป็นสีเขียว, Volume สูง

#### Inverted Hammer (ฮอมเมอร์กลับหัว)

```
         High
          │
          └────────  Upper Wick (ยาว ≥ 2 × Body)
          │
    ──────┴─────
    │           │  ← Body อยู่ในช่วงล่าง
    ──────┬─────
          │
        Low
```

**สัญญาณ:** Bullish reversal เช่นกัน (แต่ต้องยืนยันจากแท่งถัดไป)

#### Shooting Star (ดาวตก)

```
         High
          │  ← Upper Wick ยาว (≥ 2 × Body)
          │  ← Body อยู่ในช่วงล่าง
    ──────┴─────
          │
        Low
```

**สูตร:** `Upper Wick ≥ 2 × Body`, Body อยู่ในช่วงล่าง
**เงื่อนไข:** ต้องเกิดหลังจาก **Uptrend**
**สัญญาณ:** Bearish reversal — ราคามีโอกาสลง

#### Spinning Top (ลูกข่าง)

```
          High
           │
      ─────┴─────  Upper Wick (ยาว)
      │      │
      │ Body │      ← Body เล็กมาก
      │      │
      ─────┬─────  Lower Wick (ยาว)
           │
         Low
```

**ความหมาย:** ความลังเลสูง ไม่มีใครควบคุมตลาด → รอดู

#### Marubozu (ไม่มีไส้)

```
  Bullish Marubozu         Bearish Marubozu
  
       High                      High
        │  ← no wick              │
    ────┴─────  Open          ┌───┴───  Open
    │         │             │         │
    │         │             │         │
    └─────────┘  Close      └─────────┘  Close
        │                        │
      Low                       Low ← no wick
```

**Bullish:** เปิดที่ Low, ปิดที่ High → แรงซื้อเต็มที่
**Bearish:** เปิดที่ High, ปิดที่ Low → แรงขายเต็มที่

---

### 2.2 Double Candlestick Patterns (รูปแบบ 2 แท่ง)

#### Engulfing (การกลืน)

**Bullish Engulfing:**
```
  Day 1 (Bearish)     Day 2 (Bullish)
  
      │                    █
      │  █                 █ █
      █ █                  █ █
      █                    █
```

- แท่ง 1: สีแดง (Bearish) — ฝ่ายขายควบคุม
- แท่ง 2: สีเขียว (Bullish) — **กลืนแท่ง 1 ทั้งหมด**
- ต้องเกิดหลัง Downtrend

**Bearish Engulfing:**
- ตรงข้ามกับ Bullish
- แท่ง 1 สีเขียว → แท่ง 2 สีแดงกลืนทั้งหมด
- ต้องเกิดหลัง Uptrend

**สูตร:** `Body2 > Body1 (both wicks included)`

#### Piercing Line

```
  Day 1 (Bearish)     Day 2 (Bullish)
  
      │                    █
      █ █                  █ █
      █                    █
      │                    ▼  ปิดเหนือ 50% ของแท่ง 1
```

- แท่ง 1: สีแดงยาว
- แท่ง 2: เปิดต่ำกว่าต่ำสุดของแท่ง 1 → ปิด**เหนือ 50%** ของแท่ง 1
- ความแข็งแกร่ง: อ่อนกว่า Engulfing

#### Dark Cloud Cover

```
  Day 1 (Bullish)     Day 2 (Bearish)
  
      █                    │
      █ █                  █ █
      │                    █
      │  ← ปิดต่ำกว่า 50%   ▼
```

- ตรงข้ามกับ Piercing Line
- แท่ง 1 สีเขียว → แท่ง 2 สีแดงปิดต่ำกว่า 50% ของแท่ง 1

#### Harami (ตั้งครรภ์)

```
  Day 1 (Large)        Day 2 (Small)
  
      █                    │
      █ █                  █  ← อยู่ภายในแท่ง 1
      █                    │
```

- แท่ง 2 อยู่**ภายใน**แท่ง 1 (ไม่ต้องกลืนทั้งหมด)
- ความแข็งแกร่ง: อ่อนกว่า Engulfing
- Bullish Harami: แท่ง 1 สีแดง, แท่ง 2 สีเขียว
- Bearish Harami: แท่ง 1 สีเขียว, แท่ง 2 สีแดง

#### Tweezer Bottoms / Tops

```
  Tweezer Bottom         Tweezer Top
  
      │                    █
      █ █                  █ █
      █                    █
      █                    │
```

- ทั้งสองแท่งมี **Low หรือ High เท่ากัน**
- Tweezer Bottom: กลับตัวขึ้น (Low เท่ากัน)
- Tweezer Top: กลับตัวลง (High เท่ากัน)

---

### 2.3 Triple Candlestick Patterns (รูปแบบ 3 แท่ง)

#### Morning Star (ดาวรุ่ง) — กลับตัวขาขึ้น

```
  Day 1        Day 2       Day 3
  
      ██         │          ███
      ██         │          ███
      ██         ▼          ███
      ▼      (Doji/Star)     ▲
```

- **Day 1:** แท่งสีแดงยาว — แรงขายควบคุม
- **Day 2:** แท่งเล็ก (Doji หรือ Star) — ความลังเล
- **Day 3:** แท่งสีเขียวยาว — แรงซื้อกลับมา
- **เงื่อนไข:** แท่ง 3 ควรปิดเหนือ 50% ของแท่ง 1

#### Evening Star (ดาวราตรี) — กลับตัวขาลง

```
  Day 1        Day 2       Day 3
  
      ███         │           ██
      ███         │           ██
      ███         ▼           ██
        ▲     (Doji/Star)     ▼
```

- ตรงข้ามกับ Morning Star
- **Day 1:** สีเขียวยาว
- **Day 2:** แท่งเล็ก
- **Day 3:** สีแดงยาว ปิดต่ำกว่า 50% ของแท่ง 1

#### Three White Soldiers (ทหารขาวสามคน)

```
     █
    █ █       █
   █   █     █ █      █
  █     █   █   █    █ █
```

- แท่ง 3 ตัว สีเขียว ตามกันมา
- แต่ละแท่งเปิดภายใน body ของแท่งก่อน
- แต่ละแท่งปิดใกล้ High
- **สัญญาณแข็งแกร่งมาก** ของการกลับตัวขาขึ้น

#### Three Black Crows (ก raven าคน)

```
     █
    █ █       █
   █   █     █ █      █
  █     █   █   █    █ █
```

- ตรงข้ามกับ Three White Soldiers
- แท่ง 3 ตัว สีแดง ปิดใกล้ Low
- **สัญญาณแข็งแกร่งมาก** ของการกลับตัวขาลง

---

### 2.4 Gap Patterns (รูปแบบ Gap)

```
  ↑ Gap Up (Bullish)         ↓ Gap Down (Bearish)

  ███                         ███
  ──────                      ──────
  (gap)                        (gap)
  ──────                      ──────
  ███                         ███
```

| ประเภท | ความหมาย |
|--------|----------|
| **Common Gap** | ธรรมดา, เกิดบ่อย, ไม่ค่อยมีน้ำหนัก |
| **Breakaway Gap** | หลุดแนวรับ/ต้านสำคัญ → จุดเริ่มต้นแนวโน้มใหม่ |
| **Measuring Gap** | วัดระยะ gap = เป้าหมายราคา |
| **Exhaustion Gap** | ใกล้จุดจบแนวโน้ม → เตือนการกลับตัว |
| **Island Reversal** | Gap ทั้งสองข้างแยกออกจากกัน |

---

## 3. รูปแบบกราฟ (Chart Patterns)

### 3.1 Reversal Patterns (รูปแบบกลับตัว)

#### Head and Shoulders (หัวและไหล่)

```
         ┌───┐
        /  H  \      H = Head (หัว) — ยอดสูงสุด
  ┌───┐ /     \ ┌───┐
  │ L ││       ││ R │  L = Left Shoulder (ไหล่ซ้าย)
  └───┘│       │└───┘  R = Right Shoulder (ไหล่ขวา)
  ─────┴───────┴──────  Neckline
```

**วิธีระบุ:**
1. ไหล่ซ้าย (Left Shoulder) — ยอดแรก
2. หัว (Head) — ยอดที่สูงกว่าทุกยอด
3. ไหล่ขวา (Right Shoulder) — ยอดที่ 3 ต่ำกว่าหัว, ใกล้เคียงไหล่ซ้าย
4. Neckline — เส้นผ่าน Low ของไหล่ทั้งสอง

**สัญญาณ:** เมื่อราคา **หลุด Neckline ลง** → คาดขาลง
**เป้าหมายราคา:**
```
Target = (Neckline - Head) + Neckline
       = 2 × Neckline - Head
```

**Inverse Head and Shoulders** — ตรงข้าม → คาดขาขึ้น

#### Double Top (ยอดคู่)

```
       ┌───┐
      /     \       Top 1 = Top 2 (±5%)
     /   1   \
    /         \
   /     2     \
  ───────────────  Neckline
        ▲
    (หลุดลง)
```

**วิธีระบุ:**
- ยอด 2 ยอดอยู่ในระดับเดียวกัน (ต่างกันไม่เกิน 5%)
- มี Low คั่นระหว่างยอด
- Volume ที่ยอด 2 ควรน้อยกว่ายอด 1

**สัญญาณ:** หลุด Neckline → ขาลง
**เป้าหมาย:** `Target = Neckline - (Top - Neckline)`

#### Double Bottom (ก้นคู่)

```
  ───────────────
  \     1     /
   \         /
    \   2   /       ตรงข้ามกับ Double Top
     \     /
      └───┘  Bottom 1 = Bottom 2
        ▼
    (หลุดขึ้น)
```

**สัญญาณ:** หลุด Neckline → ขาขึ้น

#### Triple Top / Triple Bottom

```
  Top 1  Top 2  Top 3      คล้าย Double Top/Bottom
                          แต่มี 3 ยอด/ก้น
  ─────────────────
```

#### Rounding Bottom (ก้นกลม)

```
        /
   ___ /
  /    ---__
 /          \
/              \
```

- ค่อยๆ เปลี่ยนจากขาลง → ขาขึ้น
- คล้ายตัว "U"
- เป้าหมาย = ความสูงของ "U"

#### Cup and Handle (ถ้วยและหูช้อน)

```
      ┌───┐
     /     \
    /       \      Cup คล้าย Rounding Bottom
   /         \
  /           \
              \  Handle — พักตัวแบบ Flag
               \
                ▼
```

- Cup มีความลึก 12-15% พอดี (ลึกเกิน = หลุด pattern)
- Handle อยู่ด้านขวา พักตัว 1-2 สัปดาห์
- **Breakout ผ่าน Handle** → สัญญาณซื้อ

---

### 3.2 Continuation Patterns (รูปแบบต่อเนื่อง)

#### Symmetrical Triangle (สามเหลี่ยมสมมาตร)

```
      /\
     /  \
    /    \        เส้นบนลาดลง
   /      \
  /   ↓    \      เส้นล่างลาดขึ้น
 /   Price   \
/    Converge \
```

- ราคาแกว่งแคบลงเรื่อยๆ → รอ Breakout
- มักวิ่งต่อทิศทางเดิม (Continue)
- **Volume ลดลง** เมื่อเข้าหาจุดยุบ (Apex)

#### Ascending Triangle (สามเหลี่ยมขาขึ้น)

```
  ─────────────
  |          /
  |        /
  |      /    ← เส้นแนวนอน (แนวต้าน)
  |    /
  |  /          ← เส้นขาขึ้น (แนวรับ)
  |/
```

- **เส้นบน = แนวต้านแนวนอน** (demand แข็ง)
- เส้นล่างขึ้นเรื่อยๆ
- มัก **Breakout ขึ้น** (60-70%)
- เป้าหมาย = ความสูงสามเหลี่ยม + จุดหลุด

#### Descending Triangle (สามเหลี่ยมขาลง)

```
  \            ─────────────  เส้นแนวนอน (แนวรับ)
   \          |
    \        |    ← เส้นขาลง (แนวต้าน)
     \       |
      \      |
       \     |
```

- **เส้นล่าง = แนวรับแนวนอน** (supply แข็ง)
- มัก **Breakout ลง** (60-70%)

#### Flags (ธง)

```
  │││           ┌────  Flag Pole (เสาธง)
  │││           │││   = วิ่งฉับพลัน 1-3 วัน
  │││           │││
  │││           └────  Flag (แผ่นธง)
                       = พักตัว 3-15 วัน
                       = เฉียงเอียงไปทางตรงข้าม
```

- **Bull Flag:** ขึ้นฉับพลัน → พักตัวเล็กน้อย → ขึ้นต่อ
- **Bear Flag:** ลงฉับพลัน → พักตัวเล็กน้อย → ลงต่อ
- **เป้าหมาย:** ความสูง Flag Pole ≈ ระยะที่จะวิ่งต่อ

#### Pennants (ธงประดิษฐ์)

```
  │││              /\
  │││             /  \    Pennant = สามเหลี่ยมเล็กๆ
  │││            /    \   แทนที่จะเป็นสี่เหลี่ยม
  │││           /      \  อื่นๆ เหมือน Flags
```

- เหมือน Flags แต่แผ่นธงเป็นสามเหลี่ยมเล็ก

#### Rectangles (สี่เหลี่ยม)

```
  ───────────────  Resistance (แนวต้าน)
  │            │
  │   Range    │  Sideways / Consolidation
  │            │
  ───────────────  Support (แนวรับ)
```

- ราคาวิ่งอยู่ในกรอบแนวนอน
- **Continuation** มากกว่า Reversal
- Buy at Support, Sell at Resistance

#### Wedges (ลิ่ม)

```
  Rising Wedge           Falling Wedge

     /\                      /\
    /  \                    /  \
   /    \                  /    \
  /      \                /      \
 /        \              /        \
/          \            /          \
(mลงbreakout)          (ขึ้นbreakout)
```

- **Rising Wedge:** ทั้งสองเส้นเอียงขึ้น → มัก **Breakout ลง**
- **Falling Wedge:** ทั้งสองเส้นเอียงลง → มัก **Breakout ขึ้น**

---

### 3.3 Price Action Concepts

#### Support และ Resistance

```
  Resistance (แนวต้าน)
  ─────────────────────
        ↑
   Price turns down here
        ↓
  ─────────────────────
        ↑
   Price turns up here
        ↓
  Support (แนวรับ)
```

**วิธีระบุ Support/Resistance ที่สำคัญ:**
1. **Price ต่ำสุด/สูงสุดเดิม** — ยิ่งถูกทดสอบหลายครั้ง ยิ่งแข็ง
2. **Round numbers** — 1,000 / 100 / 50 (psychological levels)
3. **Fibonacci levels** — 38.2%, 50%, 61.8%
4. **Volume clusters** — บริเวณที่มีการซื้อขายมาก
5. **Moving Averages** — MA 50, 100, 200

**กฎ:**
- เมื่อ Support หลุด → กลายเป็น Resistance
- เมื่อ Resistance หลุด → กลายเป็น Support
- ยิ่ง Volume สูงตอนทดสอบ ยิ่งแข็งแกร่ง

#### Trendlines และ Channels

```
  Uptrend Channel         Downtrend Channel
  
  Resistance ─────         ─────────────
       /       \                \       \
      /         \                \       \
     /           \                \       \
    /             \                \       \
  Support ─────────               ─────────────
```

- **Uptrend:** ทำ Higher Highs + Higher Lows
- **Downtrend:** ทำ Lower Highs + Lower Lows
- **Sideways:** HH, HL หยุดนิ่ง / LH, LL หยุดนิ่ง

**การใช้ Channel:**
- Buy at Support (ขอบล่าง)
- Sell at Resistance (ขอบบน)
- **Channel break** = แนวโน้มเปลี่ยน

#### Breakouts และ Fakeouts

**Breakout ที่ดี:**
1. Price ปิดเหนือ/ใต้ แนวอย่างชัดเจน
2. Volume สูงตอน Breakout
3. Price ไม่กลับมาทดสอบแนวทันที

**False Breakout (Fakeout):**
- Price หลุดแนวแล้วกลับมา
- เกิดบ่อย → ใช้ **"Breakout Confirmation"**
- รอปิดเกินแนว 1-2 วัน แล้วค่อยเข้า

#### Pullback และ Retest

```
  Breakout
      ↑
      │
  ────┴───────── Resistance (เก่า)
      │    ↑
      │    └── Retest / Pullback
      │         (โอกาสเข้าซื้อ)
      ▼
  ถ้า Hold แนว = ยืนยันสำเร็จ
  ถ้าหลุด = Breakdown
```

#### Divergence (ความแตกต่าง)

```
  Regular Bullish Divergence:
  
  Price:     /\    /\         ทำ Lower Low
             /  \  /  \
            /    \/    \
  
  RSI:       /\    /\         ทำ Higher Low
             \  /  \  /
              \/    \/
```

**ประเภท:**

| ประเภท | ราคา | Indicator | ความหมาย |
|--------|------|-----------|----------|
| **Regular Bullish** | ทำ LL | ทำ HL | กลับตัวขึ้น |
| **Hidden Bullish** | ทำ HL | ทำ LL | ขึ้นต่อ (Continue) |
| **Regular Bearish** | ทำ HH | ทำ LH | กลับตัวลง |
| **Hidden Bearish** | ทำ LH | ทำ HH | ลงต่อ (Continue) |

---

## 4. ตัวชี้วัดทางเทคนิค (Technical Indicators)

### 4.1 Trend Indicators (ตัวชี้วัดแนวโน้ม)

#### Moving Averages

**Simple Moving Average (SMA)**
```
SMA = (P1 + P2 + ... + Pn) / n
```
- ใช้ราคาปิดเฉลี่ย n วัน
- SMA 50 = แนวโน้มระยะกลาง
- SMA 200 = แนวโน้มระยะยาว

**Exponential Moving Average (EMA)**
```
EMA = (Close - Prev EMA) × k + Prev EMA
k = 2 / (n + 1)
```
- ให้น้ำหนักราคาล่าสุดมากขึ้น
- ฉลวกกว่า SMA ในการตอบสนอง

**Weighted Moving Average (WMA)**
```
WMA = (P1×1 + P2×2 + ... + Pn×n) / (1+2+...+n)
```
- ให้น้ำหนักเชิงเส้นตามลำดับเวลา

**การใช้:**
- **Golden Cross:** SMA 50 ขึ้นเหนือ SMA 200 → สัญญาณซื้อ
- **Death Cross:** SMA 50 ลงใต้ SMA 200 → สัญญาณขาย
- **Price > MA** = Uptrend / **Price < MA** = Downtrend
- **MA ทำมุมชัน** = แนวโน้มแข็ง

#### MACD (Moving Average Convergence Divergence)

```
MACD Line = EMA(12) - EMA(26)
Signal Line = EMA(9) ของ MACD Line
Histogram = MACD Line - Signal Line
```

**สัญญาณ:**

| สัญญาณ | เงื่อนไข |
|--------|----------|
| **ซื้อ** | MACD ตัดขึ้นเหนือ Signal |
| **ขาย** | MACD ตัดลงใต้ Signal |
| **ซื้อแรง** | Histogram เป็นบวกและขยายตัว |
| **Divergence** | MACD กับราคาบอกทิศต่างกัน |

#### Parabolic SAR (Stop and Reverse)

```
SAR(t) = SAR(t-1) + AF × (EP - SAR(t-1))
```
- **AF (Acceleration Factor):** ค่าเริ่มที่ 0.02, สูงสุด 0.2
- **EP (Extreme Point):** High สูงสุด (ในขาขึ้น) / Low ต่ำสุด (ในขาลง)

**การใช้:**
- จุดอยู่**ใต้ราคา** = ขาขึ้น
- จุดอยู่**เหนือราคา** = ขาลง
- จุดเปลี่ยนจากล่างไปบน = สัญญาณขาย
- จุดเปลี่ยนจากบนไปล่าง = สัญญาณซื้อ

#### ADX (Average Directional Index)

```
+DI = (Smoothed +DM / ATR) × 100
-DI = (Smoothed -DM / ATR) × 100
ADX = (Smoothed DX) × 100
```

**ค่าความหมาย:**

| ADX | แนวโน้ม |
|-----|---------|
| 0-20 | ไม่มีแนวโน้ม / อ่อน |
| 20-25 | เริ่มมีแนวโน้ม |
| 25-50 | แนวโน้มแข็ง |
| 50-75 | แนวโน้มแข็งมาก |
| 75-100 | แนวโน้มแข็งสุดขีด |

**การใช้ร่วมกับ +DI / -DI:**
- **+DI > -DI** = Uptrend
- **-DI > +DI** = Downtrend
- **ADX > 25** + +DI ข้าม -DI = สัญญาณซื้อ

#### Supertrend

```
Upper Band = (High + Low) / 2 + multiplier × ATR
Lower Band = (High + Low) / 2 - multiplier × ATR
```
- **Multiplier:** ค่าปกติ = 3
- สีเขียว = ขาขึ้น / สีแดง = ขาลง
- ง่ายต่อการใช้ — ตามสี

#### Ichimoku Cloud

```
Tenkan-sen = (Highest High + Lowest Low) / 2  (9 periods)
Kijun-sen = (Highest High + Lowest Low) / 2  (26 periods)
Senkou Span A = (Tenkan-sen + Kijun-sen) / 2   (26 periods ล่วงหน้า)
Senkou Span B = (Highest High + Lowest Low) / 2 (52 periods, 26 ล่วงหน้า)
Chikou Span = ราคาปิดปัจจุบัน (26 periods ถอยหลัง)
```

**การใช้:**
- ราคาอยู่**เหนือก้อนเมฆ** = ขาขึ้น
- ราคาอยู่**ใต้ก้อนเมฆ** = ขาลง
- **Tenkan ข้าม Kijun ขึ้น** = ซื้อ
- **Kumo Cloud หนา** = แนวโน้มแข็ง / บาง = อ่อน

---

### 4.2 Momentum Indicators (ตัวชี้วัดโมเมนตัม)

#### RSI (Relative Strength Index)

```
RS = Average Gain / Average Loss (ของ 14 วัน)
RSI = 100 - (100 / (1 + RS))
```

**ค่าความหมาย:**

| ค่า RSI | สถานะ |
|---------|-------|
| **> 70** | Overbought — เตรียมขาย |
| **< 30** | Oversold — เตรียมซื้อ |
| **> 80** | Overbought รุนแรง |
| **< 20** | Oversold รุนแรง |

**สัญญาณ:**
1. **RSI > 70 แล้วลงมา** = ขาย
2. **RSI < 30 แล้วขึ้นมา** = ซื้อ
3. **Divergence** ระหว่าง RSI กับราคา
4. **Failure Swing** — RSI ทะลุ 70 แล้วลงมาไม่ถึง 70 = สัญญาณขายแข็ง

#### Stochastic Oscillator

```
%K = (Close - Lowest Low 14) / (Highest High 14 - Lowest Low 14) × 100
%D = SMA(%K, 3)
```

**ค่าความหมาย:**

| ค่า | สถานะ |
|-----|-------|
| **> 80** | Overbought |
| **< 20** | Oversold |

**สัญญาณ:**
- **%K ข้าม %D ขึ้น** ในโซน Oversold = ซื้อ
- **%K ข้าม %D ลง** ในโซน Overbought = ขาย
- **Divergence** ระหว่าง Stochastic กับราคา

#### CCI (Commodity Channel Index)

```
CCI = (Typical Price - SMA 20) / (0.015 × Mean Deviation)
Typical Price = (High + Low + Close) / 3
```

**ค่าความหมาย:**

| ค่า CCI | สถานะ |
|---------|-------|
| **> +100** | Overbought |
| **< -100** | Oversold |

**สัญญาณ:** เหมือน RSI — กลับจากโซน Overbought/Oversold

#### Williams %R

```
%R = (Highest High - Close) / (Highest High - Lowest Low) × -100
```
- **ค่า 0 ถึง -20:** Overbought
- **ค่า -80 ถึง -100:** Oversold
- ใช้คล้าย Stochastic

#### Momentum / ROC (Rate of Change)

```
Momentum = Close - Close (n periods ago)
ROC = (Close - Close n periods ago) / Close n periods ago × 100
```

**สัญญาณ:**
- ROC > 0 = ราคาขึ้น / ROC < 0 = ราคาลง
- Divergence ระหว่าง ROC กับราคา
- ROC สูงสุด/ต่ำสุด = อาจมีการกลับตัว

---

### 4.3 Volatility Indicators (ตัวชี้วัดความผันผวน)

#### Bollinger Bands

```
Middle Band = SMA(20)
Upper Band = Middle Band + (2 × StdDev)
Lower Band = Middle Band - (2 × StdDev)
```

**การใช้:**

| ลักษณะ | ความหมาย |
|--------|----------|
| **Band บีบแคบ** | ความผันผวนต่ำ → รอ Breakout |
| **Band ขยาย** | ความผันผวนสูง → แนวโน้มแข็ง |
| **ราคาแตะ Upper Band** | Overbought potential |
| **ราคาแตะ Lower Band** | Oversold potential |
| **ราคาทะลุ Band** | Breakout signal |

**Bollinger Bounce:** ราคามักจะเด้งกลับจาก Band เข้าหา Middle Band
**Bollinger Squeeze:** Band บีบแคบ → เตรียมรอ Breakout ที่จะมา

#### ATR (Average True Range)

```
TR = max(High - Low, |High - Prev Close|, |Low - Prev Close|)
ATR = SMA(TR, 14)
```

**การใช้:**
- **วัดความผันผวน** — ATR สูง = ผันผวนสูง
- **ตั้ง Stop Loss:** `Stop = Entry - 1.5 × ATR`
- **ตั้ง Take Profit:** `Target = Entry + 2 × ATR`

#### Keltner Channels

```
Middle Line = EMA(20)
Upper Band = EMA(20) + (2 × ATR)
Lower Band = EMA(20) - (2 × ATR)
```
- ใช้ทำ **Breakout Strategy**
- ราคาปิดเกิน Band = สัญญาณ Breakout

#### Donchian Channels

```
Upper = Highest High (n periods)
Lower = Lowest Low (n periods)
Middle = (Upper + Lower) / 2
```
- ใช้ใน **Breakout Strategy**
- ราคาสูงกว่า Upper = สัญญาณซื้อ

---

### 4.4 Volume Indicators (ตัวชี้วัดปริมาณ)

#### OBV (On Balance Volume)

```
ถ้า Close > Prev Close: OBV += Volume
ถ้า Close < Prev Close: OBV -= Volume
ถ้า Close = Prev Close: OBV เท่าเดิม
```

**การใช้:**
- OBV ขึ้น = กระแสเงินไหลเข้า (Bullish)
- OBV ลง = กระแสเงินไหลออก (Bearish)
- **Divergence** ระหว่าง OBV กับราคา = เตือนการกลับตัว

#### VWAP (Volume Weighted Average Price)

```
VWAP = Σ(Price × Volume) / Σ(Volume)
```
- ราคาเฉลี่ยถ่วงน้ำหนักด้วยปริมาณ
- **ราคา > VWAP** = ขาขึ้น intraday
- **ราคา < VWAP** = ขาลง intraday
- ใช้เป็น **dynamic Support/Resistance**

#### Volume Profile

```
- แสดงปริมาณซื้อขายที่แต่ละราคา
- **Point of Control (POC):** ราคาที่มีปริมาณมากที่สุด
- **Value Area High/Low (VAH/VAL):** ช่วงที่มีปริมาณ 70% ของทั้งหมด
```

**การใช้:**
- ซื้อใกล้ POC = ราคาเป็นธรรม
- ราคาสูงกว่า VAH = ราคาแพง
- ราคาต่ำกว่า VAL = ราคาถูก

#### Chaikin Money Flow (CMF)

```
MFV = ((Close - Low) - (High - Close)) / (High - Low) × Volume
CMF = Σ(MFV, 20) / Σ(Volume, 20)
```

**ค่าความหมาย:**
- **CMF > 0** = กระแสเงินไหลเข้า (Bullish)
- **CMF < 0** = กระแสเงินไหลออก (Bearish)
- **CMF ≈ 0** = ความลังเล

#### MFI (Money Flow Index)

```
Raw Money Flow = Typical Price × Volume
Money Flow Ratio = Positive MF / Negative MF (14 periods)
MFI = 100 - (100 / (1 + Money Flow Ratio))
```

- RSI ของเงิน → คล้าย RSI แต่รวม Volume
- **> 80** = Overbought / **< 20** = Oversold

---

### 4.5 การรวมตัวชี้วัด (Indicator Combinations)

#### Combination 1: Trend Following

```
SMA 50 > SMA 200 (Golden Cross)  ← ยืนยันแนวโน้ม
+ ADX > 25                          ← ยืนยันแนวโน้มแข็ง
+ RSI อยู่ระหว่าง 40-60           ← ไม่ Overbought/Oversold
→ เปิด Long เมื่อราคาลงมาใกล้ SMA 50
```

#### Combination 2: Mean Reversion

```
RSI < 30 (Oversold)                 ← ราคาถูกเกินไป
+ Bollinger Bands แตะ Lower Band   ← ยืนยัน Oversold
+ Stochastic %K < 20                ← ยืนยัน Oversold
→ สัญญาณซื้อ
```

#### Combination 3: Momentum Breakout

```
Price > SMA 20                        ← แนวโน้มขึ้น
+ MACD ข้าม Signal ขึ้น              ← Momentum ขาขึ้น
+ Volume > Avg Volume 1.5x           ← Volume ยืนยัน
+ ATR สูงขึ้น                        ← ความผันผวนเพิ่ม
→ เปิด Long
```

#### Combination 4: RSI + MACD Divergence

```
RSI ทำ Higher Low (ราคาทำ Lower Low)  ← Bullish Divergence
+ MACD ยืนยัน Divergence               ← ยืนยันซ้ำ
+ Price อยู่ใกล้ Support               ← แนวรับแข็ง
→ สัญญาณซื้อ
```

---

## 5. ทฤษฎีตลาด (Market Theories)

### 5.1 Dow Theory

**หลักการพื้นฐานของ Dow Theory:**

1. **ดัชนีทุกอย่างสะท้อนทุกสิ่ง** — ราคาสะท้อนข้อมูลทั้งหมดแล้ว
2. **ตลาดมี 3 แนวโน้ม:**
   - **Primary Trend** (1 ปีขึ้นไป) — ขาขึ้น/ขาลงใหญ่
   - **Secondary Trend** (1 เดือน-3 เดือน) — การพักตัว
   - **Minor Trend** (น้อยกว่า 1 เดือน) — สัญญาณรบกวน
3. **แนวโน้มขาขึ้น:** HH + HL (Higher Highs + Higher Lows)
4. **แนวโน้มขาลง:** LH + LL (Lower Highs + Lower Lows)
5. **ยืนยันด้วย Volume** — Volume ควรเพิ่มในทิศทางแนวโน้ม

### 5.2 Elliott Wave Theory

**โครงสร้าง волны:**

```
Impulse Wave (5 волн):
  1) ─────── ↑
  2)    ↓    │ (Retracement 2 ลง แต่ > 100% ของ волны 1)
  3) ─────── ↑ (волныที่ยาวที่สุด)
  4)    ↓    │ (Retracement 4 ลง แต่ > 100% ของ волны 3)
  5) ─────── ↑

Corrective Wave (3 волн):
  A) ─────── ↓
  B)    ↑    │ (Retracement ขึ้น)
  C) ─────── ↓
```

**กฎของ Impulse Wave:**
1. Волна 2 ไม่ลงเกินจุดเริ่มต้น волна 1
2. Волна 3 ไม่ใช่ волнаที่สั้นที่สุด
3. Волна 4 ไม่ลงเกินจุดเริ่มต้น волна 3
4. Волна 3 มักยาวที่สุด

**Fibonacci ใน Elliott Wave:**

| ความสัมพันธ์ | Retracement |
|--------------|-------------|
| Волна 2 | 38.2%, 50%, 61.8% ของ Волна 1 |
| Волна 4 | 38.2%, 50%, 61.8% ของ Волна 3 |
| Волна 5 | 61.8%, 100%, 123.6% ของ Волна 4 |

### 5.3 Fibonacci Analysis

**Fibonacci Retracement:**

```
  0% (Low)
  │
  │  ──────────────────────── 100% (High)
  │                              │
  │    38.2% ────────────────────│
  │         │                    │
  │    50% ──────────────────────│
  │         │                    │
  │    61.8% ────────────────────│
  │         │                    │
  └─────────┴────────────────────┘
```

**ระดับ Retracement ที่สำคัญ:**
- **23.6%** — ระดับตื้น (shallow)
- **38.2%** — ระดับปานกลาง
- **50%** — Halfway (ไม่ใช่ Fibonacci แต่ใช้กันมาก)
- **61.8%** — Golden Ratio — **สำคัญที่สุด**
- **78.6%** — ระดับลึก (deep)

**Fibonacci Extension:**

```
  Extension levels:  127.2%   161.8%   261.8%   423.6%
                      │        │        │        │
  ────────────────────┴────────┴────────┴────────┴── High
  │
  └─────────────────────────────────────────── 100%
```

**การใช้งาน:**
1. ลากจาก Low ไป High = หา Retracement
2. ลากจาก High ไป Low = หา Extension
3. Retracement 61.8% = จุดซื้อที่ดีที่สุด

### 5.4 Market Cycles

**วัฏจักรของตลาด:**

```
  Expansion          Peak         Contraction        Trough
     │                │                │              │
     │   Recovery     │    Slowdown    │   Recession   │
     │                │                │              │
  ───┴────────────────┴────────────────┴──────────────┴──
     ↑                                                       
  Bottom (ขวากลับ)
```

**ประเภทวัฏจักร:**

| วัฏจักร | ความยาว | ตัวอย่าง |
|---------|---------|---------|
| **Kitchin** | 3-5 ปี | วัฏจักรสินค้าคงคลัง |
| **Juglar** | 7-11 ปี | วัฏจักรการลงทุน |
| **Kuznets** | 15-25 ปี | วัฏจักรอสังหาริมทรัพย์ |
| **Kondratieff** | 45-60 ปี | วัฏจักรเศรษฐกิจใหญ่ |

**Seasonality:**
- **January Effect** — ราคามักขึ้นในเดือน 1
- **Sell in May** — สถิติตลาดลงช่วง May-October
- **Q4 Rally** — ตลาดมักขึ้นช่วง Q4

---

## 6. การบริหารความเสี่ยง (Risk Management)

### 6.1 Position Sizing (การกำหนดขนาดสถานะ)

**Fixed Amount:**
```
Position Size = Fixed Amount (เช่น $1,000 ต่อสถานะ)
```
- ง่าย, ไม่ปรับตามความเสี่ยง
- ไม่ใช้กับพอร์ตเล็ก

**Fixed Percentage:**
```
Position Size = Portfolio Value × Risk %
         = $10,000 × 2% = $200
```
- ปรับตามขนาดพอร์ต
- ใช้ 1-2% ต่อสถานะ

**Volatility-Based Sizing:**
```
Position Size = (Account × Risk %) / ATR
         = ($10,000 × 0.02) / 100 = 2 units
```
- ใช้ ATR วัดความผันผวน
- ปรับขนาดตามสภาพตลาด

### 6.2 Kelly Criterion

```
f* = (b × p - q) / b
f* = Kelly %
b = อัตราส่วน Reward/Risk (เช่น 2:1 = 2)
p = ความน่าจะเป็นชนะ
q = 1 - p
```

**ตัวอย่าง:**
```
Win Rate = 55% (p = 0.55, q = 0.45)
Reward/Risk = 2:1 (b = 2)
f* = (2 × 0.55 - 0.45) / 2 = 0.325 = 32.5%

แต่ใช้ Half-Kelly = 16.25% เพื่อความปลอดภัย
```

**กฎ:**
- ใช้ **Half-Kelly** (หรือ Quarter-Kelly) ในทางปฏิบัติ
- Kelly สูงเกินไป = Drawdown สูง

### 6.3 Stop Loss Strategies

**Fixed Stop Loss:**
```
Stop = Entry - (Entry × 2%)
     = $100 - $2 = $98
```
- ง่าย, ไม่ปรับตามตลาด

**ATR-Based Stop:**
```
Stop = Entry - (1.5 × ATR)
     = $100 - (1.5 × $2) = $97
```
- ปรับตามความผันผวน
- ดีกว่า Fixed %

**Chandelier Exit:**
```
Stop = Highest High (22 days) - (3 × ATR)
```
- ตั้ง Stop ตาม High สูงสุดถอยหลัง
- ไม่โดน Volatility ปกติ

**Support/Resistance Stop:**
```
Stop = ใต้ Support ล่าสุด หรือ เหนือ Resistance สูงสุด
```
- วาง Stop นอกแนวที่เป็นไปได้

**Time-Based Stop:**
```
ออกหลังจากเปิดสถานะ X วันแล้วไม่ได้ผลตามที่คาด
```
- ใช้เมื่อไม่มี Signal ชัดเจน

### 6.4 Risk-Reward Ratio

```
Risk-Reward Ratio = (Entry - Stop) / (Target - Entry)

ตัวอย่าง:
  Entry = $100
  Stop = $98 (Risk = $2)
  Target = $106 (Reward = $6)
  R:R = $2 : $6 = 1:3

  Win Rate ที่คุ้มทุน = 1 / (1 + 3) = 25%
```

**ความหมาย:**

| R:R Ratio | Win Rate คุ้มทุน |
|-----------|-----------------|
| 1:1 | 50% |
| 1:2 | 33% |
| 1:3 | 25% |
| 1:4 | 20% |

**กลยุทธ์:** ยิ่ง R:R สูง ยิ่งต้องการ Win Rate ต่ำ

### 6.5 Drawdown Management

```
Drawdown = (Peak - Trough) / Peak × 100%
```

**กฎ:**

| Drawdown | ต้องทำกำไรกี่% เพื่อกลับมาเท่าเดิม |
|----------|----------------------------------|
| 10% | 11% |
| 25% | 33% |
| 50% | 100% |
| 75% | 300% |

**การจำกัด Drawdown:**
1. **Max Drawdown ต่อสถานะ:** 1-2%
2. **Max Drawdown ต่อวัน:** 3-5%
3. **Max Drawdown รวม:** 10-20%
4. **Reduce Position** เมื่อ Drawdown ใกล้ขีดจำกัด

### 6.6 Portfolio Diversification

**กระจายตามประเภทสินทรัพย์:**
```
60% Equities (Stocks)
20% Fixed Income (Bonds)
10% Commodities (Gold)
10% Cash
```

**กระจายตามภูมิศาสตร์:**
```
40% Domestic
30% Developed Markets
20% Emerging Markets
10% Other
```

**Correlation:**
- เลือกสินทรัพย์ที่ **Correlation ต่ำ** กัน
- ถ้า Correlation สูง = พอร์ตลดลงเหมือนสินทรัพย์เดียว

---

## 7. กลยุทธ์การเทรด (Trading Strategies)

### 7.1 Mean Reversion (กลับสู่ค่าเฉลี่ย)

**หลักการ:** ราคาที่เบี่ยงเบนจากค่าเฉลี่ยมากๆ จะกลับมาที่ค่าเฉลี่ย

**RSI Mean Reversion:**
```
Signal: RSI < 30 (Oversold)
Entry: ซื้อเมื่อ RSI > 40 (กลับออกจาก Oversold)
Stop: ใต้ Low ของวันที่เข้า
Target: Middle Band ของ Bollinger หรือ 1:2 R:R
```

**Bollinger Band Bounce:**
```
Signal: ราคาแตะ Lower Band
Entry: ซื้อเมื่อราคาเด้งกลับเข้าหา Middle Band
Stop: ใต้ Lower Band
Target: Middle Band หรือ Upper Band
```

**MA Pullback:**
```
Signal: Uptrend (Price > SMA 200)
Entry: ซื้อเมื่อราคาลงมาแตะ SMA 50 แล้วเด้ง
Stop: ใต้ SMA 50
Target: High เดิม หรือ 1:3 R:R
```

### 7.2 Momentum / Breakout (แนวโน้ม)

**หลักการ:** ราคาที่วิ่งแรงจะวิ่งต่อ

**Breakout Strategy:**
```
Signal: Price ปิดเหนือ Resistance + Volume > Avg × 1.5
Entry: ซื้อที่ราคาปิด + 0.5% Buffer
Stop: ใต้ Resistance (หรือ Low ของวันก่อน)
Target: Height ของ Range + จุดหลุด
```

**Momentum Strategy:**
```
Signal: 
  1. SMA 50 > SMA 200 (Uptrend)
  2. RSI อยู่ระหว่าง 50-70 (ไม่ Overbought)
  3. MACD > 0 และ MACD > Signal

Entry: ซื้อเมื่อ RSI > 60
Stop: ใต้ SMA 50
Target: 1:2 R:R
```

**ADX Trend Following:**
```
Signal: ADX > 25 (แนวโน้มแข็ง)
  +DI > -DI (Uptrend)

Entry: ซื้อเมื่อ Pullback สัมผัส SMA 20
Stop: ใต้ Low ของ Pullback
Target: 1:2 ถึง 1:3 R:R
```

### 7.3 Grid Trading

**หลักการ:** วาง Orders ที่ระดับราคาห่างเท่าๆ กัน

```
Grid Lines:  $95  $97  $99  $101  $103  $105
              │   │    │    │    │    │
         ────┴───┴────┴────┴────┴────┴────
         Buy    Buy    Neutral  Sell  Sell
         Grid   Grid           Grid  Grid
```

**Grid Trading Strategy:**
```
1. กำหนดช่วงราคา (Range) — ใช้ Support/Resistance
2. กำหนดจำนวน Grid (เช่น 10 ระดับ)
3. วาง Buy Limit Orders ที่ Grid ด้านล่าง
4. วาง Sell Limit Orders ที่ Grid ด้านบน
5. เมื่อราคาขึ้นผ่าน Grid → ขาย + วาง Sell ที่ Grid ถัดไป
6. เมื่อราคาลงผ่าน Grid → ซื้อ + วาง Buy ที่ Grid ถัดไป
```

**ข้อดี:** ไม่ต้องทำนายทิศทาง
**ข้อเสีย:** ต้องมีทุนมาก, ไม่ดีใน Trend ทิศทางเดียว

### 7.4 Dollar-Cost Averaging (DCA)

**หลักการ:** ซื้อสินทรัพย์เป็นงวดๆ ไม่สนใจราคา

```
ทุกเดือน: ซื้อ $500 BTC
ไม่สนใจราคา สูงหรือต่ำ
```

**DCA vs Lump Sum:**
- **Lump Sum:** ดีกว่าในตลาดขาขึ้น
- **DCA:** ดีกว่าในตลาดผันผวน, ลดความเสี่ยงจากจังหวะ

### 7.5 Pairs Trading

**หลักการ:** เทรดความสัมพันธ์ระหว่าง 2 สินทรัพย์

```
สมมติ: BTC และ ETH Correlation = 0.85

1. คำนวณ Spread = BTC - (β × ETH)
2. เมื่อ Spread สูงกว่า Normal → Short BTC, Long ETH
3. เมื่อ Spread กลับมา Normal → ปิดสถานะ
```

**ข้อดี:** ลดความเสี่ยงตลาด (Market Neutral)

### 7.6 Smart Money Concepts (SMC)

**หลักการ:** ติดตาม "เงินอัจฉริยะ" (Institutions)

**Order Blocks:**
```
- บริเวณที่ Institutions วาง Orders ขนาดใหญ่
- มักเป็นแท่งเทียน 1-3 แท่นก่อน Trend ขนาดใหญ่
- ใช้เป็น Support/Resistance
```

**Fair Value Gap (FVG):**
```
- Gap ระหว่างแท่งเทียน 2 แท่น
- Gap = บริเวณที่ราคาว่างเปล่า
- ราคามักกลับมาเติม Gap (Fill the Gap)
```

**Inducement:**
```
- Institutions อาจ "หลอก" ให้ Retail เข้าผิดทาง
- สร้าง "Inducement" = หลอกให้ Buy/Sell ก่อน
- แล้วราคากลับตัวในทิศทางที่ Institutions ต้องการ
```

---

## 8. AI/ML สำหรับการเทรด

### 8.1 Feature Engineering

**สำหรับ Time Series แบบเทคนิค:**

```python
features = [
    # Price-based
    "returns",              # ผลตอบแทนรายวัน
    "log_returns",          # Log returns
    "high_low_ratio",       # High/Low ratio
    
    # Technical Indicators
    "sma_20", "sma_50", "sma_200",
    "ema_12", "ema_26",
    "rsi_14",
    "macd", "macd_signal", "macd_histogram",
    "bb_upper", "bb_middle", "bb_lower",
    "atr_14",
    "stochastic_k", "stochastic_d",
    
    # Pattern features
    "candle_body_size",     # ขนาดตัวแท่ง
    "candle_wick_ratio",    # อัตราส่วนไส้/ตัว
    "gap_size",             # ขนาด Gap
    
    # Volume features
    "volume", "volume_sma",
    "obv",
    "vwap_distance",
    
    # Time features
    "hour", "day_of_week",  # สำหรับ Crypto (24/7)
    "month",                # สำหรับ Stock
]
```

### 8.2 Model Types

#### LSTM (Long Short-Term Memory)

```
โครงสร้าง:
Input → LSTM Layer × N → Dense → Output
       ↑
   Memory Cell จำค่าจาก N steps ก่อนได้

ใช้สำหรับ:
- ทำนายราคาวันถัดไป
- จับ Pattern ของ Sequence
```

```python
# Pseudocode LSTM
model = Sequential([
    LSTM(100, input_shape=(60, 10)),  # 60 timesteps, 10 features
    Dropout(0.2),
    LSTM(50),
    Dropout(0.2),
    Dense(1, activation='linear')     # ทำนายราคา
])
model.compile(loss='mse', optimizer='adam')
```

#### Transformer

```
โครงสร้าง:
Input Embedding → Multi-Head Attention → Feed Forward → Output
                    ↑
            Self-Attention: Query, Key, Value

ใช้สำหรับ:
- จับ long-range dependencies
- ดีกว่า LSTM ในหลายงาน
```

#### CNN for Time Series

```
โครงสร้าง:
Input (Price Matrix) → Conv1D → Pooling → Conv1D → Dense → Output
     3D: (timesteps, features, channels)

ใช้สำหรับ:
- จำ Pattern ของ Candlestick
- จับ Chart Patterns แบบ Visual
```

### 8.3 Pattern Recognition with CNN

```python
# แปลงกราฟเป็น Image
def chart_to_image(ohlcv_data, window=60):
    # สร้างรูป 60×60 pixels
    # Y-axis = ราคา, Color = OHLC
    # คล้ายกราฟ Candlestick
    return image  # 60×60×3

# ใช้ CNN จำ Pattern
model = Sequential([
    Conv2D(32, (3,3), activation='relu'),
    MaxPooling2D((2,2)),
    Conv2D(64, (3,3), activation='relu'),
    Flatten(),
    Dense(10, activation='softmax')  # 10 patterns
])
```

### 8.4 Sentiment Analysis

```python
# ดึงข่าว/Social Media
news = fetch_news(symbol)
sentiment = model.predict(news)  # -1 ถึง +1

# ใช้ Sentiment ร่วมกับ Technical
if technical_signal == "BUY" and sentiment > 0.5:
    confidence += 1
```

### 8.5 Reinforcement Learning (RL)

```python
# Q-Learning / Policy Gradient
class TradingAgent:
    def __init__(self, state_size, action_size):
        self.q_network = NeuralNetwork(state_size, action_size)
    
    def act(self, state):
        # State: [price, indicators, position, pnl, ...]
        # Action: 0=Hold, 1=Buy, 2=Sell
        return self.q_network.forward(state)
    
    def train(self, state, action, reward, next_state):
        # Update Q-network
        loss = self.compute_loss(state, action, reward, next_state)
        self.q_network.backward(loss)
```

### 8.6 แนวทางในโปรเจกต์ Auto Trade AI

```
โครงสร้าง AI Signal Generator ของโปรเจกต์:

┌─────────────────────────────────────────────────────────┐
│  AI Signal Generator                                    │
│                                                          │
│  1. ดึงข้อมูลราคา (CCXT / Gold Feed)                     │
│  2. คำนวณ Indicators (RSI, MACD, Bollinger, etc.)      │
│  3. วิเคราะห์ Pattern (Head & Shoulders, Triangle, etc.)│
│  4. รวม Signal → Technical Score                         │
│  5. เพิ่ม Sentiment (ถ้ามีข้อมูล)                       │
│  6. LLM สร้าง Signal + คำอธิบาย                         │
│  7. → Signal: BUY / SELL / HOLD + Confidence + Reasons  │
└─────────────────────────────────────────────────────────┘
```

---

## 9. การนำไปใช้ในโปรเจกต์

### 9.1 โครงสร้าง Signal Generator

```python
# src/ai/signal_generator.py (ปัจจุบัน)
class SignalGenerator:
    def generate(self, symbol, data):
        # ใช้ LLM สร้าง Signal
        # ปรับปรุง: เพิ่ม Technical Analysis ก่อน
        
# โครงสร้างที่ควรเป็น:
class SignalGenerator:
    def generate(self, symbol, data):
        # 1. คำนวณ Indicators
        indicators = self.compute_indicators(data)
        
        # 2. ตรวจจับ Patterns
        patterns = self.detect_patterns(data)
        
        # 3. Technical Score
        score = self.technical_score(indicators, patterns)
        
        # 4. ใช้ LLM รวมข้อมูล
        signal = self.llm_signal(symbol, score)
        
        return signal
```

### 9.2 สิ่งที่ควรเพิ่มในโปรเจกต์

#### ระดับที่ 1 — Indicators (ง่าย)
```python
# เพิ่ม RSI, MACD, Bollinger Bands
import ta

rsi = ta.momentum.RSIIndicator(close, window=14).rsi()
macd = ta.trend.MACD(close)
bollinger = ta.volatility.BollingerBands(close)
```

#### ระดับที่ 2 — Pattern Detection (ปานกลาง)
```python
# เพิ่ม Pattern Recognition
from ta.trend import ADXIndicator
from ta.volume import OnBalanceVolumeIndicator

# ตรวจจับ Candlestick Patterns
def detect_engulfing(candles):
    # ตรวจ engulfing pattern
    pass
```

#### ระดับที่ 3 — ML Model (ยาก)
```python
# เพิ่ม LSTM Model
import torch

model = LSTMModel(input_size=10, hidden_size=64, num_layers=2)
prediction = model(X_train)
```

### 9.3 Tech Stack ที่แนะนำ

| ส่วน | เครื่องมือ |
|------|-----------|
| **Data** | pandas, numpy, CCXT |
| **Indicators** | ta-lib / ta |
| **ML/DL** | PyTorch, TensorFlow, scikit-learn |
| **Pattern Detection** | CNN (PyTorch), OpenCV |
| **LLM Integration** | OpenAI API, Claude API |
| **Backtesting** | backtrader, vectorbt |
| **Real-time Data** | CCXT, WebSocket |
| **Database** | SQLite, PostgreSQL |
| **Frontend** | Next.js, lightweight-charts, recharts |

### 9.4 ขั้นตอนการพัฒนา

```
Phase 1: Technical Indicators
├── เพิ่ม RSI, MACD, Bollinger Bands, ATR
├── สร้าง Scoring System
└── ทดสอบ Backtest

Phase 2: Pattern Recognition
├── ตรวจจับ Candlestick Patterns (Doji, Hammer, Engulfing, etc.)
├── ตรวจจับ Chart Patterns (Double Top/Bottom, Triangle, etc.)
└── รวมเข้ากับ Scoring System

Phase 3: AI Enhancement
├── เพิ่ม LLM Signal Generator
├── เพิ่ม Sentiment Analysis
└── เพิ่ม News Sentiment

Phase 4: ML Models
├── สร้าง LSTM/Transformer ทำนายราคา
├── สร้าง CNN ตรวจจับ Pattern จากกราฟ
└── รวม ML Predictions เข้ากับ Signal

Phase 5: Production
├── ต่อ Live Data (CCXT)
├── ต่อ Broker API
├── ระบบ Alert และ Monitoring
└── Deploy
```

---

## สรุป

การวิเคราะห์ทางเทคนิคเป็นศาสตร์ที่กว้างขวาง การใช้งานจริงควร:

1. **เริ่มจากพื้นฐาน** — เรียนรู้ Candlestick Patterns, Support/Resistance, Trendlines ก่อน
2. **เลือก Indicators 2-3 อย่าง** — ไม่ต้องใช้ทุกอย่าง (RSI, MACD, Bollinger เพียงพอ)
3. **ใช้ Volume ยืนยัน** — Volume เป็นตัวยืนยันที่สำคัญที่สุด
4. **บริหารความเสี่ยง** — Stop Loss, Position Sizing, Risk-Reward Ratio
5. **Backtest ก่อนใช้จริง** — ทดสอบ Strategy กับข้อมูลย้อนหลัง
6. **ปรับปรุงเรื่อยๆ** — ตลาดเปลี่ยน ต้องปรับตัว

---

*เอกสารนี้จัดทำเพื่อการศึกษา การลงทุนมีความเสี่ยง ผู้ลงทุนควรศึกษาข้อมูลอย่างรอบคอบก่อนตัดสินใจ*
