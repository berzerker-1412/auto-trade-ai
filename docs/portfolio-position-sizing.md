# การสร้างพอร์ตโฟลิโอและการกำหนดขนาดสถานะ (Portfolio Construction & Position Sizing)

## 1. Kelly Criterion

### ที่มาและหลักการ
Kelly Criterion พัฒนาโดย John Larry Kelly Jr. ในปี 1956 เป็นทฤษฎีทางคณิตศาสตร์สำหรับการจัดการเงินทุน (bankroll management) ในการพนันและการลงทุน สูตรพื้นฐานคือ:

**f* = (bp - q) / b**

โดยที่:
- f* = สัดส่วนเงินทุนที่ควรเดิมพัน/ลงทุน
- b = อัตราส่วนกำไรต่อขาดทุน (odds)
- p = ความน่าจะเป็นที่จะชนะ
- q = ความน่าจะเป็นที่จะแพน = 1 - p

### สูตรแบบง่ายสำหรับการเทรด:
**Kelly % = W - (1 - W) / R**

โดยที่:
- W = Win rate (อัตราการชนะ)
- R = Win/Loss Ratio (อัตราส่วนกำไรเฉลี่ยต่อขาดทุนเฉลี่ย)

### ตัวอย่าง:
- Win rate = 40% (W = 0.40)
- Average win = $100
- Average loss = $50
- R = 100/50 = 2

Kelly % = 0.40 - (0.60 / 2) = 0.40 - 0.30 = 0.10 = 10%

### Half-Kelly Rule
เนื่องจาก Kelly แบบเต็มมีความผันผวนสูงมาก นักลงทุนส่วนใหญ่ใช้ "Half-Kelly" (ครึ่งหนึ่งของ Kelly) เพื่อลดความเสี่ยง ในตัวอย่างข้างต้น = 5% ของพอร์ตต่อสถานะ

### ข้อจำกัด
1. ต้องการประมาณค่า win rate และ R ได้แม่นยำ
2. ความผันผวนสูง - ไม่เหมาะกับนักลงทุนทั่วไป
3. ให้ขนาดสถานะที่ใหญ่เกินไปในบางกรณี
4. ไม่คำนึงถึง correlation ระหว่างสถานะ

---

## 2. Risk Parity (การกระจายความเสี่ยง)

### หลักการ
Risk Parity กระจายความเสี่ยง (ไม่ใช่เงินทุน) อย่างเท่าเทียมกันระหว่างสินทรัพย์/สถานะต่างๆ แนวคิดหลักคือทุกสินทรัพย์ควรมีส่วนร่วมในความเสี่ยงของพอร์ตเท่ากัน

### วิธีคำนวณ
1. คำนวณ volatility (ความผันผวน) ของแต่ละสินทรัพย์
2. กำหนดเป้าหมายความเสี่ยงรวมของพอร์ต
3. หาสัดส่วนการลงทุน = (เป้าหมายความเสี่ยง / จำนวนสินทรัพย์) / volatility ของสินทรัพย์นั้น

### สูตร:
Weight = (Target Portfolio Risk / N) / Asset Volatility

โดย N = จำนวนสินทรัพย์

### ตัวอย่าง:
- พอร์ตมี 3 สินทรัพย์
- เป้าหมายความเสี่ยงรวม = 15%
- Volatility A = 20%, B = 10%, C = 5%

Weight A = (15% / 3) / 20% = 2.5% / 0.20 = 12.5%
Weight B = (15% / 3) / 10% = 2.5% / 0.10 = 25%
Weight C = (15% / 3) / 5% = 2.5% / 0.05 = 50%

### ข้อดี
- สร้างพอร์ตที่มี Sharpe Ratio ดี
- ลดการพึ่งพาสินทรัพย์ที่มีความผันผวนสูง
- เหมาะกับการกระจายความเสี่ยงระยะยาว

### ข้อเสีย
- ต้องใช้ leverage เพื่อเพิ่มผลตอบแทน (เพราะสินทรัพย์ที่ปลอดภัยมักให้ผลต่ำ)
- ต้อง rebalance บ่อย

---

## 3. Fixed Ratio (อัตราส่วนคงที่)

### หลักการ
Fixed Ratio พัฒนาโดย Ryan Jones ใช้กำไรสะสมเป็นตัวกำหนดขนาดสถานะ แทนที่จะใช้เปอร์เซ็นต์คงที่ของพอร์ต

### สูตร:
**Position Size = Delta * (1 + 2 * Accumulated Profit / Delta)^0.5**

