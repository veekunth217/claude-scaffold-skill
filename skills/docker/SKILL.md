---
name: docker
description: Docker best practices — Dockerfile authoring, docker-compose, multi-stage builds, container networking, volume management, Docker in CI/CD
version: 1.0.0
author: veekunth217
tags: [docker, dockerfile, docker-compose, multi-stage, containers, networking, volumes, cicd, buildkit]
platforms: [claude-code, cursor, codex]
---

# Docker Skill

Production Docker — from optimised Dockerfiles to multi-service compose stacks and CI/CD integration.

**RULE: Show Dockerfile and compose files before building. Warn before any `docker system prune` or volume removal.**

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

### Dockerfile Best Practices
<!-- TODO: Layer caching strategy, .dockerignore, non-root user -->
<!-- TODO: COPY vs ADD, ARG vs ENV, ENTRYPOINT vs CMD -->
<!-- TODO: Healthcheck instruction, signal handling (tini/dumb-init) -->
<!-- TODO: Minimal base images (alpine, distroless, scratch) -->

### docker-compose Setup
<!-- TODO: Services, networks, volumes, depends_on with healthcheck -->
<!-- TODO: Override files (docker-compose.override.yml for dev) -->
<!-- TODO: Profiles for optional services (--profile tools) -->
<!-- TODO: Secrets in compose, environment file patterns -->

### Multi-Stage Builds
<!-- TODO: Builder stage (full deps) → runner stage (minimal) -->
<!-- TODO: Node.js: build stage with devDeps → runtime with only dist/ -->
<!-- TODO: Go: compile stage → scratch runtime (5MB binary) -->
<!-- TODO: Python: venv in builder → copy to slim runtime -->

### Container Networking
<!-- TODO: Bridge, host, overlay networks -->
<!-- TODO: Service discovery by name in compose -->
<!-- TODO: Exposing ports vs internal-only services -->
<!-- TODO: Connecting to host services from container (host.docker.internal) -->

### Volume Management
<!-- TODO: Named volumes vs bind mounts vs tmpfs -->
<!-- TODO: Volume backup strategies (docker run --volumes-from) -->
<!-- TODO: Dev workflow: bind mount source code for hot reload -->
<!-- TODO: Database volumes: never bind-mount prod DB data -->

### Docker in CI/CD
<!-- TODO: GitHub Actions docker/build-push-action, layer cache with gha -->
<!-- TODO: BuildKit cache mounts (pip, npm, apt) -->
<!-- TODO: Multi-platform builds (buildx, amd64 + arm64) -->
<!-- TODO: ECR/GHCR push, image signing (cosign) -->

---

## Templates

### Node.js multi-stage
```dockerfile
# Stage 1: build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: runtime
FROM node:20-alpine AS runner
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/package.json .
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=5s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### Python multi-stage
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

FROM python:3.12-slim AS runner
RUN useradd -m app
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --chown=app:app . .
USER app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### .dockerignore
```
node_modules/
.venv/
__pycache__/
*.pyc
.git/
.env
.env.*
dist/
build/
*.log
README.md
.DS_Store
```

<!-- TODO: Add full interactive workflows for each capability above -->
