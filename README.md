# AI Agent OS

Operator tooling for a self-hosted, multi-plane AI platform. This repo manages scanning, classifying, and reporting on a local AI project tree — it is not the AI services themselves.

## Platform Architecture

Three logical planes, running on separate hardware:

| Plane | Purpose | Stack |
|---|---|---|
| **Control** | Orchestration, memory, state | FastAPI, PostgreSQL, pgvector, Docker |
| **Inference** | Model execution | Ollama, NVIDIA GPU, Open WebUI |
| **Edge** | Device integrations | Anki Vector / Wire-Pod, peripherals |

Operator machines (Mac mini, Windows workstation) connect remotely. No core AI services run on operator devices.

## agentctl.py

The single CLI entry point for all operator commands. Run from the repo root:

```bash
python3 agentctl.py <command> [options]
```

| Command | Description | Output |
|---|---|---|
| `status` | Print current state and touch `last_updated` | stdout |
| `scan --root <dir>` | Walk a directory tree and emit a file inventory | `reports/inventory.md` |
| `timeline --root <dir>` | Newest files and hot folders | `reports/timeline.md` |
| `projects --root <dir>` | Per-project file counts and timestamps | `reports/projects.md` |
| `overview --root <dir>` | Projects sorted by start date and latest activity | `reports/overview.md` |
| `overview-all --root <dir>` | Overview across all canonical category folders | `reports/overview_all.md` |
| `refresh --root <dir>` | Run inventory + timeline + overview-all in one shot | all three reports |
| `restructure --root <dir> [--dry-run]` | Generate (or apply) a category-based move plan | `reports/restructure_plan.sh` |

### Project Classification

Projects are assigned to one of six canonical categories: `AI_Infra`, `Agents`, `Career`, `Venice`, `Playground`, `Notes`.

Classification priority:
1. **Name override** — `career`/`training`/`resume` in the folder name always wins
2. **Content-based** — reads `.md` files from the project root and matches keywords
3. **Name-based fallback** — keyword matching on the folder name

## Automated Refresh

`bin/agentos_refresh.sh` runs as a LaunchAgent, calling:

```bash
python3 agentctl.py refresh --root "~/Library/Mobile Documents/com~apple~CloudDocs/AI"
```

Logs: `reports/launchagent.log` / `reports/launchagent.run.stderr.log`
Lock file: `reports/.refresh.lock` (prevents concurrent runs)

## State

`data/agent_state.json` tracks project name, canonical repo, command center host, status, and last updated timestamp. Every command updates `last_updated` on write.

## Reports

All generated reports live in `reports/`. They are regenerated on demand and should be treated as build artifacts.
