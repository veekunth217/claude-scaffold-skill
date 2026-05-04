---
name: git-safety-credentials-near-miss
description: Never use 'git add .' blindly — caught .jetro/daemon/credentials.json about to be committed
type: feedback
originSessionId: 093c4187-2dda-4c9a-bbc0-989f2dd61d0e
---
Never run `git add .` without first checking `git status` and reading every untracked file listed.

In this project, `.jetro/daemon/credentials.json` appeared as an untracked file and would have been staged and pushed to a public repo if `git add .` had run.

**Why:** .jetro/ is a tool that creates credential files in the project directory. These are not project files and must never be committed.

**How to apply:** Before any `git add`, always run `git status --short | grep "^?"` to see untracked files, then read them before staging. Prefer explicit `git add <specific-files>` over `git add .`. If a file looks like credentials, config, or tool state — check it, then add it to .gitignore immediately.

Current safe pattern for this project:
```bash
git add .gitignore README.md SKILL.md skills/ scripts/ registry/ .claude-context/
```
Never: `git add .` or `git add -A`
