#!/usr/bin/env bash
# Runs the test suite after Claude edits a file.
# Wired in via .claude/settings.json hooks.PostToolUse(matcher=Edit).
# WARNING: Only enable if your test suite is fast (<10s) — otherwise this slows every edit.

set -e

if [ -z "$CLAUDE_FILE_PATHS" ]; then
  exit 0
fi

# Skip if user only edited config/docs (heuristic — adjust to taste)
SKIP=true
while IFS= read -r file; do
  case "$file" in
    *.md|*.json|*.yml|*.yaml|*.toml|*.lock|*.gitignore) ;;
    *) SKIP=false ;;
  esac
done <<< "$CLAUDE_FILE_PATHS"

if [ "$SKIP" = "true" ]; then
  exit 0
fi

# Detect test runner and run
if [ -f package.json ] && grep -q '"test"' package.json; then
  npm test --silent 2>&1 || echo "tests: npm test failed"
elif [ -f pyproject.toml ] || [ -f pytest.ini ] || [ -f setup.cfg ]; then
  if command -v pytest >/dev/null 2>&1; then
    pytest --tb=short -x --quiet 2>&1 || echo "tests: pytest failed"
  fi
elif [ -f composer.json ] && grep -q phpunit composer.json; then
  if [ -f vendor/bin/phpunit ]; then
    vendor/bin/phpunit --stop-on-failure 2>&1 || echo "tests: phpunit failed"
  fi
elif [ -f go.mod ]; then
  go test ./... 2>&1 || echo "tests: go test failed"
elif [ -f Cargo.toml ]; then
  cargo test --quiet 2>&1 || echo "tests: cargo test failed"
fi

exit 0