โดย Delta = จำนวนเงินที่ต้องการต่อหน่วยการเทรด

### วิธีใช้งาน:
1. กำหนด Delta (เช่น $1,000 ต่อสัญญา)
2. เมื่อกำไรสะสมเพิ่มขึ้น ขนาดสถานะจะเพิ่มขึ้น
3. เมื่อขาดทุน ขนาดสถานะจะลดลง

### ตัวอย่าง:
- Delta = $1,000
- Accumulated Profit = $5,000
- Position = 1000 * (1 + 2*5000/1000)^0.5 = 1000 * (1 + 10)^0.5 = 1000 * 3.32 = 3.32 สัญญา (ปัดเป็น 3)

### ข้อดี
- ป้องกันการขาดทุนหนักเพราะขนาดสถานะลดเมื่อพอร์ตลด
- ростаช้าลงเมื่อมีกำไร (safer than fixed fraction)

### ข้อเสีย
- ซับซ้อนกว่า fixed fraction
- ต้องติดตาม accumulated profit ตลอด

---

## 4. Optimal F

### หลักการ
Optimal F พัฒนาโดย Ralph Vince คล้าย Kelly แต่ใช้ข้อมูลจริงจากผลการเทรดในอดีต หาค่า F ที่ maximizes เทอร์มินัล wealth

### วิธีคำนวณ:
1. รวบรวมผลการเทรดทั้งหมด (HPRs - Holding Period Returns)
2. ทดสอบค่า F หลายๆ ค่า (เช่น 0.01 ถึง 1.00)
3. เลือก F ที่ให้ TWR (Terminal Wealth Relative) สูงสุด

### สูตร TWR:
TWR = Product of (1 + F * HPR_i)

โดย HPR_i = ผลตอบแทนจากการเทรดครั้งที่ i

### ตัวอย่าง:
ผลการเทรด: +$100, -$50, +$200, -$30, +$150
ทดสอบ F = 0.1, 0.2, 0.3...

สมมติ F = 0.2:
HPRs: 1 + 0.2*(100/500), 1 + 0.2*(-50/500), ...
TWR = (1.04) * (0.98) * (1.08) * (0.988) * (1.06)

### ข้อจำกัด
1. ใช้ข้อมูลในอดีต - ไม่รับประกันอนาคต
2. ให้ค่า aggressive สูงเหมือน Kelly
3. ต้องใช้ Monte Carlo simulation เพื่อความแม่นยำ

---

## 5. Correlated Position Sizing (การกำหนดขนาดสถานะแบบมีสหสัมพันธ์)

### หลักการ
เมื่อสถานะในพอร์ตมี correlation กัน การรวมสถานะที่มี correlation สูงจะเพิ่มความเสี่ยงรวมมากกว่าผลรวมของความเสี่ยงแต่ละสถานะ

### Correlation Adjustment:
**Effective Position Size = Individual Size * sqrt(Correlation)**

ถ้า correlation = 1.0: Effective size = Individual size * 1.0
ถ้า correlation = 0.5: Effective size = Individual size * 0.707
ถ้า correlation = 0.0: Effective size = Individual size * 0.0

### Variance of Portfolio:
σ²_p = Σᵢ Σⱼ wᵢ wⱼ σᵢ σⱼ ρᵢⱼ

โดย ρᵢⱼ = correlation ระหว่างสถานะ i และ j

### วิธีปฏิบัติ:
1. คำนวณ correlation matrix ของสถานะทั้งหมด
2. ลดขนาดสถานะเมื่อ correlation สูง
3. ใช้หลักการ: ถ้ามี 5 สถานะที่มี correlation 0.8 กัน ให้ตัดขนาดลงประมาณ 40-50%

### Diversification Benefit:
- Correlation 0.0 ระหว่าง 2 สถานะ = ลดความเสี่ยงได้มากที่สุด
- Correlation 1.0 = ไม่มี benefit ในการกระจาย
- Correlation -1.0 = สามารถ hedge ได้สมบูรณ์

---

## 6. Drawdown Management (การจัดการ Drawdown)

### คำจำกัดความ
Drawdown = การลดลงของพอร์ตจากจุดสูงสุด (peak to trough decline)

### ประเภท:
1. **Absolute Drawdown** = จำนวนเงินที่ขาดทุนสะสม
2. **Relative Drawdown** = เปอร์เซ็นต์จาก peak
3. **Maximum Drawdown (Max DD)** = drawdown ที่ใหญ่ที่สุดในช่วงเวลาที่วิเคราะห์

