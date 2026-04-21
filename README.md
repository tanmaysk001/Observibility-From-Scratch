# Company AI Governance System

FastAPI backend and React dashboard for **authenticated, role-scoped, cost-tracked** LLM usage: identity, role-based access control, and domain separation.

## Architecture

```
app/
 ├── api/          HTTP boundary (auth / employee / admin routers)
 ├── core/         Security primitives + JWT dependencies
 ├── models/       SQLAlchemy persistent entities (User, LLMLog)
 ├── services/     Business logic (auth, llm, logging)
 ├── config.py     Env-driven configuration
 ├── database.py   Engine, session factory, declarative base
 ├── schemas.py    Pydantic request/response shapes
 └── main.py       FastAPI app + router registration
frontend/          Vite + React dashboard (login, prompt, charts)
```

Request flow: **Route → Service → Model**. Routes coordinate, services execute, models persist; the core layer centralizes security.

## Backend Setup

Requires Python 3.10+.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
copy .env.example .env         # fill in OPENAI_API_KEY + SECRET_KEY

uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000` — interactive docs at `/docs`.

### Endpoints

| Method | Path                | Auth        | Purpose                         |
|--------|---------------------|-------------|---------------------------------|
| POST   | `/auth/register`    | public      | Create user (`admin`/`employee`) |
| POST   | `/auth/login`       | public      | Exchange credentials for JWT    |
| POST   | `/employee/generate`| Bearer JWT  | Call LLM, log request           |
| GET    | `/admin/logs`       | Bearer JWT  | List logs (admin = all, employee = own) |

## Frontend Setup

Requires Node.js 18+.

```bash
cd frontend
npm install
npm run dev
```

Dashboard: `http://localhost:5173` — configure the app to use the API at `http://127.0.0.1:8000`.

## Quick test

1. Register an admin:

   ```bash
   curl -X POST http://127.0.0.1:8000/auth/register ^
     -H "Content-Type: application/json" ^
     -d "{\"name\":\"Root\",\"email\":\"admin@acme.com\",\"password\":\"pw\",\"role\":\"admin\"}"
   ```

2. Log in in the UI, send a prompt, and confirm cost/latency charts update.

## Implementation notes

- JWT tokens are stateless and include `sub` (email), `role`, and `exp`.
- `app/core/dependencies.py` decodes JWTs for protected routes.
- `app/core/security.py` exposes DB-backed `get_current_user` when full user verification is required.
- Cost is derived from token counts via `PRICE_PER_1K_INPUT` / `PRICE_PER_1K_OUTPUT` in `services/llm_service.py` — adjust to match your pricing.
