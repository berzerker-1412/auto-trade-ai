"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  createChart,
  IChartApi,
  CandlestickData,
  Time,
  CrosshairMode,
  CandlestickSeries,
  LineSeries,
} from "lightweight-charts";
import { Ticker } from "@/types";
import { cn, formatCurrency } from "@/lib/utils";
import {
  ArrowLeft,
  TrendingUp,
  TrendingDown,
  RefreshCw,
  Clock,
  Zap,
  Activity,
  BarChart2,
  ChevronDown,
} from "lucide-react";

// ─────────────────────────────────────────────────
// ข้อมูลเริ่มต้นของแต่ละ Asset
// ─────────────────────────────────────────────────
const ASSET_CONFIG: Record<string, { name: string; color: string; basePrice: number }> = {
  "BTC/USDT": { name: "Bitcoin", color: "#F7931A", basePrice: 68250 },
  "ETH/USDT": { name: "Ethereum", color: "#627EEA", basePrice: 3480 },
  "SOL/USDT": { name: "Solana", color: "#00FFA3", basePrice: 96 },
  "XAUUSD": { name: "Gold (XAU/USD)", color: "#FFD700", basePrice: 2035 },
};

// กรอบเวลาที่รองรับ
const TIMEFRAMES = [
  { label: "1m", value: "1m", seconds: 60 },
  { label: "5m", value: "5m", seconds: 300 },
  { label: "15m", value: "15m", seconds: 900 },
  { label: "1h", value: "1h", seconds: 3600 },
  { label: "4h", value: "4h", seconds: 14400 },
  { label: "1D", value: "1d", seconds: 86400 },
];

// ─────────────────────────────────────────────────
// สร้างข้อมูลเทียบ
// ─────────────────────────────────────────────────
function generateCandleData(
  basePrice: number,
  count: number,
  intervalSeconds: number,
  endTime?: number
): CandlestickData<Time>[] {
  const data: CandlestickData<Time>[] = [];
  const now = endTime ?? Math.floor(Date.now() / 1000);
  let price = basePrice * 0.85; // เริ่มต่ำกว่าปัจจุบันเล็กน้อย

  for (let i = count; i >= 0; i--) {
    const time = (now - i * intervalSeconds) as Time;
    const volatility = price * 0.008;
    const open = price;
    const change = (Math.random() - 0.47) * volatility;
    const close = open + change;
    const high = Math.max(open, close) + Math.random() * volatility * 0.4;
    const low = Math.min(open, close) - Math.random() * volatility * 0.4;

    data.push({ time, open, high, low, close });
    price = close;
  }
  return data;
}

