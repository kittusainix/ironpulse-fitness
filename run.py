"""
IronPulse Full-Stack Server Entrypoint
Runs the modular 3-tier architecture: frontend, backend, and db.

Usage (local):
    python run.py

Usage (Vercel):
    Vercel imports `app` from this module automatically via vercel.json
"""
import sys
import os
from pathlib import Path

# Add project root and module directories to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "backend"))
sys.path.insert(0, str(ROOT_DIR / "db"))

from backend.app import app  # noqa: E402 — `app` must be module-level for Vercel

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    print("=" * 64)
    print("  IRONPULSE FITNESS MANAGEMENT SYSTEM")
    print("  Frontend : ./frontend  (templates & static)")
    print("  Backend  : ./backend   (app.py & config.py)")
    print("  Database : ./db        (db.py, SQLite, PL/SQL)")
    print(f"  Server   : http://127.0.0.1:{port}")
    print("=" * 64)
    app.run(debug=debug, host="0.0.0.0", port=port)
