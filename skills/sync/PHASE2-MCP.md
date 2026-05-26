# Phase 2 — MCP Server for Live Cross-Tool Sync

**Status:** Spec — not implemented yet.
**Companion to:** `scripts/sync-tools.py` (Phase 1, file-based, shipped).

---

## Why this exists

Phase 1 makes you re-run `make sync-tools` after every edit to `.claude-context/MEMORY.md`. That's fine for the "I updated my project context, propagate it" pattern, but it breaks for live use cases:

- You're chatting with Claude Code, it learns a new fact about your project, you switch to Cursor — Cursor doesn't know yet
- A team-mate updates `.claude-context/MEMORY.md` via PR, you pull — your tools still have the old version cached until you re-run push
- You want memory updates from one tool to flow to the others *within the same session*

Phase 2 fixes this with a small MCP server that all your AI tools point at. Edits anywhere → visible everywhere, immediately.

## What MCP gives us

Model Context Protocol is the open spec from Anthropic for AI tools ↔ external context. Adopted by:

| Tool | MCP client support | Notes |
|---|---|---|
| Claude Code | ✅ stable | First-class, configured via `.claude/mcp.json` or settings |
| Cursor | ✅ stable | Configured in Cursor settings → MCP |
| Codex CLI | ✅ stable | Configured in `~/.codex/config.toml` |
| Windsurf | ✅ stable | Configured in Windsurf settings |
| Roo Code | ✅ stable | Configured in Roo settings |
| Cline | ✅ stable | Configured in Cline settings |
| Aider | 🟡 partial | Adding MCP support recently — verify before relying |
| Claude.ai web | ❌ no | Only Anthropic-owned integrations today |

So Phase 2 covers **everywhere except claude.ai web**. The file-based Phase 1 stays as the universal fallback (and as the source of truth — the MCP server reads from and writes to the same `.claude-context/` files).

## Architecture

```
              .claude-context/MEMORY.md  (source of truth, git-committed)
              .claude-context/memory/*.md
                          ↑↓ (read/write)
                          │
            ┌─────────────┴─────────────┐
            │   sync-mcp-server         │   Python stdlib, ~200 LOC
            │   (stdio transport,       │   No external deps
            │    local-only by default) │
            └─────────────┬─────────────┘
                          │ MCP over stdio
       ┌──────┬──────┬────┴────┬───────┬───────┐
       │      │      │         │       │       │
   Claude  Cursor  Codex   Windsurf   Roo   Cline
```

One process per project (auto-spawned per MCP client connection). Each AI tool's MCP config points at the same `scripts/sync-mcp-server.py` rooted at the project directory.

## MCP surface (tools exposed)

The server exposes these MCP tools:

```
memory_read           → returns the current canonical memory block
memory_search(query)  → grep across MEMORY.md + memory/*.md
memory_append(text)   → adds an entry to memory/auto-N.md (numbered)
memory_update(file, text)  → overwrites a specific memory/*.md file
memory_list           → lists every file in .claude-context/memory/
manifest              → returns the same data .claude-context/sync-manifest.json does
```

Read tools are safe (no auth needed). Write tools (`append`, `update`) gate behind a config flag — off by default, opt-in per project.

## Read/write semantics

- **Reads** go straight to disk every time (no caching) — the disk is the source of truth, the AI's MCP client caches as appropriate per the protocol.
- **Writes** are atomic file replaces (write to `.tmp`, rename). On every write, the server fires a fs-watch event and any other connected MCP client gets a `tools/list_changed` ping per the MCP spec, so it re-reads.
- **Conflict resolution** is "last write wins" — same as git's working tree before commit. If two tools write simultaneously, the later wall-clock write replaces the earlier. We can revisit with optimistic-locking later if it becomes a real problem.

## How a user sets it up

Phase 2 ships a new skill `/sync mcp setup` that:

1. Detects which MCP-capable tools are installed locally
2. For each, writes/updates the MCP server entry pointing at `scripts/sync-mcp-server.py` rooted at the current project
3. Shows the user the exact config additions, asks for `GO` before writing (per project tool policy)
4. Confirms each tool can connect by running a tiny `memory_read` ping

```bash
# Manual equivalent:
python scripts/sync-mcp-server.py --print-config claude > .claude/mcp.json
python scripts/sync-mcp-server.py --print-config cursor > ~/.cursor/mcp.json.patch
# etc.
```

## Coexistence with Phase 1

Phase 1 (file adapters via `sync-tools.py push`) stays for:
- Tools without MCP support (Aider partial, anything else that lands)
- People who don't want a background process per project
- Projects where you want the adapters committed (e.g. CLAUDE.md for code review)

Both can run side by side — the MCP server reads/writes the same `.claude-context/` files that `sync-tools.py` reads from, so there's exactly one source of truth either way.

## Open questions before implementing

1. **Per-project vs shared server.** Phase 2 spec assumes per-project (auto-spawned per MCP client). Easier to reason about. Alternative: one long-running server for all projects, identified by working-dir. Defer this — start per-project.
2. **Write authorization.** Should `memory_append`/`memory_update` require an explicit user confirmation in the tool (like Claude Code's tool-use approval), or trust the tool's own gating? Lean: trust the tool. The disk is git-tracked, so anything weird is recoverable.
3. **Schema for memory entries.** Right now we have free-form markdown. Should the MCP server enforce a schema (title, body, tags) for `memory_append`? Lean: no. Markdown is the schema.
4. **claude.ai web.** No MCP, no help today. If Anthropic opens third-party MCP for claude.ai, this server already speaks the right protocol — just add another config target.
5. **Auth on the wire.** stdio transport is local-only by definition, so no auth. If we ever add HTTP/SSE transport for remote scenarios, that needs revisiting.

## Estimated build effort

- `scripts/sync-mcp-server.py` — ~200 LOC Python stdlib (use `mcp` package or write raw JSON-RPC) — **~3 hours**
- `/sync mcp setup` subcommand — config detection + writing per tool — **~2 hours**
- Docs + per-tool setup snippets — **~1 hour**
- End-to-end testing with at least 2 MCP clients — **~2 hours**

**Total: roughly a half-day of focused work.** Pick a day when you can test against your actual installed tool stack.

## Definition of done

- [ ] `scripts/sync-mcp-server.py` runs and serves MCP over stdio
- [ ] Edits to `.claude-context/MEMORY.md` flicker through to a connected Claude Code instance within 1 second
- [ ] Same for Cursor
- [ ] `/sync mcp setup` adds the right config to each detected tool, shows diff, waits for GO
- [ ] README gains a "Phase 2 — live MCP" section under the existing cross-tool bridge
- [ ] Phase 1 (`sync-tools.py push`) still works untouched — they coexist
