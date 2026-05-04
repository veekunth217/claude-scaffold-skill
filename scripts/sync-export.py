#!/usr/bin/env python3
"""
sync-export.py — Export Claude Code project context to .claude-context/

Copies markdown context files from ~/.claude/projects/<path-hash>/
to .claude-context/ (which is committed to git), enabling cross-device sync.

WHY: Claude Code identifies projects by a hash of the absolute project path.
     On a different machine, the same project has a different hash and Claude
     loses all context. This script exports the context files so they can be
     committed and re-imported on another device.

Usage:
    python scripts/sync-export.py
    python scripts/sync-export.py --dry-run
    python scripts/sync-export.py --no-commit
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

EXPORT_DIR = ".claude-context"
MANIFEST_FILE = "sync-manifest.json"

INCLUDE_PATTERNS = [
    "MEMORY.md",
    "memory",          # folder
    "project_*.md",
    "feedback_*.md",
    "user_*.md",
    "reference_*.md",
    "*.md",
]

EXCLUDE_PATTERNS = [
    "*.jsonl",         # conversation history — too large, private
    "*.json",          # may contain API keys or settings
    "*.log",
    "__pycache__",
    ".DS_Store",
]


def get_path_hash() -> str:
    """Calculate the Claude Code path hash for the current directory."""
    abs_path = os.path.abspath(".")
    # Claude uses the absolute path with separators replaced by '-'
    # Leading slash becomes '-' on Linux/Mac, drive letter handled on Windows
    claude_key = abs_path.replace("/", "-").replace("\\", "-").replace(":", "-")
    return claude_key


def get_claude_source_dir() -> Path:
    """Return the ~/.claude/projects/<hash>/ path for this project."""
    claude_key = get_path_hash()
    home = Path.home()
    return home / ".claude" / "projects" / claude_key


def get_claude_version() -> str:
    try:
        result = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or result.stderr.strip() or "unknown"
    except Exception:
        return "unknown"


def should_exclude(name: str) -> bool:
    import fnmatch
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(name, pat):
            return True
    return False


def collect_files(source: Path) -> list[Path]:
    """Return all context files to export from the source directory."""
    if not source.exists():
        return []

    files = []
    for item in source.iterdir():
        if should_exclude(item.name):
            continue
        if item.is_file() and item.suffix == ".md":
            files.append(item)
        elif item.is_dir() and item.name == "memory":
            # Include entire memory/ subfolder
            for subfile in item.rglob("*.md"):
                if not should_exclude(subfile.name):
                    files.append(subfile)

    return sorted(files)


def export_context(dry_run: bool = False, no_commit: bool = False) -> int:
    source = get_claude_source_dir()
    export_path = Path(EXPORT_DIR)

    print(f"Claude project folder: {source}")
    print(f"Export target:         {export_path.absolute()}")
    print()

    if not source.exists():
        print(f"ERROR: Source folder does not exist: {source}")
        print("This means Claude Code has no stored context for this project yet.")
        print("Open this project in Claude Code and have a conversation first.")
        return 1

    files = collect_files(source)

    if not files:
        print("No context files found to export.")
        print(f"(Checked: {source})")
        return 0

    print(f"Found {len(files)} file(s) to export:")
    for f in files:
        rel = f.relative_to(source)
        size = f.stat().st_size
        print(f"  {rel}  ({size:,} bytes)")

    if dry_run:
        print("\n[dry-run] No files written.")
        return 0

    # Create export dir
    export_path.mkdir(exist_ok=True)
    (export_path / ".gitkeep").touch()

    copied = []
    for f in files:
        rel = f.relative_to(source)
        dest = export_path / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        copied.append(str(rel))
        print(f"  ✓ {rel}")

    # Write manifest
    manifest = {
        "version": "1.0",
        "exported_from_os": sys.platform,
        "exported_from_user": os.environ.get("USER") or os.environ.get("USERNAME") or "unknown",
        "exported_from_path": os.path.abspath("."),
        "exported_from_hash": get_path_hash(),
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "files": copied,
        "claude_version": get_claude_version(),
    }
    manifest_path = export_path / MANIFEST_FILE
    with open(manifest_path, "w") as mf:
        json.dump(manifest, mf, indent=2)
    print(f"  ✓ {MANIFEST_FILE} (manifest)")

    print(f"\n✅ Exported {len(copied)} file(s) to {EXPORT_DIR}/")

    if no_commit:
        print("Skipping git commit (--no-commit).")
        print(f"Run: git add {EXPORT_DIR}/ && git push")
        return 0

    # Git commit
    try:
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        subprocess.run(["git", "add", f"{EXPORT_DIR}/"], check=True)
        result = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
        )
        if result.returncode == 0:
            print("Nothing new to commit — context already up to date.")
        else:
            subprocess.run(
                ["git", "commit", "-m", f"context-sync: export {timestamp}"],
                check=True,
            )
            print(f"📦 Committed to git.")
            print(f"Run: git push   → to sync to other devices")
    except subprocess.CalledProcessError as e:
        print(f"WARNING: git operation failed: {e}")
        print(f"Manually run: git add {EXPORT_DIR}/ && git push")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Export Claude Code context to .claude-context/")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be exported without writing")
    parser.add_argument("--no-commit", action="store_true", help="Export files but skip git commit")
    args = parser.parse_args()
    sys.exit(export_context(dry_run=args.dry_run, no_commit=args.no_commit))


if __name__ == "__main__":
    main()
