# Alexandra — Autonomous AI Companion & Homelab Platform

> A self-hosted, production-grade AI platform with an autonomous agent named Alexandra — built from scratch on bare metal.

---

## What Alexandra Does

- **Daily intelligence brief** — Wakes at 7am, reads Gmail and Google Calendar, generates a personalized brief: agenda, flagged emails, priorities, weather, and open tasks
- **Autonomous task execution** — Polls a task queue continuously; executes approved tasks without human intervention via a Claude Code polling loop
- **Learns from you** — Every approve/reject decision updates a persistent user profile; Alexandra adapts her behavior over time
- **Persistent memory** — All conversations and agent runs stored as vector embeddings in pgvector; semantic search retrieves relevant context at inference time
- **Real-time research** — Fetches live data via `web_fetch` and DuckDuckGo; researches companies, roles, and topics on demand
- **Proactive notifications** — Sends email summaries and SMS alerts via Twilio when tasks complete or need attention
- **Multi-turn chat** — Session-aware conversation history; context window managed across turns
- **Knows who you are** — Persistent user profile tracks identity, goals, preferences, communication style, and long-term context

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        OPERATOR LAYER                               │
│                                                                     │
│   Mac mini (CC builds)    JesAir (git / Paco)    Cortez (cowork)   │
│         └──────────────────────┬────────────────────┘              │
│                                │ HTTP / SSH                         │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────┐
│                    CONTROL PLANE — CiscoKid                         │
│                      192.168.1.10                                   │
│                                                                     │
│   FastAPI orchestrator :8000      MCP server :8001                  │
│   PostgreSQL + pgvector           agent_tasks table                 │
│   Daily brief pipeline            message bus                       │
│   ReAct loop + tool registry      user profile store               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ Ollama API
┌────────────────────────────────┼────────────────────────────────────┐
│                  INFERENCE PLANE — TheBeast                         │
│                      192.168.1.152                                  │
│                                                                     │
│   Ollama                          mxbai-embed-large                 │
│   Tesla T4 GPU                    Open WebUI                        │
└─────────────────────────────────────────────────────────────────────┘

External integrations:
  Claude Haiku 4.5 API  ·  Gmail API  ·  Google Calendar API
  Twilio SMS  ·  DuckDuckGo search  ·  web_fetch
```

---

## Tech Stack

| AI / ML | Infrastructure |
|---|---|
| Claude Haiku 4.5 (reasoning + generation) | Python 3.11 / FastAPI |
| Ollama (local model serving) | PostgreSQL 15 + pgvector |
| pgvector (semantic memory) | Docker / systemd |
| mxbai-embed-large (embeddings) | Ubuntu Server 22.04 |
| ReAct agent pattern | SSH key-based mesh |
| MCP protocol (tool bridge) | launchd + cron |
| SentenceTransformers | macOS Login Item automation |

---

## Agent Network

Alexandra operates as a networked agent system, not a single process.

**Task lifecycle:**

```
Paco (Claude Code) → agent_tasks table → CC polling loop → tool execution → result stored
                              ↑
                     dashboard approve/reject
                              ↑
                     user profile update (feedback loop)
