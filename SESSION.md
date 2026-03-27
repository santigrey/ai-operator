# SESSION.md ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Project Ascension
## Date: 2026-03-27 (Day 30 of 60)
## Engineer: James Sloan | Denver, CO

---

## PROJECT STATE

Project Ascension is running on two parallel tracks that compound each other. Track 1 is a self-hosted production AI platform built on homelab hardware. Track 2 is a complete Anthropic API mastery curriculum built independently in 20 hours. Together they form a single cohesive portfolio that demonstrates both infrastructure depth and API fluency.

---

## TRACK 1 ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ HOMELAB AI PLATFORM

### Repo: github.com/santigrey/ai-operator

A three-plane distributed AI platform designed to mirror production AI infrastructure at real companies.

### Architecture
- Control Plane: Server 3 (192.168.1.10) ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ FastAPI orchestrator :8000, PostgreSQL + pgvector, MCP server :8001
- Inference Plane: Server 2 (192.168.1.152) ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Ollama, llama3.1:8b, mxbai-embed-large, Tesla T4 GPU
- Operator Layer: Thin Client 1/JesAir (git/Paco/Cowork), Mac mini (CLI/CC), Thin Client 2/Cortez (Cowork/Windows)

### Alexandra ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Autonomous AI Agent
- ReAct loop (up to 5 steps), vector memory, full event sourcing
- Tool registry: job_search_jsearch (LinkedIn/Indeed/Glassdoor via JSearch RapidAPI), job_search (Adzuna), web_search (DDG), draft_message (Ollama), ping
- Deduplication guard, JSON bleed guard, clean plain-text answers
- CLI: alexandra "find remote AI Engineer jobs" from Mac mini
- Web dashboard: dark theme, live at http://192.168.1.10:8000/dashboard
- homelab-mcp connected to Claude Desktop on JesAir via SSH stdio (id_ed25519_mcp)
- Cowork autonomously diagnosed and fixed Ollama probe bug using homelab tools

### Agent Network ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ NEW Day 25
- agent_tasks table: id, created_by, assigned_to, status (pending_approval/approved/rejected), title, payload, result, created_at, updated_at
- messages table: id, from_agent, to_agent, thread_id, content, read, created_at
- 5 new homelab-mcp tools: homelab_create_task, homelab_list_tasks, homelab_update_task, homelab_send_message, homelab_read_messages
- Dashboard Agent Tasks section: displays all tasks, Approve/Reject buttons for pending_approval rows
- FastAPI endpoints: POST /tasks/{task_id}/approve, POST /tasks/{task_id}/reject
- End-to-end verified: Paco creates task via MCP ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ PostgreSQL ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ dashboard displays ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ approve/reject works

### Infrastructure Fixes ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Day 24-25
- SSH passphrase removed permanently from id_ed25519 on JesAir
- SSH command limit raised from 500 to 2000 chars in mcp_server.py
- Python bytecode cache cleared to fix stale tool loading
- Portfolio README updated: Server 2/Server 3/Thin Client 1/Thin Client 2 naming, live screenshots

### Phase Status
- Phase I ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Agent OS scanner and refresh loop COMPLETE
- Phase II-A ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Alexandra core agent loop and CLI COMPLETE
- Phase II-B ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Web dashboard COMPLETE
- Phase II-C ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Portfolio weaponization COMPLETE
- Phase II-D ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Agent Network foundation COMPLETE (Day 25)
- Phase II-E ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ CC polling loop / autonomous task execution COMPLETE (Day 26)

---

## TRACK 2 ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ CLAUDE API MASTERY CURRICULUM

### Repo: github.com/santigrey/claude-mastery
### Built: March 24-25, 2026 (~20 hours)

A ground-up Anthropic API curriculum built independently, covering every layer from raw API calls to production agent systems.

### What Was Built
- hello_claude.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ raw API call, metadata, model understanding
- streaming.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ real-time token delivery
- structured_output.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ JSON outputs via system prompt
- conversation_memory.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ multi-turn with history management
- tool_use.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ single and parallel tool calling
- mcp_integration.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ MCP server connection
- react_agent.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ ReAct pattern from scratch
- task_planning_agent.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ multi-step planning
- production_hardening.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ retry logic, error handling, timeouts
- hybrid_inference.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Claude + local Ollama routing
- eval_harness.py ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ automated evaluation, 100% pass rate

---

## PENDING ITEMS

1. Phase II-E ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ CC polling loop: script on Mac mini that checks agent_tasks and executes approved tasks autonomously
2. Dashboard task approval screenshot for portfolio README
3. Apply to right-level remote AI Engineer roles ($120-160k) via Alexandra job search
4. SESSION.md auto-update at session close

---

## NEXT SESSION PROMPT

"Paco ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Day 26. Build CC polling loop: script on Mac mini that polls agent_tasks for approved tasks and executes them. This is Phase II-E."

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
- macOS 15 NECP workaround: SSH tunnel via Apple-signed ssh binary (localhost:15432ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂServer3:5432, localhost:18000ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂServer3:8000)
- launchd service com.ascension.cc-poller running with KeepAlive, verified end-to-end
- Cowork on Cortez connected to homelab-mcp: id_ed25519_mcp key, Windows OpenSSH, split args fix
- Full agent network verified: Paco creates task ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ dashboard approve ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ CC executes ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ completed ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Cowork reads results
- Both thin clients (JesAir + Cortez) now have homelab-mcp access
- Lesson locked in: CC self-correcting prompts own diagnosis+fix tasks autonomously

