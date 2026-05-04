---
name: claude-scaffold-skill-current-state
description: Current build state and pre-public checklist for claude-scaffold-skill repo
type: project
originSessionId: 093c4187-2dda-4c9a-bbc0-989f2dd61d0e
---
Repo is private, under active testing. Do NOT suggest making it public.

**Why:** User wants to test sync-import.py on MBP M3 and test scaffold on a fresh dummy project before going public.

**Current state (as of 2026-05-04):**
- 20 skills total (9 wizards + 11 reference)
- 17 registry entries (7 verified)
- Context sync working: export confirmed on VPS, import to be tested on MBP
- GitHub Actions: sync-registry.yml (weekly) + validate-registry.yml (PR gate)
- .claude-context/ has first real export committed
- .jetro/ added to .gitignore after credentials near-miss

**Pre-public checklist (user's own, not to rush):**
- [ ] Test sync-import.py on MBP M3
- [ ] Test /scaffold on a fresh dummy project
- [ ] Verify no API keys in any file
- [ ] Add GitHub topics: claude-skill claude-code scaffolding context-sync developer-tools
- [ ] Test GitHub Actions manually (workflow_dispatch)

**How to apply:** When user asks about going public or testing, refer to this checklist. Don't push timeline.
