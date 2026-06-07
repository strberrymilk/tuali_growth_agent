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
