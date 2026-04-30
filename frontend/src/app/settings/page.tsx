"use client";

import { useState } from "react";
import { Save, RefreshCw, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";

export default function SettingsPage() {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [settings, setSettings] = useState({
    // Exchange
    exchangeName: "binance",
    apiKey: "",
    apiSecret: "",
    testnet: true,

    // Paper Trade
    initialBalance: "100000",
    balanceCurrency: "USDT",

    // AI Settings
    aiProvider: "openai",
    openaiApiKey: "",
    aiModel: "gpt-4o",
    confidenceThreshold: "75",

    // Trading
    maxTradesPerDay: "5",
    maxPositionSize: "10",
    stopLossPercent: "2",
    takeProfitPercent: "5",
    maxConcurrentTrades: "3",

    // Gold Source
    goldSource: "demo",
    goldApiKey: "",
  });

  const handleSave = async () => {
    setSaving(true);
    // Simulate save
    await new Promise((r) => setTimeout(r, 1000));
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    setSettings(settings);
  };

  return (
    <div className="p-8 space-y-8 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Settings</h1>
          <p className="mt-1 text-gray-500">Configure your trading preferences</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={handleReset}
            className="flex items-center gap-2 rounded-lg bg-gray-800 px-4 py-2 text-sm text-gray-300 hover:bg-gray-700"
          >
            <RefreshCw className="h-4 w-4" />
            Reset
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            className={cn(
              "flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-all",
              saved
                ? "bg-emerald-500 text-white"
                : "bg-gradient-to-r from-emerald-500 to-cyan-500 text-white hover:opacity-90"
            )}
          >
            <Save className="h-4 w-4" />
            {saving ? "Saving..." : saved ? "Saved!" : "Save Changes"}
          </button>
        </div>
      </div>

      {/* Exchange Settings */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-white border-b border-gray-800 pb-2">
          Exchange Configuration
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-gray-500 mb-2">Exchange</label>
            <select
              value={settings.exchangeName}
              onChange={(e) => setSettings({ ...settings, exchangeName: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="binance">Binance</option>
              <option value="bybit">Bybit</option>
              <option value="okx">OKX</option>
            </select>
          </div>
          <div className="flex items-end">
            <label className="flex items-center gap-3 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.testnet}
                onChange={(e) => setSettings({ ...settings, testnet: e.target.checked })}
                className="h-5 w-5 rounded border-gray-700 bg-gray-800 text-emerald-500 focus:ring-emerald-500"
              />
              <span className="text-sm text-white">Use Testnet (Paper Trading)</span>
            </label>
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">API Key</label>
            <input
              type="password"
              value={settings.apiKey}
              onChange={(e) => setSettings({ ...settings, apiKey: e.target.value })}
              placeholder="Enter your API key"
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">API Secret</label>
            <input
              type="password"
              value={settings.apiSecret}
              onChange={(e) => setSettings({ ...settings, apiSecret: e.target.value })}
              placeholder="Enter your API secret"
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
        </div>
        <p className="text-xs text-gray-500">
          Get your API keys from{" "}
          <a href="https://www.binance.com" target="_blank" rel="noopener" className="text-emerald-400 hover:underline inline-flex items-center gap-1">
            Binance <ExternalLink className="h-3 w-3" />
          </a>{" "}
          or{" "}
          <a href="https://testnet.binance.vision" target="_blank" rel="noopener" className="text-emerald-400 hover:underline inline-flex items-center gap-1">
            Testnet <ExternalLink className="h-3 w-3" />
          </a>
        </p>
      </section>

      {/* Paper Trade Settings */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-white border-b border-gray-800 pb-2">
          Paper Trading
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-gray-500 mb-2">Initial Balance</label>
            <input
              type="number"
              value={settings.initialBalance}
              onChange={(e) => setSettings({ ...settings, initialBalance: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Currency</label>
            <select
              value={settings.balanceCurrency}
              onChange={(e) => setSettings({ ...settings, balanceCurrency: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="USDT">USDT</option>
              <option value="USD">USD</option>
              <option value="THB">THB</option>
            </select>
          </div>
        </div>
      </section>

      {/* AI Settings */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-white border-b border-gray-800 pb-2">
          AI Configuration
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-gray-500 mb-2">AI Provider</label>
            <select
              value={settings.aiProvider}
              onChange={(e) => setSettings({ ...settings, aiProvider: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="openai">OpenAI</option>
              <option value="anthropic">Anthropic</option>
              <option value="local">Local Model</option>
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Model</label>
            <select
              value={settings.aiModel}
              onChange={(e) => setSettings({ ...settings, aiModel: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="gpt-4o">GPT-4o</option>
              <option value="gpt-4-turbo">GPT-4 Turbo</option>
              <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
            </select>
          </div>
          <div className="md:col-span-2">
            <label className="block text-sm text-gray-500 mb-2">OpenAI API Key</label>
            <input
              type="password"
              value={settings.openaiApiKey}
              onChange={(e) => setSettings({ ...settings, openaiApiKey: e.target.value })}
              placeholder="sk-..."
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Confidence Threshold (%)</label>
            <input
              type="number"
              value={settings.confidenceThreshold}
              onChange={(e) => setSettings({ ...settings, confidenceThreshold: e.target.value })}
              min="0"
              max="100"
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
            <p className="mt-1 text-xs text-gray-500">Minimum AI confidence to execute trade</p>
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Max Trades per Day</label>
            <input
              type="number"
              value={settings.maxTradesPerDay}
              onChange={(e) => setSettings({ ...settings, maxTradesPerDay: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
        </div>
      </section>

      {/* Risk Management */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-white border-b border-gray-800 pb-2">
          Risk Management
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-gray-500 mb-2">Max Position Size (%)</label>
            <input
              type="number"
              value={settings.maxPositionSize}
              onChange={(e) => setSettings({ ...settings, maxPositionSize: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Max Concurrent Trades</label>
            <input
              type="number"
              value={settings.maxConcurrentTrades}
              onChange={(e) => setSettings({ ...settings, maxConcurrentTrades: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Default Stop Loss (%)</label>
            <input
              type="number"
              value={settings.stopLossPercent}
              onChange={(e) => setSettings({ ...settings, stopLossPercent: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-500 mb-2">Default Take Profit (%)</label>
            <input
              type="number"
              value={settings.takeProfitPercent}
              onChange={(e) => setSettings({ ...settings, takeProfitPercent: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            />
          </div>
        </div>
      </section>

      {/* Gold Settings */}
      <section className="space-y-4">
        <h2 className="text-lg font-semibold text-white border-b border-gray-800 pb-2">
          Gold Price Source
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm text-gray-500 mb-2">Data Source</label>
            <select
              value={settings.goldSource}
              onChange={(e) => setSettings({ ...settings, goldSource: e.target.value })}
              className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
            >
              <option value="demo">Demo (Simulated)</option>
              <option value="alpha_vantage">Alpha Vantage</option>
              <option value="goldapi">GoldAPI.io</option>
            </select>
          </div>
          {settings.goldSource !== "demo" && (
            <div>
              <label className="block text-sm text-gray-500 mb-2">API Key</label>
              <input
                type="password"
                value={settings.goldApiKey}
                onChange={(e) => setSettings({ ...settings, goldApiKey: e.target.value })}
                placeholder="Enter API key"
                className="w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white focus:border-emerald-500 focus:outline-none"
              />
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
