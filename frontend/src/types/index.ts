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
