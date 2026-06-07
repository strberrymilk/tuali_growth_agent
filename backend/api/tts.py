from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel

from backend.services.tts_service import generate_elevenlabs_speech_bytes


router = APIRouter(prefix="/tts", tags=["tts"])


class TTSRequest(BaseModel):
    text: str


TEST_PAGE_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>ElevenLabs TTS Test</title>
    <style>
      body {
        font-family: Georgia, serif;
        background: #f6efe3;
        color: #1f2937;
        margin: 0;
        padding: 32px;
      }
      .card {
        max-width: 720px;
        margin: 0 auto;
        background: #fffaf2;
        border: 1px solid #d6c7ae;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 18px 45px rgba(84, 63, 22, 0.12);
      }
      h1 {
        margin-top: 0;
      }
      textarea {
        width: 100%;
        min-height: 180px;
        border-radius: 12px;
        border: 1px solid #c9b693;
        padding: 14px;
        font: inherit;
        box-sizing: border-box;
        resize: vertical;
        background: #fffdf8;
      }
      button {
        margin-top: 16px;
        background: #1d4ed8;
        color: white;
        border: 0;
        border-radius: 999px;
        padding: 12px 20px;
        cursor: pointer;
        font-weight: 700;
      }
      button:disabled {
        opacity: 0.7;
        cursor: wait;
      }
      .status {
        margin-top: 12px;
      }
      audio {
        width: 100%;
        margin-top: 18px;
      }
    </style>
  </head>
  <body>
    <div class="card">
      <h1>ElevenLabs TTS Test</h1>
      <p>Write a short phrase to test speech generation for the app.</p>
      <textarea id="text">Hola, esta es una prueba de texto a voz para Tuali Growth Agent.</textarea>
      <button id="playButton">Generate Audio</button>
      <div class="status" id="status"></div>
      <audio id="player" controls></audio>
    </div>

    <script>
      const button = document.getElementById("playButton");
      const textArea = document.getElementById("text");
      const status = document.getElementById("status");
      const player = document.getElementById("player");

      button.addEventListener("click", async () => {
        button.disabled = true;
        status.textContent = "Generating audio...";

        try {
          const response = await fetch("/tts/preview", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: textArea.value })
          });

          if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Failed to generate audio.");
          }

          const blob = await response.blob();
          const url = URL.createObjectURL(blob);
          player.src = url;
          player.play();
          status.textContent = "Audio generated successfully.";
        } catch (error) {
          status.textContent = error.message;
        } finally {
          button.disabled = false;
        }
      });
    </script>
  </body>
</html>
"""


@router.get("/test-page", response_class=HTMLResponse)
def get_tts_test_page() -> str:
    return TEST_PAGE_HTML


@router.post("/preview")
def generate_tts_preview(payload: TTSRequest) -> Response:
    try:
        audio = generate_elevenlabs_speech_bytes(payload.text)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"ElevenLabs request failed: {error}") from error

    return Response(content=audio, media_type="audio/mpeg")
