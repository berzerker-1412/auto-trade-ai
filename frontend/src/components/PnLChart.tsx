"use client";

import { useMemo } from "react";
import { BarChart } from "./ui/charts/BarChart";
import { PieChart } from "./ui/charts/PieChart";
import { Card, CardHeader, CardTitle } from "./ui/layout";
import { formatCurrency } from "@/lib/utils";

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
      <BarChart
        data={distribution}
        height={192}
        title="P&L Distribution"
        subtitle="Returns by percentage range"
      />

      <Card className="p-6">
        <CardHeader>
          <CardTitle subtitle="Trade outcomes breakdown">Win Rate</CardTitle>
        </CardHeader>
        <div className="flex items-center gap-4">
          <div style={{ width: 160, height: 160 }}>
            <PieChart
              data={pieData}
              height={160}
              innerRadius={45}
              outerRadius={70}
              showLegend={false}
            />
          </div>

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
              <span className="text-emerald-400 font-medium">{formatCurrency(avgWin)}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-500">Avg Loss</span>
              <span className="text-red-400 font-medium">{formatCurrency(avgLoss)}</span>
            </div>
            {avgLoss !== 0 && (
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Avg Win/Loss</span>
                <span className="text-white font-medium">{(avgWin / Math.abs(avgLoss)).toFixed(2)}x</span>
              </div>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}
