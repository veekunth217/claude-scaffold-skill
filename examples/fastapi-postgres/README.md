# fastapi-postgres

FastAPI backend with PostgreSQL — async, typed, migration-managed.

## Quick start

```bash
# 1. Install dependencies
pyenv local 3.12.0
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Start the database
docker compose up -d db

# 3. Run migrations
alembic upgrade head

# 4. Start the dev server
uvicorn src.app.main:app --reload
```

App available at http://localhost:8000 — Swagger docs at http://localhost:8000/docs.

## Or use Docker for everything

```bash
docker compose up
```

## Project layout

See [CLAUDE.md](CLAUDE.md) for full structure and commands.