### กฎทั่วไปในการจัดการ:
**Risk per Trade ≤ Max Acceptable DD / (Average Losses per Losing Trade)**

ตัวอย่าง:
- Max Acceptable DD = 20%
- Average Loss = 2%
- Risk per Trade ≤ 20% / (ขาดทุนเฉลี่ยต่อครั้ง)

ถ้าขาดทุนเฉลี่ย 2% ต่อครั้ง = 20% / 2% = 10 ครั้งติดต่อกันที่ยังอยู่ในกรอบ

### Drawdown Recovery:
ถ้าขาดทุน 20% ต้องการกำไร 25% เพื่อกลับไป break even
สูตร: Required Gain = DD / (1 - DD)
= 0.20 / 0.80 = 0.25 = 25%

### กลยุทธ์จำกัด Drawdown:
1. **Position Sizing** - ลดขนาดเมื่อ drawdown เพิ่มขึ้น
2. **Stop Loss** - ตั้ง max loss ต่อสถานะ
3. **Correlation Limits** - จำกัด exposure เมื่อสถานะ highly correlated
4. **Circuit Breakers** - หยุดเทรดชั่วคราวเมื่อถึงเกณฑ์

---

## 7. Portfolio Risk Limits (ขีดจำกัดความเสี่ยงพอร์ต)

### VaR (Value at Risk)
ประมาณการความสูญเสียสูงสุดที่อาจเกิดในช่วงเวลาหนึ่ง ที่ระดับความเชื่อมั่นหนึ่ง

ตัวอย่าง: VaR 95%, 1 วัน = $10,000
= 95% แน่ใจว่าจะไม่ขาดทุนเกิน $10,000 ใน 1 วัน

### วิธีคำนวณ:
1. **Historical** - ใช้ข้อมูลในอดีต
2. **Variance-Covariance** - สมมติ normal distribution
3. **Monte Carlo** - จำลองสถานการณ์หลายๆ แบบ

### Risk Limits ที่ควรตั้ง:
| Limit | Typical Range |
|-------|---------------|
| Max Position Size | 2-5% ของพอร์ต |
| Max Sector Exposure | 20-30% |
| Max Correlation Exposure | หลีกเลี่ยง >0.7 |
| Max Daily Loss | 2-3% ของพอร์ต |
| Max Drawdown | 10-20% |
| VaR (95%, 1-day) | <2% ของพอร์ต |

### Stop-Out Rules:
- **Daily Stop** - หยุดเทรดวันนั้นเมื่อขาดทุนถึงระดับ
- **Weekly Stop** - หยุดสัปดาห์เมื่อขาดทุนสะสมถึงระดับ
- **Trailing Stop** - ปรับ stop loss ขึ้นตาม profit

---

# จิตวิทยาการเทรดและการเงินเชิงพฤติกรรม (Trading Psychology & Behavioral Finance)

## 1. Cognitive Biases (อคติทางปัญญา)

### 1.1 Loss Aversion (ความเกลียดการขาดทุน)

**นิยาม:** ความเจ็บปวดจากการขาดทุนรุนแรงกว่าความสุขจากกำไรเท่ากันประมาณ 2-2.5 เท่า (ตาม Prospect Theory ของ Kahneman & Tversky)

**ผลกระทบต่อการเทรด:**
- เก็บกำไรเร็วเกินไป (cut winners too early)
- ถือขาดทุนไว้นานเกินไป (ride losers too long)
- ไม่ยอมรับ small losses - รอจน loss ใหญ่ขึ้น
- เปลี่ยนแผนเพราะความกลัว (fear-driven decisions)

**วิธีแก้ไข:**
1. ตั้ง stop loss ล่วงหน้าและยึดมั่น
2. ใช้ position sizing ที่เหมาะสม (loss ที่ยอมรับได้)
3. ทำ trade plan ก่อนเข้าเทรด
4. บันทึกผลการเทรดและวิเคราะห์อย่างเป็นระบบ

### 1.2 Confirmation Bias (อคติยืนยัน)

**นิยาม:** มีแนวโน้มที่จะแสวงหาข้อมูลที่สนับสนุนความเชื่อเดิม และเพิกเฉยข้อมูลที่ขัดแย้ง

**ผลกระทบต่อการเทรด:**
- อ่านเฉพาะบทวิเคราะห์ที่สนับสนุนมุมมองตัวเอง
- ไม่ปรับแผนเมื่อมีข้อมูลใหม่
- ตีความข้อมูลในแง่ดีเกินไป
- มองหา buy signals หลังจากมี position แล้ว

