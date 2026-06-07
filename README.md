# tuali_growth_agent

Repo for Hack4her 2026 "Tuali Growth Agent" track.

## Project Structure

```text
tuali-growth-agent/
|-- frontend/
|-- backend/
|-- mock_data/
|-- tests/
|-- docs/
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Folder Guide

### `frontend/`
Contains the user-facing app.

- `pages/`: Screen-level views and route-based experiences.
- `components/`: Reusable UI building blocks shared across pages.
- `services/`: Frontend logic for API calls, helpers, and integrations.
- `styles/`: Global styles, tokens, themes, and shared CSS.

### `backend/`
Contains the server-side logic and product intelligence.

- `api/`: Routes, controllers, and request/response handlers.
- `agent/`: Core agent orchestration, prompts, and decision flows.
- `mcp/`: MCP-related integrations, adapters, or tool definitions.
- `services/`: Business logic used by the API and agent layers.
- `database/`: Connection setup, queries, migrations, or seeds.
- `models/`: Data models, schemas, and typed entities.
- `utils/`: Shared backend helpers and utility functions.

### `mock_data/`
Sample or fake data for local development, demos, and testing.

### `tests/`
Automated tests for backend logic, API endpoints, and future integrations.

### `docs/`
Internal documentation such as architecture notes, workflows, and product decisions.

### `README.md`
Quick entry point for understanding the repository.

### `requirements.txt`
Main Python dependencies for the project.

### `.gitignore`
Files and folders that should stay out of version control, such as virtual environments and cache files.

## MongoDB Setup

Tuali and Yomp are configured as separate MongoDB clusters.

Use these variables in `.env`:

```env
MONGODB_URI_ALY=mongodb+srv://<user>:<password>@<tuali-cluster>/?retryWrites=true&w=majority
MONGODB_ALY=aly_ai

MONGODB_URI_YOMP=mongodb+srv://<user>:<password>@<yomp-cluster>/?retryWrites=true&w=majority
MONGODB_YOMP=yomp_pos_db
```

Notes:

- `MONGODB_URI_ALY` is used as the Tuali cluster connection.
- `MONGODB_URI_YOMP` is used for Yomp sales and inventory data.
- `backend/database/mongo.py` supports these current names and also accepts `MONGODB_URI_TUALI` / `MONGODB_TUALI` as aliases.
- Yomp analysis will use live DB data when available and fall back to `mock_data/yomp_mock.json` only if needed for demo continuity.

## Yomp Mock Endpoints

Run the backend with:

```bash
uvicorn backend.main:app --reload
```

Run the frontend with:

```bash
cd frontend
npm install
npm run dev
```

Local app URLs:

```text
Frontend: http://localhost:5173
Backend: http://127.0.0.1:8000
```

Available demo endpoints:

```text
GET /health
GET /agent/tools
POST /agent/run/{tuali_cliente_id}
GET /agent/recommendations/{tuali_cliente_id}
GET /tts/test-page
POST /tts/generate
POST /tts/preview
GET /yomp/{tuali_cliente_id}/transactions
GET /yomp/{tuali_cliente_id}/inventory
GET /yomp/{tuali_cliente_id}/daily-sales
GET /yomp/{tuali_cliente_id}/daily-products
GET /yomp/{tuali_cliente_id}/growth-context
```

Demo client id available in mock data:

```text
TUALI_FE_88321
```

To test ElevenLabs text-to-speech, set these variables in `.env`:

```env
ELEVENLABS_API_KEY=your_api_key
ELEVENLABS_VOICE_ID=JBFqnCBsd6RMkjVDRZzb
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
```

Local SDK demo:

```bash
py -m backend.services.tts_demo
```

The demo generates an MP3 file in `generated_audio/` and prints the saved file path.

## Gemini Setup

Set these variables in `.env` to enable live Gemini synthesis:

```env
GEMINI_API_KEY=your_api_key
GEMINI_MODEL_ID=gemini-2.5-flash
```

Notes:

- The agent keeps its rule-based business signals even if Gemini is disabled.
- Gemini is used as a synthesis layer for `message`, `headline`, prioritized recommendations, and `voice_text`.
- If `GEMINI_API_KEY` is missing or the API fails, `/agent/run/{tuali_cliente_id}` still returns a successful fallback response.
- You can see whether Gemini ran in live mode or fallback mode in `data_sources`, using `source="gemini_synthesis"` and `mode="live"` or `mode="fallback"`.

## MCP-Like Tool Layer

The backend uses a lightweight MCP-like structure:

```text
Agent / Allie
-> backend/mcp/tools.py
-> backend/services/*
-> MongoDB / Gemini / ElevenLabs
```

Current MCP-like tools include:

- `get_tuali_profile(tuali_cliente_id)`
- `get_active_goal(tuali_cliente_id)`
- `get_available_promotions(tuali_cliente_id)`
- `get_loyalty_status(tuali_cliente_id)`
- `get_yomp_growth_context(tuali_cliente_id)`
- `save_recommendation(tuali_cliente_id, recommendation)`
- `get_recommendations(tuali_cliente_id)`
