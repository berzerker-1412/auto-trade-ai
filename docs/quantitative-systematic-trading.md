# การซื้อขายเชิงปริมาณแบบมีระบบ (Quantitative Systematic Trading)
## รายงานวิจัยฉบับสมบูรณ์ — ภาษาไทย

---

## 1. Statistical Arbitrage (Stat Arb) — การเก็งกำไรแบบ Statistical

### ความหมาย
Statistical Arbitrage คือ กลยุทธ์การซื้อขายที่ใช้โมเดลทางสถิติเพื่อค้นหาความผิดปกติของราคาที่ "คาดว่า" จะกลับสู่ค่าเฉลี่ย (mean reversion) ภายในเวลาสั้น โดยอาศัยความน่าจะเป็นทางสถิติมากกว่าการวิเคราะห์พื้นฐาน

### หลักการสำคัญ
- **Mean Reversion**: ราคาที่เบี่ยงเบนจากค่าเฉลี่ยในอดีตมีแนวโน้มกลับสู่ค่าเฉลี่ย
- **Central Limit Theorem**: เมื่อรวมสินทรัพย์หลายตัวเข้าด้วยกัน ผลตอบแทนจะกระจายตัวแบบ Normal Distribution
- **Law of Large Numbers**: เมื่อทำซ้ำหลายครั้ง ผลลัพธ์จะเข้าใกล้ค่าคาดหวัง

### ประเภทหลัก
1. **Mean Reversion Stat Arb**: ซื้อสินทรัพย์ที่ราคาต่ำกว่าค่าเฉลี่ย ขายเมื่อราคากลับสูง
2. **Cross-Sectional Stat Arb**: เปรียบเทียบสินทรัพย์หลายตัวในหมวดเดียวกัน ซื้อตัวที่ "ถูก" ขายตัวที่ "แพง"
3. **ETF Arbitrage**: ใช้ประโยชน์จากความแตกต่างระหว่างราคา ETF และ NAV (Net Asset Value)
4. **Index Arbitrage**: ใช้ส่วนต่างราคาระหว่าง Futures และ Spot ของดัชนี

### ตัวอย่างการคำนวณ
```
Spread = Price_A - β × Price_B
Z-Score = (Spread - Moving_Avg) / Moving_Std
Signal: |Z-Score| > 2 → Short Spread
Signal: |Z-Score| < 0.5 → Close Position
```

### ความเสี่ยง
- **Execution Risk**: ราคาเปลี่ยนแปลงระหว่างส่งคำสั่ง
- **Model Risk**: โมเดลอาจไม่ถูกต้องในสภาวะตลาดที่เปลี่ยน
- **Liquidity Risk**: ไม่สามารถออกจากตำแหน่งได้ทันที
- **Regime Change**: ตลาดอาจเปลี่ยนจาก mean-reverting เป็น trending

---

## 2. Pairs Trading & Cointegration

### Pairs Trading คืออะไร
Pairs Trading คือ กลยุทธ์ที่หาคู่สินทรัพย์ที่มี "ความสัมพันธ์กัน" (correlated) แล้วเทรดส่วนต่างของราคาเมื่อความสัมพันธ์นั้นเบี่ยงเบนจากปกติ

### หลักการ
1. หาคู่สินทรัพย์ที่มี correlation สูง (เช่น COIN-GBTC, BTC-ETH)
2. เมื่อ spread ขยายกว่าปกติ → Short ตัวที่ "แพง" + Long ตัวที่ "ถูก"
3. เมื่อ spread กลับสู่ปกติ → ปิดทั้งสองข้าง + รับกำไร

### Cointegration vs Correlation

| ตัวชี้วัด | Correlation | Cointegration |
|---|---|---|
| วัดอะไร | ทิศทางของความสัมพันธ์ | ความสมดุลระยะยาว |
| ผันผวน | สูง | ต่ำ |
| เสถียรภาพ | ไม่เสถียร | เสถียร |
| ใช้กับ | ระยะสั้น | ระยะยาว |

### การทดสอบ Cointegration — Engle-Granger Two-Step Method

**Step 1**: Regression
```
Y_t = α + β × X_t + ε_t
```

