#!/usr/bin/env python3
"""
Fetches current star counts from GitHub and updates registry/skills.json in-place.

Usage:
    python scripts/update-stars.py
    python scripts/update-stars.py --dry-run     # show changes without writing
    python scripts/update-stars.py --token YOUR_TOKEN

Requires: no external dependencies (uses stdlib urllib only)
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "registry" / "skills.json"
GITHUB_API = "https://api.github.com"
PAUSE = 0.4  # seconds between requests


def fetch_stars(repo: str, token: str | None) -> int | None:
    url = f"{GITHUB_API}/repos/{repo}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return data.get("stargazers_count", 0)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  [404] {repo} — not found on GitHub", file=sys.stderr)
        else:
            print(f"  [HTTP {e.code}] {repo}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  [ERROR] {repo} — {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(description="Update star counts in registry/skills.json")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub token")
    parser.add_argument("--registry", default=str(REGISTRY_PATH), help="Path to skills.json")
    args = parser.parse_args()

    if not args.token:
        print("Warning: No GITHUB_TOKEN — unauthenticated requests rate-limited to 60/hr", file=sys.stderr)

    path = Path(args.registry)
    if not path.exists():
        print(f"Registry not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        entries = json.load(f)

    print(f"Updating star counts for {len(entries)} entries...\n")

    changed = 0
    for entry in entries:
        repo = entry["repo"]
        old_stars = entry.get("stars", 0)
        new_stars = fetch_stars(repo, args.token)
        time.sleep(PAUSE)

        if new_stars is None:
            print(f"  SKIP  {repo}")
            continue

        delta = new_stars - old_stars
        arrow = f"+{delta}" if delta > 0 else str(delta)
        flag = f"  ({arrow})" if delta != 0 else ""
        print(f"  {new_stars:>7} ⭐  {repo}{flag}")

        if new_stars != old_stars:
            entry["stars"] = new_stars
            changed += 1

    print(f"\n{changed} entr{'y' if changed == 1 else 'ies'} changed.")

    if args.dry_run:
        print("Dry run — no file written.")
        return

    with open(path, "w") as f:
        json.dump(entries, f, indent=2)
        f.write("\n")

    print(f"Written to {path}")


if __name__ == "__main__":
    main()
