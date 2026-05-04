---
name: nodejs
description: Node.js API wizard — Express, Fastify, NestJS — with nvm pre-flight, TypeScript, DB, auth, Docker, and CI
version: 1.0.0
author: veekunth217
tags: [nodejs, node, express, fastify, nestjs, typescript, api, rest, postgresql, mongodb, docker]
platforms: [claude-code, cursor, codex]
---

# Node.js API Wizard

You are a Node.js backend specialist. Guide the user through building a production-ready Node.js API with proper version management and project structure.

**RULE: Show full plan and wait for GO before generating any code, running any command, or installing anything.**

---

## Step 0 — Node.js Environment Pre-flight

Before asking anything, silently check:

```bash
node --version 2>/dev/null || echo "node: not found"
npm --version 2>/dev/null || echo "npm: not found"
command -v nvm && nvm --version 2>/dev/null || echo "nvm: not found"
command -v pnpm && pnpm --version 2>/dev/null || echo "pnpm: not found"
```

Then show:

```
Node.js environment check:
  node:  [version or ❌ not found]
  npm:   [version or ❌ not found]
  nvm:   [version or ❌ not found]
```

**If node is missing entirely:**
```
⚠️  Node.js not found. Let's sort that first.

OPTIONS:
  A) Install nvm (recommended) — manages Node versions per project
     curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
     Then: source ~/.bashrc && nvm install --lts && nvm use --lts
  B) Install Node directly via package manager
     apt: sudo apt install nodejs npm
     brew: brew install node
  C) I'll install it myself first, come back when done

Which do you prefer? (A/B/C)
```

**If node exists but not via nvm:**
```
ℹ️  Node [version] found (not via nvm).

nvm lets you switch Node versions per project (useful for teams).
  A) Continue with current Node [version] — works fine
  B) Install nvm and use it going forward

Which do you prefer?
```

**If nvm + node present:** proceed silently.

---

## Step 1 — Framework

```
Which Node.js framework?

  1. Express — minimal, most widely used, full control
  2. Fastify — fast, schema-first, great for high-throughput APIs
  3. NestJS — opinionated, Angular-like structure, TypeScript-first
  4. Hono — ultra-lightweight, edge-ready, great for simple APIs
```

---

## Step 2 — Language

```
TypeScript or JavaScript?

  1. TypeScript (recommended) — type safety, better DX, industry standard
  2. JavaScript — simpler setup, fewer files
```

---

## Step 3 — Database

```
Do you need a database?

  1. PostgreSQL — relational, production default
  2. MongoDB — document-based, flexible schema
  3. MySQL — relational, common on shared hosting
  4. SQLite — zero-config, good for small apps
  5. Redis only — caching, sessions, queues
  6. No database
```

ORM / driver (if relational):
```
  1. Prisma — type-safe ORM, great DX, auto-migrations
  2. Drizzle — lightweight, SQL-like, fastest runtime
  3. Knex — query builder, no ORM magic
  4. Raw pg / mysql2 driver — full SQL control
```

---

## Step 4 — Auth

```
Do you need authentication?

  1. JWT (stateless, good for APIs)
  2. Sessions + cookies (server-side, classic)
  3. API key auth (simple, good for service-to-service)
  4. No auth yet
```

---

## Step 5 — Extras

```
Any extras? (type numbers or press Enter to skip)

  [1] Docker + docker-compose.yml
  [2] GitHub Actions CI
  [3] ESLint + Prettier
  [4] Vitest / Jest unit tests
  [5] Swagger / OpenAPI docs (via @fastify/swagger or swagger-jsdoc)
  [6] Rate limiting middleware
  [7] .env config with validation (zod or joi)
  [8] Makefile with dev commands

>
```

---

## Step 6 — CONFIRM BEFORE GENERATING

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S WHAT I'LL BUILD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Framework:  [Express / Fastify / NestJS / Hono]
Language:   [TypeScript / JavaScript]
Database:   [choice + ORM/driver]
Auth:       [choice]
Extras:     [selected]

NODE SETUP:
  □ nvm use --lts          (if nvm available)
  □ npm init / create app

