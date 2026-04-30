"use client";

import { cn } from "@/lib/utils";
import { forwardRef, InputHTMLAttributes } from "react";

export interface TextInputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(
  ({ label, error, hint, className, ...props }, ref) => {
    return (
      <div>
        {label && (
          <label className="block text-sm text-gray-500 mb-2">{label}</label>
        )}
        <input
          ref={ref}
          className={cn(
            "w-full rounded-lg bg-gray-800 border border-gray-700 px-4 py-3 text-white placeholder-gray-500",
            "focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/50",
            "transition-colors",
            error && "border-red-500 focus:border-red-500 focus:ring-red-500/50",
            className
          )}
          {...props}
        />
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

TextInput.displayName = "TextInput";
