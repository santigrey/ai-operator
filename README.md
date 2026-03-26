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
│  CiscoKid · 192.168.1.10                                   │
│                                                             │
│  FastAPI Orchestrator  :8000    MCP Server         :8001   │
│  PostgreSQL + pgvector          Event sourcing             │
│  Alexandra agent loop           Tool registry              │
│  Web dashboard                  Memory write-back          │
├─────────────────────────────────────────────────────────────┤
│                     INFERENCE PLANE                         │
│  TheBeast · 192.168.1.152                                  │
│                                                             │
│  Ollama runtime                 llama3.1:8b                │
│  Tesla T4 GPU                   mxbai-embed-large          │
│  Dedicated GPU node             No CPU contention          │
├─────────────────────────────────────────────────────────────┤
│                      OPERATOR LAYER                         │
│  JesAir · Mac mini · Cortez (Windows)                      │
│                                                             │
│  alexandra CLI                  Claude Desktop + Cowork    │
│  Claude Code builds             homelab-mcp connected      │
│  Git operations                 Job search workflow        │
└─────────────────────────────────────────────────────────────┘
```