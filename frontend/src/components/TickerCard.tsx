"use client";

import { cn, formatCurrency, formatNumber } from "@/lib/utils";
import { Ticker } from "@/types";
import { TrendingUp, TrendingDown } from "lucide-react";

interface TickerCardProps {
  ticker: Ticker;
  onClick?: () => void;
}

export function TickerCard({ ticker, onClick }: TickerCardProps) {
  const isCrypto = ticker.symbol !== "XAUUSD";
  const priceChange = ticker.high - ticker.low;
  const priceChangePercent = ((priceChange / ticker.low) * 100).toFixed(2);
  const isPositive = Math.random() > 0.3; // Mock for demo

  return (
    <div
      onClick={onClick}
      className={cn(
        "rounded-xl bg-gray-900/50 backdrop-blur-xl border border-gray-800 p-4 cursor-pointer hover:border-emerald-500/50 transition-all",
        onClick && "cursor-pointer"
      )}
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-500">{ticker.symbol}</p>
          <p className="mt-1 text-xl font-bold text-white">
            {isCrypto ? "$" : ""}{formatCurrency(ticker.price, isCrypto ? "USD" : "XAU")}
          </p>
        </div>
        <div
          className={cn(
            "flex items-center gap-1 rounded-lg px-2 py-1 text-xs font-medium",
            isPositive ? "bg-emerald-500/10 text-emerald-400" : "bg-red-500/10 text-red-400"
          )}
        >
          {isPositive ? (
            <TrendingUp className="h-3 w-3" />
          ) : (
            <TrendingDown className="h-3 w-3" />
          )}
          {priceChangePercent}%
        </div>
      </div>
      <div className="mt-4 grid grid-cols-3 gap-4">
        <div>
          <p className="text-xs text-gray-500">24h High</p>
          <p className="text-sm font-medium text-white">${formatCurrency(ticker.high)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">24h Low</p>
          <p className="text-sm font-medium text-white">${formatCurrency(ticker.low)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">Volume</p>
          <p className="text-sm font-medium text-white">
            {ticker.volume > 1000 ? `${(ticker.volume / 1000).toFixed(0)}K` : ticker.volume}
          </p>
        </div>
      </div>
    </div>
  );
}
