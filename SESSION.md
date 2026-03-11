# Session Anchor — Project Ascension
## Last Updated 2026-03-10

## Current Status
- Login Item agent: STABLE — 900s interval, clean START→END
- Vector DB: LIVE — 27 project files ingested, HNSW search validated
- MCP Server: LIVE — homelab_mcp running on CiscoKid port 8001 (systemd)
- SSH: passwordless access from Mac mini and Cortez to all nodes

## Completed
- Vector DB layer live and validated
- File ingest pipeline (27 files, 0 errors, mxbai-embed-large)
- SSH config on Mac mini and Cortez — beast, ciscokid, slimjim, kalipi
- MCP server built and deployed as systemd service on CiscoKid port 8001
- Tools: homelab_ssh_run, homelab_memory_search, homelab_memory_store, homelab_file_read, homelab_agent_status

## Pending
- [ ] Wire MCP server into Claude — connect claude.ai to homelab_mcp endpoint
- [ ] Expand ingest to full 203 file set
- [ ] Wire memory.search() into orchestrator agent loop
- [ ] SSH key setup for KaliPi

## Next Step
Connect Claude to the MCP server — wire claude.ai Connectors to http://192.168.1.10:8001/mcp so Claude can call homelab tools directly.

## Operating Notes
- Ollama: 127.0.0.1:11434 on TheBeast — intentional LAN-restriction
- Ingest: ~/ingest_files.py on TheBeast, MAX_CHARS=500
- DB: controlplane @ CiscoKid, user=admin, pass=adminpass
- Embedding model: mxbai-embed-large (1024d)
- Vector table: memory — id, source, content, embedding, embedding_model
- SSH aliases: beast=192.168.1.152, ciscokid=192.168.1.10, slimjim=192.168.1.40, kalipi=192.168.1.254
- Mac mini: 192.168.1.13 — SSH config with all node aliases
- Cortez (Windows): SSH config configured, passwordless access to all nodes
- MCP server: /home/jes/control-plane/mcp_server.py on CiscoKid, FASTMCP_PORT=8001
