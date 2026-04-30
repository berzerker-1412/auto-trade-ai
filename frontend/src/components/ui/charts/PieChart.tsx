"use client";

import { useMemo } from "react";
import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { cn } from "@/lib/utils";

interface PieChartProps {
  data: { name: string; value: number; color: string }[];
  innerRadius?: number;
  outerRadius?: number;
  height?: number;
  title?: string;
  subtitle?: string;
  showLegend?: boolean;
  className?: string;
}

export function PieChart({
  data,
  innerRadius = 45,
  outerRadius = 70,
  height = 160,
  title,
  subtitle,
  showLegend = true,
  className,
}: PieChartProps) {
  const filteredData = useMemo(() => data.filter((d) => d.value > 0), [data]);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const tooltipFormatter = (value: any) => [value, "Count"];

  return (
    <div className={cn("rounded-xl bg-gray-900/50 border border-gray-800 p-6", className)}>
      {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
      {subtitle && <p className="text-sm text-gray-500 mb-4">{subtitle}</p>}

      <div className="flex items-center gap-4">
        <div style={{ width: height, height }}>
          <ResponsiveContainer width="100%" height="100%">
            <RechartsPieChart>
              <Pie
                data={filteredData}
                cx="50%"
                cy="50%"
                innerRadius={innerRadius}
                outerRadius={outerRadius}
                paddingAngle={2}
                dataKey="value"
              >
                {filteredData.map((entry, index) => (
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
                formatter={tooltipFormatter}
              />
            </RechartsPieChart>
          </ResponsiveContainer>
        </div>

        {showLegend && (
          <div className="flex-1 space-y-3">
            {filteredData.map((entry) => (
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
          </div>
        )}
      </div>
    </div>
  );
}
