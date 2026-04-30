"use client";

import { cn, formatCurrency, formatDate, formatTime, formatEntryExit, getStatusColor, getDirectionColor, getPnLColor } from "@/lib/utils";
import { Trade } from "@/types";
import { ArrowUpRight, ArrowDownRight, ExternalLink, ChevronDown, ChevronUp, Clock } from "lucide-react";
import Link from "next/link";
import { useState } from "react";

interface TradeTableProps {
  trades: Trade[];
  title?: string;
  limit?: number;
}

function TradeRow({ trade }: { trade: Trade }) {
  const [expanded, setExpanded] = useState(false);

  // คำอธิบาย trigger ภาษาไทย
  const triggerLabels: Record<string, string> = {
    stop_loss: "🔴 Stop Loss",
    take_profit: "🟢 Take Profit",
    trailing_stop: "📈 Trailing Stop",
    regime_change: "🔄 Regime Change",
    risk_manager: "⚠️ Risk Manager",
    manual: "✋ Manual",
  };

  return (
    <>
      <tr
        className="hover:bg-gray-800/50 transition-colors cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <td className="px-6 py-4">
          <div className="flex items-center gap-2">
            <span className="font-medium text-white">{trade.symbol}</span>
            {trade.asset_type === "gold" && (
              <span className="text-xs text-yellow-500">GOLD</span>
            )}
            {trade.asset_type === "crypto" && (
              <span className="text-xs text-blue-400">CRYPTO</span>
            )}
          </div>
        </td>
        <td className="px-6 py-4">
          <span
            className={cn(
              "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium",
              getDirectionColor(trade.direction)
            )}
          >
            {trade.direction === "buy" ? (
              <ArrowUpRight className="h-3 w-3" />
            ) : (
              <ArrowDownRight className="h-3 w-3" />
            )}
            {trade.direction.toUpperCase()}
          </span>
        </td>
        <td className="px-6 py-4 text-sm text-gray-400">
          ${formatCurrency(trade.entry_price)}
        </td>
        <td className="px-6 py-4 text-sm text-gray-400">
          {trade.exit_price ? `$${formatCurrency(trade.exit_price)}` : "—"}
        </td>
        <td className="px-6 py-4 text-sm text-gray-400">
          {trade.quantity}
        </td>
        <td className={cn("px-6 py-4 font-medium", getPnLColor(trade.pnl))}>
          {trade.pnl !== null && trade.pnl !== undefined
            ? `${trade.pnl >= 0 ? "+" : ""}${formatCurrency(trade.pnl)}`
            : "—"}
        </td>
        <td className="px-6 py-4">
          <span
            className={cn(
              "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium capitalize",
              getStatusColor(trade.status)
            )}
          >
            {trade.status}
          </span>
        </td>
        {/* เวลาเข้า */}
        <td className="px-6 py-4">
          <div className="flex items-center gap-1 text-sm text-gray-500">
            <Clock className="h-3 w-3" />
            <span>{formatDate(trade.entry_time)}</span>
          </div>
          {/* เวลาออก — แสดงเมื่อปิดแล้ว */}
          {trade.status === "closed" && trade.exit_time && (
            <div className="flex items-center gap-1 text-sm text-gray-500 mt-0.5">
              <span className="text-gray-600">→</span>
              <span>{formatDate(trade.exit_time)}</span>
            </div>
          )}
        </td>
        {/* เหตุผลเข้า */}
        <td className="px-6 py-4 max-w-[200px]">
          <div className="text-xs text-gray-400 truncate" title={trade.entry_reason?.summary || "-"}>
            {formatEntryExit(trade.entry_reason) || "—"}
          </div>
          {trade.status === "closed" && trade.exit_reason && (
            <div className="text-xs text-gray-500 truncate mt-0.5" title={trade.exit_reason.summary}>
              {triggerLabels[trade.exit_reason.trigger] || trade.exit_reason.trigger}: {trade.exit_reason.trigger_detail?.slice(0, 40) || "-"}
            </div>
          )}
        </td>
        <td className="px-6 py-4">
          {expanded ? (
            <ChevronUp className="h-4 w-4 text-gray-500" />
          ) : (
            <ChevronDown className="h-4 w-4 text-gray-500" />
          )}
        </td>
      </tr>
      {/* Expanded detail row */}
      {expanded && (
        <tr>
          <td colSpan={10} className="px-6 py-4 bg-gray-900/80 border-t border-gray-800">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* เหตุผลเปิด */}
              {trade.entry_reason && (
                <div className="rounded-lg bg-gray-800/50 p-4">
                  <p className="text-xs text-emerald-400 font-medium mb-2">📋 เหตุผลเปิด Trade</p>
                  <pre className="text-xs text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
                    {trade.entry_reason.summary || "ไม่มีข้อมูล"}
                  </pre>
                </div>
              )}
              {/* เหตุผลปิด */}
              {trade.exit_reason && (
                <div className="rounded-lg bg-gray-800/50 p-4">
                  <p className="text-xs text-amber-400 font-medium mb-2">📋 เหตุผลปิด Trade</p>
                  <pre className="text-xs text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">
                    {trade.exit_reason.summary || "ไม่มีข้อมูล"}
                  </pre>
                </div>
              )}
              {!trade.entry_reason && !trade.exit_reason && (
                <div className="text-xs text-gray-500 col-span-2">
                  ไม่มีข้อมูลเหตุผล — trade ก่อนหน้านี้ยังไม่ได้บันทึกเหตุผล
                </div>
              )}
            </div>
          </td>
        </tr>
      )}
    </>
  );
}

export function TradeTable({ trades, title, limit }: TradeTableProps) {
  const displayTrades = limit ? trades.slice(0, limit) : trades;

  return (
    <div className="rounded-2xl bg-gray-900/50 backdrop-blur-xl border border-gray-800 overflow-hidden">
      {title && (
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800">
          <h2 className="text-lg font-semibold text-white">{title}</h2>
          {limit && trades.length > limit && (
            <Link
              href="/history"
              className="flex items-center gap-1 text-sm text-emerald-400 hover:text-emerald-300"
            >
              View all <ExternalLink className="h-3.5 w-3.5" />
            </Link>
          )}
        </div>
      )}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-800 text-left text-xs text-gray-500 uppercase tracking-wider">
              <th className="px-6 py-3 font-medium">Symbol</th>
              <th className="px-6 py-3 font-medium">Direction</th>
              <th className="px-6 py-3 font-medium">Entry</th>
              <th className="px-6 py-3 font-medium">Exit</th>
              <th className="px-6 py-3 font-medium">Qty</th>
              <th className="px-6 py-3 font-medium">P&L</th>
              <th className="px-6 py-3 font-medium">Status</th>
              <th className="px-6 py-3 font-medium">Time (เข้า→ออก)</th>
              <th className="px-6 py-3 font-medium">Reason (เหตุผล)</th>
              <th className="px-6 py-3 font-medium w-8"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {displayTrades.length === 0 ? (
              <tr>
                <td colSpan={10} className="px-6 py-12 text-center text-gray-500">
                  No trades yet
                </td>
              </tr>
            ) : (
              displayTrades.map((trade) => (
                <TradeRow key={trade.id} trade={trade} />
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
