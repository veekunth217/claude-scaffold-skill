# Contributing to claude-scaffold-skill

Thanks for wanting to contribute. There are three ways to help.

---

## 1. Add a Skill to the Registry

**Option A — Submit a PR:**

1. Fork this repo
2. Edit `registry/skills.json` — add your entry at the end of the array:

```json
{
  "name": "Your Skill Name",
  "repo": "github-username/repo-name",
  "description": "One sentence, max 120 chars, what it does",
  "tags": ["relevant", "tags"],
  "install": "git clone https://github.com/github-username/repo-name.git ~/.claude/skills/repo-name",
  "stars": 0,
  "verified": false,
  "added": "YYYY-MM-DD"
}
```

3. Validate: `python scripts/validate-registry.py`
4. Open a PR — a maintainer sets `"verified": true` after review

**Option B — Make your repo auto-discoverable:**

Add these GitHub topics to your repo:
- `claude-skill`
- `claude-code-skill`

And put a `SKILL.md` in your root with YAML frontmatter:

```yaml
---
name: your-skill-name
description: What your skill does
version: 1.0.0
author: your-github-username
tags: [tag1, tag2]
---
```

The weekly scraper will find it and open a GitHub Issue for maintainer review.

### What the scraper actually does (and what it doesn't)

The scraper **never auto-adds skills to `registry/skills.json`.** It writes everything it finds to `registry/discovered.json` — a sorted review queue — with a quality score from 0–100. Each run it also diffs against the previous `discovered.json` and opens a GitHub Issue **only for the candidates that are new since last time** (or stays silent if nothing new appeared). The full browsable queue always lives in `discovered.json`; the Issue is just a nudge about what changed. Maintainers PR only the skills that pass review.

**Quality scoring breakdown (max 100):**

| Signal | Points | Why it matters |
|---|---|---|
| Has `SKILL.md` in root | 30 | Confirms it's actually a Claude Code skill |
| Uses canonical topic (`claude-skill` / `claude-skills` / `claude-code-skill` / `claude-code-skills`) | 20 | Author tagged it correctly |
| Description ≥ 30 chars | 20 | Skill explains itself |
| Stars ≥ 10 | 15 | Some community validation |
| Pushed within last 365 days | 10 | Still maintained |
| Has `README.md` | 5 | Basic documentation |
| Archived repo | **−30** | Strong negative signal |

**Flags that lower priority but don't block:**
- `low_stars` — under 3 stars
- `stale` — no commits in 12+ months
- `thin_desc` — description shorter than 30 chars
- `non_canonical_topic` — found via fallback search, not a canonical tag
- `thin_fork` — small fork without original work

**What we look for during human review (qualitative):**
- Does the SKILL.md follow the **confirm-before-generate** pattern? (Phase 1 detect → ask → show plan → wait for GO → execute)
- Is the scope focused? (one job, done well — not a kitchen sink)
- Is the install path reasonable? (not running arbitrary remote code)
- Does it duplicate an existing registry entry? (we prefer one well-maintained skill over five forks)

---

## 2. Improve the Scaffolding Wizard

The main `SKILL.md` is the scaffolding wizard. If you want to add a new stack:

1. Add the stack entry to the **Question 1 menu** in `SKILL.md`
2. Add a **Stack-specific execution guide** section
3. Update `references/stacks.md` with version requirements and commands
4. Test on at least two environments (local + VPS or Docker)
5. Open a PR

Stack additions must follow the golden rules:
- Never auto-install without user approval
- Always prefer version managers
- Safe for VPS console use (no GUI assumptions)
- Non-destructive on existing projects

---

## 3. Improve the Skill Picker

Edit `skills/picker/SKILL.md` to improve the scoring logic, formatting, or fallback behavior. Keep it under 5000 tokens total.

---

## Registry Schema Reference

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| name | string | yes | Display name |
| repo | string | yes | `user/repo` format |
| description | string | yes | Max 120 chars |
| tags | string[] | yes | Max 10, lowercase, hyphenated |
| install | string | yes | Full git clone command |
| stars | integer | yes | Use 0 if unknown |
| verified | boolean | yes | Set to false on submission |
| added | string | yes | YYYY-MM-DD |
| future | boolean | no | Use true for tracking-only entries |

Run `python scripts/validate-registry.py` before every PR. It exits 0 on success, 1 on errors.

---

## Code of Conduct

- Be respectful in PR reviews and issues
- No spam entries — every registry submission must be a real, working skill
- Verified skills must have a working `SKILL.md` with YAML frontmatter
