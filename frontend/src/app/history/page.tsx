"use client";

import { useEffect, useState } from "react";
import { TradeTable } from "@/components/TradeTable";
import { api } from "@/lib/api";
import { Trade } from "@/types";
import { Filter, Download } from "lucide-react";

export default function HistoryPage() {
  const [trades, setTrades] = useState<Trade[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<"all" | "open" | "closed">("all");

  useEffect(() => {
    async function loadTrades() {
      try {
        const data = await api.getTrades(100);
        setTrades(data);
      } catch (error) {
        console.error("Failed to load trades:", error);
      } finally {
        setLoading(false);
      }
    }
    loadTrades();
  }, []);

  const filteredTrades = trades.filter((trade) => {
    if (filter === "all") return true;
    return trade.status === filter;
  });

  const stats = {
    total: trades.length,
    open: trades.filter((t) => t.status === "open").length,
    closed: trades.filter((t) => t.status === "closed").length,
    totalPnl: trades.reduce((sum, t) => sum + (t.pnl || 0), 0),
    winningTrades: trades.filter((t) => t.status === "closed" && (t.pnl || 0) > 0).length,
    losingTrades: trades.filter((t) => t.status === "closed" && (t.pnl || 0) < 0).length,
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
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Trade History</h1>
          <p className="mt-1 text-gray-500">Complete record of all your trades</p>
        </div>
        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 rounded-lg bg-gray-800 px-4 py-2 text-sm text-gray-300 hover:bg-gray-700">
            <Download className="h-4 w-4" />
            Export CSV
          </button>
        </div>
      </div>

      {/* Stats Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <p className="text-xs text-gray-500">Total Trades</p>
          <p className="mt-1 text-2xl font-bold text-white">{stats.total}</p>
        </div>
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <p className="text-xs text-gray-500">Open Positions</p>
          <p className="mt-1 text-2xl font-bold text-blue-400">{stats.open}</p>
        </div>
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <p className="text-xs text-gray-500">Closed Trades</p>
          <p className="mt-1 text-2xl font-bold text-emerald-400">{stats.closed}</p>
        </div>
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <p className="text-xs text-gray-500">Total P&L</p>
          <p className={`mt-1 text-2xl font-bold ${stats.totalPnl >= 0 ? "text-emerald-400" : "text-red-400"}`}>
            ${stats.totalPnl.toLocaleString()}
          </p>
        </div>
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <p className="text-xs text-gray-500">Winning</p>
          <p className="mt-1 text-2xl font-bold text-emerald-400">{stats.winningTrades}</p>
        </div>
        <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
          <p className="text-xs text-gray-500">Losing</p>
          <p className="mt-1 text-2xl font-bold text-red-400">{stats.losingTrades}</p>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center gap-2">
        <Filter className="h-4 w-4 text-gray-500" />
        <div className="flex gap-2">
          {(["all", "open", "closed"] as const).map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`rounded-lg px-4 py-2 text-sm font-medium transition-colors ${
                filter === f
                  ? "bg-emerald-500/10 text-emerald-400"
                  : "text-gray-400 hover:bg-gray-800"
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
              {f === "all" && ` (${stats.total})`}
              {f === "open" && ` (${stats.open})`}
              {f === "closed" && ` (${stats.closed})`}
            </button>
          ))}
        </div>
      </div>

      {/* Trade Table */}
      <TradeTable trades={filteredTrades} />
    </div>
  );
}
