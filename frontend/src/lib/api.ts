// API Client for Auto Trade AI Backend
// ดึงข้อมูลจาก FastAPI server ที่ http://localhost:8000

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

// ─── Trader State Interface ─────────────────────────────────
export interface TraderStatus {
  running: boolean;
  mode: string;
  asset: string;
  symbols: string[];
  balance: number;
  initial_balance: number;
}

export interface TraderStats {
  current_balance: number;
  initial_balance: number;
  total_pnl: number;
  total_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: string;
}

export interface ExchangeRates {
  "USD/THB": number;
  "EUR/THB"?: number;
  "GBP/THB"?: number;
  "JPY/THB"?: number;
  lastUpdated?: string;
}

// ─── API Fetch Helper ────────────────────────────────────────
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
    const error = await response.text();
    throw new Error(`API Error ${response.status}: ${error}`);
  }

  return response.json();
}

// ─── Mock Data ──────────────────────────────────────────────
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
      pnl: null,
      pnl_percent: null,
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
  ] as Trade[],
  tickers: {
    "BTC/USDT": { symbol: "BTC/USDT", price: 68250, bid: 68240, ask: 68260, high: 68800, low: 67800, volume: 25000 },
    "ETH/USDT": { symbol: "ETH/USDT", price: 3480, bid: 3478, ask: 3482, high: 3520, low: 3430, volume: 180000 },
    "SOL/USDT": { symbol: "SOL/USDT", price: 96, bid: 95.8, ask: 96.2, high: 99, low: 94, volume: 500000 },
    "XAUUSD": { symbol: "XAUUSD", price: 2035, bid: 2034.5, ask: 2035.5, high: 2040, low: 2020, volume: 0 },
  } as Record<string, Ticker>,
};

// ─── API Client ─────────────────────────────────────────────
// ตั้ง USE_MOCK = false เมื่อ backend รันอยู่
const USE_MOCK = false;

