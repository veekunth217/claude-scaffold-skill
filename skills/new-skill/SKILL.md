---
name: new-skill
description: Scaffold a new Claude Code skill — generates SKILL.md with proper frontmatter, optionally wires a route in the main SKILL.md, and prepares it for PR submission to the registry.
version: 1.0.0
author: veekunth217
tags: [meta, skill-author, contributor, scaffold, registry]
platforms: [claude-code, cursor, codex]
---

# /new-skill — Skill Author Wizard

You help a community contributor scaffold a new Claude Code skill the right way.

**RULE: Show the full plan and wait for `GO` before creating any files.**

---

## Phase 1 — Detect Context

Run silently before talking:

```bash
# Are we inside the claude-scaffold-skill repo?
[ -f SKILL.md ] && grep -q "claude-scaffold-skill\|veekunth217" SKILL.md 2>/dev/null && echo "IN_SCAFFOLD_REPO=true" || echo "IN_SCAFFOLD_REPO=false"

# Are we in any skills folder structure?
[ -d skills ] && echo "HAS_SKILLS_DIR=true"

# Existing skills (to avoid name collisions)
[ -d skills ] && ls -1 skills/ 2>/dev/null

# Current git remote
git config --get remote.origin.url 2>/dev/null
```

Synthesize into one short summary — don't dump output.

---

## Phase 2 — Gather Skill Details

Ask these in order. Wait for each answer before the next.

### Question 1 — Skill name (slash command)

```
What's the slash command for your skill?
(short, lowercase, hyphenated — becomes /your-skill)

Examples:
  /lint-fix       — opinionated lint + auto-fix workflow
  /pr-review      — wrapper around code review tools
  /db-seed        — generates seed data from a schema
  /a11y-audit     — accessibility audit on the current frontend
```

Validate the answer:
- Lowercase letters, digits, hyphens only
- 2-30 characters
- Not already in `skills/` folder (check from Phase 1 detection)
- If collision: tell them which existing skill conflicts and ask for a different name

### Question 2 — One-sentence description

```
In one sentence (under 150 chars), what does this skill do?
This goes in the registry and shows up in /bootstrap recommendations.

Good examples:
  "Generates seed data for any Postgres/MySQL schema with realistic faker values"
  "Runs WCAG 2.2 audit on the current frontend, produces fix-ordered report"

Bad (vague):
  "A useful tool for developers"
```

### Question 3 — Skill type

```
What kind of skill is this?

  1. Wizard — asks questions, then generates files / runs commands
  2. Reference — provides snippets and config guidance, no generation
  3. Hybrid — answers + may generate small artifacts

(Wizards must always show a plan + wait for GO. Reference skills don't need that.)
```

### Question 4 — Tags

```
What tags apply? (3-5, lowercase, hyphens not spaces)

Common existing tags you can reuse for cross-discovery:
  Languages:  python, nodejs, php, rust, go, typescript
  Roles:      frontend, backend, fullstack, devops
  Tools:      docker, kubernetes, terraform, react, nextjs
  Features:   testing, security, deploy, migrations, auth
```

### Question 5 — Trigger words for the main router (optional)

```
If your skill belongs in the main /scaffold router, what trigger words
should activate it? (comma-separated)

Examples:
  /lint-fix:  "lint, format, prettier, eslint, code style"
  /pr-review: "review pr, code review, pull request review"

Type SKIP if this skill is standalone (only invoked directly via its slash command).
```

### Question 6 — Author handle

```
What's your GitHub username? (used in the SKILL.md frontmatter)
```

---

## Phase 3 — Show Plan and Wait for GO

Print this exact format with the captured answers filled in:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEW SKILL — PROPOSED PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Slash command:   /[name]
Type:            [Wizard / Reference / Hybrid]
Description:     [one-sentence description]
Tags:            [tags comma-separated]
Author:          [github-handle]

FILES I WILL CREATE:
  skills/[name]/SKILL.md         (frontmatter + scaffold body)

