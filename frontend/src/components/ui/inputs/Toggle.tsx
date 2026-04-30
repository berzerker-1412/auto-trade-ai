"use client";

import { cn } from "@/lib/utils";
import { InputHTMLAttributes, forwardRef } from "react";

export interface ToggleProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: string;
  description?: string;
}

export const Toggle = forwardRef<HTMLInputElement, ToggleProps>(
  ({ label, description, className, ...props }, ref) => {
    return (
      <label className={cn("flex items-start gap-3 cursor-pointer", className)}>
        <div className="relative mt-0.5">
          <input
            ref={ref}
            type="checkbox"
            className="sr-only peer"
            {...props}
          />
          <div className="w-10 h-6 rounded-full bg-gray-700 peer-checked:bg-emerald-500 transition-colors" />
          <div className="absolute left-1 top-1 w-4 h-4 rounded-full bg-white transition-transform peer-checked:translate-x-4" />
        </div>
        <div className="flex-1">
          {label && (
            <span className="block text-sm text-white">{label}</span>
          )}
          {description && (
            <span className="block text-xs text-gray-500 mt-0.5">{description}</span>
          )}
        </div>
      </label>
    );
  }
);

Toggle.displayName = "Toggle";
