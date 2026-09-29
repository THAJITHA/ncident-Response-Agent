# Incident Response Agent

A security operations dashboard for recording, triaging, investigating, and resolving service incidents. The React dashboard reads incident data from a FastAPI backend, displays live operational metrics, and refreshes incident data every 15 seconds.

## Features

- Dashboard metrics, incident activity chart, severity distribution, and priority queue.
- Incident register with search, severity/status filters, and date sorting.
- Incident detail drawer with evidence, response timeline, investigation output, and recommendations.
- Incident creation and backend-persisted response actions: investigate, start response, assign, contain, add note, escalate, and resolve.
- Agent investigation and recommendation endpoints, with optional Groq analysis and a built-in fallback when no Groq key is configured.
- Operations memory view backed by incident records in the local database.
- Responsive layout for desktop and mobile, loading/error states, and dismissible notifications.

## Architecture

- Frontend: React 18, Vite, Recharts, and Lucide icons.
- Backend: FastAPI with SQLAlchemy.
- Storage: SQLite by default. Incident records and response timeline events are stored locally.
- Analysis: Groq can be configured for LLM-assisted investigation. Without a key, the backend returns its built-in fallback analysis.

The current memory adapter searches locally stored incident records. Configure external Hindsight credentials only if you are using a backend version that integrates with your Hindsight service.

## Prerequisites

- Python 3.10 or newer.
- Node.js 18 or newer and npm.
- PowerShell on Windows, or equivalent shells on other platforms.

## Setup

Open two terminals in VS Code. Run the backend in the first terminal and the frontend in the second. Commands below assume the repository folder is named `incident-response-agent`.

### 1. Configure the backend

```powershell
cd "C:\path\to\incident-response-agent\backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `backend/.env` only if you want to provide an LLM key. `GROQ_API_KEY` can remain empty; the built-in analysis fallback will be used. Never commit `.env` or put credentials in source files. The repository ignores local `.env` files.

### 2. Start the backend

In the backend terminal, with the virtual environment active:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is available at `http://localhost:8000`. Open `http://localhost:8000/docs` to explore the interactive OpenAPI documentation. Verify the backend at `http://localhost:8000/api/health`.

### 3. Start the frontend

In the second terminal:

```powershell
cd "C:\path\to\incident-response-agent\frontend"
npm install
npm run dev
```

Open the URL printed by Vite, normally `http://localhost:5173`. Keep both terminal processes running while using the dashboard.

The frontend defaults to `http://localhost:8000` for its API. To use another backend URL, create `frontend/.env.local` with:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Restart Vite after changing frontend environment variables. If the API is offline, the dashboard displays a connection error and retry action; it does not substitute demo incident data.

## Using the dashboard

1. Start both backend and frontend as described above.
2. Select **New incident** to submit a title, service, severity, description, and alert/log evidence.
3. Open an incident from the priority queue or incident list to inspect its evidence and response timeline.
4. Use **Investigate** for agent analysis, or **Recommend** to request response guidance from the backend.
5. Record operational work using assignment, notes, response start, containment, escalation, and resolution actions. These operations write to the backend and appear in the incident timeline.
6. Use **Operations memory** to search incident records already stored by the backend.

Severity values accepted by the incident API are `SEV-1` (Critical), `SEV-2` (High), `SEV-3` (Medium), and `SEV-4` (Low). Status values include `OPEN`, `INVESTIGATING`, `CONTAINED`, and `RESOLVED`.

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Backend health check |
| `GET` | `/api/incidents` | List incidents |
| `POST` | `/api/incidents` | Create an incident |
| `GET` | `/api/incidents/{incident_id}` | Retrieve incident details |
| `GET` | `/api/incidents/{incident_id}/events` | Retrieve response timeline events |
| `POST` | `/api/incidents/{incident_id}/actions` | Record a response action and update supported statuses |
| `POST` | `/api/incidents/{incident_id}/investigate` | Run agent investigation |
| `POST` | `/api/incidents/{incident_id}/recommend` | Generate response recommendation |
| `POST` | `/api/incidents/{incident_id}/postmortem` | Generate a post-incident review |
| `GET` | `/api/memory/incidents` | List incident memory records |
| `POST` | `/api/memory/search` | Search incident memory |

The action endpoint accepts an action name (`investigate`, `start_response`, `assign`, `contain`, `resolve`, `add_note`, or `escalate`) and optional `detail` and `assigned_to` fields. Assignment requires `assigned_to`; notes and resolution require `detail`.

Example incident creation payload:

```json
{
  "title": "Elevated errors on payment API",
  "service": "payments-api",
  "severity": "SEV-2",
  "symptoms": "Customers are seeing intermittent payment failures.",
  "error_logs": "HTTP 503 responses increased after the latest deployment.",
  "environment": "production"
}
```

## Checks

Build the frontend:

```powershell
cd "C:\path\to\incident-response-agent\frontend"
npm run build
```

Run backend tests, if the project test suite is present:

```powershell
cd "C:\path\to\incident-response-agent\backend"
.\.venv\Scripts\Activate.ps1
pytest -q
```

## Security

- Do not commit `.env` files, API keys, tokens, or production incident evidence.
- Keep credentials in local environment variables and rotate any credential that has been exposed.
- The development CORS configuration is permissive; restrict allowed origins before deploying the backend publicly.
- This project is a hackathon/demo foundation. Add authentication, authorization, audit controls, and production hardening before using it for real security incidents.
