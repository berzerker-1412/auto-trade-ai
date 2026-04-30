"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { Ticker } from "@/types";
import { LiveTickerCard } from "@/components/LiveTickerCard";
import { api } from "@/lib/api";

// รายการ asset ทั้งหมด
const ASSETS = [
  { symbol: "BTC/USDT", name: "Bitcoin", color: "#F7931A" },
  { symbol: "ETH/USDT", name: "Ethereum", color: "#627EEA" },
  { symbol: "SOL/USDT", name: "Solana", color: "#00FFA3" },
  { symbol: "XAUUSD", name: "Gold (XAU/USD)", color: "#FFD700" },
];

export default function LivePage() {
  const [tickers, setTickers] = useState<Record<string, Ticker>>({});
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [connected, setConnected] = useState(false);

  // โหลดข้อมูลเริ่มต้น
  const loadTickers = useCallback(async () => {
    try {
      const data = await api.getTickers();
      setTickers(data);
      setLastUpdate(new Date());
      setConnected(true);
      } catch (error) {
      console.error("Failed to load tickers:", error);
    }
  }, []);

  useEffect(() => {
    loadTickers();

    // อัปเดตทุก 5 วินาที (polling)
    const interval = setInterval(loadTickers, 5000);
    return () => clearInterval(interval);
  }, [loadTickers]);

  // สร้าง mock price simulation สำหรับ demo
  const [simulatedTickers, setSimulatedTickers] = useState<Record<string, Ticker>>({});

  useEffect(() => {
    // เริ่มต้น simulated tickers จาก mock data
    const initial: Record<string, Ticker> = {
      "BTC/USDT": { symbol: "BTC/USDT", price: 68250, bid: 68240, ask: 68260, high: 68800, low: 67800, volume: 25000 },
      "ETH/USDT": { symbol: "ETH/USDT", price: 3480, bid: 3478, ask: 3482, high: 3520, low: 3430, volume: 180000 },
      "SOL/USDT": { symbol: "SOL/USDT", price: 96, bid: 95.8, ask: 96.2, high: 99, low: 94, volume: 500000 },
      "XAUUSD": { symbol: "XAUUSD", price: 2035, bid: 2034.5, ask: 2035.5, high: 2040, low: 2020, volume: 0 },
    };
    setSimulatedTickers(initial);

    // อัปเดตราคาแบบสุ่มทุก 2 วินาที
    const priceInterval = setInterval(() => {
      setSimulatedTickers(prev => {
        const next = { ...prev };
        for (const symbol of Object.keys(next)) {
          const t = next[symbol];
          const volatility = t.price * (symbol === "XAUUSD" ? 0.0003 : 0.001);
          const change = (Math.random() - 0.48) * volatility;
          const newPrice = Math.max(t.price + change, 0.01);
          const spread = newPrice * 0.0002;

          next[symbol] = {
            ...t,
            price: newPrice,
            bid: newPrice - spread,
            ask: newPrice + spread,
            high: Math.max(t.high, newPrice),
            low: Math.min(t.low, newPrice),
          };
        }
        return next;
      });
      setLastUpdate(new Date());
    }, 2000);

    return () => clearInterval(priceInterval);
  }, []);

  // ใช้ simulated tickers ถ้ามี ถ้าไม่มีใช้จาก API
  const displayTickers = Object.keys(simulatedTickers).length > 0 ? simulatedTickers : tickers;

  return (
    <div className="p-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500" />
            </span>
            Live Market
          </h1>
          <p className="mt-1 text-gray-500">
            Real-time prices · Updated {lastUpdate.toLocaleTimeString()}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-2 h-2 rounded-full ${connected ? "bg-emerald-500" : "bg-red-500"}`} />
          <span className="text-xs text-gray-500">{connected ? "Connected" : "Disconnected"}</span>
        </div>
      </div>

      {/* Asset Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {ASSETS.map((asset) => {
          const ticker = displayTickers[asset.symbol];
          return (
            <Link key={asset.symbol} href={`/live/${encodeURIComponent(asset.symbol)}`}>
              <LiveTickerCard
                symbol={asset.symbol}
                name={asset.name}
                color={asset.color}
                ticker={ticker}
              />
            </Link>
          );
        })}
      </div>

      {/* Quick Info Bar */}
      <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-6">
            <span className="text-gray-500">Data Source:</span>
            <span className="text-white font-medium">Binance (Simulated)</span>
          </div>
          <div className="flex items-center gap-6">
            <span className="text-gray-500">Update Interval:</span>
            <span className="text-emerald-400 font-medium">2s</span>
          </div>
          <div className="flex items-center gap-6">
            <span className="text-gray-500">Total Assets:</span>
            <span className="text-white font-medium">4</span>
          </div>
          <Link
            href="/analysis"
            className="text-emerald-400 hover:text-emerald-300 transition-colors font-medium"
          >
            View Analysis →
          </Link>
        </div>
      </div>
    </div>
  );
}