// ─────────────────────────────────────────────────
// Indicator Panel Component
// ─────────────────────────────────────────────────
function IndicatorPanel({ ticker, symbol }: { ticker: Ticker; symbol: string }) {
  const isCrypto = symbol !== "XAUUSD";

  // Mock indicators for demo
  const indicators = {
    rsi: 30 + Math.random() * 60,
    macd: (Math.random() - 0.4) * 100,
    macdSignal: (Math.random() - 0.4) * 80,
    adx: 15 + Math.random() * 40,
    ema20: ticker.price * 0.998,
    ema50: ticker.price * 0.995,
    sma200: ticker.price * 0.97,
    bbUpper: ticker.price * 1.015,
    bbLower: ticker.price * 0.985,
    atr: ticker.price * 0.005,
    volume: ticker.volume,
  };

  const indicatorItems = [
    { label: "RSI (14)", value: indicators.rsi.toFixed(1), unit: "", status: indicators.rsi > 70 ? "overbought" : indicators.rsi < 30 ? "oversold" : "neutral" },
    { label: "MACD", value: indicators.macd.toFixed(2), unit: "", status: "neutral" },
    { label: "MACD Signal", value: indicators.macdSignal.toFixed(2), unit: "", status: "neutral" },
    { label: "ADX", value: indicators.adx.toFixed(1), unit: "", status: indicators.adx > 25 ? "strong" : "weak" },
    { label: "EMA 20", value: formatCurrency(indicators.ema20, "USD"), unit: "", status: ticker.price > indicators.ema20 ? "bullish" : "bearish" },
    { label: "EMA 50", value: formatCurrency(indicators.ema50, "USD"), unit: "", status: ticker.price > indicators.ema50 ? "bullish" : "bearish" },
    { label: "SMA 200", value: formatCurrency(indicators.sma200, "USD"), unit: "", status: ticker.price > indicators.sma200 ? "bullish" : "bearish" },
    { label: "BB Upper", value: formatCurrency(indicators.bbUpper, "USD"), unit: "", status: "neutral" },
    { label: "BB Lower", value: formatCurrency(indicators.bbLower, "USD"), unit: "", status: "neutral" },
    { label: "ATR (14)", value: indicators.atr.toFixed(2), unit: "", status: "neutral" },
    { label: "Volume 24h", value: `${(indicators.volume / 1000).toFixed(0)}K`, unit: "", status: "neutral" },
    { label: "Spread", value: `${((ticker.ask - ticker.bid) / ticker.price * 100).toFixed(3)}%`, unit: "", status: "neutral" },
  ];

  return (
    <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
      <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
        <Activity className="h-4 w-4 text-emerald-400" />
        Technical Indicators
      </h3>
      <div className="grid grid-cols-2 gap-2">
        {indicatorItems.map((item) => (
          <div
            key={item.label}
            className="flex items-center justify-between px-3 py-2 rounded-lg bg-gray-800/50 hover:bg-gray-800 transition-colors"
          >
            <span className="text-xs text-gray-500">{item.label}</span>
            <span
              className={cn(
                "text-xs font-semibold",
                item.status === "overbought"
                  ? "text-red-400"
                  : item.status === "oversold"
                  ? "text-emerald-400"
                  : item.status === "bullish"
                  ? "text-emerald-400"
                  : item.status === "bearish"
                  ? "text-red-400"
                  : item.status === "strong"
                  ? "text-emerald-400"
                  : item.status === "weak"
                  ? "text-yellow-400"
                  : "text-white"
              )}
            >
              {item.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────
// Signal Badge Component
// ─────────────────────────────────────────────────
function SignalBadge({ confidence }: { confidence: number }) {
  const level =
    confidence >= 0.7 ? "STRONG" :
    confidence >= 0.4 ? "MODERATE" : "WEAK";

  const colorClass =
    confidence >= 0.7 ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30" :
    confidence >= 0.4 ? "bg-yellow-500/10 text-yellow-400 border-yellow-500/30" :
    "bg-red-500/10 text-red-400 border-red-500/30";

  const direction = Math.random() > 0.5 ? "BUY" : "SELL";

  return (
    <div className={cn("rounded-lg border px-3 py-2 text-center", colorClass)}>
      <p className="text-xs font-bold">{direction}</p>
      <p className="text-xs text-gray-400 mt-0.5">
        {level} · {(confidence * 100).toFixed(0)}% confidence
      </p>
    </div>
  );
}

// ─────────────────────────────────────────────────
// Main Live View Page
// ─────────────────────────────────────────────────
export default function LiveAssetPage() {
  const params = useParams();
  const symbol = decodeURIComponent(params.symbol as string);
  const config = ASSET_CONFIG[symbol] ?? ASSET_CONFIG["BTC/USDT"];

  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const candleSeriesRef = useRef<unknown>(null);
  const prevPriceRef = useRef<number>(config.basePrice);

  const [ticker, setTicker] = useState<Ticker>({
    symbol,
    price: config.basePrice,
    bid: config.basePrice - 5,
    ask: config.basePrice + 5,
    high: config.basePrice * 1.02,
    low: config.basePrice * 0.98,
    volume: symbol === "XAUUSD" ? 0 : 25000,
  });

  const [selectedTimeframe, setSelectedTimeframe] = useState("1h");
  const [priceFlash, setPriceFlash] = useState<"up" | "down" | null>(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [isConnected, setIsConnected] = useState(true);
  const [showTimeframeDropdown, setShowTimeframeDropdown] = useState(false);

  const isCrypto = symbol !== "XAUUSD";

  // ── Initialize Chart ───────────────────────────────────
  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { color: "transparent" },
        textColor: "#9ca3af",
      },
      grid: {
        vertLines: { color: "#1f2937" },
        horzLines: { color: "#1f2937" },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { color: "#6b7280", width: 1, style: 2, labelBackgroundColor: "#374151" },
        horzLine: { color: "#6b7280", width: 1, style: 2, labelBackgroundColor: "#374151" },
      },
      rightPriceScale: { borderColor: "#374151" },
      timeScale: { borderColor: "#374151", timeVisible: true, secondsVisible: false },
      handleScale: { axisPressedMouseMove: true },
      handleScroll: { vertTouchDrag: false },
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: "#10b981",
      downColor: "#ef4444",
      borderUpColor: "#10b981",
      borderDownColor: "#ef4444",
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });

    chartRef.current = chart;
    (candleSeriesRef as React.MutableRefObject<unknown>).current = candleSeries;

    // โหลดข้อมูลเริ่มต้น
    const tf = TIMEFRAMES.find((t) => t.value === selectedTimeframe) ?? TIMEFRAMES[3];
    const data = generateCandleData(config.basePrice, 100, tf.seconds);
    candleSeries.setData(data);

    // Resize handler
    const handleResize = () => {
      if (containerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: containerRef.current.clientWidth });
      }
    };
    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, [symbol, selectedTimeframe, config.basePrice]);

  // ── Live Price Simulation ──────────────────────────────
  useEffect(() => {
    let direction = 1;
    let currentPrice = config.basePrice;

    const interval = setInterval(() => {
      const volatility = currentPrice * (symbol === "XAUUSD" ? 0.0002 : 0.0008);
      const change = (Math.random() - 0.48) * volatility;
      currentPrice = Math.max(currentPrice + change, 0.01);
      direction = change >= 0 ? 1 : -1;

      const spread = currentPrice * 0.0002;
      const newTicker: Ticker = {
        symbol,
        price: currentPrice,
        bid: currentPrice - spread,
        ask: currentPrice + spread,
        high: Math.max(ticker.high, currentPrice),
        low: Math.min(ticker.low, currentPrice),
        volume: ticker.volume + Math.floor(Math.random() * 100),
      };

      setTicker(newTicker);
      setLastUpdate(new Date());
      prevPriceRef.current = currentPrice;

      // Flash animation
      setPriceFlash(direction > 0 ? "up" : "down");
      setTimeout(() => setPriceFlash(null), 400);

      // อัปเดตแท่งสุดท้ายบนกราฟ
      if (candleSeriesRef.current) {
        const candleSeries = candleSeriesRef.current as { update: (c: CandlestickData<Time>) => void };
        const tf = TIMEFRAMES.find((t) => t.value === selectedTimeframe) ?? TIMEFRAMES[3];
        const now = Math.floor(Date.now() / 1000);
        const currentBarTime = (now - (now % tf.seconds)) as Time;

        candleSeries.update({
          time: currentBarTime,
          open: currentPrice,
          high: currentPrice,
          low: currentPrice,
          close: currentPrice,
        });
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [symbol, selectedTimeframe, config.basePrice]);

  // ── Timeframe change → reload chart data ──────────────
  const handleTimeframeChange = useCallback((tfValue: string) => {
    setSelectedTimeframe(tfValue);
    setShowTimeframeDropdown(false);
  }, []);

  const priceChange = ticker.high - ticker.low;
  const priceChangePercent = ((priceChange / ticker.low) * 100).toFixed(2);

  return (
    <div className="p-6 space-y-4">
      {/* ── Header ── */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <Link
            href="/live"
            className="flex items-center gap-1 text-gray-500 hover:text-white transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white">{config.name}</h1>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full animate-pulse" style={{ backgroundColor: config.color }} />
                <span className="text-sm text-gray-500">{symbol}</span>
              </div>
            </div>
            <p className="text-xs text-gray-600 mt-0.5">
              Live · Updated {lastUpdate.toLocaleTimeString()}
            </p>
          </div>
        </div>

        {/* Timeframe Selector */}
        <div className="relative">
          <button
            onClick={() => setShowTimeframeDropdown(!showTimeframeDropdown)}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-gray-800 border border-gray-700 text-white hover:border-gray-600 transition-colors"
          >
            <Clock className="h-4 w-4 text-gray-400" />
            <span className="font-medium">{selectedTimeframe}</span>
            <ChevronDown className="h-4 w-4 text-gray-400" />
          </button>

          {showTimeframeDropdown && (
            <div className="absolute right-0 mt-2 w-28 rounded-xl bg-gray-900 border border-gray-800 shadow-xl z-50 overflow-hidden">
              {TIMEFRAMES.map((tf) => (
                <button
                  key={tf.value}
                  onClick={() => handleTimeframeChange(tf.value)}
                  className={cn(
                    "w-full text-left px-4 py-2 text-sm hover:bg-gray-800 transition-colors",
                    selectedTimeframe === tf.value
                      ? "text-emerald-400 bg-gray-800/50"
                      : "text-gray-400"
                  )}
                >
                  {tf.label}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ── Price Display ── */}
      <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-6">
        <div className="flex items-start justify-between">
          {/* ราคาหลัก */}
          <div>
            <div className="flex items-baseline gap-3">
              <span
                className={cn(
                  "text-5xl font-bold text-white transition-colors duration-300",
                  priceFlash === "up" && "text-emerald-400",
                  priceFlash === "down" && "text-red-400"
                )}
              >
                {isCrypto ? "$" : ""}
                {formatCurrency(ticker.price, isCrypto ? "USD" : "XAU")}
              </span>
              <span
                className={cn(
                  "text-lg font-semibold",
                  parseFloat(priceChangePercent) >= 0 ? "text-emerald-400" : "text-red-400"
                )}
              >
                {parseFloat(priceChangePercent) >= 0 ? "+" : ""}
                {priceChangePercent}%
              </span>
            </div>

            {/* Bid / Ask */}
            <div className="mt-3 flex items-center gap-6">
              <div>
                <span className="text-xs text-gray-500">Bid </span>
                <span className="text-sm font-semibold text-emerald-400">
                  {formatCurrency(ticker.bid, isCrypto ? "USD" : "XAU")}
                </span>
              </div>
              <div>
                <span className="text-xs text-gray-500">Ask </span>
                <span className="text-sm font-semibold text-red-400">
                  {formatCurrency(ticker.ask, isCrypto ? "USD" : "XAU")}
                </span>
              </div>
              <div className="text-xs text-gray-600">
                Spread: {((ticker.ask - ticker.bid) / ticker.price * 100).toFixed(3)}%
              </div>
            </div>

            {/* Stats */}
            <div className="mt-4 flex items-center gap-6 text-sm">
              <div>
                <span className="text-gray-500">24h High: </span>
                <span className="text-white font-medium">{formatCurrency(ticker.high)}</span>
              </div>
              <div>
                <span className="text-gray-500">24h Low: </span>
                <span className="text-white font-medium">{formatCurrency(ticker.low)}</span>
              </div>
              <div>
                <span className="text-gray-500">24h Vol: </span>
                <span className="text-white font-medium">
                  {ticker.volume > 1000 ? `${(ticker.volume / 1000).toFixed(0)}K` : ticker.volume}
                </span>
              </div>
            </div>
          </div>

          {/* Signal + Connection */}
          <div className="flex flex-col items-end gap-3">
            <div className="flex items-center gap-2">
              <div className={cn("w-2 h-2 rounded-full", isConnected ? "bg-emerald-500 animate-pulse" : "bg-red-500")} />
              <span className="text-xs text-gray-500">{isConnected ? "Live" : "Disconnected"}</span>
            </div>
            <SignalBadge confidence={0.3 + Math.random() * 0.5} />
          </div>
        </div>
      </div>

      {/* ── Chart ── */}
      <div className="rounded-xl bg-gray-900/50 border border-gray-800 overflow-hidden">
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <BarChart2 className="h-4 w-4 text-emerald-400" />
            <span className="text-sm font-medium text-white">Price Chart</span>
            <span className="text-xs text-gray-500">· {selectedTimeframe}</span>
          </div>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <RefreshCw className="h-3 w-3" />
            Auto-refresh
          </div>
        </div>
        <div ref={containerRef} className="h-80" />
      </div>

      {/* ── Bottom Grid: Indicators + Actions ── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Indicators */}
        <div className="lg:col-span-2">
          <IndicatorPanel ticker={ticker} symbol={symbol} />
        </div>

        {/* Quick Actions */}
        <div className="space-y-4">
          {/* Trade Actions */}
          <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
            <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
              <Zap className="h-4 w-4 text-yellow-400" />
              Quick Trade
            </h3>
            <div className="space-y-2">
              <button className="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm transition-colors">
                Buy / Long
              </button>
              <button className="w-full py-2.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-semibold text-sm transition-colors">
                Sell / Short
              </button>
              <Link
                href="/trade"
                className="block w-full py-2.5 rounded-xl border border-gray-700 hover:border-gray-600 text-gray-400 hover:text-white text-center text-sm font-medium transition-colors"
              >
                Open Paper Trade
              </Link>
            </div>
          </div>

          {/* Asset Info */}
          <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
            <h3 className="text-sm font-semibold text-white mb-3">Asset Info</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Type</span>
                <span className="text-white">{isCrypto ? "Crypto" : "Commodity"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Exchange</span>
                <span className="text-white">{isCrypto ? "Binance" : "Forex"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Update</span>
                <span className="text-emerald-400">2s</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Status</span>
                <span className="text-emerald-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  Active
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
