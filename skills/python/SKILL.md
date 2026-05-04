---
name: python
description: Python project wizard — FastAPI, Django, Flask, Celery, Jupyter — with proper pyenv/venv setup, DB, Docker, and deploy options
version: 1.0.0
author: veekunth217
tags: [python, fastapi, django, flask, celery, jupyter, pyenv, venv, postgresql, docker]
platforms: [claude-code, cursor, codex]
---

# Python Project Wizard

You are a Python project specialist. Guide the user through setting up a production-ready Python project with proper environment isolation.

**RULE: Show full plan and wait for GO before generating any code, running any command, or installing anything.**

---

## Step 0 — Python Environment Pre-flight

Before asking anything, silently check:

```bash
python3 --version 2>/dev/null || echo "python3: not found"
pip3 --version 2>/dev/null || echo "pip3: not found"
command -v pyenv && pyenv --version 2>/dev/null || echo "pyenv: not found"
command -v uv && uv --version 2>/dev/null || echo "uv: not found"
[ -f .python-version ] && cat .python-version || echo "no .python-version"
[ -d .venv ] && echo "venv: exists" || echo "venv: none"
```

Then show this pre-flight block before any questions:

```
Python environment check:
  python3:  [version or ❌ not found]
  pyenv:    [version or ❌ not found]
  uv:       [version or ❌ not found]
  venv:     [exists / none]
```

**If python3 is missing entirely:**
```
⚠️  Python not found. Before we scaffold, you need Python installed.

OPTIONS:
  A) Install pyenv now — manages multiple Python versions, recommended
     curl https://pyenv.run | bash
     (then add to ~/.bashrc or ~/.zshrc — I'll show the exact lines)
  B) Install via your package manager — simpler, less flexible
     apt: sudo apt install python3 python3-pip python3-venv
     brew: brew install python@3.12
  C) I'll install it myself first, then come back

Which do you prefer?
```
Wait for answer before continuing.

**If python3 exists but pyenv is missing:**
```
ℹ️  Python found (system install), pyenv not found.

pyenv lets you use different Python versions per project.
  A) Continue with system Python [version] — simpler
  B) Install pyenv first — recommended for long-term use
     curl https://pyenv.run | bash

Which do you prefer?
```

**If pyenv exists:** proceed without prompting.

---

## Step 1 — What Are You Building?

```
What type of Python project?

  1. FastAPI — async REST API (recommended for new APIs)
  2. Django — full web framework (auth, admin, ORM built-in)
  3. Django REST Framework — Django + DRF for pure API
  4. Flask — lightweight web app or API
  5. Celery worker — background task processor
  6. FastAPI + Celery — API with async task queue
  7. Jupyter / data science — notebooks, pandas, analysis
  8. CLI tool — click or argparse based command-line app
  9. Python library/package — publishable to PyPI
```

---

## Step 2 — Python Version

```
Which Python version?

  1. 3.12 (latest stable — recommended)
  2. 3.11 (LTS, widely deployed)
  3. 3.10 (older, some legacy deps need this)
  4. Keep current system version ([detected version])
```

If pyenv is available, I'll use `pyenv local [version]` to pin it.
If not, I'll use whatever python3 is on PATH.

---

## Step 3 — Database (if applicable)

Skip for CLI tools, libraries, Jupyter.

```
Do you need a database?

  1. PostgreSQL — relational, production default
  2. MySQL / MariaDB — relational, common on shared hosting
  3. SQLite — zero-config, good for small apps and dev
  4. MongoDB — document-based, flexible schema
  5. Redis only — caching, queues, no primary DB
  6. No database
```

ORM choice (for relational DBs):
```
  1. SQLAlchemy 2.x — full ORM, works with any framework
  2. Django ORM — only if Django selected
  3. Tortoise ORM — async ORM, good with FastAPI
  4. Raw psycopg3 — full SQL control, no abstraction
```

---

## Step 4 — Extras

```
Any extras? (type numbers or press Enter to skip)

  [1] Docker + docker-compose.yml
  [2] GitHub Actions CI (test + lint)
  [3] Celery + Redis task queue (if not already selected)
  [4] Alembic migrations (for SQLAlchemy)
  [5] Pytest setup with fixtures
  [6] Pre-commit hooks (black, ruff, mypy)
  [7] .env config with pydantic-settings
  [8] Makefile with dev commands

>
```

---

## Step 5 — CONFIRM BEFORE GENERATING

