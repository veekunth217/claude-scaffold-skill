---
name: server
description: Linux server setup & tuning — Nginx, PHP-FPM, SSL/Certbot, UFW, Redis, MySQL/PostgreSQL, PM2, DigitalOcean Droplet
version: 1.0.0
author: veekunth217
tags: [nginx, php-fpm, ssl, certbot, ufw, fail2ban, redis, mysql, postgresql, pm2, digitalocean, ubuntu, server]
platforms: [claude-code, cursor, codex]
---

# Server Skill

Production Linux server setup, configuration, and tuning — from fresh Droplet to fully hardened, optimised web server.

**RULE: Show every command before running. For destructive ops (UFW enable, service restart), always confirm.**

> **🚧 Status: Stub — implementation pending**
>
> This reference skill has the structure but the snippet content is still being filled in
> (you'll see `<!-- TODO -->` placeholders below). It activates and tells Claude the topic
> exists, but won't yield deep snippets yet.
>
> **Want to help?** Pick any TODO, write the snippet, open a PR. See [CONTRIBUTING.md](../../CONTRIBUTING.md).
> Each contribution moves the skill closer to "Ready" status.

---

## Capabilities

### Nginx Configuration
<!-- TODO: Server blocks, upstream proxies, gzip, HTTP/2, rate limiting -->
<!-- TODO: nginx.conf tuning (worker_processes, worker_connections, keepalive) -->
<!-- TODO: Nginx as reverse proxy for Node/Python/PHP -->
<!-- TODO: Static file caching headers, try_files patterns -->

### PHP-FPM Tuning
<!-- TODO: Pool config (pm = dynamic vs ondemand vs static) -->
<!-- TODO: max_children calculation based on RAM -->
<!-- TODO: PHP-FPM status page, slow log -->
<!-- TODO: opcache settings for production -->

### SSL / Let's Encrypt (Certbot)
<!-- TODO: Certbot install, --nginx plugin, wildcard certs via DNS challenge -->
<!-- TODO: Auto-renewal, pre/post hooks -->
<!-- TODO: SSL hardening (TLS 1.2+, ciphers, HSTS, OCSP stapling) -->

### UFW Firewall Rules
<!-- TODO: Basic ruleset (SSH, HTTP, HTTPS, custom ports) -->
<!-- TODO: Limiting SSH brute force with UFW rate limit -->
<!-- TODO: Allow by IP range, delete rules -->

### Redis Setup & Tuning
<!-- TODO: Redis install, bind config, requirepass, maxmemory + eviction policy -->
<!-- TODO: Redis as PHP session handler, WP object cache -->
<!-- TODO: Redis persistence (RDB vs AOF), replication basics -->

### MySQL / PostgreSQL Tuning
<!-- TODO: MySQL: innodb_buffer_pool_size, query cache (off in 8.0), slow query log -->
<!-- TODO: PostgreSQL: shared_buffers, work_mem, pg_stat_statements -->
<!-- TODO: Backup strategies: mysqldump, pg_dump, automated cron -->

### PM2 Process Management
<!-- TODO: ecosystem.config.js, cluster mode, log rotation -->
<!-- TODO: PM2 startup systemd, monit integration -->
<!-- TODO: Zero-downtime reload, graceful shutdown -->

### DigitalOcean Droplet Setup
<!-- TODO: Initial hardening (disable root, SSH key only, fail2ban) -->
<!-- TODO: Swap setup for low-RAM droplets -->
<!-- TODO: DO monitoring agent, droplet metrics -->

---

## Quick Configs

### Nginx performance baseline
```nginx
worker_processes auto;
worker_rlimit_nofile 65535;
events { worker_connections 4096; multi_accept on; }
http {
  sendfile on; tcp_nopush on; tcp_nodelay on;
  keepalive_timeout 65; keepalive_requests 100;
  gzip on; gzip_types text/plain text/css application/json application/javascript;
  gzip_comp_level 5; gzip_min_length 256;
  server_tokens off;
}
```

### PHP-FPM pool calculation
```
RAM for PHP = Total RAM - OS (200MB) - MySQL (25%) - Redis (10%)
max_children = RAM for PHP / avg PHP process size (typically 30-50MB)
start_servers = max_children / 4
min_spare_servers = max_children / 4
max_spare_servers = max_children / 2
```

### UFW baseline
```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp comment 'SSH'
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'
ufw limit 22/tcp comment 'SSH rate limit'
ufw --force enable
```

<!-- TODO: Add full interactive workflows for each capability above -->
