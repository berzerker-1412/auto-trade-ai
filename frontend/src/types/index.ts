// Types for Auto Trade AI

export enum AssetType {
  CRYPTO = "crypto",
  GOLD = "gold"
}

export enum TradeDirection {
  BUY = "buy",
  SELL = "sell"
}

export enum TradeStatus {
  PENDING = "pending",
  OPEN = "open",
  CLOSED = "closed",
  CANCELLED = "cancelled"
}

export interface Trade {
  id: number;
  symbol: string;
  asset_type: AssetType;
  direction: TradeDirection;
  entry_price: number;
  exit_price: number | null;
  quantity: number;
  stop_loss: number | null;
  take_profit: number | null;
  status: TradeStatus;
  entry_time: string | null;
  exit_time: string | null;
  trade_number: number;
  pnl?: number | null;
  pnl_percent?: number | null;
  entry_reason?: EntryReason | null;
  exit_reason?: ExitReason | null;
}

export interface EntryReason {
  timestamp: string;
  symbol: string;
  direction: string;
  signal_direction: string;
  signal_confidence: number;
  signal_reasoning: string;
  regime_name: string;
  regime_confidence: number;
  regime_reason: string;
  strategy_used: string;
  indicators: Record<string, number>;
  news_bias: string;
  news_score: number;
  sizing_method: string;
  sizing_kelly_pct: number | null;
  sizing_size: number;
  sizing_quantity: number;
  sizing_reason: string;
  entry_price: number;
  stop_loss: number;
  take_profit: number;
  risk_reward_ratio: number;
  risk_check_passed: boolean;
  risk_check_reason: string;
  summary: string;
}

export interface ExitReason {
  timestamp: string;
  symbol: string;
  trade_number: number;
  trigger: string;
  trigger_detail: string;
  entry_price: number;
  exit_price: number;
  holding_period_minutes: number;
  pnl: number;
  pnl_pct: number;
  vs_entry_expectation: string;
  trailing_highest_price: number | null;
  trailing_locked_pct: number | null;
  summary: string;
}

export interface TradeSignal {
  symbol: string;
  direction: TradeDirection;
  entry_price: number;
  quantity: number;
  stop_loss?: number;
  take_profit?: number;
  confidence: number;
  reasoning: string;
}

export interface Balance {
  balance: number;
  currency: string;
  initial_balance: number;
  total_pnl: number;
  active_trades: number;
}

export interface TradeStats {
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: string;
  total_pnl: number;
  current_balance: number;
}

export interface Ticker {
  symbol: string;
  price: number;
  bid: number;
  ask: number;
  high: number;
  low: number;
  volume: number;
  change_24h?: number;
}
