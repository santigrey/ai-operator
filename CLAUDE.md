# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

`AI_Agent_OS` is the management/operator layer for a self-hosted AI platform. It does **not** contain the AI services themselves — it contains tooling to scan, classify, and report on a separate project tree rooted at `~/Library/Mobile Documents/com~apple~CloudDocs/AI`.

The platform follows a three-plane architecture:
- **Control Plane** — FastAPI orchestrator (systemd), PostgreSQL + pgvector, Docker (runs on `CiscoKid` server)
- **Inference Plane** — Ollama + NVIDIA GPU, Open WebUI (runs on dedicated GPU node at `192.168.1.152`)
- **Edge Plane** — Device integrations (Anki Vector / Wire-Pod, peripherals)

Operator machines (Mac mini, Windows workstation) connect remotely — no core AI services run locally.

## agentctl.py — The Main CLI

`agentctl.py` is the single entry point for all operator commands. Run from the repo root:

```bash
python3 agentctl.py <command> [options]
```

### Commands

| Command | Purpose | Output |
|---|---|---|
| `status` | Print state + update `last_updated` | stdout |
| `scan --root <dir>` | Walk a directory tree, emit file inventory | `reports/inventory.md` |
| `timeline --root <dir> [--max-rows N]` | Newest files + hot folders | `reports/timeline.md` |
| `projects --root <dir>` | Per-project file counts and timestamps | `reports/projects.md` |
| `overview --root <dir>` | Projects sorted by start date + latest activity | `reports/overview.md` |
| `overview-all --root <dir>` | Same but across all canonical category folders | `reports/overview_all.md` |
| `refresh --root <dir>` | Run inventory + timeline + overview-all in one shot (with lock) | all three reports |
| `restructure --root <dir> [--dry-run]` | Generate (or apply) category-based `mv` plan | `reports/restructure_plan.sh` |

### State File

`data/agent_state.json` — JSON with `project`, `canonical_repo`, `command_center`, `status`, `last_updated`. Every command touches `last_updated` on write.

## Project Classification

`classify_project()` assigns each project directory to one of six canonical categories: `AI_Infra`, `Agents`, `Career`, `Venice`, `Playground`, `Notes`.

Priority order:
1. **Name override** — `career`/`training`/`resume` in the folder name always wins
2. **Content-based** — reads `.md` files (up to 50 KB each) from the project root and matches keywords
3. **Name-based fallback** — keyword matching on the folder name

## Automated Refresh

`bin/agentos_refresh.sh` is invoked by a LaunchAgent every 900 seconds and at login.

- Logs: `reports/launchagent.log` (stdout) and `reports/launchagent.run.stderr.log` (python stderr)
- Lock: `reports/.refresh.lockdir` — atomic `mkdir`-based, always removed on exit via `trap`, treated as stale after 1800s
- Timeout: 300s via `/usr/bin/timeout` or a background pid+watchdog fallback
- Lock ownership: the shell script owns the lock entirely; `agentctl.py refresh` has no lock logic

### LaunchAgent plist

Canonical plist lives at `launchagent/com.sloan.agentos.refresh.plist`. To install:

```zsh
cp launchagent/com.sloan.agentos.refresh.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.sloan.agentos.refresh.plist
launchctl list | grep agentos   # verify: should show PID and exit 0
```

## Reports Directory

All generated reports live in `reports/`. They are regenerated on demand — treat them as build artifacts, not source of truth.
