#!/usr/bin/env bash
# Notifies when Claude session ends.
# Wired in via .claude/settings.json hooks.Stop.
# Supports: Linux (notify-send), Mac (osascript), Slack (webhook), terminal bell.

PROJECT=$(basename "$PWD")
MSG="Claude finished in $PROJECT"

# Desktop notification
if command -v notify-send >/dev/null 2>&1; then
  notify-send "Claude Code" "$MSG" 2>/dev/null || true
elif command -v osascript >/dev/null 2>&1; then
  osascript -e "display notification \"$MSG\" with title \"Claude Code\"" 2>/dev/null || true
elif command -v powershell.exe >/dev/null 2>&1; then
  powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('$MSG','Claude Code')" 2>/dev/null || true
fi

# Slack (if SLACK_HOOK_URL set in .env.local)
if [ -f .env.local ]; then
  # shellcheck disable=SC1091
  set -a; source .env.local; set +a
fi

if [ -n "$SLACK_HOOK_URL" ]; then
  curl -s -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\":robot_face: $MSG\"}" \
    "$SLACK_HOOK_URL" >/dev/null 2>&1 || true
fi

# Terminal bell
printf '\a'
exit 0