**วิธีแก้ไข:**
1. ค้นหาข้อมูลที่ขัดแย้งโดยเจตนา
2. ใช้ checklist ในการตัดสินใจ
3. มี mentor หรือ accountability partner ที่ตรงไปตรงมา
4. ทำ journaling อย่างตรงไปตรงมา

### 1.3 Anchoring Bias (อคติยึดติด)

**นิยาม:** มีแนวโน้มที่จะให้น้ำหนักกับข้อมูลแรกที่ได้รับมากเกินไป

**ผลกระทบต่อการเทรด:**
- ติดอยู่กับราคาเข้าซื้อ (cost anchor)
- รอราคาถึง "ราคาที่ควรจะเป็น" ที่ไม่มีเหตุผล
- ไม่ปรับ targets เมื่อ fundamentals เปลี่ยน
- เปรียบเทียบกับ entry price แทนที่จะดู fair value

**ตัวอย่าง:**
- ซื้อที่ $50 และรอขายที่ $60 แม้ fair value = $40
- ถือ position ที่ขาดทุนเพราะ "เคยขึ้นไปถึง $55"

**วิธีแก้ไข:**
1. ใช้ absolute valuation methods
2. ปรับ targets ตาม new information
3. ถามว่า "ถ้าไม่มี position นี้ จะซื้อที่ราคานี้ไหม?"

### 1.4 Availability Bias (อคติความพร้อมใช้)

**นิยาม:** ประมาณความน่าจะเป็นจากความง่ายในการนึกภาพ ไม่ใช่ความถี่ที่แท้จริง

**ผลกระทบ:**
- กลัวเหตุการณ์ที่มีการรายงานมาก (plane crash, market crash)
- ไม่ลงทุนเพราะเห็นข่าวร้ายบ่อย
- ป недооценка risks ที่ไม่ค่อยมีข่าว

### 1.5 Recency Bias (อคติความจำเห็นใหม่)

**นิยาม:** ให้น้ำหนักกับเหตุการณ์ล่าสุดมากเกินไป

**ผลกระทบ:**
- คิดว่า trend จะดำเนินต่อเพราะ "trend ยังไม่เปลี่ยน"
- ละเลย reversal signals
- เปลี่ยน strategy บ่อยเกินไปหลังจาก losses

**วิธีแก้ไข:**
- ใช้ multi-timeframe analysis
- ดูผลการเทรดในระยะยาว ไม่ใช่แค่ recent trades
- มี written trading plan

### 1.6 Overconfidence Bias (อคติมั่นใจเกิน)

**นิยาม:** ประเมินความสามารถตัวเองสูงเกินไป

**ผลกระทบ:**
- เทรดใหญ่เกินไป
- ไม่ใช้ stop loss
- ไม่ทำ research เพียงพอ
- เชื่อว่า "ควบคุม" ตลาดได้

---

## 2. Backtesting Pitfalls (ข้อผิดพลาดในการทำ Backtest)

### 2.1 Overfitting (การ overfit)

**นิยาม:** ปรับ strategy ให้ fit กับข้อมูลในอดีตมากเกินไป จนไม่สามารถ generalize ไปใช้ในอนาคตได้

**สัญญาณ:**
- Strategy มี rules เยอะมาก
- มี parameters หลายตัวที่ "tuned"
- ผล backtest สวยเกินไป (too good to be true)
- Forward test หรือ live ผลต่างจาก backtest มาก

**วิธีป้องกัน:**
1. **Out-of-sample testing** - แบ่งข้อมูล train/test
2. **Walk-forward analysis** - ทดสอบแบบ rolling
3. **Simple is better** - ใช้ rules น้อยที่สุด
4. **Monte Carlo simulation** - ทดสอบความ robustness

### 2.2 Look-Ahead Bias (อคติมองไปข้างหน้า)

**นิยาม:** ใช้ข้อมูลที่ยังไม่มีในเวลานั้นในการตัดสินใจ

**ตัวอย่าง:**
- ใช้ earnings data ที่ประกาศแล้วก่อนวันที่ประกาศ
- ใช้ closing price ของวันเดียวกัน (ซึ่งยังไม่รู้ตอนเทรด intraday)
- ใช้ data ที่ revised แล้ว

**วิธีป้องกัน:**
- ใช้ only available data at each point in time
- ตรวจสอบ timestamp ของ data
- ใช้ point-in-time data

