# AI Chat API

A production-oriented FastAPI starter for a versioned AI chat API, using Python 3.12.

## Quick start

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python server.py
```

Open `http://localhost:8000/docs` for interactive API documentation.

## Example request

```bash
curl -X POST http://localhost:8000/api/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"messages":[{"role":"user","content":"Hello"}],"temperature":0.7}'
```

The included chat service is deliberately provider-neutral and returns a deterministic placeholder. Connect your AI SDK inside `services/chat_service.py`; request validation and HTTP routes remain unchanged. Store provider credentials in `.env`, never in source control.

## Project structure

- `main.py` creates the ASGI application, middleware, routes, lifecycle hooks, and global error handling.
- `server.py` is the executable Uvicorn launcher; deploy with `uvicorn main:app` in a process manager/container.
- `routers/` contains thin HTTP endpoint modules, separated by resource and API version.
- `services/` owns business logic and third-party AI-provider integration, keeping routers testable and transport-focused.
- `models/` contains Pydantic request/response contracts used for validation and OpenAPI documentation.
- `utils/` holds cross-cutting helpers such as consistent exception handling.
- `config.py` centralizes typed environment configuration and loads local `.env` values.
- `.env.example` documents required configuration without exposing secrets.

## Production notes

Set `ENVIRONMENT=production`, `DEBUG=false`, and explicit `ALLOWED_ORIGINS`. Run multiple workers through your platform/process manager, for example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Put the service behind TLS termination, add authentication and rate limiting before making a public AI endpoint, and replace the placeholder service with your selected provider client.