### NEXT SESSION PROMPT ÃÂÃÂ¢ÃÂÃÂÃÂÃÂ SUPERSEDED

"Paco ÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ Day 27. Phase III: job search automation. Use Alexandra + agent_tasks to find 5 right-level remote AI Engineer roles ($120-160k), create tasks for each, approve them, CC drafts applications."

### Day 26 Late Session
- user_profile table created in PostgreSQL (12 rows: identity, goals, preferences, context)
- homelab_get_profile and homelab_update_profile MCP tools live (12 total tools)
- agent.py modified: loads user_profile at start of every run, prepends to system prompt
- Alexandra answered "who am I and what are we building?" correctly from profile ÃÂÃÂ¢ÃÂÃÂÃÂÃÂ no tools, no prompting
- Alexandra is now a companion with persistent identity context, not just a task executor

### NEXT SESSION PROMPT
"Paco ÃÂÃÂ¢ÃÂÃÂÃÂÃÂ Day 27. Build Alexandra's proactive daily brief: every morning she wakes up, reads the user profile, checks the task queue, searches for relevant news/jobs, and sends a summary. This is Phase IV."

### Day 27
- daily_brief.py on Server 3: reads user_profile, pending tasks, calls Alexandra agent, stores brief in agent_tasks
- Cron job: runs daily at 7am UTC automatically
- Dashboard Daily Brief section: appears at top of dashboard, shows today's brief on load
- Verified: Alexandra generated morning brief from profile data ÃÂ¢ÃÂÃÂ job focus, pending tasks, proactive suggestion
- Alexandra now wakes up daily without being asked

### NEXT SESSION PROMPT
"Paco ÃÂ¢ÃÂÃÂ Day 28. Phase V: wire Gmail and Google Calendar MCP tools into Alexandra so she can read your email and calendar as part of the daily brief and task creation."

### Day 28
- Google Cloud project alexandra-ascension created
- Gmail API + Google Calendar API enabled
- OAuth2 credentials: client alexandra-daily-brief, token saved to Server 3
- google_readers.py: get_recent_emails() + get_todays_calendar() functions
- daily_brief.py updated: reads real Gmail (last 24h) + calendar events into brief
- Verified: brief surfaced real emails (Tomas Stockton reply needed), 0 calendar events
- CC bonus fix: embed query truncation bug causing HTTP 500 on long prompts
- Credentials: /home/jes/control-plane/google_credentials.json + google_token.json on Server 3

### NEXT SESSION PROMPT
"Paco Ã¢ÂÂ Day 29. Phase VI: build Alexandra's feedback loop Ã¢ÂÂ when you approve/reject tasks or act on brief suggestions, she learns your preferences and updates the user_profile automatically."

### Day 29
- feedback column added to agent_tasks
- infer_and_store_preference() function in app.py: fires in background thread on every approve/reject
- Calls Alexandra agent to infer preference from task title + feedback reason
- Upserts inferred preference into user_profile with source=feedback
- Dashboard Approve/Reject buttons now show prompt() dialog for optional reason
- Verified: rejected task with feedback "I prefer not to use LinkedIn" â preferences.linkedin = avoid stored in user_profile
- Alexandra now learns from every decision you make

### NEXT SESSION PROMPT
"Paco â Day 30. Alexandra is now a learning companion. Assess where she stands vs Jarvis and define the next 10 days of build priorities."

### Day 30
- Alexandra brain upgraded from Ollama/llama3.1:8b to Claude Haiku 4.5 via Anthropic API
- anthropic SDK installed on Server 3, ANTHROPIC_API_KEY stored in .env and orchestrator/.env
- claude_chat() function added to agent.py with Ollama fallback if API unavailable
- Verified: Alexandra answered identity question correctly using Claude Haiku 4.5
- Alexandra is now ~50% of Jarvis — foundation complete, intelligence significantly upgraded

### Next 10 Days Build Plan
1. Cross-session conversation memory (pgvector)
2. Proactive push notifications (email/SMS on important events)
3. Autonomous web research tool
4. Natural multi-turn chat interface on dashboard
5. Portfolio documentation sprint (README, architecture diagram, demo)

### NEXT SESSION PROMPT
"Paco — Day 31. Build cross-session memory: Alexandra stores and retrieves past conversation exchanges via pgvector so she remembers what we discussed last week."
*Built by James Sloan ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ· Denver, CO ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ· 2026*

### Day 26 Additions
- cc_poller.py on Mac mini: polls agent_tasks every 60s, SSH tunnel workaround for macOS 15 NECP, json.dumps fix, rollback fix
- launchd service com.ascension.cc-poller running with KeepAlive
- Phase II-E verified: task created by Paco ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ approved ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ CC executes ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ¢ÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂÃÂ completed autonomously
- Lesson: CC self-correcting prompts beat manual step-by-step for diagnosis tasks
