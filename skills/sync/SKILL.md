---
name: sync
description: Share project memory across devices AND across AI tools (Claude Code, Cursor, Codex, Roo, Cline, Aider, Windsurf) — git-native, no SaaS, no lock-in.
version: 2.0.0
author: veekunth217
tags: [sync, context, memory, cross-device, cross-tool, mcp, portable, git, backup]
platforms: [claude-code, cursor, codex]
---

# Context Sync — Cross-Device + Cross-Tool

Two problems, one canonical source of truth:

1. **Cross-device** — Claude Code identifies projects by a hash of the absolute path, so context is lost between machines (`/home/alice/myapp` → `-home-alice-myapp` ≠ `/Users/john/myapp` → `-Users-john-myapp`). Solved by `export` / `import`.

2. **Cross-tool** — You use Claude Code, Cursor, Codex CLI, Roo, Cline, Aider, or Windsurf — each has its own instruction/memory file (`CLAUDE.md`, `.cursorrules`, `AGENTS.md`, ...). You re-explain your project to every one. Solved by `tools push` — one canonical memory file → adapter files for every detected tool.

**The shared truth:** `.claude-context/MEMORY.md` (+ `memory/*.md`), committed to git.
Every tool reads from a locally-generated adapter file pointing at that truth.
No SaaS. No proprietary memory broker. No vendor lock-in.

---

## Commands

### `/sync export`

Export current project context to `.claude-context/` and commit.

Run:
```bash
python scripts/sync-export.py
```

What it does:
1. Calculates the Claude path hash for the current directory
2. Finds `~/.claude/projects/<hash>/` — reads all `.md` context files
3. Copies them to `.claude-context/` in the project
4. Creates `.claude-context/sync-manifest.json` with device metadata
5. Runs `git add .claude-context/ && git commit -m "context-sync: export <timestamp>"`
6. Prints: push reminder

Then push:
```bash
git push
```

**What gets exported:**
- `MEMORY.md` — your project memory index
- `memory/*.md` — individual memory files
- `project_*.md`, `feedback_*.md`, `user_*.md`, `reference_*.md` — all context docs

**What stays private (never exported):**
- `*.jsonl` — conversation history (too large, private)
- `*.json` — may contain API keys or settings

---

### `/sync import`

Restore project context on this device from `.claude-context/`.

Run:
```bash
python scripts/sync-import.py
```

What it does:
1. Runs `git pull` to get latest `.claude-context/`
2. Reads the manifest to confirm what was exported
3. Calculates the path hash for **this device**
4. Creates `~/.claude/projects/<this-hash>/` if needed
5. Copies all files from `.claude-context/` to the correct local target
6. Prints a summary of restored files

After import: restart Claude Code or open the project. Claude immediately has full context.

---

### `/sync status`

Show what has changed between the exported context and the current local context.

Check manually:
```bash
# What's in the local Claude folder
ls -la ~/.claude/projects/$(python3 -c "import os; print(os.path.abspath('.').replace('/', '-').replace('\\\\', '-').replace(':', '-'))")/

# What's been exported
ls -la .claude-context/

# Diff a specific file
diff .claude-context/MEMORY.md ~/.claude/projects/$(python3 -c "import os; print(os.path.abspath('.').replace('/', '-').replace('\\\\', '-').replace(':', '-'))")/MEMORY.md
```

Or ask Claude directly to compare them and summarize what's new, changed, or missing.

---

### `/sync clean`

Remove large files from the local Claude project folder to reduce size before export.

Run:
```bash
# Show what's in your Claude project folder
python3 -c "
import os
from pathlib import Path
key = os.path.abspath('.').replace('/', '-').replace('\\\\', '-').replace(':', '-')
folder = Path.home() / '.claude' / 'projects' / key
if folder.exists():
    for f in sorted(folder.iterdir()):
        print(f'{f.stat().st_size:>10,}  {f.name}')
else:
    print('No Claude project folder found')
"

# Remove conversation history (*.jsonl) to free space
python3 -c "
import os
from pathlib import Path
key = os.path.abspath('.').replace('/', '-').replace('\\\\', '-').replace(':', '-')
folder = Path.home() / '.claude' / 'projects' / key
removed = 0
for f in folder.glob('*.jsonl'):
    size = f.stat().st_size
    f.unlink()
    print(f'Removed {f.name} ({size:,} bytes)')
    removed += size
print(f'Freed {removed:,} bytes')
"
```

---

### `/sync tools detect`

List which AI dev tools are present in this project — shows what `tools push` would write.

Run:
```bash
python scripts/sync-tools.py detect
```

Detection (no false positives — we only write where the tool already lives):

