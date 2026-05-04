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
    "topic:claude-skill",
    "topic:claude-code-skill",
    "topic:claude-code filename:SKILL.md",
]

REGISTRY_PATH = Path(__file__).parent.parent / "registry" / "skills.json"
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


def build_entry(item: dict) -> dict:
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

    print(f"\nTotal unique repos found: {len(all_raw)}")

    entries = []
    seen_repos = set(existing_repos)

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
            print("found")
            time.sleep(RATE_LIMIT_PAUSE)

        entries.append(build_entry(item))

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_searched": len(all_raw),
        "new_discoveries": entries,
        "skipped_already_in_registry": len([i for i in all_raw if i["full_name"] in existing_repos]),
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nDone. {len(entries)} new skill(s) discovered.")
    print(f"Output: {out_path}")
    if entries:
        for e in entries:
            print(f"  - {e['repo']} ({e['stars']} ⭐)")


if __name__ == "__main__":
    main()
