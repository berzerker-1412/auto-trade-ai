// Utility functions

import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatNumber(num: number, decimals = 2): string {
  return num.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

export function formatCurrency(amount: number, currency = "USD"): string {
  const isTHB = currency === "THB";
  return new Intl.NumberFormat(isTHB ? "th-TH" : "en-US", {
    style: "currency",
    currency,
    minimumFractionDigits: isTHB ? 2 : 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function formatPercent(value: number): string {
  const sign = value >= 0 ? "+" : "";
  return `${sign}${value.toFixed(2)}%`;
}

export function formatDate(date: string | null, locale = "th-TH"): string {
  if (!date) return "-";
  const d = new Date(date);
  const lang = locale === "th" ? "th-TH" : "en-US";
  const year = locale === "th" ? d.getFullYear() + 543 : d.getFullYear();
  return d.toLocaleString(lang, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    year: "numeric",
  }).replace(String(d.getFullYear()), String(year));
}

export function formatTime(date: string | null): string {
  if (!date) return "-";
  return new Date(date).toLocaleString("th-TH", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

export function formatEntryExit(reason: { summary?: string; trigger?: string; trigger_detail?: string } | null | undefined): string {
  if (!reason) return "-";
  if (reason.summary) {
    // เอาแค่บรรทัดแรกของ summary
    const firstLine = reason.summary.split("\n")[0];
    return firstLine.replace(/^[^\w]+/, "").slice(0, 60);
  }
  if (reason.trigger) {
    const triggerText: Record<string, string> = {
      stop_loss: "Stop Loss",
      take_profit: "Take Profit",
      trailing_stop: "Trailing Stop",
      regime_change: "Regime Change",
      risk_manager: "Risk Manager",
      manual: "Manual",
    };
    return `${triggerText[reason.trigger] || reason.trigger}: ${reason.trigger_detail || ""}`;
  }
  return "-";
}

export function getStatusColor(status: string): string {
  switch (status) {
    case "open":
      return "text-blue-400 bg-blue-400/10";
    case "closed":
      return "text-green-400 bg-green-400/10";
    case "pending":
      return "text-yellow-400 bg-yellow-400/10";
    case "cancelled":
      return "text-gray-400 bg-gray-400/10";
    default:
      return "text-gray-400 bg-gray-400/10";
  }
}

export function getDirectionColor(direction: string): string {
  return direction === "buy"
    ? "text-emerald-400 bg-emerald-400/10"
    : "text-red-400 bg-red-400/10";
}

export function getPnLColor(value: number | null | undefined): string {
  if (value === null || value === undefined) return "text-gray-400";
  return value >= 0 ? "text-emerald-400" : "text-red-400";
}
