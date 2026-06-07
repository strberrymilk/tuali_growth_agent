from __future__ import annotations

import uuid

from backend.mcp.tools import collect_tool_outputs, save_recommendation
from backend.models import (
    ActiveGoal,
    AgentDataSource,
    AgentRecommendation,
    AgentRunResponse,
    AgentSummary,
    LoyaltyStatus,
    Promotion,
    StoreProfile,
    YompGrowthContext,
)
from backend.services.gemini_service import GeminiStructuredResponse, synthesize_growth_response


LOW_TICKET_THRESHOLD = 65
LOW_GOAL_PROGRESS_THRESHOLD = 85


def run_allie_agent(
    tuali_cliente_id: str,
    selected_tools: list[str] | None = None,
) -> AgentRunResponse:
    tool_outputs, data_sources = collect_tool_outputs(tuali_cliente_id, selected_tools)

    profile: StoreProfile = tool_outputs.get("tuali_profile", StoreProfile())
    promotions: list[Promotion] = tool_outputs.get("available_promotions", [])
    loyalty_status: LoyaltyStatus | None = tool_outputs.get("loyalty_status")
    yomp_context: YompGrowthContext | None = tool_outputs.get("yomp_growth_context")
    active_goal: ActiveGoal | None = tool_outputs.get("active_goal")

    draft_recommendations = _build_rule_based_recommendations(yomp_context, promotions, loyalty_status)
    draft_priority_actions = draft_recommendations[:3]
    draft_summary = _build_summary(
        tuali_cliente_id=tuali_cliente_id,
        profile=profile,
        promotions=promotions,
        loyalty_status=loyalty_status,
        yomp_context=yomp_context,
        recommendation_count=len(draft_recommendations),
    )
    draft_message = _build_message(profile, yomp_context)
    draft_voice_text = _build_voice_text(profile, yomp_context, draft_priority_actions)

    fallback_payload = GeminiStructuredResponse(
        message=draft_message,
        headline=draft_summary.headline,
        recommendations=draft_recommendations,
        priority_actions=draft_priority_actions,
        voice_text=draft_voice_text,
    )

    gemini_result = synthesize_growth_response(
        _build_gemini_context(
            tuali_cliente_id=tuali_cliente_id,
            profile=profile,
            active_goal=active_goal,
            promotions=promotions,
            loyalty_status=loyalty_status,
            yomp_context=yomp_context,
            recommendations=draft_recommendations,
            summary=draft_summary,
        ),
        fallback_payload,
    )

    recommendations = gemini_result.payload.recommendations
    priority_actions = gemini_result.payload.priority_actions[:3]
    summary = draft_summary.model_copy(
        update={
            "headline": gemini_result.payload.headline,
            "recommendation_count": len(recommendations),
        }
    )
    message = gemini_result.payload.message
    voice_text = gemini_result.payload.voice_text

    data_sources.append(
        AgentDataSource(
            source="gemini_synthesis",
            connected=gemini_result.mode == "live",
            items_found=1,
            mode=gemini_result.mode,
        )
    )

    _persist_recommendations(
        tuali_cliente_id=tuali_cliente_id,
        recommendations=recommendations,
        source_model=gemini_result.model_id if gemini_result.mode == "live" else "rule_based_fallback",
    )

    return AgentRunResponse(
        status="success",
        message=message,
        summary=summary,
        recommendations=recommendations,
        priority_actions=priority_actions,
        data_sources=data_sources,
        voice_text=voice_text,
    )


def _build_summary(
    *,
    tuali_cliente_id: str,
    profile: StoreProfile,
    promotions: list[Promotion],
    loyalty_status: LoyaltyStatus | None,
    yomp_context: YompGrowthContext | None,
    recommendation_count: int,
) -> AgentSummary:
    daily_sales = yomp_context.daily_sales if yomp_context else None

    headline = "Analisis generado con datos base de Tuali."
    if yomp_context:
        headline = (
            f"Hoy vendiste ${daily_sales.total_venta_dinero} y llevas "
            f"{daily_sales.meta_progreso_porcentaje}% de tu meta diaria."
        )

    return AgentSummary(
        tuali_cliente_id=tuali_cliente_id,
        store_name=profile.store_name,
        headline=headline,
        ticket_average=daily_sales.ticket_promedio_dia if daily_sales else None,
        goal_progress=daily_sales.meta_progreso_porcentaje if daily_sales else None,
        critical_stock_count=len(yomp_context.critical_stock) if yomp_context else 0,
        stagnant_product_count=len(yomp_context.stagnant_products) if yomp_context else 0,
        available_promotions_count=len(promotions),
        loyalty_points=loyalty_status.points_balance if loyalty_status else None,
        recommendation_count=recommendation_count,
    )


