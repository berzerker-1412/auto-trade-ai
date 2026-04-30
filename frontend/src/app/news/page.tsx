"use client";

import { Newspaper } from "lucide-react";
import { NewsFeed } from "@/components/NewsFeed";

export default function NewsPage() {
  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-white flex items-center gap-3">
          <Newspaper className="w-8 h-8" />
          News Intelligence
        </h1>
        <p className="mt-1 text-gray-500">
          ข่าวจาก Reuters, Bloomberg, BBC และสำนักข่าวไทย พร้อม sentiment analysis และ trade signals
        </p>
      </div>

      <NewsFeed />
    </div>
  );
}
