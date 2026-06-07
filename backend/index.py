"""Vercel entrypoint — minimal diagnostic (no imports from main)."""

from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok", "mode": "minimal_diagnostic"}


@app.get("/")
def root():
    return {"status": "ok"}
