#!/usr/bin/env python3
"""
sync-import.py — Import Claude Code project context from .claude-context/

Reads exported context files from .claude-context/ and installs them into
~/.claude/projects/<this-device-hash>/ so Claude Code finds them immediately.

This is the counterpart to sync-export.py. Run after `git pull` on a new device.

Usage:
    python scripts/sync-import.py
    python scripts/sync-import.py --dry-run
    python scripts/sync-import.py --no-pull
"""

import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

EXPORT_DIR = ".claude-context"
MANIFEST_FILE = "sync-manifest.json"


def get_path_hash() -> str:
    """Calculate the Claude Code path hash for the current directory on THIS device."""
    abs_path = os.path.abspath(".")
    claude_key = abs_path.replace("/", "-").replace("\\", "-").replace(":", "-")
    return claude_key


def get_claude_target_dir() -> Path:
    """Return the ~/.claude/projects/<hash>/ path for this project on this device."""
    claude_key = get_path_hash()
    home = Path.home()
    return home / ".claude" / "projects" / claude_key


def import_context(dry_run: bool = False, no_pull: bool = False) -> int:
    export_path = Path(EXPORT_DIR)
    target = get_claude_target_dir()

    print(f"Import source: {export_path.absolute()}")
    print(f"Target folder: {target}")
    print()

    # git pull
    if not no_pull:
        print("Pulling latest context from git...")
        try:
            result = subprocess.run(
                ["git", "pull", "--rebase"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"  {result.stdout.strip() or 'Already up to date.'}")
            else:
                print(f"  WARNING: git pull failed: {result.stderr.strip()}")
                print("  Continuing with local .claude-context/ as-is.")
        except FileNotFoundError:
            print("  WARNING: git not found, skipping pull.")
        print()

    # Check export dir exists
    if not export_path.exists():
        print(f"ERROR: {EXPORT_DIR}/ not found.")
        print("Run sync-export.py on another device first, then push.")
        return 1

    # Read manifest
    manifest_path = export_path / MANIFEST_FILE
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path) as mf:
            manifest = json.load(mf)
        print("Manifest:")
        print(f"  Exported from: {manifest.get('exported_from_path', 'unknown')}")
        print(f"  Exported by:   {manifest.get('exported_from_user', 'unknown')} on {manifest.get('exported_from_os', 'unknown')}")
        print(f"  Exported at:   {manifest.get('exported_at', 'unknown')}")
        print(f"  Files:         {len(manifest.get('files', []))}")
        print()

    # Collect files to import
    files_to_import = []
    for item in export_path.iterdir():
        if item.name in (".gitkeep", MANIFEST_FILE, ".gitignore"):
            continue
        if item.is_file() and item.suffix == ".md":
            files_to_import.append(item)
        elif item.is_dir() and item.name == "memory":
            for subfile in item.rglob("*.md"):
                files_to_import.append(subfile)

    if not files_to_import:
        print("No context files found in .claude-context/")
        print("Make sure sync-export.py was run on another device and changes were pushed.")
        return 0

    print(f"Files to import:")
    for f in sorted(files_to_import):
        rel = f.relative_to(export_path)
        print(f"  {rel}")

    if dry_run:
        print(f"\n[dry-run] Would restore to: {target}")
        print("No files written.")
        return 0

    # Create target directory
    target.mkdir(parents=True, exist_ok=True)

    restored = []
    for f in sorted(files_to_import):
        rel = f.relative_to(export_path)
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest)
        restored.append(str(rel))
        print(f"  ✓ {rel}")

    print()
    print(f"✅ Context restored on this device")
    print(f"📁 Restored to: {target}/")
    print(f"📄 Files restored: {', '.join(restored)}")
    print()

    # Path hash diff notice
    exported_hash = manifest.get("exported_from_hash", "")
    this_hash = get_path_hash()
    if exported_hash and exported_hash != this_hash:
        print(f"ℹ️  Path hash difference (expected — different device or username):")
        print(f"   Source hash: {exported_hash}")
        print(f"   This hash:   {this_hash}")
        print(f"   Files were correctly installed to the right location for this device.")
    print()
    print(f"💡 Claude Code will now remember your project context on this device.")
    print(f"   Restart Claude Code or open this project to verify.")

    return 0


def main():
    parser = argparse.ArgumentParser(description="Import Claude Code context from .claude-context/")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported without writing")
    parser.add_argument("--no-pull", action="store_true", help="Skip git pull, use local .claude-context/ as-is")
    args = parser.parse_args()
    sys.exit(import_context(dry_run=args.dry_run, no_pull=args.no_pull))


if __name__ == "__main__":
    main()