export const api = {
  // ── Trader Control ────────────────────────────────────────
  async getTraderStatus(): Promise<TraderStatus> {
    if (USE_MOCK) {
      return {
        running: false,
        mode: "paper",
        asset: "both",
        symbols: ["BTC/USDT", "ETH/USDT", "XAUUSD"],
        balance: 105000,
        initial_balance: 100000,
      };
    }
    return fetchAPI<TraderStatus>("/api/trader/status");
  },

  async startTrader(config: {
    mode?: string;
    asset?: string;
    symbols?: string[];
    balance?: number;
  }): Promise<TraderStatus> {
    if (USE_MOCK) {
      return {
        running: true,
        mode: config.mode ?? "paper",
        asset: config.asset ?? "both",
        symbols: config.symbols ?? ["BTC/USDT", "ETH/USDT", "XAUUSD"],
        balance: config.balance ?? 100000,
        initial_balance: config.balance ?? 100000,
      };
    }
    return fetchAPI<TraderStatus>("/api/trader/start", {
      method: "POST",
      body: JSON.stringify({
        mode: config.mode ?? "paper",
        asset: config.asset ?? "both",
        symbols: config.symbols ?? ["BTC/USDT", "ETH/USDT", "XAUUSD"],
        balance: config.balance ?? 100000,
      }),
    });
  },

  async stopTrader(): Promise<{ success: boolean; message: string }> {
    if (USE_MOCK) return { success: true, message: "Trader stopped" };
    return fetchAPI<{ success: boolean; message: string }>("/api/trader/stop", {
      method: "POST",
    });
  },

  async getTraderStats(): Promise<TraderStats> {
    if (USE_MOCK) {
      return {
        current_balance: 105000,
        initial_balance: 100000,
        total_pnl: 5000,
        total_trades: 25,
        winning_trades: 16,
        losing_trades: 9,
        win_rate: "64%",
      };
    }
    return fetchAPI<TraderStats>("/api/trader/stats");
  },

  // ── Balance ───────────────────────────────────────────────
  async getBalance(): Promise<Balance> {
    if (USE_MOCK) return MOCK_DATA.balance;
    return fetchAPI<Balance>("/api/balance");
  },

  // ── Stats ─────────────────────────────────────────────────
  async getStats(): Promise<TradeStats> {
    if (USE_MOCK) return MOCK_DATA.stats;
    return fetchAPI<TradeStats>("/api/stats");
  },

  // ── Trades ───────────────────────────────────────────────
  async getTrades(limit = 50): Promise<Trade[]> {
    if (USE_MOCK) return MOCK_DATA.trades;
    return fetchAPI<Trade[]>(`/api/trades?limit=${limit}`);
  },

  async getOpenTrades(): Promise<Trade[]> {
    if (USE_MOCK) return MOCK_DATA.trades.filter((t) => t.status === TradeStatus.OPEN);
    return fetchAPI<Trade[]>("/api/trades/open");
  },

  async closeTrade(symbol: string, exitPrice: number): Promise<Trade> {
    if (USE_MOCK) {
      const trade = MOCK_DATA.trades.find(
        (t) => t.symbol === symbol && t.status === TradeStatus.OPEN
      );
      if (trade) {
        trade.exit_price = exitPrice;
        trade.status = TradeStatus.CLOSED;
        trade.exit_time = new Date().toISOString();
        trade.pnl = (exitPrice - trade.entry_price) * trade.quantity;
        trade.pnl_percent =
          ((exitPrice - trade.entry_price) / trade.entry_price) * 100;
        return trade;
      }
      throw new Error("No open trade found");
    }
    return fetchAPI<Trade>("/api/trades/close", {
      method: "POST",
      body: JSON.stringify({ symbol, exit_price: exitPrice }),
    });
  },

  async createTrade(trade: {
    symbol: string;
    direction: string;
    quantity: number;
    entry_price?: number;
    stop_loss?: number;
    take_profit?: number;
  }): Promise<Trade> {
    if (USE_MOCK) {
      const newTrade: Trade = {
        id: MOCK_DATA.trades.length + 1,
        symbol: trade.symbol,
        asset_type:
          trade.symbol === "XAUUSD" ? AssetType.GOLD : AssetType.CRYPTO,
        direction: trade.direction as TradeDirection,
        entry_price: trade.entry_price ?? 0,
        exit_price: null,
        quantity: trade.quantity,
        stop_loss: trade.stop_loss ?? null,
        take_profit: trade.take_profit ?? null,
        status: TradeStatus.OPEN,
        entry_time: new Date().toISOString(),
        exit_time: null,
        trade_number: MOCK_DATA.trades.length + 1,
        pnl: null,
        pnl_percent: null,
      };
      MOCK_DATA.trades.push(newTrade);
      return newTrade;
    }
    return fetchAPI<Trade>("/api/trades", {
      method: "POST",
      body: JSON.stringify(trade),
    });
  },

  // ── Tickers ───────────────────────────────────────────────
  async getTickers(): Promise<Record<string, Ticker>> {
    if (USE_MOCK) return MOCK_DATA.tickers;
    return fetchAPI<Record<string, Ticker>>("/api/tickers");
  },

  async getTicker(symbol: string): Promise<Ticker> {
    if (USE_MOCK) return MOCK_DATA.tickers[symbol] || MOCK_DATA.tickers["BTC/USDT"];
    return fetchAPI<Ticker>(`/api/ticker/${encodeURIComponent(symbol)}`);
  },

  // ── Execute Signal ────────────────────────────────────────
  async executeSignal(signal: TradeSignal): Promise<Trade> {
    if (USE_MOCK) {
      const ticker = MOCK_DATA.tickers[signal.symbol];
      const newTrade: Trade = {
        id: MOCK_DATA.trades.length + 1,
        symbol: signal.symbol,
        asset_type:
          signal.symbol === "XAUUSD" ? AssetType.GOLD : AssetType.CRYPTO,
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
        pnl: null,
        pnl_percent: null,
      };
      MOCK_DATA.trades.push(newTrade);
      return newTrade;
    }
    return fetchAPI<Trade>("/api/trade/execute", {
      method: "POST",
      body: JSON.stringify(signal),
    });
  },

  // ── Exchange Rates ────────────────────────────────────────
  async getExchangeRates(): Promise<ExchangeRates> {
    if (USE_MOCK) {
      return {
        "USD/THB": 35.5,
        "EUR/THB": 38.2,
        "GBP/THB": 44.5,
        "JPY/THB": 0.235,
        lastUpdated: undefined,
      };
    }
    return fetchAPI<ExchangeRates>("/api/exchange-rates");
  },

  // ── Settings ───────────────────────────────────────────────
  async getSettings(): Promise<Record<string, string>> {
    if (USE_MOCK) {
      return {
        max_position_size: "0.1",
        stop_loss_percent: "2.0",
        take_profit_percent: "5.0",
        max_concurrent_trades: "3",
      };
    }
    return fetchAPI<Record<string, string>>("/api/settings");
  },

  async updateSettings(settings: Record<string, string>): Promise<{ success: boolean }> {
    if (USE_MOCK) return { success: true };
    return fetchAPI<{ success: boolean }>("/api/settings", {
      method: "POST",
      body: JSON.stringify(settings),
    });
  },

  // ── News / Intelligence ────────────────────────────────────

  async getNewsFeed(limit = 50, category?: string): Promise<{
    articles: NewsArticle[];
    trade_signal: NewsSignal;
    total: number;
    generated_at: string;
  }> {
    if (USE_MOCK) {
      return {
        articles: MOCK_NEWS_ARTICLES,
        trade_signal: MOCK_NEWS_SIGNAL,
        total: MOCK_NEWS_ARTICLES.length,
        generated_at: new Date().toISOString(),
      };
    }
    const params = new URLSearchParams({ limit: String(limit) });
    if (category && category !== "all") params.set("category", category);
    return fetchAPI(`/api/news/feed?${params}`);
  },

  async triggerNewsScrape(): Promise<{
    status: string;
    total_saved: number;
    sources_scraped: number;
    errors: string[];
  }> {
    return fetchAPI("/api/news/scrape", { method: "POST" });
  },

  async getNewsSignal(): Promise<NewsSignal> {
    if (USE_MOCK) return MOCK_NEWS_SIGNAL;
    return fetchAPI("/api/news/signal");
  },

  async getNewsArticle(id: number): Promise<NewsArticle> {
    if (USE_MOCK) {
      return MOCK_NEWS_ARTICLES.find((a) => a.id === id) || MOCK_NEWS_ARTICLES[0];
    }
    return fetchAPI(`/api/news/article/${id}`);
  },
};

