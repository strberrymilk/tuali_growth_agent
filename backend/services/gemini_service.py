from __future__ import annotations

import json
import os
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import BaseModel, ConfigDict, Field

from agent.prompts import build_growth_prompt
from models import AgentRecommendation


load_dotenv()

class GeminiStructuredResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    message: str
    headline: str
    recommendations: list[AgentRecommendation] = Field(default_factory=list)
    priority_actions: list[AgentRecommendation] = Field(default_factory=list)
    voice_text: str


class GeminiSynthesisResult(BaseModel):
    mode: Literal["live", "fallback"]
    payload: GeminiStructuredResponse
    reason: str | None = None
    model_id: str | None = None


class GeminiChatResult(BaseModel):
    mode: Literal["live", "fallback"]
    message: str
    reason: str | None = None
    model_id: str | None = None


GEMINI_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "required": ["message", "headline", "recommendations", "priority_actions", "voice_text"],
    "properties": {
        "message": {"type": "STRING"},
        "headline": {"type": "STRING"},
        "voice_text": {"type": "STRING"},
        "recommendations": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "required": ["title", "detail", "priority", "signal"],
                "properties": {
                    "title": {"type": "STRING"},
                    "detail": {"type": "STRING"},
                    "priority": {"type": "STRING", "enum": ["high", "medium", "low"]},
                    "signal": {"type": "STRING"},
                },
            },
        },
        "priority_actions": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "required": ["title", "detail", "priority", "signal"],
                "properties": {
                    "title": {"type": "STRING"},
                    "detail": {"type": "STRING"},
                    "priority": {"type": "STRING", "enum": ["high", "medium", "low"]},
                    "signal": {"type": "STRING"},
                },
            },
        },
    },
}


def synthesize_growth_response(
    context: dict[str, Any],
    fallback_payload: GeminiStructuredResponse,
) -> GeminiSynthesisResult:
    gemini_api_key = _get_gemini_api_key()
    gemini_model_id = _get_gemini_model_id()

    if not gemini_api_key:
        return GeminiSynthesisResult(
            mode="fallback",
            payload=fallback_payload,
            reason="missing_api_key",
        )

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return GeminiSynthesisResult(
            mode="fallback",
            payload=fallback_payload,
            reason="sdk_not_installed",
        )

    try:
        prompt = build_growth_prompt(context)
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model=gemini_model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
                response_schema=GEMINI_RESPONSE_SCHEMA,
            ),
        )

        raw_text = response.text or ""
        if not raw_text.strip():
            raise ValueError("empty_response")

        parsed = json.loads(raw_text)
        payload = GeminiStructuredResponse.model_validate(parsed)
        payload = _merge_with_fallback(payload, fallback_payload)

        return GeminiSynthesisResult(
            mode="live",
            payload=payload,
            model_id=gemini_model_id,
        )
    except Exception as error:
        return GeminiSynthesisResult(
            mode="fallback",
            payload=fallback_payload,
            reason=error.__class__.__name__,
            model_id=gemini_model_id,
        )


def chat_with_growth_context(
    *,
    tuali_cliente_id: str,
    report_context: dict[str, Any],
    user_message: str,
    history: list[dict[str, str]] | None = None,
) -> GeminiChatResult:
    gemini_api_key = _get_gemini_api_key()
    gemini_model_id = _get_gemini_model_id()

    if not gemini_api_key:
        return GeminiChatResult(
            mode="fallback",
            message=_build_chat_fallback(report_context, user_message),
            reason="missing_api_key",
        )

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        return GeminiChatResult(
            mode="fallback",
            message=_build_chat_fallback(report_context, user_message),
            reason="sdk_not_installed",
        )

    try:
        from agent.prompts import build_growth_chat_prompt

        prompt = build_growth_chat_prompt(
            tuali_cliente_id=tuali_cliente_id,
            report_context=report_context,
            user_message=user_message,
            history=history,
        )
        client = genai.Client(api_key=gemini_api_key)
        response = client.models.generate_content(
            model=gemini_model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.5,
            ),
        )

        text = (response.text or "").strip()
        if not text:
            raise ValueError("empty_response")

        return GeminiChatResult(
            mode="live",
            message=text,
            model_id=gemini_model_id,
        )
    except Exception as error:
        return GeminiChatResult(
            mode="fallback",
            message=_build_chat_fallback(report_context, user_message),
            reason=error.__class__.__name__,
            model_id=gemini_model_id,
        )


def _merge_with_fallback(
    payload: GeminiStructuredResponse,
    fallback_payload: GeminiStructuredResponse,
) -> GeminiStructuredResponse:
    recommendations = payload.recommendations or fallback_payload.recommendations
    priority_actions = payload.priority_actions or recommendations[:3] or fallback_payload.priority_actions

    return GeminiStructuredResponse(
        message=payload.message or fallback_payload.message,
        headline=payload.headline or fallback_payload.headline,
        recommendations=recommendations,
        priority_actions=priority_actions,
        voice_text=payload.voice_text or fallback_payload.voice_text,
    )


def _get_gemini_api_key() -> str:
    return os.getenv("GEMINI_API_KEY", "").strip()


def _get_gemini_model_id() -> str:
    return os.getenv("GEMINI_MODEL_ID", "gemini-2.5-flash").strip() or "gemini-2.5-flash"


def _build_chat_fallback(report_context: dict[str, Any], user_message: str) -> str:
    summary = report_context.get("summary", {}) if isinstance(report_context, dict) else {}
    recommendations = report_context.get("recommendations", []) if isinstance(report_context, dict) else []
    store_name = summary.get("store_name", "tu tienda")
    headline = summary.get("headline")

    if recommendations:
        first = recommendations[0]
        title = first.get("title", "una prioridad importante") if isinstance(first, dict) else "una prioridad importante"
        return (
            f"Tomando en cuenta el reporte de {store_name}, mi mejor recomendacion sobre '{user_message}' "
            f"es empezar por {title}. {headline or 'Si quieres, puedo ayudarte a aterrizarlo en pasos concretos.'}"
        )

    return (
        f"Con lo que veo en el reporte de {store_name}, puedo ayudarte con '{user_message}', "
        "pero necesito un poco mas de contexto para responder con precision."
    )