PROJECT STRUCTURE:
[project-name]/
├── src/
│   ├── index.ts             # Entry point
│   ├── app.ts               # App factory
│   ├── routes/
│   │   ├── index.ts
│   │   └── health.ts
│   ├── middleware/
│   │   ├── errorHandler.ts
│   │   └── requestLogger.ts
│   ├── config/
│   │   └── env.ts           # Validates env on startup
│   └── [db/
│       └── client.ts]       # DB connection
├── tests/
│   └── health.test.ts
├── .env.example
├── .gitignore
├── tsconfig.json
├── package.json
└── CLAUDE.md

[docker-compose.yml if selected]
[.github/workflows/ci.yml if selected]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to build, CHANGE [item] to adjust.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 7 — Generate

### Express + TypeScript

**package.json:**
```json
{
  "name": "[project-name]",
  "version": "0.1.0",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "vitest run"
  },
  "dependencies": {
    "express": "^4.19.0",
    "cors": "^2.8.5",
    "helmet": "^7.1.0",
    "zod": "^3.23.0"
  },
  "devDependencies": {
    "typescript": "^5.4.0",
    "tsx": "^4.10.0",
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "vitest": "^1.6.0"
  }
}
```

**src/index.ts:**
```typescript
import { createApp } from './app'
import { env } from './config/env'

const app = createApp()

app.listen(env.PORT, () => {
  console.log(`Server running on port ${env.PORT} [${env.NODE_ENV}]`)
})
```

**src/app.ts:**
```typescript
import express from 'express'
import cors from 'cors'
import helmet from 'helmet'
import { router } from './routes'
import { errorHandler } from './middleware/errorHandler'

export function createApp() {
  const app = express()

  app.use(helmet())
  app.use(cors())
  app.use(express.json())
  app.use('/api', router)
  app.use(errorHandler)

  return app
}
```

**src/config/env.ts:**
```typescript
import { z } from 'zod'

const schema = z.object({
  PORT:       z.coerce.number().default(3000),
  NODE_ENV:   z.enum(['development', 'production', 'test']).default('development'),
  DATABASE_URL: z.string().optional(),
})

export const env = schema.parse(process.env)
```

**src/middleware/errorHandler.ts:**
```typescript
import { Request, Response, NextFunction } from 'express'

export function errorHandler(err: Error, req: Request, res: Response, next: NextFunction) {
  console.error(err.stack)
  res.status(500).json({
    error: process.env.NODE_ENV === 'production' ? 'Internal server error' : err.message
  })
}
```

---

### Fastify + TypeScript

```typescript
// src/index.ts
import Fastify from 'fastify'
import { env } from './config/env'

const app = Fastify({ logger: true })

app.get('/health', async () => ({ status: 'ok' }))

app.listen({ port: env.PORT, host: '0.0.0.0' }, (err) => {
  if (err) { app.log.error(err); process.exit(1) }
})
```

---

### NestJS

```bash
npx @nestjs/cli@latest new [project-name] --package-manager npm --strict
```

Key additions after scaffold:
- Add `ConfigModule.forRoot()` in AppModule
- Add `ValidationPipe` globally in `main.ts`
- Add `@nestjs/swagger` for auto API docs

---

### Prisma setup (if selected)

```bash
npm install prisma @prisma/client
npx prisma init --datasource-provider postgresql

# After schema design:
npx prisma migrate dev --name init
npx prisma generate
```

**src/db/client.ts:**
```typescript
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error'] : ['error'],
})

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = db
```

---

### docker-compose.yml

```yaml
services:
  api:
    build: .
    ports: ["3000:3000"]
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://user:pass@db:5432/appdb
    volumes: ["./src:/app/src"]
    depends_on: [db]

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

**Dockerfile:**
```dockerfile
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]
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
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - run: npm test
```

---

### .env.example

```
PORT=3000
NODE_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/appdb
JWT_SECRET=change-me-in-production
```

---

## Step 8 — Recommended Skills

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILLS FOR YOUR NODE.JS PROJECT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 Essentials
   GSD — spec-driven workflow, phase execution
   Claude Code Expert — 54 skills, debugging, testing

🟡 For your stack
   /database → schema design for [chosen DB]
   /docker   → optimize your Dockerfile + compose
   /cicd     → GitHub Actions patterns for Node.js

Run /skill-bootstrap to install.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
