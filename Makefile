.PHONY: validate validate-full test search update-stars discover discover-capabilities help

help:
	@echo "claude-scaffold-skill — available commands:"
	@echo ""
	@echo "  make validate               Validate registry structure (fast, no network)"
	@echo "  make validate-full          Validate + verify every repo exists on GitHub"
	@echo "  make test                   Alias for validate-full (CI entry point)"
	@echo "  make search Q=<keyword>     Search the registry (e.g. make search Q=pdf)"
	@echo "  make update-stars           Refresh star counts in skills.json from GitHub API"
	@echo "  make discover               Run skill discovery scraper → registry/discovered.json"
	@echo "  make discover-capabilities  Scan Anthropic docs → registry/discovered-capabilities.json"
	@echo ""
	@echo "Set GITHUB_TOKEN env var before running network commands."

validate:
	python scripts/validate-registry.py

validate-full:
	python scripts/validate-registry.py --check-github

test: validate-full

search:
	@if [ -z "$(Q)" ]; then \
		echo "Usage: make search Q=<keyword>   (e.g. make search Q=pdf)"; \
		exit 1; \
	fi
	@python scripts/search-registry.py "$(Q)"

update-stars:
	python scripts/update-stars.py

discover:
	python scripts/fetch-skills.py --output registry/discovered.json

discover-capabilities:
	python scripts/fetch-capabilities.py --output registry/discovered-capabilities.json
