"use client";

import { useEffect, useState } from "react";
import {
  Newspaper,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Zap,
  Globe,
  ChevronRight,
  RefreshCw,
  Loader2,
} from "lucide-react";

type SentimentLabel = "positive" | "negative" | "neutral";

interface TradeSignal {
  bias: string;
  score: number;
  signal: {
    direction: string;
    top_assets: string[];
    confidence: number;
    reason?: string;
  } | null;
  reason: string;
  impacted_assets: string[];
  asset_sentiments: Record<string, number>;
  category_breakdown: Record<string, number>;
  risk_level: string;
  article_count: number;
}

interface Article {
  id: number;
  title: string;
  url: string;
  source: string;
  category: string;
  published_at: string | null;
  summary: string;
  sentiment_score: number;
  sentiment_label: SentimentLabel;
  impact_tags: string[];
}

interface NewsFeedResponse {
  articles: Article[];
  trade_signal: TradeSignal;
  total: number;
  generated_at: string;
}

const SENTIMENT_CONFIG = {
  positive: {
    color: "text-green-400",
    bg: "bg-green-500/10",
    border: "border-green-500/30",
    icon: TrendingUp,
    label: "Positive",
  },
  negative: {
    color: "text-red-400",
    bg: "bg-red-500/10",
    border: "border-red-500/30",
    icon: TrendingDown,
    label: "Negative",
  },
  neutral: {
    color: "text-gray-400",
    bg: "bg-gray-500/10",
    border: "border-gray-500/30",
    icon: Globe,
    label: "Neutral",
  },
};

const RISK_CONFIG = {
  low: { color: "text-green-400", label: "Low Risk" },
  medium: { color: "text-yellow-400", label: "Medium Risk" },
  high: { color: "text-red-400", label: "HIGH RISK" },
};

const CATEGORY_COLORS: Record<string, string> = {
  war: "bg-red-500/20 text-red-400",
  finance: "bg-blue-500/20 text-blue-400",
  economy: "bg-yellow-500/20 text-yellow-400",
  crypto: "bg-orange-500/20 text-orange-400",
  commodities: "bg-amber-500/20 text-amber-400",
  markets: "bg-purple-500/20 text-purple-400",
  international: "bg-cyan-500/20 text-cyan-400",
  general: "bg-gray-500/20 text-gray-400",
};