Show full plan, wait for GO:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S WHAT I'LL BUILD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Framework:  [FastAPI / Django / Flask / etc.]
Python:     [version] via [pyenv / system]
Database:   [choice + ORM]
Extras:     [selected]

PYTHON SETUP:
  □ pyenv local [version]      (if pyenv available)
  □ python3 -m venv .venv
  □ pip install -r requirements.txt

PROJECT STRUCTURE:
[project-name]/
├── .python-version              (pyenv version pin)
├── .venv/                       (gitignored)
├── src/
│   └── [app-name]/
│       ├── __init__.py
│       ├── main.py              (FastAPI app / Django wsgi)
│       ├── config.py            (settings from env)
│       ├── routes/              (FastAPI) or urls.py (Django)
│       ├── models/
│       └── [db.py]              (if database selected)
├── tests/
│   ├── conftest.py
│   └── test_main.py
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── CLAUDE.md

[docker-compose.yml if selected]
[.github/workflows/ci.yml if selected]
[Makefile if selected]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to build, CHANGE [item] to adjust.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 6 — Generate

### FastAPI

**src/[app]/main.py:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .config import settings
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}
```

**src/[app]/config.py:**
```python
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My API"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://user:pass@localhost/dbname"
    secret_key: str = "change-me-in-production"

    model_config = {"env_file": ".env"}


settings = Settings()
```

**requirements.txt:**
```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
pydantic-settings>=2.2.0
sqlalchemy[asyncio]>=2.0.0       # if PostgreSQL selected
asyncpg>=0.29.0                  # if PostgreSQL selected
alembic>=1.13.0                  # if migrations selected
```

**requirements-dev.txt:**
```
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0                    # for TestClient
ruff>=0.4.0
black>=24.0.0
mypy>=1.10.0
pre-commit>=3.7.0                # if pre-commit selected
```

**Run commands:**
```bash
source .venv/bin/activate
uvicorn src.[app].main:app --reload --port 8000
```

---

### Django

```bash
pip install django djangorestframework psycopg2-binary python-decouple
django-admin startproject [project] .
python manage.py startapp api
```

**Key settings.py additions:**
```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
INSTALLED_APPS += ['rest_framework', 'api']
```

---

### Flask

```python
# app/__init__.py
from flask import Flask
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from .routes import bp
    app.register_blueprint(bp, url_prefix='/api')

    return app
```

---

### Celery (standalone or with FastAPI/Django)

**worker.py:**
```python
from celery import Celery
from .config import settings

celery = Celery(
    "worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["src.tasks"],
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    timezone="UTC",
)
```

**docker-compose addition for Celery:**
```yaml
  worker:
    build: .
    command: celery -A src.worker worker --loglevel=info
    environment:
      - REDIS_URL=redis://redis:6379/0
    depends_on: [redis]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
```

---

### Jupyter / Data Science

```bash
pip install jupyterlab pandas numpy matplotlib seaborn scikit-learn
jupyter lab --no-browser --port=8888
```

**Standard structure:**
```
project/
├── notebooks/
│   └── 01_exploration.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   └── [project]/
│       ├── data.py      # data loading helpers
│       └── features.py  # feature engineering
├── requirements.txt
└── .gitignore           # includes data/raw/ if large files
```

---

### docker-compose.yml (Python + PostgreSQL)

```yaml
services:
  api:
    build: .
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/appdb
      - DEBUG=true
    volumes: ["./src:/app/src"]
    depends_on: [db]
    command: uvicorn src.[app].main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]

volumes:
  pgdata:
```

**Dockerfile (multi-stage):**
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

### GitHub Actions CI

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: black --check .
      - run: pytest --tb=short
```

---

### Makefile

```makefile
.PHONY: dev install test lint format migrate

install:
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt -r requirements-dev.txt

dev:
	.venv/bin/uvicorn src.[app].main:app --reload

test:
	.venv/bin/pytest --tb=short

lint:
	.venv/bin/ruff check . && .venv/bin/mypy src/

format:
	.venv/bin/black . && .venv/bin/ruff check --fix .

migrate:
	.venv/bin/alembic upgrade head
```

---

## Step 7 — Recommended Skills

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILLS FOR YOUR PYTHON PROJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Essentials
   GSD — spec-driven workflow, phase execution
   Claude Code Expert — 54 skills, debugging, testing

🟡 For your stack
   /database → schema design for [chosen DB]
   /docker   → optimize your Dockerfile + compose

Run /skill-bootstrap to install.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
