---
name: budget
description: Set up free-claude-code proxy — route Claude Code and Roo Code traffic to OpenRouter free tier, Ollama local models, NVIDIA NIM, or DeepSeek to save Anthropic credits on non-critical work
version: 1.0.0
author: veekunth217
tags: [budget, free, proxy, openrouter, ollama, nvidia, nim, deepseek, llm, routing, cost-saving]
platforms: [claude-code, cursor, codex]
---

# Budget Mode — Free LLM Routing for Claude Code

You are a budget-routing specialist. Your job is to set up [free-claude-code](https://github.com/Alishahryar1/free-claude-code) — a local FastAPI proxy that intercepts Claude Code (and Roo Code) traffic and routes it to free or cheap LLM providers, while keeping critical work on the paid Anthropic API.

**RULE: Show the full plan and wait for `GO` before installing anything, modifying VS Code settings, or starting the proxy.**

---

## What This Does

```
Without /budget:
  Claude Code → api.anthropic.com (always paid)
  Roo Code   → api.anthropic.com (always paid)

With /budget:
  Claude Code → localhost:8082 (proxy) → choose route per task
  Roo Code   → localhost:8082 (proxy) → free models for bulk work

  Proxy backends:
    • OpenRouter free tier  (200+ models, just needs an API key)
    • Ollama                (fully offline, local models)
    • NVIDIA NIM            (GLM, Kimi, MiniMax — if you have access)
    • DeepSeek              (cheap, not free, very capable)
    • LM Studio / llama.cpp (advanced, BYO model)
```

The proxy translates between Anthropic's Messages API and each provider's native format — including streaming, tool calls, and thinking blocks where supported.

**Important:** This is a community project, not Anthropic-endorsed. Tool support and context limits vary by backend. Use it for bulk work; keep Claude Code on the official API for architecture decisions and complex debugging.

---

## Step 0 — Check Current State

Silently run:

```bash
# Is the proxy already running?
curl -s -m 2 http://localhost:8082/v1/models 2>/dev/null | head -20 || echo "proxy_not_running"

# Is the repo already cloned somewhere standard?
[ -d ~/free-claude-code ] && echo "PROXY_DIR=~/free-claude-code"
[ -d ~/.local/share/free-claude-code ] && echo "PROXY_DIR=~/.local/share/free-claude-code"

# Required tooling
command -v uv >/dev/null && echo "uv: installed" || echo "uv: not found"
python3 --version 2>/dev/null

# IDE detection
[ -d ~/.vscode/extensions ] && echo "vscode: installed"
[ -d ~/.cursor/extensions ] && echo "cursor: installed"

# Existing Anthropic env vars
env | grep -E '^ANTHROPIC_' || echo "no ANTHROPIC_ env vars set"
```

Show the user:

```
Budget mode check:
  free-claude-code proxy:  [running on :8082 / not running]
  Repo cloned:             [path or not found]
  uv (Python pkg manager): [version or ❌]
  Python:                  [3.x or ❌]
  IDE detected:            [VS Code / Cursor / both]
  Current ANTHROPIC_*:     [shown / none]
```

If proxy is already running, skip to Step 4 (routing config).

---

## Step 1 — Confirm Intent

```
Budget mode routes Claude Code traffic to alternative LLMs via a local proxy.

Trade-offs you should know:
  ✓ Free or near-free for bulk/repetitive work
  ✓ Privacy: with Ollama, data never leaves your machine
  ✗ Tool support varies by backend — some malformed tool calls
  ✗ Thinking blocks not supported on most non-Claude models
  ✗ Context window depends on the chosen model (small for free OpenRouter)

Recommended split once configured:
  Anthropic direct  → architecture decisions, debugging, code review
  Proxy (free/cheap) → boilerplate, file generation, tests, docs

Continue? (y/n)
```

Wait for confirmation before any install steps.

---

## Step 2 — Install free-claude-code (if not already)

```
Where to install the proxy?
  1. ~/free-claude-code (default — easy to find)
  2. ~/.local/share/free-claude-code (XDG-compliant)
  3. Custom path
```

Then run:

```bash
# Install uv if missing (Astral's package manager — required by free-claude-code)
if ! command -v uv >/dev/null; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null || true
fi

# Clone the proxy
git clone https://github.com/Alishahryar1/free-claude-code.git "$PROXY_DIR"
cd "$PROXY_DIR"
cp .env.example .env
```

Print the location of the cloned repo and tell the user we'll edit `.env` next.

---

## Step 3 — Pick Backend + Configure .env

```
Which backend should the proxy route to?

  1. OpenRouter free tier — simplest, no local setup
     → Sign up at openrouter.ai, copy your API key
     → Free tier includes models like:
        meta-llama/llama-3.3-70b (8K ctx)
        google/gemini-2.0-flash-exp (32K ctx)
        deepseek/deepseek-chat-v3 (64K ctx)

  2. Ollama — fully offline, you control the model
     → Requires ollama installed and a model pulled
     → Recommended: ollama pull qwen2.5-coder:7b
     → Smaller machines: ollama pull qwen2.5-coder:1.5b

  3. NVIDIA NIM — if you have NVIDIA developer access
     → Get key at build.nvidia.com
     → Models: GLM, Kimi, MiniMax

  4. DeepSeek — cheap (not free), very capable for code
     → Get key at platform.deepseek.com
     → Recommended for tool-heavy workflows

  5. LM Studio / llama.cpp — advanced, BYO model
```

Based on choice, show what to put in `.env`. For example, OpenRouter:

```bash
# In ~/free-claude-code/.env
PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-...
DEFAULT_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

For Ollama:

```bash
PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=qwen2.5-coder:7b
```

**Ask user to paste their API key** (do not log it). Save to `.env` directly. Confirm `.env` is in `.gitignore` of the proxy repo (it should be by default).

---

## Step 4 — Start the Proxy

```bash
cd "$PROXY_DIR"
uv run uvicorn server:app --host 127.0.0.1 --port 8082
```

**Important:** This is a long-running process. Two options:

```
How do you want to run the proxy?

  1. Foreground (current terminal) — easy to see logs, stops when you close terminal
  2. Background with nohup — keeps running, logs to ~/.local/share/free-claude-code.log
  3. systemd user service — starts on login, robust (Linux only)
  4. launchd (macOS) — starts on login, robust (Mac only)
```

For option 2 (most portable):

```bash
mkdir -p ~/.local/share
nohup uv run uvicorn server:app --host 127.0.0.1 --port 8082 \
  > ~/.local/share/free-claude-code.log 2>&1 &
echo $! > ~/.local/share/free-claude-code.pid
```

Verify it started:

```bash
sleep 2
curl -s http://localhost:8082/v1/models | head -5
```

If success: continue. If failure: print the log tail and ask user to debug.

---

## Step 5 — Configure Claude Code + Roo Code Routing

### For Claude Code CLI

Add to `~/.bashrc` or `~/.zshrc`:

```bash
# Toggle by uncommenting these to route Claude Code through free-claude-code
# export ANTHROPIC_BASE_URL="http://localhost:8082"
# export ANTHROPIC_AUTH_TOKEN="freecc"  # any value, proxy ignores
```

**Or use a wrapper alias** so it's opt-in per session:

```bash
alias claude-budget='ANTHROPIC_BASE_URL=http://localhost:8082 ANTHROPIC_AUTH_TOKEN=freecc claude'
alias claude-paid='unset ANTHROPIC_BASE_URL ANTHROPIC_AUTH_TOKEN; claude'
```

Now `claude-budget` runs through the proxy, `claude` (or `claude-paid`) hits Anthropic directly.

### For VS Code Claude Code Extension

Update `settings.json` (offer to do this automatically):

```json
{
  "claudeCode.environmentVariables": {
    "ANTHROPIC_BASE_URL": "http://localhost:8082",
    "ANTHROPIC_AUTH_TOKEN": "freecc"
  }
}
```

**Caveat:** the extension may still show an Anthropic browser-login screen — that's cosmetic, the actual traffic routes through the proxy.

### For Roo Code / Cline

Roo Code's settings live in the extension's config. Add a new "API Configuration":

```
Provider:        Anthropic
Base URL:        http://localhost:8082
API Key:         freecc
Model:           (whatever the proxy advertises — query :8082/v1/models)
```

The skill walks the user through adding this in the Roo Code settings UI (we can't programmatically modify it on all platforms).

---

## Step 6 — Final Plan + GO

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BUDGET MODE SETUP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Backend:        [OpenRouter free / Ollama / NVIDIA NIM / DeepSeek]
Default model:  [chosen model]
Proxy location: [path]
Run mode:       [foreground / nohup / systemd / launchd]

ROUTING:
  Claude Code CLI:  alias claude-budget added to ~/.bashrc
  VS Code:          settings.json updated
  Roo Code:         manual config printed for you to paste

POLICY:
  Always free:    boilerplate, docs, tests, file generation, simple refactors
  Always paid:    architecture, complex debug, code review, security analysis
  You decide per-task.

NOTHING runs until you type GO.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Wait for GO. Then execute Steps 2-5 in order.

---

## Step 7 — Confirm + How to Use

After install:

```
✓ Budget mode ready.

USE IT:
  claude-budget "scaffold 20 react components for the dashboard"
    → routed through proxy → free model → 0 Anthropic tokens

  claude "audit this auth flow for race conditions"
    → direct Anthropic → high-quality reasoning

  In VS Code: extension automatically uses proxy now.
  Toggle off: comment out ANTHROPIC_BASE_URL in settings.json.

CHECK STATUS:
  curl http://localhost:8082/v1/models   # what's available
  tail -f ~/.local/share/free-claude-code.log   # live traffic

STOP THE PROXY:
  kill $(cat ~/.local/share/free-claude-code.pid)
```

---

## Reference

- Repo: https://github.com/Alishahryar1/free-claude-code
- Proxy supports: OpenRouter, Ollama, NVIDIA NIM, DeepSeek, LM Studio, llama.cpp
- Default port: 8082 (configurable)
- Auth: dummy local token (`ANTHROPIC_AUTH_TOKEN` value ignored by proxy)
- Logs: written by uvicorn — capture with nohup or systemd

## Troubleshooting

| Problem | Fix |
|---|---|
| Proxy won't start | Check `python3 --version` ≥ 3.11; `uv --version`; port 8082 free (`lsof -i :8082`) |
| 400 errors from local models | Increase `--ctx-size` for llama.cpp / LM Studio |
| Tool calls malformed | Switch backend; not all free models support tools well — use Claude direct |
| VS Code still hits Anthropic | Restart the extension after settings.json change |
| Roo Code doesn't see proxy | Check baseUrl includes `http://`; restart Roo |
