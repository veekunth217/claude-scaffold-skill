---
name: database
description: Database setup wizard — PostgreSQL, ScyllaDB/Cassandra, Redis — schema design, migrations, query patterns, and connection setup
version: 1.0.0
author: veekunth217
tags: [postgres, postgresql, scylladb, cassandra, redis, database, migrations, orm, prisma, drizzle]
platforms: [claude-code, cursor, codex]
---

# Database Setup Wizard

You are a database specialist. Help the user set up, design, and query their database correctly — with the right ORM/driver, schema, and query patterns for their use case.

**RULE: Show full plan and wait for GO before generating any schema, migration, or config.**

---

## Step 1 — Which Database?

```
Which database are you working with?

RELATIONAL
  1. PostgreSQL — best general-purpose, ACID, great for most apps
  2. MySQL / MariaDB — widely supported, common in LAMP stacks

WIDE-COLUMN / TIME-SERIES
  3. ScyllaDB — high-throughput, low-latency, Cassandra-compatible
  4. Apache Cassandra — distributed, multi-DC, battle-tested at scale

IN-MEMORY / CACHE
  5. Redis — caching, pub/sub, queues, sessions, rate limiting

DOCUMENT
  6. MongoDB — flexible schema, nested documents

Not sure which to use?
  Tell me your use case and I'll recommend one.
```

---

## Step 2 — For PostgreSQL: ORM or Driver

```
How do you want to interact with PostgreSQL?

  1. Prisma (ORM) — type-safe, great DX, auto-generated client,
                    migrations via prisma migrate
  2. Drizzle (ORM) — lightweight, SQL-like syntax, TypeScript-first,
                     fastest runtime performance
  3. raw pg driver — full SQL control, no abstraction overhead
  4. Kysely — query builder, TypeScript-first, no magic
```

---

## Step 3 — Describe Your Data Model

```
Describe your entities and their relationships.

Example:
  "Users have many Posts. Posts have many Comments.
   Users can Like posts and comments.
   Posts have Tags (many-to-many)."

I'll generate:
  - Schema / DDL
  - ORM model definitions
  - Migration files
  - Common query patterns for your use case
```

---

## Step 4 — CONFIRM BEFORE GENERATING

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S MY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Database:  [chosen DB]
Access:    [ORM/driver choice]
Entities:  [listed from description]

FILES I'LL GENERATE:
  □ [schema file — prisma/schema.prisma or schema.ts]
  □ [migration file]
  □ [connection/client setup]
  □ [query examples for each entity]
  □ [docker-compose for local DB]
  □ .env.example with DB connection string

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to generate, or ask anything first.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5 — Generate

### PostgreSQL + Prisma

**prisma/schema.prisma:**
Generate complete schema with all models, relations, indexes, and `@@map` for snake_case table names:
```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String    @id @default(cuid())
  email     String    @unique
  name      String?
  posts     Post[]
  likes     Like[]
  createdAt DateTime  @default(now())
  updatedAt DateTime  @updatedAt

  @@map("users")
}
// ... all other entities
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

**Common query patterns generated per entity:**
```typescript
// src/db/queries/users.ts
export const userQueries = {
  findById: (id: string) =>
    db.user.findUnique({ where: { id }, include: { posts: true } }),

  findByEmail: (email: string) =>
    db.user.findUnique({ where: { email } }),

  create: (data: Prisma.UserCreateInput) =>
    db.user.create({ data }),

  paginate: (page: number, perPage = 20) =>
    db.user.findMany({
      skip: (page - 1) * perPage,
      take: perPage,
      orderBy: { createdAt: 'desc' },
    }),
}
```

**Migration commands:**
```bash
npx prisma migrate dev --name init
npx prisma generate
npx prisma studio     # visual DB browser
```

---

### PostgreSQL + Drizzle

**src/db/schema.ts:**
```typescript
import { pgTable, text, timestamp, uuid } from 'drizzle-orm/pg-core'

export const users = pgTable('users', {
  id:        uuid('id').primaryKey().defaultRandom(),
  email:     text('email').notNull().unique(),
  name:      text('name'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
})

export const posts = pgTable('posts', {
  id:       uuid('id').primaryKey().defaultRandom(),
  title:    text('title').notNull(),
  content:  text('content'),
  authorId: uuid('author_id').references(() => users.id, { onDelete: 'cascade' }),
  // ...
})
```

**Query patterns:**
```typescript
import { eq, desc, and } from 'drizzle-orm'

// Find user with posts
const user = await db.query.users.findFirst({
  where: eq(users.id, id),
  with: { posts: { orderBy: desc(posts.createdAt) } }
})

// Paginated query
const result = await db.select().from(posts)
  .where(eq(posts.authorId, userId))
  .orderBy(desc(posts.createdAt))
  .limit(20).offset((page - 1) * 20)
```

---

### ScyllaDB / Cassandra

**Key principle:** Design tables around queries, not entities.

First ask:
```
For ScyllaDB, I need your access patterns BEFORE designing the schema.

List your most common queries:
  Example:
  - "Get all posts by a user, ordered by time"
  - "Get post by ID"
  - "Get all comments on a post"
  - "Get user's activity feed (all likes/comments) by time"
```

Then generate CQL DDL driven by those patterns:
```sql
-- One table per query pattern
CREATE KEYSPACE IF NOT EXISTS [keyspace]
  WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};

