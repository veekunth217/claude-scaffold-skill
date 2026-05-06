# Security Policy

## Reporting a vulnerability

If you find a security issue in this repo (e.g. a SKILL.md that runs unsafe shell, a script
that exfiltrates data, a registry entry pointing to a compromised repo), please report it
privately first — don't open a public issue.

**How to report:**

1. Open a [private security advisory](https://github.com/veekunth217/claude-scaffold-skill/security/advisories/new) on GitHub, OR
2. Open a regular issue with the title `[Security]` and we'll triage it without details.

We'll acknowledge within 72 hours and aim for a fix within 7 days for verified issues.

## What this project ships

- **Markdown SKILL.md files** — instructions Claude reads. They are not executable code,
  but they do tell Claude what shell commands to suggest. Audit any new skill before merging.
- **Shell scripts in `templates/hooks/`** — these run in the user's environment when wired
  into `.claude/settings.json`. Scope is limited to lint/format/block-dangerous patterns.
- **Python scripts in `scripts/`** — registry tooling. Stdlib only, no external deps.
- **Registry entries** — point to third-party GitHub repos. We verify URLs exist (CI), but
  we do **not** audit the contents of every linked skill. Treat unverified entries as
  community submissions, not endorsements.

## What this project does NOT do

- Send any telemetry or analytics
- Auto-execute remote code on install
- Modify your shell config without explicit user approval
- Read or transmit your project files outside the local machine

## Auditing third-party skills before installing

Before installing any skill from the registry:

```bash
# 1. Read the SKILL.md
cat ~/.claude/skills/<skill-name>/SKILL.md

# 2. Check what shell commands it instructs Claude to run
grep -E '\$\(|`[^`]*`|exec\(|subprocess|os\.system' ~/.claude/skills/<skill-name>/SKILL.md

# 3. Look for any scripts it ships
find ~/.claude/skills/<skill-name> -name "*.sh" -o -name "*.py"
```

If anything looks suspicious, uninstall: `rm -rf ~/.claude/skills/<skill-name>`.
