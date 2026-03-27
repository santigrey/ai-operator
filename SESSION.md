# SESSION.md â Project Ascension
## Date: 2026-03-27 (Day 26 of 60)
## Engineer: James Sloan | Denver, CO

---

## PROJECT STATE

Project Ascension is running on two parallel tracks that compound each other. Track 1 is a self-hosted production AI platform built on homelab hardware. Track 2 is a complete Anthropic API mastery curriculum built independently in 20 hours. Together they form a single cohesive portfolio that demonstrates both infrastructure depth and API fluency.

---

## TRACK 1 â HOMELAB AI PLATFORM

### Repo: github.com/santigrey/ai-operator

A three-plane distributed AI platform designed to mirror production AI infrastructure at real companies.

### Architecture
- Control Plane: Server 3 (192.168.1.10) â FastAPI orchestrator :8000, PostgreSQL + pgvector, MCP server :8001
- Inference Plane: Server 2 (192.168.1.152) â Ollama, llama3.1:8b, mxbai-embed-large, Tesla T4 GPU
- Operator Layer: Thin Client 1/JesAir (git/Paco/Cowork), Mac mini (CLI/CC), Thin Client 2/Cortez (Cowork/Windows)

### Alexandra â Autonomous AI Agent
- ReAct loop (up to 5 steps), vector memory, full event sourcing
- Tool registry: job_search_jsearch (LinkedIn/Indeed/Glassdoor via JSearch RapidAPI), job_search (Adzuna), web_search (DDG), draft_message (Ollama), ping
- Deduplication guard, JSON bleed guard, clean plain-text answers
- CLI: alexandra "find remote AI Engineer jobs" from Mac mini
- Web dashboard: dark theme, live at http://192.168.1.10:8000/dashboard
- homelab-mcp connected to Claude Desktop on JesAir via SSH stdio (id_ed25519_mcp)
- Cowork autonomously diagnosed and fixed Ollama probe bug using homelab tools

### Agent Network â NEW Day 25
- agent_tasks table: id, created_by, assigned_to, status (pending_approval/approved/rejected), title, payload, result, created_at, updated_at
- messages table: id, from_agent, to_agent, thread_id, content, read, created_at
- 5 new homelab-mcp tools: homelab_create_task, homelab_list_tasks, homelab_update_task, homelab_send_message, homelab_read_messages
- Dashboard Agent Tasks section: displays all tasks, Approve/Reject buttons for pending_approval rows
- FastAPI endpoints: POST /tasks/{task_id}/approve, POST /tasks/{task_id}/reject
- End-to-end verified: Paco creates task via MCP â PostgreSQL â dashboard displays â approve/reject works

### Infrastructure Fixes â Day 24-25
- SSH passphrase removed permanently from id_ed25519 on JesAir
- SSH command limit raised from 500 to 2000 chars in mcp_server.py
- Python bytecode cache cleared to fix stale tool loading
- Portfolio README updated: Server 2/Server 3/Thin Client 1/Thin Client 2 naming, live screenshots

### Phase Status
- Phase I â Agent OS scanner and refresh loop COMPLETE
- Phase II-A â Alexandra core agent loop and CLI COMPLETE
- Phase II-B â Web dashboard COMPLETE
- Phase II-C â Portfolio weaponization COMPLETE
- Phase II-D â Agent Network foundation COMPLETE (Day 25)
- Phase II-E â CC polling loop / autonomous task execution COMPLETE (Day 26)

---

## TRACK 2 â CLAUDE API MASTERY CURRICULUM

### Repo: github.com/santigrey/claude-mastery
### Built: March 24-25, 2026 (~20 hours)

A ground-up Anthropic API curriculum built independently, covering every layer from raw API calls to production agent systems.

### What Was Built
- hello_claude.py â raw API call, metadata, model understanding
- streaming.py â real-time token delivery
- structured_output.py â JSON outputs via system prompt
- conversation_memory.py â multi-turn with history management
- tool_use.py â single and parallel tool calling
- mcp_integration.py â MCP server connection
- react_agent.py â ReAct pattern from scratch
- task_planning_agent.py â multi-step planning
- production_hardening.py â retry logic, error handling, timeouts
- hybrid_inference.py â Claude + local Ollama routing
- eval_harness.py â automated evaluation, 100% pass rate

---

## PENDING ITEMS

1. Phase II-E â CC polling loop: script on Mac mini that checks agent_tasks and executes approved tasks autonomously
2. Dashboard task approval screenshot for portfolio README
3. Apply to right-level remote AI Engineer roles ($120-160k) via Alexandra job search
4. SESSION.md auto-update at session close

---

## NEXT SESSION PROMPT

"Paco â Day 26. Build CC polling loop: script on Mac mini that polls agent_tasks for approved tasks and executes them. This is Phase II-E."

---

## KEY FILES
- MCP server: /home/jes/control-plane/mcp_server.py (Server 3)
- MCP stdio wrapper: /home/jes/control-plane/mcp_stdio.py (Server 3)
- Dashboard: /home/jes/control-plane/orchestrator/ai_operator/dashboard/dashboard.py (Server 3)
- App routes: /home/jes/control-plane/orchestrator/ai_operator/main or app.py (Server 3)
- Alexandra CLI: /Users/jes/bin/alexandra (Mac mini)
- Claude Desktop config: ~/Library/Application Support/Claude/claude_desktop_config.json (JesAir)
- SESSION.md: github.com/santigrey/ai-operator/blob/main/SESSION.md

---


### Day 26 Additions
- cc_poller.py on Mac mini: polls agent_tasks every 60s for approved tasks assigned to cc
- macOS 15 NECP workaround: SSH tunnel via Apple-signed ssh binary (localhost:15432→Server3:5432, localhost:18000→Server3:8000)
- launchd service com.ascension.cc-poller running with KeepAlive, verified end-to-end
- Cowork on Cortez connected to homelab-mcp: id_ed25519_mcp key, Windows OpenSSH, split args fix
- Full agent network verified: Paco creates task → dashboard approve → CC executes → completed → Cowork reads results
- Both thin clients (JesAir + Cortez) now have homelab-mcp access
- Lesson locked in: CC self-correcting prompts own diagnosis+fix tasks autonomously

### NEXT SESSION PROMPT
"Paco — Day 27. Phase III: job search automation. Use Alexandra + agent_tasks to find 5 right-level remote AI Engineer roles ($120-160k), create tasks for each, approve them, CC drafts applications."
*Built by James Sloan Â· Denver, CO Â· 2026*

### Day 26 Additions
- cc_poller.py on Mac mini: polls agent_tasks every 60s, SSH tunnel workaround for macOS 15 NECP, json.dumps fix, rollback fix
- launchd service com.ascension.cc-poller running with KeepAlive
- Phase II-E verified: task created by Paco â approved â CC executes â completed autonomously
- Lesson: CC self-correcting prompts beat manual step-by-step for diagnosis tasks
