"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Ticker, TradeSignal, TradeDirection } from "@/types";
import {
  formatCurrency,
  cn,
  getDirectionColor,
} from "@/lib/utils";
import {
  ArrowUpRight,
  ArrowDownRight,
  Play,
  RefreshCw,
  Zap,
} from "lucide-react";

export default function TradePage() {
  const [tickers, setTickers] = useState<Record<string, Ticker>>({});
  const [selectedSymbol, setSelectedSymbol] = useState("BTC/USDT");
  const [direction, setDirection] = useState<TradeDirection>(TradeDirection.BUY);
  const [quantity, setQuantity] = useState("0.01");
  const [stopLoss, setStopLoss] = useState("");
  const [takeProfit, setTakeProfit] = useState("");
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  useEffect(() => {
    async function loadTickers() {
      try {
        const data = await api.getTickers();
        setTickers(data);
      } catch (error) {
        console.error("Failed to load tickers:", error);
      } finally {
        setLoading(false);
      }
    }
    loadTickers();
    const interval = setInterval(loadTickers, 5000);
    return () => clearInterval(interval);
  }, []);

  const currentTicker = tickers[selectedSymbol];

  const handleExecute = async () => {
    if (!currentTicker) return;

    setExecuting(true);
    setResult(null);

    try {
      const signal: TradeSignal = {
        symbol: selectedSymbol,
        direction,
        entry_price: currentTicker.price,
        quantity: parseFloat(quantity),
        stop_loss: stopLoss ? parseFloat(stopLoss) : undefined,
        take_profit: takeProfit ? parseFloat(takeProfit) : undefined,
        confidence: 0.85,
        reasoning: "Manual paper trade execution",
      };

      await api.executeSignal(signal);
      setResult({ success: true, message: `Position opened: ${direction.toUpperCase()} ${quantity} ${selectedSymbol}` });
      setStopLoss("");
      setTakeProfit("");
    } catch (error) {
      setResult({ success: false, message: "Failed to execute trade" });
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-400" />
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Paper Trade</h1>
        <p className="mt-1 text-gray-500">Execute simulated trades without real money</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Symbol Selection */}
        <div className="lg:col-span-2 space-y-6">
          {/* Symbol Tabs */}
          <div className="flex gap-2 flex-wrap">
            {Object.keys(tickers).map((symbol) => (
              <button
                key={symbol}
                onClick={() => setSelectedSymbol(symbol)}
                className={cn(
                  "rounded-lg px-4 py-2 text-sm font-medium transition-all",
                  selectedSymbol === symbol
                    ? "bg-emerald-500 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                )}
              >
                {symbol}
              </button>
            ))}
          </div>

          {/* Price Display */}
          {currentTicker && (
            <div className="rounded-2xl bg-gray-900/50 border border-gray-800 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">{currentTicker.symbol}</p>
                  <p className="mt-2 text-4xl font-bold text-white">
                    {formatCurrency(currentTicker.price)}
                  </p>
                </div>
                <div className="text-right">
                  <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm">
                    <div>
                      <p className="text-gray-500">High</p>
                      <p className="font-medium text-white">{formatCurrency(currentTicker.high)}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Low</p>
                      <p className="font-medium text-white">{formatCurrency(currentTicker.low)}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Bid</p>
                      <p className="font-medium text-emerald-400">{formatCurrency(currentTicker.bid)}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Ask</p>
                      <p className="font-medium text-red-400">{formatCurrency(currentTicker.ask)}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Trading Form */}
          <div className="rounded-2xl bg-gray-900/50 border border-gray-800 p-6 space-y-6">
            <h3 className="text-lg font-semibold text-white">New Position</h3>

            {/* Direction Toggle */}
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => setDirection(TradeDirection.BUY)}
                className={cn(
                  "flex items-center justify-center gap-2 rounded-xl py-4 font-semibold transition-all",
                  direction === TradeDirection.BUY
                    ? "bg-emerald-500 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                )}
              >
                <ArrowUpRight className="h-5 w-5" />
                BUY / LONG
              </button>
              <button
                onClick={() => setDirection(TradeDirection.SELL)}
                className={cn(
                  "flex items-center justify-center gap-2 rounded-xl py-4 font-semibold transition-all",
                  direction === TradeDirection.SELL
                    ? "bg-red-500 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                )}
              >
                <ArrowDownRight className="h-5 w-5" />
                SELL / SHORT
              </button>
            </div>

            {/* Quantity */}
            <div>
              <label className="block text-sm text-gray-500 mb-2">Quantity</label>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                step="0.001"
                className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
              />
            </div>

            {/* SL/TP */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-500 mb-2">Stop Loss (Optional)</label>
                <input
                  type="number"
                  value={stopLoss}
                  onChange={(e) => setStopLoss(e.target.value)}
                  placeholder="0.00"
                  className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-500 mb-2">Take Profit (Optional)</label>
                <input
                  type="number"
                  value={takeProfit}
                  onChange={(e) => setTakeProfit(e.target.value)}
                  placeholder="0.00"
                  className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
            </div>

            {/* Execute Button */}
            <button
              onClick={handleExecute}
              disabled={executing || !quantity}
              className={cn(
                "w-full flex items-center justify-center gap-2 rounded-xl py-4 font-semibold transition-all",
                executing
                  ? "bg-gray-700 text-gray-400 cursor-not-allowed"
                  : direction === TradeDirection.BUY
                  ? "bg-emerald-500 text-white hover:bg-emerald-600"
                  : "bg-red-500 text-white hover:bg-red-600"
              )}
            >
              {executing ? (
                <>
                  <RefreshCw className="h-5 w-5 animate-spin" />
                  Executing...
                </>
              ) : (
                <>
                  <Play className="h-5 w-5" />
                  Execute {direction.toUpperCase()}
                </>
              )}
            </button>

            {/* Result */}
            {result && (
              <div
                className={cn(
                  "rounded-lg p-4 text-sm",
                  result.success
                    ? "bg-emerald-500/10 text-emerald-400"
                    : "bg-red-500/10 text-red-400"
                )}
              >
                {result.message}
              </div>
            )}
          </div>
        </div>

        {/* Sidebar - Quick Info */}
        <div className="space-y-6">
          {/* AI Suggestion */}
          <div className="rounded-2xl bg-gradient-to-br from-emerald-500/10 to-cyan-500/10 border border-emerald-500/20 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Zap className="h-5 w-5 text-emerald-400" />
              <h3 className="font-semibold text-white">AI Suggestion</h3>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Direction</span>
                <span className="text-emerald-400 font-medium">BUY</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Confidence</span>
                <span className="text-white font-medium">78%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Entry Zone</span>
                <span className="text-white font-medium">$67,200 - $67,500</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Risk/Reward</span>
                <span className="text-white font-medium">1:2.5</span>
              </div>
            </div>
            <button className="mt-4 w-full rounded-lg bg-emerald-500/20 py-2 text-sm text-emerald-400 hover:bg-emerald-500/30">
              Apply Suggestion
            </button>
          </div>

          {/* Risk Calculator */}
          <div className="rounded-2xl bg-gray-900/50 border border-gray-800 p-6">
            <h3 className="font-semibold text-white mb-4">Risk Calculator</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Position Size</span>
                <span className="text-white">${(parseFloat(quantity) * (currentTicker?.price || 0)).toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Risk per Trade</span>
                <span className="text-red-400">$150 (1.5%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Max Loss (SL)</span>
                <span className="text-red-400">
                  ${((parseFloat(quantity) * ((currentTicker?.price || 0) - (parseFloat(stopLoss) || 0))).toFixed(2))}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
