# AI Operator — Phase I (Runtime Core) Freeze

Date: 2026-02-20  
Status: ACTIVE (Phase I in progress, runtime core operational)

## Roadmap Timeline (Graphic)

```mermaid
timeline
    title AI Operator Roadmap (Phase I → II)
    2026-02-19 : Canonical brain repo created (ai-operator)
              : ARCHITECTURE / RUNBOOK / ROADMAP / CONTROL_ROOM added
    2026-02-20 : Control-plane orchestrator hardened (healthz/readyz)
              : Memory normalized EVENT envelopes persisted in Postgres
              : Tool registry (schema validated) + single-step tool execution loop
              : run_id correlation across tool_call/tool_result/response
              : /trace/<run_id> endpoint working
              : Request logging middleware (run_id + timing)
    Next       : Phase I Freeze + Tag
              : Phase II begins (task queue + workers + agent profiles)

## Canonical Anchors

These commit SHAs are the authoritative Phase I runtime reference points.

- ai-operator (canonical brain): `47c1456`
- control-plane-lab (runtime core): `b30201e`  # Observability: request logging middleware with run_id + timing


## Resume in 60 seconds (operator checklist)

1) Verify repos + anchors
- ai-operator tag: phase1-freeze-2026-02-20
- control-plane-lab: use pinned SHA in this doc

2) Control plane health
- Control plane host: CiscoKid (192.168.1.10)
- Orchestrator:
  - curl -sS http://127.0.0.1:8000/readyz
  - curl -sS http://127.0.0.1:8000/docs | head
- Expected: /readyz returns {"status":"ok","details":{"postgres":"ok","ollama":"ok"}}

3) Smoke test agent runtime (tool loop)
- curl -sS http://127.0.0.1:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"prompt":"Return exactly this JSON and nothing else: {\"tool\":\"ping\",\"args\":{\"message\":\"resume_check\"}}"}'

- Expected: response includes tool_used="ping", echo="resume_check", and run_id present.
- Then:
  - curl -sS "http://127.0.0.1:8000/trace/<run_id>" | head -n 120
- Expected trace: tool_call → tool_result → response (3 events), each includes run_id.

4) If anything fails
- sudo journalctl -u orchestrator -n 120 --no-pager
- Verify DATABASE_URL in /home/jes/control-plane/orchestrator/.env matches POSTGRES_PASSWORD in container.
