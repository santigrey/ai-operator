# Project Ascension

## Overview

**Project Ascension** is a multi-node, self-hosted AI platform designed to demonstrate **production-grade applied AI infrastructure**.  
The system is intentionally decomposed into independent functional planes to mirror how real-world AI platforms are built, secured, and scaled.

The project emphasizes:
- Clear separation of concerns (control, inference, edge)
- GPU-backed local inference with measurable performance
- Minimal, explicit network exposure
- Operational simplicity over orchestration complexity
- Documentation suitable for technical interviews and portfolio review

This is not a demo stack — it is a **deliberately operated platform**.

---

## Node Topology (Logical Roles)

| Server | Role | Primary Responsibility |
|------|------|------------------------|
| **Server 3** | Control Plane | Orchestration, databases, observability |
| **Server 2** | Inference Plane | GPU-backed LLM inference |
| **Server 1** | Edge / Services Plane | Edge workloads, integrations, automation |

Each node can evolve independently without coupling failures across planes.

---

## Server 3 — Control Plane

**Purpose**: Central coordination, persistence, and observability layer.

### Responsibilities
- Container orchestration
- Persistent relational storage
- Vector-enabled memory
- Platform monitoring

### Services
- **Docker Engine** — container runtime
- **PostgreSQL** — relational datastore
- **pgvector** — vector similarity search
- **Netdata** — host and service observability

### Design Characteristics
- CPU-focused (no GPU dependency)
- Stable, predictable networking
- Designed to expand into scheduling, auth, and control APIs

---

## Server 2 — Inference Plane

**Purpose**: High-performance AI inference node optimized for GPU workloads.

### Responsibilities
- Local LLM inference
- Model serving
- Human-facing AI interaction

### Services
- **NVIDIA Driver + CUDA** — GPU acceleration
- **Ollama** — local LLM runtime
- **Open WebUI** — user interface for inference
- **Netdata** — performance monitoring

### Networking Model
- Open WebUI runs on **host networking** for reliability
- Ollama bound to host and **LAN-restricted**
- Avoids Docker bridge routing and firewall edge cases

### Design Characteristics
- GPU persistence enabled
- Verified GPU utilization under load
- Inference isolated from control logic for safety and performance

---

## Server 1 — Edge / Services Plane

**Purpose**: Edge-facing workloads and peripheral integrations.

### Responsibilities
- Edge services
- Device or automation integrations
- Experimental or low-risk workloads

### Example Use Cases
- Robotics or device control
- Voice or assistant edge components
- Automation workflows

### Design Characteristics
- Lightweight and flexible
- Can be iterated or replaced without impacting inference or control planes

---

## Security & Networking Principles

- Default-deny firewall posture
- Explicit port allow-listing
- LAN-restricted inference APIs
- No unnecessary container-to-host routing
- Clear ownership of ports per service

### Exposed Ports

| Port | Service | Scope |
|----|--------|-------|
| 22 | SSH | Administrative access |
| 19999 | Netdata | Monitoring |
| 8080 | Open WebUI | Human-facing UI |
| 11434 | Ollama | LAN only |

---

## Logical Architecture Diagram
┌─────────────────────────┐
│        Users / UI        │
│   Browser / Local LAN    │
└────────────┬────────────┘
│
:8080 │
│
┌────────────▼────────────┐
│     Server 2             │
│   Inference Plane        │
│                          │
│  Open WebUI              │
│        │                 │
│        ▼                 │
│     Ollama (GPU)         │
│                          │
└────────┬────────────────┘
│
Control / Data APIs
│
┌────────▼────────────────┐
│     Server 3             │
│   Control Plane          │
│                          │
│  PostgreSQL + pgvector   │
│  Observability           │
└────────┬────────────────┘
│
Edge Services
│
┌────────▼────────────────┐
│     Server 1             │
│  Edge / Services Plane   │
│                          │
│  Devices / Automation    │
└─────────────────────────┘

---

## Why This Architecture Matters

This platform mirrors real production AI systems:

- **Inference is isolated** for performance and blast-radius control
- **Control plane scales independently** of model workloads
- **Edge services remain flexible** and low-risk
- Operational complexity is minimized without sacrificing capability

It demonstrates senior-level thinking around:
- System boundaries
- Failure isolation
- Security posture
- Operational trade-offs

---

## Next Phase (Planned)

- Formalize inter-node APIs
- Introduce workload scheduling and job routing
- Expand vector-backed memory usage
- Add production-style diagrams and operational runbooks
- Identify the highest-value demo or monetizable feature

---

**Status**: Baseline complete. Platform stable and operational.


