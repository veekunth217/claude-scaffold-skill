<div align="center">

# claude-scaffold-skill

**Turn Claude Code into a full dev toolkit — scaffolding, skills, and workflow automation in one install.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-30%2B-brightgreen.svg)](#skills)
[![Registry](https://img.shields.io/badge/Community%20Registry-18%20skills-orange.svg)](registry/skills.json)
[![Updated](https://img.shields.io/badge/Updated-May%202026-lightgrey.svg)](#)
[![Validate Registry](https://github.com/veekunth217/claude-scaffold-skill/actions/workflows/validate-registry.yml/badge.svg)](https://github.com/veekunth217/claude-scaffold-skill/actions)

<br/>

> **One install. Scaffold any stack. Discover the right skills. Sync context across devices.**

<br/>

<!-- DEMO GIF — record with: npx terminalizer record demo && npx terminalizer render demo -->
<!-- Replace this block once recorded -->
```
┌─────────────────────────────────────────────┐
│  📹  Demo GIF coming — recording in progress │
│  /scaffold → "FastAPI backend with Postgres" │
│  → plan shown → GO → files generated         │
└─────────────────────────────────────────────┘
```

</div>

---

## Why this exists

Claude Code is powerful. But out of the box, every new project starts the same way — blank directory, blank CLAUDE.md, you explaining your stack from scratch again.

This skill collection fixes that:

- **`/scaffold`** — describe your project in plain English, get production-ready files, a CLAUDE.md, and `.vscode/` config. No templates to browse, no boilerplate to copy.
- **`/bootstrap`** — after every scaffold, Claude surfaces the right community skills for your stack, tiered by how much you need them.
- **`/sync`** — Claude stores project memory in a path-hashed folder that breaks between machines. Sync exports it to git, imports it anywhere.

Everything else (`/hooks`, `/budget`, `/handoff`, `/dark-mode`, `/launch`, `/saas`...) extends your workflow once the foundation is set.

---

## Install

```bash
git clone https://github.com/veekunth217/claude-scaffold-skill.git \
  ~/.claude/skills/claude-scaffold-skill
```

Open Claude Code in any project and type `/scaffold`. That's it.

> **No restart needed.** Claude Code picks up skills from `~/.claude/skills/` automatically.

---

## Quick Start — 60 seconds to first scaffold

```
mkdir my-app && cd my-app
```

Open Claude Code → type:

```
/scaffold
```

Claude checks your environment silently, then asks one question:

```
What are you building?
```

Type anything. Plain English. Claude routes it, asks 3-5 focused questions, shows you the full plan, and waits for:

```
GO
```

Before touching a single file.

---

## How the routing works

The main `SKILL.md` reads your description and routes to the right specialist — no flags, no subcommands.

```
/scaffold "a FastAPI backend with PostgreSQL"
  → /python  → pyenv check → venv → DB → Docker → CI → GO → files

/scaffold "Node REST API with Prisma"
  → /nodejs  → nvm check → TypeScript → ORM → auth → GO → files

/scaffold "Terraform AWS EKS cluster"
  → /terraform → AWS EKS preset or custom picker → GO → .tf files

/scaffold "WordPress plugin for WooCommerce"
  → /wordpress → plugin boilerplate → DDEV → WP-CLI → GO → files

/scaffold "not sure what stack to use"
  → /suggest → options with tradeoffs → you pick → routes to specialist
```

Every route follows the same contract: **show the plan, wait for GO, then generate.**

---

## Skills

### Wizards — ask questions, generate real code

| Skill | Command | What it does |
|-------|---------|-------------|
| **Scaffold** | `/scaffold` | Main entry — plain English → right specialist |
| **Python** | `/python` | FastAPI / Django / Flask / Celery / Jupyter — pyenv, venv, DB, Docker, CI |
| **Node.js** | `/nodejs` | Express / Fastify / NestJS / Hono — nvm, TypeScript, Prisma/Drizzle, auth |
| **Terraform** | `/terraform` | AWS EKS preset · DO Kubernetes preset · custom component picker |
| **Web App** | `/webapp` | Angular/React/Vue + Node — DB, auth, Docker, deploy |
| **GraphQL** | `/graphql` | Apollo / Yoga / Pothos + Prisma / ScyllaDB + DataLoader + codegen |
| **Database** | `/database` | Schema-first wizard — PG / ScyllaDB / Redis, migrations, query patterns |
| **Deploy** | `/deploy` | DigitalOcean or AWS EC2 — Nginx, SSL, systemd/PM2, deploy script |
| **WordPress** | `/wordpress` | Site / plugin / theme — DDEV, WP-CLI, hooks, REST endpoints |
| **Suggest** | `/suggest` | No stack preference → options with tradeoffs + recommendation |
| **Clone** | `/clone` | Any GitHub repo as skeleton — strips history, detects stack, adds CLAUDE.md |
| **Design** | `/design` | Extract design tokens from any website via designmd.me → CSS vars, Tailwind, theme.ts |
| **Dark Mode** | `/dark-mode` | Full dark mode + **Black or White** animated toggle (MJ tribute) — View Transitions API |
| **SaaS** | `/saas` | Product wizard — auth, billing, onboarding → GSD phase plan + UI/UX Pro Max brief |
| **Launch** | `/launch` | Submission packs for CodeCanyon · WP.org · Product Hunt · SaaS pre-launch audit |
| **Hooks** | `/hooks` | Wire `.claude/settings.json` — auto-lint, block `rm -rf`, run tests on edit |
| **Budget** | `/budget` | Route Claude Code + Roo Code traffic to free models via local proxy |
| **Handoff** | `/handoff` | Split tasks between Claude and Roo Code — generates self-contained Roo prompts |
| **Context Sync** | `/sync` | Export/import Claude project memory across machines |
| **Bootstrap** | `/skill-bootstrap` | Tiered skill installer — runs automatically after every scaffold |

### Reference Skills — working snippets and config guides

| Skill | Command | Covers |
|-------|---------|--------|
| **AWS** | `/aws` | EKS, ECR, VPC, RDS, ElastiCache, S3, Route53, ACM, IAM |
| **Kubernetes** | `/kubernetes` | Helm, ArgoCD, Ingress-nginx, HPA, Blue/Green, debug playbook |
| **CI/CD** | `/cicd` | GitHub Actions, self-hosted runners, Docker push, OIDC to AWS |
| **Server** | `/server` | Nginx, PHP-FPM, Certbot, UFW, fail2ban, Redis, MySQL/PG, PM2 |
| **DigitalOcean** | `/digitalocean` | Droplets, Managed DBs, Spaces, Load Balancers, DNS, Terraform |
| **Docker** | `/docker` | Dockerfile best practices, multi-stage, compose, networking |
| **Security** | `/security` | OWASP Top 10, WP hardening, server hardening, SSL/TLS, WAF |
| **PHP** | `/php` | OOP, Laravel, WordPress plugin dev, REST, wpdb, nonces |
| **WooCommerce** | `/woocommerce` | Products, pricing, payment gateways, hooks, checkout |
| **WordPress Server** | `/wordpress-server` | Nginx+WP, PHP 8.3-FPM, Redis cache, WP Rocket, hardening |
| **Database** | `/db` | MySQL, PostgreSQL, MongoDB, Redis, ScyllaDB, Meilisearch |

---

## The 3-Tool AI Dev Stack

The most cost-effective way to build with AI in 2026. Claude thinks, Roo types, you pay only for thinking.

| Role | Tool | Best for | Cost |
|------|------|----------|------|
| 🧠 Architect | **Claude Code** | Decisions, debugging, code review, architecture | Paid (Anthropic) |
| ✍️ Executor | **Roo Code / Cline** | Bulk generation, boilerplate, mechanical refactors | Lower — or free via proxy |
| 🔀 Router | **free-claude-code** | Routes Roo traffic → OpenRouter free / Ollama / NIM / DeepSeek | Free (local) |

```
Set up in 5 minutes:
  /budget    → installs the proxy, wires VS Code + shell
  /handoff   → splits any task list between Claude and Roo
```

The `/handoff` skill detects when the proxy is running and auto-routes Roo tasks through it. Heavy lifting runs on free models. Critical work stays on Anthropic.

---

## Context Sync — take your Claude memory anywhere

Claude stores project memory in `~/.claude/projects/<path-hash>/`. The hash is derived from your absolute path, so it breaks between machines:

```
/home/bunny/myapp   → -home-bunny-myapp      ← Machine A
/Users/john/myapp   → -Users-john-myapp       ← Machine B (Claude loses everything)
```

The `/sync` skill solves it. Export to `.claude-context/` (committed to git), push, import on any device:

```bash
# After a productive session on Machine A
python scripts/sync-export.py && git push

# On Machine B after pull
python scripts/sync-import.py
```

The import script calculates the correct path hash for the current machine automatically.

```
/sync export   → export + commit
/sync import   → pull + restore to correct hash
/sync status   → diff between exported and live
/sync clean    → strip *.jsonl before export (reduces size)
```

What syncs: `MEMORY.md`, `memory/*.md`, feedback files, project notes
What stays private: `*.jsonl` (conversation history), `*.json` (may contain keys)

---

## After every scaffold — the skill bootstrapper

Once your project is generated, `/bootstrap` opens automatically and shows you what to install next:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLAUDE CODE SKILL INSTALLER
Project detected: python, fastapi, docker
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 ESSENTIALS — pre-selected
   [1] ✓ Get Shit Done (GSD)           ⭐ 59,791
   [2] ✓ Awesome Claude Code           ⭐ 42,429
   [3] ✓ Claude Code Expert            ⭐ 0
   [4] ✓ Code Review Graph             ⭐ 15,203

🟡 STACK MATCH — for your python + docker project
   [5]   Claude Memory                 ⭐ 71,750

🟢 COMMUNITY PICKS
   [6]   Everything Claude Code        ⭐ 172,979
   [7]   Superpowers                   ⭐ 177,817
   ...

💡 ALREADY IN CLAUDE CODE — no install needed
   ↳ Hooks · MCP Servers · /ultrareview · CLAUDE.md · IDE Extension
   ↳ The 3-Tool AI Dev Stack (Claude + Roo + free proxy)

Currently selected: 1, 2, 3, 4
Type numbers to toggle, "all", "none", or "go" to install.
```

---

## Community Registry

`registry/skills.json` tracks 18 verified community skills. It auto-updates every Sunday:

```
GitHub Action → scans topic:claude-skill + topic:claude-code-skill
             → finds repos with SKILL.md in root
             → deduplicates, opens Issue for review
             → maintainer adds via PR
             → PR blocked by CI if any repo returns 404
```

A second registry (`registry/claude-capabilities.json`) tracks 16 built-in Claude Code features — surfaced as `💡` awareness items matched to your stack.

### Add your skill

1. Fork, edit `registry/skills.json`:

```json
{
  "name": "Your Skill",
  "repo": "your-username/your-repo",
  "description": "One sentence, max 120 chars",
  "tags": ["relevant", "tags"],
  "install": "git clone https://github.com/your-username/your-repo.git ~/.claude/skills/your-skill",
  "stars": 0,
  "verified": false,
  "added": "2026-05-05"
}
```

2. `make validate-full` — blocks if your repo 404s
3. Open a PR

### Make your repo auto-discoverable

Add GitHub topics `claude-skill` or `claude-code-skill` and put a `SKILL.md` in root with YAML frontmatter:

```yaml
---
name: your-skill-name
description: What it does
version: 1.0.0
author: your-github-username
tags: [tag1, tag2]
---
```

The weekly scraper finds it automatically.

---

## Supported Stacks

| Category | Stacks |
|----------|--------|
| Frontend | React (Vite+TS), Vue 3, Angular, Next.js, Hugo |
| Backend | Express, Fastify, NestJS, Hono, FastAPI, Django, Flask, Laravel |
| CMS | WordPress — site, plugin, theme, WooCommerce |
| Full-stack | MERN, LAMP, LEMP, Angular+Node, React+Node |
| API | GraphQL (Apollo/Yoga/Pothos), REST (Express/Fastify/FastAPI) |
| Infrastructure | Terraform (AWS EKS preset, DO K8s preset), Terragrunt |
| Deployment | DigitalOcean Ubuntu/CentOS, AWS EC2, AWS ECS |
| Database | PostgreSQL, MySQL, MongoDB, Redis, ScyllaDB, Meilisearch |

---

## Project Structure

```
claude-scaffold-skill/
├── SKILL.md                         # Main entry — NL router (Routes A-S)
├── Makefile                         # Dev commands
├── CONTRIBUTING.md                  # How to add skills and contribute
│
├── skills/                          # 30+ skills
│   ├── scaffold/   python/   nodejs/   terraform/   deploy/
│   ├── wordpress/  webapp/   graphql/  database/    suggest/
│   ├── sync/       hooks/    budget/   handoff/     clone/
│   ├── design/     dark-mode/ saas/   launch/      bootstrap/
│   └── aws/ kubernetes/ cicd/ server/ digitalocean/
│       woocommerce/ wordpress-server/ php/ docker/ security/ db/
│
├── templates/
│   ├── hooks/          # lint.sh, block-dangerous.sh, test-on-edit.sh, notify-stop.sh
│   ├── vscode/         # extensions.json, settings.json, tasks.json
│   └── dark-mode/      # CSS tokens, toggle component, Black or White animation
│
├── registry/
│   ├── skills.json                  # 18 verified community skills
│   ├── discovered.json              # Weekly auto-discoveries (pending review)
│   ├── claude-capabilities.json     # 16 built-in Claude Code features
│   └── discovered-capabilities.json # Weekly docs scan results
│
├── scripts/
│   ├── sync-export.py               # Export context → .claude-context/
│   ├── sync-import.py               # Import from .claude-context/ → correct hash
│   ├── fetch-skills.py              # GitHub scraper
│   ├── update-stars.py              # Star count refresher
│   └── validate-registry.py        # Structure + 404 validator
│
├── references/
│   ├── stacks.md                    # Version requirements + commands per stack
│   ├── environments.md              # Environment detection edge cases
│   └── vscode-extensions.md        # Per-stack VS Code extension + settings overrides
│
└── .github/workflows/
    ├── sync-registry.yml            # Weekly: refresh stars + discover
    └── validate-registry.yml        # PR gate: blocks 404 repos
```

---

## Developer Commands

```bash
make validate               # validate registry structure (fast, no network)
make validate-full          # validate + verify all repos exist on GitHub
make update-stars           # refresh star counts from GitHub API
make discover               # run scraper → registry/discovered.json
make discover-capabilities  # scan Claude Code releases → discovered-capabilities.json
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

- **Add a registry entry** — edit `registry/skills.json`, run `make validate-full`, open PR
- **Add a wizard skill** — create `skills/your-skill/SKILL.md`, follow confirm-before-generate pattern
- **Improve an existing skill** — PRs welcome, no CLA
- **Make your repo discoverable** — add `claude-skill` topic to your GitHub repo

---

## Credits

Built on patterns from:
- [hmohamed01/Claude-Code-Scaffolding-Skill](https://github.com/hmohamed01/Claude-Code-Scaffolding-Skill) — conversational CLI patterns and template scaffolding
- [reedmayhew18/claude-code-expert](https://github.com/reedmayhew18/claude-code-expert) — skill split design and production wizard structure

---

## License

MIT — see [LICENSE](LICENSE)
