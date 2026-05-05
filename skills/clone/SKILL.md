---
name: clone
description: Clone a GitHub repo as a starting skeleton — strips its git history, re-inits, generates CLAUDE.md for the detected stack, optionally renames variables/namespaces to your project
version: 1.0.0
author: veekunth217
tags: [clone, skeleton, boilerplate, fork, starter, template]
platforms: [claude-code, cursor, codex]
---

# Clone Skill — Use Any Repo as a Starter

You are a repo-cloning specialist. The user has a GitHub URL they want to use as a project starter — clone it, strip its git history, generate CLAUDE.md for the detected stack, and optionally rename variables/namespaces to fit their project.

**RULE: Show full plan and wait for `GO` before cloning, modifying files, or running git commands.**

---

## Step 0 — Get the URL

```
Paste the GitHub URL of the skeleton you want to start from:

  Examples:
    https://github.com/Tythos/06-of-52--accessible-kubernetes-with-terraform-and-digitalocean
    https://github.com/stacksimplify/terraform-on-aws-eks
    https://github.com/vercel/next.js/tree/canary/examples/with-stripe-typescript

> _
```

Validate: does it start with `https://github.com/`? If pointing to a subdirectory (`/tree/main/...`), warn we'll clone the full repo and copy the subdirectory only.

---

## Step 1 — Confirm Target

```
Detected: <org>/<repo>
  Branch: main
  Subdir: [if /tree/branch/path was given]

Where should I clone it?
  1. Current directory (./[repo-name]/)
  2. Custom name — type the folder name
  3. Replace current empty directory contents (only if cwd is empty)

Strip the original git history?
  1. Yes — fresh git init, you own the codebase (recommended)
  2. No — keep the original history (you'll inherit their commits)
```

---

## Step 2 — Inspect the Repo (Read-Only Probe)

Before cloning the full repo, fetch metadata + tree to understand what's coming:

```bash
curl -s "https://api.github.com/repos/<org>/<repo>" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(f\"Stars: {d.get('stargazers_count', 0)}\")
print(f\"Lang:  {d.get('language', '?')}\")
print(f\"Size:  {d.get('size', 0)} KB\")
print(f\"License: {(d.get('license') or {}).get('spdx_id', 'none')}\")
print(f\"Topics: {', '.join(d.get('topics', []))}\")
"

curl -s "https://api.github.com/repos/<org>/<repo>/git/trees/<branch>?recursive=1" | python3 -c "
import json, sys
d = json.load(sys.stdin)
files = [t['path'] for t in d.get('tree', []) if t['type'] == 'blob']
print(f'Total files: {len(files)}')
key = [f for f in files if f.lower() in ('readme.md','license','package.json','requirements.txt','main.tf','composer.json','go.mod','cargo.toml','dockerfile')]
for f in key: print(f'  • {f}')
"
```

Show summary so user knows what they're getting.

---

## Step 3 — Detect What's Inside

After clone (Step 5), detect the stack from the cloned files:

```bash
[ -f "$DIR/package.json" ] && cat "$DIR/package.json" | grep -E '"(react|next|vue|angular|fastify|express|nestjs)"' | head -5
[ -f "$DIR/requirements.txt" ] && head -10 "$DIR/requirements.txt"
[ -f "$DIR/main.tf" ] && grep -E 'provider "(aws|google|azurerm|digitalocean)"' "$DIR"/*.tf
[ -f "$DIR/composer.json" ] && head -10 "$DIR/composer.json"
[ -f "$DIR/Dockerfile" ] && grep "^FROM" "$DIR/Dockerfile"
```

Identify the stack tags: `python`, `node`, `react`, `terraform-aws`, `terraform-do`, `kubernetes`, etc.

---

## Step 4 — Show Plan

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLONE PLAN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Source:    https://github.com/<org>/<repo>
Stars:     N | License: MIT | Lang: TypeScript
Size:      <N> KB, <N> files
Target:    ./<folder>/