**Step 2**: ทดสอบ Unit Root ใน Residuals (ADF Test)
```
Δε_t = γ × ε_{t-1} + Σδ_i × Δε_{t-i} + u_t
```
ถ้า γ < 0 แสดงว่า residuals มี mean-reverting → Cointegrated

### การทดสอบ ADF (Augmented Dickey-Fuller)
- H0: Series มี Unit Root (ไม่ stationary)
- H1: Series ไม่มี Unit Root (stationary / mean-reverting)
- p-value < 0.05 → ปฏิเสธ H0 → Cointegrated

### ตัวอย่าง Pair ยอดนิยม
- **Crypto**: BTC/USD - ETH/USD, Coinbase - Binance
- **หุ้น**: KO - PEP, GS - JPM, XOM - CVX
- **ETF**: SPY - QQQ, IWM - VB

### สูตรคำนวณ Spread และ Z-Score
```
β = Cov(R_A, R_B) / Var(R_B)
Spread = R_A - β × R_B
Z-Score = (Spread - μ_spread) / σ_spread
```

### ปัจจัยที่ต้องพิจารณา
- **Lookback Period**: ควรใช้ข้อมูล 60-120 วัน
- **Entry Threshold**: Z-Score > 2.0 หรือ < -2.0
- **Exit Threshold**: Z-Score เข้าใกล้ 0
- **Half-Life ของ Spread**: T = -ln(2) / λ (จาก Ornstein-Uhlenbeck)

---

## 3. Market Making (การทำตลาด)

### ความหมาย
Market Maker คือ ผู้ที่คอยส่งคำสั่งซื้อและขาย (Bid และ Ask) ตลอดเวลา เพื่อสร้างสภาพคล่องให้ตลาด และเก็งกำไรจาก Spread

### รายได้ของ Market Maker
```
P&L = (Bid_Fill_Rate × Spread/2) - (Adverse_Selection_Loss)
```

### กลยุทธ์หลัก

#### A. Simple Spread Model
- ส่ง Bid ที่ราคา Bid = Mid - Spread/2
- ส่ง Ask ที่ราคา Ask = Mid + Spread/2
- รอให้เติมคำสั่ง (fill) ทั้งสองข้าง

#### B. Avellaneda-Stoikov Model (2008)
โมเดลที่ใช้มากที่สุดในการทำ Market Making

**Reservation Price:**
```
r(t) = s(t) - q × γ × σ² × (T - t)
```
- s(t) = mid price at time t
- q = inventory (long=+1, short=-1)
- γ = risk aversion parameter
- σ = volatility
- T = end of trading horizon

**Optimal Bid/Ask:**
```
Bid = r(t) - δ - (γ × σ² × (T-t)) / 2
Ask = r(t) + δ + (γ × σ² × (T-t)) / 2
```

#### C. Inventory-Based Model
- พยายามรักษา inventory ให้เป็นกลาง (neutral)
- ขายเมื่อ inventory มากเกินไป (overbought)
- ซื้อเมื่อ inventory น้อยเกินไป (oversold)

#### D. Volume-Wweighted Model
- ส่งคำสั่งขนาดใหญ่ในช่วงที่ volume สูง
- ลดขนาดในช่วงที่ volume ต่ำ

### ความเสี่ยงของ Market Maker

| ความเสี่ยง | คำอธิบาย |
|---|---|
| **Adverse Selection** | เจอ insider หรือ algo ที่รู้ข่าวก่อน |
| **Inventory Risk** | ราคาเคลื่อนที่ตรงข้าม position |
| **Crowding Risk** | market maker คนอื่นเผชิญหน้า |
| **Latency Risk** | ราคาเปลี่ยนก่อนที่จะ update quote |

### การจัดการความเสี่ยง
```
Max Position = Portfolio_Value × 0.02  # ไม่เกิน 2% ของพอร์ต
Max Inventory = 1000 units
Max Loss per Day = Portfolio_Value × 0.01
```

---

## 4. Momentum vs Mean Reversion ใน Crypto

### Momentum Strategy

#### หลักการ
"สิ่งที่ขึ้น จะขึ้นต่อ" — ซื้อสินทรัพย์ที่มีผลตอบแทนดีในอดีต แล้วถือต่อ

