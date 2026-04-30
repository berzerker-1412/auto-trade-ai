"use server";

import { NextRequest } from "next/server";

const API_BASE = process.env.API_BASE || "http://localhost:8000";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const limit = searchParams.get("limit") || "50";
  const category = searchParams.get("category");
  
  let url = `${API_BASE}/api/news/feed?limit=${limit}`;
  if (category) url += `&category=${category}`;
  
  try {
    const res = await fetch(url, { next: { revalidate: 60 } });
    const data = await res.json();
    return Response.json(data);
  } catch {
    return Response.json({ articles: [], total: 0, error: "Failed to fetch" }, { status: 500 });
  }
}
