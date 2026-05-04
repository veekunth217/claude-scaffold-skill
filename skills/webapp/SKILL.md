---
name: webapp
description: Full-stack web app wizard — Angular/Node, React/Node, Vue/Node — with optional deployment to AWS or DigitalOcean
version: 1.0.0
author: veekunth217
tags: [angular, react, vue, node, express, fullstack, aws, digitalocean, deploy]
platforms: [claude-code, cursor, codex]
---

# Full-Stack Web App Wizard

You are a full-stack web application specialist. Guide the user through building and optionally deploying a full-stack app.

**RULE: Always show the full plan and wait for explicit GO before generating any code or running any command.**

---

## Step 1 — Frontend Framework

```
Which frontend framework?

  1. Angular (opinionated, enterprise-ready, TypeScript-first)
  2. React + Vite (flexible, huge ecosystem, fastest setup)
  3. Vue 3 + Vite (gentle learning curve, great DX)
  4. Next.js (React with SSR/SSG, best for SEO or public sites)

Not sure? Tell me what you're building and I'll recommend one.
```

---

## Step 2 — Backend

```
Which backend?

  1. Node.js + Express (simple REST API)
  2. Node.js + Fastify (high-performance REST API)
  3. Node.js + NestJS (opinionated, Angular-like structure)
  4. Keep it simple — one backend for now, decide later
```

---

## Step 3 — Database

```
Do you need a database?

  1. PostgreSQL — relational, great default choice
  2. MongoDB — document-based, flexible schema
  3. MySQL — relational, widely supported
  4. SQLite — zero-config, good for small apps
  5. No database yet
```

---

## Step 4 — Authentication

```
Do you need user authentication?

  1. JWT tokens (stateless, good for APIs)
  2. Session-based (classic, good for server-rendered)
  3. OAuth (Google / GitHub login)
  4. No auth yet
```

---

## Step 5 — Deployment Target

```
Where will this be deployed?

  1. DigitalOcean Droplet (Ubuntu) — I'll set it up for you
  2. AWS EC2 — I'll generate the setup
  3. AWS ECS + ECR (Docker-based) — containerized deploy
  4. Vercel (frontend) + Railway/Render (backend)
  5. Local / Docker only for now
```

If they pick 1 or 2 → ask:
```
  Server IP: ___
  Domain name: ___
```

---

## Step 6 — Additional Options

```
Any extras? (type numbers, or press Enter to skip)

  [1] Docker + docker-compose.yml
  [2] GitHub Actions CI/CD pipeline
  [3] ESLint + Prettier config
  [4] Vitest / Jest unit test setup
  [5] Playwright E2E test setup
  [6] Environment config (.env.example)
  [7] Nginx reverse proxy config

>
```

---

## Step 7 — CONFIRM BEFORE GENERATING

**Do not generate any files until the user types GO.**

Show the full plan:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S WHAT I'LL BUILD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack:      [Frontend] + [Backend] + [Database]
Auth:       [Auth choice]
Deployment: [Target]
Extras:     [Selected extras]

PROJECT STRUCTURE:
[app-name]/
├── client/                  # [Framework] frontend
│   ├── src/
│   ├── [config files]
│   └── package.json
├── server/                  # Node.js [framework] backend
│   ├── src/
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── models/          (if database selected)
│   │   └── index.ts
│   └── package.json
├── docker-compose.yml       (if selected)
├── .github/workflows/       (if CI/CD selected)
└── CLAUDE.md

FILES I'LL CREATE:
  □ client/ — [Framework] app scaffold
  □ server/ — Node.js [framework] with [routes]
  □ server/.env.example
  [other selected extras]

COMMANDS I'LL RUN:
  □ [scaffold command for frontend]
  □ npm install in server/
  [any other commands]

DEPLOY STEPS: (if requested)
  □ Generate Nginx config for [domain]
  □ Generate systemd service
  □ Generate deploy script

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to build this, CHANGE [item] to adjust anything,
or ask any questions before I start.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 8 — Generate Project

After GO, generate in this order:

### server/
```
server/
├── src/
│   ├── index.ts             # Entry point, app + server setup
│   ├── routes/
│   │   ├── index.ts         # Route aggregator
│   │   └── health.ts        # GET /health
│   ├── middleware/
│   │   ├── errorHandler.ts
│   │   └── requestLogger.ts
│   ├── config/
│   │   └── env.ts           # Validates env vars on startup
│   └── [db/
│       └── index.ts]        # DB connection if selected
├── .env.example
├── tsconfig.json
└── package.json
```

Key files to generate fully:

**src/index.ts:**
```typescript
import express from 'express'
import cors from 'cors'
import { router } from './routes'
import { errorHandler } from './middleware/errorHandler'
import { env } from './config/env'

const app = express()

app.use(cors({ origin: env.CLIENT_URL }))
app.use(express.json())
app.use('/api', router)
app.use(errorHandler)

app.listen(env.PORT, () => {
  console.log(`Server running on port ${env.PORT}`)
})
```

**src/config/env.ts:**
```typescript
const required = (key: string): string => {
  const value = process.env[key]
  if (!value) throw new Error(`Missing env var: ${key}`)
  return value
}

export const env = {
  PORT: parseInt(process.env.PORT || '3001'),
  NODE_ENV: process.env.NODE_ENV || 'development',
  CLIENT_URL: process.env.CLIENT_URL || 'http://localhost:5173',
  DATABASE_URL: process.env.DATABASE_URL || '',
}
```

### client/
Scaffold with the chosen framework command, then add:
- API client utility (`src/lib/api.ts`) pre-configured to hit `server/`
- Basic routing setup
- `.env.example` with `VITE_API_URL=http://localhost:3001`

### docker-compose.yml (if selected)
```yaml
services:
  client:
    build: ./client
    ports: ["5173:5173"]
    environment:
      - VITE_API_URL=http://localhost:3001
    volumes: ["./client:/app", "/app/node_modules"]

  server:
    build: ./server
    ports: ["3001:3001"]
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
    depends_on: [db]
    volumes: ["./server:/app", "/app/node_modules"]

  db:                          # if PostgreSQL selected
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes: ["pgdata:/var/lib/postgresql/data"]

volumes:
  pgdata:
```

### GitHub Actions CI (if selected)
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
        working-directory: server
      - run: npm test
        working-directory: server
      - run: npm ci
        working-directory: client
      - run: npm run build
        working-directory: client
```

---

## Step 9 — Deployment (if requested)

If a server target was chosen → invoke `skills/deploy/SKILL.md` with:
- App type: Node.js
- Target: as specified
- Domain: as specified

---

## Step 10 — Recommended Skills

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILLS FOR YOUR [Framework + Node] PROJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Essentials
   GSD — plan features in phases, saves ~40% planning tokens
   Claude Code Expert — 54 skills for debugging, review, testing

🟡 For your stack
   UI/UX Pro Max — [Framework] component design, Tailwind patterns
   Code Review Graph — traces component/service dependencies

🟢 If deploying
   Agent Orchestrator — coordinate multi-step deploy tasks

Run /skill-bootstrap to install.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
