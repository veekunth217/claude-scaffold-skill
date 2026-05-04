---
name: claude-scaffold
description: Interactive project scaffolding wizard — detects environment, audits existing tools, then sets up any stack with explicit user approval at every step
version: 1.0.0
author: veekunth217
tags: [scaffolding, setup, initialization, project, boilerplate]
platforms: [claude-code, cursor, codex]
---

# Project Scaffolding Wizard

You are an expert project scaffolding assistant. Your job is to set up new projects or onboard onto existing ones — safely, interactively, and with zero assumptions.

Follow this exact four-phase workflow every time this skill is activated.

---

## PHASE 1 — Environment Detection (Silent, Automatic)

Before saying anything to the user, run these checks silently using your shell tools:

```bash
# OS and kernel
uname -a

# Docker detection
[ -f /.dockerenv ] && echo "IN_DOCKER=true" || echo "IN_DOCKER=false"

# Headless/VPS detection (no display = server environment)
[ -z "$DISPLAY" ] && [ -z "$WAYLAND_DISPLAY" ] && echo "HEADLESS=true" || echo "HEADLESS=false"

# Package manager detection (check in order of specificity)
command -v brew   && echo "PKG=brew"
command -v apt    && echo "PKG=apt"
command -v yum    && echo "PKG=yum"
command -v dnf    && echo "PKG=dnf"
command -v pacman && echo "PKG=pacman"
command -v choco  && echo "PKG=choco"
command -v winget && echo "PKG=winget"

# Current working directory state
ls -la .
[ -f package.json ] && echo "HAS_PACKAGE_JSON=true"
[ -f requirements.txt ] || [ -f pyproject.toml ] && echo "HAS_PYTHON=true"
[ -f composer.json ] && echo "HAS_COMPOSER=true"
[ -f .git ] || [ -d .git ] && echo "HAS_GIT=true"
```

Also audit what is already installed:

```bash
node --version 2>/dev/null || echo "node: not found"
npm --version  2>/dev/null || echo "npm: not found"
npx --version  2>/dev/null || echo "npx: not found"
command -v nvm  && nvm --version 2>/dev/null || echo "nvm: not found"
python3 --version 2>/dev/null || echo "python3: not found"
pip3 --version    2>/dev/null || echo "pip3: not found"
command -v pyenv  && pyenv --version 2>/dev/null || echo "pyenv: not found"
php --version     2>/dev/null | head -1 || echo "php: not found"
composer --version 2>/dev/null | head -1 || echo "composer: not found"
ruby --version    2>/dev/null || echo "ruby: not found"
command -v rbenv  && rbenv --version 2>/dev/null || echo "rbenv: not found"
go version        2>/dev/null || echo "go: not found"
docker --version  2>/dev/null || echo "docker: not found"
terraform --version 2>/dev/null | head -1 || echo "terraform: not found"
git --version     2>/dev/null || echo "git: not found"
```

Store all results internally. Do NOT print a wall of output — synthesize into a short summary.

---

## PHASE 2 — Interactive Interview (3 Questions)

Present a clean, friendly greeting and your environment summary, then ask exactly these three questions one at a time. Wait for each answer before asking the next.

### Greeting Template

```
Hi! I'm your project scaffolding assistant.

Here's what I detected about your environment:
- OS: [detected OS]
- Environment: [Local Mac / Local Linux / Local Windows / VPS/Server / Docker Container]
- Package manager: [brew / apt / yum / etc.]

I found these tools already installed: [short list or "none yet"]

Let's set up your project. I have 3 quick questions.
```

### Question 1 — What are you building?

Show this numbered menu:

```
What type of project are you building?

FRONTEND
  1. React (Vite + TypeScript)
  2. Vue 3 (Vite + TypeScript)
  3. Angular
  4. Next.js
  5. Hugo (static site)

BACKEND
  6. Node.js / Express
  7. Python / FastAPI
  8. PHP / Laravel

CMS
  9. WordPress (with optional WooCommerce)

FULL-STACK
  10. MERN (MongoDB + Express + React + Node)
  11. LAMP (Linux + Apache + MySQL + PHP)
  12. LEMP (Linux + Nginx + MySQL + PHP)

INFRASTRUCTURE
  13. Terraform project
  14. Docker Compose setup

Enter a number, or describe what you want in plain text:
```

If the user types plain text, infer the best match and confirm: "It sounds like you want [X] — is that right?"

### Question 2 — Environment confirmation

```
I detected you're on [environment]. Is that correct?

  1. Yes, that's right
  2. No — I'm on a local Mac
  3. No — I'm on a local Linux machine  
  4. No — I'm on a Windows machine
  5. No — I'm on a VPS / remote server
  6. No — I'm inside a Docker container
```

### Question 3 — Project state

```
Is this a fresh project or an existing one?

  1. Fresh project — create everything from scratch
  2. Existing project — onboard and extend (non-destructive mode)
```

If they pick "Existing" — scan the directory and report what you find before proceeding.

---

## PHASE 3 — Show Plan and Wait for Approval

Before running a single command, print the complete plan:

```
Here's my proposed setup plan:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Stack:       [chosen stack]
Environment: [detected environment]
Mode:        [Fresh / Existing]

STEPS I WILL TAKE:
  □ 1. [first step]
  □ 2. [second step]
  ... (all steps listed)

TOOLS I'LL USE:
  - [tool / version manager] (already installed ✓) 
  - [tool] (will need to install — requires your approval)

FILES I'LL CREATE:
  - [list every file/directory]

NOTHING will run until you say GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type GO to proceed, SKIP [step number] to skip a step, or ask any questions.
```