ROUTER UPDATE (main SKILL.md):
  [if trigger words provided]
  → Add Route [next-letter] with triggers: [trigger words]
  [if SKIP]
  → No router update needed (standalone skill)

REGISTRY ENTRY (registry/skills.json):
  Will append a draft entry with verified=false.
  You'll need to push to your own GitHub repo and update the
  install line before opening a PR.

VALIDATION:
  After generating, I will run `make validate` to confirm everything
  passes. The CI workflow will re-validate when you open a PR.

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type GO to generate, EDIT to change any answer, or CANCEL.
```

---

## Phase 4 — Generate Files

When the user types GO, generate:

### A. `skills/[name]/SKILL.md`

For a **Wizard** skill, use this template:

```markdown
---
name: [name]
description: [one-sentence description]
version: 1.0.0
author: [github-handle]
tags: [comma-separated tags wrapped in brackets]
platforms: [claude-code, cursor, codex]
---

# /[name] — [Title Case Name]

[One-paragraph what-it-does explanation.]

**RULE: Show the full plan and wait for `GO` before [the destructive thing your skill does].**

---

## Phase 1 — Detect

[What does the skill silently check before greeting? List the bash commands.]

```bash
# Add detection commands here
```

---

## Phase 2 — Ask Focused Questions

[3-5 questions the skill needs answered before it can build the plan.]

### Question 1 — [topic]
```
[exact prompt text shown to user]
```

### Question 2 — [topic]
```
[exact prompt text]
```

---

## Phase 3 — Show Plan, Wait for GO

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[SKILL NAME] — PROPOSED PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Restate user's choices]

FILES I WILL CREATE:
  [list every file/directory]

COMMANDS I WILL RUN:
  [list every shell command]

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type GO to proceed.
```

---

## Phase 4 — Execute

[The actual generation/execution steps, only run after GO.]

---

## Phase 5 — Summary

```
✓ [Skill name] complete!

What was done:
  - [bullet]
  - [bullet]

Next steps:
  - [what user should do]
```
```

For a **Reference** skill, use a simpler template — no Phase 3/Phase 4, just sections of guidance organized by topic.

For a **Hybrid** skill, combine — use the wizard template but mark sections that don't generate files clearly.

### B. Update `SKILL.md` (main router) — only if trigger words provided

Find the next available route letter (T, U, V, ...) and append a route block:

```markdown
### Route [letter] — [Title Case Name]
**Trigger words:** [comma-separated trigger words]

→ Confirm: "Got it — [restate the goal]. Let me walk you through it."
→ Hand off to: `skills/[name]/SKILL.md`
```

Insert it before the catch-all "Route K" block in `SKILL.md`.

### C. Append draft registry entry to `registry/skills.json`

Add this entry to the array:

```json
{
  "name": "[Title Case Name]",
  "repo": "[github-handle]/[repo-slug-placeholder]",
  "description": "[description]",
  "tags": [comma-separated tags],
  "install": "git clone https://github.com/[github-handle]/[repo-slug-placeholder].git ~/.claude/skills/[name]",
  "stars": 0,
  "verified": false,
  "added": "[YYYY-MM-DD]"
}
```

The user will need to:
1. Push their skill to a GitHub repo
2. Update `repo` and `install` paths to match their real repo
3. Open a PR

### D. Run `make validate`

If validation fails, surface the exact errors and offer to fix them.

---

## Phase 5 — Final Summary

```
✓ Skill scaffolded successfully!

Created:
  skills/[name]/SKILL.md

Updated:
  [SKILL.md — if route added]
  [registry/skills.json — draft entry appended]

To submit your skill to the registry:

  1. Customize skills/[name]/SKILL.md with your actual logic
  2. Push to your own GitHub repo:
       gh repo create [name] --public --source=.
       git push -u origin main
  3. Update registry/skills.json with the real repo URL
  4. Run: make validate-full
  5. Open a PR against veekunth217/claude-scaffold-skill

Test it locally first:
  Open Claude Code in any folder → type /[name]

Reference: see CONTRIBUTING.md for the full submission guide.
```
