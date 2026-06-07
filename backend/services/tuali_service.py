from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.models import ActiveGoal, LoyaltyStatus, Promotion, StoreProfile


TUALI_MOCK_DATA_PATH = Path(__file__).resolve().parents[2] / "mock_data" / "tuali_mock.json"


DEFAULT_STORE_PROFILE = StoreProfile(
    store_name="Abarrotes Chabelita",
    segment="Abarrotes",
    city="Mazatlan",
)

DEFAULT_PROMOTIONS = [
    Promotion(
        title="Combo refresco + botana",
        description="Empaqueta refrescos y botanas para elevar el valor por ticket.",
        category_focus=["Refrescos", "Botanas"],
    ),
    Promotion(
        title="Promocion de media tarde",
        description="Activa descuentos ligeros en horas de baja afluencia para mover inventario.",
        category_focus=["Jugos", "Botanas"],
    ),
]

DEFAULT_LOYALTY_STATUS = LoyaltyStatus(
    program_name="Gana Coca-Cola",
    points_balance=1450,
    tier="oro",
    next_reward="Canje por productos Coca-Cola",
)

DEFAULT_ACTIVE_GOAL = ActiveGoal(
    goal_name="Meta diaria de ventas",
    metric="ventas",
    target_value=10800,
    period="daily",
    currency="MXN",
)


def _load_mock_data() -> dict[str, Any]:
    if not TUALI_MOCK_DATA_PATH.exists():
        return {}

    with TUALI_MOCK_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _get_mock_client_data(tuali_cliente_id: str) -> dict[str, Any]:
    data = _load_mock_data()
    return data.get(tuali_cliente_id, {})


def get_store_profile(tuali_cliente_id: str) -> StoreProfile:
    client_data = _get_mock_client_data(tuali_cliente_id)
    raw_profile = client_data.get("store_profile")
    return StoreProfile.model_validate(raw_profile or DEFAULT_STORE_PROFILE.model_dump())


def get_available_promotions(tuali_cliente_id: str) -> list[Promotion]:
    client_data = _get_mock_client_data(tuali_cliente_id)
    raw_promotions = client_data.get("available_promotions")
    if not raw_promotions:
        return DEFAULT_PROMOTIONS

    return [Promotion.model_validate(promotion) for promotion in raw_promotions]


def get_loyalty_status(tuali_cliente_id: str) -> LoyaltyStatus:
    client_data = _get_mock_client_data(tuali_cliente_id)
    raw_status = client_data.get("loyalty_status")
    return LoyaltyStatus.model_validate(raw_status or DEFAULT_LOYALTY_STATUS.model_dump())


def get_active_goal(tuali_cliente_id: str) -> ActiveGoal:
    client_data = _get_mock_client_data(tuali_cliente_id)
    raw_goal = client_data.get("active_goal")
    return ActiveGoal.model_validate(raw_goal or DEFAULT_ACTIVE_GOAL.model_dump())
