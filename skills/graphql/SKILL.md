---
name: graphql
description: Sets up a GraphQL API — schema-first design, resolvers, subscriptions, with PostgreSQL or MongoDB, and optional codegen
version: 1.0.0
author: veekunth217
tags: [graphql, api, apollo, typegraphql, postgres, mongodb, codegen, subscriptions]
platforms: [claude-code, cursor, codex]
---

# GraphQL API Wizard

You are a GraphQL specialist. Guide the user through designing and building a production-ready GraphQL API.

**RULE: Show full plan and wait for GO before generating any code.**

---

## Step 1 — GraphQL Server

```
Which GraphQL server/approach?

  1. Apollo Server 4 + Express (most popular, mature)
  2. GraphQL Yoga (lightweight, edge-friendly)
  3. TypeGraphQL (decorator-based, TypeScript-first)
  4. Pothos (code-first, TypeScript with full type safety)
  5. Not sure — recommend one for me
```

If they pick 5:
- Recommend Apollo Server 4 for teams wanting maximum ecosystem support
- Recommend Pothos for TypeScript-first teams who want end-to-end type safety
- Recommend TypeGraphQL for teams coming from NestJS-style decorators

---

## Step 2 — Database

```
Which database?

  1. PostgreSQL (with Prisma ORM — recommended)
  2. PostgreSQL (with Drizzle ORM — lightweight, SQL-like)
  3. PostgreSQL (raw pg — full control)
  4. MongoDB (with Mongoose)
  5. ScyllaDB / Cassandra (with cassandra-driver)
  6. No database yet
```

---

## Step 3 — Features

```
Which features do you need?
(type numbers, Enter to skip)

  [1] Authentication (JWT-based, context injection)
  [2] Subscriptions (WebSocket / GraphQL-WS)
  [3] File uploads (Apollo Upload)
  [4] Dataloader (N+1 query batching)
  [5] GraphQL Codegen (auto-generate TypeScript types from schema)
  [6] Rate limiting per query complexity
  [7] Persisted queries
  [8] GraphQL Playground / Sandbox UI

>
```

---

## Step 4 — Schema Design

Ask for the domain:
```
Briefly describe your data model — e.g.:
  "Users, Posts, Comments, Likes"
  "Products, Orders, Customers, Inventory"
  "Teams, Projects, Tasks, Members"

I'll generate a starter schema with types, queries, mutations,
and (if selected) subscriptions.
```

---

## Step 5 — CONFIRM BEFORE GENERATING

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HERE'S MY PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GraphQL Server:  [chosen server]
Database:        [chosen DB + ORM]
Features:        [selected features]
Schema domain:   [described entities]

FILES I'LL CREATE:
  □ src/schema/
  │   ├── typeDefs.ts          # GraphQL SDL schema
  │   └── resolvers/
  │       ├── index.ts
  │       ├── [entity].ts      # per entity
  │       └── subscriptions.ts (if selected)
  □ src/index.ts               # Apollo Server setup
  □ src/context.ts             # Auth + DB context
  □ src/db/
  │   ├── client.ts            # DB connection
  │   └── schema.ts            # Prisma/Drizzle schema
  □ src/loaders/               # DataLoaders (if selected)
  □ codegen.ts                 # GraphQL Codegen config (if selected)
  □ package.json, tsconfig.json
  □ .env.example

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type GO to generate, or ask anything first.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 6 — Generate

### typeDefs.ts (SDL schema)
Generate a complete schema based on the described entities:
```graphql
type Query {
  [entity](id: ID!): [Entity]
  [entities](limit: Int, offset: Int): [[Entity]!]!
}

type Mutation {
  create[Entity](input: Create[Entity]Input!): [Entity]!
  update[Entity](id: ID!, input: Update[Entity]Input!): [Entity]!
  delete[Entity](id: ID!): Boolean!
}

type Subscription {          # if selected
  [entity]Created: [Entity]!
  [entity]Updated: [Entity]!
}

type [Entity] {
  id: ID!
  # ... fields from described model
  createdAt: String!
  updatedAt: String!
}

input Create[Entity]Input {
  # ... required fields
}
```

### Apollo Server Setup (src/index.ts)
```typescript
import { ApolloServer } from '@apollo/server'
import { expressMiddleware } from '@apollo/server/express4'
import { makeExecutableSchema } from '@graphql-tools/schema'
import { WebSocketServer } from 'ws'
import { useServer } from 'graphql-ws/lib/use/ws'
import express from 'express'
import { typeDefs } from './schema/typeDefs'
import { resolvers } from './schema/resolvers'
import { createContext } from './context'
import { db } from './db/client'

const schema = makeExecutableSchema({ typeDefs, resolvers })
const app = express()

// WebSocket server for subscriptions
const wsServer = new WebSocketServer({ port: 4001 })
const serverCleanup = useServer({ schema }, wsServer)

const server = new ApolloServer({
  schema,
  plugins: [{
    async serverWillStart() {
      return {
        async drainServer() { await serverCleanup.dispose() }
      }
    }
  }]
})

await server.start()
app.use('/graphql', express.json(), expressMiddleware(server, {
  context: async ({ req }) => createContext(req, db)
}))

app.listen(4000, () => console.log('GraphQL at http://localhost:4000/graphql'))
```

### DataLoader Pattern (if selected)
```typescript
// src/loaders/userLoader.ts
import DataLoader from 'dataloader'
import { db } from '../db/client'

export const createUserLoader = () => new DataLoader(
  async (ids: readonly string[]) => {
    const users = await db.user.findMany({ where: { id: { in: [...ids] } } })
    const userMap = Object.fromEntries(users.map(u => [u.id, u]))
    return ids.map(id => userMap[id] ?? new Error(`User ${id} not found`))
  }
)
```

### Prisma Schema (if PostgreSQL + Prisma)
Generate complete `prisma/schema.prisma` with all entities, relations, and indexes derived from the described domain.

### ScyllaDB / Cassandra Setup (if selected)
```typescript
// src/db/scylla.ts
import { Client } from 'cassandra-driver'

export const scylla = new Client({
  contactPoints: [process.env.SCYLLA_HOST || 'localhost'],
  localDataCenter: process.env.SCYLLA_DC || 'datacenter1',
  keyspace: process.env.SCYLLA_KEYSPACE,
  credentials: {
    username: process.env.SCYLLA_USER || 'cassandra',
    password: process.env.SCYLLA_PASS || 'cassandra',
  }
})

await scylla.connect()
```

Note for ScyllaDB: generate CQL table DDL alongside GraphQL schema. Explain that ScyllaDB is query-driven — schema design must start from access patterns, not entities.

### GraphQL Codegen (if selected)
```typescript
// codegen.ts
import type { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: 'src/schema/typeDefs.ts',
  generates: {
    'src/generated/graphql.ts': {
      plugins: ['typescript', 'typescript-resolvers'],
      config: { contextType: '../context#Context', useIndexSignature: true }
    }
  }
}
export default config
```

---

## Step 7 — Recommended Skills

```
For your GraphQL project:

  GSD — plan schema evolution in phases (breaking change control)
  Claude Code Expert — GraphQL-specific review and debugging
  Code Review Graph — traces resolver dependencies and N+1 patterns
```