#### ประเภท
1. **Time-Series Momentum**: ซื้อเมื่อผลตอบแทน N วันก่อนเป็นบวก
2. **Cross-Sectional Momentum**: ซื้อสินทรัพย์ที่ทำผลตอบแทนดีกว่าเพื่อนร่วมกลุ่ม
3. **Factor Momentum**: ซื้อสินทรัพย์ที่มี factor exposure สูง

#### ตัวชี้วัด
```
Momentum = Price_t / Price_{t-N} - 1
ROC (Rate of Change) = (P_t - P_{t-N}) / P_{t-N}
```

#### ข้อดีใน Crypto
- Crypto มี trending ชัดเจนกว่าหุ้น (bull/bear cycle รุนแรง)
- ใช้ได้ดีในช่วงตลาด breakout
- เหมาะกับ timeframe 1D-1W

### Mean Reversion Strategy

#### หลักการ
"สิ่งที่เบี่ยงเบน จะกลับมา" — ซื้อเมื่อ RSI ต่ำ ขายเมื่อ RSI สูง

#### ตัวชี้วัด
```
RSI = 100 - (100 / (1 + RS))
RS = Average Gain / Average Loss (14 periods)
Bollinger Bands: Upper = MA + 2σ, Lower = MA - 2σ
Z-Score = (Price - MA) / σ
```

#### ข้อดีใน Crypto
- ใช้ได้ดีในช่วง sideways/ranging market
- มี mean-reverting ชัดเจนในกราฟระยะสั้น (4H-1D)
- ทำกำไรได้แม้ตลาดไม่มี direction

### Momentum vs Mean Reversion — เปรียบเทียบ

| ตัวแปร | Momentum | Mean Reversion |
|---|---|---|
| **ตลาด** | Trending | Range-bound |
| **Volatility** | สูงดี | ปานกลาง |
| **Timeframe** | ยาว (1W-1M) | สั้น (1H-1D) |
| **Risk/Reward** | High R/R | Low R/R, High Winrate |
| **Max Drawdown** | สูง | ต่ำกว่า |
| **Signal** | Breakout, Trendline | RSI, Bollinger, Z-Score |
| **Stop Loss** | Wide (10-20%) | Tight (2-5%) |

### การใช้ร่วมกัน — Regime Detection
```
Trend Strength = SMA_50 / SMA_200 (SMA > 1 = Uptrend)
Volatility = ATR / Close

IF Trend > 0.8 AND Volatility > 0.5: → Use Momentum
ELIF Trend < 0.2 AND Volatility < 0.3: → Use Mean Reversion
ELSE: → Wait or reduce size
```

---

## 5. Cross-Asset Correlations: BTC, ETH, Gold, S&P500

### ความเข้าใจเรื่อง Correlation

Correlation วัด "ทิศทาง" ที่สินทรัพย์สองตัวเคลื่อนไหวร่วมกัน:
- **ρ = +1**: เคลื่อนไหวไปในทิศเดียวกันเสมอ
- **ρ = 0**: ไม่มีความสัมพันธ์
- **ρ = -1**: เคลื่อนไหวในทิศตรงข้ามเสมอ

### Correlation Matrix — Crypto & Traditional Assets

```
         BTC    ETH    Gold   SPX    DXY
BTC     1.00   0.85   0.15  -0.10  -0.25
ETH     0.85   1.00   0.12  -0.08  -0.20
Gold    0.15   0.12   1.00   0.20   0.30
SPX    -0.10  -0.08   0.20   1.00   0.45
DXY   -0.25  -0.20   0.30   0.45   1.00
```

### ความหมายของแต่ละคู่

#### BTC-ETH (ρ ≈ 0.85)
- สูงมาก เพราะอยู่ใน ecosystem เดียวกัน
- ETH มี correlation ต่ำกว่า BTC กับทองเล็กน้อย (0.12 vs 0.15)
- ใช้เป็น hedge ซึ่งกันและกันไม่ได้ → ไม่เหมาะเป็น pair trade

