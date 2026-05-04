---
name: picker
description: Redirects to the skill bootstrapper — the full interactive skill installer that detects your stack and recommends skills in tiers
version: 2.0.0
author: veekunth217
tags: [skills, discovery, registry, recommendations, install]
platforms: [claude-code, cursor, codex]
---

# Skill Picker → Bootstrapper

This skill has been superseded by the more powerful **Skill Bootstrapper**.

When this skill is activated, immediately run the full bootstrapper workflow defined in `skills/bootstrap/SKILL.md`.

The bootstrapper does everything the picker did, plus:
- Detects your project stack automatically
- Tiers recommendations: Essentials → Stack Match → Community Picks
- Actually installs skills (not just lists them)
- Reads both `registry/skills.json` and `registry/discovered.json`
- Has a fallback hardcoded list if registry is unavailable

**Do not show this redirect message to the user.** Just start the bootstrapper flow immediately.
