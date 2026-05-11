#!/usr/bin/env python3
"""
Triage the discovered-skills queue, one page at a time.

The scraper writes every candidate to registry/discovered.json, sorted by
quality score. This tool lets you page through them and record decisions:

  - ACCEPT → appended to registry/skills.json with verified=true
  - REJECT → repo slug added to registry/rejected.json (scraper skips it forever)
  - (no decision) → stays in the queue, shows up again next time

Usage:
    # Show the next page of un-decided candidates (default 25 per page)
    python scripts/review-queue.py
    python scripts/review-queue.py --page 2 --size 25
    python scripts/review-queue.py --all            # print the whole queue

    # Record decisions (repeatable, comma-separated, or multiple flags)
    python scripts/review-queue.py --accept owner/repo --accept other/repo
    python scripts/review-queue.py --reject a/b,c/d

    # Stats
    python scripts/review-queue.py --status

No external dependencies — stdlib only.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).parent.parent
DISCOVERED = ROOT / "registry" / "discovered.json"
SKILLS = ROOT / "registry" / "skills.json"
REJECTED = ROOT / "registry" / "rejected.json"

# ── Sections ───────────────────────────────────────────────────────
# Candidates are grouped so you can triage by flavour, not one flat list.
SECTIONS = [
    ("just-launched", "🆕 Just launched", "pushed in the last 45 days"),
    ("popular",       "🔥 Popular",       "≥ 50 stars (battle-tested, any age)"),
    ("quiet-gem",     "💎 Quiet gems",    "< 50 stars but quality score ≥ 70 and not stale"),
    ("long-tail",     "📦 Long tail",     "everything else — lower signal, skim or skip"),
]
SECTION_ORDER = {key: i for i, (key, _, _) in enumerate(SECTIONS)}
SECTION_LABEL = {key: label for key, label, _ in SECTIONS}
SECTION_DESC = {key: desc for key, _, desc in SECTIONS}


def days_since_push(entry: dict) -> int | None:
    ts = entry.get("pushed_at", "")
    if not ts:
        return None
    try:
        pushed = datetime.strptime(ts[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - pushed).days
    except ValueError:
        return None


def classify_section(entry: dict) -> str:
    stars = entry.get("stars", 0)
    score = entry.get("quality_score", 0)
    age = days_since_push(entry)
    flags = set(entry.get("quality_flags", []))

    if age is not None and age <= 45:
        return "just-launched"
    if stars >= 50:
        return "popular"
    if score >= 70 and "stale" not in flags:
        return "quiet-gem"
    return "long-tail"


def sort_key(entry: dict) -> tuple:
    """Section priority first, then quality score desc, then stars desc."""
    sec = classify_section(entry)
    return (SECTION_ORDER.get(sec, 99), -entry.get("quality_score", 0), -entry.get("stars", 0))


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def save_json(path: Path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def load_queue() -> list[dict]:
    data = load_json(DISCOVERED, {})
    return data.get("new_discoveries", [])


def accepted_repos() -> set[str]:
    return {e["repo"] for e in load_json(SKILLS, [])}


def rejected_repos() -> set[str]:
    return set(load_json(REJECTED, {}).get("rejected", []))


def pending_queue(section: str | None = None) -> list[dict]:
    """Pending entries (not accepted, not rejected), grouped+sorted by section.

    If `section` is given, only that section's entries are returned.
    """
    acc, rej = accepted_repos(), rejected_repos()
    q = [e for e in load_queue() if e["repo"] not in acc and e["repo"] not in rej]
    if section:
        q = [e for e in q if classify_section(e) == section]
    q.sort(key=sort_key)
    return q


def section_counts(items: list[dict]) -> dict[str, int]:
    counts = {key: 0 for key, _, _ in SECTIONS}
    for e in items:
        counts[classify_section(e)] += 1
    return counts


def cmd_status():
    queue = load_queue()
    acc, rej = accepted_repos(), rejected_repos()
    pend = pending_queue()
    counts = section_counts(pend)
    print("Review queue status")
    print("───────────────────")
    print(f"  In discovered.json:  {len(queue)}")
    print(f"  Accepted (in skills.json): {len(acc)}")
    print(f"  Rejected:            {len(rej)}")
    print(f"  Still pending:       {len(pend)}")
    if pend:
        print()
        print("  Pending by section:")
        for key, label, desc in SECTIONS:
            n = counts[key]
            if n:
                pages = (n + 24) // 25
                print(f"    {label:<18} {n:>4}   ({desc})  → {pages} pg")
        print()
        print("  Review a section:  python scripts/review-queue.py --section just-launched")
        print("  Or the whole pile: python scripts/review-queue.py")


def render_page(items: list[dict], page: int, size: int, section: str | None = None):
    total = len(items)
    if total == 0:
        if section:
            print(f"Nothing pending in section '{section}'. 🎉  Try another, or run --status.")
        else:
            print("Nothing pending — the queue is fully triaged. 🎉")
        return
    pages = (total + size - 1) // size
    page = max(1, min(page, pages))
    start = (page - 1) * size
    chunk = items[start : start + size]

    where = f"section {SECTION_LABEL.get(section, section)} — " if section else ""
    print(f"\nReview queue — {where}page {page}/{pages}  (showing {len(chunk)} of {total} pending)\n")

    current_section = None
    for i, e in enumerate(chunk, start=start + 1):
        sec = classify_section(e)
        if sec != current_section:
            current_section = sec
            print(f"  ── {SECTION_LABEL[sec]}  ({SECTION_DESC[sec]}) ──\n")
        repo = e.get("repo", "?")
        score = e.get("quality_score", "?")
        stars = e.get("stars", 0)
        age = days_since_push(e)
        age_str = f"  {age}d ago" if age is not None else ""
        desc = (e.get("description") or "").strip()
        flags = [f for f in e.get("quality_flags", []) if f not in ("has_skill_md", "has_readme", "canonical_topic")]
        flag_str = f"  ⚠ {', '.join(flags)}" if flags else ""
        print(f"  [{i:>3}] score {score:>3}  ⭐ {stars:<6}{age_str}  {repo}{flag_str}")
        if desc:
            print(f"        {desc}")
        print(f"        https://github.com/{repo}  ·  SKILL.md: https://github.com/{repo}/blob/HEAD/SKILL.md")
        print()

    print("─" * 60)
    print("Record decisions for this page:")
    accepts = " ".join(f"--accept {e['repo']}" for e in chunk[:3])
    print(f"  python scripts/review-queue.py {accepts} ...")
    print(f"  python scripts/review-queue.py --reject {','.join(e['repo'] for e in chunk[:3])} ...")
    sec_flag = f" --section {section}" if section else ""
    if page < pages:
        print(f"Next page:  python scripts/review-queue.py{sec_flag} --page {page + 1}")
    else:
        print("(last page of this view)")


def do_accept(repos: list[str]):
    skills = load_json(SKILLS, [])
    existing = {e["repo"] for e in skills}
    queue = {e["repo"]: e for e in load_queue()}
    rej = load_json(REJECTED, {"rejected": []})
    added = []
    for repo in repos:
        if repo in existing:
            print(f"  ⊝ {repo} already in skills.json — skipping")
            continue
        src = queue.get(repo)
        if not src:
            print(f"  ✗ {repo} not found in discovered.json — add it manually if you want it")
            continue
        entry = {
            "name": src.get("name", repo.split("/")[-1]),
            "repo": repo,
            "description": (src.get("description") or "")[:120] or "No description provided",
            "tags": (src.get("tags") or [])[:10],
            "install": src.get("install") or f"git clone https://github.com/{repo}.git ~/.claude/skills/{repo.split('/')[-1]}",
            "stars": src.get("stars", 0),
            "verified": True,
            "added": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        }
        skills.append(entry)
        existing.add(repo)
        added.append(repo)
        # If it was previously rejected, un-reject it
        if repo in rej.get("rejected", []):
            rej["rejected"].remove(repo)
        print(f"  ✓ accepted {repo} → skills.json (verified)")
    if added:
        save_json(SKILLS, skills)
        rej["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        save_json(REJECTED, rej)
        print(f"\n{len(added)} skill(s) added. Run `python scripts/validate-registry.py` then commit.")
    else:
        print("Nothing added.")


def do_reject(repos: list[str]):
    rej = load_json(REJECTED, {"rejected": []})
    rejected = set(rej.get("rejected", []))
    skills_repos = accepted_repos()
    changed = []
    for repo in repos:
        if repo in skills_repos:
            print(f"  ⚠ {repo} is in skills.json (accepted) — remove it there first if you really want to reject it")
            continue
        if repo in rejected:
            print(f"  ⊝ {repo} already rejected")
            continue
        rejected.add(repo)
        changed.append(repo)
        print(f"  ✗ rejected {repo} — scraper will skip it from now on")
    if changed:
        rej["rejected"] = sorted(rejected)
        rej["updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        # preserve any _comment key
        save_json(REJECTED, rej)
        print(f"\n{len(changed)} repo(s) added to rejected.json. Commit to persist.")
    else:
        print("Nothing changed.")


def split_csv(values: list[str]) -> list[str]:
    out = []
    for v in values or []:
        out.extend(part.strip() for part in v.split(",") if part.strip())
    return out


def main():
    p = argparse.ArgumentParser(description="Triage the discovered-skills queue")
    p.add_argument("--page", type=int, default=1, help="page number (default 1)")
    p.add_argument("--size", type=int, default=25, help="page size (default 25)")
    p.add_argument("--section", choices=[k for k, _, _ in SECTIONS], help="only review this section")
    p.add_argument("--all", action="store_true", help="print the entire pending queue (all sections)")
    p.add_argument("--status", action="store_true", help="show counts per section and exit")
    p.add_argument("--accept", action="append", default=[], help="repo slug(s) to accept into skills.json (repeatable / comma-sep)")
    p.add_argument("--reject", action="append", default=[], help="repo slug(s) to reject (repeatable / comma-sep)")
    args = p.parse_args()

    if not DISCOVERED.exists():
        print(f"No {DISCOVERED} yet — run the scraper first: make discover", file=sys.stderr)
        sys.exit(1)

    accepts = split_csv(args.accept)
    rejects = split_csv(args.reject)

    if accepts:
        do_accept(accepts)
    if rejects:
        do_reject(rejects)
    if accepts or rejects:
        print()
        cmd_status()
        return

    if args.status:
        cmd_status()
        return

    pending = pending_queue(section=args.section)
    if args.all:
        render_page(pending, 1, max(len(pending), 1), section=args.section)
    else:
        render_page(pending, args.page, args.size, section=args.section)


if __name__ == "__main__":
    main()
