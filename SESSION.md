# Session Anchor — Project Ascension
## Last Updated 2026-03-10

## Current Status
- Login Item agent: STABLE — 900s interval, clean START→END
- Reports generating: inventory.md, timeline.md, overview_all.md, delta.md
- 27 project files ingested into pgvector memory table — search returning real content
- Vector DB layer: FULLY OPERATIONAL
- SSH config: permanent aliases for beast, ciscokid, slimjim on Mac mini

## Completed
- Vector DB layer live and validated
- File ingest pipeline built and executed (27 files, 0 errors)
- SSH config created on Mac mini — passwordless access to all nodes
- iCloud docs pushed to repo — full architecture context in GitHub permanently
- Search test validated — real content, meaningful similarity scores

## Pending
- [ ] MCP server wrapper for agentctl — bridge for autonomous Claude access
- [ ] Expand ingest to full 203 file set from all projects
- [ ] Wire memory.search() into orchestrator agent loop
- [ ] SSH key setup for CiscoKid and SlimJim (same as beast)

## Next Step
Build MCP server wrapper — this is the bridge that gives Claude autonomous access to all homelab nodes.

## Operating Notes
- Ollama: bound to 127.0.0.1:11434 on TheBeast — intentional security design
- Ingest script: ~/ingest_files.py on TheBeast — MAX_CHARS=500 (mxbai context limit)
- DB: controlplane @ CiscoKid (192.168.1.10), user=admin, pass=adminpass
- Embedding model: mxbai-embed-large (1024d)
- Vector table: memory — id, source, content, embedding, embedding_model
- SSH aliases: beast=192.168.1.152, ciscokid=192.168.1.10, slimjim=192.168.1.254
- Mac mini: 192.168.1.13, user=jes
- KaliPi: 192.168.1.254
