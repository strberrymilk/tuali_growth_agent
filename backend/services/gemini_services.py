import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class GeminiService:
    def __init__(self):
        # 1. Inicializar cliente oficial de Gemini
        self.client = genai.Client()
        
        # 2. Cargar la configuración unificada
        current_dir = os.path.dirname(__file__)
        config_path = os.path.join(current_dir, 'gemini_config.json')
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_data = json.load(f)
            
        self.model_name = self.config_data["gemini_model_settings"]["model_name"]
        self.system_instruction = self.config_data["system_instruction"]
        self.temperature = self.config_data["gemini_model_settings"]["generation_config"]["temperature"]

    def analizar_datos_tienda(self, pregunta_usuario: str, datos_mongodb: dict) -> dict:
        """
        Analiza los datos de MongoDB y entrega un diccionario estructurado (JSON)
        listo para el Frontend y ElevenLabs.
        """
        # Adjuntamos las reglas de salida en el prompt para obligar la estructura exacta del JSON
        prompt_final = f"""
        CONTEXTO REAL DE MONGO DB:
        {json.dumps(datos_mongodb, ensure_ascii=False, default=str)}

        ESTRUCTURA DE RESPUESTA REQUERIDA (JSON):
        {json.dumps(self.config_data["response_schema_definition"], ensure_ascii=False)}

        PREGUNTA DEL TENDERO:
        "{pregunta_usuario}"
        """

        try:
            # 3. Llamada a la API configurando la salida como JSON
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt_final,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=self.temperature,
                    response_mime_type="application/json" # Fuerza a Gemini a responder en JSON
                ),
            )
            
            # 4. Limpieza y parseo seguro del resultado
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text.lstrip("```json").rstrip("```")
            elif raw_text.startswith("```"):
                raw_text = raw_text.lstrip("```").rstrip("```")
                
            return json.loads(raw_text.strip())
            
        except Exception as e:
            # En caso de error, devolvemos una estructura limpia que no rompa el frontend
            return {
                "gancho": f"Lo siento, tuvimos un pequeño contratiempo al analizar los datos: {str(e)}",
                "recomendaciones": [],
                "promo_activa": None
            }