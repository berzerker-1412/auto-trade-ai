"use client";

import { useMemo } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
} from "recharts";
import { formatCurrency, formatPercent } from "@/lib/utils";

interface PnLChartProps {
  trades: {
    id: number;
    pnl?: number | null;
    pnl_percent?: number | null;
    entry_time: string | null;
  }[];
}

export function PnLDistribution({ trades }: PnLChartProps) {
  const closedTrades = trades.filter((t) => t.pnl !== null && t.pnl_percent !== null);

  const distribution = useMemo(() => {
    const bins = [
      { range: "< -5%", min: -Infinity, max: -5, count: 0 },
      { range: "-5% to -2%", min: -5, max: -2, count: 0 },
      { range: "-2% to 0%", min: -2, max: 0, count: 0 },
      { range: "0% to 2%", min: 0, max: 2, count: 0 },
      { range: "2% to 5%", min: 2, max: 5, count: 0 },
      { range: "> 5%", min: 5, max: Infinity, count: 0 },
    ];

    closedTrades.forEach((trade) => {
      const pct = trade.pnl_percent!;
      const bin = bins.find((b) => pct >= b.min && pct < b.max);
      if (bin) bin.count++;
    });

    return bins.map((b) => ({
      range: b.range,
      count: b.count,
      color: b.max <= 0 ? "#ef4444" : "#10b981",
    }));
  }, [closedTrades]);

  const pieData = useMemo(() => {
    const wins = closedTrades.filter((t) => (t.pnl || 0) > 0).length;
    const losses = closedTrades.filter((t) => (t.pnl || 0) < 0).length;
    const breakeven = closedTrades.filter((t) => (t.pnl || 0) === 0).length;
    return [
      { name: "Wins", value: wins, color: "#10b981" },
      { name: "Losses", value: losses, color: "#ef4444" },
      { name: "Breakeven", value: breakeven, color: "#6b7280" },
    ].filter((d) => d.value > 0);
  }, [closedTrades]);

  const avgWin = useMemo(() => {
    const wins = closedTrades.filter((t) => (t.pnl || 0) > 0);
    return wins.length > 0 ? wins.reduce((sum, t) => sum + (t.pnl || 0), 0) / wins.length : 0;
  }, [closedTrades]);

  const avgLoss = useMemo(() => {
    const losses = closedTrades.filter((t) => (t.pnl || 0) < 0);
    return losses.length > 0 ? losses.reduce((sum, t) => sum + (t.pnl || 0), 0) / losses.length : 0;
  }, [closedTrades]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Distribution Histogram */}
      <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-6">
        <h3 className="text-lg font-semibold text-white mb-2">P&L Distribution</h3>
        <p className="text-sm text-gray-500 mb-4">Returns by percentage range</p>

        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={distribution} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis
                dataKey="range"
                stroke="#6b7280"
                fontSize={10}
                tickLine={false}
                axisLine={{ stroke: "#374151" }}
              />
              <YAxis
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: "#374151" }}
                allowDecimals={false}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#1f2937",
                  border: "1px solid #374151",
                  borderRadius: "8px",
                  color: "#f9fafb",
                }}
                formatter={(value) => [value, "Trades"]}
              />
              <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                {distribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Win/Loss Pie + Stats */}
      <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-6">
        <h3 className="text-lg font-semibold text-white mb-2">Win Rate</h3>
        <p className="text-sm text-gray-500 mb-4">Trade outcomes breakdown</p>

        <div className="flex items-center gap-4">
          {/* Pie Chart */}
          <div className="h-40 w-40">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={45}
                  outerRadius={70}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#1f2937",
                    border: "1px solid #374151",
                    borderRadius: "8px",
                    color: "#f9fafb",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Legend & Stats */}
          <div className="flex-1 space-y-3">
            {pieData.map((entry) => (
              <div key={entry.name} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: entry.color }}
                  />
                  <span className="text-sm text-gray-400">{entry.name}</span>
                </div>
                <span className="text-sm font-medium text-white">{entry.value}</span>
              </div>
            ))}

            <div className="h-px bg-gray-800 my-2" />

            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Avg Win</span>
              <span className="text-emerald-400 font-medium">
                ${formatCurrency(avgWin)}
              </span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Avg Loss</span>
              <span className="text-red-400 font-medium">
                ${formatCurrency(avgLoss)}
              </span>
            </div>
            {avgLoss !== 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Avg Win/Loss</span>
                <span className="text-white font-medium">
                  {(avgWin / Math.abs(avgLoss)).toFixed(2)}x
                </span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
