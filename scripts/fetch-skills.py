#!/usr/bin/env python3
"""
GitHub scraper for discovering Claude Code skills.

Usage:
    python scripts/fetch-skills.py
    python scripts/fetch-skills.py --output registry/discovered.json
    python scripts/fetch-skills.py --token YOUR_GITHUB_TOKEN

Requires: requests (pip install requests)
No other external dependencies.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


SEARCH_QUERIES = [
    "topic:claude-skill",
    "topic:claude-code-skill",
    "topic:claude-code filename:SKILL.md",
]

REGISTRY_PATH = Path(__file__).parent.parent / "registry" / "skills.json"
GITHUB_API = "https://api.github.com"
RATE_LIMIT_PAUSE = 2  # seconds between requests to avoid rate limiting


def get_headers(token: str | None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def load_existing_registry(path: Path) -> set[str]:
    """Return set of repo slugs already in the main registry."""
    if not path.exists():
        return set()
    with open(path) as f:
        data = json.load(f)
    return {entry["repo"] for entry in data}


def search_github(query: str, headers: dict) -> list[dict]:
    """Search GitHub repos and return raw results."""
    results = []
    page = 1

    while True:
        url = f"{GITHUB_API}/search/repositories"
        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": 30,
            "page": page,
        }

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
        except requests.exceptions.RequestException as e:
            print(f"  Request error: {e}", file=sys.stderr)
            break

        if resp.status_code == 403:
            print(f"  Rate limited. Waiting 60 seconds...", file=sys.stderr)
            time.sleep(60)
            continue

        if resp.status_code != 200:
            print(f"  API error {resp.status_code}: {resp.text[:200]}", file=sys.stderr)
            break

        data = resp.json()
        items = data.get("items", [])
        if not items:
            break

        results.extend(items)

        # GitHub search API caps at 1000 results; stop at page 10
        if page >= 10 or len(items) < 30:
            break

        page += 1
        time.sleep(RATE_LIMIT_PAUSE)

    return results


def has_skill_md(repo_full_name: str, headers: dict) -> bool:
    """Check if the repo has a SKILL.md in its root."""
    url = f"{GITHUB_API}/repos/{repo_full_name}/contents/SKILL.md"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        return resp.status_code == 200
    except requests.exceptions.RequestException:
        return False


def build_entry(item: dict) -> dict:
    """Build a registry-compatible entry from a GitHub search result."""
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
    }


def deduplicate(discovered: list[dict], existing_repos: set[str]) -> list[dict]:
    """Remove entries already in the main registry and deduplicate within results."""
    seen = set(existing_repos)
    unique = []
    for entry in discovered:
        if entry["repo"] not in seen:
            seen.add(entry["repo"])
            unique.append(entry)
    return unique


def main():
    parser = argparse.ArgumentParser(description="Discover Claude Code skills on GitHub")
    parser.add_argument("--output", default="registry/discovered.json", help="Output JSON file path")
    parser.add_argument("--token", help="GitHub personal access token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--skip-skill-check", action="store_true", help="Skip SKILL.md verification (faster)")
    args = parser.parse_args()

    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print("Warning: No GITHUB_TOKEN set. Unauthenticated requests are rate-limited to 10/min.", file=sys.stderr)

    headers = get_headers(token)
    existing_repos = load_existing_registry(REGISTRY_PATH)
    print(f"Loaded {len(existing_repos)} repos from existing registry.")

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

    print(f"\nTotal unique repos found across all queries: {len(all_raw)}")

    # Build entries and optionally verify SKILL.md exists
    entries = []
    for item in all_raw:
        repo = item["full_name"]
        if repo in existing_repos:
            continue

        if not args.skip_skill_check:
            print(f"  Checking SKILL.md: {repo} ... ", end="", flush=True)
            if not has_skill_md(repo, headers):
                print("not found, skipping")
                continue
            print("found")
            time.sleep(RATE_LIMIT_PAUSE)

        entries.append(build_entry(item))

    new_discoveries = deduplicate(entries, existing_repos)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_searched": len(all_raw),
        "new_discoveries": new_discoveries,
        "skipped_already_in_registry": len([i for i in all_raw if i["full_name"] in existing_repos]),
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone. {len(new_discoveries)} new skill(s) discovered.")
    print(f"Output written to: {out_path}")

    if new_discoveries:
        print("\nNew discoveries:")
        for entry in new_discoveries:
            print(f"  - {entry['repo']} ({entry['stars']} stars)")


if __name__ == "__main__":
    main()
