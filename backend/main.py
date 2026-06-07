from fastapi import FastAPI
from backend.routes.agent_router import router as agent_router
from fastapi.middleware.cors import CORSMiddleware

from backend.api.agent import router as agent_router
from backend.api.tts import router as tts_router
from backend.api.yomp import router as yomp_router


app = FastAPI(title="Tuali Growth Agent API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(agent_router)
app.include_router(tts_router)
app.include_router(yomp_router)
app.include_router(agent_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
