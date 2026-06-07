"""Vercel entrypoint for FastAPI application."""

from pathlib import Path
import sys
import traceback

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

_import_error: str | None = None

try:
    from main import app
except Exception:
    _import_error = traceback.format_exc()
    from fastapi import FastAPI

    app = FastAPI(title="Tuali Growth Agent - Boot Error")

    @app.get("/health")
    def health():
        return {"status": "boot_error", "detail": _import_error}

    @app.get("/")
    def root():
        return {"status": "boot_error", "detail": _import_error}

__all__ = ["app"]
