from __future__ import annotations

from fastapi import APIRouter, Body, Query

from agent.recommendation_service import run_allie_agent
from mcp.tools import get_mcp_tools, get_recommendations
from models import AgentChatRequest, AgentChatResponse, AgentRunRequest, AgentRunResponse, StoredRecommendation
from services.gemini_service import chat_with_growth_context


router = APIRouter(prefix="/agent", tags=["agent"])


@router.get("/tools")
def list_agent_tools() -> dict[str, list[dict[str, str | bool]]]:
    return {"tools": [tool.model_dump() for tool in get_mcp_tools()]}


@router.post("/run/{tuali_cliente_id}", response_model=AgentRunResponse)
def run_agent(
    tuali_cliente_id: str,
    payload: AgentRunRequest | None = Body(default=None),
) -> AgentRunResponse:
    selected_tools = payload.selected_tools if payload else None
    return run_allie_agent(tuali_cliente_id, selected_tools)


@router.post("/chat/{tuali_cliente_id}", response_model=AgentChatResponse)
def chat_with_agent(
    tuali_cliente_id: str,
    payload: AgentChatRequest,
) -> AgentChatResponse:
    result = chat_with_growth_context(
        tuali_cliente_id=tuali_cliente_id,
        report_context=payload.report_context,
        user_message=payload.message,
        history=[message.model_dump() for message in payload.history],
    )

    return AgentChatResponse(
        status="success",
        message=result.message,
        source_mode=result.mode,
        model_id=result.model_id,
    )


@router.get("/recommendations/{tuali_cliente_id}", response_model=list[StoredRecommendation])
def list_recommendations(
    tuali_cliente_id: str,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[StoredRecommendation]:
    return get_recommendations(tuali_cliente_id, limit=limit)
