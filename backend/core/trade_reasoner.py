"""Trade Reasoner — บันทึกและอธิบายเหตุผลที่เปิด/ปิด trade

หน้าที่:
1. บันทึก context ณ จุดเปิด trade (market regime, indicators, sentiment, sizing)
2. บันทึกเหตุผลที่ปิด trade (trigger: SL/TP/Trailing/Regime/Manual)
3. สร้าง natural language explanation สำหรับแต่ละ trade

ทำไมต้องมี:
- ต้องการ audit trail ว่าระบบตัดสินใจด้วยเหตุผลอะไร
- ป้องกัน "black box" — เห็น logic ทั้งหมด
- ใช้ review หลัง trade ได้ว่าถูกต้องหรือไม่
"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class EntryReason:
    """เหตุผลที่เปิด trade"""
    timestamp: str
    symbol: str
    direction: str                    # "BUY" or "SELL"
    
    # Signal info
    signal_direction: str             # "BUY" or "SELL" จาก AI
    signal_confidence: float          # 0-1
    signal_reasoning: str             # AI reasoning text
    
    # Market regime
    regime_name: str                 # "TRENDING" / "RANGING" / "VOLATILE" / "CRASH"
    regime_confidence: float
    regime_reason: str
    
    # Strategy selection
    strategy_used: str              # "momentum" / "mean_reversion" / "none"
    
    # Technical indicators
    indicators: Dict[str, float]    # e.g. {"RSI": 65, "ADX": 35}
    
    # News sentiment
    news_bias: str                  # "bullish" / "bearish" / "neutral"
    news_score: float
    news_impacted_assets: List[str]
    
    # Position sizing
    sizing_method: str
    sizing_kelly_pct: Optional[float]
    sizing_size: float               # notional value
    sizing_quantity: float
    sizing_reason: str
    
    # Entry price
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    
    # Risk check result
    risk_check_passed: bool
    risk_check_reason: str
    
    # Plain text summary
    summary: str = ""


@dataclass
class ExitReason:
    """เหตุผลที่ปิด trade"""
    timestamp: str
    symbol: str
    trade_number: int
    trigger: str                    # "stop_loss" | "take_profit" | "trailing_stop" | "regime_change" | "manual" | "risk_manager"
    trigger_detail: str             # รายละเอียดเพิ่มเติม
    entry_price: float
    exit_price: float
    holding_period_minutes: float
    pnl: float
    pnl_pct: float
    vs_entry_expectation: str       # "Exceeded TP" / "Stopped out" / "Early exit"
    trailing_highest_price: Optional[float] = None
    trailing_locked_pct: Optional[float] = None
    summary: str = ""


@dataclass
class TradeReasonLog:
    """บันทึกเหตุผลทั้งหมดของ trade"""
    trade_id: str
    trade_number: int
    symbol: str
    wallet_type: str
    direction: str
    
    entry: Optional[EntryReason] = None
    exit: Optional[ExitReason] = None
    
    # Tags for filtering
    tags: List[str] = field(default_factory=list)
    
    # Timestamps
    opened_at: str = ""
    closed_at: str = ""
    duration_minutes: float = 0.0


class TradeReasoner:
    """
    บันทึกและสร้างเหตุผลสำหรับทุก trade
    
    Usage:
        reasoner = TradeReasoner()
        
        # บันทึกเหตุผลเปิด
        reasoner.log_entry(
            trade_id="123",
            signal=signal,
            regime=regime,
            sizing_result=sizing,
            risk_check_result=risk_check,
            news_signal=news_signal,
            indicators={"RSI": 65, "MACD": 0.5},
        )
        
        # บันทึกเหตุผลปิด
        reasoner.log_exit(
            trade_id="123",
            trigger="trailing_stop",
            trigger_detail="Price pulled back to trailing @ 60200",
            trailing_info={"high": 61500, "locked_pct": 0.038},
        )
        
        # ดึงเหตุผล
        log = reasoner.get_trade_reason("123")
        print(log.entry.summary)    # "Opened LONG BTC @ 60000..."
        print(log.exit.summary)     # "Closed @ 60200 (+3.8%)..."
    """

    def __init__(self):
        self.trade_logs: Dict[str, TradeReasonLog] = {}
        self.all_reasons: List[TradeReasonLog] = []

    def log_entry(
        self,
        trade_id: str,
        trade_number: int,
        symbol: str,
        direction: str,
        wallet_type: str,
        entry_price: float,
        stop_loss: Optional[float],
        take_profit: Optional[float],
        signal: Any,                 # TradeSignal
        regime: Optional[Any],        # MarketRegime
        sizing_result: Any,          # PositionSizeResult
        risk_check_result: Any,      # RiskCheckResult
        news_signal: Optional[Dict[str, Any]] = None,
        indicators: Optional[Dict[str, float]] = None,
        tags: Optional[List[str]] = None,
    ) -> TradeReasonLog:
        """
        บันทึกเหตุผลที่เปิด trade
        """
        now = datetime.now().isoformat()
        
        # Calculate risk/reward
        if stop_loss and stop_loss != entry_price and take_profit:
            risk = abs(entry_price - stop_loss)
            reward = abs(take_profit - entry_price)
            rr = reward / risk if risk > 0 else 0
        else:
            rr = 0.0
        
        # Build entry reason
        entry = EntryReason(
            timestamp=now,
            symbol=symbol,
            direction=direction,
            signal_direction=getattr(signal, 'direction', None) or getattr(signal, 'direction', 'UNKNOWN'),
            signal_confidence=getattr(signal, 'confidence', 0.0),
            signal_reasoning=getattr(signal, 'reasoning', ''),
            regime_name=getattr(regime, 'name', 'UNKNOWN') if regime else 'UNKNOWN',
            regime_confidence=getattr(regime, 'confidence', 0.0) if regime else 0.0,
            regime_reason=getattr(regime, 'reason', '') if regime else '',
            strategy_used=getattr(regime, 'recommended_strategy', 'unknown') if regime else 'unknown',
            indicators=indicators or {},
            news_bias=(news_signal or {}).get('bias', 'neutral') if news_signal else 'none',
            news_score=(news_signal or {}).get('score', 0.0) if news_signal else 0.0,
            news_impacted_assets=(news_signal or {}).get('impacted_assets', []) if news_signal else [],
            sizing_method=getattr(sizing_result, 'method', 'unknown'),
            sizing_kelly_pct=getattr(sizing_result, 'kelly_pct', None),
            sizing_size=getattr(sizing_result, 'size', 0.0),
            sizing_quantity=getattr(sizing_result, 'size', 0.0) / entry_price if entry_price > 0 else 0,
            sizing_reason=getattr(sizing_result, 'reason', ''),
            entry_price=entry_price,
            stop_loss=stop_loss or 0.0,
            take_profit=take_profit or 0.0,
            risk_reward_ratio=rr,
            risk_check_passed=getattr(risk_check_result, 'allowed', False),
            risk_check_reason=getattr(risk_check_result, 'reason', ''),
            summary="",  # fill below
        )
        
        # Generate natural language summary
        entry.summary = self._generate_entry_summary(entry, risk_check_result)
        
        # Create trade log
        log = TradeReasonLog(
            trade_id=trade_id,
            trade_number=trade_number,
            symbol=symbol,
            wallet_type=wallet_type,
            direction=direction,
            entry=entry,
            opened_at=now,
            tags=tags or [],
        )
        
        self.trade_logs[trade_id] = log
        self.all_reasons.append(log)
        
        return log

    def log_exit(
        self,
        trade_id: str,
        trade_number: int,
        trigger: str,
        trigger_detail: str,
        exit_price: float,
        entry_price: float,
        pnl: float,
        pnl_pct: float,
        closed_at: Optional[str] = None,
        trailing_info: Optional[Dict[str, float]] = None,
        tags: Optional[List[str]] = None,
    ) -> Optional[ExitReason]:
        """
        บันทึกเหตุผลที่ปิด trade
        """
        now = closed_at or datetime.now().isoformat()
        
        # Calculate holding period
        if trade_id in self.trade_logs:
            entry_time_str = self.trade_logs[trade_id].opened_at
            try:
                entry_time = datetime.fromisoformat(entry_time_str)
                closed_time = datetime.fromisoformat(now)
                duration_min = (closed_time - entry_time).total_seconds() / 60
            except (ValueError, TypeError):
                duration_min = 0.0
        else:
            duration_min = 0.0
        
        # Determine vs expectation
        if trigger == "take_profit":
            vs_exp = "Took profit as planned"
        elif trigger == "stop_loss":
            vs_exp = "Stopped out per risk rule"
        elif trigger == "trailing_stop":
            vs_exp = "Locked profit via trailing stop"
        elif trigger == "regime_change":
            vs_exp = "Exited due to market regime change"
        elif trigger == "risk_manager":
            vs_exp = "Risk manager forced exit"
        else:
            vs_exp = "Manual exit"
        
        exit_reason = ExitReason(
            timestamp=now,
            symbol=self.trade_logs[trade_id].symbol if trade_id in self.trade_logs else "UNKNOWN",
            trade_number=trade_number,
            trigger=trigger,
            trigger_detail=trigger_detail,
            entry_price=entry_price,
            exit_price=exit_price,
            holding_period_minutes=duration_min,
            pnl=pnl,
            pnl_pct=pnl_pct,
            trailing_highest_price=trailing_info.get("high") if trailing_info else None,
            trailing_locked_pct=trailing_info.get("locked_pct") if trailing_info else None,
            vs_entry_expectation=vs_exp,
            summary="",
        )
        
        # Generate natural language summary
        exit_reason.summary = self._generate_exit_summary(exit_reason)
        
        # Attach to existing log
        if trade_id in self.trade_logs:
            self.trade_logs[trade_id].exit = exit_reason
            self.trade_logs[trade_id].closed_at = now
            self.trade_logs[trade_id].duration_minutes = duration_min
        
        return exit_reason

    def _generate_entry_summary(self, entry: EntryReason, risk_check: Any) -> str:
        """สร้างข้อความสรุปเหตุผลเปิด trade"""
        direction_emoji = "🟢" if entry.direction == "BUY" else "🔴"
        
        # Regime description
        regime_desc = {
            "TRENDING": f"ตลาดเป็นเทรนด์ (ADX={entry.regime_confidence:.0%})",
            "RANGING": f"ตลาดแกว่ง/ไม่มีทิศทาง (ADX={entry.regime_confidence:.0%})",
            "VOLATILE": f"ตลาดผันผวนสูง — ใช้ความระมัดระวัง",
            "CRASH": f"ตลาด crash ตรวจพบ — ไม่แนะนำเปิด new positions",
            "UNKNOWN": "ยังไม่ทราบ regime",
        }.get(entry.regime_name, entry.regime_name)
        
        # News description
        if entry.news_bias != "none" and entry.news_bias != "neutral":
            news_desc = f"ข่าว {entry.news_bias} (score={entry.news_score:+.2f}) ส่งผลต่อ {', '.join(entry.news_impacted_assets) if entry.news_impacted_assets else 'ตลาดทั่วไป'}"
        else:
            news_desc = "ไม่มีข่าวสำคัญที่กระทบ"
        
        # Strategy
        strategy_desc = {
            "momentum": "ใช้ Momentum strategy (เทรนด์ต่อเนื่อง)",
            "mean_reversion": "ใช้ Mean Reversion strategy (กลับเข้า mean)",
            "none": "ไม่เทรดเนื่องจาก regime ไม่เหมาะสม",
        }.get(entry.strategy_used, entry.strategy_used)
        
        # Sizing
        if entry.sizing_kelly_pct is not None:
            sizing_desc = f"Kelly {entry.sizing_method}={entry.sizing_kelly_pct:.2%}"
        else:
            sizing_desc = f"{entry.sizing_method} sizing"
        
        # SL/TP
        if entry.stop_loss and entry.stop_loss != entry.entry_price:
            sl_desc = f"SL @ {entry.stop_loss:.2f}"
        else:
            sl_desc = "ไม่มี SL"
        
        if entry.take_profit and entry.take_profit != entry.entry_price:
            tp_desc = f"TP @ {entry.take_profit:.2f}"
        else:
            tp_desc = "ไม่มี TP"
        
        lines = [
            f"{direction_emoji} เปิด {entry.direction} {entry.symbol} @ {entry.entry_price:.2f}",
            f"   Regime: {regime_desc}",
            f"   Strategy: {strategy_desc}",
            f"   {news_desc}",
            f"   Signal confidence: {entry.signal_confidence:.0%} | Reasoning: {entry.signal_reasoning[:80] if entry.signal_reasoning else 'N/A'}",
            f"   {sizing_desc} → size ${entry.sizing_size:,.0f} ({entry.sizing_quantity:.4f} units)",
            f"   {sl_desc} | {tp_desc} | R:R = {entry.risk_reward_ratio:.1f}:1",
            f"   Risk check: {'✅ PASSED' if entry.risk_check_passed else '⚠️ ' + entry.risk_check_reason}",
        ]
        
        return "\n".join(lines)

    def _generate_exit_summary(self, exit: ExitReason) -> str:
        """สร้างข้อความสรุปเหตุผลปิด trade"""
        # Emoji based on P&L
        if exit.pnl > 0:
            emoji = "✅"
            pnl_desc = f"+${exit.pnl:.2f} (+{exit.pnl_pct:.2%})"
        else:
            emoji = "❌"
            pnl_desc = f"${exit.pnl:.2f} ({exit.pnl_pct:.2%})"
        
        # Trigger description
        trigger_desc = {
            "stop_loss": "ถูก Stop Loss",
            "take_profit": "ถึง Take Profit",
            "trailing_stop": "ถูก Trailing Stop",
            "regime_change": "Regime เปลี่ยน",
            "risk_manager": "Risk Manager สั่งปิด",
            "manual": "ปิดเอง",
        }.get(exit.trigger, exit.trigger)
        
        # Duration
        if exit.holding_period_minutes >= 60:
            duration_desc = f"{exit.holding_period_minutes/60:.1f} ชม."
        else:
            duration_desc = f"{exit.holding_period_minutes:.0f} นาที"
        
        lines = [
            f"{emoji} ปิด #{exit.trade_number} {exit.symbol} @ {exit.exit_price:.2f}",
            f"   Trigger: {trigger_desc} — {exit.trigger_detail}",
            f"   ถือมา: {duration_desc}",
            f"   P&L: {pnl_desc}",
            f"   {exit.vs_entry_expectation}",
        ]
        
        if exit.trailing_highest_price:
            lines.append(f"   Trailing: high={exit.trailing_highest_price:.2f}, locked={exit.trailing_locked_pct:.2%}")
        
        return "\n".join(lines)

    def get_trade_reason(self, trade_id: str) -> Optional[TradeReasonLog]:
        """ดึงเหตุผลของ trade ที่ระบุ"""
        return self.trade_logs.get(trade_id)

    def get_all_reasons(self) -> List[TradeReasonLog]:
        """ดึงเหตุผลทั้งหมด"""
        return self.all_reasons

    def print_trade_reason(self, trade_id: str):
        """พิมพ์เหตุผลของ trade สวยงาม"""
        log = self.get_trade_reason(trade_id)
        if not log:
            print(f"ไม่พบ trade {trade_id}")
            return
        
        print("=" * 60)
        print(f"📋 TRADE #{log.trade_number} | {log.symbol} | {log.direction}")
        print("=" * 60)
        
        if log.entry:
            print(log.entry.summary)
        
        if log.exit:
            print()
            print(log.exit.summary)
        else:
            print()
            print("⏳ ยังเปิดอยู่ — รอปิด...")
        
        if log.tags:
            print(f"   Tags: {', '.join(log.tags)}")
        
        print("=" * 60)
