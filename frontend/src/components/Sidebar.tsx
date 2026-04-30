"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  History,
  Play,
  Settings,
  TrendingUp,
  Wallet,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Trade History", href: "/history", icon: History },
  { name: "Paper Trade", href: "/trade", icon: Play },
  { name: "Settings", href: "/settings", icon: Settings },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 bg-gray-900/50 backdrop-blur-xl border-r border-gray-800">
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="flex h-16 items-center gap-3 px-6 border-b border-gray-800">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-emerald-400 to-cyan-500">
            <TrendingUp className="h-5 w-5 text-gray-900" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-white">Auto Trade</h1>
            <p className="text-xs text-gray-500">AI Powered</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navigation.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                  isActive
                    ? "bg-emerald-500/10 text-emerald-400"
                    : "text-gray-400 hover:bg-gray-800 hover:text-white"
                )}
              >
                <item.icon
                  className={cn(
                    "h-5 w-5 transition-colors",
                    isActive ? "text-emerald-400" : "text-gray-500 group-hover:text-white"
                  )}
                />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Balance Card */}
        <div className="p-4 border-t border-gray-800">
          <div className="rounded-xl bg-gradient-to-br from-gray-800 to-gray-900 p-4">
            <div className="flex items-center gap-2 text-xs text-gray-500 mb-1">
              <Wallet className="h-3.5 w-3.5" />
              Paper Balance
            </div>
            <div className="text-2xl font-bold text-white">$105,000</div>
            <div className="text-sm text-emerald-400">+$5,000 (5.0%)</div>
          </div>
        </div>
      </div>
    </aside>
  );
}