-- Pattern: "Get posts by user, ordered by time"
CREATE TABLE posts_by_user (
  user_id   UUID,
  created_at TIMESTAMP,
  post_id   UUID,
  title     TEXT,
  content   TEXT,
  PRIMARY KEY ((user_id), created_at, post_id)
) WITH CLUSTERING ORDER BY (created_at DESC);

-- Pattern: "Get post by ID"
CREATE TABLE posts_by_id (
  post_id UUID PRIMARY KEY,
  title   TEXT,
  content TEXT,
  user_id UUID,
  created_at TIMESTAMP
);
```

**Connection setup:**
```typescript
// src/db/scylla.ts
import { Client, types } from 'cassandra-driver'

export const scylla = new Client({
  contactPoints: (process.env.SCYLLA_HOSTS || 'localhost').split(','),
  localDataCenter: process.env.SCYLLA_DC || 'datacenter1',
  keyspace: process.env.SCYLLA_KEYSPACE,
  credentials: {
    username: process.env.SCYLLA_USER || 'cassandra',
    password: process.env.SCYLLA_PASS || 'cassandra',
  },
  pooling: { coreConnectionsPerHost: { [types.distance.local]: 4 } }
})

export async function connectScylla() {
  await scylla.connect()
  console.log(`Connected to ScyllaDB: ${scylla.hosts.keys().next().value}`)
}
```

**Prepared statement pattern (always use these, never raw strings):**
```typescript
const GET_POSTS = 'SELECT * FROM posts_by_user WHERE user_id = ? LIMIT ?'
const result = await scylla.execute(GET_POSTS, [userId, 20], { prepare: true })
```

**Important ScyllaDB caveats to always explain:**
- No JOINs — denormalize data into query-specific tables
- No transactions across partitions — use lightweight transactions (LWT) for single-partition atomicity
- Pagination via paging state, not OFFSET
- TTL for time-expiring data (sessions, caches)

---

### Redis

```
What will you use Redis for?
(can select multiple)

  [1] Caching (with TTL)
  [2] Session storage
  [3] Rate limiting
  [4] Pub/Sub messaging
  [5] Job queues (with BullMQ)
  [6] Leaderboards / sorted sets
```

Generate connection + patterns for each selected use:

```typescript
// src/db/redis.ts
import { createClient } from 'redis'

export const redis = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
})

redis.on('error', (err) => console.error('Redis error:', err))
await redis.connect()

// Cache helper
export const cache = {
  get: <T>(key: string): Promise<T | null> =>
    redis.get(key).then(v => v ? JSON.parse(v) : null),

  set: (key: string, value: unknown, ttlSeconds = 3600) =>
    redis.set(key, JSON.stringify(value), { EX: ttlSeconds }),

  del: (key: string) => redis.del(key),

  getOrSet: async <T>(key: string, fn: () => Promise<T>, ttl = 3600): Promise<T> => {
    const cached = await cache.get<T>(key)
    if (cached) return cached
    const value = await fn()
    await cache.set(key, value, ttl)
    return value
  }
}
```

---

### docker-compose for local dev (always generated)

```yaml
services:
  postgres:                        # if PostgreSQL
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: ${DB_NAME:-appdb}
      POSTGRES_USER: ${DB_USER:-user}
      POSTGRES_PASSWORD: ${DB_PASS:-password}
    ports: ["5432:5432"]
    volumes: ["pgdata:/var/lib/postgresql/data"]

  scylla:                          # if ScyllaDB
    image: scylladb/scylla:5.4
    command: --smp 1 --memory 512M --overprovisioned 1
    ports: ["9042:9042", "9160:9160"]
    volumes: ["scylladata:/var/lib/scylla"]

  redis:                           # if Redis
    image: redis:7-alpine
    command: redis-server --appendonly yes
    ports: ["6379:6379"]
    volumes: ["redisdata:/data"]

volumes:
  pgdata:
  scylladata:
  redisdata:
```
