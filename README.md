# Project Ascension — AI Platform Engineering Portfolio

**James Sloan** · Former Senior Software Engineer at Optum (UnitedHealth Group), now building AI infrastructure systems. · Denver, CO · [github.com/santigrey](https://github.com/santigrey)

---

## What This Is

A self-hosted, production-grade AI platform built from scratch on homelab hardware — designed to mirror how real AI infrastructure companies architect their systems. Not a tutorial follow-along. Not a demo. A working platform that runs autonomously, finds real jobs from LinkedIn and Indeed, drafts outreach, and gets better every session.

Built in 24 days during a career transition from enterprise infrastructure engineering into applied AI.

---

## Live Screenshots

**Alexandra Web Dashboard** — platform status, agent history, run-agent interface:

![Alexandra Dashboard](docs/screenshots/dashboard.png)

**Alexandra CLI** — one-step job search returning 10 real results from LinkedIn/Indeed/Glassdoor:

![Alexandra CLI](docs/screenshots/cli.png)

---

## The Platform

Three logical planes running on separate physical hardware — the same separation of concerns you find at companies like Weights & Biases, Modal, and Replicate.

```
┌─────────────────────────────────────────────────────────────┐
│                      CONTROL PLANE                          │
│  Server 3 · 192.168.1.10                                   │
│                                                             │
│  FastAPI Orchestrator  :8000    MCP Server         :8001   │
│  PostgreSQL + pgvector          Event sourcing             │
│  Alexandra agent loop           Tool registry              │
│  Web dashboard                  Memory write-back          │
├─────────────────────────────────────────────────────────────┤
│                     INFERENCE PLANE                         │
│  Server 2 · 192.168.1.152                                  │
│                                                             │
│  Ollama runtime                 llama3.1:8b                │
│  Tesla T4 GPU                   mxbai-embed-large          │
│  Dedicated GPU node             No CPU contention          │
├─────────────────────────────────────────────────────────────┤
│                      OPERATOR LAYER                         │
│  Thin Client 1 · Mac mini · Thin Client 2 (Windows)        │
│                                                             │
│  alexandra CLI                  Claude Desktop + Cowork    │
│  Claude Code builds             homelab-mcp connected      │
│  Git operations                 Job search workflow        │
└─────────────────────────────────────────────────────────────┘
```

**Why this architecture matters:** Inference is isolated from orchestration. State is externalized from models. Tools are registered, not hardcoded. Every agent run is traced with a `run_id`. This is how production AI systems are built.

---

## Alexandra — Autonomous AI Agent

The flagship product. Alexandra is a multi-step autonomous agent that reasons, uses tools, searches for jobs, drafts outreach, and writes results to memory — without human intervention.

### How it works

```
User prompt
    │
    ▼
Embed → pgvector recall (semantic memory)
    │
    ▼
LLM call (llama3.1:8b via Server 2)
    │
    ├── Tool call? ──► Execute → append to history → loop
    │
    └── Final answer? ──► Write to pgvector → return
```

### Tool Registry

| Tool | Source | What it does |
|------|--------|--------------|
| `job_search_jsearch` | JSearch / RapidAPI | Real jobs from LinkedIn, Indeed, Glassdoor |
| `job_search` | Adzuna API | Fallback job search |
| `web_search` | DuckDuckGo | General web research |
| `draft_message` | Ollama | Writes personalized outreach messages |
| `ping` | Internal | Connectivity check |

### Production features

- **ReAct loop** — up to 5 reasoning + action iterations per request
- **Deduplication guard** — MD5 hash of (tool, args) prevents redundant calls
- **JSON bleed guard** — regex scan catches embedded tool calls in final answers
- **Event sourcing** — every step logged to PostgreSQL with `run_id`, `tool`, `args`, `result`
- **Memory write-back** — responses embedded and stored in pgvector for future recall
- **Trace endpoint** — `/trace/{run_id}` returns full chronological event log

### Interfaces

```bash
# CLI — runs on Mac mini, hits Server 3:8000/agent
alexandra "find remote AI Platform Engineer jobs"
alexandra "find remote MLOps Engineer jobs"

# HTTP API
POST http://192.168.1.10:8000/agent
{"prompt": "find remote AI Platform Engineer jobs"}

# Web dashboard
http://192.168.1.10:8000/dashboard
```

---

## Real Results

Alexandra found these roles autonomously in a single agent run (March 2026):

| Role | Company | Salary | Source |
|------|---------|--------|--------|
| Remote Full-Stack AI Engineer: Deploy Production ML | Pavago | $100k–$130k | LinkedIn |
| HPC - AI and ML Platform Engineer | Ford Motor Company | $113k–$191k | LinkedIn |
| Staff AI / MLOps Engineer - Clinical AI | IMO Health | $170k–$250k | Indeed |
| Remote Senior MLOps Engineer: Real-Time ML Pipelines | Quanata | — | LinkedIn |
| Senior AI Engineer, World Foundation Models & Video | NVIDIA | $184k–$288k | LinkedIn |
| Founding AI Systems Engineer (100% Remote) | Close | $140k–$210k | Indeed |

Outreach was drafted and sent to True Anomaly (Staff Platform Engineer AI, $175k–$250k) using the `draft_message` tool — with mission-specific language pulled from autonomous company research.

---

## Web Dashboard

A dark-theme terminal-aesthetic dashboard served directly by the FastAPI orchestrator.

- Live platform status badges (API, PostgreSQL, Ollama, worker)
- Last 10 agent runs with prompts, answers, timestamps and run IDs
- Run Agent input — fires the `/agent` endpoint inline
- Accessible from any device on the LAN

---

## homelab-mcp

A custom MCP (Model Context Protocol) server running on Server 3, exposing homelab tools to any MCP-compatible client — including Claude Desktop, Claude Code, and Cowork.

**Tools exposed:**

| Tool | Description |
|------|-------------|
| `homelab_ssh_run` | Execute shell commands on any homelab node |
| `homelab_file_read` | Read files from any node via SSH |
| `homelab_memory_search` | Semantic search against pgvector memory |
| `homelab_memory_store` | Write new entries to memory |
| `homelab_agent_status` | Health check across all services |

**In practice:** Cowork connected to homelab-mcp and autonomously diagnosed and fixed an Ollama health probe bug — without being asked. It SSHed into Server 2, identified the empty response issue, rewrote the probe, and restarted the service.

---

## Agent OS

An always-running background system that scans, classifies, and reports on the local AI project tree every 15 minutes.

- Indexes 203 files across 10 projects in 6 categories
- Categories: `AI_Infra`, `Agents`, `Career`, `Venice`, `Playground`, `Notes`
- Generates `inventory.md`, `timeline.md`, `overview_all.md`
- Runs as a macOS Login Item — survives reboots, never needs manual restart

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Orchestration | FastAPI, Python 3.11, uvicorn |
| Memory | PostgreSQL 15, pgvector, psycopg3 |
| Inference | Ollama, llama3.1:8b, mxbai-embed-large |
| Agent protocol | Custom ReAct loop, MCP (FastMCP 1.26) |
| Job data | JSearch (RapidAPI), Adzuna API |
| Web search | duckduckgo-search |
| Monitoring | Custom healthz/readyz endpoints, event log |
| Infrastructure | Ubuntu 22.04, systemd, SSH, NVIDIA T4 |
| Operator tooling | Claude Code, Claude Desktop, Cowork |

---

## Related: Claude Mastery Curriculum

**[github.com/santigrey/claude-mastery](https://github.com/santigrey/claude-mastery)**

A companion repo built in parallel — 20 hours covering the Anthropic API from raw SDI calls to production agent systems. Streaming, structured outputs, conversation memory, tool use, parallel tool calling, MCP integration, ReAct pattern from scratch, task planning agents, production hardening, hybrid inference, and eval harnesses with 100% pass rate.

The two repos are complementary: `claude-mastery` demonstrates API fluency and engineering fundamentals. `ai-operator` demonstrates what those fundamentals look like deployed on real infrastructure.

---

## Architectural Principles

These match how production AI platforms are actually built:

- **Inference isolation** — Model execution separated from orchestration logic
- **State externalization** — pgvector and PostgreSQL hold all state; the model holds none
- **Explicit service boundaries** — each plane has one job and fails independently
- **Tool-capable runtime** — agent behavior extended via registered tools, not prompt hacks
- **Full observability** — every request has a `run_id`, every step logged, every trace queryable
- **Production-style health checks** — `/healthz` and `/readyz` endpoints mirror real deployment patterns

---

## Why This Matters

Most people applying for AI engineering roles have called the OpenAI API and built a chatbot. This platform demonstrates:

1. **Systems thinking** — three-plane architecture with deliberate separation of concerns
2. **Infrastructure depth** — systemd services, GPU binding, SSH key management, LAN networking
3. **Agent design** — ReAct loop, tool registry, memory, deduplication, event sourcing
4. **Production mindset** - health checks, trace endpoints, error guards, observability
5. **Operational discipline** — 24 days of daily commits, SESSION.md tracking, SOP documentation
6. **Real output** - the platform found real jobs, drafted real outreach, and sent it

---

*Built by James Sloan · Denver, CO · 2026*
