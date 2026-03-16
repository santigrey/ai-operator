# SESSION.md — Project Ascension
## Date: 2026-03-16 (Day 22 of 60)

## Completed this session
- True Anomaly outreach sent to Logan Tunget (Sr. Technical Recruiter) via LinkedIn
- SSH keys configured on JesAir for passwordless access to CiscoKid and Mac mini
- GitHub auth fixed on JesAir (PAT configured, credential helper set)
- job-search folder moved from Cortez OneDrive to GitHub repo — now accessible from all devices
- Machine map locked: JesAir=git/paco, Mac mini=alexandra CLI/CC, Cortez=Cowork
- Agent deduplication fix — seen_calls guard prevents redundant tool calls
- Agent now runs job_search exactly once per session (verified)
- 2 HirexHire LLM Ops Engineer roles added to pipeline ($133k, $172k)
- Phase II-B COMPLETE — Alexandra web dashboard live at http://ciscokid.local:8000/dashboard
  - Dark theme terminal aesthetic
  - Platform status badges (api, postgres, ollama, worker)
  - Recent runs display (10 agent runs with prompts + answers)
  - Run Agent input box — fires /agent endpoint inline
  - CORS middleware added to orchestrator
  - JS fix applied (quote bug in loadStatus)
- Dashboard accessible from JesAir via Safari at http://192.168.1.10:8000/dashboard
- ciscokid.local hostname added to /etc/hosts on JesAir

## Platform status
- Orchestrator: up (CiscoKid:8000, 0.0.0.0)
- pgvector: up
- Ollama: up (TheBeast)
- MCP server: up (CiscoKid:8001)
- homelab-mcp: up
- alexandra CLI: live on Mac mini
- Cowork: live on Cortez
- Dashboard: live at http://ciscokid.local:8000/dashboard

## Job search pipeline (as of Day 22)
- 15 roles tracked in job-search/applications.csv
- True Anomaly Staff PE AI: APPLIED (outreach sent to Logan Tunget)
- HirexHire LLM Ops Engineer x2: identified ($172k priority)
- Coinbase Sr Staff SWE AI DevEx: application walked through
- Prologis Senior Applied AI Engineer: identified
- Teradata Principal Engineer Agentic AI: identified

## Machine map
- JesAir: git operations, Paco sessions, browser
- Mac mini (ssh macmini): alexandra CLI, CC builds, homelab dev
- CiscoKid (ssh ciscokid): orchestrator, pgvector, MCP server
- TheBeast: Ollama inference (via CiscoKid)
- Cortez: Cowork, Windows-only tasks

## Next session — Phase II-C
1. Agent team — outreach agent runs on schedule, not on demand
2. Portfolio weaponization — README, architecture diagram, demo harness
3. Follow up on True Anomaly if no response in 5 days
4. Apply to HirexHire $172k LLM Ops role