#### BTC-Gold (ρ ≈ 0.15)
- มี correlation ต่ำ → ใช้เป็น portfolio diversifier ได้
- ในช่วง crisis (2008, COVID, 2022) correlation อาจพุ่งสูงถึง 0.5-0.7
- BTC ถูกมองว่าเป็น "Digital Gold" แต่ในความเป็นจริง correlation ยังต่ำ

#### BTC-SPX (ρ ≈ -0.10)
- แทบไม่มี correlation → สามารถใช้กระจายความเสี่ยงได้
- ในช่วง market crash (March 2020) BTC ลงไปด้วย แสดง correlation เปลี่ยนแปลงได้
- ช่วง 2022 (ดอกเบี้ยขึ้น) correlation กลายเป็นบวก

#### DXY (Dollar Index) — BTC (ρ ≈ -0.25)
- USD แข็ง → BTC มีแนวโน้มอ่อน
- เป็น negative correlation ที่น่าสนใจสำหรับ macro hedging

### Regime-Based Correlation
```
High Risk Environment (Crisis):
  BTC-SPX → +0.60 to +0.80 (ไม่ได้เป็น safe haven)

Risk-On Environment:
  BTC-SPX → +0.30 to +0.50
  BTC-Gold → +0.20 to +0.40

Risk-Off / Deflationary Scenario:
  BTC-SPX → +0.60
  BTC-Gold → +0.70
  DXY-BTC → -0.50
```

### การใช้ Correlation ในการเทรด

#### Pair Trading ข้ามตลาด
```
IF BTC-SPX Correlation < -0.2: 
  → Long BTC, Short SPX (หรือ SPY)
  → หวังว่า correlation จะกลับสู่ 0

IF BTC-Gold Correlation > 0.5:
  → Reduce BTC allocation (hedge ด้วย gold)
```

#### Portfolio Diversification (Risk Parity)
```
Asset     Weight    Vol    Risk Contribution
BTC        10%     70%       7%
ETH        10%     80%       8%
Gold       20%     15%       3%
SPX        30%     18%       5.4%
Bonds      30%      8%       2.4%
───────────────────────────────
Total Risk Contribution ≈ 25.8%
```

---

## 6. Orderbook, VWAP, และ TWAP

### Orderbook (รายงานคำสั่ง)

#### โครงสร้าง
```
BID (ผู้ซื้อ)              ASK (ผู้ขาย)
Price    Size    |    Price    Size
─────────────────────────────
100.00   500    |   100.05   300
 99.99   200    |   100.10   150
 99.95   100    |   100.15   200
```

#### ข้อมูลสำคัญใน Orderbook
- **Bid-Ask Spread**: ความต่างระหว่าง Bid สูงสุด กับ Ask ต่ำสุด
- **Depth**: ปริมาณคำสั่งซื้อ/ขายที่แต่ละระดับราคา
- **Imbalance**: ความไม่สมดุลระหว่าง Bid และ Ask
- **Mid Price**: (Best Bid + Best Ask) / 2

#### Orderbook Imbalance (OBI)
```
OBI = (Bid_Volume - Ask_Volume) / (Bid_Volume + Ask_Volume)
```
- OBI > +0.3 → มีแรงซื้อมากกว่า → ราคาอาจขึ้น
- OBI < -0.3 → มีแรงขายมากกว่า → ราคาอาจลง

### VWAP (Volume Weighted Average Price)

#### ความหมาย
VWAP = ราคาเฉลี่ยที่ถ่วงน้ำหนักด้วย volume ตั้งแต่เปิดตลาด

#### สูตร
```
VWAP = Σ(Price_i × Volume_i) / Σ(Volume_i)
```

#### การใช้งาน
1. **Execution Benchmark**: เปรียบเทียบว่าซื้อ/ขายดีกว่า VWAP หรือไม่
2. **Trend Indicator**: ราคา > VWAP → Uptrend, ราคา < VWAP → Downtrend
3. **Support/Resistance**: VWAP เป็นแนวรับ-แนวต้านที่มี significance

#### ตัวอย่าง
```
Period     Price    Volume    P×V
09:00      100       500      50000
09:15      101       300      30300
09:30       99       400      39600
09:45      100       200      20000
─────────────────────────────
Total     —        1400      139900
VWAP = 139900 / 1400 = 99.93
```

