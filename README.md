# AI Observability

Full-stack AI observability app with:
- FastAPI backend (`app/`)
- React + Vite dashboard (`dashboard/`)
- SQLite by default (`ai_logs.db`)

# Full Explaination of the Project
- [Article 1](https://medium.com/@sayedebad.777/building-an-ai-observability-system-from-scratch-fastapi-openai-react-part-1-87421b664859)
- [Article 2](https://medium.com/@sayedebad.777/building-an-ai-observability-system-from-scratch-fastapi-openai-react-part-2-2f325db57177)

## Features

- Register and login with role-based users (`admin`, `employee`)
- Send prompts to an LLM
- Track request cost and latency
- View request logs
  - `admin`: sees all logs
  - `employee`: sees only their own logs

## Project Structure

```text
app/
 ├── api/
 │    ├── admin_routes.py
 │    ├── auth_routes.py
 │    ├── employee_routes.py
 │    ├── __init__.py
 ├── core/
 │    ├── dependencies.py
 │    ├── security.py
 │    ├── __init__.py
 ├── models/
 │    ├── llm_log.py
 │    ├── user.py
 │    ├── __init__.py
 ├── services/
 │    ├── auth_service.py
 │    ├── llm_service.py
 │    ├── logging_service.py
 │    ├── __init__.py
 ├── config.py
 ├── database.py
 ├── main.py
 ├── schemas.py
```

## Prerequisites

- Python 3.11+
- Node.js 18+ (or latest LTS)
- npm
- OpenAI API key

## 1) Backend Setup

From project root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
pip install "python-jose[cryptography]" "passlib[bcrypt]"
```

Create/update `.env` in project root:

```env
DATABASE_URL=sqlite:///./ai_logs.db
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

Run backend:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL: `http://127.0.0.1:8000`

## 2) Frontend Setup

In a new terminal:

```powershell
cd dashboard
npm install
npm run dev
```

Dashboard URL (usually): `http://127.0.0.1:5173`

## 3) First-Time Usage

1. Open the dashboard.
2. Register a user using API (Swagger/Postman/curl), then login in UI.
3. Submit prompts from the dashboard.

Open Swagger docs:
- `http://127.0.0.1:8000/docs`

Useful endpoints:
- `POST /auth/register`
- `POST /auth/login`
- `POST /employee/generate` (Bearer token required)
- `GET /admin/logs` (Bearer token required)

Example register payload:

```json
{
  "name": "Admin User",
  "email": "admin@example.com",
  "password": "admin123",
  "role": "admin"
}
```

Employee payload is the same with `"role": "employee"`.

## Run with Docker (backend only)

From project root:

```powershell
docker build -t ai-observability .
docker run --rm -p 8000:8000 --env-file .env ai-observability
```

## Troubleshooting

- `403 Not authorized` on generate/logs:
  - Login again to refresh token.
  - Ensure role is `admin` or `employee`.
- `401 Invalid token`:
  - Token missing/expired, login again.
- OpenAI errors:
  - Check `OPENAI_API_KEY` in `.env`.
- Missing module errors (`jose`, `passlib`):
  - Install extra packages:
    - `pip install "python-jose[cryptography]" "passlib[bcrypt]"`

## Notes

- CORS is currently open (`allow_origins=["*"]`) for local development.
- Default DB is SQLite file `ai_logs.db`.
