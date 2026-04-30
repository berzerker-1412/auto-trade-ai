# สาระน่ารู้เกี่ยวกับ Crypto Derivatives

## บทนำ

ตลาด Crypto Derivatives เป็นหนึ่งใน segment ที่เติบโตเร็วที่สุดในอุตสาหกรรมคริปโต โดยปริมาณการซื้อขาย futures และ options มีมูลค่าหลายล้านล้านดอลลาร์ต่อวัน การทำความเข้าใจเทคนิคและกลยุทธ์ต่างๆ ในตลาดนี้จึงมีความสำคัญอย่างยิ่งสำหรับนักลงทุนและนักเก็งกำไร

---

## 1. กลยุทธ์ Options สำหรับ BTC และ ETH

### 1.1 พื้นฐาน Options

**Options** คือสัญญาที่ให้สิทธิ์แก่ผู้ถือ (holder) ในการซื้อหรือขายสินทรัพย์ในราคาที่กำหนดไว้ล่วงหน้า (strike price) ภายในระยะเวลาที่กำหนด

**Call Option** - สิทธิ์ในการซื้อสินทรัพย์
**Put Option** - สิทธิ์ในการขายสินทรัพย์

### 1.2 กลยุทธ์พื้นฐาน

#### a) Covered Call (สำหรับ BTC/ETH)
- ขาย Call Option โดยถือสินทรัพย์อ้างอิง (underlying asset) ครอบไว้
- เหมาะสำหรับตลาด sideway หรือ bull market ที่คาดว่าราคาจะไม่พุ่งสูงเกินไป
- รายได้จาก premium ช่วยลดต้นทุนถือสินทรัพย์

#### b) Protective Put
- ซื้อ Put Option เพื่อป้องกันความเสี่ยงจากการลงทุนใน BTC/ETH
- เหมือนการทำประกันราคา - จำกัดความเสียหายสูงสุดไว้ที่ strike price
- เหมาะสำหรับการป้องกันความเสี่ยงในช่วงที่ตลาดผันผวน

#### c) Cash-Secured Put
- ขาย Put Option โดยมีเงินสดพร้อมไว้ซื้อสินทรัพย์หากถูก exercise
- ผู้ขายได้ premium และยินดีซื้อ BTC/ETH ที่ strike price ที่ต่ำกว่าตลาด
- เป็นกลยุทธ์ "buy the dip" แบบมีโครงสร้าง

#### d) Bull Spread / Bear Spread
- ซื้อและขาย options ที่ strike prices ต่างกันเพื่อสร้าง directional bet
- Bull Call Spread: ซื้อ Call ที่ strike ต่ำ + ขาย Call ที่ strike สูงกว่า
- Bear Put Spread: ซื้อ Put ที่ strike สูง + ขาย Put ที่ strike ต่ำกว่า

### 1.3 กลยุทธ์ขั้นสูง

#### e) Straddle และ Strangle
- **Straddle**: ซื้อ Call และ Put ที่ strike เดียวกัน (same strike)
- **Strangle**: ซื้อ Call และ Put ที่ strike ต่างกัน (different strikes)
- ใช้เมื่อคาดว่าจะมี big move แต่ไม่แน่ใจทิศทาง (volatility trade)
- กำไรเกิดจากความผันผวนที่สูง ไม่ใช่ทิศทางราคา

#### f) Iron Condor
- รวม Bull Put Spread + Bear Call Spread
- สร้างกำไรจากช่วงที่ราคา sideways ในกรอบแคบ
- Max profit = net premium received
- Max loss = width of strikes - net premium

---

## 2. Funding Rate Arbitrage (การเก็งกำไรจาก Funding Rate)

### 2.1 ที่มาของ Funding Rate

**Perpetual Futures** (หรือ "Perps") คือ futures ที่ไม่มีวันหมดอายุ โดยมี **Funding Rate** เป็นกลไกในการรักษาราคาให้ใกล้เคียง spot price

