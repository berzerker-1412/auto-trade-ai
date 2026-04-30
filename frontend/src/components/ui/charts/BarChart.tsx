"use client";

import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { cn } from "@/lib/utils";

interface BarChartProps {
  data: { range: string; count: number; color: string }[];
  height?: number;
  title?: string;
  subtitle?: string;
  className?: string;
}

export function BarChart({ data, height = 192, title, subtitle, className }: BarChartProps) {
  return (
    <div className={cn("rounded-xl bg-gray-900/50 border border-gray-800 p-6", className)}>
      {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
      {subtitle && <p className="text-sm text-gray-500 mb-4">{subtitle}</p>}

      <div style={{ height }}>
        <ResponsiveContainer width="100%" height="100%">
          <RechartsBarChart data={data} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
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
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </RechartsBarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
