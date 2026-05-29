<div align="center">

# claude-scaffold-skill

**Turn Claude Code into a full dev toolkit — scaffolding, skills, and workflow automation in one install.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/Skills-30%2B-brightgreen.svg)](#skills)
[![Registry](https://img.shields.io/badge/Community%20Registry-35%20skills-orange.svg)](registry/skills.json)
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

The registry also surfaces **Anthropic's official document skills** (PDF, Excel, Word, PowerPoint) and the **Vercel cross-agent skills CLI** as awareness cards — so you always know what's available beyond this collection.

---

## Install

```bash
git clone https://github.com/veekunth217/claude-scaffold-skill.git \
  ~/.claude/skills/claude-scaffold-skill
```

Open Claude Code in any project and type `/scaffold`. That's it.

> **No restart needed.** Claude Code picks up skills from `~/.claude/skills/` automatically.

### Keeping skills updated

New skills land in this repo every week. To pull the latest:

```bash
# Quick — just one command
cd ~/.claude/skills/claude-scaffold-skill && git pull
```

Or use the built-in updater (it scans every git-installed skill in `~/.claude/skills/`, shows you what changed, asks before pulling):

```
/update-skills
```

**Other install paths:**
- Skills installed via `/plugin install` (e.g. Anthropic document skills) → update with `/plugin update`
- Skills installed via `npx skills add` (Vercel CLI) → update with `npx skills update`

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

When you say "fresh project," `/scaffold` asks where it should land — current directory, a new subfolder you name, or an absolute path — before generating anything. Never overwrites a non-empty directory unless you explicitly chose "Existing" mode.

> **Curious what `/scaffold` actually generates?** See [examples/](examples/) for committed reference outputs (FastAPI + Postgres, Next.js + Tailwind) — same shape `/scaffold` writes into your project.

---

## Document support — Anthropic's official skills, surfaced for you

If your project ever touches PDFs, Excel, Word, or PowerPoint, `/bootstrap` surfaces Anthropic's official document skills as an awareness card:

```bash
# Install the official Anthropic marketplace
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

This gives Claude native read/write for `.pdf`, `.xlsx`, `.docx`, and `.pptx` — automatically suggested for SaaS, WordPress, Python data, reports, docs, and ETL projects.

The registry also surfaces the **Vercel cross-agent Skills CLI** (`npx skills add` / `npx skills find`) so you know about the broader skills ecosystem beyond this collection.

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
| **Context Sync** | `/sync` | Export/import Claude memory across machines, **and** push it as adapter files to Cursor, Codex, Roo, Cline, Aider, Windsurf (cross-tool memory bridge — git-native alternative to Vilix) |
| **Bootstrap** | `/skill-bootstrap` | Tiered skill installer — runs automatically after every scaffold |
| **New Skill** | `/new-skill` | Author a new Claude Code skill — generates SKILL.md + draft registry entry, ready for PR |
| **Update Skills** | `/update-skills` | Pull latest commits for every git-installed skill in `~/.claude/skills/` — preview changes, ask before applying |
| **Review Skills** | `/review-skills` | Triage the discovered-skills queue 25 at a time — keep good ones into the registry, reject the rest (persisted, resumable) |

### Reference Skills — config guides and snippet collections

These are **directly-invoked** skills (type `/aws`, `/kubernetes`, etc.) — they're not part of the `/scaffold` router. Use them when you want focused help on a specific topic.

> **Honest status:** Most reference skills below are **stubs** — they have the structure
> (sections, RULE, frontmatter) but the actual snippet content is still being filled in. They
> activate and surface the topic to Claude, but won't yield deep snippets until contributors
> write them. Each stub is clearly marked at the top of its `SKILL.md`. **PRs welcome** — see
> [CONTRIBUTING.md](CONTRIBUTING.md). The `/db` skill is the only fully-written reference today.

| Skill | Command | Covers | Status |
|-------|---------|--------|--------|
| **AWS** | `/aws` | EKS, ECR, VPC, RDS, ElastiCache, S3, Route53, ACM, IAM | 🚧 Stub |
| **Kubernetes** | `/kubernetes` | Helm, ArgoCD, Ingress-nginx, HPA, Blue/Green, debug playbook | 🚧 Stub |
| **CI/CD** | `/cicd` | GitHub Actions, self-hosted runners, Docker push, OIDC to AWS | 🚧 Stub |
| **Server** | `/server` | Nginx, PHP-FPM, Certbot, UFW, fail2ban, Redis, MySQL/PG, PM2 | 🚧 Stub |
| **DigitalOcean** | `/digitalocean` | Droplets, Managed DBs, Spaces, Load Balancers, DNS | 🚧 Stub |
| **Docker** | `/docker` | Dockerfile best practices, multi-stage, compose, networking | 🚧 Stub |
| **Security** | `/security` | OWASP Top 10, WP hardening, server hardening, SSL/TLS, WAF | 🚧 Stub |
| **PHP** | `/php` | OOP, Laravel, WordPress plugin dev, REST, wpdb, nonces | 🚧 Stub |
| **WooCommerce** | `/woocommerce` | Products, pricing, payment gateways, hooks, checkout | 🚧 Stub |
| **WordPress Server** | `/wordpress-server` | Nginx+WP, PHP 8.3-FPM, Redis cache, WP Rocket | 🚧 Stub |
| **Database** | `/db` | MySQL, PostgreSQL, MongoDB, Redis, ScyllaDB, Meilisearch | ✅ Ready |

---

## Speed & cost modes — what you can actually toggle

Three usage patterns. Only one is a real toggle; the other two are behavioral patterns you ask for in plain English.

| Mode | How to activate | How to check | What you get |
|---|---|---|---|
| **Fast** | `/fast` (real toggle) | type `/fast` again — it shows ON/OFF | Opus 4.6 with faster output. Costs more tokens. Toggle on for hard problems, off when done. |
| **Default** | (no toggle — it's the baseline) | Status bar shows model = Sonnet 4.6 | Sonnet 4.6 with sub-agents on demand. Balanced. |
| **Careful** | Ask: "do this serially, no sub-agents" | (no command — pattern only) | One task at a time. Slowest, cheapest. |

Other useful asks:
- **Force parallel:** "spawn 4 sub-agents to do X" → faster, costs more
- **Check current model:** look at the Claude Code status bar — model name shows there
- **Restart from fresh context:** `/clear`

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

### A fourth, optional tier — async agents

For fire-and-forget work (dependency bumps, mechanical PRs, "fix this flaky test"), there's a whole category of **asynchronous cloud agents**: [Jules](https://jules.google/) (Google, Gemini-powered), the OpenAI Codex agent, Devin, GitHub Copilot agent mode. You hand them a task + a repo, they spin up a VM, make the change, run tests, and open a PR you review later.

| Tier | Tool | Interaction model |
|---|---|---|
| 🧠 Architect | Claude Code | live, turn-by-turn |
| ✍️ Executor | Roo Code / Cline | live, bulk in-editor |
| 🔀 Router | free-claude-code | (config — routes Roo to free models) |
| 📨 Delegate | Jules / Codex / Devin | async — fire a task, get a PR |

Not Claude Code skills (so not in the registry) — but if you're already splitting work with `/handoff`, the "delegate the boring PR to an async agent" tier slots in naturally above it.

---

## Cross-tool memory bridge — git-native alternative to Vilix/Mem0

Use Claude Code **and** Cursor **and** Codex CLI **and** Roo Code **and** Aider on the same project? Each one has its own instruction/memory file — `CLAUDE.md`, `.cursorrules`, `AGENTS.md`, etc. — and you re-explain your project to every one of them.

`/sync tools push` writes them all from **one canonical source** (`.claude-context/MEMORY.md`, committed to git):

```bash
make sync-tools-detect      # see which tool configs exist in this project
make sync-tools             # generate adapter files for every detected tool
make sync-tools DRY=1       # show what would change without writing
make sync-tools ONLY=cursor,claude
```

| Tool | Adapter file | Written when |
|---|---|---|
| Claude Code | `CLAUDE.md` | always |
| Cursor | `.cursor/rules/memory.mdc` | `.cursor/` or `.cursorrules` exists |
| Roo Code | `.roo/rules/memory.md` | `.roo/` exists |
| Cline | `.clinerules/memory.md` | `.clinerules` exists |
| Codex CLI | `AGENTS.md` | `.codex/` or `AGENTS.md` exists |
| Aider | `CONVENTIONS.md` | `.aider/` or `CONVENTIONS.md` exists |
| Windsurf | `.windsurfrules` | `.windsurfrules` exists |

**vs Vilix / Mem0 (proprietary SaaS at ~$20/mo):**
- ✅ Git-native — memory lives in your repo, `git blame`-able, code-review-able
- ✅ Zero vendor lock-in — plain markdown, works offline forever
- ✅ One source of truth, regenerable — new dev runs `make sync-tools` after `git clone` and every AI tool they use immediately knows the project
- ⏳ Not live yet — re-run after editing the source. **Phase 2 (spec'd, not built):** [skills/sync/PHASE2-MCP.md](skills/sync/PHASE2-MCP.md) — a small MCP server so Claude / Cursor / Codex / Roo / Cline / Windsurf see edits live, no re-run. ~half-day build, contributions welcome.

---

## Context Sync — take your Claude memory anywhere

Claude stores project memory in `~/.claude/projects/<path-hash>/`. The hash is derived from your absolute path, so it breaks between machines:

```
/home/alice/myapp   → -home-alice-myapp      ← Machine A
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
   ↳ Anthropic Document Skills (PDF · Excel · Word · PowerPoint)
   ↳ Vercel Skills CLI (cross-agent skill discovery)

Currently selected: 1, 2, 3, 4
Type numbers to toggle, "all", "none", or "go" to install.
```

---

## Community Registry

`registry/skills.json` tracks 35 community skills (incl. Anthropic's official document marketplace, the Vercel cross-agent CLI, MCP servers, and curated agent collections). It auto-updates every Sunday:

```
GitHub Action → scans 10 topic queries (claude-skill, claude-skills, etc.)
             → finds repos with SKILL.md in root
             → scores each on 6 quality signals (stars, recency, topics,
               description length, README, archived status — max 100)
             → writes the full sorted queue to registry/discovered.json
             → diffs against last run → opens an Issue ONLY for the new
               candidates (or stays silent if nothing new appeared)
             → maintainer reads the Issue, picks the worthwhile ones, PRs
             → PR blocked by CI if any repo returns 404
```

**No skill enters `registry/skills.json` without human review.** `discovered.json` is a sorted candidate queue you browse at your own pace; the weekly Issue only nudges you about what's *newly* appeared since the last scrape. Quality scoring criteria are documented in [CONTRIBUTING.md](CONTRIBUTING.md#what-the-scraper-actually-does-and-what-it-doesnt).

### Triaging the queue — page by page

The queue is grouped into sections (🆕 just launched · 🔥 popular · 💎 quiet gems · 📦 long tail) so you can review by flavour. Work through it 25 at a time:

```bash
make review-status                    # how many pending, broken down by section
make review                           # show the next page (default 25)
make review SECTION=just-launched     # only the freshly-launched ones
make review PAGE=3                    # jump to page 3

# Record decisions (they persist):
python scripts/review-queue.py --accept owner/repo   # → appended to skills.json, verified
python scripts/review-queue.py --reject owner/repo   # → added to rejected.json, never shown again
```

Or run it conversationally inside Claude Code with **`/review-skills`** — it shows you a page, you say "keep 1 3 7, reject the rest", it updates the files and offers to commit. Rejected repos go in `registry/rejected.json`; the scraper skips them on every future run, so the queue only ever shrinks toward "done."

A second registry (`registry/claude-capabilities.json`) tracks 16 built-in Claude Code features — surfaced as `💡` awareness items matched to your stack.

### Add your skill

**The easy way** — open Claude Code and type `/new-skill`. The wizard walks you through name, description, tags, and trigger words; generates a properly-structured `skills/your-name/SKILL.md`, optionally wires a route in the main router, and appends a draft registry entry. Then you push it to your own GitHub repo and open a PR.

**The manual way:**

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
├── SKILL.md                         # Main entry — NL router (Routes A-T)
├── Makefile                         # Dev commands
├── CONTRIBUTING.md                  # How to add skills and contribute
│
├── skills/                          # 33 skills
│   ├── scaffold/   python/   nodejs/   terraform/   deploy/
│   ├── wordpress/  webapp/   graphql/  database/    suggest/
│   ├── sync/       hooks/    budget/   handoff/     clone/
│   ├── design/     dark-mode/ saas/    launch/      bootstrap/
│   ├── new-skill/      ← author a new skill via /new-skill
│   ├── update-skills/  ← refresh installed skills via /update-skills
│   ├── picker/         ← legacy redirect to /skill-bootstrap (kept for compat)
│   └── aws/ kubernetes/ cicd/ server/ digitalocean/
│       woocommerce/ wordpress-server/ php/ docker/ security/ db/
│
├── examples/                        # Reference outputs from /scaffold
│   ├── fastapi-postgres/            # Python + FastAPI + Postgres
│   └── nextjs-tailwind/             # Next.js + TypeScript + Tailwind
│
├── templates/
│   ├── hooks/          # lint.sh, block-dangerous.sh, test-on-edit.sh, notify-stop.sh
│   ├── vscode/         # extensions.json, settings.json, tasks.json
│   └── dark-mode/      # CSS tokens, toggle component, Black or White animation
│
├── registry/
│   ├── skills.json                  # 35 community skills (21 verified, incl. Anthropic + Vercel)
│   ├── discovered.json              # Candidate queue from the scraper (sorted, sectioned)
│   ├── rejected.json                # Repos rejected during review — scraper skips these
│   ├── claude-capabilities.json     # 16 built-in Claude Code features
│   └── discovered-capabilities.json # Weekly docs scan results
│
├── scripts/
│   ├── sync-export.py               # Export context → .claude-context/
│   ├── sync-import.py               # Import from .claude-context/ → correct hash
│   ├── fetch-skills.py              # GitHub scraper (10 queries, quality scoring, skips rejected)
│   ├── search-registry.py           # CLI search across the local registry
│   ├── review-queue.py              # Page/triage discovered.json — accept/reject decisions
│   ├── sync-tools.py                # Cross-tool memory bridge — write adapter files for every AI tool
│   ├── update-stars.py              # Star count refresher
│   └── validate-registry.py         # Structure + 404 validator
│
├── references/
│   ├── stacks.md                    # Version requirements + commands per stack
│   ├── environments.md              # Environment detection edge cases
│   └── vscode-extensions.md        # Per-stack VS Code extension + settings overrides
│
├── SECURITY.md                      # Disclosure flow + how to audit 3rd-party skills
│
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md     # PR checklist
    ├── ISSUE_TEMPLATE/              # Bug report + skill submission forms
    └── workflows/
        ├── sync-registry.yml        # Weekly: refresh stars + discover
        └── validate-registry.yml    # PR gate: blocks 404 repos
```

---

## Developer Commands

```bash
make validate               # validate registry structure (fast, no network)
make validate-full          # validate + verify all repos exist on GitHub
make test                   # alias for validate-full (CI entry point)
make search Q=<keyword>     # search the registry (e.g. make search Q=pdf)
make update-stars           # refresh star counts from GitHub API
make discover               # run scraper → registry/discovered.json
make discover-capabilities  # scan Claude Code releases → discovered-capabilities.json
```

**Search examples:**

```bash
make search Q=pdf       # → Anthropic Document Skills
make search Q=agents    # → 6 entries (Ruflo, Agent Orchestrator, Browser Use, ...)
make search Q=dashboard # → Octogent
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
