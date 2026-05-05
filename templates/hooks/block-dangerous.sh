#!/usr/bin/env bash
# Blocks destructive commands before Claude runs them.
# Wired in via .claude/settings.json hooks.PreToolUse(matcher=Bash).
# Exit 2 = block the tool call. stderr is shown to Claude.

# Read the tool input JSON from stdin or env var
if [ -n "$CLAUDE_TOOL_INPUT" ]; then
  INPUT="$CLAUDE_TOOL_INPUT"
else
  INPUT=$(cat 2>/dev/null || echo "")
fi

if [ -z "$INPUT" ]; then
  exit 0
fi

# Extract the proposed command (Python is more reliable than jq for arbitrary JSON)
CMD=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('command', ''))
except Exception:
    pass
" 2>/dev/null)

if [ -z "$CMD" ]; then
  exit 0
fi

# Dangerous patterns — extend as needed
PATTERNS=(
  'rm[[:space:]]+-rf?[[:space:]]+/[[:space:]]*$'
  'rm[[:space:]]+-rf?[[:space:]]+~'
  'rm[[:space:]]+-rf?[[:space:]]+\$HOME'
  'rm[[:space:]]+-rf?[[:space:]]+\*'
  ':\(\)\{[[:space:]]*:\|:&[[:space:]]*\};:'
  'mkfs\.'
  'dd[[:space:]]+if=.*of=/dev/(sd|nvme|hd)'
  'git[[:space:]]+push.*--force'
  'git[[:space:]]+push.*-f([[:space:]]|$)'
  'git[[:space:]]+reset[[:space:]]+--hard[[:space:]]+HEAD~'
  'git[[:space:]]+clean[[:space:]]+-[fdx]+'
  'DROP[[:space:]]+DATABASE'
  'DROP[[:space:]]+TABLE'
  'TRUNCATE[[:space:]]+TABLE'
  '>[[:space:]]*/dev/(sd|nvme|hd)'
  'chmod[[:space:]]+-R[[:space:]]+777[[:space:]]+/'
  'chown[[:space:]]+-R[[:space:]]+.*[[:space:]]+/'
  'sudo[[:space:]]+rm[[:space:]]+-rf'
  'curl[[:space:]]+.*\|[[:space:]]*sh'
  'wget[[:space:]]+.*\|[[:space:]]*sh'
)

for pattern in "${PATTERNS[@]}"; do
  if echo "$CMD" | grep -qE "$pattern"; then
    cat >&2 <<EOF
BLOCKED by hooks/block-dangerous.sh
  Pattern matched: $pattern
  Command:         $CMD

If this is a false positive, edit scripts/hooks/block-dangerous.sh
or temporarily disable the hook in .claude/settings.json.
EOF
    exit 2
  fi
done

exit 0
