from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class YompTransactionProduct(BaseModel):
    model_config = ConfigDict(extra="ignore")

    codigo_barras: str | None = None
    nombre: str
    categoria: str | None = None
    cantidad: int = 0
    precio_unitario: float = 0


class YompTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tuali_cliente_id: str | None = None
    folio_ticket: str | None = None
    fecha_hora: str | datetime | None = None
    metodo_pago: str | None = None
    productos_vendidos: list[YompTransactionProduct] = Field(default_factory=list)
    total_ticket: float = 0


class YompInventoryProduct(BaseModel):
    model_config = ConfigDict(extra="ignore")

    codigo_barras: str | None = None
    nombre: str
    stock_actual: int = 0
    stock_minimo: int = 0
    precio_venta_publico: float | None = None


class YompInventory(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tuali_cliente_id: str | None = None
    ultima_actualizacion: str | datetime | None = None
    productos: list[YompInventoryProduct] = Field(default_factory=list)


class YompDailySalesReport(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tuali_cliente_id: str | None = None
    fecha: str | date | datetime | None = None
    total_venta_dinero: float = 0
    total_tickets_emitidos: int = 0
    ticket_promedio_dia: float = 0
    metodos_pago_resumen: dict[str, float] = Field(default_factory=dict)
    meta_progreso_porcentaje: float = 0


class YompTopProduct(BaseModel):
    model_config = ConfigDict(extra="ignore")

    nombre: str
    unidades_vendidas: int = 0
    total_ingreso: float = 0


class YompStagnantProduct(BaseModel):
    model_config = ConfigDict(extra="ignore")

    nombre: str
    unidades_sin_movimiento_dias: int = 0


class YompCategorySummary(BaseModel):
    model_config = ConfigDict(extra="ignore")

    categoria: str
    unidades_totales: int = 0
    total_ingreso: float = 0


class YompDailyProductReport(BaseModel):
    model_config = ConfigDict(extra="ignore")

    tuali_cliente_id: str | None = None
    fecha: str | date | datetime | None = None
    productos_mas_vendidos: list[YompTopProduct] = Field(default_factory=list)
    productos_estancados: list[YompStagnantProduct] = Field(default_factory=list)
    resumen_categorias: list[YompCategorySummary] = Field(default_factory=list)


class YompCriticalStock(BaseModel):
    model_config = ConfigDict(extra="ignore")

    nombre: str
    stock_actual: int = 0
    stock_minimo: int = 0


class YompDailySalesMetrics(BaseModel):
    model_config = ConfigDict(extra="ignore")

    total_venta_dinero: float = 0
    ticket_promedio_dia: float = 0
    total_tickets_emitidos: int = 0
    meta_progreso_porcentaje: float = 0


class YompGrowthContext(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source: str
    connected: bool
    tuali_cliente_id: str
    daily_sales: YompDailySalesMetrics
    payment_methods: dict[str, float] = Field(default_factory=dict)
    top_products: list[YompTopProduct] = Field(default_factory=list)
    stagnant_products: list[YompStagnantProduct] = Field(default_factory=list)
    critical_stock: list[YompCriticalStock] = Field(default_factory=list)
    category_summary: list[YompCategorySummary] = Field(default_factory=list)
    detected_opportunities: list[str] = Field(default_factory=list)
