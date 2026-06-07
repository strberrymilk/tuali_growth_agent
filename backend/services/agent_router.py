from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any

# Importamos los servicios que ya tienes listos
from backend.services.yomp_service import obtener_todo_el_contexto
from backend.services.gemini_services import GeminiService
from backend.services.tts_service import generate_elevenlabs_speech_bytes
from fastapi.responses import Response

router = APIRouter(prefix="/agent", tags=["growth-agent"])

# Instanciamos el servicio de Gemini una sola vez al arrancar
gemini_ai = GeminiService()

class ChatRequest(BaseModel):
    tuali_cliente_id: str
    mensaje_usuario: str

@router.post("/chat")
def interactuar_con_agente(payload: ChatRequest):
    """
    Endpoint principal del Hackathon: Recibe la duda del tendero, 
    extrae el contexto real de MongoDB, consulta a Gemini y devuelve 
    las recomendaciones estructuradas junto con el texto listo para audio.
    """
    # 1. Obtener el super-diccionario con los datos reales de MongoDB
    contexto_tienda = obtener_todo_el_contexto(payload.tuali_cliente_id)
    
    if not contexto_tienda:
        raise HTTPException(status_code=404, detail="No se encontró contexto para este cliente.")
        
    # 2. Mandar los datos de la DB y la pregunta a Gemini
    # Gracias a tu JSON maestro, esto devuelve un diccionario con 'gancho', 'recomendaciones' y 'promo_activa'
    analisis_json = gemini_ai.analizar_datos_tienda(payload.mensaje_usuario, contexto_tienda)
    
    return {
        "status": "success",
        "tuali_cliente_id": payload.tuali_cliente_id,
        "agente_analisis": analisis_json  # Aquí va el JSON estructurado con las tarjetas para el Frontend
    }
