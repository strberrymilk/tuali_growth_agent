import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.tts_service import generate_tts

file_path = generate_tts("La semana pasada compraste más de 1000 unidades de este producto")
print(file_path)
