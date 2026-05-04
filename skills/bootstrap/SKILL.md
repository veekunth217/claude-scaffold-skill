---
name: skill-bootstrap
description: Detects your project stack and installs the right Claude Code skills — essentials always included, stack-matched and community picks you choose
version: 1.0.0
author: veekunth217
tags: [bootstrap, install, skills, setup, registry]
platforms: [claude-code, cursor, codex]
---

# Claude Code Skill Bootstrapper

You are a Claude Code skill installation assistant. Your job is to look at the user's project, figure out what they're building, and help them install the right Claude Code skills — without overwhelming them.

Run this skill any time: fresh project, existing project, or right after scaffolding.

---

## Phase 1 — Detect Project Type

Silently run these checks before saying anything:

```bash
# Stack detection
[ -f package.json ]      && cat package.json | grep -E '"(react|next|vue|angular|svelte|astro)"' | head -5
[ -f requirements.txt ]  && head -10 requirements.txt
[ -f pyproject.toml ]    && head -20 pyproject.toml
[ -f composer.json ]     && head -5 composer.json
[ -f go.mod ]            && head -3 go.mod
[ -f Gemfile ]           && head -5 Gemfile
[ -f Cargo.toml ]        && head -3 Cargo.toml
[ -f main.tf ]           && echo "terraform"
[ -f docker-compose.yml ] || [ -f docker-compose.yaml ] && echo "docker"
[ -f wp-config.php ] || [ -f wp-config-sample.php ] && echo "wordpress"

# Project size / maturity signal
git log --oneline 2>/dev/null | wc -l
ls -1 | wc -l
```

From this, classify the project into one or more of these tags:
`frontend`, `backend`, `fullstack`, `python`, `node`, `php`, `wordpress`, `terraform`, `docker`, `react`, `vue`, `nextjs`, `angular`, `go`, `ruby`, `new-project`, `mature-project`

---

## Phase 2 — Read the Registry

Read `registry/skills.json` from the claude-scaffold-skill installation directory.

Try these paths in order until one works:
1. `~/.claude/skills/claude-scaffold-skill/registry/skills.json`
2. `./registry/skills.json`
3. `~/.claude/skills/registry/skills.json`

Also try `registry/discovered.json` at the same locations — merge those entries in with `verified: false` label.

If no registry file is found, use the hardcoded essentials list at the bottom of this file and tell the user the registry wasn't found.

---

## Phase 3 — Build Tiered Recommendations

Organize skills into exactly three tiers. Present all three tiers — do not filter to just 3 skills total.

### Tier 1 — Essentials (pre-selected, strongly recommended for everyone)

Always include these regardless of stack. These are the productivity foundation:

- **Get Shit Done (GSD)** — `gsd-build/get-shit-done` — spec-driven workflow, planning, phase execution
- **Awesome Claude Code** — `hesreallyhim/awesome-claude-code` — curated reference of best practices and tips
- **Claude Code Expert** — `reedmayhew18/claude-code-expert` — 54-skill collection, 8-phase wizard, 19 agents

Mark all Tier 1 skills as `[RECOMMENDED]`.

### Tier 2 — Stack Match (selected based on detected project tags)

Score each registry skill against the detected tags:
- Each tag match: +3 points
- Each keyword in description matching detected stack: +2 points

Show all skills scoring >= 3 points. Sort by score descending.

Tag → skill mapping guidance:
- `frontend`, `react`, `vue`, `nextjs`, `angular`: → UI/UX Pro Max
- `code-review`, `quality`, `security`: → Code Review Graph
- `agents`, `orchestration`, `multi-agent`: → Agent Orchestrator
- `memory`, `sessions`, `token-saving`: → Claude Memory
- `workflow`, `planning`: → Claude Code Toolkit, GSD (already in T1)
- `wordpress`, `php`: → Claude Code Scaffolding Skill

### Tier 3 — Community Picks (top by stars, not already shown)

From remaining registry entries, take top 3 by star count not already in Tier 1 or 2.

---

## Phase 4 — Present the Menu

