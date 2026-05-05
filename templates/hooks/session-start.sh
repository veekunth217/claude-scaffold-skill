#!/usr/bin/env bash
# Prints project context when Claude opens.
# Wired in via .claude/settings.json hooks.SessionStart.

if [ -f CLAUDE.md ]; then
  echo "── CLAUDE.md highlights ──"
  head -30 CLAUDE.md
  echo ""
fi

if [ -f TODO.md ]; then
  echo "── Open TODOs ──"
  grep -E '^\s*-\s*\[ \]' TODO.md 2>/dev/null | head -10 || true
  echo ""
fi

# Recent git activity (last 5 commits, current branch)
if [ -d .git ]; then
  echo "── Recent commits ──"
  git log --oneline -5 2>/dev/null || true
  echo ""
  BRANCH=$(git branch --show-current 2>/dev/null)
  if [ -n "$BRANCH" ] && [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
    echo "→ on branch: $BRANCH"
  fi
fi

exit 0