export function NewsFeed() {
  const [feed, setFeed] = useState<NewsFeedResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("all");
  const [scrapeLoading, setScrapeLoading] = useState(false);

  const fetchFeed = async () => {
    setLoading(true);
    try {
      const url = filter === "all"
        ? "/api/news/feed?limit=50"
        : `/api/news/feed?limit=50&category=${filter}`;
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setFeed(data);
      }
    } catch (e) {
      console.error("Failed to fetch news feed", e);
    } finally {
      setLoading(false);
    }
  };

  const triggerScrape = async () => {
    setScrapeLoading(true);
    try {
      const res = await fetch("/api/news/scrape", { method: "POST" });
      if (res.ok) {
        await fetchFeed();
      }
    } catch (e) {
      console.error("Scrape failed", e);
    } finally {
      setScrapeLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
  }, [filter]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-gray-500" />
      </div>
    );
  }

  if (!feed) {
    return (
      <div className="text-center text-gray-500 py-12">
        <Newspaper className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>ไม่สามารถโหลดข่าวได้</p>
        <button onClick={fetchFeed} className="mt-3 text-blue-400 hover:underline">
          ลองใหม่
        </button>
      </div>
    );
  }

  const { trade_signal, articles } = feed;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Newspaper className="w-5 h-5" />
            News Intelligence Feed
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            ข่าว {feed.total} ข่าว • อัปเดต {new Date(feed.generated_at).toLocaleTimeString("th-TH")}
          </p>
        </div>
        <button
          onClick={triggerScrape}
          disabled={scrapeLoading}
          className="flex items-center gap-2 px-3 py-1.5 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-800 text-white rounded-lg text-sm transition-colors"
        >
          {scrapeLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <RefreshCw className="w-4 h-4" />
          )}
          Scrape ข่าวใหม่
        </button>
      </div>

      {/* Trade Signal Banner */}
      {trade_signal && (
        <TradeSignalBanner signal={trade_signal} />
      )}

      {/* Filters */}
      <div className="flex gap-2 flex-wrap">
        {["all", "war", "finance", "crypto", "economy", "markets"].map((cat) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            className={`px-3 py-1 rounded-full text-sm transition-colors ${
              filter === cat
                ? "bg-blue-600 text-white"
                : "bg-gray-800 text-gray-400 hover:bg-gray-700"
            }`}
          >
            {cat === "all" ? "ทั้งหมด" : cat.charAt(0).toUpperCase() + cat.slice(1)}
          </button>
        ))}
      </div>

      {/* Articles */}
      <div className="space-y-3">
        {articles.length === 0 && (
          <div className="text-center text-gray-500 py-12">
            <Newspaper className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>ยังไม่มีข่าวในหมวดนี้</p>
          </div>
        )}
        {articles.map((article) => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
}

function TradeSignalBanner({ signal }: { signal: TradeSignal }) {
  const riskCfg = RISK_CONFIG[signal.risk_level as keyof typeof RISK_CONFIG] || RISK_CONFIG.low;
  const isBullish = signal.bias === "bullish";
  const isBearish = signal.bias === "bearish";

  return (
    <div className={`rounded-xl border p-4 ${
      isBullish ? "bg-green-500/10 border-green-500/30" :
      isBearish ? "bg-red-500/10 border-red-500/30" :
      "bg-gray-800 border-gray-700"
    }`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            {isBullish && <TrendingUp className="w-5 h-5 text-green-400" />}
            {isBearish && <TrendingDown className="w-5 h-5 text-red-400" />}
            {!isBullish && !isBearish && <Zap className="w-5 h-5 text-gray-400" />}
            <span className={`text-lg font-bold ${
              isBullish ? "text-green-400" : isBearish ? "text-red-400" : "text-gray-400"
            }`}>
              {signal.bias === "bullish" ? "📈 BULLISH BIAS" :
               signal.bias === "bearish" ? "📉 BEARISH BIAS" : "⚖️ NEUTRAL"}
            </span>
          </div>
          <p className="text-sm text-gray-400 mt-1">{signal.reason}</p>
        </div>
        <div className="text-right">
          <span className={`text-2xl font-bold ${riskCfg.color}`}>
            {signal.score > 0 ? "+" : ""}{signal.score.toFixed(2)}
          </span>
          <p className={`text-xs mt-1 ${riskCfg.color}`}>{riskCfg.label}</p>
        </div>
      </div>

      {signal.signal && (
        <div className="mt-3 pt-3 border-t border-white/10">
          <div className="flex items-center gap-4 flex-wrap">
            <div>
              <span className="text-xs text-gray-500 uppercase">Signal</span>
              <p className={`font-semibold ${
                signal.signal.direction === "buy" ? "text-green-400" : "text-red-400"
              }`}>
                {signal.signal.direction.toUpperCase()} — {Math.round(signal.signal.confidence * 100)}% confidence
              </p>
            </div>
            {signal.signal.top_assets && signal.signal.top_assets.length > 0 && (
              <div>
                <span className="text-xs text-gray-500 uppercase">Assets</span>
                <div className="flex gap-1 mt-1">
                  {signal.signal.top_assets.map((asset) => (
                    <span key={asset} className="px-2 py-0.5 bg-blue-500/20 text-blue-300 rounded text-xs">
                      {asset}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {signal.signal.reason && (
              <div>
                <span className="text-xs text-gray-500 uppercase">Reason</span>
                <p className="text-sm text-gray-300 mt-1">{signal.signal.reason}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Category breakdown */}
      {signal.category_breakdown && Object.keys(signal.category_breakdown).length > 0 && (
        <div className="mt-3 flex gap-2 flex-wrap">
          {Object.entries(signal.category_breakdown).map(([cat, count]) => (
            <span key={cat} className={`px-2 py-0.5 rounded text-xs ${CATEGORY_COLORS[cat] || CATEGORY_COLORS.general}`}>
              {cat} ({count})
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function ArticleCard({ article }: { article: Article }) {
  const cfg = SENTIMENT_CONFIG[article.sentiment_label];
  const SentimentIcon = cfg.icon;

  const [expanded, setExpanded] = useState(false);

  const timeAgo = article.published_at
    ? new Date(article.published_at).toLocaleString("th-TH", { hour: "2-digit", minute: "2-digit", day: "numeric", month: "short" })
    : "ไม่ระบุเวลา";

  return (
    <div className={`rounded-lg border p-4 ${cfg.bg} ${cfg.border} transition-colors hover:border-opacity-60`}>
      <div className="flex gap-3">
        {/* Sentiment indicator */}
        <div className="flex flex-col items-center gap-1 pt-0.5">
          <SentimentIcon className={`w-4 h-4 ${cfg.color}`} />
          <span className={`text-xs font-medium ${cfg.color}`}>
            {article.sentiment_score > 0 ? "+" : ""}{article.sentiment_score.toFixed(2)}
          </span>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <span className="text-xs text-gray-500">{article.source}</span>
            <span className="text-xs text-gray-600">•</span>
            <span className="text-xs text-gray-500">{timeAgo}</span>
            <span className={`px-1.5 py-0.5 rounded text-xs ${CATEGORY_COLORS[article.category] || CATEGORY_COLORS.general}`}>
              {article.category}
            </span>
          </div>

          <h3
            className="font-medium text-white leading-snug cursor-pointer"
            onClick={() => setExpanded(!expanded)}
          >
            {article.title}
          </h3>

          {expanded && article.summary && (
            <p className="mt-2 text-sm text-gray-400 leading-relaxed">{article.summary}</p>
          )}

          <div className="mt-2 flex items-center justify-between">
            <div className="flex gap-1 flex-wrap">
              {article.impact_tags?.map((tag) => (
                <span key={tag} className="px-1.5 py-0.5 bg-gray-700/50 text-gray-400 rounded text-xs">
                  {tag}
                </span>
              ))}
            </div>
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-xs text-blue-400 hover:text-blue-300"
              onClick={(e) => e.stopPropagation()}
            >
              อ่านต่อ <ChevronRight className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NewsFeed;
