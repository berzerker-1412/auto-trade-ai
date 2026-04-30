"use client";

import { useEffect, useState } from "react";
import { formatCurrency } from "@/lib/utils";

// อัตราแลกเปลี่ยนเริ่มต้น (fallback ถ้า API ไม่ได้)
const DEFAULT_RATES = {
  USD_THB: 35.50,       // 1 USD = 35.50 THB
  EUR_THB: 38.20,        // 1 EUR = 38.20 THB
  GBP_THB: 44.50,        // 1 GBP = 44.50 THB
  JPY_THB: 0.235,        // 1 JPY = 0.235 THB
  lastUpdated: null as string | null,
};

export interface ExchangeRates {
  USD_THB: number;
  EUR_THB: number;
  GBP_THB: number;
  JPY_THB: number;
  lastUpdated: string | null;
}

export function useExchangeRates() {
  const [rates, setRates] = useState<ExchangeRates>(DEFAULT_RATES);
  const [loading, setLoading] = useState(false);

  // ดึงอัตราแลกเปลี่ยนจาก API หรือ cache
  useEffect(() => {
    async function fetchRates() {
      setLoading(true);
      try {
        // ลองดึงจาก backend API
        const res = await fetch("/api/exchange-rates");
        if (res.ok) {
          const data = await res.json();
          setRates({
            USD_THB: data["USD/THB"] ?? 35.50,
            EUR_THB: data["EUR/THB"] ?? 38.20,
            GBP_THB: data["GBP/THB"] ?? 44.50,
            JPY_THB: data["JPY/THB"] ?? 0.235,
            lastUpdated: data.lastUpdated,
          });
        }
      } catch {
        // ใช้ fallback
      } finally {
        setLoading(false);
      }
    }

    fetchRates();
    // อัปเดตทุก 1 ชั่วโมง
    const interval = setInterval(fetchRates, 3600000);
    return () => clearInterval(interval);
  }, []);

  // แปลง USD → THB
  const toTHB = (usdAmount: number): number => {
    return usdAmount * rates.USD_THB;
  };

  // แปลง THB → USD
  const toUSD = (thbAmount: number): number => {
    return thbAmount / rates.USD_THB;
  };

  return { rates, loading, toTHB, toUSD };
}

// ─────────────────────────────────────────────────────────
// THB Balance Display Component
// ─────────────────────────────────────────────────────────
interface THBBalanceProps {
  usdAmount: number;
  className?: string;
}

export function THBBalance({ usdAmount, className }: THBBalanceProps) {
  const { rates, loading } = useExchangeRates();
  const thbAmount = usdAmount * rates.USD_THB;

  return (
    <span className={className}>
      {formatCurrency(thbAmount, "THB")}
      {!loading && (
        <span className="text-xs text-gray-500 ml-1">
          (~${formatCurrency(usdAmount)})
        </span>
      )}
    </span>
  );
}

// ─────────────────────────────────────────────────────────
// Exchange Rate Ticker Component
// ─────────────────────────────────────────────────────────
export function ExchangeRateTicker() {
  const { rates, loading, toTHB } = useExchangeRates();
  const [time, setTime] = useState(new Date());

  // อัปเดตเวลาทุกวินาที
  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  const pairs = [
    { from: "USD", to: "THB", value: rates.USD_THB, flag: "🇺🇸🇹🇭" },
    { from: "EUR", to: "THB", value: rates.EUR_THB, flag: "🇪🇺🇹🇭" },
    { from: "GBP", to: "THB", value: rates.GBP_THB, flag: "🇬🇧🇹🇭" },
    { from: "JPY", to: "THB", value: rates.JPY_THB, flag: "🇯🇵🇹🇭", decimals: 4 },
  ];

  return (
    <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-white flex items-center gap-2">
          💱 อัตราแลกเปลี่ยน (THB)
        </h3>
        <div className="flex items-center gap-2 text-xs text-gray-500">
          {loading ? (
            <span className="animate-pulse">กำลังโหลด...</span>
          ) : (
            <>
              <span>อัปเดต {time.toLocaleTimeString("th-TH")}</span>
              <span className="text-emerald-400">● LIVE</span>
            </>
          )}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        {pairs.map((pair) => (
          <div
            key={`${pair.from}/${pair.to}`}
            className="flex items-center justify-between px-3 py-2 rounded-lg bg-gray-800/50 hover:bg-gray-800 transition-colors"
          >
            <span className="text-xs text-gray-400 font-medium">
              {pair.from}/{pair.to}
            </span>
            <span className="text-sm font-bold text-white">
              {pair.value.toFixed(pair.decimals ?? 2)}
            </span>
          </div>
        ))}
      </div>

      {/* Quick converter */}
      <div className="mt-3 pt-3 border-t border-gray-800">
        <div className="flex items-center gap-2 text-xs">
          <span className="text-gray-500">1 USD =</span>
          <span className="text-emerald-400 font-bold text-sm">
            {rates.USD_THB.toFixed(4)} THB
          </span>
          <span className="text-gray-600">|</span>
          <span className="text-gray-500">1 THB =</span>
          <span className="text-amber-400 font-bold text-sm">
            {(1 / rates.USD_THB).toFixed(4)} USD
          </span>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────
// THB Stats Component (แสดง THB ใน Dashboard/Stats)
// ─────────────────────────────────────────────────────────
interface THBStatsCardProps {
  title: string;
  usdValue: number;
  icon: React.ReactNode;
  subValue?: string;
}

export function THBStatsCard({ title, usdValue, icon, subValue }: THBStatsCardProps) {
  const { rates } = useExchangeRates();
  const thbValue = usdValue * rates.USD_THB;

  return (
    <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
      <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
        {icon}
        {title}
      </div>
      <div className="text-2xl font-bold text-white">
        {formatCurrency(thbValue, "THB")}
      </div>
      {subValue && (
        <div className="text-sm text-emerald-400 mt-0.5">
          ~${formatCurrency(usdValue)}
        </div>
      )}
    </div>
  );
}
