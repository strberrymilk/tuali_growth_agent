from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.services.yomp_service import (
    get_yomp_daily_product_report,
    get_yomp_daily_sales_report,
    get_yomp_growth_context,
    get_yomp_inventory,
    get_yomp_transactions,
)


router = APIRouter(prefix="/yomp", tags=["yomp"])


@router.get("/{tuali_cliente_id}/transactions")
def read_transactions(tuali_cliente_id: str) -> list[dict]:
    data = get_yomp_transactions(tuali_cliente_id)
    if not data:
        raise HTTPException(status_code=404, detail="No Yomp transactions found for this client.")
    return [transaction.model_dump(mode="json") for transaction in data]


@router.get("/{tuali_cliente_id}/inventory")
def read_inventory(tuali_cliente_id: str) -> dict:
    data = get_yomp_inventory(tuali_cliente_id)
    if not data:
        raise HTTPException(status_code=404, detail="No Yomp inventory found for this client.")
    return data.model_dump(mode="json")


@router.get("/{tuali_cliente_id}/daily-sales")
def read_daily_sales(tuali_cliente_id: str) -> dict:
    data = get_yomp_daily_sales_report(tuali_cliente_id)
    if not data:
        raise HTTPException(status_code=404, detail="No Yomp daily sales report found for this client.")
    return data.model_dump(mode="json")


@router.get("/{tuali_cliente_id}/daily-products")
def read_daily_products(tuali_cliente_id: str) -> dict:
    data = get_yomp_daily_product_report(tuali_cliente_id)
    if not data:
        raise HTTPException(status_code=404, detail="No Yomp daily product report found for this client.")
    return data.model_dump(mode="json")


@router.get("/{tuali_cliente_id}/growth-context")
def read_growth_context(tuali_cliente_id: str) -> dict:
    data = get_yomp_growth_context(tuali_cliente_id)
    if not data:
        raise HTTPException(status_code=404, detail="No Yomp growth context found for this client.")
    return data.model_dump(mode="json")
