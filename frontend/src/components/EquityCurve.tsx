"use client";

import { useMemo } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import { formatCurrency } from "@/lib/utils";

interface EquityCurveProps {
  data: { date: string; equity: number; pnl: number }[];
  initialBalance: number;
}

export function EquityCurve({ data, initialBalance }: EquityCurveProps) {
  const chartData = useMemo(() => {
    return data.map((d) => ({
      ...d,
      dateLabel: new Date(d.date).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      }),
    }));
  }, [data]);

  const minValue = Math.min(...data.map((d) => d.equity));
  const maxValue = Math.max(...data.map((d) => d.equity));
  const yMin = Math.floor((minValue - initialBalance * 0.05) / 1000) * 1000;
  const yMax = Math.ceil((maxValue + initialBalance * 0.05) / 1000) * 1000;

  return (
    <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-white">Equity Curve</h3>
          <p className="text-sm text-gray-500">Portfolio value over time</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-gray-500">Current</p>
          <p className="text-xl font-bold text-white">
            ${formatCurrency(data[data.length - 1]?.equity || 0)}
          </p>
        </div>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="equityGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity={0.3} />
                <stop offset="50%" stopColor="#10b981" stopOpacity={0.1} />
                <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="pnlGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity={0.5} />
                <stop offset="100%" stopColor="#ef4444" stopOpacity={0.5} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis
              dataKey="dateLabel"
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={{ stroke: "#374151" }}
            />
            <YAxis
              stroke="#6b7280"
              fontSize={12}
              tickLine={false}
              axisLine={{ stroke: "#374151" }}
              domain={[yMin, yMax]}
              tickFormatter={(value) => `$${(value / 1000).toFixed(0)}k`}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: "#1f2937",
                border: "1px solid #374151",
                borderRadius: "8px",
                color: "#f9fafb",
              }}
              labelStyle={{ color: "#9ca3af" }}
              formatter={(value) => [
                `$${formatCurrency(Number(value))}`,
                "Value",
              ]}
            />
            <ReferenceLine
              y={initialBalance}
              stroke="#6b7280"
              strokeDasharray="5 5"
              label={{
                value: "Initial",
                position: "insideTopRight",
                fill: "#6b7280",
                fontSize: 10,
              }}
            />
            <Area
              type="monotone"
              dataKey="equity"
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#equityGradient)"
            />
            <Area
              type="monotone"
              dataKey="pnl"
              stroke="#fbbf24"
              strokeWidth={1}
              fill="url(#pnlGradient)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="flex items-center justify-center gap-6 mt-4 text-xs text-gray-500">
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-emerald-500" />
          <span>Equity</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-yellow-500" />
          <span>P&L</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-0.5 bg-gray-600 border-dashed" style={{ borderBottom: "1px dashed" }} />
          <span>Initial Balance</span>
        </div>
      </div>
    </div>
  );
}