- เมื่อราคา Perp > Spot → Funding Rate เป็นบวก → ผู้ long จ่ายให้ผู้ short
- เมื่อราคา Perp < Spot → Funding Rate เป็นลบ → ผู้ short จ่ายให้ผู้ long

### 2.2 กลยุทธ์ Funding Rate Arbitrage

#### วิธีที่ 1: Spot-Perp Arbitrage
1. ซื้อสินทรัพย์ใน spot market
2. Short futures/perpetual ที่ราคาสูงกว่า
3. รอจนกว่า funding rate ทำให้ราคา收敛
4. ปิด positions ทั้งสองข้าง

**ตัวอย่าง:**
- ซื้อ BTC ที่ $60,000 ใน spot
- Short BTC-Perp ที่ $60,200
- Funding rate = +0.01% ทุก 8 ชั่วโมง
- ทุก 8 ชั่วโมง ได้รับ $6 (0.01% ของ $60,000)
- ต่อเดือน = ~$54 จาก funding alone

#### วิธีที่ 2: Future Curve Arbitrage
- เมื่อ futures แพงเกินไป (contango มาก) → sell futures แพง, buy spot ถูก
- เมื่อ futures ถูกเกินไป (backwardation) → buy futures ถูก, short spot
- หาเส้นอ้างอิงที่เบี่ยงเบนมากผิดปกติ

#### วิธีที่ 3: Cross-Exchange Arbitrage
- Binance funding rate: +0.02%
- Bybit funding rate: -0.01%
- หาผลต่างนี้ → วิธีที่ 1 จ่ายที่ exchange แรก, วิธีที่ 2 ได้รับที่ exchange ที่สอง

### 2.3 ความเสี่ยง

- **Execution risk**: ราคาอาจเปลี่ยนก่อนที่จะปิดออเดอร์ทั้งสองข้าง
- **Liquidity risk**: บาง exchange มี liquidity ต่ำ
- **Counterparty risk**: เลือก exchange ที่น่าเชื่อถือ
- **Margin call risk**: หากราคาวิ่งตรงข้าม position

---

## 3. Basis Trading (การเทรด Basis)

### 3.1 ความหมายของ Basis

**Basis** = Futures Price - Spot Price

- **Positive Basis (Contango)**: Futures > Spot (ปกติ)
- **Negative Basis (Backwardation)**: Futures < Spot (ผิดปกติ)

### 3.2 กลยุทธ์ Basis Trading

#### กลยุทธ์ที่ 1: Cash and Carry
1. ซื้อสินทรัพย์ใน spot
2. Short futures ในราคาที่สูงกว่า
3. ถือจน futures หมดอายุ → basis = 0
4. กำไร = Futures Price - Spot Price - Cost of Carry

**Cost of Carry ประกอบด้วย:**
- ค่า storage
- ค่าธรรมเนียม financing
- ผลตอบแทนที่เสียโอกาส (opportunity cost)

#### กลยุทธ์ที่ 2: Reverse Cash and Carry
1. Short spot (ยืมมาขาย)
2. Long futures
3. รอจน basis กลับสู่ปกติ
4. หาก basis กลายเป็นลบมาก → ทำกำไรได้มาก

#### กลยุทธ์ที่ 3: Basis Mean Reversion
- เมื่อ basis สูงกว่าค่าเฉลี่ยทางประวัติศาสตร์มาก → คาดว่าจะลดลง
- เมื่อ basis ต่ำกว่าค่าเฉลี่ยมาก → คาดว่าจะเพิ่มขึ้น
- ใช้ statistical indicators เช่น z-score, Bollinger Bands

### 3.3 ตัวอย่างใน crypto

**สถานการณ์: BTC Spot = $50,000, BTC Futures 1 เดือน = $51,000**

Cash and Carry:
- ซื้อ BTC Spot: $50,000
- Short BTC Futures 1 เดือน: $51,000
- Basis = $1,000 (2%)
- ถ้า cost of carry = $200 → กำไรที่แน่นอน = $800

---

## 4. Gamma และ Theta Strategies

### 4.1 ความหมายของ Greeks