| Tool | Output adapter file | Detected by |
|---|---|---|
| Claude Code | `CLAUDE.md` | always written (universal) |
| Cursor | `.cursor/rules/memory.mdc` | `.cursor/` or `.cursorrules` exists |
| Roo Code | `.roo/rules/memory.md` | `.roo/` or `.rooignore` exists |
| Cline | `.clinerules/memory.md` | `.clinerules` exists |
| Codex CLI | `AGENTS.md` | `.codex/` or `AGENTS.md` exists |
| Aider | `CONVENTIONS.md` | `.aider/`, `CONVENTIONS.md`, or `.aider.conf.yml` |
| Windsurf | `.windsurfrules` | `.windsurfrules` or `.windsurf/` exists |

---

### `/sync tools push`

Generate adapter files from `.claude-context/MEMORY.md` for every detected tool.

Run:
```bash
python scripts/sync-tools.py push            # write them
python scripts/sync-tools.py push --dry-run  # show diff without writing
python scripts/sync-tools.py push --only cursor,claude  # subset
```

What it does:
1. Assembles the canonical memory (`MEMORY.md` + every `memory/*.md`) into one block
2. For each detected tool, wraps it in the right format (e.g. Cursor `.mdc` gets YAML frontmatter) with a clear "AUTO-GENERATED" header pointing back to the source
3. Writes `.claude-context/sync-tools-manifest.json` listing what was written

**Why this is better than commercial cross-AI memory tools (Vilix, Mem0):**
- No SaaS subscription
- Memory lives in your git repo, not a third-party DB
- One canonical file you can `git blame`, diff, and review like code
- New devs run `python scripts/sync-tools.py push` after `git clone` — every AI tool they use immediately has the project context
- When you update `.claude-context/MEMORY.md`, re-run push and every adapter regenerates

**Why most adapter files are gitignored:**
They're per-machine projections of the canonical source. Committing them would create merge conflicts every time someone with a different tool stack syncs. The source-of-truth (`.claude-context/`) is what's committed; the adapters are local rebuilds.

**Phase 2 — live MCP sync (planned, contributions welcome):**
See [PHASE2-MCP.md](PHASE2-MCP.md) for the full spec. Adds a small MCP server alongside the file adapters so edits flow between tools without re-running push. Covers every MCP-capable tool (Claude Code, Cursor, Codex CLI, Windsurf, Roo, Cline). The file-based Phase 1 stays as the universal fallback and the source of truth.

---

## How the Path Hash Works

Claude Code generates the project key from the absolute path:

```python
abs_path = os.path.abspath('.')
# /home/alice/myapp
# → replace '/' with '-'
# → -home-alice-myapp

claude_key = abs_path.replace('/', '-').replace('\\', '-').replace(':', '-')
source = f"~/.claude/projects/{claude_key}/"
```

| Device | Path | Hash |
|--------|------|------|
| Linux VPS | `/home/alice/myapp` | `-home-alice-myapp` |
| Mac | `/Users/john/myapp` | `-Users-john-myapp` |
| Windows | `C:\Users\john\myapp` | `-C--Users-john-myapp` |

These are all the same project but Claude sees three different contexts. `sync-import.py` handles this automatically — it always installs to the correct hash for **the current device**, regardless of where it was exported from.

---

## Full Cross-Device Workflow

```
Device A (VPS):
  1. Open project in Claude Code
  2. Work — Claude builds up memory, project context
  3. /sync export → git push

Device B (Mac / laptop):
  1. git clone <repo> (or git pull)
  2. /sync import
  3. Open project in Claude Code
  4. Claude remembers everything from Device A

Keep in sync:
  Device A: /sync export → git push   (after significant sessions)
  Device B: /sync import              (after git pull)
```

---

## Setup (one-time)

The `.claude-context/` folder is already part of the repo (committed). The scripts are in `scripts/`. No dependencies — pure Python stdlib.

Make sure `.claude-context/` is **not** in `.gitignore` (this is intentional — it's the sync mechanism). The `*.jsonl` exclusion in `.gitignore` prevents conversation history from being committed.

---

## What Gets Synced

| File type | Synced | Why |
|-----------|--------|-----|
| `MEMORY.md` | ✅ | Project memory index |
| `memory/*.md` | ✅ | Individual memory entries |
| `project_*.md` | ✅ | Project context docs |
| `feedback_*.md` | ✅ | Behavioral feedback |
| `user_*.md` | ✅ | User profile context |
| `reference_*.md` | ✅ | Reference links |
| `*.jsonl` | ❌ | Conversation history — private, too large |
| `*.json` | ❌ | Settings — may contain keys |
