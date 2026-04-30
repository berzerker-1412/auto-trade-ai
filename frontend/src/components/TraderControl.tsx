"use client";

import { useEffect, useState, useCallback } from "react";
import { Play, Square, Settings2, Loader2, AlertCircle, CheckCircle2, XCircle } from "lucide-react";
import { api, TraderStatus } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";

export default function TraderControl() {
  const [status, setStatus] = useState<TraderStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showConfig, setShowConfig] = useState(false);
  const [config, setConfig] = useState({
    mode: "paper",
    asset: "both",
    balance: 100000,
    symbols: ["BTC/USDT", "ETH/USDT", "XAUUSD"],
  });
  const [checking, setChecking] = useState(false);

  // ดึงสถานะ trader ทุก 3 วินาทีเมื่อรันอยู่
  const fetchStatus = useCallback(async () => {
    try {
      const s = await api.getTraderStatus();
      setStatus(s);
      setError(null);
    } catch (e) {
      // Backend ไม่ได้รัน ก็ไม่ต้องแสดง error
      setChecking(true);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 3000);
    return () => clearInterval(interval);
  }, [fetchStatus]);

  const handleStart = async () => {
    setLoading(true);
    setError(null);
    try {
      const s = await api.startTrader(config);
      setStatus(s);
      setShowConfig(false);
    } catch (e: any) {
      setError(e.message || "Failed to start trader");
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    setLoading(true);
    setError(null);
    try {
      await api.stopTrader();
      await fetchStatus();
    } catch (e: any) {
      setError(e.message || "Failed to stop trader");
    } finally {
      setLoading(false);
    }
  };

  const isRunning = status?.running ?? false;
  const isChecking = checking && !status;

  return (
    <div className="rounded-xl bg-gray-900/50 border border-gray-800 p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <h3 className="text-sm font-semibold text-white flex items-center gap-2">
            🤖 Auto Trader
          </h3>
          {isChecking && (
            <span className="text-xs text-gray-500">Backend offline</span>
          )}
          {status && (
            <StatusBadge running={isRunning} mode={status.mode} />
          )}
        </div>
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="p-1.5 rounded-lg hover:bg-gray-800 transition-colors"
          title="Trader Settings"
        >
          <Settings2 className="h-4 w-4 text-gray-500" />
        </button>
      </div>

      {/* Status Row */}
      {status && (
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="text-center">
            <div className="text-xs text-gray-500 mb-0.5">Balance</div>
            <div className="text-sm font-bold text-white">
              ${formatCurrency(status.balance)}
            </div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-500 mb-0.5">Mode</div>
            <div className={`text-sm font-bold ${status.mode === "paper" ? "text-blue-400" : "text-red-400"}`}>
              {status.mode.toUpperCase()}
            </div>
          </div>
          <div className="text-center">
            <div className="text-xs text-gray-500 mb-0.5">P&L</div>
            <div className={`text-sm font-bold ${status.balance >= status.initial_balance ? "text-emerald-400" : "text-red-400"}`}>
              {status.balance >= status.initial_balance ? "+" : ""}
              ${formatCurrency(status.balance - status.initial_balance)}
            </div>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="flex items-center gap-2 text-red-400 text-xs mb-3 p-2 bg-red-400/10 rounded-lg">
          <AlertCircle className="h-3.5 w-3.5 shrink-0" />
          {error}
        </div>
      )}

      {/* Config Panel */}
      {showConfig && (
        <div className="mb-4 p-3 bg-gray-800/50 rounded-lg space-y-3">
          {/* Mode */}
          <div>
            <label className="text-xs text-gray-500 block mb-1">Mode</label>
            <div className="flex gap-2">
              {["paper", "live"].map((m) => (
                <button
                  key={m}
                  onClick={() => setConfig({ ...config, mode: m })}
                  className={`flex-1 py-1.5 text-xs rounded-lg font-medium transition-colors ${
                    config.mode === m
                      ? m === "paper"
                        ? "bg-blue-500/20 text-blue-400 border border-blue-500/30"
                        : "bg-red-500/20 text-red-400 border border-red-500/30"
                      : "bg-gray-700/50 text-gray-400 border border-gray-700"
                  }`}
                >
                  {m === "paper" ? "📝 Paper" : "💰 Live"}
                </button>
              ))}
            </div>
          </div>

          {/* Asset */}
          <div>
            <label className="text-xs text-gray-500 block mb-1">Assets</label>
            <div className="flex gap-2">
              {[
                { value: "crypto", label: "₿ Crypto" },
                { value: "gold", label: "🥇 Gold" },
                { value: "both", label: "₿+🥇 Both" },
              ].map((opt) => (
                <button
                  key={opt.value}
                  onClick={() => setConfig({ ...config, asset: opt.value })}
                  className={`flex-1 py-1.5 text-xs rounded-lg font-medium transition-colors ${
                    config.asset === opt.value
                      ? "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                      : "bg-gray-700/50 text-gray-400 border border-gray-700"
                  }`}
                >
                  {opt.label}
                </button>
              ))}
            </div>
          </div>

          {/* Balance (paper mode only) */}
          {config.mode === "paper" && (
            <div>
              <label className="text-xs text-gray-500 block mb-1">
                Initial Balance (USDT)
              </label>
              <input
                type="number"
                value={config.balance}
                onChange={(e) =>
                  setConfig({ ...config, balance: parseFloat(e.target.value) || 0 })
                }
                className="w-full bg-gray-700/50 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-white focus:outline-none focus:border-emerald-500"
                min={1000}
                step={1000}
              />
            </div>
          )}

          {/* Symbols */}
          <div>
            <label className="text-xs text-gray-500 block mb-1">Symbols</label>
            <div className="flex flex-wrap gap-1.5">
              {["BTC/USDT", "ETH/USDT", "SOL/USDT", "XAUUSD"].map((sym) => (
                <button
                  key={sym}
                  onClick={() => {
                    const syms = config.symbols.includes(sym)
                      ? config.symbols.filter((s) => s !== sym)
                      : [...config.symbols, sym];
                    setConfig({ ...config, symbols: syms });
                  }}
                  className={`px-2 py-1 text-xs rounded-md font-medium transition-colors ${
                    config.symbols.includes(sym)
                      ? "bg-amber-500/20 text-amber-400 border border-amber-500/30"
                      : "bg-gray-700/50 text-gray-400 border border-gray-700"
                  }`}
                >
                  {sym}
                </button>
              ))}
            </div>
          </div>

          {config.mode === "live" && (
            <div className="flex items-start gap-2 p-2 bg-red-500/10 rounded-lg">
              <AlertCircle className="h-3.5 w-3.5 text-red-400 shrink-0 mt-0.5" />
              <p className="text-xs text-red-400">
                Live trading will execute real orders on your exchange account.
                Make sure you have funds available.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-2">
        {!isRunning ? (
          <button
            onClick={handleStart}
            disabled={loading}
            className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-semibold text-sm transition-colors"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4" />
            )}
            {loading ? "Starting..." : "Start Auto Trader"}
          </button>
        ) : (
          <button
            onClick={handleStop}
            disabled={loading}
            className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-red-500/20 hover:bg-red-500/30 disabled:opacity-50 disabled:cursor-not-allowed text-red-400 font-semibold text-sm transition-colors border border-red-500/20"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Square className="h-4 w-4" />
            )}
            {loading ? "Stopping..." : "Stop Trader"}
          </button>
        )}
      </div>

      {/* Symbols being monitored */}
      {status?.symbols && status.symbols.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-800">
          <div className="text-xs text-gray-500 mb-1.5">Monitoring</div>
          <div className="flex flex-wrap gap-1.5">
            {status.symbols.map((sym) => (
              <span
                key={sym}
                className="px-2 py-0.5 bg-gray-800/50 rounded text-xs text-gray-400"
              >
                {sym}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Status Badge ──────────────────────────────────────────────
function StatusBadge({ running, mode }: { running: boolean; mode: string }) {
  if (running) {
    return (
      <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-medium">
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
        </span>
        Running
      </span>
    );
  }

  return (
    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-gray-500/10 text-gray-400 text-xs font-medium">
      <XCircle className="h-2.5 w-2.5" />
      Stopped
    </span>
  );
}
