---
name: no-roo-on-scaffold-project
description: User is not using Roo Code for the claude-scaffold-skill project — do all work directly
type: feedback
originSessionId: 093c4187-2dda-4c9a-bbc0-989f2dd61d0e
---
Do not suggest Roo prompts or Roo-based parallel workflows for the claude-scaffold-skill project. User tried it and it didn't work well (hallucinated repo names, needed too much hand-holding). Handle all tasks directly in this project.

**Why:** Roo generated fake repo slugs from prompt examples and nearly committed them to the registry.
**How to apply:** On any task for claude-scaffold-skill, just do it directly. Never offer "here's a prompt for Roo to do X."
