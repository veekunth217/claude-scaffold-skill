# claude-scaffold-skill

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Skills: 3](https://img.shields.io/badge/Skills-3-green.svg)
![Registry: 16 skills](https://img.shields.io/badge/Registry-16%20skills-orange.svg)
![Last Updated](https://img.shields.io/badge/Updated-May%202026-lightgrey.svg)

An open-source Claude Code skill repository with **three core features**:
1. **Scaffolding Wizard** — set up any stack interactively, safely, from any environment
2. **Skill Picker** — find and install the right community skill for your task
3. **Community Registry** — auto-discovering, curated index of Claude Code skills

---

## What It Does

### 1. Project Scaffolding Wizard (`SKILL.md`)

An interactive wizard that:
- **Detects your environment** (Mac, Linux, Windows, VPS, Docker) before asking anything
- **Audits what's already installed** (Node, Python, PHP, Docker, etc.) — never assumes
- **Asks 3 questions** to understand your stack and goals
- **Shows the full plan** and waits for your approval before running a single command
- **Always uses version managers** (nvm, pyenv, rbenv) over direct installs
- **Generates `CLAUDE.md`** and `.gitignore` after scaffolding

**Safe for:** local machines, VPS consoles, Docker containers, CI environments.

### 2. Skill Picker (`skills/picker/SKILL.md`)

A discovery assistant that:
- Asks what you're trying to accomplish in plain English
- Reads `registry/skills.json` and scores skills by relevance
- Recommends the **top 3 matching skills** with explanations of why they fit
- Offers to install any of them with your confirmation

### 3. Community Registry (`registry/skills.json`)

A curated, versioned JSON registry of Claude Code skills that:
- Is **auto-updated weekly** via GitHub Actions (discoveries go to `discovered.json` for review)
- Has a **scraper** (`scripts/fetch-skills.py`) you can run locally
- Requires **maintainer review** before skills are added to the main registry
- Is validated by `scripts/validate-registry.py` on every PR

---

## Quick Install

```bash
# Clone to your Claude skills directory
git clone https://github.com/veekunth217/claude-scaffold-skill.git ~/.claude/skills/claude-scaffold-skill

# Verify it's there
ls ~/.claude/skills/claude-scaffold-skill/
```

Then in Claude Code, activate the skill with:
```
/scaffold
```

---

## Usage

### Scaffolding Wizard

```
/scaffold
```

The wizard will:
1. Silently detect your environment and installed tools
2. Ask what you're building (shows a menu of stacks)
3. Confirm your environment
4. Ask if this is a fresh or existing project
5. Show the full plan — wait for your **GO**
6. Execute and generate `CLAUDE.md` + `.gitignore`

### Skill Picker

```
/skill-picker
```

Example session:
```
You: I want to add AI/LLM features to my Python app

Skill Picker: Found 3 matches...

#1 — Claude Code Expert (verified ✓)
    54-skill collection with AI/ML agents and Python specialization...

#2 — Everything Claude Code
    Comprehensive tips for integrating Claude into development workflows...

Would you like to install any? (1, 2, 3, all, or none)
```

### Run the Scraper Locally

```bash
export GITHUB_TOKEN=your_token_here
python scripts/fetch-skills.py

# With custom output
python scripts/fetch-skills.py --output /tmp/new-skills.json
```

### Validate the Registry

```bash
python scripts/validate-registry.py
# Valid! 7 entries, 7 verified.
```

---

## Supported Stacks

| Category | Stack | Key Tools |
|----------|-------|-----------|
| Frontend | React | Vite, TypeScript, npx |
| Frontend | Vue 3 | Vite, TypeScript, npx |
| Frontend | Angular | @angular/cli via npx |
| Frontend | Next.js | create-next-app, Tailwind |
| Frontend | Hugo | Hugo binary, themes |
| Backend | Node.js / Express | npm, nodemon, TypeScript |
| Backend | Python / FastAPI | pyenv, uvicorn, venv |
| Backend | PHP / Laravel | composer, artisan |
| CMS | WordPress | + WooCommerce option |
| Full-stack | MERN | MongoDB, Express, React, Node |
| Full-stack | LAMP | Apache, MySQL, PHP |
| Full-stack | LEMP | Nginx, MySQL, PHP |
| Infra | Terraform | tfenv, providers |
| Infra | Docker Compose | docker compose v2 |

---

## Community Registry

### Current Skills (16 entries — 7 verified)

| Skill | Repo | Verified | Tags |
|-------|------|----------|------|
| Claude Code Scaffolding | hmohamed01/Claude-Code-Scaffolding-Skill | ✓ | scaffolding, 70+ templates |
| Claude Code Expert | reedmayhew18/claude-code-expert | ✓ | wizard, agents, workflow |
| Everything Claude Code | affaan-m/everything-claude-code | ✓ | collection, tips |
| Superpowers | obra/superpowers | ✓ | professional, workflow |
| UI/UX Pro Max | nextlevelbuilder/ui-ux-pro-max-skill | ✓ | design, 67 styles |
| Claude Skills | mastepanoski/claude-skills | ✓ | debugging, docs |
| Code Review Graph | tirth8205/code-review-graph | ✓ | review, graph analysis |
| Claude Code Toolkit | applied-artificial-intelligence/claude-code-toolkit | — | workflow, planning, memory |
| Get Shit Done (GSD) | gsd-build/get-shit-done | — | spec, planning, phases |
| Awesome Claude Code | hesreallyhim/awesome-claude-code | — | collection, reference |
| Agent Orchestrator | ComposioHQ/agent-orchestrator | — | agents, orchestration |
| claude-mem | thedotmack/claude-mem | — | memory, token-saving |
| gstack *(future)* | garrytan/gstack | — | scaffolding, full-stack |
| OpenMemory *(future)* | CaviraOSS/OpenMemory | — | memory, agents |
| Free Claude Code *(future)* | Alishahryar1/free-claude-code | — | community |
| Browser Use *(future)* | browser-use/browser-use | — | browser, automation |

### How the Auto-Discovery Works

```
Every Sunday at midnight UTC
         ↓
GitHub Action runs fetch-skills.py
         ↓
Searches: topic:claude-skill, topic:claude-code-skill, filename:SKILL.md
         ↓
Deduplicates against existing registry
         ↓
Writes → registry/discovered.json
         ↓
Opens GitHub Issue listing new discoveries
         ↓
Maintainer reviews → merges PR to skills.json
```

---

## How to Contribute a Skill

### Option A: Submit to the Registry

1. Fork this repo
2. Add your skill entry to `registry/skills.json`:

```json
{
  "name": "Your Skill Name",
  "repo": "your-github-username/your-repo",
  "description": "One clear sentence describing what it does",
  "tags": ["relevant", "tags", "here"],
  "install": "git clone https://github.com/your-github-username/your-repo.git ~/.claude/skills/your-skill",
  "stars": 0,
  "verified": false,
  "added": "2026-05-04"
}
```

3. Run the validator: `python scripts/validate-registry.py`
4. Open a PR — a maintainer will review and set `"verified": true`

### Option B: Make Your Repo Discoverable

Add these topics to your GitHub repo so the weekly scraper finds it:
- `claude-skill`
- `claude-code-skill`

And put a `SKILL.md` in your repo root with YAML frontmatter:

```yaml
---
name: your-skill-name
description: What your skill does
version: 1.0.0
author: your-github-username
tags: [tag1, tag2, tag3]
---
```

---

## Project Structure

```
claude-scaffold-skill/
├── SKILL.md                        # Main scaffolding wizard
├── README.md                       # This file
├── LICENSE                         # MIT
├── .github/
│   └── workflows/
│       └── sync-registry.yml       # Weekly auto-discovery action
├── skills/
│   └── picker/
│       └── SKILL.md                # Skill picker/recommender
├── registry/
│   ├── skills.json                 # Curated community registry
│   └── discovered.json             # Auto-generated weekly discoveries
├── scripts/
│   ├── fetch-skills.py             # GitHub scraper
│   └── validate-registry.py       # Registry structure validator
└── references/
    ├── stacks.md                   # Stack version requirements & commands
    └── environments.md             # Environment detection edge cases
```

---

## Credits

Built on patterns and inspiration from:
- [hmohamed01/Claude-Code-Scaffolding-Skill](https://github.com/hmohamed01/Claude-Code-Scaffolding-Skill) — 70+ template scaffolding approach and conversational CLI patterns
- [reedmayhew18/claude-code-expert](https://github.com/reedmayhew18/claude-code-expert) — active/available skill split, context budgeting, and production wizard design

This project takes the best ideas from both and adds environment-aware detection, a community registry, and auto-discovery tooling.

---

## License

MIT — see [LICENSE](LICENSE)
