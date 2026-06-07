import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.services.tts_service import generate_tts

file_path = generate_tts("La semana pasada compraste más de 1000 unidades de este producto")
print(file_path)