### TWAP (Time Weighted Average Price)

#### ความหมาย
TWAP = ราคาเฉลี่ยที่ถ่วงน้ำหนักด้วยเวลา (ไม่สนใจ volume)

#### สูตร
```
TWAP = Σ(Price_i) / N
```
หรือแบบต่อเนื่อง:
```
TWAP = (1/T) × Σ(s(t) × dt)
```

#### VWAP vs TWAP

| ตัวชี้วัด | VWAP | TWAP |
|---|---|---|
| ถ่วงน้ำหนัก | Volume | เวลา |
| ซ่อนคำสั่ง | ดีกว่า (volume-aware) | ด้อยกว่า |
| ความแม่นยำ | สูง | ปานกลาง |
| ใช้เมื่อ | ต้องการ execution ที่ดี | ต้องการ simplicity |
| เหมาะกับ | คำสั่งขนาดใหญ่ | คำสั่งขนาดเล็ก-กลาง |

### Orderbook-Based Execution Strategies

#### 1. Iceberg Order
ส่งคำสั่งที่แสดงเฉพาะ "ยอดสังหาริมทรัพย์" ให้คนอื่นเห็น ส่วนที่ซ่อนไว้จะค่อยๆ เผย
```
Visible: 100 shares @ $100
Hidden: 1000 shares @ $100
→ ค่อยๆ ติด execution ทีละ 100
```

#### 2. POV (Percentage of Volume)
```
Target_POV = 10%
Child_Order_Size = POV × Current_Volume
```

#### 3. Implementation Shortfall (IS)
```
IS = (Execution_Price - Decision_Price) × Direction
Minimize IS = ซื้อเร็ว ขายเร็ว แต่รับ impact มาก
Minimize Market_Impact = ซื้อช้า กระจาย แต่รับ timing risk
```

---

## 7. HFT Concepts สำหรับ Retail Trader

### HFT (High-Frequency Trading) คืออะไร
การซื้อขายความเร็วสูงมาก ใช้คอมพิวเตอร์เทรดในระดับ microsecond ถึง millisecond

### ส่วนประกอบหลักของ HFT System

```
┌─────────────────────────────────────────────────────┐
│                   HFT Architecture                   │
├─────────────────────────────────────────────────────┤
│  Market Data Feed ──→ Pre-Processor ──→ Strategy    │
│                           │                          │
│                      Risk Engine                     │
│                           │                          │
│                    Order Router ──→ Exchange        │
│                           │                          │
│                   Execution Report                   │
└─────────────────────────────────────────────────────┘
```

### Latency Components
```
Total Latency = Network + Preprocessing + Strategy + Routing
              = 100μs + 50μs + 10μs + 50μs
              = 210μs (0.21 ms)
```

### สำหรับ Retail Trader — สิ่งที่ทำได้จริง

#### 1. VPS (Virtual Private Server)
- เช่า VPS ใกล้ exchange data center
- เช่น: AWS Tokyo, Singapore, or HK
- Latency: 1-10ms แทนที่จะเป็น 50-200ms จากบ้าน

#### 2. Co-Location
- ติดตั้งเซิร์ฟเวอร์ใน data center เดียวกับ exchange
- ใช้ได้เฉพาะ institutional (ราคาแพงมาก)
- Retail ใช้ VPS คุณภาพสูงแทนได้

#### 3. Market Data Feed
- Exchange API: REST (slow) หรือ WebSocket (fast)
- Crypto: Binance WebSocket, Coinbase WebSocket
- รองรับ 100+ updates/second

#### 4. Order Types ที่เหมาะกับ Retail
```
- Limit Order: ควบคุมราคา แต่อาจไม่ fill
- Stop-Loss: อัตโนมัติเมื่อราคาถึง
- TWAP/VWAP: กระจายคำสั่งตามเวลา/volume
- Iceberg: ซ่อนขนาดคำสั่งใหญ่
```

### กลยุทธ์ที่ Retail สามารถใช้ได้ (Low-Frequency)

