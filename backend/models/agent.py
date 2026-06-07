from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AgentToolDescriptor(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    label: str
    description: str
    source: str
    default_enabled: bool = True


class AgentRunRequest(BaseModel):
    selected_tools: list[str] = Field(default_factory=list)


class AgentRecommendation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    detail: str
    priority: Literal["high", "medium", "low"]
    signal: str


class AgentDataSource(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source: str
    connected: bool
    items_found: int = 0
    mode: Literal["db", "mock", "mixed", "live", "fallback"] | None = None


class AgentSummary(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tuali_cliente_id: str
    store_name: str
    headline: str
    ticket_average: float | None = None
    goal_progress: float | None = None
    critical_stock_count: int = 0
    stagnant_product_count: int = 0
    available_promotions_count: int = 0
    loyalty_points: int | None = None
    recommendation_count: int = 0


class AgentRunResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    status: Literal["success"]
    message: str
    summary: AgentSummary
    recommendations: list[AgentRecommendation]
    priority_actions: list[AgentRecommendation]
    data_sources: list[AgentDataSource]
    voice_text: str


class StoredRecommendation(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tuali_cliente_id: str
    title: str
    detail: str
    priority: Literal["high", "medium", "low"]
    signal: str
    created_at: datetime | str | None = None
    run_id: str | None = None
    source_model: str | None = None
