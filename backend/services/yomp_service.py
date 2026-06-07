from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from pymongo.errors import PyMongoError

from backend.database.mongo import get_yomp_collection
from backend.models import (
    YompCriticalStock,
    YompDailyProductReport,
    YompDailySalesMetrics,
    YompDailySalesReport,
    YompGrowthContext,
    YompInventory,
    YompStagnantProduct,
    YompTopProduct,
    YompTransaction,
)


MOCK_DATA_PATH = Path(__file__).resolve().parents[2] / "mock_data" / "yomp_mock.json"

TRANSACTIONS_COLLECTION = os.getenv("YOMP_TRANSACTIONS_COLLECTION", "transacciones_caja").strip() or "transacciones_caja"
INVENTORY_COLLECTION = os.getenv("YOMP_INVENTORY_COLLECTION", "inventario_tienda").strip() or "inventario_tienda"
DAILY_SALES_COLLECTION = os.getenv("YOMP_DAILY_SALES_COLLECTION", "reporte_ventas_diario").strip() or "reporte_ventas_diario"
DAILY_PRODUCTS_COLLECTION = os.getenv("YOMP_DAILY_PRODUCTS_COLLECTION", "reporte_producto_diario").strip() or "reporte_producto_diario"
YOMP_CLIENT_ID_FIELD = os.getenv("YOMP_CLIENT_ID_FIELD", "").strip()
FALLBACK_CLIENT_ID_FIELDS = [
    "tuali_cliente_id",
    "cliente_id",
    "merchant_id",
    "store_id",
    "client_id",
]


def _load_mock_data() -> dict[str, Any]:
    if not MOCK_DATA_PATH.exists():
        return {}

    with MOCK_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _get_mock_client_data(tuali_cliente_id: str) -> dict[str, Any] | None:
    data = _load_mock_data()
    return data.get(tuali_cliente_id)


def _build_client_query(tuali_cliente_id: str) -> dict[str, Any]:
    if YOMP_CLIENT_ID_FIELD:
        return {YOMP_CLIENT_ID_FIELD: tuali_cliente_id}

    return {
        "$or": [{field: tuali_cliente_id} for field in FALLBACK_CLIENT_ID_FIELDS],
    }


def _safe_find_many(collection_name: str, tuali_cliente_id: str) -> tuple[list[dict[str, Any]], str]:
    try:
        collection = get_yomp_collection(collection_name)
        documents = list(collection.find(_build_client_query(tuali_cliente_id), {"_id": 0}))
        if documents:
            return documents, "db"
    except (ValueError, PyMongoError):
        pass
    return [], "mock"


def _safe_find_one(collection_name: str, tuali_cliente_id: str) -> tuple[dict[str, Any] | None, str]:
    try:
        collection = get_yomp_collection(collection_name)
        document = collection.find_one(_build_client_query(tuali_cliente_id), {"_id": 0})
        if document:
            return document, "db"
    except (ValueError, PyMongoError):
        pass
    return None, "mock"


def _get_transactions_with_source(tuali_cliente_id: str) -> tuple[list[YompTransaction], str]:
    mongo_data, source = _safe_find_many(TRANSACTIONS_COLLECTION, tuali_cliente_id)
    if mongo_data:
        return [YompTransaction.model_validate(document) for document in mongo_data], source

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return [], "mock"

    return [
        YompTransaction.model_validate(document)
        for document in mock_client.get("transacciones_caja", [])
    ], "mock"


def _get_inventory_with_source(tuali_cliente_id: str) -> tuple[YompInventory | None, str]:
    mongo_data, source = _safe_find_one(INVENTORY_COLLECTION, tuali_cliente_id)
    if mongo_data:
        return YompInventory.model_validate(mongo_data), source

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return None, "mock"

    inventory = mock_client.get("inventario_tienda")
    if not inventory:
        return None, "mock"

    return YompInventory.model_validate(inventory), "mock"


