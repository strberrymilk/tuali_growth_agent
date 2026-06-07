"""Vercel entrypoint for FastAPI application."""

from pathlib import Path
import sys


CURRENT_DIR = Path(__file__).resolve().parent

if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

try:
    from .main import app
except ImportError:
    from main import app

__all__ = ["app"]
