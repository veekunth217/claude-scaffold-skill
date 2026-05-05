#!/usr/bin/env bash
# Lints files Claude just wrote/edited.
# Auto-detects file type and runs the right tool. Failures don't block — just warn.
# Wired in via .claude/settings.json hooks.PostToolUse(matcher=Write|Edit).

set -e

if [ -z "$CLAUDE_FILE_PATHS" ]; then
  exit 0
fi

while IFS= read -r file; do
  [ -z "$file" ] && continue
  [ ! -f "$file" ] && continue

  case "$file" in
    *.js|*.jsx|*.ts|*.tsx|*.mjs|*.cjs)
      if [ -f node_modules/.bin/eslint ]; then
        npx eslint --fix "$file" 2>&1 || echo "lint: eslint warnings on $file"
      fi
      if [ -f node_modules/.bin/prettier ]; then
        npx prettier --write --log-level=warn "$file" 2>&1 || true
      fi
      ;;
    *.py)
      if command -v ruff >/dev/null 2>&1; then
        ruff format "$file" 2>&1 || true
        ruff check --fix "$file" 2>&1 || echo "lint: ruff warnings on $file"
      elif command -v black >/dev/null 2>&1; then
        black --quiet "$file" 2>&1 || true
      fi
      ;;
    *.php)
      if [ -f vendor/bin/phpcs ]; then
        vendor/bin/phpcs --standard=PSR12 "$file" 2>&1 || echo "lint: phpcs warnings on $file"
      fi
      ;;
    *.go)
      if command -v gofmt >/dev/null 2>&1; then
        gofmt -w "$file"
      fi
      ;;
    *.rs)
      if command -v rustfmt >/dev/null 2>&1; then
        rustfmt "$file" 2>&1 || true
      fi
      ;;
    *.tf|*.tfvars)
      if command -v terraform >/dev/null 2>&1; then
        terraform fmt "$file" 2>&1 || true
      fi
      ;;
    *.json)
      if command -v jq >/dev/null 2>&1; then
        jq . "$file" >/dev/null 2>&1 || echo "lint: invalid JSON in $file"
      fi
      ;;
    *.sh)
      if command -v shellcheck >/dev/null 2>&1; then
        shellcheck "$file" 2>&1 || echo "lint: shellcheck warnings on $file"
      fi
      ;;
  esac
done <<< "$CLAUDE_FILE_PATHS"

exit 0