WILL DO:
  □ git clone <url> <folder>
  □ rm -rf <folder>/.git           (strip history)
  □ cd <folder> && git init        (fresh repo)
  □ Detect stack: <tags>
  □ Generate CLAUDE.md tailored for <stack>
  □ Update .gitignore for <stack>
  □ Generate .vscode/extensions.json (recommends Claude Code + stack extensions)
  □ Initial commit: "chore: initial scaffold from <org>/<repo>"

WILL NOT:
  - Push to any remote (you do that)
  - Install dependencies (you do that — saves time, avoids surprises)
  - Run anything from the cloned repo (Makefile / scripts / etc.)

OPTIONAL: rename variables/namespaces?
  Some skeleton repos have placeholder names (e.g., "myapp", "doproject", "wwwnamespace").
  After clone, I can scan + offer to rename them to fit your project.
  → choose later (Y/n)

Type GO to clone, CANCEL to abort.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for GO.

---

## Step 5 — Execute

```bash
git clone --depth 1 <url> <folder>
cd <folder>
rm -rf .git
git init
git add .
git commit -m "chore: initial scaffold from <org>/<repo>"
```

**For subdirectory clones** (`/tree/branch/path/`):

```bash
# Sparse checkout — only the subdirectory
git clone --depth 1 --filter=blob:none --sparse <url> <folder>
cd <folder>
git sparse-checkout set <path>
# Move the contents of <path> to root
mv <path>/* .
rm -rf <path>
rm -rf .git
git init
```

---

## Step 6 — Detect & Generate CLAUDE.md

Based on detected stack, generate a CLAUDE.md following the patterns in the main `/scaffold` skill (see references in `references/stacks.md`).

Minimal CLAUDE.md template:

```markdown
# <Project Name>

Cloned from: <source-url> (started: YYYY-MM-DD)

## Stack
<detected stack with versions>

## Commands
- Install: <stack-appropriate install command>
- Dev:     <stack-appropriate dev command>
- Test:    <stack-appropriate test command>
- Build:   <stack-appropriate build command>

## What's Here
<short summary of what the cloned repo provides>
<list any major folders the user should know about>

## What to Customize
<placeholders detected in the original repo, if any>
```

---

## Step 7 — Optional Rename Pass

If user agreed, scan for placeholder strings and offer to rename:

```bash
# Common placeholder patterns to scan
grep -rE '(myapp|my-app|MY_APP|mycompany|example\.com|YOUR_|TODO_)' \
  --include="*.tf" --include="*.tfvars" --include="*.json" --include="*.yaml" \
  --include="*.yml" --include="*.md" --include="*.env*" \
  -l | head -20
```

Show findings:

```
Found placeholders in 8 files:
  doproject/docluster.tf      → "doproject" → ?
  certsnamespace/clusterissuer.tf → "example.com" → ?
  variables.tf                → "MY_APP_NAME" → ?
  ...

Want to rename any of these?
  1. Rename "doproject" → ____
  2. Rename "example.com" → ____
  3. Rename "MY_APP_NAME" → ____
  4. Skip — I'll edit manually
```

Use `find` + `sed` (carefully) to do find-replace, but show the diff first.

---

## Step 8 — Final Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ CLONED AND READY

Project:   ./<folder>/
Source:    <url>
Stack:     <detected>
Renamed:   N placeholders (or "none")
History:   stripped, fresh git init

NEXT STEPS:
  cd <folder>
  <install command>
  <dev command>

  Want to install Claude Code skills for this stack?
  → /skill-bootstrap will pick the right ones for you
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

After done, optionally trigger `/skill-bootstrap` since this is now a fresh project ready for tooling.

---

## Notes

- Always use `--depth 1` to avoid pulling years of history we're going to strip anyway
- Always strip `.git` for fresh ownership unless user explicitly wants the history
- Never push, never install dependencies — those are the user's decisions
- Respect the source license — generated CLAUDE.md mentions the source repo for attribution
