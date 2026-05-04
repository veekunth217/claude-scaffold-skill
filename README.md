# claude-scaffold-skill

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Skills](https://img.shields.io/badge/Skills-23+-green.svg)
![Registry](https://img.shields.io/badge/Registry-17%20community%20skills-orange.svg)
![Last Updated](https://img.shields.io/badge/Updated-May%202026-lightgrey.svg)
![Validate Registry](https://github.com/veekunth217/claude-scaffold-skill/actions/workflows/validate-registry.yml/badge.svg)

> Scaffold any project. Pick the right skills. Sync your Claude context across all your devices.

A Claude Code skill collection that solves three real developer problems:
1. **Scaffold** — Turn a blank directory into a production-ready project using plain English
2. **Skill discovery** — Find and install the right community skills for your stack (10+ recommendations)
3. **Context sync** — Take your Claude project memory to any machine without losing anything

---

## Prerequisites

- **Claude Code** — [Install here](https://claude.ai/code) if you don't have it
- **Git** — for install and context sync
- **Python 3** — for context sync scripts (`python3 --version` to check)

That's it. No other dependencies.

---

## Install

```bash
git clone https://github.com/veekunth217/claude-scaffold-skill.git \
  ~/.claude/skills/claude-scaffold-skill
```

**Verify it worked** — open Claude Code in any project and type:
```
/scaffold
```
Claude should respond with an environment check and ask what you're building. If nothing happens, restart Claude Code once.

---

## How It Works

Describe your project in plain English — Claude routes to the right specialist, asks focused questions, shows a complete plan, and waits for **GO** before touching anything.

```
mkdir my-app && cd my-app
open Claude Code → /scaffold

"What are you building?"

→ "a FastAPI backend with PostgreSQL"
   Checks: python3 ✅  pyenv ❌ (offers to install)
   Asks: Django / Flask / FastAPI? DB ORM? Docker? CI?
   Shows full plan → type GO
   Generates: src/, tests/, requirements.txt, .env.example, Dockerfile, CLAUDE.md

→ "Node.js REST API with Prisma and Postgres"
   Checks: node ✅ via nvm ✅
   Asks: Express / Fastify / NestJS? Auth? Extras?
   Shows full plan → type GO
   Generates: src/, tsconfig.json, package.json, docker-compose.yml, CLAUDE.md

→ "terraform infra on AWS with EKS, RDS and Redis"
   Asks: Terraform or Terragrunt? Which region?
   Shows component checklist: VPC, EKS, ECR, RDS, ElastiCache...
   Confirms full plan → type GO
   Generates: providers.tf, modules/vpc/, modules/eks/, modules/rds/

→ "WordPress plugin for WooCommerce payments"
   Asks: plugin name, type, namespace
   Confirms full plan → type GO
   Generates: full plugin boilerplate, REST endpoints, hooks, tests

→ "Angular frontend and Node backend, deploy to DigitalOcean"
   Asks: DB, auth, extras (Docker, CI/CD, ESLint)
   Confirms full plan → type GO
   Generates: client/ (Angular), server/ (Express), docker-compose.yml
   Generates: Nginx config, systemd service, deploy script, SSL setup

→ "a PDF generator, not sure what language"
   Shows: Python+WeasyPrint vs Node+Puppeteer vs PHP+DOMPDF
   Explains tradeoffs → Confirms → scaffolds chosen stack

→ "graphql api with postgres and subscriptions"
   Asks: Apollo vs Yoga vs Pothos, ORM choice, entities
   Generates: full SDL schema, resolvers, DataLoader, Prisma schema

→ "react app"  (simple → standard scaffold)
   Creates: Vite + TypeScript, CLAUDE.md, .gitignore
```

**Every wizard shows you the complete plan and waits for GO before touching anything.**

---

## Skills

### Wizards — Interactive, generate real code

| Skill | Activate | What it does |
|-------|----------|-------------|
| **Scaffold** | `/scaffold` | Main entry — describes your project in plain English, routes to specialist |
| **Python** | `/python` | FastAPI/Django/Flask/Celery/Jupyter — pyenv pre-flight, venv, DB, Docker, CI |
| **Node.js** | `/nodejs` | Express/Fastify/NestJS/Hono — nvm pre-flight, TypeScript, Prisma/Drizzle, auth, Docker |
| **Terraform** | `/terraform` | AWS component picker → real `.tf` files, Terragrunt multi-env, Helm on EKS |
| **Deploy** | `/deploy` | DO Ubuntu/CentOS or AWS EC2 → Nginx, SSL, systemd/PM2, deploy script |
| **WordPress** | `/wordpress` | Site / plugin / theme — DDEV local dev, WP-CLI, plugin boilerplate |
| **Web App** | `/webapp` | Angular/React/Vue + Node — DB, auth, Docker, CI/CD, deploy |
| **GraphQL** | `/graphql` | Apollo/Yoga/Pothos + Prisma/Drizzle/ScyllaDB + DataLoader + codegen |
| **Database** | `/database` | PG/ScyllaDB/Redis — schema-first wizard, migrations, query patterns |
| **Suggest** | `/suggest` | No stack preference → options with tradeoffs + recommendations |
| **Context Sync** | `/sync` | Export/import Claude project memory across devices — solves the path hash problem |
| **Bootstrap** | `/skill-bootstrap` | Standalone skill installer — runs automatically after every scaffold |

### Reference Skills — Working snippets + configuration guides

| Skill | Activate | Covers |
|-------|----------|--------|
| **AWS** | `/aws` | EKS, ECR, VPC, RDS, ElastiCache, S3, Route53, ACM, Secrets Manager, CloudWatch, IAM |
| **Kubernetes** | `/kubernetes` | Helm, ArgoCD GitOps, Ingress-nginx, HPA, Blue/Green, debugging playbook |
| **CI/CD** | `/cicd` | GitHub Actions, self-hosted runners, Docker push, OIDC to AWS, rollback |
| **Server** | `/server` | Nginx, PHP-FPM, Certbot, UFW, fail2ban, Redis, MySQL/PG, PM2 |
| **DigitalOcean** | `/digitalocean` | Droplets, Managed DBs, Spaces, Load Balancers, Firewalls, DNS, Terraform |
| **WooCommerce** | `/woocommerce` | Products, pricing rules, payment gateways, hooks, checkout, WebToffee CSV |
| **WordPress Server** | `/wordpress-server` | Nginx+WP, PHP 8.3-FPM, Redis object cache, WP Rocket, hardening, multisite |
| **PHP** | `/php` | OOP, Laravel, plugin dev, REST API, wpdb queries, nonces, sanitization |
| **Docker** | `/docker` | Dockerfile best practices, multi-stage, compose, networking, CI/CD |
| **Security** | `/security` | OWASP Top 10, WP hardening, server hardening, SSL/TLS, secrets, WAF |
| **DB** | `/db` | MySQL, PostgreSQL, MongoDB, Redis, ScyllaDB, Meilisearch — full setup + tuning |

---

## Full User Journey

```
Step 1 — Install (once)
  git clone https://github.com/veekunth217/claude-scaffold-skill.git \
    ~/.claude/skills/claude-scaffold-skill

Step 2 — Create your project folder
  mkdir my-app && cd my-app

Step 3 — Open Claude Code and type /scaffold

Step 4 — Claude silently checks your environment:
  OS (Mac/Linux/Windows/VPS/Docker)
  Package manager (brew/apt/dnf/choco)
  What's installed (node, python, php, docker, terraform...)
  nvm / pyenv / version managers

Step 5 — "What are you building?" — describe in plain English

Step 6 — Claude routes to the right specialist:
  Python → /python   Node.js → /nodejs   Terraform → /terraform
  WordPress → /wordpress   GraphQL → /graphql   Deploy → /deploy
  Fullstack → /webapp   DB-only → /database   Unsure → /suggest

Step 7 — Specialist asks focused questions (5 questions max)
  Pre-flight if tools are missing:
  ⚠️  pyenv not found.
      A) Install pyenv now   B) Use system Python   C) I'll do it myself

Step 8 — Shows complete plan — every file, every command
  YOU TYPE GO

Step 9 — Code generated. CLAUDE.md written. .gitignore created.

Step 10 — Skill bootstrapper opens automatically:
  🔴 Essentials (GSD + Claude Code Expert) — pre-selected
  🟡 Stack match — picked for your detected stack
  🟢 Community picks — top by stars, not already shown
  💡 Built into Claude Code — features you already have (Hooks, MCP, /ultrareview...)
  → Toggle numbers, type GO → skills installed to ~/.claude/skills/
```

---

## Context Sync

Claude Code stores project memory in `~/.claude/projects/<path-hash>/`. The hash comes from your absolute project path:

```
Machine A:  /home/bunny/myapp   → -home-bunny-myapp
Machine B:  /Users/john/myapp   → -Users-john-myapp   ← different hash, Claude loses context
```

**The fix:** export context to `.claude-context/` (committed to git), push, import on the new device.

```bash
# Machine A — after a productive session
python scripts/sync-export.py
git push

# Machine B — after git clone or git pull
python scripts/sync-import.py
```

The import script calculates the correct path hash for the current device automatically. Claude Code immediately has your full project memory — stack notes, feedback, conventions, everything.

**Or use the skill directly:**
```
/sync export   → export + commit
/sync import   → git pull + restore
/sync status   → diff between exported and local
/sync clean    → remove *.jsonl to reduce size before export
```

What syncs: `MEMORY.md`, `memory/*.md`, `project_*.md`, `feedback_*.md`, `user_*.md`  
What stays private: `*.jsonl` (conversation history), `*.json` (may contain keys)

---

## Community Registry

The registry at `registry/skills.json` tracks 17 community skills. It updates automatically every Sunday:

```
GitHub Action → searches topic:claude-skill, topic:claude-code-skill
             → finds repos with SKILL.md
             → deduplicates against registry
             → writes registry/discovered.json
             → opens GitHub Issue for maintainer review
             → maintainer adds verified entries via PR
             → PR blocked by CI if any repo returns 404
```

### Claude Code Capabilities Registry

A second registry (`registry/claude-capabilities.json`) tracks 16 built-in Claude Code features — things already available without any install. The bootstrapper surfaces these as `💡` awareness items matched to your stack (Hooks, MCP Servers, `/ultrareview`, CLAUDE.md, IDE extension, Extended Thinking, etc.).

Updated weekly by scanning the Claude Code releases page.

### Add your skill to the registry

1. Fork this repo
2. Add your entry to `registry/skills.json`:
```json
{
  "name": "Your Skill",
  "repo": "your-username/your-repo",
  "description": "One sentence, max 120 chars",
  "tags": ["relevant", "tags"],
  "install": "git clone https://github.com/your-username/your-repo.git ~/.claude/skills/your-skill",
  "stars": 0,
  "verified": false,
  "added": "2026-05-04"
}
```
3. Run `make validate-full` — blocks if your repo doesn't exist on GitHub
4. Open a PR

### Make your repo auto-discoverable

Add GitHub topics `claude-skill` or `claude-code-skill` to your repo, and put a `SKILL.md` in the root with YAML frontmatter:

```yaml
---
name: your-skill-name
description: What it does
version: 1.0.0
author: your-github-username
tags: [tag1, tag2]
---
```

The weekly scraper will find it automatically.

---

## Developer Commands

```bash
make validate               # validate registry structure (fast, no network)
make validate-full          # validate + verify all repos exist on GitHub
make update-stars           # refresh star counts from GitHub API
make discover               # run scraper → registry/discovered.json
make discover-capabilities  # scan Claude Code releases → registry/discovered-capabilities.json
```

---

## Project Structure

```
claude-scaffold-skill/
├── SKILL.md                         # Main entry — NL router (Routes A-K)
├── Makefile                         # Dev commands
├── CONTRIBUTING.md                  # How to add skills and contribute
├── LICENSE                          # MIT
│
├── skills/
│   ├── bootstrap/SKILL.md           # Tiered skill installer (auto post-scaffold)
│   ├── suggest/SKILL.md             # Stack suggester with tradeoffs
│   ├── python/SKILL.md              # Python wizard (FastAPI/Django/Flask/Celery/Jupyter)
│   ├── nodejs/SKILL.md              # Node.js wizard (Express/Fastify/NestJS/Hono)
│   ├── terraform/SKILL.md           # AWS IaC wizard + Helm on EKS
│   ├── deploy/SKILL.md              # Server deployment wizard
│   ├── wordpress/SKILL.md           # WP site/plugin/theme wizard
│   ├── webapp/SKILL.md              # Full-stack web app wizard
│   ├── graphql/SKILL.md             # GraphQL API wizard
│   ├── database/SKILL.md            # DB schema wizard
│   ├── sync/SKILL.md                # Context sync skill
│   ├── aws/SKILL.md                 # AWS reference skill
│   ├── kubernetes/SKILL.md          # Kubernetes reference skill
│   ├── cicd/SKILL.md                # CI/CD reference skill
│   ├── server/SKILL.md              # Server tuning reference skill
│   ├── digitalocean/SKILL.md        # DigitalOcean reference skill
│   ├── woocommerce/SKILL.md         # WooCommerce reference skill
│   ├── wordpress-server/SKILL.md    # WP server reference skill
│   ├── php/SKILL.md                 # PHP reference skill
│   ├── docker/SKILL.md              # Docker reference skill
│   ├── security/SKILL.md            # Security reference skill
│   ├── db/SKILL.md                  # Database reference skill (6 DBs)
│   └── picker/SKILL.md              # Legacy — redirects to bootstrap
│
├── registry/
│   ├── skills.json                  # Curated community registry (17 entries)
│   ├── discovered.json              # Weekly auto-discoveries (pending review)
│   ├── claude-capabilities.json     # Built-in Claude Code features (16 entries)
│   └── discovered-capabilities.json # Weekly docs scan results (pending review)
│
├── .claude-context/                 # Context sync folder — committed to git intentionally
│   ├── .gitkeep
│   └── sync-manifest.json           # Auto-generated by sync-export.py
│
├── scripts/
│   ├── sync-export.py               # Export Claude context → .claude-context/
│   ├── sync-import.py               # Import from .claude-context/ → ~/.claude/projects/
│   ├── fetch-skills.py              # GitHub scraper (stdlib only)
│   ├── fetch-capabilities.py        # Claude Code releases scraper (stdlib only)
│   ├── update-stars.py              # Refresh star counts (stdlib only)
│   └── validate-registry.py        # Structure + GitHub existence validator
│
├── references/
│   ├── stacks.md                    # Stack version requirements + commands
│   └── environments.md              # Environment detection edge cases
│
└── .github/workflows/
    ├── sync-registry.yml            # Weekly: refresh stars + discover + open Issue
    └── validate-registry.yml        # PR gate: blocks 404 repos
```

---

## Supported Stacks

| Category | Stacks |
|----------|--------|
| Frontend | React (Vite+TS), Vue 3, Angular, Next.js, Hugo |
| Backend | Node/Express, Node/Fastify, Node/NestJS, Python/FastAPI, Python/Django, PHP/Laravel |
| CMS | WordPress (site, plugin, theme, WooCommerce) |
| Full-stack | MERN, LAMP, LEMP, Angular+Node, React+Node |
| API | GraphQL (Apollo/Yoga/Pothos + any DB), REST (Express/Fastify/FastAPI) |
| Infrastructure | Terraform/Terragrunt (AWS), Docker Compose |
| Deployment | DigitalOcean Ubuntu/CentOS, AWS EC2, AWS ECS |
| Database | PostgreSQL, MySQL, MongoDB, Redis, ScyllaDB, Meilisearch |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

Quick version:
- **Add a registry entry** — edit `registry/skills.json`, run `make validate-full`, open PR
- **Add a new wizard skill** — create `skills/your-skill/SKILL.md`, follow the confirm-before-generate pattern, set `name:` to match the slash command you want
- **Improve an existing skill** — PRs welcome
- **Make your repo discoverable** — add `claude-skill` topic to your GitHub repo

---

## Credits

Built on patterns and ideas from:
- [hmohamed01/Claude-Code-Scaffolding-Skill](https://github.com/hmohamed01/Claude-Code-Scaffolding-Skill) — 70+ template scaffolding and conversational CLI patterns
- [reedmayhew18/claude-code-expert](https://github.com/reedmayhew18/claude-code-expert) — active/available skill split and production wizard design

---

## License

MIT — see [LICENSE](LICENSE)
