#!/bin/bash
# ============================================================
# Auto Trade AI — Startup Script
# ============================================================
# รันทั้ง Backend (FastAPI) และ Frontend (Next.js)
#
# วิธีใช้:
#   ./run.sh              # รันทั้งสอง
#   ./run.sh --api        # รันเฉพาะ API
#   ./run.sh --frontend   # รันเฉพาะ Frontend
#
# ต้องติดตั้ง dependencies ก่อน:
#   pip install -r api/requirements.txt
#   cd frontend && npm install
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODE="${1:-all}"

echo "========================================"
echo "  Auto Trade AI — Starting"
echo "========================================"

# ตรวจสอบ Python dependencies
if ! python3 -c "import fastapi" 2>/dev/null; then
    echo "[!] Installing Python API dependencies..."
    pip install -q -r api/requirements.txt
fi

# ── Start API Server ───────────────────────────────────────
start_api() {
    echo "[+] Starting API Server on http://localhost:8000"
    echo "[+] API Docs: http://localhost:8000/docs"
    echo "[+] Health:   http://localhost:8000/api/health"
    cd "$SCRIPT_DIR"
    python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
}

# ── Start Frontend ─────────────────────────────────────────
start_frontend() {
    echo "[+] Starting Frontend on http://localhost:3000"
    cd "$SCRIPT_DIR/frontend"
    npm run dev
}

# ── Run ───────────────────────────────────────────────────
case "$MODE" in
    --api)
        start_api
        ;;
    --frontend)
        start_frontend
        ;;
    *)
        # รันทั้งสองใน background
        start_api &
        API_PID=$!
        sleep 3
        start_frontend &
        FRONTEND_PID=$!

        echo ""
        echo "========================================"
        echo "  Auto Trade AI is running!"
        echo "  API:   http://localhost:8000"
        echo "  Docs:  http://localhost:8000/docs"
        echo "  Front: http://localhost:3000"
        echo "========================================"
        echo "Press Ctrl+C to stop all services"
        echo ""

        # รอ interrupt
        trap "kill $API_PID $FRONTEND_PID 2>/dev/null; echo '[*] Stopped'; exit 0" SIGINT SIGTERM
        wait
        ;;
esac
