"use client";

import { AreaChart as AreaChartWrapper } from "./ui/charts/AreaChart";

interface EquityCurveProps {
  data: { date: string; equity: number; pnl: number }[];
  initialBalance: number;
}

export function EquityCurve({ data, initialBalance }: EquityCurveProps) {
  return <AreaChartWrapper data={data} initialBalance={initialBalance} />;
}
