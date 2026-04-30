"use client";

import { cn, formatCurrency, formatDate, getStatusColor, getDirectionColor, getPnLColor } from "@/lib/utils";
import { Trade } from "@/types";
import { ArrowUpRight, ArrowDownRight, ExternalLink } from "lucide-react";
import Link from "next/link";

interface TradeTableProps {
  trades: Trade[];
  title?: string;
  limit?: number;
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
              <th className="px-6 py-3 font-medium">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {displayTrades.length === 0 ? (
              <tr>
                <td colSpan={8} className="px-6 py-12 text-center text-gray-500">
                  No trades yet
                </td>
              </tr>
            ) : (
              displayTrades.map((trade) => (
                <tr key={trade.id} className="hover:bg-gray-800/50 transition-colors">
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
                    {trade.exit_price ? `$${formatCurrency(trade.exit_price)}` : "-"}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-400">
                    {trade.quantity}
                  </td>
                  <td className={cn("px-6 py-4 font-medium", getPnLColor(trade.pnl))}>
                    {trade.pnl !== null && trade.pnl !== undefined
                      ? `${trade.pnl >= 0 ? "+" : ""}$${formatCurrency(trade.pnl)}`
                      : "-"}
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
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {formatDate(trade.entry_time)}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
