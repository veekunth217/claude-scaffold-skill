#!/usr/bin/env python3
"""
Validates registry/skills.json for structure correctness.

Usage:
    python scripts/validate-registry.py
    python scripts/validate-registry.py --registry path/to/skills.json

Exit codes:
    0 = valid
    1 = validation errors found
"""

import argparse
import json
import sys
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


def validate_entry(entry: dict, index: int) -> list[str]:
    errors = []
    prefix = f"Entry #{index} ({entry.get('repo', 'unknown')})"

    # Check required fields
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
        return errors  # skip further checks if basics are broken

    # repo format: "user/repo"
    repo = entry["repo"]
    if "/" not in repo or repo.count("/") != 1:
        errors.append(f"{prefix}: 'repo' must be 'user/repo' format, got '{repo}'")

    # description length
    if len(entry["description"]) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            f"{prefix}: description too long ({len(entry['description'])} chars, max {MAX_DESCRIPTION_LENGTH})"
        )

    if len(entry["description"].strip()) == 0:
        errors.append(f"{prefix}: description cannot be empty")

    # tags: list of strings, not too many
    for i, tag in enumerate(entry["tags"]):
        if not isinstance(tag, str):
            errors.append(f"{prefix}: tags[{i}] must be a string")
    if len(entry["tags"]) > MAX_TAGS:
        errors.append(f"{prefix}: too many tags ({len(entry['tags'])}, max {MAX_TAGS})")

    # stars: non-negative
    if entry["stars"] < 0:
        errors.append(f"{prefix}: 'stars' must be >= 0")

    # added: must be a valid YYYY-MM-DD date
    try:
        datetime.strptime(entry["added"], "%Y-%m-%d")
    except ValueError:
        errors.append(f"{prefix}: 'added' must be YYYY-MM-DD format, got '{entry['added']}'")

    # install: must reference the repo
    repo_name = repo.split("/")[-1]
    if repo_name not in entry["install"] and repo not in entry["install"]:
        errors.append(
            f"{prefix}: 'install' command doesn't reference the repo name '{repo_name}'"
        )

    return errors


def validate_registry(path: Path) -> tuple[bool, list[str]]:
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

        # Duplicate check
        repo = entry.get("repo", "")
        if repo in repos_seen:
            all_errors.append(f"Entry #{i+1}: duplicate repo '{repo}'")
        repos_seen.add(repo)

    return len(all_errors) == 0, all_errors


def main():
    parser = argparse.ArgumentParser(description="Validate registry/skills.json")
    parser.add_argument(
        "--registry",
        default=str(Path(__file__).parent.parent / "registry" / "skills.json"),
        help="Path to skills.json",
    )
    args = parser.parse_args()

    path = Path(args.registry)
    print(f"Validating: {path}")

    valid, errors = validate_registry(path)

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