```

**Control plane services:**

| Service | Role |
|---|---|
| FastAPI `:8000` | Orchestrator — `/agent`, `/ask`, `/dashboard`, `/healthz` |
| MCP server `:8001` | Tool bridge — 12 tools exposed over HTTP |
| PostgreSQL | State store — tasks, memory, messages, user profile |
| pgvector | Semantic layer — cosine similarity search over all agent memory |

**MCP tool registry (12 tools):**

`homelab_ssh_run` · `homelab_file_read` · `homelab_memory_search` · `homelab_memory_store` · `homelab_agent_status` · `homelab_create_task` · `homelab_list_tasks` · `homelab_update_task` · `homelab_send_message` · `homelab_read_messages` · `homelab_get_profile` · `homelab_update_profile`

---

## How It Works

**ReAct loop.** Alexandra runs a standard Reason → Act → Observe cycle. Each turn, Claude Haiku receives the current task, the tool registry, and relevant memory retrieved via pgvector similarity search. It emits a tool call or a final answer. The orchestrator executes the tool, appends the result to the context window, and loops. A `seen_calls` guard prevents redundant tool calls within a single run.

**Daily brief pipeline.** A cron trigger fires at 7am. Alexandra calls the Gmail API for unread messages, the Google Calendar API for the day's events, and checks the open task queue. She generates a structured brief — agenda, flagged items, priorities — and delivers it via email and optionally SMS through Twilio. The brief is also stored as a memory entry in pgvector, making it retrievable in future sessions.

**Persistent user profile.** Every interaction is an opportunity to learn. When a user approves or rejects a task, the outcome is written back to a `user_profile` table keyed by category and attribute. Over time this profile captures communication preferences, domain expertise, recurring goals, and behavioral patterns. The profile is injected into every agent context window as a system-level brief.

**Operator tooling.** `agentctl.py` is the CLI layer — it scans the project tree (rooted in iCloud Drive), classifies each project into one of six canonical categories (`AI_Infra`, `Agents`, `Career`, `Venice`, `Playground`, `Notes`), generates delta reports of changed files, and embeds documents into pgvector for cross-session search. A persistent background loop (macOS Login Item) runs `agentctl refresh` every 15 minutes, keeping the operator's view of the platform current.

---

## Portfolio Signal

Building Alexandra required the full stack of an AI platform engineer: designing a distributed three-plane system, integrating LLM APIs into a production service loop, implementing semantic memory with pgvector, wiring external APIs (Gmail, Calendar, Twilio), and operating real hardware under real constraints. This wasn't a tutorial project or a hosted demo — it runs on bare metal, survives reboots, handles concurrency, and learns from live feedback. The architectural decisions (inference plane isolation, MCP as a tool protocol boundary, event-sourced memory, operator/agent separation) reflect the same concerns that appear in production AI infrastructure at scale. It demonstrates that I can design, build, operate, and iterate on an end-to-end AI platform independently — which is exactly the job.

---

## Build Log

| Phase | Days | What Was Built |
|---|---|---|
| **Phase I — Runtime Core** | 1–7 | FastAPI orchestrator, PostgreSQL schema, pgvector integration, tool registry, single-step ReAct loop, `/agent` endpoint |
| **Phase I — Memory & Tools** | 8–14 | Event-sourced memory normalized to `EVENT` envelopes, `/ask` multi-turn endpoint, `seen_calls` deduplication, `/trace/<run_id>` debug endpoint, Phase I frozen at `47c1456` |
| **Phase II-A — MCP Bridge** | 15–20 | MCP server on CiscoKid `:8001`, 12 tools registered, SSH mesh to all homelab nodes, Claude Desktop connected, per-host SSH user support |
| **Phase II-B — Dashboard & Alexandra** | 21–22 | Dark-theme web dashboard (platform badges, agent run history, inline run input), Alexandra CLI on Mac mini, CORS middleware, daily brief pipeline scaffolded |
| **Phase II-C — Integrations** | 23–28 | Gmail API + Google Calendar API wired, Twilio SMS, DuckDuckGo research tool, web_fetch tool, user profile feedback loop |
| **Phase II-D — Operator Layer** | 29–35 | `agentctl.py` project scanner/classifier, delta reports, pgvector document indexing, iCloud-aware refresh loop, job search pipeline integrated |

---

## Running the Operator CLI

```bash
# From repo root
python3 agentctl.py status
python3 agentctl.py refresh --root ~/path/to/projects
python3 agentctl.py search --query "vector database memory"
python3 agentctl.py delta --root ~/path/to/projects
```

## Homelab Topology

| Host | IP | Role |
|---|---|---|
| CiscoKid | 192.168.1.10 | Control plane (FastAPI, PostgreSQL, MCP) |
| TheBeast | 192.168.1.152 | Inference (Ollama, Tesla T4) |
| SlimJim | 192.168.1.40 | General compute |
| KaliPi | 192.168.1.254 | Edge / security tooling |
| Mac mini | 192.168.1.13 | Operator (Alexandra CLI, CC builds) |

---

*Built by James Sloan — AI Systems Engineer*
*Project Ascension · Day 35 of 60*
