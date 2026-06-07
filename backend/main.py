from fastapi import FastAPI

from backend.api.tts import router as tts_router
from backend.api.yomp import router as yomp_router


app = FastAPI(title="Tuali Growth Agent API", version="0.1.0")
app.include_router(tts_router)
app.include_router(yomp_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
