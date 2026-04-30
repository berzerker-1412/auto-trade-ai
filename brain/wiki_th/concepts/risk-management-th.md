# Risk Management

## สรุปสั้นๆ
กฎทองในการเทรด: เสียน้อย อยู่ได้นาน

## หลักการ

1. **Position Sizing** — ไม่เทรดเกิน 10% ของ balance
2. **Stop-loss บังคับ** — ขาดทุนได้แค่ 2% ต่อ trade
3. **Take-profit ชัดเจน** — เอากำไร +5%
4. **Confidence Threshold** — ไม่แน่ใจ ไม่เทรด (≥ 0.75)

## สูตร

```
Position = Balance × 0.10
Stop-loss = Entry × 0.98  (BUY) หรือ Entry × 1.02 (SELL)
Take-profit = Entry × 1.05 (BUY) หรือ Entry × 0.95 (SELL)
```
