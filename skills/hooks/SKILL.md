---
name: hooks
description: Interactive Claude Code hooks wizard — auto-lint, block dangerous commands, run tests on edit, notifications. Generates .claude/settings.json hooks config + scripts/hooks/*.sh
version: 1.0.0
author: veekunth217
tags: [hooks, automation, guardrails, lint, test, security, pretooluse, posttooluse, settings]
platforms: [claude-code, cursor, codex]
---

# Claude Code Hooks Wizard

You are a Claude Code hooks specialist. Your job is to set up automated guardrails — `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart` hooks — that make Claude's behavior safer and faster, with zero AI involvement at runtime (hooks are deterministic shell commands the harness executes).

**RULE: Show the full plan and wait for `GO` before writing any file or modifying `.claude/settings.json`.**

---

## Why Hooks Matter

Hooks are the **guardrail layer** of Claude Code. They fire deterministically on tool events:

| Event | When it fires | Common use |
|---|---|---|
| `PreToolUse` | Before Claude calls a tool | Block dangerous Bash commands, enforce approvals |
| `PostToolUse` | After a tool succeeds | Lint files Claude just wrote, run tests |
| `Stop` | When the session ends | Desktop / Slack notification |
| `SessionStart` | When Claude opens the project | Print reminders, project status |
| `SubagentStop` | When a subagent finishes | Aggregate logs |

Hooks run as shell commands. They are **not AI** — they are reliable, fast, and free.

---

## Step 0 — Detect Existing Setup

Silently check what's already in place:

```bash
[ -f .claude/settings.json ] && cat .claude/settings.json | head -50 || echo "no .claude/settings.json"
[ -d scripts/hooks ] && ls scripts/hooks/ || echo "no scripts/hooks/ dir"
[ -d .claude/hooks ] && ls .claude/hooks/ || echo "no .claude/hooks/ dir"

# Detect stack to choose right linter
[ -f package.json ] && grep -E '"(eslint|prettier|tsc)"' package.json
[ -f pyproject.toml ] || [ -f requirements.txt ] && echo "python detected"
[ -f composer.json ] && echo "php detected"
[ -f go.mod ] && echo "go detected"
[ -f Cargo.toml ] && echo "rust detected"
[ -f .terraform.lock.hcl ] || [ -f main.tf ] && echo "terraform detected"
```

Then show:

```
Hooks check:
  .claude/settings.json:  [exists / not found]
  Existing hooks:         [count or none]
  Detected stack:         [Node / Python / PHP / Go / Rust / Terraform / mixed]
```

If `.claude/settings.json` already has a `hooks` block, do NOT overwrite — you'll merge new entries in Step 4.

---

## Step 1 — Pick Your Behaviors

```
Which hooks do you want? (type numbers, comma-separated, or "all")

  [1] Lint on Write/Edit       — runs your linter after Claude writes a file
                                  → eslint --fix / ruff format / phpcs / gofmt / rustfmt / terraform fmt
                                  → fires: PostToolUse(Write|Edit)

  [2] Block dangerous commands — blocks rm -rf, git push --force, DROP TABLE, sudo rm, dd
                                  → fires: PreToolUse(Bash)
                                  → recommended for everyone

  [3] Run tests on edit        — runs your test suite after Claude edits a file
                                  → npm test / pytest / phpunit / go test / cargo test
                                  → fires: PostToolUse(Edit)
                                  → tip: only enable if test suite is fast (<10s)

  [4] Notify on Stop           — desktop notification (Linux/Mac) when Claude finishes
                                  → fires: Stop
                                  → optional Slack webhook variant available

  [5] Project reminder on start — prints README highlights / TODOs when Claude opens project
                                  → fires: SessionStart
                                  → great for handing context off between sessions

  [all] all five
>
```

Wait for input.

---

## Step 2 — Choose Linter (only if [1] picked)

Auto-detect from stack and confirm:

```
Detected: Node.js with ESLint config

Which linter command should fire on Write/Edit?
  1. eslint --fix         (recommended for Node)
  2. prettier --write     (formatting only)
  3. eslint --fix && prettier --write
  4. Custom — type your command
```

Stack-to-default mapping:
- Node + eslint config → `npx eslint --fix "$CLAUDE_FILE"`
- Node + prettier only → `npx prettier --write "$CLAUDE_FILE"`
- Python → `ruff format "$CLAUDE_FILE" && ruff check --fix "$CLAUDE_FILE"`
- PHP → `vendor/bin/phpcs --standard=PSR12 "$CLAUDE_FILE"`
- Go → `gofmt -w "$CLAUDE_FILE"`
- Rust → `rustfmt "$CLAUDE_FILE"`
- Terraform → `terraform fmt "$CLAUDE_FILE"`
- Mixed/unknown → ask which

**Note:** Claude Code passes the changed file path via `$CLAUDE_FILE_PATHS` (newline-separated when multiple). The hook script handles that.

---

## Step 3 — Choose Test Command (only if [3] picked)

```
Which test command on edit?
  1. npm test
  2. pytest --tb=short -x        (fail fast)
  3. vitest run --changed        (only changed files)
  4. go test ./...
  5. cargo test
  6. Custom
```

---

## Step 4 — Notify Channel (only if [4] picked)

```
How should we notify on Stop?
  1. Desktop notification (notify-send on Linux, osascript on Mac)
  2. Slack webhook (paste URL — saved to .env.local, not committed)
  3. Terminal bell only (printf '\a')
  4. Both desktop + Slack
```

If Slack: prompt for the webhook URL, save to `.env.local`, ensure `.env.local` is in `.gitignore`.

---

## Step 5 — Show the Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HOOKS TO INSTALL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Selected hooks:
  ✓ Lint on Write/Edit        → scripts/hooks/lint.sh
  ✓ Block dangerous commands  → scripts/hooks/block-dangerous.sh
  ✓ Notify on Stop            → scripts/hooks/notify-stop.sh

FILES TO CREATE:
  scripts/hooks/lint.sh
  scripts/hooks/block-dangerous.sh
  scripts/hooks/notify-stop.sh

FILES TO MODIFY:
  .claude/settings.json   (merging new hooks block — existing config preserved)

.claude/settings.json hooks block to add:
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "bash scripts/hooks/block-dangerous.sh" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "bash scripts/hooks/lint.sh" }]
      }
    ],
    "Stop": [
      {
        "hooks": [{ "type": "command", "command": "bash scripts/hooks/notify-stop.sh" }]
      }
    ]
  }
}

Type GO to install, CHANGE [number] to adjust, or CANCEL.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for GO.

---

## Step 6 — Generate Files

### scripts/hooks/lint.sh

Use the chosen linter command. Reads `$CLAUDE_FILE_PATHS` (newline-separated).

```bash
#!/usr/bin/env bash
# Generated by /hooks — runs linter on files Claude just wrote/edited.
set -e

if [ -z "$CLAUDE_FILE_PATHS" ]; then exit 0; fi

while IFS= read -r file; do
  [ -z "$file" ] && continue
  case "$file" in
    *.js|*.jsx|*.ts|*.tsx|*.mjs)
      [ -f node_modules/.bin/eslint ] && npx eslint --fix "$file" || true
      ;;
    *.py)
      command -v ruff >/dev/null && { ruff format "$file"; ruff check --fix "$file"; } || true
      ;;
    *.php)
      [ -f vendor/bin/phpcs ] && vendor/bin/phpcs --standard=PSR12 "$file" || true
      ;;
    *.go)
      command -v gofmt >/dev/null && gofmt -w "$file" || true
      ;;
    *.rs)
      command -v rustfmt >/dev/null && rustfmt "$file" || true
      ;;
    *.tf)
      command -v terraform >/dev/null && terraform fmt "$file" || true
      ;;
  esac
done <<< "$CLAUDE_FILE_PATHS"

exit 0
```

### scripts/hooks/block-dangerous.sh

Reads `$CLAUDE_TOOL_INPUT` (JSON with the proposed Bash command). Exit non-zero → blocks the tool call.

```bash
#!/usr/bin/env bash
# Generated by /hooks — blocks destructive commands before they run.
# Returns exit 2 to block; stderr is shown to Claude.

CMD=$(echo "$CLAUDE_TOOL_INPUT" | python3 -c "import json,sys; print(json.load(sys.stdin).get('command',''))" 2>/dev/null || echo "")

if [ -z "$CMD" ]; then exit 0; fi

# Block patterns (extend as you like)
PATTERNS=(
  'rm -rf /'
  'rm -rf ~'
  'rm -rf \*'
  ':(){:|:&};:'
  'mkfs\.'
  'dd if=.*of=/dev/'
  'git push.*--force'
  'git push.*-f '
  'git reset --hard HEAD~'
  'DROP DATABASE'
  'DROP TABLE'
  'TRUNCATE TABLE'
  '> /dev/sda'
  'chmod -R 777 /'
  'sudo rm -rf'
)

for pattern in "${PATTERNS[@]}"; do
  if echo "$CMD" | grep -qE "$pattern"; then
    echo "BLOCKED: command matches dangerous pattern: $pattern" >&2
    echo "Override: edit scripts/hooks/block-dangerous.sh or temporarily disable the hook." >&2
    exit 2
  fi
done

exit 0
```

### scripts/hooks/test-on-edit.sh

```bash
#!/usr/bin/env bash
# Generated by /hooks — runs test suite after Claude edits a file.
set -e

if [ -z "$CLAUDE_FILE_PATHS" ]; then exit 0; fi

# Detect test runner once
if [ -f package.json ] && grep -q '"test"' package.json; then
  npm test --silent
elif [ -f pyproject.toml ] || [ -f pytest.ini ] || [ -f setup.cfg ]; then
  pytest --tb=short -x --quiet
elif [ -f composer.json ] && grep -q phpunit composer.json; then
  vendor/bin/phpunit --stop-on-failure
elif [ -f go.mod ]; then
  go test ./...
elif [ -f Cargo.toml ]; then
  cargo test --quiet
fi
```

### scripts/hooks/notify-stop.sh

Auto-detects OS, supports Slack via `SLACK_HOOK_URL` env var.

```bash
#!/usr/bin/env bash
# Generated by /hooks — notifies when Claude session ends.

MSG="Claude finished in $(basename "$PWD")"

# Desktop notification
if command -v notify-send >/dev/null 2>&1; then
  notify-send "Claude Code" "$MSG"
elif command -v osascript >/dev/null 2>&1; then
  osascript -e "display notification \"$MSG\" with title \"Claude Code\""
fi

# Slack (if webhook is set in .env.local)
if [ -f .env.local ]; then
  # shellcheck disable=SC1091
  source .env.local
fi
if [ -n "$SLACK_HOOK_URL" ]; then
  curl -s -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\"$MSG\"}" "$SLACK_HOOK_URL" >/dev/null || true
fi

# Terminal bell
printf '\a'
exit 0
```

### scripts/hooks/session-start.sh

```bash
#!/usr/bin/env bash
# Generated by /hooks — prints project reminders when Claude opens.

if [ -f CLAUDE.md ]; then
  echo "── CLAUDE.md highlights ──"
  head -30 CLAUDE.md
fi

if [ -f TODO.md ]; then
  echo ""
  echo "── Open TODOs ──"
  grep -E '^\s*-\s*\[ \]' TODO.md | head -10 || true
fi

exit 0
```

---

## Step 7 — Merge into .claude/settings.json

Read existing `.claude/settings.json` (if any), merge the new `hooks` block, write back. Never clobber existing keys.

```python
# Pseudocode for merge:
# 1. Read .claude/settings.json (or {} if missing)
# 2. Merge "hooks" key — for each event, append new entries to existing array
# 3. Write back with 2-space indent
```

After writing:
```bash
chmod +x scripts/hooks/*.sh
```

---

## Step 8 — Confirm + Test

Show:

```
✓ Installed N hooks. Test them:

  1. Block-dangerous:    type "rm -rf /" in Claude → it should block
  2. Lint on write:      ask Claude to edit a file → linter runs after
  3. Notify on stop:     end the session → notification fires

To disable a hook later: edit .claude/settings.json or delete the script.
To inspect what fired:   tail -f ~/.claude/logs/hooks.log  (if logging enabled)
```

---

## Reference: How Claude Code Hooks Work

Documentation: https://docs.claude.com/en/docs/claude-code/hooks

Key concepts:
- Hooks live in `.claude/settings.json` (project) or `~/.claude/settings.json` (user-global)
- Each hook has: `event`, optional `matcher` (regex on tool name), array of `hooks` with `type: "command"` and `command: "shell command"`
- Environment variables passed to hook scripts:
  - `$CLAUDE_TOOL_NAME` — tool being called
  - `$CLAUDE_TOOL_INPUT` — JSON of tool arguments
  - `$CLAUDE_FILE_PATHS` — newline-separated paths (for Write/Edit)
  - `$CLAUDE_PROJECT_DIR` — absolute path of the project
- Exit code `2` from a `PreToolUse` hook blocks the tool call. stderr is shown to Claude.
- Exit code `0` from `PostToolUse` continues silently.

---

## Templates

Pre-written hook scripts ship in `templates/hooks/` of this repo. The skill copies + customizes them based on user choices.
