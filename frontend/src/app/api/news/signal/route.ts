"use server";

import { NextRequest } from "next/server";

const API_BASE = process.env.API_BASE || "http://localhost:8000";

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/news/signal`, { next: { revalidate: 300 } });
    const data = await res.json();
    return Response.json(data);
  } catch {
    return Response.json({ error: "Failed to fetch signal" }, { status: 500 });
  }
}
