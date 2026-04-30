"use client";

import { cn, formatCurrency, formatNumber, formatPercent } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface StatCardProps {
  title: string;
  value: string | number;
  subValue?: string;
  icon: LucideIcon;
  trend?: number;
  className?: string;
}

export function StatCard({
  title,
  value,
  subValue,
  icon: Icon,
  trend,
  className,
}: StatCardProps) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl bg-gray-900/50 backdrop-blur-xl border border-gray-800 p-6",
        className
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="mt-2 text-3xl font-bold text-white">
            {typeof value === "number" ? formatNumber(value) : value}
          </p>
          {subValue && (
            <p
              className={cn(
                "mt-1 text-sm",
                trend !== undefined
                  ? trend >= 0
                    ? "text-emerald-400"
                    : "text-red-400"
                  : "text-gray-400"
              )}
            >
              {subValue}
            </p>
          )}
        </div>
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-emerald-500/20 to-cyan-500/20">
          <Icon className="h-6 w-6 text-emerald-400" />
        </div>
      </div>
    </div>
  );
}