### 2.3 Survival Bias (อคติความอยู่รอด)

**นิยาม:** เลือกดูแค่ "ผู้รอดชีวิต" ไม่สนใจ "ผู้เสียชีวิต"

**ตัวอย่าง:**
- วิเคราะห์หุ้นใน S&P 500 ปัจจุบัน - ไม่รวมหุ้นที่เคยอยู่ใน index แล้วล้มหายตายจาก
- ดูแค่กองทุนที่ยังมีอยู่ ไม่ดูกองที่ปิดตัวไปแล้ว
- ทำ backtest แค่ on symbols ที่ยังมีอยู่

### 2.4 Transaction Costs Oversight

**ปัญหา:**
- ไม่รวม spread, commission, slippage
- หรือใช้ค่าใช้จ่ายที่ต่ำเกินไป
- ไม่รวม impact ของตลาด (market impact)

**ผลกระทบ:**
- Strategy ที่ใช้ได้ใน backtest อาจขาดทุนจริง
- High-frequency strategies มีปัญหามากที่สุด

**วิธีแก้ไข:**
- ใช้ conservative estimates
- รวม bid-ask spread
- ปรับ slippage ตาม liquidity

### 2.5 Time Period Bias

**ปัญหา:**
- ทดสอบในช่วงเวลาที่เอื้ออำนวยเกินไป
- ไม่ทดสอบในตลาดขาลงหรือ sideways
- ผล backtest ขึ้นกับช่วงเวลาที่เลือก

**วิธีป้องกัน:**
- ทดสอบในหลายๆ ช่วงเวลา
- รวม periods ที่ยากลำบาก (2008, 2020, etc.)
- ใช้ rolling windows

### 2.6 Data Snooping (การส่องข้อมูล)

**นิยาม:** ทดสอบ hypotheses หลายตัวจนกว่าจะเจอตัวที่ works โดยบังเอิญ

**ผลกระทบ:**
- Strategy ที่ไม่มี edge จริงดูเหมือนมี edge
- p-hacking ในการเทรด

**วิธีป้องกัน:**
- กำหนด rules ก่อนดูข้อมูล
- ใช้ statistical significance tests
- ทดสอบบน out-of-sample data

---

## 3. Trade Journaling (การบันทึกสมุดบันทึกการเทรด)

### ความสำคัญ
สมุดบันทึกการเทรดเป็นเครื่องมือสำคัญในการพัฒนาตัวเอง ช่วยระบุ:
- Strengths และ weaknesses
- Patterns ที่ซ้ำๆ
- Emotional triggers
- ประสิทธิภาพของ strategy

### สิ่งที่ควรบันทึก:

#### ก่อนเข้าเทรด:
- เหตุผลในการเข้า (thesis)
- ราคาเข้า, stop loss, target
- Position size และเหตุผล
- Timeframe
- ความเชื่อมั่น (1-10)

#### หลังออกจากสถานะ:
- ผลลัพธ์จริง (P&L)
- ราคาออก
- ระยะเวลาถือ
- ดำเนินการตาม plan ไหม?
- อารมณ์ขณะเทรด
- สิ่งที่เรียนรู้

### ตัวอย่าง Format:

```
Date: 2024-01-15
Symbol: AAPL
Direction: Long
Entry: $185.50
Stop: $182.00
Target: $192.00
Size: 100 shares
Thesis: Breakout above resistance with volume
Confidence: 7/10
Exit: $190.00
P&L: +$450
Duration: 3 days
Followed Plan: Yes
Emotions: Calm, disciplined
Lessons: Need larger stop on breakouts
```

### Metrics ที่ควรติดตาม:
1. **Win Rate** = Wins / Total Trades
2. **Average Win** = Total Wins / Number of Wins
3. **Average Loss** = Total Losses / Number of Losses
4. **R-Multiple** = (Exit - Entry) / (Entry - Stop)
5. **Expectancy** = (Win Rate × Avg Win) - (Loss Rate × Avg Loss)
6. **Max Consecutive Losses**
7. **Average Holding Time**
8. **P&L per Day**

### การวิเคราะห์ประจำเดือน:
- รวบรวม statistics
- ดู patterns ใน wins และ losses
- ตรวจสอบ emotional patterns
- ปรับปรุง plan

---

## 4. Mental Models (โมเดลความคิด)

### 4.1 First Principles Thinking (การคิดจากหลักการพื้นฐาน)

