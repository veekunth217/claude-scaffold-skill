---
name: db
description: Full database skill — MySQL, PostgreSQL, MongoDB, Redis, ScyllaDB, Meilisearch — setup, queries, optimization, backups, debugging
version: 1.0.0
author: veekunth217
tags: [mysql, postgresql, mongodb, redis, scylladb, meilisearch, database, optimization, backup, slow-query]
platforms: [claude-code, cursor, codex]
---

# Database Skill

Full-stack database expertise — relational, document, wide-column, cache, and search. From initial setup to production tuning.

**RULE: Show all schema changes, config changes, and migrations before applying. Wait for GO.**

---

## MySQL — Setup & Optimization

### Installation (Ubuntu)
```bash
apt-get install -y mysql-server
mysql_secure_installation
```

### Key tuning (my.cnf)
```ini
[mysqld]
innodb_buffer_pool_size = 1G          # 70-80% of RAM for DB-only servers
innodb_buffer_pool_instances = 4      # 1 per GB of buffer pool
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2    # slightly less durable, much faster
innodb_flush_method = O_DIRECT
query_cache_type = 0                  # disabled in MySQL 8+
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 1
max_connections = 200
```

### Common operations
```sql
-- Show running queries
SHOW PROCESSLIST;
SHOW FULL PROCESSLIST;

-- Explain a slow query
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
EXPLAIN ANALYZE SELECT ...;           -- MySQL 8+

-- Check index usage
SHOW INDEX FROM table_name;

-- Add index
ALTER TABLE orders ADD INDEX idx_user_created (user_id, created_at);

-- Backup
mysqldump -u root -p --single-transaction --routines --triggers mydb > backup.sql
```

---

## PostgreSQL — Setup & Optimization

### Installation (Ubuntu)
```bash
apt-get install -y postgresql postgresql-contrib
sudo -u postgres psql
```

### Key tuning (postgresql.conf)
```ini
shared_buffers = 256MB               # 25% of RAM
effective_cache_size = 1GB           # 75% of RAM
work_mem = 16MB                      # per sort/hash operation
maintenance_work_mem = 256MB
wal_buffers = 16MB
checkpoint_completion_target = 0.9
random_page_cost = 1.1               # for SSD
effective_io_concurrency = 200       # for SSD
max_connections = 100
shared_preload_libraries = 'pg_stat_statements'
```

### pg_stat_statements (slow query analysis)
```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

### Common operations
```sql
-- List all databases/tables
\l
\dt

-- Explain + analyze
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = $1;

-- Index types
CREATE INDEX CONCURRENTLY idx_orders_user ON orders(user_id);  -- no table lock
CREATE INDEX idx_gin ON posts USING gin(to_tsvector('english', content));  -- full-text

-- Backup
pg_dump -U postgres -Fc mydb > mydb.dump
pg_restore -U postgres -d mydb mydb.dump
```

---

## MongoDB — Setup & Configuration

### Installation (Ubuntu)
```bash
# Add MongoDB 7 repo
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg -o /usr/share/keyrings/mongodb.gpg --dearmor
echo "deb [ signed-by=/usr/share/keyrings/mongodb.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" > /etc/apt/sources.list.d/mongodb-org-7.0.list
apt-get update && apt-get install -y mongodb-org
systemctl enable --now mongod
```

### mongod.conf (production)
```yaml
storage:
  dbPath: /var/lib/mongodb
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1          # 50% of RAM minus OS overhead

net:
  bindIp: 127.0.0.1           # never 0.0.0.0 without auth
  port: 27017

security:
  authorization: enabled

operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp
```

### Common operations
```js
// Explain a slow query
db.orders.find({ userId: ObjectId("...") }).explain("executionStats")

// Create indexes
db.orders.createIndex({ userId: 1, createdAt: -1 })
db.products.createIndex({ name: "text", description: "text" })  // text search

// Aggregation pipeline
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $group: { _id: "$userId", total: { $sum: "$amount" } } },
  { $sort: { total: -1 } },
  { $limit: 10 }
])

// Backup
mongodump --db mydb --out /backup/$(date +%Y%m%d)
mongorestore --db mydb /backup/20260504/mydb
```

---

## Redis — Setup & Configuration

### Installation (Ubuntu)
```bash
apt-get install -y redis-server
```

### redis.conf (production)
```conf
bind 127.0.0.1
port 6379
requirepass [strong-password]
maxmemory 512mb
maxmemory-policy allkeys-lru      # for pure cache
# maxmemory-policy volatile-lru   # if mixing cache + persistent keys
appendonly no                     # disable for pure cache use
save ""                           # disable RDB for pure cache

# For session/persistent use — enable persistence:
# appendonly yes
# appendfsync everysec
```

### Patterns
```bash
# Monitor live commands
redis-cli MONITOR

# Memory analysis
redis-cli --memkeys                # memory by key pattern
redis-cli INFO memory

# Flush (careful in prod)
redis-cli FLUSHDB                  # current DB only
redis-cli FLUSHALL                 # ALL databases
```

---

## ScyllaDB — Setup & Configuration

### Installation (Ubuntu/Docker)
```bash
# Docker (easiest for dev)
docker run -d --name scylla \
  -p 9042:9042 \
  -v scylla-data:/var/lib/scylla \
  scylladb/scylla:5.4 \
  --smp 2 --memory 2G --overprovisioned 1

