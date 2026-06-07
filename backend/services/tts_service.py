import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from elevenlabs import save
from elevenlabs.client import ElevenLabs


load_dotenv()


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
ELEVENLABS_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")
ELEVENLABS_STS_MODEL_ID = os.getenv("ELEVENLABS_STS_MODEL_ID", "eleven_multilingual_sts_v2")
AUDIO_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "generated_audio"


def _get_client() -> ElevenLabs:
    if not ELEVENLABS_API_KEY:
        raise ValueError("Missing ELEVENLABS_API_KEY in environment variables.")

    return ElevenLabs(api_key=ELEVENLABS_API_KEY)


def _convert_text_to_speech(text: str):
    if not text.strip():
        raise ValueError("Text is required to generate speech.")

    client = _get_client()
    return client.text_to_speech.convert(
        text=text,
        voice_id=ELEVENLABS_VOICE_ID,
        model_id=ELEVENLABS_MODEL_ID,
        output_format="mp3_44100_128",
    )


def _convert_speech_to_speech(
    audio_bytes: bytes,
    source_filename: str,
    content_type: str | None = None,
    voice_id: str | None = None,
):
    if not audio_bytes:
        raise ValueError("Audio input is required for voice-to-voice conversion.")

    client = _get_client()
    return client.speech_to_speech.convert(
        voice_id=voice_id or ELEVENLABS_VOICE_ID,
        audio=(source_filename, audio_bytes, content_type or "application/octet-stream"),
        model_id=ELEVENLABS_STS_MODEL_ID,
        output_format="mp3_44100_128",
    )


def generate_tts(text: str) -> str:
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"tts_{uuid.uuid4().hex}.mp3"
    file_path = AUDIO_OUTPUT_DIR / filename

    audio = _convert_text_to_speech(text)
    save(audio, str(file_path))

    return str(file_path)


def generate_elevenlabs_speech_bytes(text: str) -> bytes:
    audio = _convert_text_to_speech(text)
    return b"".join(chunk for chunk in audio if isinstance(chunk, bytes))

class VoiceRequest(BaseModel):
    texto_gancho: str

@router.post("/speak")
def generar_voz_agente(payload: VoiceRequest):
    """
    Recibe el 'gancho' generado por Gemini y lo convierte en bytes de audio
    usando ElevenLabs para que el usuario escuche a su asesor.
    """
    try:
        # Reutiliza tu lógica existente de tts_service.py
        audio_bytes = generate_elevenlabs_speech_bytes(payload.texto_gancho)[cite: 6]
        return Response(content=audio_bytes, media_type="audio/mpeg")[cite: 1]
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Error con ElevenLabs: {error}")[cite: 1]

def generate_voice_to_voice(
    audio_bytes: bytes,
    source_filename: str,
    content_type: str | None = None,
    voice_id: str | None = None,
) -> str:
    AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"voice_to_voice_{uuid.uuid4().hex}.mp3"
    file_path = AUDIO_OUTPUT_DIR / filename

    audio = _convert_speech_to_speech(
        audio_bytes=audio_bytes,
        source_filename=source_filename,
        content_type=content_type,
        voice_id=voice_id,
    )
    save(audio, str(file_path))

    return str(file_path)
