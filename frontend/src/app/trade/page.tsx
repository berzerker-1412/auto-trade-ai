"use client";

import { useEffect, useState } from "react";
import { Zap, Play, RefreshCw } from "lucide-react";
import { api } from "@/lib/api";
import { Ticker, TradeSignal, TradeDirection } from "@/types";
import { formatCurrency, cn } from "@/lib/utils";
import { Button, NumberInput, DirectionToggle } from "@/components/ui/inputs";
import { Card, CardHeader, CardTitle } from "@/components/ui/layout";

export default function TradePage() {
  const [tickers, setTickers] = useState<Record<string, Ticker>>({});
  const [selectedSymbol, setSelectedSymbol] = useState("BTC/USDT");
  const [direction, setDirection] = useState<TradeDirection>(TradeDirection.BUY);
  const [quantity, setQuantity] = useState("0.01");
  const [stopLoss, setStopLoss] = useState("");
  const [takeProfit, setTakeProfit] = useState("");
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState<{ success: boolean; message: string } | null>(null);

  useEffect(() => {
    async function loadTickers() {
      try {
        const data = await api.getTickers();
        setTickers(data);
      } catch (error) {
        console.error("Failed to load tickers:", error);
      } finally {
        setLoading(false);
      }
    }
    loadTickers();
    const interval = setInterval(loadTickers, 5000);
    return () => clearInterval(interval);
  }, []);

  const currentTicker = tickers[selectedSymbol];

  const handleExecute = async () => {
    if (!currentTicker) return;

    setExecuting(true);
    setResult(null);

    try {
      const signal: TradeSignal = {
        symbol: selectedSymbol,
        direction,
        entry_price: currentTicker.price,
        quantity: parseFloat(quantity),
        stop_loss: stopLoss ? parseFloat(stopLoss) : undefined,
        take_profit: takeProfit ? parseFloat(takeProfit) : undefined,
        confidence: 0.85,
        reasoning: "Manual paper trade execution",
      };

      await api.executeSignal(signal);
      setResult({ success: true, message: `Position opened: ${direction.toUpperCase()} ${quantity} ${selectedSymbol}` });
      setStopLoss("");
      setTakeProfit("");
    } catch (error) {
      setResult({ success: false, message: "Failed to execute trade" });
    } finally {
      setExecuting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-400" />
      </div>
    );
  }

  return (
    <div className="p-8 space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Paper Trade</h1>
        <p className="mt-1 text-gray-500">Execute simulated trades without real money</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Symbol Selection */}
        <div className="lg:col-span-2 space-y-6">
          {/* Symbol Tabs */}
          <div className="flex gap-2 flex-wrap">
            {Object.keys(tickers).map((symbol) => (
              <button
                key={symbol}
                onClick={() => setSelectedSymbol(symbol)}
                className={cn(
                  "rounded-lg px-4 py-2 text-sm font-medium transition-all",
                  selectedSymbol === symbol
                    ? "bg-emerald-500 text-white"
                    : "bg-gray-800 text-gray-400 hover:bg-gray-700"
                )}
              >
                {symbol}
              </button>
            ))}
          </div>

          {/* Price Display */}
          {currentTicker && (
            <Card className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">{currentTicker.symbol}</p>
                  <p className="mt-2 text-4xl font-bold text-white">
                    {formatCurrency(currentTicker.price)}
                  </p>
                </div>
                <div className="text-right">
                  <div className="grid grid-cols-2 gap-x-8 gap-y-2 text-sm">
                    <div>
                      <p className="text-gray-500">High</p>
                      <p className="font-medium text-white">{formatCurrency(currentTicker.high)}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Low</p>
                      <p className="font-medium text-white">{formatCurrency(currentTicker.low)}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Bid</p>
                      <p className="font-medium text-emerald-400">{formatCurrency(currentTicker.bid)}</p>
                    </div>
                    <div>
                      <p className="text-gray-500">Ask</p>
                      <p className="font-medium text-red-400">{formatCurrency(currentTicker.ask)}</p>
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          )}

          {/* Trading Form */}
          <Card className="p-6">
            <CardHeader>
              <CardTitle>New Position</CardTitle>
            </CardHeader>

            <div className="space-y-6">
              {/* Direction Toggle */}
              <DirectionToggle
                value={direction}
                onChange={setDirection}
                disabled={executing}
              />

              {/* Quantity */}
              <NumberInput
                label="Quantity"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                step="0.001"
              />

              {/* SL/TP */}
              <div className="grid grid-cols-2 gap-4">
                <NumberInput
                  label="Stop Loss (Optional)"
                  value={stopLoss}
                  onChange={(e) => setStopLoss(e.target.value)}
                  placeholder="0.00"
                />
                <NumberInput
                  label="Take Profit (Optional)"
                  value={takeProfit}
                  onChange={(e) => setTakeProfit(e.target.value)}
                  placeholder="0.00"
                />
              </div>

              {/* Execute Button */}
              <Button
                variant={direction === TradeDirection.BUY ? "success" : "danger"}
                size="lg"
                className="w-full"
                loading={executing}
                disabled={executing || !quantity}
                icon={<Play className="h-5 w-5" />}
                onClick={handleExecute}
              >
                {executing ? "Executing..." : `Execute ${direction.toUpperCase()}`}
              </Button>

              {/* Result */}
              {result && (
                <div
                  className={cn(
                    "rounded-lg p-4 text-sm",
                    result.success
                      ? "bg-emerald-500/10 text-emerald-400"
                      : "bg-red-500/10 text-red-400"
                  )}
                >
                  {result.message}
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Sidebar - Quick Info */}
        <div className="space-y-6">
          {/* AI Suggestion */}
          <Card className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Zap className="h-5 w-5 text-emerald-400" />
              <CardTitle>AI Suggestion</CardTitle>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Direction</span>
                <span className="text-emerald-400 font-medium">BUY</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Confidence</span>
                <span className="text-white font-medium">78%</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Entry Zone</span>
                <span className="text-white font-medium">$67,200 - $67,500</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Risk/Reward</span>
                <span className="text-white font-medium">1:2.5</span>
              </div>
            </div>
            <Button variant="outline" size="sm" className="mt-4 w-full">
              Apply Suggestion
            </Button>
          </Card>

          {/* Risk Calculator */}
          <Card className="p-6">
            <CardHeader>
              <CardTitle>Risk Calculator</CardTitle>
            </CardHeader>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-500">Position Size</span>
                <span className="text-white">
                  ${(parseFloat(quantity) * (currentTicker?.price || 0)).toFixed(2)}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Risk per Trade</span>
                <span className="text-red-400">$150 (1.5%)</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Max Loss (SL)</span>
                <span className="text-red-400">
                  ${((parseFloat(quantity) * ((currentTicker?.price || 0) - (parseFloat(stopLoss) || 0))).toFixed(2))}
                </span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