#### A. Liquidity Provision (เทียบเท่า Market Making ระดับต่ำ)
```
1. ส่ง limit order ทั้ง bid และ ask
2. รับ spread เป็นกำไร
3. ใช้ได้กับ centralized exchanges (CEX) ที่มี maker fee ต่ำ
4. ระวัง: impermanent loss, adverse selection
```

#### B. Statistical Arbitrage (ระดับต่ำ)
```
1. ใช้ Python คำนวณ spread ระหว่าง BTC spot และ BTC futures
2. เมื่อ spread > funding rate → ปิด position
3. ใช้เวลา minutes ถึง hours ไม่ใช่ microseconds
```

#### C. Momentum on Low Timeframe (Scalping)
```
1. 5-min chart, EMA crossover
2. Entry: EMA 9 ข้าม EMA 21 ขึ้น
3. Exit: EMA 9 ข้าม EMA 21 ลง
4. Stop Loss: 0.5-1% (tight)
5. ต้องมี low fee + fast execution
```

### Tools สำหรับ Retail

| Tool | ประเภท | ความเร็ว | ราคา |
|---|---|---|---|
| **Binance API** | Crypto | Fast | ฟรี |
| **CCXT** | Multi-exchange | Medium | ฟรี |
| **TradingView** | Charting + Alert | Slow | $15-60/เดือน |
| **Python + WebSocket** | Custom algo | Fast | ฟรี |
| **Interactive Brokers** | Stocks/Futures | Fast | $0.005/share |

### ข้อจำกัดของ Retail เทียบกับ HFT

| ปัจจัย | Institutional HFT | Retail Trader |
|---|---|---|
| **Latency** | < 0.1ms | 10-100ms |
| **Capital** | $100M+ | < $100K |
| **Data** | Full orderbook | Last 100 trades |
| **Co-location** | Yes | No |
| **Strategy** | Complex stat arb | Simple momentum |
| **Competition** | vs other HFTs | vs HFTs + Retail |

### สิ่งที่ Retail ทำได้ดีกว่า HFT
1. **การบริหารความเสี่ยง**: HFT ต้องเทรดขนาดใหญ่ → ความเสี่ยงสูง
2. **เฟรมเวิร์กใหญ่**: HFT มองแค่ microseconds → retail มอง trend ระดับชั่วโมง-วัน
3. **ความยืดหยุ่น**: Retail เปลี่ยน strategy ได้ง่ายกว่า
4. **ไม่ต้อง compete โดยตรง**: เลือก timeframe ที่ HFT ไม่สนใจ (เช่น 4H, 1D)

---

## สรุป (Summary)

การซื้อขายเชิงปริมาณแบบมีระบบ (Quantitative Systematic Trading) ประกอบด้วยองค์ประกอบหลัก 8 ด้าน:

1. **Statistical Arbitrage** — ใช้สถิติหาความผิดปกติของราคาที่คาดว่าจะกลับสู่ค่าเฉลี่ย
2. **Pairs Trading & Cointegration** — หาคู่สินทรัพย์ที่สมดุลระยะยาว ใช้ ADF test ยืนยัน
3. **Market Making** — สร้างสภาพคล่อง รับ spread เป็นกำไร ต้องจัดการ inventory risk
4. **Momentum vs Mean Reversion** — Momentum เหมาะตลาด trending, Mean Reversion เหมาะตลาด sideways
5. **Cross-Asset Correlation** — BTC-ETH สูง (0.85), BTC-Gold ต่ำ (0.15), ใช้กระจายพอร์ตได้
6. **Orderbook/VWAP/TWAP** — ใช้วัด liquidity และเป็น benchmark สำหรับ execution
7. **HFT Concepts** — Retail ไม่สามารถแข่ง latency ได้ แต่สามารถใช้กลยุทธ์ low-frequency ที่มีประสิทธิภาพได้

### หลักการสำคัญที่สุด
> **"Systematic Trading ไม่ใช่การหา Holy Grail แต่คือการบริหารความเสี่ยงอย่างมีระบบ และรักษาวินัยในการ execute ตามกลยุทธ์ที่ออกแบบไว้"**

---

*เอกสารนี้จัดทำเพื่อวัตถุประสงค์ทางการศึกษา ผลการเทรดในอดีตไม่รับประกันผลตอบแทนในอนาคต*
