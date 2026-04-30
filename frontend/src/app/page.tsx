"use client";

import { useEffect, useState } from "react";
import {
  Wallet,
  TrendingUp,
  Target,
  Award,
  Activity,
} from "lucide-react";
import { StatCard } from "@/components/StatCard";
import { TradeTable } from "@/components/TradeTable";
import { TickerCard } from "@/components/TickerCard";
import { ExchangeRateTicker, THBStatsCard } from "@/components/ExchangeRate";
import TraderControl from "@/components/TraderControl";
import { api } from "@/lib/api";
import { Trade, Ticker } from "@/types";

export default function DashboardPage() {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [tickers, setTickers] = useState<Record<string, Ticker>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [tradesData, tickersData] = await Promise.all([
          api.getTrades(10),
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
    const interval = setInterval(loadData, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const stats = {
    balance: 105000,
    totalPnl: 5000,
    winRate: 64,
    totalTrades: 25,
    activeTrades: trades.filter((t) => t.status === "open").length,
  };

  const openTrades = trades.filter((t) => t.status === "open");
  const recentTrades = trades.slice(0, 5);

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
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="mt-1 text-gray-500">Overview of your paper trading performance</p>
      </div>

      {/* Auto Trader Control */}
      <div className="max-w-md">
        <TraderControl />
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Total Balance"
          value={stats.balance}
          subValue="Paper Trading Mode"
          icon={Wallet}
        />
        <StatCard
          title="Total P&L"
          value={stats.totalPnl}
          subValue="+$5,000 (5.0%)"
          icon={TrendingUp}
          trend={5}
        />
        <StatCard
          title="Win Rate"
          value={`${stats.winRate}%`}
          subValue="16W / 9L"
          icon={Target}
        />
        <StatCard
          title="Total Trades"
          value={stats.totalTrades}
          subValue={`${stats.activeTrades} active`}
          icon={Award}
        />
      </div>

      {/* THB Exchange Rate */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <h2 className="text-xl font-semibold text-white mb-4">💱 อัตราแลกเปลี่ยน (THB)</h2>
          <ExchangeRateTicker />
        </div>
        <div className="space-y-4">
          <THBStatsCard
            title="Balance (THB)"
            usdValue={stats.balance}
            icon={<Wallet className="h-3.5 w-3.5" />}
            subValue="≈ $105,000"
          />
          <THBStatsCard
            title="Total P&L (THB)"
            usdValue={stats.totalPnl}
            icon={<TrendingUp className="h-3.5 w-3.5" />}
            subValue="+$5,000"
          />
        </div>
      </div>

      {/* Market Tickers */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Market Prices</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.values(tickers).map((ticker) => (
            <TickerCard key={ticker.symbol} ticker={ticker} />
          ))}
        </div>
      </div>

      {/* Open Positions */}
      {openTrades.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-white mb-4">Open Positions</h2>
          <TradeTable trades={openTrades} />
        </div>
      )}

      {/* Recent Trades */}
      <div>
        <h2 className="text-xl font-semibold text-white mb-4">Recent Trades</h2>
        <TradeTable trades={recentTrades} limit={5} />
      </div>

      {/* Quick Actions */}
      <div className="flex gap-4">
        <a
          href="/trade"
          className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-emerald-500 to-cyan-500 px-6 py-3 font-semibold text-white hover:opacity-90 transition-opacity"
        >
          <Activity className="h-5 w-5" />
          New Paper Trade
        </a>
      </div>
    </div>
  );
}
