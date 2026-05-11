---
name: review-skills
description: Page through the discovered-skills queue 25 at a time — keep the good ones into the verified registry, reject the rest so they never re-appear. Resumes where you left off.
version: 1.0.0
author: veekunth217
tags: [review, triage, registry, discovery, maintainer, curation]
platforms: [claude-code, cursor, codex]
---

# /review-skills — Triage the Discovery Queue

The weekly scraper drops every Claude Code skill it finds into `registry/discovered.json`, sorted by quality score. This skill walks you through that queue **25 at a time**, so you can decide per skill: **keep** (→ verified registry) or **reject** (→ never shown again). Your decisions persist between sessions — next run picks up where you stopped.

**RULE: Never modify `registry/skills.json` or `registry/rejected.json` without showing the user the exact change and getting `GO`.**

---

## Phase 1 — Where Are We

Run silently:

```bash
# Must be inside the claude-scaffold-skill repo (or have it as ~/.claude/skills/claude-scaffold-skill)
[ -f registry/discovered.json ] && echo "HERE=local" || \
  ([ -f ~/.claude/skills/claude-scaffold-skill/registry/discovered.json ] && echo "HERE=installed" || echo "HERE=missing")

# Status snapshot
python scripts/review-queue.py --status 2>/dev/null || \
  python ~/.claude/skills/claude-scaffold-skill/scripts/review-queue.py --status 2>/dev/null
```

If `HERE=missing`:
```
No discovery queue found. Run the scraper first:
  cd ~/.claude/skills/claude-scaffold-skill && make discover
(or trigger the weekly GitHub Action manually)
```
Then stop.

Otherwise, show the status block to the user:
```
Review queue
────────────
  In discovered.json:  [N]
  Already accepted:    [N]   (in skills.json)
  Already rejected:    [N]
  Still pending:       [N]   → [pages] pages of 25 left

Ready to review the next page? (yes / set page <n> / status / quit)
```

---

## Phase 2 — Show a Page

Run `python scripts/review-queue.py --page <n> --size 25` and present the output as a clean numbered list. For each candidate show:

```
[ 1] ⭐ 17,127  score 100   zarazhangrui/frontend-slides
     Create beautiful slides on the web using Claude's frontend skills
     → github.com/zarazhangrui/frontend-slides   ·   SKILL.md ↗
     flags: (none)

[ 2] ⭐  1,046  score 100   eugeniughelbur/obsidian-second-brain
     Claude Code skill for Obsidian — turn your vault into an AI-first second brain
     → github.com/eugeniughelbur/obsidian-second-brain   ·   SKILL.md ↗
     flags: (none)

...up to 25...
```

If a candidate has flags (`low_stars`, `stale`, `thin_desc`, `non_canonical_topic`, `archived`, `thin_fork`), surface them — they're hints to lean toward reject.

Then ask:

```
For this page (1–25), tell me your decisions. Examples:
  "keep 1 3 7, reject the rest"
  "keep 2, skip the others for now"
  "reject all"
  "open 4"  → I'll fetch and summarize that repo's SKILL.md so you can judge
  "next"    → move on without deciding (they stay in the queue)
```

Support `open <n>` — fetch `https://github.com/<repo>/blob/HEAD/SKILL.md` (raw), summarize what it does, whether it follows confirm-before-generate, scope, and any red flags in the install command. Then re-ask for decisions.

**Default for anything not mentioned:** leave it pending (no decision). Never auto-reject silently.

---

## Phase 3 — Confirm the Batch

Before writing anything, show exactly what will change:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROPOSED CHANGES — page [n]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEEP → registry/skills.json (verified=true):
  + zarazhangrui/frontend-slides
  + dpconde/claude-android-skill

REJECT → registry/rejected.json (scraper skips forever):
  − some/low-effort-repo
  − another/archived-thing
  ...

LEFT PENDING (no change):
  [count] — will show up again next time

NOTHING is written until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Type GO to apply, EDIT to change decisions, or CANCEL.
```

---

## Phase 4 — Apply

On GO, run the persistence tool:

```bash
# Accepts (each one appended to skills.json as verified)
python scripts/review-queue.py --accept owner/repo --accept owner/repo2 ...

# Rejects (each one added to rejected.json)
python scripts/review-queue.py --reject owner/bad1,owner/bad2 ...
```

Then validate:

```bash
python scripts/validate-registry.py
```

If validation fails (e.g. a description over 150 chars, a tag with spaces), fix the offending entry in `skills.json` and re-validate. Common fixes:
- Trim description to ≤ 150 chars
- Lowercase + hyphenate tags, cap at 10
- Ensure `added` is `YYYY-MM-DD`

---

## Phase 5 — Continue or Stop

```
✓ Page [n] done.

  Accepted this page:  [N]
  Rejected this page:  [N]
  Remaining pending:   [N]  ([pages] pages left)

Next?  (next page / set page <n> / status / commit / quit)
```

- **next page** → loop back to Phase 2 with page n+1
- **commit** → stage `registry/skills.json` + `registry/rejected.json`, show the diff, and on GO run:
  ```bash
  git add registry/skills.json registry/rejected.json
  git commit -m "registry: review pass — keep N, reject M"
  git push
  ```
  (If branch protection blocks the push, remind the user the weekly Action uses PAT_TOKEN; for manual pushes they push as themselves.)
- **quit** → remind them their decisions are saved in the files but not yet committed; they can resume `/review-skills` anytime.

---

## Notes

- **Rejected ≠ deleted.** Rejected repos live in `registry/rejected.json`. The scraper skips anything listed there, so they won't clutter `discovered.json` on the next run. Un-reject by removing the slug (or by `--accept`ing it later — that auto-removes it from rejected).
- **Accepted skills get `verified: true`** — that's the human-review stamp. The CI 404-check still runs on the PR.
- **`discovered.json` is regenerated every scrape.** Pending items persist because the scraper re-finds them; accepted/rejected ones drop out because the scraper skips repos in `skills.json` and `rejected.json`.
- This skill is the interactive front-end for `scripts/review-queue.py` — you can also drive that script directly (`--page`, `--accept`, `--reject`, `--status`, `--all`).
