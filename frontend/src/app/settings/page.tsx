"use client";

import { useState } from "react";
import { Save, RefreshCw, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";
import { TextInput, SelectInput, NumberInput, Toggle, Button } from "@/components/ui/inputs";
import { Section, Card, CardHeader, CardTitle } from "@/components/ui/layout";

export default function SettingsPage() {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  const [settings, setSettings] = useState({
    exchangeName: "binance",
    apiKey: "",
    apiSecret: "",
    testnet: true,
    initialBalance: "100000",
    balanceCurrency: "USDT",
    aiProvider: "openai",
    openaiApiKey: "",
    aiModel: "gpt-4o",
    confidenceThreshold: "75",
    maxTradesPerDay: "5",
    maxPositionSize: "10",
    stopLossPercent: "2",
    takeProfitPercent: "5",
    maxConcurrentTrades: "3",
    goldSource: "demo",
    goldApiKey: "",
  });

  const handleSave = async () => {
    setSaving(true);
    await new Promise((r) => setTimeout(r, 1000));
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    setSettings(settings);
  };

  const set = (key: keyof typeof settings) => (val: string | boolean) =>
    setSettings((s) => ({ ...s, [key]: val }));

  return (
    <div className="p-8 space-y-8 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Settings</h1>
          <p className="mt-1 text-gray-500">Configure your trading preferences</p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" size="md" icon={<RefreshCw className="h-4 w-4" />} onClick={handleReset}>
            Reset
          </Button>
          <Button
            variant={saved ? "success" : "primary"}
            size="md"
            loading={saving}
            icon={<Save className="h-4 w-4" />}
            onClick={handleSave}
          >
            {saving ? "Saving..." : saved ? "Saved!" : "Save Changes"}
          </Button>
        </div>
      </div>

      {/* Exchange Settings */}
      <Section
        title="Exchange Configuration"
        className="bg-gray-900/50 border border-gray-800 rounded-xl p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SelectInput
            label="Exchange"
            value={settings.exchangeName}
            onChange={(e) => set("exchangeName")(e.target.value)}
            options={[
              { value: "binance", label: "Binance" },
              { value: "bybit", label: "Bybit" },
              { value: "okx", label: "OKX" },
            ]}
          />
          <Toggle
            label="Use Testnet (Paper Trading)"
            checked={settings.testnet}
            onChange={(e) => set("testnet")(e.target.checked)}
          />
          <TextInput
            label="API Key"
            type="password"
            value={settings.apiKey}
            onChange={(e) => set("apiKey")(e.target.value)}
            placeholder="Enter your API key"
          />
          <TextInput
            label="API Secret"
            type="password"
            value={settings.apiSecret}
            onChange={(e) => set("apiSecret")(e.target.value)}
            placeholder="Enter your API secret"
          />
        </div>
        <p className="text-xs text-gray-500 mt-4">
          Get your API keys from{" "}
          <a href="https://www.binance.com" target="_blank" rel="noopener" className="text-emerald-400 hover:underline inline-flex items-center gap-1">
            Binance <ExternalLink className="h-3 w-3" />
          </a>{" "}
          or{" "}
          <a href="https://testnet.binance.vision" target="_blank" rel="noopener" className="text-emerald-400 hover:underline inline-flex items-center gap-1">
            Testnet <ExternalLink className="h-3 w-3" />
          </a>
        </p>
      </Section>

      {/* Paper Trade Settings */}
      <Section
        title="Paper Trading"
        className="bg-gray-900/50 border border-gray-800 rounded-xl p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <NumberInput
            label="Initial Balance"
            value={settings.initialBalance}
            onChange={(e) => set("initialBalance")(e.target.value)}
          />
          <SelectInput
            label="Currency"
            value={settings.balanceCurrency}
            onChange={(e) => set("balanceCurrency")(e.target.value)}
            options={[
              { value: "USDT", label: "USDT" },
              { value: "USD", label: "USD" },
              { value: "THB", label: "THB" },
            ]}
          />
        </div>
      </Section>

      {/* AI Settings */}
      <Section
        title="AI Configuration"
        className="bg-gray-900/50 border border-gray-800 rounded-xl p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SelectInput
            label="AI Provider"
            value={settings.aiProvider}
            onChange={(e) => set("aiProvider")(e.target.value)}
            options={[
              { value: "openai", label: "OpenAI" },
              { value: "anthropic", label: "Anthropic" },
              { value: "local", label: "Local Model" },
            ]}
          />
          <SelectInput
            label="Model"
            value={settings.aiModel}
            onChange={(e) => set("aiModel")(e.target.value)}
            options={[
              { value: "gpt-4o", label: "GPT-4o" },
              { value: "gpt-4-turbo", label: "GPT-4 Turbo" },
              { value: "gpt-3.5-turbo", label: "GPT-3.5 Turbo" },
            ]}
          />
          <div className="md:col-span-2">
            <TextInput
              label="OpenAI API Key"
              type="password"
              value={settings.openaiApiKey}
              onChange={(e) => set("openaiApiKey")(e.target.value)}
              placeholder="sk-..."
            />
          </div>
          <NumberInput
            label="Confidence Threshold (%)"
            value={settings.confidenceThreshold}
            onChange={(e) => set("confidenceThreshold")(e.target.value)}
            min={0}
            max={100}
            hint="Minimum AI confidence to execute trade"
          />
          <NumberInput
            label="Max Trades per Day"
            value={settings.maxTradesPerDay}
            onChange={(e) => set("maxTradesPerDay")(e.target.value)}
          />
        </div>
      </Section>

      {/* Risk Management */}
      <Section
        title="Risk Management"
        className="bg-gray-900/50 border border-gray-800 rounded-xl p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <NumberInput
            label="Max Position Size (%)"
            value={settings.maxPositionSize}
            onChange={(e) => set("maxPositionSize")(e.target.value)}
          />
          <NumberInput
            label="Max Concurrent Trades"
            value={settings.maxConcurrentTrades}
            onChange={(e) => set("maxConcurrentTrades")(e.target.value)}
          />
          <NumberInput
            label="Default Stop Loss (%)"
            value={settings.stopLossPercent}
            onChange={(e) => set("stopLossPercent")(e.target.value)}
          />
          <NumberInput
            label="Default Take Profit (%)"
            value={settings.takeProfitPercent}
            onChange={(e) => set("takeProfitPercent")(e.target.value)}
          />
        </div>
      </Section>

      {/* Gold Settings */}
      <Section
        title="Gold Price Source"
        className="bg-gray-900/50 border border-gray-800 rounded-xl p-6"
      >
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <SelectInput
            label="Data Source"
            value={settings.goldSource}
            onChange={(e) => set("goldSource")(e.target.value)}
            options={[
              { value: "demo", label: "Demo (Simulated)" },
              { value: "alpha_vantage", label: "Alpha Vantage" },
              { value: "goldapi", label: "GoldAPI.io" },
            ]}
          />
          {settings.goldSource !== "demo" && (
            <TextInput
              label="API Key"
              type="password"
              value={settings.goldApiKey}
              onChange={(e) => set("goldApiKey")(e.target.value)}
              placeholder="Enter API key"
            />
          )}
        </div>
      </Section>
    </div>
  );
}
