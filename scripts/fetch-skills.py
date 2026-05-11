#!/usr/bin/env python3
"""
GitHub scraper for discovering Claude Code skills.

Usage:
    python scripts/fetch-skills.py
    python scripts/fetch-skills.py --output registry/discovered.json
    python scripts/fetch-skills.py --token YOUR_GITHUB_TOKEN
    python scripts/fetch-skills.py --skip-skill-check   # faster, no SKILL.md verification

No external dependencies — uses stdlib only.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SEARCH_QUERIES = [
    # Exact topic matches — singular and plural variants
    "topic:claude-skill",
    "topic:claude-code-skill",
    "topic:claude-skills",
    "topic:claude-code-skills",
    # Related activity topics people use without the right canonical tag
    "topic:claude-hooks filename:SKILL.md",
    "topic:claude-agents filename:SKILL.md",
    "topic:claude-code-agent filename:SKILL.md",
    # Broad SKILL.md scan scoped to Claude repos
    "topic:claude-code filename:SKILL.md",
    "topic:anthropic filename:SKILL.md",
    # Description-based fallback — catches repos that tag poorly but name correctly
    '"claude code" "skill" filename:SKILL.md',
]

REGISTRY_PATH = Path(__file__).parent.parent / "registry" / "skills.json"
REJECTED_PATH = Path(__file__).parent.parent / "registry" / "rejected.json"
GITHUB_API = "https://api.github.com"
RATE_LIMIT_PAUSE = 2


def get_headers(token: str | None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def api_get(path: str, headers: dict, params: dict | None = None) -> dict | None:
    url = path if path.startswith("http") else f"{GITHUB_API}{path}"
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("  Rate limited — waiting 60s...", file=sys.stderr)
            time.sleep(60)
            return api_get(path, headers, params)
        print(f"  HTTP {e.code}: {url}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  Request error: {e}", file=sys.stderr)
        return None


def load_existing_registry(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with open(path) as f:
        data = json.load(f)
    return {entry["repo"] for entry in data}


def load_rejected(path: Path) -> set[str]:
    """Repos a maintainer explicitly rejected during review — never re-list them."""
    if not path.exists():
        return set()
    try:
        with open(path) as f:
            data = json.load(f)
        return set(data.get("rejected", []))
    except (json.JSONDecodeError, KeyError):
        return set()


def search_github(query: str, headers: dict) -> list[dict]:
    results = []
    page = 1
    while page <= 10:
        data = api_get(
            "/search/repositories",
            headers,
            {"q": query, "sort": "stars", "order": "desc", "per_page": 30, "page": page},
        )
        if not data:
            break
        items = data.get("items", [])
        if not items:
            break
        results.extend(items)
        if len(items) < 30:
            break
        page += 1
        time.sleep(RATE_LIMIT_PAUSE)
    return results


def has_skill_md(repo_full_name: str, headers: dict) -> bool:
    data = api_get(f"/repos/{repo_full_name}/contents/SKILL.md", headers)
    return data is not None


# ── Quality scoring criteria ────────────────────────────────────────
# We do NOT auto-add discovered skills to skills.json. They land in
# discovered.json with a quality_score so the maintainer review pass
# (weekly Issue) can prioritize the strong candidates.
#
# Scoring is intentionally lenient — borderline skills still appear in
# the queue, just lower-ranked. Maintainers make the final call.

QUALITY_FLAG_THRESHOLDS = {
    "low_stars": 3,           # < this = `low_stars` flag (still listed)
    "stale_days": 365,        # last commit older than this = `stale` flag
    "min_desc_chars": 30,     # description shorter than this = `thin_desc`
}


def quality_score(item: dict, headers: dict) -> tuple[int, list[str]]:
    """Return (score, flags) for a discovered repo.

    Scoring weights (max ~100):
      +30  has SKILL.md in root
      +20  has at least one canonical topic (claude-skill / claude-code-skill / etc.)
      +20  description is >= 30 chars and non-empty
      +15  stars >= 10
      +10  pushed within last 365 days
      + 5  README.md exists in root
    """
    score = 0
    flags = []
    repo = item["full_name"]

    # SKILL.md presence (already checked but recorded for transparency)
    score += 30
    flags.append("has_skill_md")

    # Canonical topics
    topics = set(item.get("topics", []))
    canonical = {
        "claude-skill", "claude-code-skill",
        "claude-skills", "claude-code-skills",
    }
    if topics & canonical:
        score += 20
        flags.append("canonical_topic")
    else:
        flags.append("non_canonical_topic")

    # Description quality
    desc = (item.get("description") or "").strip()
    if len(desc) >= QUALITY_FLAG_THRESHOLDS["min_desc_chars"]:
        score += 20
    else:
        flags.append("thin_desc")

    # Stars
    stars = item.get("stargazers_count", 0)
    if stars >= 10:
        score += 15
    elif stars < QUALITY_FLAG_THRESHOLDS["low_stars"]:
        flags.append("low_stars")

    # Recency — `pushed_at` from search API
    pushed_at = item.get("pushed_at", "")
    if pushed_at:
        try:
            pushed = datetime.strptime(pushed_at[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            days_old = (datetime.now(timezone.utc) - pushed).days
            if days_old <= QUALITY_FLAG_THRESHOLDS["stale_days"]:
                score += 10
            else:
                flags.append("stale")
        except ValueError:
            pass

    # README.md presence (cheap check)
    if api_get(f"/repos/{repo}/contents/README.md", headers) is not None:
        score += 5
        flags.append("has_readme")

    # Archived = strong negative signal
    if item.get("archived"):
        score -= 30
        flags.append("archived")

    # Fork-of-fork-of with no own activity
    if item.get("fork") and item.get("size", 0) < 50:
        flags.append("thin_fork")

    return score, flags


def build_entry(item: dict, score: int, flags: list[str]) -> dict:
    repo = item["full_name"]
    return {
        "name": item.get("name", repo.split("/")[-1]),
        "repo": repo,
        "description": (item.get("description") or "No description provided")[:120],
        "tags": item.get("topics", []),
        "install": f"git clone https://github.com/{repo}.git ~/.claude/skills/{repo.split('/')[-1]}",
        "stars": item.get("stargazers_count", 0),
        "verified": False,
        "added": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        # Quality metadata for the maintainer review queue
        "quality_score": score,
        "quality_flags": flags,
        "pushed_at": item.get("pushed_at", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Discover Claude Code skills on GitHub")
    parser.add_argument("--output", default="registry/discovered.json")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--skip-skill-check", action="store_true")
    args = parser.parse_args()

    if not args.token:
        print("Warning: No GITHUB_TOKEN — unauthenticated requests rate-limited to 10/min.", file=sys.stderr)

    headers = get_headers(args.token)
    existing_repos = load_existing_registry(REGISTRY_PATH)
    rejected_repos_set = load_rejected(REJECTED_PATH)
    # Anything verified OR explicitly rejected is "decided" — skip it.
    decided_repos = existing_repos | rejected_repos_set
    print(f"Loaded {len(existing_repos)} verified + {len(rejected_repos_set)} rejected = "
          f"{len(decided_repos)} decided repos to skip.")

    # Load the *previous* discovered.json so we can tell what's genuinely new
    # this run vs. what was already in the review queue last time.
    out_path_pre = Path(args.output)
    previously_discovered: set[str] = set()
    if out_path_pre.exists():
        try:
            with open(out_path_pre) as f:
                prev = json.load(f)
            previously_discovered = {e["repo"] for e in prev.get("new_discoveries", [])}
            print(f"Loaded {len(previously_discovered)} repos from previous discovered.json.")
        except (json.JSONDecodeError, KeyError):
            print("Previous discovered.json unreadable — treating all finds as new.")

    all_raw: list[dict] = []
    seen_ids: set[int] = set()

    for query in SEARCH_QUERIES:
        print(f"\nSearching: {query}")
        results = search_github(query, headers)
        print(f"  Found {len(results)} results")
        for item in results:
            if item["id"] not in seen_ids:
                seen_ids.add(item["id"])
                all_raw.append(item)
        time.sleep(RATE_LIMIT_PAUSE)

    print(f"\nTotal unique repos found: {len(all_raw)}")

    entries = []
    seen_repos = set(decided_repos)  # skip verified + rejected

    for item in all_raw:
        repo = item["full_name"]
        if repo in seen_repos:
            continue
        seen_repos.add(repo)

        if not args.skip_skill_check:
            print(f"  Checking SKILL.md: {repo} ... ", end="", flush=True)
            if not has_skill_md(repo, headers):
                print("not found, skipping")
                continue
            print("found", end="")
            time.sleep(RATE_LIMIT_PAUSE)

        score, flags = quality_score(item, headers)
        if not args.skip_skill_check:
            print(f"  (score={score}, flags={','.join(flags) or 'none'})")
            time.sleep(RATE_LIMIT_PAUSE)

        entries.append(build_entry(item, score, flags))

    # Sort highest-quality candidates first so maintainer review queue
    # is pre-prioritized. Borderline candidates still appear, just lower.
    entries.sort(key=lambda e: -e.get("quality_score", 0))

    # Split into "new this run" (never seen in a prior discovered.json or the
    # verified registry) vs "already in the queue from before".
    new_this_run = [e for e in entries if e["repo"] not in previously_discovered]
    carried_over = [e for e in entries if e["repo"] in previously_discovered]

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_searched": len(all_raw),
        "queue_size": len(entries),
        "new_this_run": len(new_this_run),
        "carried_over": len(carried_over),
        "scoring_criteria": {
            "max_score": 100,
            "weights": {
                "has_skill_md": 30,
                "canonical_topic": 20,
                "good_description": 20,
                "stars_gte_10": 15,
                "recently_pushed": 10,
                "has_readme": 5,
                "archived_penalty": -30,
            },
            "flags_explained": {
                "canonical_topic": "uses claude-skill/claude-code-skill/claude-skills/claude-code-skills topic",
                "non_canonical_topic": "no canonical topic — found via fallback queries",
                "thin_desc": "description < 30 chars",
                "low_stars": "fewer than 3 stars",
                "stale": "no push in over 365 days",
                "archived": "repo is archived (strong negative signal)",
                "thin_fork": "is a fork with little code",
            },
        },
        # Full queue (everything found this run, minus what's already verified),
        # sorted by quality score. This is the browsable review list.
        "new_discoveries": entries,
        # Just the repos that first appeared this run — what the weekly Issue reports.
        "newly_added_this_run": new_this_run,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone. Queue: {len(entries)} candidate(s) "
          f"({len(new_this_run)} new this run, {len(carried_over)} carried over).")
    print(f"Output: {out_path}")
    if new_this_run:
        print("New this run:")
        for e in new_this_run[:20]:
            print(f"  - {e['repo']} ({e['stars']} ⭐, score {e.get('quality_score')})")
        if len(new_this_run) > 20:
            print(f"  ... and {len(new_this_run) - 20} more")


if __name__ == "__main__":
    main()
