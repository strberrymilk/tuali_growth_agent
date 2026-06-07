from __future__ import annotations

from typing import Any

from models import AgentDataSource, AgentRecommendation, AgentToolDescriptor, YompGrowthContext
from services.recommendation_store import (
    get_recommendations as get_recommendations_from_store,
    save_recommendation as save_recommendation_to_store,
)
from services.tuali_service import (
    get_active_goal as get_active_goal_from_service,
    get_available_promotions as get_available_promotions_from_service,
    get_loyalty_status as get_loyalty_status_from_service,
    get_store_profile as get_store_profile_from_service,
)
from services.yomp_service import get_yomp_growth_context as get_yomp_growth_context_from_service


TOOL_CATALOG = [
    AgentToolDescriptor(
        id="tuali_profile",
        label="Tuali Profile",
        description="Store profile and baseline Tuali business context.",
        source="tuali",
        default_enabled=True,
    ),
    AgentToolDescriptor(
        id="active_goal",
        label="Active Goal",
        description="Current growth goal or sales target for the merchant.",
        source="tuali",
        default_enabled=True,
    ),
    AgentToolDescriptor(
        id="available_promotions",
        label="Available Promotions",
        description="Promotions and combo ideas currently available for the store.",
        source="tuali",
        default_enabled=True,
    ),
    AgentToolDescriptor(
        id="loyalty_status",
        label="Loyalty Status",
        description="Points, tier, and reward readiness for the merchant.",
        source="tuali",
        default_enabled=True,
    ),
    AgentToolDescriptor(
        id="yomp_growth_context",
        label="Yomp Growth Context",
        description="Sales, inventory, and daily product signals from Yomp POS.",
        source="yomp",
        default_enabled=True,
    ),
    AgentToolDescriptor(
        id="save_recommendation",
        label="Save Recommendation",
        description="Persist a generated recommendation for future retrieval.",
        source="tuali",
        default_enabled=False,
    ),
    AgentToolDescriptor(
        id="get_recommendations",
        label="Get Recommendations",
        description="Retrieve previously saved recommendations for the merchant.",
        source="tuali",
        default_enabled=False,
    ),
]


def get_mcp_tools() -> list[AgentToolDescriptor]:
    return TOOL_CATALOG


def resolve_selected_tools(selected_tools: list[str] | None) -> list[str]:
    available_tool_ids = {tool.id for tool in TOOL_CATALOG}
    default_tool_ids = [tool.id for tool in TOOL_CATALOG if tool.default_enabled]

    if not selected_tools:
        return default_tool_ids

    resolved = [tool_id for tool_id in selected_tools if tool_id in available_tool_ids]
    if "active_goal" not in resolved:
        resolved.append("active_goal")

    return resolved or default_tool_ids


def get_tuali_profile(tuali_cliente_id: str):
    return get_store_profile_from_service(tuali_cliente_id)


def get_available_promotions(tuali_cliente_id: str):
    return get_available_promotions_from_service(tuali_cliente_id)


def get_loyalty_status(tuali_cliente_id: str):
    return get_loyalty_status_from_service(tuali_cliente_id)


def get_active_goal(tuali_cliente_id: str):
    return get_active_goal_from_service(tuali_cliente_id)


def get_yomp_growth_context(tuali_cliente_id: str):
    return get_yomp_growth_context_from_service(tuali_cliente_id)


def save_recommendation(
    tuali_cliente_id: str,
    recommendation: AgentRecommendation,
    *,
    run_id: str | None = None,
    source_model: str | None = None,
):
    return save_recommendation_to_store(
        tuali_cliente_id,
        recommendation,
        run_id=run_id,
        source_model=source_model,
    )


def get_recommendations(tuali_cliente_id: str, limit: int = 20):
    return get_recommendations_from_store(tuali_cliente_id, limit=limit)


def collect_tool_outputs(
    tuali_cliente_id: str,
    selected_tools: list[str] | None = None,
) -> tuple[dict[str, Any], list[AgentDataSource]]:
    resolved_tools = resolve_selected_tools(selected_tools)
    outputs: dict[str, Any] = {}
    data_sources: list[AgentDataSource] = []

    if "tuali_profile" in resolved_tools:
        profile = get_tuali_profile(tuali_cliente_id)
        outputs["tuali_profile"] = profile
        data_sources.append(
            AgentDataSource(
                source="tuali_profile",
                connected=True,
                items_found=1,
                mode="mock",
            )
        )

    if "active_goal" in resolved_tools:
        active_goal = get_active_goal(tuali_cliente_id)
        outputs["active_goal"] = active_goal
        data_sources.append(
            AgentDataSource(
                source="active_goal",
                connected=True,
                items_found=1,
                mode="mock",
            )
        )

    if "available_promotions" in resolved_tools:
        promotions = get_available_promotions(tuali_cliente_id)
        outputs["available_promotions"] = promotions
        data_sources.append(
            AgentDataSource(
                source="available_promotions",
                connected=True,
                items_found=len(promotions),
                mode="mock",
            )
        )

    if "loyalty_status" in resolved_tools:
        loyalty_status = get_loyalty_status(tuali_cliente_id)
        outputs["loyalty_status"] = loyalty_status
        data_sources.append(
            AgentDataSource(
                source="loyalty_status",
                connected=True,
                items_found=1,
                mode="mock",
            )
        )

    if "yomp_growth_context" in resolved_tools:
        yomp_context = get_yomp_growth_context(tuali_cliente_id)
        outputs["yomp_growth_context"] = yomp_context
        data_sources.append(_build_yomp_data_source(yomp_context))

    return outputs, data_sources


def _build_yomp_data_source(yomp_context: YompGrowthContext | None) -> AgentDataSource:
    if not yomp_context:
        return AgentDataSource(
            source="yomp_growth_context",
            connected=False,
            items_found=0,
            mode="fallback",
        )

    mode = "mock"
    if yomp_context.source == "yomp_db":
        mode = "db"
    elif yomp_context.source == "yomp_mixed":
        mode = "mixed"

    return AgentDataSource(
        source="yomp_growth_context",
        connected=yomp_context.connected,
        items_found=len(yomp_context.model_dump()),
        mode=mode,
    )
