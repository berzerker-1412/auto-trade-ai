"use client";

import { useEffect, useRef, useState } from "react";
import { cn, formatCurrency } from "@/lib/utils";
import { Ticker } from "@/types";
import { TrendingUp, TrendingDown } from "lucide-react";

interface TickerCardProps {
  ticker: Ticker;
  onClick?: () => void;
}

export function TickerCard({ ticker, onClick }: TickerCardProps) {
  const [flashClass, setFlashClass] = useState("");
  const prevPriceRef = useRef<number | null>(null);
  const isCrypto = ticker.symbol !== "XAUUSD";
  const priceChange = ticker.high - ticker.low;
  const priceChangePercent = ((priceChange / ticker.low) * 100).toFixed(2);
  const isPositive = parseFloat(priceChangePercent) >= 0;

  // กระพริบเมื่อราคาเปลี่ยน
  useEffect(() => {
    if (prevPriceRef.current === null) {
      prevPriceRef.current = ticker.price;
      return;
    }
    if (ticker.price > prevPriceRef.current) {
      setFlashClass("ring-1 ring-emerald-500/40");
      setTimeout(() => setFlashClass(""), 600);
    } else if (ticker.price < prevPriceRef.current) {
      setFlashClass("ring-1 ring-red-500/40");
      setTimeout(() => setFlashClass(""), 600);
    }
    prevPriceRef.current = ticker.price;
  }, [ticker.price]);

  return (
    <div
      onClick={onClick}
      className={cn(
        "rounded-xl bg-gray-900/50 backdrop-blur-xl border border-gray-800 p-4 cursor-pointer hover:border-emerald-500/50 transition-all",
        onClick && "cursor-pointer",
        flashClass
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
          <p className="text-sm font-medium text-white">{formatCurrency(ticker.high)}</p>
        </div>
        <div>
          <p className="text-xs text-gray-500">24h Low</p>
          <p className="text-sm font-medium text-white">{formatCurrency(ticker.low)}</p>
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