#### Gamma (Γ)
- อัตราการเปลี่ยนแปลงของ Delta ต่อการเปลี่ยนแปลงราคา 1 หน่วย
- วัด "ความเร็ว" ของ delta hedging
- Options ที่ near ATM มี gamma สูงสุด
- Gamma สูง → delta เปลี่ยนเร็ว → ต้อง rebalance บ่อย

#### Theta (Θ)
- มูลค่าที่ option สูญเสียต่อวัน (time decay)
- โดยทั่วไป = negative (option เสื่อมค่าตลอดเวลา)
- ATM options มี theta สูงสุด
- เข้าใจว่า "เวลาคือศัตรูของ option buyer, เพื่อนของ option seller"

### 4.2 กลยุทธ์ Gamma Scalping

**แนวคิด:** ต้องการได้กำไรจากการเคลื่อนไหวของราคา โดยไม่ต้อง predict ทิศทาง

**วิธีการ:**
1. ซื้อ straddle หรือ strangle (gamma สูง)
2. เมื่อราคาขึ้น → delta เพิ่มขึ้น → ขายบางส่วนเพื่อล็อกกำไร
3. เมื่อราคาลง → delta ลดลง → ซื้อเพิ่ม
4. ทำซ้ำ → สร้างกำไรจากทั้ง gamma และ theta

**สิ่งสำคัญ:**
- ต้อง rebalance สม่ำเสมอ
- ยิ่ง volatility สูง → gamma scalping ยิ่งได้กำไรมาก
- ควรใช้ในช่วงที่ IV (Implied Volatility) ต่ำกว่า RV (Realized Volatility)

### 4.3 กลยุทธ์ Theta Harvesting (Yield Generation)

**แนวคิด:** ขาย options เพื่อเก็บ premium (theta) เป็นรายได้ประจำ

#### a) Wheel Strategy (สำหรับ BTC/ETH)
1. เริ่มจาก cash → ขาย Put (CSP - Cash Secured Put)
2. ถ้าถูก exercise → ได้ BTC/ETH → ขาย Covered Call
3. ถ้าไม่ถูก → ได้ premium → ทำซ้ำ

#### b) Short Strangle
- ขาย OTM Call + OTM Put ในเวลาเดียวกัน
- Premium สูงกว่า short straddle แต่ range กว้างกว่า
- เหมาะสำหรับ sideways market ที่คาดว่าจะอยู่ในกรอบ

#### c) Iron Condor (Theta-positive)
- ขาย inner strikes + ซื้อ outer strikes เพื่อลด risk
- Max profit = net premium
- ต้องกำหนด strikes ให้เหมาะสมกับ volatility

### 4.4 ความเสี่ยงของ Gamma/Theta Strategies

**Gamma Risk:**
- เมื่อราคาวิ่งเร็วมาก → delta เปลี่ยนเร็วเกินไป
- "Gamma squeeze" → losses สะสมเร็ว

**Theta Risk:**
- ทิศทางผิด → premium ที่ได้มาไม่คุ้มกับ loss
- Sideways มากเกินไป → theta ทำงานได้ดี (ดี)
- Volatility crush → IV ลดเร็ว → option ขายไม่ได้ราคา

---

## 5. Volatility Surface Trading

### 5.1 ความหมายของ Volatility Surface

**Volatility Surface** คือ 3D surface ที่แสดง implied volatility (IV) ของ options ที่ strike prices และ expirations ต่างกัน

**แกน X**: Strike Price
**แกน Y**: Time to Expiration  
**แกน Z**: Implied Volatility

### 5.2 Volatility Smile / Skew

**Volatility Smile:**
- ATM options มี IV ต่ำที่สุด
- OTM options มี IV สูงกว่า
- เกิดจาก demand สำหรับ downside protection

**Volatility Skew:**
- บางครั้ง IV ของ OTM puts สูงกว่า OTM calls (negative skew)
- บางครั้ง IV ของ OTM calls สูงกว่า (positive skew)
- Skew บอก "sentiment" ของตลาด

