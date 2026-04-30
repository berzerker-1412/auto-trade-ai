"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { cn, formatCurrency } from "@/lib/utils";
import { Ticker } from "@/types";
import { TrendingUp, TrendingDown, BarChart2, ArrowRight } from "lucide-react";

interface LiveTickerCardProps {
  symbol: string;
  name: string;
  color: string;
  ticker?: Ticker;
}

export function LiveTickerCard({ symbol, name, color, ticker }: LiveTickerCardProps) {
  const [flashClass, setFlashClass] = useState("");
  const prevPriceRef = useRef<number | null>(null);

  // กระพริบเมื่อราคาเปลี่ยน
  useEffect(() => {
    if (!ticker) return;
    if (prevPriceRef.current === null) {
      prevPriceRef.current = ticker.price;
      return;
    }

    if (ticker.price > prevPriceRef.current) {
      setFlashClass("ring-2 ring-emerald-500/50");
      setTimeout(() => setFlashClass(""), 500);
    } else if (ticker.price < prevPriceRef.current) {
      setFlashClass("ring-2 ring-red-500/50");
      setTimeout(() => setFlashClass(""), 500);
    }
    prevPriceRef.current = ticker.price;
  }, [ticker?.price]);

  const isCrypto = symbol !== "XAUUSD";
  const priceChange = ticker ? ticker.high - ticker.low : 0;
  const priceChangePercent = ticker && ticker.low > 0
    ? ((priceChange / ticker.low) * 100).toFixed(2)
    : "0.00";

  // สร้าง mini sparkline จาก random data
  const sparkline = Array.from({ length: 20 }, (_, i) =>
    50 + Math.sin(i * 0.5) * 20 + Math.random() * 10
  );

  return (
    <div
      className={cn(
        "relative rounded-xl bg-gray-900/50 backdrop-blur-xl border border-gray-800 p-5",
        "hover:border-gray-700 hover:bg-gray-900/70 transition-all duration-300",
        "cursor-pointer group",
        flashClass
      )}
    >
      {/* ขอบสีด้านบน */}
      <div
        className="absolute top-0 left-4 right-4 h-0.5 rounded-full"
        style={{ backgroundColor: color }}
      />

      <div className="flex items-start justify-between">
        {/* ซ้าย: ชื่อ + ราคา */}
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <div
              className="w-2 h-2 rounded-full animate-pulse"
              style={{ backgroundColor: color }}
            />
            <p className="text-sm font-medium text-gray-400">{name}</p>
          </div>
          <p className="text-xs text-gray-600 mt-0.5">{symbol}</p>

          <div className="mt-3">
            <p className="text-2xl font-bold text-white">
              {isCrypto ? "$" : ""}
              {ticker ? formatCurrency(ticker.price, isCrypto ? "USD" : "XAU") : "—"}
            </p>
          </div>

          {/* Bid/Ask */}
          {ticker && (
            <div className="mt-2 flex items-center gap-3 text-xs">
              <span className="text-gray-500">
                Bid: <span className="text-emerald-400 font-medium">{formatCurrency(ticker.bid, isCrypto ? "USD" : "XAU")}</span>
              </span>
              <span className="text-gray-500">
                Ask: <span className="text-red-400 font-medium">{formatCurrency(ticker.ask, isCrypto ? "USD" : "XAU")}</span>
              </span>
            </div>
          )}
        </div>

        {/* ขวา: แนวโน้ม + Mini chart */}
        <div className="flex flex-col items-end gap-2">
          {/* เปอร์เซ็นต์ */}
          <div
            className={cn(
              "flex items-center gap-1 rounded-lg px-2 py-1 text-xs font-semibold",
              parseFloat(priceChangePercent) >= 0
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-red-500/10 text-red-400"
            )}
          >
            {parseFloat(priceChangePercent) >= 0 ? (
              <TrendingUp className="h-3 w-3" />
            ) : (
              <TrendingDown className="h-3 w-3" />
            )}
            {priceChangePercent}%
          </div>

          {/* Mini Sparkline */}
          <div className="w-24 h-8">
            <svg viewBox="0 0 100 40" className="w-full h-full">
              <polyline
                fill="none"
                stroke={parseFloat(priceChangePercent) >= 0 ? "#10b981" : "#ef4444"}
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
                points={sparkline.map((v, i) => `${i * 5},${40 - v}`).join(" ")}
              />
            </svg>
          </div>

          {/* ไอคอน Analysis */}
          <div className="flex items-center gap-1 text-gray-600 group-hover:text-emerald-400 transition-colors">
            <BarChart2 className="h-3 w-3" />
            <span className="text-xs">Analysis</span>
            <ArrowRight className="h-3 w-3" />
          </div>
        </div>
      </div>

      {/* Stats Row */}
      {ticker && (
        <div className="mt-4 pt-3 border-t border-gray-800 grid grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-gray-600">24h High</p>
            <p className="text-sm font-semibold text-white mt-0.5">
              {formatCurrency(ticker.high)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600">24h Low</p>
            <p className="text-sm font-semibold text-white mt-0.5">
              {formatCurrency(ticker.low)}
            </p>
          </div>
          <div>
            <p className="text-xs text-gray-600">Volume</p>
            <p className="text-sm font-semibold text-white mt-0.5">
              {ticker.volume > 1000 ? `${(ticker.volume / 1000).toFixed(0)}K` : ticker.volume}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
