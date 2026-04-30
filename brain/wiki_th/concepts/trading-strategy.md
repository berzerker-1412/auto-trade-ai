# Trading Strategy — AI Signal Generation

## สรุปสั้นๆ
ระบบ AI สร้างสัญญาณ BUY/SELL โดยใช้ GPT-4o วิเคราะห์ข้อมูลตลาด

## วิธีทำงาน

1. ดึงข้อมูลตลาด (price, volume, OHLCV)
2. ส่ง prompt ให้ GPT-4o พร้อม system role "professional trading signal generator"
3. รับ JSON กลับมา: direction, entry_price, stop_loss, take_profit, confidence
4. ถ้า confidence >= 0.75 → execute trade

## สิ่งที่ยังไม่ชัด
- Prompt ปัจจุบันค่อนข้างง่าย — ปรับปรุงได้
- ยังไม่มี technical indicators ใน prompt (RSI, MACD, etc.)
- ควรมี news sentiment analysis ไหม?