**ใน crypto:**
- BTC มักมี negative skew (puts �แพงกว่า calls) → ตลาดเป็น risk-off
- ETH อาจมี skew ที่ต่างกันในบางช่วง

### 5.3 Term Structure

**Term Structure** คือความสัมพันธ์ระหว่าง IV กับ time to expiration

**Contango (ปกติ):**
- Near-term IV < Long-term IV
- คาดว่าจะมี event หรือ uncertainty ในอนาคต

**Backwardation:**
- Near-term IV > Long-term IV
- มักเกิดในช่วงตลาดกระทิงหรือ crisis

### 5.4 กลยุทธ์ Volatility Surface

#### กลยุทธ์ที่ 1: Delta Hedged Vol Trade
1. ซื้อ options ที่ IV ต่ำ (ถูก)
2. Delta hedge ด้วย futures/spot
3. รอจน IV กลับสู่ปกติ
4. กำไรจาก IV expansion

#### กลยุทธ์ที่ 2: Skew Trading
1. เมื่อ skew บิดเบี้ยวมากเกินไป → ซื้อ options ที่ "ถูกเกินไป" ทาง skew
2. รอจน market reprice skew
3. ปิด position เมื่อ skew กลับปกติ

#### กลยุทธ์ที่ 3: Calendar Spread (Term Structure)
1. ซื้อ long-term options
2. ขาย short-term options (ที่ IV สูงกว่า)
3. เหมาะเมื่อ near-term IV สูงผิดปกติ
4. กำไรจาก "mean reversion" ของ term structure

#### กลยุทธ์ที่ 4: Volatility Arbitrage
1. คำนวณ theoretical IV จาก historical data
2. หา options ที่ IV > Theoretical (แพง) → ขาย
3. หา options ที่ IV < Theoretical (ถูก) → ซื้อ
4. Delta hedge ทั้งหมด → กำไรจาก mispricing

### 5.5 การใช้งาน Volatility Surface ในทางปฏิบัติ

**สำหรับ BTC:**
- ดู 25-delta skew ระหว่าง calls และ puts
- ถ้า skew > 5% → negative sentiment
- ถ้า skew < -5% → positive sentiment

**สำหรับ ETH:**
- ETH มี term structure ที่ "steeper" กว่า BTC
- เหมาะสำหรับ calendar spreads มากกว่า

**Tools แนะนำ:**
- Deribit: ดู IV surface แบบ real-time
- Skew.com: วิเคราะห์ volatility ข้าม exchanges
- TradingView: สร้าง custom volatility indicators

---

## 6. Risk Management รวม

### 6.1 Position Sizing
- อย่าใช้เงินเกิน 1-2% ต่อ position
- คำนวณ max loss ก่อนเข้าทุกครั้ง

### 6.2 Stop Loss
- ใช้ trailing stop สำหรับ options positions
- ตั้ง max loss ที่ยอมรับได้ (เช่น 50% ของ premium)

### 6.3 Diversification
- กระจายข้าม assets (BTC + ETH)
- กระจายข้าม strategies
- อย่า over-concentrate ใน single position

### 6.4 Hedging
- ใช้ options เป็น insurance
- ถือ spot + protective put = zero-risk floor

---

## 7. แหล่งข้อมูลแนะนำ

- **Deribit** - ดู IV surface, funding rates
- **Skew** - วิเคราะห์ derivatives metrics
- **Laevitas** - วิเคราะห์ BTC/ETH options
- **TradingView** - สร้าง custom indicators
- **Glassnode** - On-chain metrics ประกอบการตัดสินใจ

---

## สรุป

การเทรด crypto derivatives ต้องการความเข้าใจลึกซึ้งใน:
1. **Options Greeks** - delta, gamma, theta, vega
2. **Funding mechanics** - ทำไม funding rate เป็นบวกหรือลบ
3. **Volatility dynamics** - IV vs RV, smile, skew, term structure
4. **Risk management** - position sizing, stop loss, diversification

กลยุทธ์แต่ละตัวมีความเสี่ยงและผลตอบแทนต่างกัน - เลือกให้เหมาะกับ market condition และ risk appetite ของตัวเอง
