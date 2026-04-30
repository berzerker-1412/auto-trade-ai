"use client";

import { cn } from "@/lib/utils";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";
import { TradeDirection } from "@/types";

interface DirectionToggleProps {
  value: TradeDirection;
  onChange: (direction: TradeDirection) => void;
  disabled?: boolean;
}

export function DirectionToggle({ value, onChange, disabled }: DirectionToggleProps) {
  return (
    <div className="grid grid-cols-2 gap-4">
      <button
        type="button"
        disabled={disabled}
        onClick={() => onChange(TradeDirection.BUY)}
        className={cn(
          "flex items-center justify-center gap-2 rounded-xl py-4 font-semibold transition-all",
          value === TradeDirection.BUY
            ? "bg-emerald-500 text-white"
            : "bg-gray-800 text-gray-400 hover:bg-gray-700",
          disabled && "opacity-50 cursor-not-allowed"
        )}
      >
        <ArrowUpRight className="h-5 w-5" />
        BUY / LONG
      </button>
      <button
        type="button"
        disabled={disabled}
        onClick={() => onChange(TradeDirection.SELL)}
        className={cn(
          "flex items-center justify-center gap-2 rounded-xl py-4 font-semibold transition-all",
          value === TradeDirection.SELL
            ? "bg-red-500 text-white"
            : "bg-gray-800 text-gray-400 hover:bg-gray-700",
          disabled && "opacity-50 cursor-not-allowed"
        )}
      >
        <ArrowDownRight className="h-5 w-5" />
        SELL / SHORT
      </button>
    </div>
  );
}
