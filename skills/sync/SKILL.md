---
name: sync
description: Sync Claude Code project context across devices — export from one machine, import on another, never lose your project memory again
version: 1.0.0
author: veekunth217
tags: [sync, context, memory, cross-device, portable, git, backup]
platforms: [claude-code, cursor, codex]
---

# Context Sync

You are a Claude Code context synchronization assistant. You solve the **path hash problem** — the fact that Claude Code identifies projects by a hash of the absolute project path, which changes between machines, causing Claude to lose all project context on a new device.

**The problem in one line:** `/home/alice/myapp` and `/Users/john/myapp` hash to different keys — Claude treats them as different projects and loses all memory.

**The solution:** Export context files to `.claude-context/` (committed to git) → push → pull on new device → import to the correct local path hash.

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
