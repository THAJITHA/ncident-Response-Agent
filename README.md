# Incident Response Agent

## Project overview

This project is a DevOps and SRE incident response assistant that learns from historical incidents and retrieves similar previous cases to help engineers diagnose, recommend runbooks, and resolve incidents faster.

The core idea is simple: Hindsight is not optional. It is the long-term memory layer that stores past incidents, their symptoms, causes, actions, and lessons learned, so future incidents can reuse proven knowledge.

## Architecture

- Backend: FastAPI
- Storage: SQLite for local incident records
- Persistent memory: Hindsight via the official `hindsight-client` SDK
- AI reasoning: Groq-ready LLM integration
- Frontend: React/Vite (not implemented in this Phase 2 scope)

## How Hindsight is used

The application stores incident narratives in a configured Hindsight bank called `incident-response`. Each stored memory includes the incident summary, service, symptoms, cause, investigation steps, runbook, actions, resolution, and lessons learned.

When a new incident is investigated, the backend calls Hindsight recall against the same bank and searches for similar historical cases. The system then surfaces the matched memories and uses that evidence to produce a useful recommendation.

## Setup

### 1. Create a virtual environment

```powershell
cd "c:\Users\ANIL\Desktop\hacakthon\incident-response-agent\backend"
python -m venv .venv
```

### 2. Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create environment variables

Copy the example file and fill in the values you need:

```powershell
Copy-Item .env.example .env
```

Example values:

```env
HINDSIGHT_API_KEY=
HINDSIGHT_API_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=incident-response
GROQ_API_KEY=
```

> Do not commit `.env` files. Keep API keys in local environment variables only.

## Running the backend

```powershell
cd "c:\Users\ANIL\Desktop\hacakthon\incident-response-agent\backend"
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API endpoints

- `GET /api/health`
- `POST /api/incidents`
- `GET /api/incidents`
- `GET /api/incidents/{incident_id}`
- `POST /api/incidents/{incident_id}/remember`
- `POST /api/memory/search`

## Example memory search payload

```json
{
  "query": "Payment service is returning HTTP 503 after deployment"
}
```

## Security warning

Never hardcode API keys in source code. Always use environment variables. The project intentionally keeps `.env` excluded from Git and only references values from the environment at runtime.

## Testing the Hindsight connection

1. Set `HINDSIGHT_API_KEY` and `HINDSIGHT_API_URL` in `.env`.
2. Run the backend.
3. Call the memory endpoint with a real incident query.
4. If the request fails, the service will return a safe, descriptive error instead of exposing the key or sensitive details.

## Validation

The backend includes a small test file that validates:

- FastAPI starts
- `/api/health` works
- incident creation works
- incident retrieval works
- Hindsight service initialization is safe without live credentials
- memory search handles empty or invalid requests gracefully

Run:

```powershell
cd "c:\Users\ANIL\Desktop\hacakthon\incident-response-agent\backend"
.\.venv\Scripts\Activate.ps1
pytest -q
```

## Phase 2 status

This phase focuses on the backend foundation and the real Hindsight integration. The frontend and advanced recommendation workflows are intentionally not included yet.
