"use client";

import { useEffect, useRef, useState } from "react";
import {
  createChart,
  IChartApi,
  CandlestickData,
  Time,
  CrosshairMode,
  CandlestickSeries,
  LineSeries,
} from "lightweight-charts";
import { cn } from "@/lib/utils";

interface ChartProps {
  symbol: string;
}

export interface DrawingTool {
  id: string;
  type: "trendline" | "horizontal";
  points: { time: Time; price: number }[];
  color: string;
}

const DRAWING_COLORS = [
  "#10b981",
  "#f59e0b",
  "#3b82f6",
  "#ef4444",
  "#8b5cf6",
  "#ec4899",
];

export function PriceChart({ symbol }: ChartProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const drawingsRef = useRef<Map<string, unknown>>(new Map());
  const [drawings, setDrawings] = useState<DrawingTool[]>([]);
  const [showToolbar, setShowToolbar] = useState(true);

  // Generate sample candlestick data
  const generateCandleData = (basePrice = 67500): CandlestickData<Time>[] => {
    const data: CandlestickData<Time>[] = [];
    const now = Math.floor(Date.now() / 1000);
    const dayInSeconds = 86400;
    let price = basePrice;

    for (let i = 365; i >= 0; i--) {
      const time = (now - i * dayInSeconds) as Time;
      const volatility = price * 0.02;
      const open = price;
      const change = (Math.random() - 0.48) * volatility;
      const close = open + change;
      const high = Math.max(open, close) + Math.random() * volatility * 0.5;
      const low = Math.min(open, close) - Math.random() * volatility * 0.5;

      data.push({ time, open, high, low, close });
      price = close;
    }
    return data;
  };

  useEffect(() => {
    if (!containerRef.current) return;

    const chart = createChart(containerRef.current, {
      layout: {
        background: { color: "transparent" },
        textColor: "#9ca3af",
      },
      grid: {
        vertLines: { color: "#1f2937" },
        horzLines: { color: "#1f2937" },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: {
          color: "#6b7280",
          width: 1,
          style: 2,
          labelBackgroundColor: "#374151",
        },
        horzLine: {
          color: "#6b7280",
          width: 1,
          style: 2,
          labelBackgroundColor: "#374151",
        },
      },
      rightPriceScale: {
        borderColor: "#374151",
      },
      timeScale: {
        borderColor: "#374151",
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: "#10b981",
      downColor: "#ef4444",
      borderUpColor: "#10b981",
      borderDownColor: "#ef4444",
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });

    chartRef.current = chart;

    // Load data
    candleSeries.setData(generateCandleData());

    // Handle resize
    const handleResize = () => {
      if (containerRef.current && chartRef.current) {
        chartRef.current.applyOptions({ width: containerRef.current.clientWidth });
      }
    };

    window.addEventListener("resize", handleResize);
    handleResize();

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
    };
  }, [symbol]);

  // Render drawings on chart
  useEffect(() => {
    if (!chartRef.current) return;

    // Clear existing drawings
    drawingsRef.current.forEach((line) => {
      if (typeof line === "object" && line && "remove" in line) {
        (line as { remove: () => void }).remove();
      }
    });
    drawingsRef.current.clear();

    drawings.forEach((drawing) => {
      if (!chartRef.current) return;

      const line = chartRef.current.addSeries(LineSeries, {
        color: drawing.color,
        lineWidth: 2,
        lineStyle: 0,
        crosshairMarkerVisible: false,
        lastValueVisible: true,
        title: "",
      });

      const startTime = (Math.floor(Date.now() / 1000) - 365 * 86400) as Time;
      const endTime = (Math.floor(Date.now() / 1000)) as Time;

      if (drawing.type === "horizontal") {
        line.setData([
          { time: startTime, value: drawing.points[0].price },
          { time: endTime, value: drawing.points[0].price },
        ]);
      } else if (drawing.points.length >= 2) {
        line.setData(drawing.points.map(p => ({ time: p.time, value: p.price })) as { time: Time; value: number }[]);
      }

      drawingsRef.current.set(drawing.id, line);
    });
  }, [drawings]);

  const addHorizontalLine = () => {
    // Add a horizontal line at the middle of visible price range
    // Using a fixed price for demo purposes - in production, use chart coordinate APIs
    const midPrice = 67500 + Math.random() * 5000;
    const now = Math.floor(Date.now() / 1000) as Time;

    const newDrawing: DrawingTool = {
      id: `${Date.now()}`,
      type: "horizontal",
      points: [{ time: now, price: midPrice }],
      color: DRAWING_COLORS[drawings.length % DRAWING_COLORS.length],
    };

    setDrawings((prev) => [...prev, newDrawing]);
  };

  const clearDrawings = () => {
    drawingsRef.current.forEach((line) => {
      if (typeof line === "object" && line && "remove" in line) {
        (line as { remove: () => void }).remove();
      }
    });
    drawingsRef.current.clear();
    setDrawings([]);
  };

  return (
    <div className="relative rounded-xl bg-gray-900/50 border border-gray-800 overflow-hidden">
      {/* Chart Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800">
        <div className="flex items-center gap-3">
          <h3 className="font-semibold text-white">{symbol}</h3>
          <span className="text-xs text-gray-500">Daily</span>
        </div>
        <button
          onClick={() => setShowToolbar(!showToolbar)}
          className="text-xs text-gray-500 hover:text-white transition-colors"
        >
          {showToolbar ? "Hide Tools" : "Show Tools"}
        </button>
      </div>

      {/* Drawing Toolbar */}
      {showToolbar && (
        <div className="flex items-center gap-2 px-4 py-2 border-b border-gray-800 bg-gray-900/30">
          <button
            onClick={addHorizontalLine}
            className="px-3 py-1.5 text-xs rounded-lg text-gray-400 hover:bg-gray-800 transition-colors"
          >
            + Add Horizontal Line
          </button>

          <div className="h-4 w-px bg-gray-700 mx-2" />

          <button
            onClick={clearDrawings}
            className="px-3 py-1.5 text-xs rounded-lg text-gray-400 hover:bg-gray-800 transition-colors"
          >
            Clear All
          </button>

          <div className="ml-auto text-xs text-gray-500">
            {drawings.length} line{drawings.length !== 1 ? "s" : ""}
          </div>
        </div>
      )}

      {/* Chart Container */}
      <div ref={containerRef} className="h-96" />

      {/* Drawing List */}
      {drawings.length > 0 && (
        <div className="px-4 py-2 border-t border-gray-800 bg-gray-900/30">
          <p className="text-xs text-gray-500 mb-2">Lines</p>
          <div className="flex flex-wrap gap-2">
            {drawings.map((d, i) => (
              <div
                key={d.id}
                className="flex items-center gap-2 px-2 py-1 rounded bg-gray-800 text-xs"
              >
                <div className="w-3 h-0.5" style={{ backgroundColor: d.color }} />
                <span className="text-gray-300">${d.points[0].price.toFixed(2)}</span>
                <button
                  onClick={() => setDrawings((prev) => prev.filter((_, idx) => idx !== i))}
                  className="text-gray-500 hover:text-red-400 ml-1"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
