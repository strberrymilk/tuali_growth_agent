import json
from pathlib import Path
from typing import Any

from pymongo.errors import PyMongoError

from backend.database.mongo import get_company_one_collection


MOCK_DATA_PATH = Path(__file__).resolve().parents[2] / "mock_data" / "yomp_mock.json"


def _load_mock_data() -> dict[str, Any]:
    with MOCK_DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _get_mock_client_data(tuali_cliente_id: str) -> dict[str, Any] | None:
    data = _load_mock_data()
    return data.get(tuali_cliente_id)


def _safe_find_many(collection_name: str, tuali_cliente_id: str) -> list[dict[str, Any]]:
    try:
        collection = get_company_one_collection(collection_name)
        documents = list(collection.find({"tuali_cliente_id": tuali_cliente_id}, {"_id": 0}))
        if documents:
            return documents
    except (ValueError, PyMongoError):
        pass
    return []


def _safe_find_one(collection_name: str, tuali_cliente_id: str) -> dict[str, Any] | None:
    try:
        collection = get_company_one_collection(collection_name)
        document = collection.find_one({"tuali_cliente_id": tuali_cliente_id}, {"_id": 0})
        if document:
            return document
    except (ValueError, PyMongoError):
        pass
    return None


def get_yomp_transactions(tuali_cliente_id: str) -> list[dict[str, Any]]:
    mongo_data = _safe_find_many("transacciones_caja", tuali_cliente_id)
    if mongo_data:
        return mongo_data

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return []
    return mock_client.get("transacciones_caja", [])


def get_yomp_inventory(tuali_cliente_id: str) -> dict[str, Any] | None:
    mongo_data = _safe_find_one("inventario_tienda", tuali_cliente_id)
    if mongo_data:
        return mongo_data

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return None
    return mock_client.get("inventario_tienda")


def get_yomp_daily_sales_report(tuali_cliente_id: str) -> dict[str, Any] | None:
    mongo_data = _safe_find_one("reporte_ventas_diario", tuali_cliente_id)
    if mongo_data:
        return mongo_data

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return None
    return mock_client.get("reporte_ventas_diario")


def get_yomp_daily_product_report(tuali_cliente_id: str) -> dict[str, Any] | None:
    mongo_data = _safe_find_one("reporte_producto_diario", tuali_cliente_id)
    if mongo_data:
        return mongo_data

    mock_client = _get_mock_client_data(tuali_cliente_id)
    if not mock_client:
        return None
    return mock_client.get("reporte_producto_diario")


def get_yomp_growth_context(tuali_cliente_id: str) -> dict[str, Any] | None:
    daily_sales = get_yomp_daily_sales_report(tuali_cliente_id)
    inventory = get_yomp_inventory(tuali_cliente_id)
    daily_products = get_yomp_daily_product_report(tuali_cliente_id)

    if not daily_sales or not inventory or not daily_products:
        return None

    critical_stock = [
        {
            "nombre": product["nombre"],
            "stock_actual": product["stock_actual"],
            "stock_minimo": product["stock_minimo"],
        }
        for product in inventory.get("productos", [])
        if product.get("stock_actual", 0) <= product.get("stock_minimo", 0)
    ]

    opportunities: list[str] = []
    if critical_stock:
        opportunities.append("Reabastecer productos con stock critico.")
    if daily_products.get("productos_estancados"):
        opportunities.append("Impulsar productos estancados con promociones.")
    if daily_products.get("productos_mas_vendidos") and daily_products.get("resumen_categorias"):
        opportunities.append("Crear combos entre categorias de alta rotacion.")

    return {
        "source": "yomp_mock",
        "connected": True,
        "tuali_cliente_id": tuali_cliente_id,
        "daily_sales": {
            "total_venta_dinero": daily_sales.get("total_venta_dinero", 0),
            "ticket_promedio_dia": daily_sales.get("ticket_promedio_dia", 0),
            "total_tickets_emitidos": daily_sales.get("total_tickets_emitidos", 0),
            "meta_progreso_porcentaje": daily_sales.get("meta_progreso_porcentaje", 0),
        },
        "payment_methods": daily_sales.get("metodos_pago_resumen", {}),
        "top_products": daily_products.get("productos_mas_vendidos", []),
        "stagnant_products": daily_products.get("productos_estancados", []),
        "critical_stock": critical_stock,
        "category_summary": daily_products.get("resumen_categorias", []),
        "detected_opportunities": opportunities,
    }