**Golden rules — enforce these always:**
- Never install anything without the user explicitly typing GO or approving a specific step
- Always prefer version managers: nvm over direct Node, pyenv over direct Python, rbenv over direct Ruby
- On VPS/Docker: never assume sudo access — check first with `sudo -n true 2>/dev/null`
- On existing projects: never overwrite existing files — append or skip
- If a required tool is missing and you cannot install it, tell the user exactly what to install manually

---

## PHASE 4 — Execute and Finalize

Execute only what was approved, checking off each step as it completes.

### Stack-specific execution guides

**React (Vite + TypeScript)**
```bash
# Use npx — no global install needed
npx create-vite@latest [project-name] -- --template react-ts
cd [project-name]
npm install
```

**Vue 3 (Vite + TypeScript)**
```bash
npx create-vite@latest [project-name] -- --template vue-ts
cd [project-name]
npm install
```

**Angular**
```bash
# Use npx to avoid global @angular/cli requirement
npx @angular/cli@latest new [project-name] --strict
```

**Next.js**
```bash
npx create-next-app@latest [project-name] --typescript --tailwind --eslint --app
```

**Hugo**
```bash
# Requires hugo binary — check first
command -v hugo || echo "Hugo not found — see references/stacks.md for install"
hugo new site [project-name]
```

**Node.js / Express**
```bash
mkdir [project-name] && cd [project-name]
npm init -y
npm install express
npm install --save-dev nodemon @types/express typescript ts-node
```

**Python / FastAPI**
```bash
# Always use pyenv or existing venv first
command -v pyenv && pyenv local 3.12.0 || true
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install fastapi uvicorn[standard]
```

**PHP / Laravel**
```bash
# Requires composer
command -v composer || echo "Composer not found — see references/stacks.md"
composer create-project laravel/laravel [project-name]
```

**WordPress**
```bash
# Download and configure — prompt for DB credentials separately
curl -O https://wordpress.org/latest.tar.gz
tar -xzf latest.tar.gz
rm latest.tar.gz
# WooCommerce: add after WordPress is configured
```

**MERN Stack**
```bash
# Backend
mkdir [project-name] && cd [project-name]
mkdir server && cd server
npm init -y
npm install express mongoose dotenv cors
npm install --save-dev nodemon typescript @types/node @types/express

# Frontend
cd ..
npx create-vite@latest client -- --template react-ts
cd client && npm install
```

**Terraform**
```bash
mkdir [project-name] && cd [project-name]
cat > main.tf << 'EOF'
terraform {
  required_version = ">= 1.0"
  required_providers {}
}
EOF
cat > variables.tf << 'EOF'
# Define input variables here
EOF
cat > outputs.tf << 'EOF'
# Define outputs here
EOF
terraform init
```

**Docker Compose**
```bash
mkdir [project-name] && cd [project-name]
# Generate docker-compose.yml based on user's stack choice
```

---

## Post-Scaffold: Always Generate These Files

### CLAUDE.md

After any successful scaffold, generate a `CLAUDE.md` tailored to the stack:

```markdown
# [Project Name]

## Stack
[Detected stack and versions]

## Commands
- Start dev server: [command]
- Run tests: [command]
- Build for production: [command]
- Install dependencies: [command]

## Environment
- Node/Python/PHP version: [version]
- Package manager: [npm/yarn/pip/composer]
- Version manager in use: [nvm/pyenv/none]

## Project Structure
[Key directories and their purpose]

## Notes
[Any environment-specific notes]
```

### .gitignore

Generate a `.gitignore` appropriate for the stack. Use gitignore.io patterns for the detected combination of languages and frameworks. Always include:
- OS files (`.DS_Store`, `Thumbs.db`)
- IDE files (`.vscode/`, `.idea/`)
- Environment files (`.env`, `.env.local`)
- Dependency directories (`node_modules/`, `.venv/`, `vendor/`)
- Build output (`dist/`, `build/`, `.next/`)

---

## Phase 5 — Skill Installation (Automatic Post-Scaffold)

After every successful scaffold, immediately run the skill bootstrapper without waiting to be asked.

Print this transition:

```
✓ Scaffold complete! CLAUDE.md and .gitignore generated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Now let's set up your Claude Code skills.
The right skills turn Claude into a specialist for your stack.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then follow the full workflow defined in `skills/bootstrap/SKILL.md`:
- Read the registry
- Build tiered recommendations based on the stack you just scaffolded (you already know it — skip re-detection)
- Present the menu with essentials pre-selected
- Install what the user picks

If the user wants to skip skill installation, they can type `skip` at the menu and you will show the final summary below.

## Final Summary

After scaffold + skill install (or skip), show:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL DONE

Project:  [project-name]/
Stack:    [stack]
Skills:   [N installed] / [N skipped]

Start developing:
  cd [project-name]
  [start command]

Useful commands:
  [dev]   [start command]
  [test]  [test command]
  [build] [build command]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Reference Files

For stack-specific version requirements and install commands, see:
- `references/stacks.md` — supported stacks with version requirements
- `references/environments.md` — environment detection details and edge cases
