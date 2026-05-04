#!/usr/bin/env python3
"""
Scrapes Anthropic Claude Code docs and changelog for new built-in capabilities
not yet tracked in registry/claude-capabilities.json.

Outputs: registry/discovered-capabilities.json

Usage:
    python scripts/fetch-capabilities.py
    python scripts/fetch-capabilities.py --output registry/discovered-capabilities.json
    python scripts/fetch-capabilities.py --dry-run
"""

import json
import sys
import os
import argparse
import re
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urljoin

# NOTE: Anthropic's docs site is JavaScript-rendered — urllib fetches the shell HTML,
# not the rendered content. This scraper will produce results if/when the docs expose
# a server-rendered or static-export version. The curated claude-capabilities.json
# remains the primary source of truth; this script catches genuinely new features.
DOCS_PAGES = [
    "https://docs.anthropic.com/en/claude-code/overview",
    "https://docs.anthropic.com/en/claude-code/settings",
    "https://docs.anthropic.com/en/claude-code/hooks",
    "https://docs.anthropic.com/en/claude-code/mcp",
    "https://docs.anthropic.com/en/claude-code/slash-commands",
    "https://docs.anthropic.com/en/claude-code/ide-integrations",
    "https://docs.anthropic.com/en/claude-code/github-actions",
    # GitHub releases page is server-rendered and more scrapeable
    "https://github.com/anthropics/claude-code/releases",
]

CHANGELOG_URL = "https://github.com/anthropics/claude-code/releases"  # server-rendered, scrapeable

CAPABILITY_SIGNALS = [
    # (pattern, candidate_name, candidate_category, candidate_tags)
    (r"/ultrareview", "Ultra Review", "code-review", ["code-review", "pr", "multi-agent"]),
    (r"\bhooks?\b", "Hooks", "automation", ["automation", "workflow", "linting"]),
    (r"\bMCP\b|model context protocol", "MCP Servers", "integration", ["mcp", "integration", "database"]),
    (r"CLAUDE\.md", "Project Memory (CLAUDE.md)", "context", ["memory", "context", "workflow"]),
    (r"extended thinking", "Extended Thinking", "reasoning", ["reasoning", "architecture", "debugging"]),
    (r"sub.?agent|parallel agent|task tool", "Parallel Sub-agents", "performance", ["multi-agent", "parallel", "performance"]),
    (r"/fast\b|fast mode", "Fast Mode", "performance", ["performance", "speed"]),
    (r"VS Code|JetBrains|IDE extension", "IDE Extension", "ide", ["vscode", "jetbrains", "ide"]),
    (r"permission mode|skip.permissions|dangerously", "Permission Modes", "safety", ["security", "permissions", "safety"]),
    (r"web search|search the web", "Web Search", "research", ["research", "docs", "debugging"]),
    (r"image|screenshot|multimodal|paste.*image", "Image Input", "multimodal", ["frontend", "ui", "design"]),
    (r"codebase index|semantic index", "Codebase Indexing", "navigation", ["large-codebase", "navigation"]),
    (r"claude\.ai/code|web app", "Claude Code Web App", "access", ["browser", "remote", "no-install"]),
    (r"slash command|custom skill", "Custom Skills", "extensibility", ["workflow", "team", "customization"]),
]

HEADERS = {
    "User-Agent": "claude-scaffold-skill/1.0 (capability-discovery-bot; github.com/veekunth217/claude-scaffold-skill)"
}


def fetch_page(url: str) -> str | None:
    try:
        req = Request(url, headers=HEADERS)
        with urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (URLError, HTTPError) as e:
        print(f"  WARN: could not fetch {url}: {e}", file=sys.stderr)
        return None


def strip_html(html: str) -> str:
    # Remove script/style blocks
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    # Remove HTML tags
    html = re.sub(r"<[^>]+>", " ", html)
    # Collapse whitespace
    html = re.sub(r"\s+", " ", html)
    return html


def extract_headings(html: str) -> list[str]:
    """Extract h1-h4 text from HTML."""
    headings = re.findall(r"<h[1-4][^>]*>(.*?)</h[1-4]>", html, flags=re.DOTALL | re.IGNORECASE)
    return [re.sub(r"<[^>]+>", "", h).strip() for h in headings]


