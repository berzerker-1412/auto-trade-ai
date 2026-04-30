// API Client for Auto Trade AI Backend

import {
  Trade,
  TradeStats,
  Balance,
  Ticker,
  TradeSignal,
  AssetType,
  TradeDirection,
  TradeStatus,
} from "../types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }

  return response.json();
}

// Mock data for demo when backend is not running
const MOCK_DATA = {
  balance: {
    balance: 105000,
    currency: "USDT",
    initial_balance: 100000,
    total_pnl: 5000,
    active_trades: 2,
  },
  stats: {
    total_trades: 25,
    winning_trades: 16,
    losing_trades: 9,
    win_rate: "64%",
    total_pnl: 5000,
    current_balance: 105000,
  },
  trades: [
    {
      id: 1,
      symbol: "BTC/USDT",
      asset_type: AssetType.CRYPTO,
      direction: TradeDirection.BUY,
      entry_price: 67500,
      exit_price: 68200,
      quantity: 0.01,
      stop_loss: 66500,
      take_profit: 69000,
      status: TradeStatus.CLOSED,
      entry_time: "2024-01-15T10:30:00",
      exit_time: "2024-01-15T14:45:00",
      trade_number: 1,
      pnl: 700,
      pnl_percent: 1.04,
    },
    {
      id: 2,
      symbol: "ETH/USDT",
      asset_type: AssetType.CRYPTO,
      direction: TradeDirection.BUY,
      entry_price: 3450,
      exit_price: null,
      quantity: 0.5,
      stop_loss: 3380,
      take_profit: 3600,
      status: TradeStatus.OPEN,
      entry_time: "2024-01-15T09:00:00",
      exit_time: null,
      trade_number: 2,
    },
    {
      id: 3,
      symbol: "XAUUSD",
      asset_type: AssetType.GOLD,
      direction: TradeDirection.BUY,
      entry_price: 2020,
      exit_price: 2035,
      quantity: 1,
      stop_loss: 2000,
      take_profit: 2050,
      status: TradeStatus.CLOSED,
      entry_time: "2024-01-14T15:00:00",
      exit_time: "2024-01-14T18:30:00",
      trade_number: 1,
      pnl: 15,
      pnl_percent: 0.74,
    },
    {
      id: 4,
      symbol: "BTC/USDT",
      asset_type: AssetType.CRYPTO,
      direction: TradeDirection.SELL,
      entry_price: 68000,
      exit_price: 67200,
      quantity: 0.005,
      stop_loss: 68500,
      take_profit: 66500,
      status: TradeStatus.CLOSED,
      entry_time: "2024-01-13T11:00:00",
      exit_time: "2024-01-13T16:00:00",
      trade_number: 3,
      pnl: 40,
      pnl_percent: 1.18,
    },
    {
      id: 5,
      symbol: "SOL/USDT",
      asset_type: AssetType.CRYPTO,
      direction: TradeDirection.BUY,
      entry_price: 98,
      exit_price: 95,
      quantity: 5,
      stop_loss: 96,
      take_profit: 105,
      status: TradeStatus.CLOSED,
      entry_time: "2024-01-12T10:00:00",
      exit_time: "2024-01-12T15:00:00",
      trade_number: 4,
      pnl: -15,
      pnl_percent: -3.06,
    },
  ] as Trade[],
  tickers: {
    "BTC/USDT": { symbol: "BTC/USDT", price: 68250, bid: 68240, ask: 68260, high: 68800, low: 67800, volume: 25000 },
    "ETH/USDT": { symbol: "ETH/USDT", price: 3480, bid: 3478, ask: 3482, high: 3520, low: 3430, volume: 180000 },
    "SOL/USDT": { symbol: "SOL/USDT", price: 96, bid: 95.8, ask: 96.2, high: 99, low: 94, volume: 500000 },
    "XAUUSD": { symbol: "XAUUSD", price: 2035, bid: 2034.5, ask: 2035.5, high: 2040, low: 2020, volume: 0 },
  } as Record<string, Ticker>,
};

const USE_MOCK = true;

export const api = {
  // Balance
  async getBalance(): Promise<Balance> {
    if (USE_MOCK) return MOCK_DATA.balance;
    return fetchAPI<Balance>("/api/balance");
  },

  // Stats
  async getStats(symbol?: string): Promise<TradeStats> {
    if (USE_MOCK) return MOCK_DATA.stats;
    return fetchAPI<TradeStats>(`/api/stats${symbol ? `?symbol=${symbol}` : ""}`);
  },

  // Trades
  async getTrades(limit = 50): Promise<Trade[]> {
    if (USE_MOCK) return MOCK_DATA.trades;
    return fetchAPI<Trade[]>(`/api/trades?limit=${limit}`);
  },

  async getOpenTrades(): Promise<Trade[]> {
    if (USE_MOCK) return MOCK_DATA.trades.filter((t) => t.status === "open");
    return fetchAPI<Trade[]>("/api/trades/open");
  },

  async closeTrade(symbol: string, exitPrice: number): Promise<Trade> {
    if (USE_MOCK) {
      const trade = MOCK_DATA.trades.find((t) => t.symbol === symbol && t.status === "open");
      if (trade) {
        trade.exit_price = exitPrice;
        trade.status = TradeStatus.CLOSED;
        trade.exit_time = new Date().toISOString();
        trade.pnl = (exitPrice - trade.entry_price) * trade.quantity;
        return trade;
      }
      throw new Error("No open trade found");
    }
    return fetchAPI<Trade>(`/api/trades/close`, {
      method: "POST",
      body: JSON.stringify({ symbol, exit_price: exitPrice }),
    });
  },

  // Tickers
  async getTickers(): Promise<Record<string, Ticker>> {
    if (USE_MOCK) return MOCK_DATA.tickers;
    return fetchAPI<Record<string, Ticker>>("/api/tickers");
  },

  async getTicker(symbol: string): Promise<Ticker> {
    if (USE_MOCK) return MOCK_DATA.tickers[symbol] || MOCK_DATA.tickers["BTC/USDT"];
    return fetchAPI<Ticker>(`/api/ticker/${encodeURIComponent(symbol)}`);
  },

  // Execute Signal
  async executeSignal(signal: TradeSignal): Promise<Trade> {
    if (USE_MOCK) {
      const ticker = MOCK_DATA.tickers[signal.symbol];
      const newTrade: Trade = {
        id: MOCK_DATA.trades.length + 1,
        symbol: signal.symbol,
        asset_type: signal.symbol === "XAUUSD" ? AssetType.GOLD : AssetType.CRYPTO,
        direction: signal.direction,
        entry_price: ticker?.price || signal.entry_price,
        exit_price: null,
        quantity: signal.quantity,
        stop_loss: signal.stop_loss ?? null,
        take_profit: signal.take_profit ?? null,
        status: TradeStatus.OPEN,
        entry_time: new Date().toISOString(),
        exit_time: null,
        trade_number: MOCK_DATA.trades.length + 1,
      };
      MOCK_DATA.trades.push(newTrade);
      return newTrade;
    }
    return fetchAPI<Trade>("/api/trade/execute", {
      method: "POST",
      body: JSON.stringify(signal),
    });
  },
};