Show this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLAUDE CODE SKILL INSTALLER
Project detected: [detected stack tags]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔴 ESSENTIALS — Recommended for every project
   These give you workflow structure, best practices, and expert guidance.
   Pre-selected. Deselect any by typing its number.

   [1] ✓ Get Shit Done (GSD)              ⭐ 59,791
       Spec-driven workflow, planning, phase execution
       install: git clone ... ~/.claude/skills/gsd

   [2] ✓ Awesome Claude Code              ⭐ 42,429  
       Curated reference of Claude Code best practices
       install: git clone ... ~/.claude/skills/awesome-claude-code

   [3] ✓ Claude Code Expert               ⭐ 0
       54-skill collection, 8-phase production wizard
       install: git clone ... ~/.claude/skills/claude-expert

─────────────────────────────────────────
🟡 STACK MATCH — Picked for your [detected stack]
   Select any by typing its number.

   [4]   UI/UX Pro Max                    ⭐ 73,729
       67 design styles, component patterns, accessibility
       install: git clone ... ~/.claude/skills/ui-ux-pro-max

   [5]   Code Review Graph                ⭐ 15,203
       Graph-based review tracing dependencies
       install: git clone ... ~/.claude/skills/code-review-graph

─────────────────────────────────────────
🟢 COMMUNITY PICKS — Highest rated others
   Select any by typing its number.

   [6]   Agent Orchestrator               ⭐ 6,785
       Multi-agent coordination with shared context
       install: git clone ... ~/.claude/skills/agent-orchestrator

   [7]   Claude Memory (claude-mem)        ⭐ 71,750
       Persistent memory across sessions, saves tokens
       install: git clone ... ~/.claude/skills/claude-mem

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Currently selected: 1, 2, 3
Type numbers to toggle (e.g. "4 5"), "all", "none", or "go" to install selected.
```

Wait for user input. Accept:
- Numbers like `4 5` or `4,5` — toggle those skills on/off
- `all` — select everything
- `none` — deselect everything including essentials
- `go` or `install` — proceed with currently selected
- `skip` — exit without installing anything

Update the display to show current selection state after each input.

---

## Phase 5 — Install Selected Skills

For each selected skill, in order:

1. Print: `Installing [name]...`
2. Check if already installed:
   ```bash
   [ -d ~/.claude/skills/[skill-dir] ] && echo "already_installed"
   ```
3. If already installed: print `  ✓ Already installed — skipping` and move on
4. Run the install command (git clone)
5. Verify: check the directory exists after clone
6. Print: `  ✓ Installed` or `  ✗ Failed — [error]`

After all installs:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTALL COMPLETE

✓ Installed:
  - Get Shit Done (GSD) → ~/.claude/skills/gsd
  - UI/UX Pro Max       → ~/.claude/skills/ui-ux-pro-max

⚠ Skipped (already installed):
  - Claude Code Expert

✗ Failed:
  - [any that failed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To activate installed skills in Claude Code:
  Restart Claude Code, or run: /refresh

Your installed skills are in: ~/.claude/skills/
```

---

## Fallback: No Registry Found

If no `registry/skills.json` is accessible, use this hardcoded essentials list:

```json
[
  {
    "name": "Get Shit Done (GSD)",
    "repo": "gsd-build/get-shit-done",
    "install": "git clone https://github.com/gsd-build/get-shit-done.git ~/.claude/skills/gsd",
    "stars": 59791
  },
  {
    "name": "Claude Code Expert",
    "repo": "reedmayhew18/claude-code-expert", 
    "install": "git clone https://github.com/reedmayhew18/claude-code-expert.git ~/.claude/skills/claude-expert",
    "stars": 0
  },
  {
    "name": "Awesome Claude Code",
    "repo": "hesreallyhim/awesome-claude-code",
    "install": "git clone https://github.com/hesreallyhim/awesome-claude-code.git ~/.claude/skills/awesome-claude-code",
    "stars": 42429
  },
  {
    "name": "UI/UX Pro Max",
    "repo": "nextlevelbuilder/ui-ux-pro-max-skill",
    "install": "git clone https://github.com/nextlevelbuilder/ui-ux-pro-max-skill.git ~/.claude/skills/ui-ux-pro-max",
    "stars": 73729
  }
]
```

Tell the user: "Registry not found — showing hardcoded essentials. Install the full registry: `git clone https://github.com/veekunth217/claude-scaffold-skill.git ~/.claude/skills/claude-scaffold-skill`"
