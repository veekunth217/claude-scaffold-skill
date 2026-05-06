#!/usr/bin/env python3
"""
Search the local registry by keyword.

Usage:
    python scripts/search-registry.py pdf
    python scripts/search-registry.py "code review"
    python scripts/search-registry.py --tag agents
"""

import argparse
import json
import sys
from pathlib import Path

REGISTRY = Path(__file__).parent.parent / "registry" / "skills.json"


def search(query: str, tag_only: bool, registry_path: Path) -> list[dict]:
    with open(registry_path) as f:
        entries = json.load(f)

    q = query.lower().strip()
    results = []

    for entry in entries:
        tags = [t.lower() for t in entry.get("tags", [])]
        if tag_only:
            if q in tags:
                results.append(entry)
            continue

        haystack = " ".join([
            entry.get("name", "").lower(),
            entry.get("repo", "").lower(),
            entry.get("description", "").lower(),
            " ".join(tags),
        ])
        if q in haystack:
            results.append(entry)

    return results


def main():
    parser = argparse.ArgumentParser(description="Search the local skills registry")
    parser.add_argument("query", help="Keyword to search for")
    parser.add_argument("--tag", action="store_true", help="Match only against tags")
    parser.add_argument("--registry", default=str(REGISTRY))
    args = parser.parse_args()

    results = search(args.query, args.tag, Path(args.registry))

    if not results:
        print(f"No matches for '{args.query}'.")
        print(f"Tip: try `python scripts/search-registry.py --tag <tag>` to browse by tag.")
        sys.exit(1)

    print(f"\n{len(results)} match(es) for '{args.query}':\n")
    for r in sorted(results, key=lambda e: -e.get("stars", 0)):
        verified = "✓" if r.get("verified") else " "
        market = " [marketplace]" if r.get("marketplace") else ""
        stars = r.get("stars", 0)
        print(f"  [{verified}] {r['name']}{market}  ⭐ {stars}")
        print(f"      {r['repo']}")
        print(f"      {r['description']}")
        print(f"      install: {r['install']}")
        print()


if __name__ == "__main__":
    main()
