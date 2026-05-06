# fastapi-postgres

## Stack
- Python 3.12 (managed via pyenv)
- FastAPI + Uvicorn
- PostgreSQL 16 + SQLAlchemy 2.x + Alembic migrations
- Docker Compose for local dev
- pytest + httpx for tests
- ruff for lint + format

## Commands
- Start dev server: `uvicorn src.app.main:app --reload`
- Run tests: `pytest`
- Run with Docker: `docker compose up`
- Run migrations: `alembic upgrade head`
- New migration: `alembic revision --autogenerate -m "description"`
- Lint + format: `ruff check . && ruff format .`

## Environment
- Python: 3.12 via pyenv (`.python-version` set)
- Package manager: pip (or uv if installed)
- Virtual env: `.venv/` at project root
- Activate: `source .venv/bin/activate`

## Project Structure
- `src/app/` — FastAPI application code
  - `main.py` — app entrypoint
  - `routers/` — endpoint modules
  - `models/` — SQLAlchemy models
  - `schemas/` — Pydantic schemas
  - `db.py` — engine + session factory
- `migrations/` — Alembic versions
- `tests/` — pytest test modules

## Notes
- DB credentials live in `.env` (gitignored). See `.env.example` for the shape.
- Always run migrations before starting dev server after schema changes.
- Never commit `.env` or `.venv/`.
