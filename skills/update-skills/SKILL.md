---
name: update-skills
description: Pull the latest version of claude-scaffold-skill (and other installed skills) — shows the changelog, asks before applying, validates after.
version: 1.0.0
author: veekunth217
tags: [update, refresh, maintenance, install, registry, skills]
platforms: [claude-code, cursor, codex]
---

# /update-skills — Refresh Installed Skills

Keeps your `~/.claude/skills/` directory current. Pulls the latest commits from the upstream repo for `claude-scaffold-skill` and any other skills you've installed via `git clone`, shows you what changed, and waits for `GO` before applying.

**RULE: Show every change before pulling. Wait for `GO` before running `git pull` on any skill.**

---

## Phase 1 — Detect Installed Skills

Run silently:

```bash
# Find all skill directories under ~/.claude/skills/
SKILLS_ROOT="$HOME/.claude/skills"
[ ! -d "$SKILLS_ROOT" ] && echo "MISSING=true" && exit 0

# List skill folders that are git repositories (i.e. installed via git clone)
for d in "$SKILLS_ROOT"/*/; do
  [ -d "$d/.git" ] || continue
  name=$(basename "$d")
  cd "$d"
  remote=$(git config --get remote.origin.url 2>/dev/null)
  branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
  ahead_behind=$(git fetch --quiet 2>/dev/null && git rev-list --count --left-right "$branch...origin/$branch" 2>/dev/null)
  echo "SKILL=$name|REMOTE=$remote|BRANCH=$branch|AHEAD_BEHIND=$ahead_behind"
done
```

Parse the output into a table — for each skill, you now know:
- name (folder)
- remote URL
- current branch
- how many commits **behind** origin (number of new updates available)
- how many commits **ahead** (your local edits, if any)

---

## Phase 2 — Show Update Summary

Print this exact format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTALLED SKILLS — UPDATE STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Found [N] skill(s) installed via git:

  ✓ Up to date:
    [list skills with 0 commits behind]

  ⬆ Updates available:
    [N]  claude-scaffold-skill   (8 commits behind main)
    [N]  some-other-skill        (3 commits behind main)

  ⚠ Local changes:
    [list any with commits ahead — would be merged, not lost]

  ⚠ Detached / non-standard branch:
    [list any not on main/master]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

For each skill that has updates, show the **commit log preview**:

```
─────────────────────────────────────
What's new in claude-scaffold-skill:
─────────────────────────────────────
3be461d chore: public-readiness fixes — flag stub skills, anonymize
3940801 feat: /new-skill wizard + examples folder + Route T
ca4a2e2 docs: README — surface document support, search command
ed3f1ba feat: registry search via 'make search Q=<keyword>'
dba9e93 feat: Anthropic + Vercel skills, scaffold UX fix, security
... (showing latest 5)
```

Generate the log with:

```bash
cd "$SKILLS_ROOT/$skill_name"
git log --oneline HEAD..origin/main | head -10
```

---

## Phase 3 — Show Plan, Wait for GO

```
PROPOSED PLAN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I will run `git pull` on these skills:
  □ claude-scaffold-skill
  □ some-other-skill

I will SKIP:
  - skill-with-local-changes (would need merge — review manually)
  - skill-on-feature-branch  (you're not on main, leaving alone)

After pulling, I will:
  □ Run `make validate` on claude-scaffold-skill (registry sanity check)
  □ Show you the updated skill count and any new slash commands

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type GO to update all, NUMBERS (e.g. "1 3") to update specific skills,
or CANCEL to skip.
```

---

## Phase 4 — Apply Updates

For each approved skill, run:

```bash
cd "$SKILLS_ROOT/$skill_name"
git pull --ff-only
```

If `--ff-only` fails (because of local edits), do not force. Stop, surface the issue:

```
⚠️ Could not update [skill] — you have local edits.

Options:
  A) Review your edits:  cd ~/.claude/skills/[skill] && git status
  B) Stash and pull:     git stash && git pull && git stash pop
  C) Discard your edits: git reset --hard origin/main  (DANGEROUS)

Skipping this skill for now. Re-run /update-skills after resolving.
```

Otherwise, run the post-update validator if the skill has one:

```bash
[ -f "$SKILLS_ROOT/$skill_name/Makefile" ] && \
  grep -q "^validate:" "$SKILLS_ROOT/$skill_name/Makefile" && \
  (cd "$SKILLS_ROOT/$skill_name" && make validate)
```

---

## Phase 5 — Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UPDATE COMPLETE

✓ Pulled:
  - claude-scaffold-skill (8 new commits)

⊝ Skipped:
  - some-other-skill (had local edits)

✗ Failed:
  - [any that errored]

To activate updated skills in this Claude Code session:
  Restart Claude Code, or run: /refresh
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases

**No skills installed yet:**
```
No skills found in ~/.claude/skills/.
Install one first:
  git clone https://github.com/veekunth217/claude-scaffold-skill.git \
    ~/.claude/skills/claude-scaffold-skill
```

**Skills installed via the Vercel CLI (`npx skills add`)** appear as regular folders without their own `.git/` — those are managed by the CLI, not us. Detect and tell the user:
```
⚠️  Some skills look like they were installed via the Vercel skills CLI:
    [list them]
    Run: npx skills update  (manages those separately)
```

**Skills installed via Claude Code plugin marketplace** (e.g. Anthropic document skills via `/plugin install`):
```
ℹ️  These are managed by Claude Code itself, not by /update-skills.
   Update via: /plugin update
```

---

## Notes

- This skill never modifies skills outside `~/.claude/skills/`.
- It uses `--ff-only` to avoid surprise merge commits.
- It does NOT delete uninstalled skills automatically — use `rm -rf ~/.claude/skills/<name>` for that.
- Star-count refreshes for the registry happen via the **weekly GitHub Action** in this repo, independent of this skill.