**แนวคิด:** แยกปัญหาออกเป็นส่วนย่อยๆ และสร้างคำตอบจากศูนย์

**การใช้ในเทรด:**
- ถามว่า "ทำไม price ถึงขึ้น/ลง?"
- ไม่ยอมรับ explanations ที่ไม่มีเหตุผลรองรับ
- สร้าง own understanding ของ market

### 4.2 Inversion (การกลับประเด็น)

**แนวคิด:** คิดถึงปัญหาในทางตรงข้าม

**การใช้ในเทรด:**
- แทนที่จะถาม "จะทำกำไรอย่างไร?" → ถาม "จะขาดทุนอย่างไร?"
- แทนที่จะถาม "จะเข้าเมื่อไหร่?" → ถาม "เมื่อไหร่จะห้ามเข้า?"
- ระบุ failure modes ก่อน

### 4.3 Circle of Competence (วงในความสามารถ)

**แนวคิด:** รู้ว่าตัวเองเก่งอะไร และอะไรที่ไม่เก่ง

**การใช้ในเทรด:**
- มุ่งเน้นเฉพาะ strategies ที่เข้าใจ
- ปฏิเสธ opportunities ที่ไม่เข้าใจ
- ขยาย circle อย่างช้าๆ

### 4.4 Probabilistic Thinking (การคิดเชิงความน่าจะเป็น)

**แนวคิด:** ทุกการตัดสินใจมีความน่าจะเป็น ไม่มีอะไรแน่นอน

**การใช้ในเทรด:**
- คิดในแง่ edge และ probability
- ยอมรับ losses โดยไม่ต้อง "เจ็บปวด"
- ประเมิน risk/reward เป็น probability distributions

### 4.5 Margin of Safety (ขอบความปลอดภัย)

**แนวคิด:** ซื้อ asset เมื่อราคาต่ำกว่า intrinsic value มากพอ

**การใช้ในเทรด:**
- เข้าเทรดเมื่อ risk/reward ดีเป็นพิเศษ
- ไม่เข้าเทรดเมื่อ risk/reward ไม่ดีพอ
- ใช้ position sizing เพื่อสร้าง margin of safety

### 4.6 Sunk Cost Fallacy (ความผิดพลาดจากต้นทุนจม)

**แนวคิด:** ตัดสินใจบนพื้นฐานของที่ลงทุนไปแล้ว ไม่ใช่ expected value

**การใช้ในเทรด:**
- อย่าถือ position ที่ขาดทุนเพราะ "ซื้อมาแพง"
- อย่าทำ average down เพราะอยากหาทุน
- ตัดสินใจบน forward-looking basis

### 4.7 Second-Order Thinking (การคิดลำดับสอง)

**แนวคิด:** คิดถึงผลกระทบของผลกระทบ

**การใช้ในเทรด:**
- ถามว่า "แล้วหลังจากนั้นจะเกิดอะไร?"
- คิดถึง market's reaction ต่อ news
- ระวัง crowded trades

### 4.8 Hanlon's Razor (ใบมีด Hanlon)

**แนวคิด:** อย่าตั้งสมมติฐานว่าเป็นเจตนาร้ายเมื่ออธิบายได้ด้วยความโชคไม่ดี

**การใช้ในเทรด:**
- อย่าตำหนิโบรกเกอร์หรือตลาดเมื่อขาดทุน
- มองหาสิ่งที่ทำผิดพลาดในระบบ
- ปรับปรุงแทนที่จะโทษ

---

## สรุปแนวทางปฏิบัติ

### ด้าน Position Sizing:
1. ใช้ Kelly หรือ Half-Kelly เป็นจุดเริ่มต้น
2. ปรับตาม correlation และ volatility
3. กำหนด drawdown limits ชัดเจน
4. มี risk limits ที่ยึดมั่น

### ด้านจิตวิทยา:
1. รู้จัก biases ของตัวเอง
2. ทำ trade journaling อย่างจริงจัง
3. มี written trading plan
4. ยึดมั่นใน process ไม่ใช่ผลลัพธ์ระยะสั้น

### ด้าน Backtesting:
1. ใช้ out-of-sample testing
2. รวม transaction costs อย่าง conservative
3. ทดสอบหลายช่วงเวลา
4. ระวัง overfitting

---

*เอกสารนี้รวบรวมแนวคิดจากทฤษฎีการเงินเชิงพฤติกรรม การจัดการความเสี่ยง และประสบการณ์จากนักลงทุนและเทรดเดอร์ที่ประสบความสำเร็จ*