def _get_daily_sales_with_source(tuali_cliente_id: str) -> tuple[YompDailySalesReport | None, str]:
    mongo_data, source = _safe_find_one(DAILY_SALES_COLLECTION, tuali_cliente_id)
    if mongo_data:
        return YompDailySalesReport.model_validate(mongo_data), source

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return None, "mock"

    report = mock_client.get("reporte_ventas_diario")
    if not report:
        return None, "mock"

    return YompDailySalesReport.model_validate(report), "mock"


def _get_daily_product_report_with_source(
    tuali_cliente_id: str,
) -> tuple[YompDailyProductReport | None, str]:
    mongo_data, source = _safe_find_one(DAILY_PRODUCTS_COLLECTION, tuali_cliente_id)
    if mongo_data:
        return YompDailyProductReport.model_validate(mongo_data), source

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return None, "mock"

    report = mock_client.get("reporte_producto_diario")
    if not report:
        return None, "mock"

    return YompDailyProductReport.model_validate(report), "mock"


def get_yomp_transactions(tuali_cliente_id: str) -> list[YompTransaction]:
    transactions, _ = _get_transactions_with_source(tuali_cliente_id)
    return transactions


def get_yomp_inventory(tuali_cliente_id: str) -> YompInventory | None:
    inventory, _ = _get_inventory_with_source(tuali_cliente_id)
    return inventory


def get_yomp_daily_sales_report(tuali_cliente_id: str) -> YompDailySalesReport | None:
    report, _ = _get_daily_sales_with_source(tuali_cliente_id)
    return report


def get_yomp_daily_product_report(tuali_cliente_id: str) -> YompDailyProductReport | None:
    report, _ = _get_daily_product_report_with_source(tuali_cliente_id)
    return report


def get_yomp_growth_context(tuali_cliente_id: str) -> YompGrowthContext | None:
    daily_sales, daily_sales_source = _get_daily_sales_with_source(tuali_cliente_id)
    inventory, inventory_source = _get_inventory_with_source(tuali_cliente_id)
    daily_products, daily_products_source = _get_daily_product_report_with_source(tuali_cliente_id)

    if not daily_sales or not inventory or not daily_products:
        return None

    critical_stock = [
        YompCriticalStock(
            nombre=product.nombre,
            stock_actual=product.stock_actual,
            stock_minimo=product.stock_minimo,
        )
        for product in inventory.productos
        if product.stock_actual <= product.stock_minimo
    ]

    opportunities: list[str] = []
    if critical_stock:
        opportunities.append("Reabastecer productos con stock critico.")
    if daily_products.productos_estancados:
        opportunities.append("Impulsar productos estancados con promociones.")
    if daily_products.productos_mas_vendidos and daily_products.resumen_categorias:
        opportunities.append("Crear combos entre categorias de alta rotacion.")

    source_modes = {daily_sales_source, inventory_source, daily_products_source}
    if source_modes == {"db"}:
        source = "yomp_db"
        connected = True
    elif "db" in source_modes:
        source = "yomp_mixed"
        connected = True
    else:
        source = "yomp_mock"
        connected = False

    return YompGrowthContext(
        source=source,
        connected=connected,
        tuali_cliente_id=tuali_cliente_id,
        daily_sales=YompDailySalesMetrics(
            total_venta_dinero=daily_sales.total_venta_dinero,
            ticket_promedio_dia=daily_sales.ticket_promedio_dia,
            total_tickets_emitidos=daily_sales.total_tickets_emitidos,
            meta_progreso_porcentaje=daily_sales.meta_progreso_porcentaje,
        ),
        payment_methods=daily_sales.metodos_pago_resumen,
        top_products=[
            YompTopProduct.model_validate(product.model_dump())
            for product in daily_products.productos_mas_vendidos
        ],
        stagnant_products=[
            YompStagnantProduct.model_validate(product.model_dump())
            for product in daily_products.productos_estancados
        ],
        critical_stock=critical_stock,
        category_summary=daily_products.resumen_categorias,
        detected_opportunities=opportunities,
    )
