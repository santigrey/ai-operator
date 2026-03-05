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
| `refresh --root <dir> [--verbose]` | Run inventory + timeline + overview-all + delta in one shot | all four reports |
| `delta --root <dir>` | New/modified/deleted files since last scan | `reports/delta.md` |
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

Two scripts work together:

- **`bin/agentos_agent.sh`** — persistent loop (Login Item), calls `agentos_refresh.sh` every 900s
- **`bin/agentos_refresh.sh`** — the actual refresh: acquires lock, runs pre-flight, calls `agentctl.py refresh`

Key properties of `agentos_refresh.sh`:
- Logs: `reports/launchagent.log` (stdout) and `reports/launchagent.run.stderr.log` (python stderr)
- Lock: `reports/.refresh.lockdir` — atomic `mkdir`-based, always removed on exit via `trap`, stale after 1800s
- Pre-flight: 15s `ls` check on the iCloud root — exits with `rc=icloud-unavailable` if it stalls or fails
- Timeout: 600s via `/usr/bin/timeout` if present, otherwise background pid+watchdog
- Lock ownership: shell script owns entirely; `agentctl.py refresh` has no lock logic
- Verbosity: default output is 3 OK summary lines; pass `--verbose` to `agentctl.py` for `ENTER dir:` logging

### Why Login Item, not LaunchAgent

The LaunchAgent plist (`launchagent/com.sloan.agentos.refresh.plist`) is kept for reference but **does not work** — the macOS iCloud file provider XPC service is unavailable in the launchd session context, causing all filesystem access to the iCloud Drive path to hang or fail with EPERM regardless of TCC/FDA grants. The Login Item runs in the full GUI user session where iCloud is accessible.

### Install

**System Settings → General → Login Items & Extensions → Open at Login → `+`** → select `bin/agentos_agent.sh`

To start immediately: `/Users/jes/AI_Agent_OS/bin/agentos_agent.sh &`
To stop: `pkill -f agentos_agent.sh`

## Delta Report

`reports/delta.md` is generated automatically on every `refresh` and via `agentctl delta --root <dir>`. It compares the current scan against the previous snapshot stored at `data/last_scan.json` (gitignored) and reports:

- **Added** — files present now but not in the last snapshot
- **Modified** — files whose `mtime_epoch` or `bytes` changed
- **Deleted** — files in the last snapshot that no longer exist

The first run after no snapshot exists shows all files as added. Output line format: `+N ~N -N`.

## Reports Directory

All generated reports live in `reports/`. They are regenerated on demand — treat them as build artifacts, not source of truth.
