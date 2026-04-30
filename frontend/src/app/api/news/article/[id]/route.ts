import { NextRequest } from "next/server";

const API_BASE = process.env.API_BASE || "http://localhost:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  const { id } = await params;
  try {
    const res = await fetch(`${API_BASE}/api/news/article/${id}`, {
      // @ts-ignore-next-line
      next: { revalidate: 300 },
    });
    if (!res.ok) {
      return Response.json({ error: "Article not found" }, { status: res.status });
    }
    return Response.json(await res.json());
  } catch {
    return Response.json({ error: "Failed to fetch article" }, { status: 500 });
  }
}
