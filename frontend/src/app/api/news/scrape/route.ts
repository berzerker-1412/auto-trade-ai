"use server";

import { NextRequest } from "next/server";

const API_BASE = process.env.API_BASE || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    const res = await fetch(`${API_BASE}/api/news/scrape`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    const data = await res.json();
    return Response.json(data);
  } catch {
    return Response.json({ error: "Scrape failed" }, { status: 500 });
  }
}
