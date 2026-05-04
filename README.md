# claude-scaffold-skill

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Skills](https://img.shields.io/badge/Skills-20+-green.svg)
![Registry](https://img.shields.io/badge/Registry-16%20community%20skills-orange.svg)
![Last Updated](https://img.shields.io/badge/Updated-May%202026-lightgrey.svg)
![Validate Registry](https://github.com/veekunth217/claude-scaffold-skill/actions/workflows/validate-registry.yml/badge.svg)

A Claude Code skill collection that turns a blank directory into a production-ready project. Describe what you're building in plain English — it routes to the right specialist wizard, generates real code, installs the right Claude Code skills for your stack, and deploys if you want.

---

## How It Works

```
mkdir my-app && cd my-app
↓  open VS Code
↓  open Claude Code
↓  /scaffold

"What are you building?"

→ "terraform infra on AWS with EKS, RDS and Redis"
   Asks: Terraform or Terragrunt? Which region?
   Shows component checklist: VPC, EKS, ECR, RDS, ElastiCache...
   Confirms full plan → type GO
   Generates: providers.tf, modules/vpc/, modules/eks/, modules/rds/
   Asks: Add Helm chart for your app on EKS? (ingress-nginx, AWS LBC)
   Then: installs GSD + relevant skills from the registry

→ "WordPress plugin for WooCommerce payments"
   Asks: plugin name, type, namespace
   Confirms full plan → type GO
   Generates: full plugin boilerplate, REST endpoints, hooks, tests
   Recommends: GSD + chromium testing skill

→ "Angular frontend and Node backend, deploy to DigitalOcean"
   Asks: DB, auth, extras (Docker, CI/CD, ESLint)
   Confirms full plan → type GO
   Generates: client/ (Angular), server/ (Express/Fastify), docker-compose.yml
   Generates: Nginx config, systemd service, deploy script, SSL setup

→ "a PDF generator, not sure what language"
   Shows: Python+WeasyPrint vs Node+Puppeteer vs PHP+DOMPDF
   Explains tradeoffs, recommends for your context
   Confirms → scaffolds chosen stack

→ "graphql api with postgres and subscriptions"
   Asks: Apollo vs Yoga vs Pothos, ORM choice
   Asks: describe your entities
   Generates: full SDL schema, resolvers, DataLoader, Prisma schema

→ "react app"  (simple → standard scaffold)
   Creates: Vite + TypeScript, CLAUDE.md, .gitignore
```

**Every wizard shows you the complete plan and waits for GO before touching anything.**

---

## Install

```bash
git clone https://github.com/veekunth217/claude-scaffold-skill.git \
  ~/.claude/skills/claude-scaffold-skill
```

Then in Claude Code:
```
/scaffold
```

That's it.

---

## Skills

### Wizards — Interactive, generate real code

| Skill | Activate | What it does |
|-------|----------|-------------|
| **Scaffold** | `/scaffold` | Main entry — NL router, detects your environment, routes to specialist |
| **Terraform** | `/terraform` | AWS component picker → real `.tf` files, Terragrunt multi-env, Helm on EKS |
| **Deploy** | `/deploy` | DO Ubuntu/CentOS or AWS EC2 → Nginx, SSL, systemd/PM2, deploy script |
| **WordPress** | `/wordpress` | Site / plugin / theme — DDEV local dev, WP-CLI, plugin boilerplate |
| **Web App** | `/webapp` | Angular/React/Vue + Node — DB, auth, Docker, CI/CD, deploy |
| **GraphQL** | `/graphql` | Apollo/Yoga/Pothos + Prisma/Drizzle/ScyllaDB + DataLoader + codegen |
| **Database** | `/database` | PG/ScyllaDB/Redis — schema-first wizard, migrations, query patterns |
| **Suggest** | `/suggest` | No stack preference → 2-3 options with tradeoffs + skill recommendations |
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

### Community Registry

Separate from the skill files above, a curated registry of 16 community skills auto-discovered weekly from GitHub:

```
/skill-bootstrap   →   reads registry → shows tiered recommendations → installs
```

---

## Full User Journey

```
1. mkdir my-app && cd my-app

2. Open Claude Code → type /scaffold

3. Claude silently checks:
   - OS (Mac/Linux/Windows/VPS/Docker)
   - Package manager (brew/apt/dnf/choco)
   - What's already installed (node, python, php, docker, terraform...)

4. "What are you building?" — you describe in plain English

5. Claude routes to the right specialist:
   terraform / deploy / wordpress / webapp / graphql / database / suggest

6. Specialist asks focused questions (5-8 questions max)

7. Shows complete plan — files to create, commands to run
   YOU TYPE GO

8. Code generated. CLAUDE.md written. .gitignore created.

9. Skill bootstrapper opens automatically:
   🔴 Essentials (GSD + Claude Code Expert) — pre-selected
   🟡 Stack match (UI/UX Pro Max for frontend, Code Review Graph, etc.)
   🟢 Community picks by stars
   → You toggle numbers, type GO → skills installed to ~/.claude/skills/
```

---

## Community Registry

The registry at `registry/skills.json` tracks 16 verified community skills. It updates automatically every Sunday:

```
GitHub Action → searches topic:claude-skill, topic:claude-code-skill
             → finds repos with SKILL.md
             → deduplicates against registry
             → writes registry/discovered.json
             → opens GitHub Issue for maintainer review
             → maintainer adds verified entries via PR
             → PR blocked by CI if any repo returns 404
```

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
make validate        # validate registry structure (fast, no network)
make validate-full   # validate + verify all repos exist on GitHub
make update-stars    # refresh star counts from GitHub API
make discover        # run scraper → registry/discovered.json
```

---

## Project Structure

```
claude-scaffold-skill/
├── SKILL.md                         # Main entry — NL router (Routes A-H)
├── Makefile                         # Dev commands
├── CONTRIBUTING.md                  # How to add skills and contribute
├── LICENSE                          # MIT
│
├── skills/
│   ├── bootstrap/SKILL.md           # Tiered skill installer (auto post-scaffold)
│   ├── suggest/SKILL.md             # Stack suggester with tradeoffs + benefits
│   ├── terraform/SKILL.md           # AWS IaC wizard + Helm on EKS
│   ├── deploy/SKILL.md              # Server deployment wizard
│   ├── wordpress/SKILL.md           # WP site/plugin/theme wizard
│   ├── webapp/SKILL.md              # Full-stack web app wizard
│   ├── graphql/SKILL.md             # GraphQL API wizard
│   ├── database/SKILL.md            # DB schema wizard
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
│   ├── db/SKILL.md                  # Database reference skill (all 6 DBs)
│   └── picker/SKILL.md              # Legacy — redirects to bootstrap
│
├── registry/
│   ├── skills.json                  # Curated community registry (16 entries)
│   └── discovered.json              # Weekly auto-discoveries (pending review)
│
├── scripts/
│   ├── fetch-skills.py              # GitHub scraper (stdlib only)
│   ├── update-stars.py              # Refresh star counts (stdlib only)
│   └── validate-registry.py        # Structure + GitHub existence validator
│
├── references/
│   ├── stacks.md                    # Stack version requirements + commands
│   └── environments.md             # Environment detection edge cases
│
└── .github/workflows/
    ├── sync-registry.yml            # Weekly: refresh stars + discover + open Issue
    └── validate-registry.yml        # PR gate: blocks 404 repos
```

---

## Supported Stacks (Scaffold Wizard)

| Category | Stacks |
|----------|--------|
| Frontend | React (Vite+TS), Vue 3, Angular, Next.js, Hugo |
| Backend | Node/Express, Node/Fastify, Node/NestJS, Python/FastAPI, PHP/Laravel |
| CMS | WordPress (site, plugin, theme, WooCommerce) |
| Full-stack | MERN, LAMP, LEMP, Angular+Node, React+Node |
| API | GraphQL (Apollo/Yoga/Pothos + any DB) |
| Infrastructure | Terraform/Terragrunt (AWS), Docker Compose |
| Deployment | DigitalOcean Ubuntu/CentOS, AWS EC2, AWS ECS |
| Database | PostgreSQL, MySQL, MongoDB, Redis, ScyllaDB, Meilisearch |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

Quick version:
- **Add a registry entry** — edit `skills.json`, run `make validate-full`, open PR
- **Add a new wizard skill** — create `skills/your-skill/SKILL.md`, follow the confirm-before-generate pattern
- **Improve an existing skill** — PRs welcome, especially filling in `<!-- TODO -->` sections
- **Make your repo discoverable** — add `claude-skill` topic to your GitHub repo

---

## Credits

Built on patterns and ideas from:
- [hmohamed01/Claude-Code-Scaffolding-Skill](https://github.com/hmohamed01/Claude-Code-Scaffolding-Skill) — 70+ template scaffolding and conversational CLI patterns
- [reedmayhew18/claude-code-expert](https://github.com/reedmayhew18/claude-code-expert) — active/available skill split and production wizard design

---

## License

MIT — see [LICENSE](LICENSE)
