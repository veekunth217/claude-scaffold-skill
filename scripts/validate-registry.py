#!/usr/bin/env python3
"""
Validates registry/skills.json for structure correctness.

Usage:
    python scripts/validate-registry.py
    python scripts/validate-registry.py --registry path/to/skills.json
    python scripts/validate-registry.py --check-github   # also verify repos exist on GitHub

Exit codes:
    0 = valid
    1 = validation errors found
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

REQUIRED_FIELDS = {
    "name": str,
    "repo": str,
    "description": str,
    "tags": list,
    "install": str,
    "stars": int,
    "verified": bool,
    "added": str,
}

MAX_DESCRIPTION_LENGTH = 150
MAX_TAGS = 10


def github_repo_exists(repo: str, token: str | None) -> bool:
    try:
        import urllib.request
        url = f"https://api.github.com/repos/{repo}"
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github+json")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


def validate_entry(entry: dict, index: int) -> list[str]:
    errors = []
    prefix = f"Entry #{index} ({entry.get('repo', 'unknown')})"

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in entry:
            errors.append(f"{prefix}: missing required field '{field}'")
            continue
        if not isinstance(entry[field], expected_type):
            errors.append(
                f"{prefix}: '{field}' must be {expected_type.__name__}, "
                f"got {type(entry[field]).__name__}"
            )

    if errors:
        return errors

    repo = entry["repo"]
    if "/" not in repo or repo.count("/") != 1:
        errors.append(f"{prefix}: 'repo' must be 'user/repo' format, got '{repo}'")

    if len(entry["description"]) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"{prefix}: description too long ({len(entry['description'])} chars, max {MAX_DESCRIPTION_LENGTH})"
        )

    if len(entry["description"].strip()) == 0:
        errors.append(f"{prefix}: description cannot be empty")

    for i, tag in enumerate(entry["tags"]):
        if not isinstance(tag, str):
            errors.append(f"{prefix}: tags[{i}] must be a string")
        elif tag != tag.lower():
            errors.append(f"{prefix}: tags[{i}] '{tag}' must be lowercase")
        elif " " in tag:
            errors.append(f"{prefix}: tags[{i}] '{tag}' must not contain spaces — use hyphens")

    if len(entry["tags"]) > MAX_TAGS:
        errors.append(f"{prefix}: too many tags ({len(entry['tags'])}, max {MAX_TAGS})")

    if entry["stars"] < 0:
        errors.append(f"{prefix}: 'stars' must be >= 0")

    try:
        datetime.strptime(entry["added"], "%Y-%m-%d")
    except ValueError:
        errors.append(f"{prefix}: 'added' must be YYYY-MM-DD format, got '{entry['added']}'")

    repo_name = repo.split("/")[-1]
    if repo_name not in entry["install"] and repo not in entry["install"]:
        errors.append(
            f"{prefix}: 'install' command doesn't reference the repo name '{repo_name}'"
        )

    return errors


def validate_registry(path: Path, check_github: bool = False, token: str | None = None) -> tuple[bool, list[str]]:
    if not path.exists():
        return False, [f"Registry file not found: {path}"]

    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]

    if not isinstance(data, list):
        return False, ["Registry must be a JSON array at the top level"]

    if len(data) == 0:
        return False, ["Registry is empty — at least one entry required"]

    all_errors = []
    repos_seen = set()

    for i, entry in enumerate(data):
        errors = validate_entry(entry, i + 1)
        all_errors.extend(errors)

        repo = entry.get("repo", "")
        if repo in repos_seen:
            all_errors.append(f"Entry #{i+1}: duplicate repo '{repo}'")
        repos_seen.add(repo)

    if check_github and not all_errors:
        print(f"  Checking {len(data)} repos exist on GitHub...")
        for i, entry in enumerate(data):
            repo = entry["repo"]
            exists = github_repo_exists(repo, token)
            status = "✓" if exists else "✗ 404"
            print(f"    [{status}] {repo}")
            if not exists:
                all_errors.append(f"Entry #{i+1} ({repo}): repo does not exist on GitHub (404)")
            time.sleep(0.5)

    return len(all_errors) == 0, all_errors


def main():
    parser = argparse.ArgumentParser(description="Validate registry/skills.json")
    parser.add_argument(
        "--registry",
        default=str(Path(__file__).parent.parent / "registry" / "skills.json"),
        help="Path to skills.json",
    )
    parser.add_argument(
        "--check-github",
        action="store_true",
        help="Also verify every repo exists on GitHub (makes HTTP requests)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub token for API requests (or set GITHUB_TOKEN env var)",
    )
    args = parser.parse_args()

    path = Path(args.registry)
    print(f"Validating: {path}")
    if args.check_github:
        print("  GitHub existence checks enabled")

    valid, errors = validate_registry(path, check_github=args.check_github, token=args.token)

    if valid:
        with open(path) as f:
            data = json.load(f)
        verified = sum(1 for e in data if e.get("verified"))
        print(f"  Valid! {len(data)} entries, {verified} verified.")
        sys.exit(0)
    else:
        print(f"  INVALID — {len(errors)} error(s) found:\n")
        for err in errors:
            print(f"  [ERROR] {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