// ── Mock Data ────────────────────────────────────────────────

const MOCK_NEWS_ARTICLES: NewsArticle[] = [
  {
    id: 1,
    title: "Fed signals potential rate cut amid cooling inflation data",
    url: "https://reuters.com",
    source: "Reuters",
    category: "economy",
    published_at: new Date(Date.now() - 3600000).toISOString(),
    summary: "Federal Reserve officials indicated they may consider cutting interest rates...",
    content: "",
    sentiment_score: 0.4,
    sentiment_label: "positive",
    impact_tags: ["USD", "DXY", "FOREX"],
  },
  {
    id: 2,
    title: "Bitcoin surges past $68,000 as institutional inflows continue",
    url: "https://bloomberg.com",
    source: "Bloomberg",
    category: "crypto",
    published_at: new Date(Date.now() - 7200000).toISOString(),
    summary: "Bitcoin price rallied to new highs amid continued institutional buying...",
    content: "",
    sentiment_score: 0.6,
    sentiment_label: "positive",
    impact_tags: ["CRYPTO", "BTC"],
  },
  {
    id: 3,
    title: "Ukraine-Russia conflict escalates with new offensive operations",
    url: "https://bbc.com",
    source: "BBC News",
    category: "war",
    published_at: new Date(Date.now() - 10800000).toISOString(),
    summary: "Military operations intensified along the eastern front lines...",
    content: "",
    sentiment_score: -0.7,
    sentiment_label: "negative",
    impact_tags: ["XAUUSD", "EUR", "RISK_OFF"],
  },
  {
    id: 4,
    title: "Gold hits record high as safe-haven demand surges",
    url: "https://reuters.com",
    source: "Reuters",
    category: "commodities",
    published_at: new Date(Date.now() - 14400000).toISOString(),
    summary: "Gold prices climbed to all-time highs driven by geopolitical uncertainty...",
    content: "",
    sentiment_score: 0.5,
    sentiment_label: "positive",
    impact_tags: ["XAUUSD"],
  },
  {
    id: 5,
    title: "Solana network experiences outage amid high transaction volume",
    url: "https://coindesk.com",
    source: "CoinDesk",
    category: "crypto",
    published_at: new Date(Date.now() - 18000000).toISOString(),
    summary: "Solana blockchain went offline for several hours due to network congestion...",
    content: "",
    sentiment_score: -0.5,
    sentiment_label: "negative",
    impact_tags: ["CRYPTO", "SOL"],
  },
];

const MOCK_NEWS_SIGNAL: NewsSignal = {
  bias: "bullish",
  score: 0.27,
  signal: {
    direction: "buy",
    top_assets: ["CRYPTO", "XAUUSD", "USD"],
    confidence: 0.55,
  },
  reason: "Mixed sentiment (0.27) from 5 articles — crypto bullish offset by war risk",
  impacted_assets: ["CRYPTO", "XAUUSD", "USD", "EUR"],
  asset_sentiments: { CRYPTO: 0.55, XAUUSD: 0.5, USD: 0.4, EUR: -0.35 },
  category_breakdown: { crypto: 2, war: 1, economy: 1, commodities: 1 },
  risk_level: "medium",
  article_count: 5,
};

interface NewsArticle {
  id: number;
  title: string;
  url: string;
  source: string;
  category: string;
  published_at: string | null;
  summary: string;
  content: string;
  content_th?: string;     // เนื้อหาแปลไทย
  sentiment_score: number;
  sentiment_label: "positive" | "negative" | "neutral";
  impact_tags: string[];
}

interface NewsSignal {
  bias: string;
  score: number;
  signal: {
    direction: string;
    top_assets: string[];
    confidence: number;
    reason?: string;
  } | null;
  reason: string;
  impacted_assets: string[];
  asset_sentiments: Record<string, number>;
  category_breakdown: Record<string, number>;
  risk_level: string;
  article_count: number;
}

