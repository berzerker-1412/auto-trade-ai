"use client";

import { useEffect, useState, useMemo } from "react";
import { api } from "@/lib/api";
import { Trade, Ticker } from "@/types";
import { PriceChart } from "@/components/PriceChart";
import { EquityCurve } from "@/components/EquityCurve";
import { PnLDistribution } from "@/components/PnLChart";
import { formatCurrency, formatPercent, formatDate } from "@/lib/utils";
import {
  TrendingUp,
  TrendingDown,
  Calendar,
  BarChart3,
  ArrowUpRight,
  ArrowDownRight,
} from "lucide-react";

export default function AnalysisPage() {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [tickers, setTickers] = useState<Record<string, Ticker>>({});
  const [selectedSymbol, setSelectedSymbol] = useState("BTC/USDT");
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState<"1W" | "1M" | "3M" | "ALL">("3M");

  useEffect(() => {
    async function loadData() {
      try {
        const [tradesData, tickersData] = await Promise.all([
          api.getTrades(100),
          api.getTickers(),
        ]);
        setTrades(tradesData);
        setTickers(tickersData);
      } catch (error) {
        console.error("Failed to load data:", error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // Generate equity curve data
  const equityData = useMemo(() => {
    const closedTrades = trades
      .filter((t) => t.status === "closed" && t.exit_time)
      .sort((a, b) => new Date(a.exit_time!).getTime() - new Date(b.exit_time!).getTime());

    let equity = 100000; // initial balance
    const data: { date: string; equity: number; pnl: number }[] = [
      { date: new Date().toISOString(), equity, pnl: 0 },
    ];

    closedTrades.forEach((trade) => {
      if (trade.pnl) {
        equity += trade.pnl;
        data.push({
          date: trade.exit_time!,
          equity,
          pnl: trade.pnl,
        });
      }
    });

    return data;
  }, [trades]);

  // Monthly stats
  const monthlyStats = useMemo(() => {
    const now = new Date();
    const thisMonth = trades.filter((t) => {
      if (!t.exit_time) return false;
      const d = new Date(t.exit_time);
      return d.getMonth() === now.getMonth() && d.getFullYear() === now.getFullYear();
    });

    const wins = thisMonth.filter((t) => (t.pnl || 0) > 0);
    const losses = thisMonth.filter((t) => (t.pnl || 0) < 0);
    const totalPnl = thisMonth.reduce((sum, t) => sum + (t.pnl || 0), 0);

    return {
      totalTrades: thisMonth.length,
      wins: wins.length,
      losses: losses.length,
      totalPnl,
      winRate: thisMonth.length > 0 ? (wins.length / thisMonth.length) * 100 : 0,
    };
  }, [trades]);

  // Best/worst trades
  const bestTrade = useMemo(() => {
    return trades
      .filter((t) => t.pnl !== null)
      .sort((a, b) => (b.pnl || 0) - (a.pnl || 0))[0];
  }, [trades]);

  const worstTrade = useMemo(() => {
    return trades
      .filter((t) => t.pnl !== null)
      .sort((a, b) => (a.pnl || 0) - (b.pnl || 0))[0];
  }, [trades]);

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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Analysis</h1>
          <p className="mt-1 text-gray-500">Charts, performance metrics & technical analysis</p>
        </div>

        {/* Time Range Filter */}
        <div className="flex items-center gap-2">
          {(["1W", "1M", "3M", "ALL"] as const).map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${
                timeRange === range
                  ? "bg-emerald-500/10 text-emerald-400"
                  : "text-gray-400 hover:bg-gray-800"
              }`}
            >
              {range}
            </button>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
            <Calendar className="h-4 w-4" />
            This Month
          </div>
          <p className="text-2xl font-bold text-white">{monthlyStats.totalTrades}</p>
          <p className="text-sm text-gray-500">trades</p>
        </div>

        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
            <BarChart3 className="h-4 w-4" />
            Win Rate
          </div>
          <p className="text-2xl font-bold text-white">{monthlyStats.winRate.toFixed(0)}%</p>
          <p className="text-sm text-gray-500">
            {monthlyStats.wins}W / {monthlyStats.losses}L
          </p>
        </div>

        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
            {monthlyStats.totalPnl >= 0 ? (
              <TrendingUp className="h-4 w-4 text-emerald-400" />
            ) : (
              <TrendingDown className="h-4 w-4 text-red-400" />
            )}
            Monthly P&L
          </div>
          <p
            className={`text-2xl font-bold ${
              monthlyStats.totalPnl >= 0 ? "text-emerald-400" : "text-red-400"
            }`}
          >
            {monthlyStats.totalPnl >= 0 ? "+" : ""}{formatCurrency(monthlyStats.totalPnl)}
          </p>
        </div>

        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <div className="flex items-center gap-2 text-sm text-gray-500 mb-1">
            <ArrowUpRight className="h-4 w-4 text-emerald-400" />
            Best Trade
          </div>
          <p className="text-2xl font-bold text-emerald-400">
            +{formatCurrency(bestTrade?.pnl || 0)}
          </p>
          <p className="text-sm text-gray-500">{bestTrade?.symbol}</p>
        </div>
      </div>

      {/* Best/Worst Trade Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Best Trade */}
        <div className="rounded-xl bg-gradient-to-br from-emerald-500/10 to-emerald-900/10 border border-emerald-500/20 p-6">
          <div className="flex items-center gap-2 mb-4">
            <ArrowUpRight className="h-5 w-5 text-emerald-400" />
            <span className="text-sm text-emerald-400 font-medium">Best Trade</span>
          </div>
          {bestTrade && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-white font-semibold">{bestTrade.symbol}</span>
                <span className="text-2xl font-bold text-emerald-400">
                  +{formatCurrency(bestTrade.pnl || 0)}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">Entry</p>
                  <p className="text-white">{formatCurrency(bestTrade.entry_price)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Exit</p>
                  <p className="text-white">{formatCurrency(bestTrade.exit_price || 0)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Return</p>
                  <p className="text-emerald-400">
                    {formatPercent(bestTrade.pnl_percent || 0)}
                  </p>
                </div>
              </div>
              <p className="text-xs text-gray-500">{formatDate(bestTrade.exit_time)}</p>
            </div>
          )}
        </div>

        {/* Worst Trade */}
        <div className="rounded-xl bg-gradient-to-br from-red-500/10 to-red-900/10 border border-red-500/20 p-6">
          <div className="flex items-center gap-2 mb-4">
            <ArrowDownRight className="h-5 w-5 text-red-400" />
            <span className="text-sm text-red-400 font-medium">Worst Trade</span>
          </div>
          {worstTrade && (
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-white font-semibold">{worstTrade.symbol}</span>
                <span className="text-2xl font-bold text-red-400">
                  {formatCurrency(worstTrade.pnl || 0)}
                </span>
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div>
                  <p className="text-gray-500">Entry</p>
                  <p className="text-white">{formatCurrency(worstTrade.entry_price)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Exit</p>
                  <p className="text-white">{formatCurrency(worstTrade.exit_price || 0)}</p>
                </div>
                <div>
                  <p className="text-gray-500">Return</p>
                  <p className="text-red-400">
                    {formatPercent(worstTrade.pnl_percent || 0)}
                  </p>
                </div>
              </div>
              <p className="text-xs text-gray-500">{formatDate(worstTrade.exit_time)}</p>
            </div>
          )}
        </div>
      </div>

      {/* Equity Curve */}
      <EquityCurve data={equityData} initialBalance={100000} />

      {/* P&L Distribution */}
      <PnLDistribution trades={trades} />

      {/* Price Chart with Drawing Tools */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white">Technical Analysis</h2>
          <div className="flex gap-2">
            {["BTC/USDT", "ETH/USDT", "SOL/USDT", "XAUUSD"].map((symbol) => (
              <button
                key={symbol}
                onClick={() => setSelectedSymbol(symbol)}
                className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                  selectedSymbol === symbol
                    ? "bg-emerald-500 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                }`}
              >
                {symbol}
              </button>
            ))}
          </div>
        </div>
        <PriceChart symbol={selectedSymbol} />
      </div>
    </div>
  );
}
