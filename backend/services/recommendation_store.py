from __future__ import annotations

import os
from datetime import datetime, timezone

from pymongo.errors import PyMongoError

from backend.database.mongo import get_tuali_collection
from backend.models import AgentRecommendation, StoredRecommendation


RECOMMENDATIONS_COLLECTION = (
    os.getenv("ALLIE_RECOMMENDATIONS_COLLECTION", "allie_recommendations").strip()
    or "allie_recommendations"
)


def save_recommendation(
    tuali_cliente_id: str,
    recommendation: AgentRecommendation,
    *,
    run_id: str | None = None,
    source_model: str | None = None,
) -> StoredRecommendation | None:
    record = StoredRecommendation(
        tuali_cliente_id=tuali_cliente_id,
        title=recommendation.title,
        detail=recommendation.detail,
        priority=recommendation.priority,
        signal=recommendation.signal,
        created_at=datetime.now(timezone.utc),
        run_id=run_id,
        source_model=source_model,
    )

    try:
        collection = get_tuali_collection(RECOMMENDATIONS_COLLECTION)
        collection.insert_one(record.model_dump(mode="json"))
        return record
    except (ValueError, PyMongoError):
        return None


def get_recommendations(tuali_cliente_id: str, limit: int = 20) -> list[StoredRecommendation]:
    try:
        collection = get_tuali_collection(RECOMMENDATIONS_COLLECTION)
        documents = list(
            collection.find({"tuali_cliente_id": tuali_cliente_id}, {"_id": 0})
            .sort("created_at", -1)
            .limit(limit)
        )
        return [StoredRecommendation.model_validate(document) for document in documents]
    except (ValueError, PyMongoError):
        return []