def _build_rule_based_recommendations(
    yomp_context: YompGrowthContext | None,
    promotions: list[Promotion],
    loyalty_status: LoyaltyStatus | None,
) -> list[AgentRecommendation]:
    recommendations: list[AgentRecommendation] = []

    if yomp_context:
        critical_stock = yomp_context.critical_stock
        if critical_stock:
            item = critical_stock[0]
            recommendations.append(
                AgentRecommendation(
                    title=f"Reabastece {item.nombre}",
                    detail=(
                        f"Solo quedan {item.stock_actual} unidades y el minimo sugerido es "
                        f"{item.stock_minimo}."
                    ),
                    priority="high",
                    signal="stock_critico",
                )
            )

        stagnant_products = yomp_context.stagnant_products
        if stagnant_products:
            item = stagnant_products[0]
            recommendations.append(
                AgentRecommendation(
                    title=f"Activa una promo para {item.nombre}",
                    detail=(
                        f"Este producto lleva {item.unidades_sin_movimiento_dias} dias sin movimiento."
                    ),
                    priority="medium",
                    signal="producto_estancado",
                )
            )

        ticket_average = yomp_context.daily_sales.ticket_promedio_dia
        if ticket_average and ticket_average < LOW_TICKET_THRESHOLD:
            combo_categories = _get_combo_categories(yomp_context)
            recommendations.append(
                AgentRecommendation(
                    title="Sube el ticket promedio con combos",
                    detail=(
                        f"Tu ticket promedio esta en ${ticket_average}. "
                        f"Prueba combos de {combo_categories} para aumentar el valor por compra."
                    ),
                    priority="medium",
                    signal="ticket_promedio_bajo",
                )
            )

        goal_progress = yomp_context.daily_sales.meta_progreso_porcentaje
        if goal_progress and goal_progress < LOW_GOAL_PROGRESS_THRESHOLD:
            recommendations.append(
                AgentRecommendation(
                    title="Impulsa ventas para acercarte a la meta",
                    detail=(
                        f"Hoy llevas {goal_progress}% de la meta. "
                        "Conviene destacar promociones y productos de alta rotacion."
                    ),
                    priority="high",
                    signal="progreso_bajo_meta",
                )
            )

        if yomp_context.category_summary and promotions:
            promo = promotions[0]
            recommendations.append(
                AgentRecommendation(
                    title="Aprovecha una oportunidad de combo",
                    detail=(
                        f"Promueve '{promo.title}' para mover categorias con alta rotacion "
                        "y sumar mas ingreso por ticket."
                    ),
                    priority="medium",
                    signal="oportunidad_combo",
                )
            )

    if promotions:
        promo = promotions[0]
        recommendations.append(
            AgentRecommendation(
                title=f"Lanza la promo '{promo.title}'",
                detail=promo.description,
                priority="medium",
                signal="promocion_disponible",
            )
        )

    if loyalty_status and loyalty_status.points_balance >= 1000:
        recommendations.append(
            AgentRecommendation(
                title="Activa una campana para clientes frecuentes",
                detail=(
                    f"Tienes {loyalty_status.points_balance} puntos acumulados en {loyalty_status.program_name}. "
                    "Es buen momento para empujar recompensas o canjes."
                ),
                priority="low",
                signal="fidelidad_lista",
            )
        )

    if not recommendations:
        recommendations.append(
            AgentRecommendation(
                title="Conecta mas herramientas para enriquecer el analisis",
                detail="Allie puede darte mejores recomendaciones al combinar Tuali, Yomp y promociones.",
                priority="low",
                signal="analisis_base",
            )
        )

    return recommendations


def _build_message(profile: StoreProfile, yomp_context: YompGrowthContext | None) -> str:
    store_name = profile.store_name
    if not yomp_context:
        return f"Allie genero un analisis base para {store_name} usando herramientas de Tuali."

    if yomp_context.source == "yomp_db":
        return f"Allie genero un analisis de negocio para {store_name} usando datos reales de Tuali y Yomp."

    if yomp_context.source == "yomp_mixed":
        return (
            f"Allie genero un analisis de negocio para {store_name} con datos parciales de Yomp y "
            "apoyo de datos mock para completar la demo."
        )

    return (
        f"Allie genero un analisis demo para {store_name} usando herramientas de Tuali y "
        "datos mock de Yomp."
    )


def _build_voice_text(
    profile: StoreProfile,
    yomp_context: YompGrowthContext | None,
    priority_actions: list[AgentRecommendation],
) -> str:
    store_name = profile.store_name
    intro = f"Hola. Ya tengo listo el analisis de {store_name}."

    if yomp_context:
        intro = (
            f"Hola. Ya tengo listo el analisis de {store_name}. "
            f"Hoy vendiste {yomp_context.daily_sales.total_venta_dinero} pesos y llevas "
            f"{yomp_context.daily_sales.meta_progreso_porcentaje} por ciento de tu meta diaria."
        )

    action_lines = [action.title for action in priority_actions[:3]]
    if not action_lines:
        return intro

    return f"{intro} Mis prioridades recomendadas son: {'; '.join(action_lines)}."


def _get_combo_categories(yomp_context: YompGrowthContext) -> str:
    categories = [item.categoria for item in yomp_context.category_summary if item.categoria]
    if len(categories) >= 2:
        return f"{categories[0]} y {categories[1]}"
    if categories:
        return categories[0]
    return "tus categorias mas fuertes"


def _build_gemini_context(
    *,
    tuali_cliente_id: str,
    profile: StoreProfile,
    active_goal: ActiveGoal | None,
    promotions: list[Promotion],
    loyalty_status: LoyaltyStatus | None,
    yomp_context: YompGrowthContext | None,
    recommendations: list[AgentRecommendation],
    summary: AgentSummary,
) -> dict:
    return {
        "tuali_cliente_id": tuali_cliente_id,
        "store_profile": profile.model_dump(mode="json"),
        "active_goal": active_goal.model_dump(mode="json") if active_goal else None,
        "promotions": [promotion.model_dump(mode="json") for promotion in promotions],
        "loyalty_status": loyalty_status.model_dump(mode="json") if loyalty_status else None,
        "yomp_growth_context": yomp_context.model_dump(mode="json") if yomp_context else None,
        "summary": summary.model_dump(mode="json"),
        "detected_signals": [recommendation.model_dump(mode="json") for recommendation in recommendations],
    }


def _persist_recommendations(
    *,
    tuali_cliente_id: str,
    recommendations: list[AgentRecommendation],
    source_model: str,
) -> None:
    run_id = str(uuid.uuid4())

    for recommendation in recommendations:
        save_recommendation(
            tuali_cliente_id,
            recommendation,
            run_id=run_id,
            source_model=source_model,
        )