# Check it's up
docker exec -it scylla nodetool status
```

### scylla.yaml (production key settings)
```yaml
cluster_name: 'my-cluster'
num_tokens: 256
authenticator: PasswordAuthenticator
authorizer: CassandraAuthorizer
commitlog_sync: periodic
commitlog_sync_period_in_ms: 10000
compaction_throughput_mb_per_sec: 16
read_request_timeout_in_ms: 5000
write_request_timeout_in_ms: 2000
```

### Schema design (access-pattern-first)
```sql
-- CREATE KEYSPACE first
CREATE KEYSPACE myapp
  WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': 3}
  AND durable_writes = true;

-- Design tables around queries, NOT entities
-- Query: "get messages in a room, newest first"
CREATE TABLE messages_by_room (
  room_id   UUID,
  sent_at   TIMESTAMP,
  msg_id    UUID,
  sender_id UUID,
  body      TEXT,
  PRIMARY KEY ((room_id), sent_at, msg_id)
) WITH CLUSTERING ORDER BY (sent_at DESC)
  AND default_time_to_live = 2592000;  -- 30 day TTL

-- Always use prepared statements
-- Never use ALLOW FILTERING in production
-- Page results with paging_state, never OFFSET
```

---

## Meilisearch — Setup & Configuration

### Installation
```bash
# Docker (recommended)
docker run -d --name meilisearch \
  -p 7700:7700 \
  -v meilisearch-data:/meili_data \
  -e MEILI_MASTER_KEY='[strong-key]' \
  -e MEILI_ENV=production \
  getmeili/meilisearch:v1.8

# Or binary
curl -L https://install.meilisearch.com | sh
./meilisearch --master-key '[key]' --env production
```

### config.toml (production)
```toml
env = "production"
master_key = "[strong-master-key]"
db_path = "/var/lib/meilisearch/data"
dump_dir = "/var/lib/meilisearch/dumps"
snapshot_dir = "/var/lib/meilisearch/snapshots"
http_addr = "127.0.0.1:7700"       # bind to localhost, proxy via Nginx
log_level = "WARN"
max_indexing_memory = "512 MiB"
```

### Nginx reverse proxy for Meilisearch
```nginx
location /search/ {
  proxy_pass http://127.0.0.1:7700/;
  proxy_set_header Host $host;
  # Only expose search endpoint, not admin
  limit_except GET { deny all; }
}
```

### Index setup & search (Node.js SDK)
```typescript
import { MeiliSearch } from 'meilisearch'

const client = new MeiliSearch({
  host: 'http://127.0.0.1:7700',
  apiKey: process.env.MEILI_MASTER_KEY,
})

// Create index with primary key
await client.createIndex('products', { primaryKey: 'id' })

// Configure searchable + filterable attributes
await client.index('products').updateSettings({
  searchableAttributes: ['name', 'description', 'tags'],
  filterableAttributes: ['category', 'price', 'in_stock'],
  sortableAttributes: ['price', 'created_at'],
  rankingRules: ['words', 'typo', 'proximity', 'attribute', 'sort', 'exactness'],
})

// Add documents
await client.index('products').addDocuments(products)

// Search
const results = await client.index('products').search('wireless headphones', {
  filter: ['category = "electronics"', 'price < 100', 'in_stock = true'],
  sort: ['price:asc'],
  limit: 20,
  offset: 0,
  attributesToHighlight: ['name', 'description'],
})
```

### Sync from primary DB (PostgreSQL → Meilisearch)
```typescript
// Pattern: full re-index + incremental sync
async function syncToMeilisearch() {
  const products = await db.select().from(productsTable)
    .where(gt(productsTable.updatedAt, lastSyncAt))

  if (products.length === 0) return

  await client.index('products').addDocuments(products, { primaryKey: 'id' })
  await updateLastSyncTimestamp()
}

// Run every 5 minutes via cron or queue job
```

---

## Backup Strategies

| Database | Backup command | Restore |
|---|---|---|
| MySQL | `mysqldump --single-transaction mydb > db.sql` | `mysql mydb < db.sql` |
| PostgreSQL | `pg_dump -Fc mydb > db.dump` | `pg_restore -d mydb db.dump` |
| MongoDB | `mongodump --db mydb --out /backup/` | `mongorestore /backup/mydb/` |
| Redis | `redis-cli BGSAVE` → copy `/var/lib/redis/dump.rdb` | Copy back + restart |
| ScyllaDB | `nodetool snapshot myks` | `sstableloader` |
| Meilisearch | `curl -X POST 'http://localhost:7700/dumps'` | Restart with dump |

---

## Slow Query Debugging

```bash
# MySQL — enable slow log temporarily
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.5;
SHOW VARIABLES LIKE 'slow_query_log_file';

# PostgreSQL — pg_stat_statements
SELECT query, calls, mean_exec_time FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

# MongoDB — profiler
db.setProfilingLevel(1, { slowms: 100 })
db.system.profile.find().sort({ ts: -1 }).limit(10)

# Redis — slowlog
redis-cli SLOWLOG GET 10
redis-cli SLOWLOG RESET
```
