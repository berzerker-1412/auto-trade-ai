"use client";

import { cn } from "@/lib/utils";
import { SelectHTMLAttributes, forwardRef } from "react";

export interface SelectOption {
  value: string;
  label: string;
}

export interface SelectInputProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  hint?: string;
  options: SelectOption[];
}

export const SelectInput = forwardRef<HTMLSelectElement, SelectInputProps>(
  ({ label, error, hint, options, className, ...props }, ref) => {
    return (
      <div>
        {label && (
          <label className="block text-sm text-gray-500 mb-2">{label}</label>
        )}
        <select
          ref={ref}
          className={cn(
            "w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white",
            "focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/50",
            "transition-colors cursor-pointer",
            error && "border-red-500 focus:border-red-500 focus:ring-red-500/50",
            className
          )}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {hint && !error && (
          <p className="mt-1 text-xs text-gray-500">{hint}</p>
        )}
        {error && (
          <p className="mt-1 text-xs text-red-400">{error}</p>
        )}
      </div>
    );
  }
);

SelectInput.displayName = "SelectInput";