def detect_capabilities(text: str) -> list[dict]:
    """Match text against capability signal patterns."""
    found = []
    text_lower = text.lower()
    for pattern, name, category, tags in CAPABILITY_SIGNALS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append({
                "name": name,
                "category": category,
                "tags": tags,
                "matched_pattern": pattern,
            })
    return found


def load_known_capabilities(path: str) -> set[str]:
    """Return set of known capability names (lowercased) from the curated file."""
    if not os.path.isfile(path):
        return set()
    try:
        with open(path) as f:
            data = json.load(f)
        return {c["name"].lower() for c in data.get("capabilities", [])}
    except Exception as e:
        print(f"  WARN: could not load {path}: {e}", file=sys.stderr)
        return set()


def scrape_changelog(url: str) -> list[dict]:
    """
    Scrape the changelog page and return a list of recent entries as dicts
    with keys: date, title, summary.
    """
    html = fetch_page(url)
    if not html:
        return []

    text = strip_html(html)
    headings = extract_headings(html)

    # Look for date-like headings (changelog entries are typically dated)
    date_pattern = re.compile(r"\b(20\d\d[-/]\d{2}[-/]\d{2}|January|February|March|April|May|June|July|August|September|October|November|December)\b")
    entries = []
    for h in headings:
        if date_pattern.search(h) or re.search(r"\bv\d+\.\d+", h):
            entries.append({"heading": h})

    return entries[:10]  # Last 10 changelog entries


def main():
    parser = argparse.ArgumentParser(description="Discover new Claude Code capabilities from Anthropic docs")
    parser.add_argument("--output", default="registry/discovered-capabilities.json")
    parser.add_argument("--capabilities", default="registry/claude-capabilities.json")
    parser.add_argument("--dry-run", action="store_true", help="Print results but don't write file")
    args = parser.parse_args()

    known = load_known_capabilities(args.capabilities)
    print(f"Loaded {len(known)} known capabilities from {args.capabilities}")

    all_detected: dict[str, dict] = {}

    # Scrape docs pages
    for url in DOCS_PAGES:
        print(f"Fetching {url}...")
        html = fetch_page(url)
        if not html:
            continue
        text = strip_html(html)
        detected = detect_capabilities(text)
        for cap in detected:
            name_key = cap["name"].lower()
            if name_key not in all_detected:
                all_detected[name_key] = {**cap, "sources": [url]}
            else:
                all_detected[name_key]["sources"].append(url)

    # Scrape changelog
    print(f"Fetching changelog: {CHANGELOG_URL}...")
    changelog_entries = scrape_changelog(CHANGELOG_URL)

    # Also detect capabilities from changelog
    html = fetch_page(CHANGELOG_URL)
    if html:
        text = strip_html(html)
        for cap in detect_capabilities(text):
            name_key = cap["name"].lower()
            if name_key not in all_detected:
                all_detected[name_key] = {**cap, "sources": [CHANGELOG_URL]}

    # Separate new (not in curated list) from confirmed
    new_capabilities = []
    confirmed_capabilities = []
    for name_key, cap in all_detected.items():
        if name_key not in known:
            new_capabilities.append(cap)
        else:
            confirmed_capabilities.append(cap["name"])

    print(f"\nResults:")
    print(f"  Confirmed existing: {len(confirmed_capabilities)}")
    print(f"  Potentially new:    {len(new_capabilities)}")

    if new_capabilities:
        print("\nPotentially new capabilities (not in curated list):")
        for cap in new_capabilities:
            print(f"  - {cap['name']} ({cap['category']}) — matched: {cap['matched_pattern']}")

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "docs_pages_scanned": len(DOCS_PAGES) + 1,
        "confirmed_count": len(confirmed_capabilities),
        "new_count": len(new_capabilities),
        "new_capabilities": new_capabilities,
        "recent_changelog_entries": changelog_entries,
    }

    if args.dry_run:
        print("\n[dry-run] Would write:")
        print(json.dumps(result, indent=2))
        return

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nWrote {args.output}")


if __name__ == "__main__":
    main()
