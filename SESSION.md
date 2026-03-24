# SESSION.md — Project Ascension
## Date: 2026-03-24 (Day 23 of 60)

## Completed this session
- JSearch API integrated into Alexandra (RapidAPI — free tier)
  - Real job listings from LinkedIn, Indeed, Glassdoor
  - job_search_jsearch tool added to registry
  - Agent now uses JSearch first, Adzuna as fallback
  - CLI updated to display JSearch results
- Agent query bug fixed — location no longer stuffed into "what" field
- Agent dedup prompt updated — stops after JSearch succeeds
- Pipeline recalibrated — hybrid roles excluded, mid-level focus
  - All identified roles ruled out (too senior, hybrid, or wrong fit)
  - Teradata rejected, Coinbase rejected
  - Prologis applied (Saturday), True Anomaly deprioritized
- Mac mini ~/ai-operator repo cloned and SSH auth fixed (SSH keys)
- JesAir SSH auth fixed — both machines now use SSH keys, no tokens
- homelab-mcp connected to Claude Desktop on JesAir
  - SSH stdio transport via passwordless key (id_ed25519_mcp)
  - mcp_stdio.py wrapper created on CiscoKid
  - All 5 homelab tools live in Claude Desktop and Cowork
- Cowork used homelab tools autonomously — diagnosed and fixed Ollama probe bug
  - Old probe: curl pipe to python json.load — crashed on empty body
  - New probe: direct requests.get to TheBeast — clean and reliable
- Platform status: all green (orchestrator, pgvector, Ollama)

## Platform status
- Orchestrator: up (CiscoKid:8000)
- pgvector: up (592 memory rows)
- Ollama: up (TheBeast) — probe fixed
- MCP server: up (CiscoKid:8001)
- homelab-mcp: connected to Claude Desktop on JesAir
- alexandra CLI: live on Mac mini
- Cowork: live on JesAir (connected to homelab)
- Dashboard: live at http://ciscokid.local:8000/dashboard

## Machine map
- JesAir: git ops, Paco sessions, Claude Desktop + Cowork + homelab-mcp
- Mac mini (ssh macmini): alexandra CLI, CC builds, ~/ai-operator repo
- CiscoKid (ssh ciscokid): orchestrator, pgvector, MCP server
- TheBeast: Ollama inference
- Cortez: Windows — available when at desk

## Job search pipeline (as of Day 23)
- Prologis Senior Applied AI Engineer: applied
- True Anomaly Staff PE AI: applied, deprioritized
- Coinbase Sr Staff SWE AI DevEx: rejected
- Teradata Principal Engineer Agentic AI: rejected
- Target band: mid-level AI Engineer, $120-160k, remote preferred

## Next session — Phase II-C
1. Portfolio weaponization — README, architecture diagram, demo harness
2. Run targeted remote AI Engineer searches with JSearch
3. Apply to right-level roles found
4. SESSION.md and OPERATING-PROCEDURES.md updates
