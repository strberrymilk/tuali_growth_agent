from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class StoreProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")

    store_name: str = "Negocio Tuali"
    segment: str | None = None
    city: str | None = None


class Promotion(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str
    description: str
    category_focus: list[str] = Field(default_factory=list)


class LoyaltyStatus(BaseModel):
    model_config = ConfigDict(extra="ignore")

    program_name: str
    points_balance: int = 0
    tier: str | None = None
    next_reward: str | None = None


class ActiveGoal(BaseModel):
    model_config = ConfigDict(extra="ignore")

    goal_name: str = "Meta diaria de ventas"
    metric: str = "ventas"
    target_value: float = 0
    period: str = "daily"
    currency: str = "MXN"
