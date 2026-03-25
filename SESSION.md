# SESSION.md — Project Ascension
## Date: 2026-03-25 (Day 24 of 60)
## Engineer: James Sloan | Denver, CO

---

## PROJECT STATE

Project Ascension is running on two parallel tracks that compound each
other. Track 1 is a self-hosted production AI platform built on homelab
hardware. Track 2 is a complete Anthropic API mastery curriculum built
independently in 20 hours. Together they form a single cohesive portfolio
that demonstrates both infrastructure depth and API fluency.

---

## TRACK 1 — HOMELAB AI PLATFORM
### Repo: github.com/santigrey/ai-operator

A three-plane distributed AI platform designed to mirror production
AI infrastructure at real companies.

### Architecture
- Control Plane: CiscoKid (192.168.1.10) — FastAPI orchestrator :8000,
  PostgreSQL + pgvector, MCP server :8001
- Inference Plane: TheBeast (192.168.1.152) — Ollama, llama3.1:8b,
  mxbai-embed-large, Tesla T4 GPU
- Operator Layer: JesAir (git/Paco/Cowork), Mac mini (CLI/CC),
  Cortez (Cowork/Windows)

### Alexandra — Autonomous AI Agent
- ReAct loop (up to 5 steps), vector memory, full event sourcing
- Tool registry: job_search_jsearch (LinkedIn/Indeed/Glassdoor via
  JSearch RapidAPI), job_search (Adzuna), web_search (DDG),
  draft_message (Ollama), ping
- Deduplication guard, JSON bleed guard, clean plain-text answers
- CLI: alexandra "find remote AI Engineer jobs" from Mac mini
- Web dashboard: dark theme, live at http://ciscokid.local:8000/dashboard
- homelab-mcp connected to Claude Desktop on JesAir via SSH stdio
- Cowork autonomously diagnosed and fixed Ollama probe bug using
  homelab tools

### Phase Status
- Phase I  — Agent OS scanner and refresh loop         COMPLETE
- Phase II-A — Alexandra core agent loop and CLI       COMPLETE
- Phase II-B — Web dashboard                           COMPLETE
- Phase II-C — Portfolio weaponization                 IN PROGRESS
- Phase II-D — Scheduled agent team                    PENDING

---

## TRACK 2 — CLAUDE API MASTERY CURRICULUM
### Repo: github.com/santigrey/claude-mastery
### Built: March 24-25, 2026 (~20 hours)

A ground-up Anthropic API curriculum built independently, covering
every layer from raw API calls to production agent systems.

### What Was Built
- hello_claude.py — raw API call, metadata, model understanding
- streaming.py — real-time token delivery
- structured_output.py — JSON outputs via system prompt
