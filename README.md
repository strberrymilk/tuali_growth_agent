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

For two sister-company databases in the same MongoDB cluster, use one shared URI and two database names in `.env`:

```env
MONGO_URI=mongodb+srv://<user>:<password>@<cluster-url>/?retryWrites=true&w=majority
MONGO_DB_COMPANY_ONE=company_one
MONGO_DB_COMPANY_TWO=company_two
```

Backend connection helper lives in `backend/database/mongo.py`.

## Yomp Mock Endpoints

Run the backend with:

```bash
uvicorn backend.main:app --reload
```

Available demo endpoints:

```text
GET /health
GET /tts/test-page
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
