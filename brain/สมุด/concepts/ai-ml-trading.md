# AI/ML สำหรับการเทรด

## สรุปสั้นๆ

AI/ML ในเทรดมี 2 แนวทาง:
- **Supervised Learning** — ทำนายราคาหรือทิศ
- **Reinforcement Learning** — เรียนรู้ policy การเทรดจาก interaction

**ปัญหาหลัก:** ตลาดไม่หยุดนิ่ง — pattern ที่เคยใช้ได้อาจใช้ไม่ได้แล้ว

## สิ่งที่ wow

### LSTM
- ทำนายราคาจาก sequence ของข้อมูล
- เหมาะกับข้อมูล time series เช่น OHLCV
- แต่... ใช้ predict ราคาตรงๆ ได้ยาก — มัก predict direction ดีกว่า

### Sentiment Analysis
```
ข่าว/โซเชียล → NLP → Sentiment Score → สัญญาณ
```
- ข่าว = signal ที่ดีกว่าโซเชียล (โซเชียล noisy มาก)
- FinBERT = BERT ที่ fine-tune สำหรับ financial text

### Reinforcement Learning
```
Environment: ตลาด (ข้อมูลราคา)
Agent: กลยุทธ์เทรด
State: portfolio + features
Action: BUY / SELL / HOLD
Reward: return หรือ Sharpe ratio
```

## Feature Engineering สำคัญที่สุด

ML ทำงานได้ดีขึ้นเยอะถ้าใส่ features ที่ดี:

```python
features = {
    # Price-based
    "returns_1d": (price - price.shift(1)) / price.shift(1),
    "returns_7d": (price - price.shift(7)) / price.shift(7),

    # Technical indicators
    "rsi_14": calculate_rsi(close, period=14),
    "macd_signal": calculate_macd(close)["signal"],
    "bb_position": (close - bb_lower) / (bb_upper - bb_lower),

    # Volume
    "volume_ratio": volume / volume.rolling(20).mean(),

    # Cross-asset
    "btc_correlation_7d": close.rolling(7).corr(btc_close),
}
```

## ในโปรเจกต์ (auto-trade-ai)

ระยะที่วางไว้:
- **Phase 1 (ปัจจุบัน):** Rule-based signals จาก indicators
- **Phase 2:** LSTM price prediction
- **Phase 3:** Sentiment analysis จาก crypto news
- **Phase 4:** RL agent สำหรับ portfolio management

## ปัญหาที่ต้องระวัง

- Overfitting กับ historical data — ใช้ walk-forward validation
- Non-stationarity — market regime เปลี่ยน = model เดิมใช้ไม่ได้
- Look-ahead bias — ต้อง ensure ไม่ใช้ข้อมูลอนาคตใน training

## เชื่อมกับ

- [[technical-indicators]] — indicators เป็น features หลัก
- [[risk-management]] — RL reward ต้อง include risk (Sharpe ratio)
- [[trading-strategies]] — strategies = action space ของ RL agent
