# AI Operator Architecture

AI Operator is a three-plane, self-hosted AI platform designed to mirror real-world production AI systems with clear separation of concerns, failure isolation, and operational clarity.

---

## Logical Planes

### 1. Control Plane

**Purpose:** Coordination, persistence, and orchestration.

**Components:**
- FastAPI-based Orchestrator (systemd-managed service)
- PostgreSQL (relational storage)
- pgvector (vector similarity search)
- Docker runtime
- Observability (host-level monitoring)

**Responsibilities:**
- Request intake
- Memory storage and retrieval
- Tool execution
- State persistence
- Structured response generation

Design Characteristics:
- CPU-focused
- No GPU dependency
- Deterministic networking
- Explicit service boundaries

---

### 2. Inference Plane

**Purpose:** Dedicated AI inference and model execution.

**Components:**
- NVIDIA GPU (T4-class)
- Ollama (LLM runtime)
- Open WebUI (human-facing interface)

**Responsibilities:**
- Local LLM inference
- Embedding generation
- Model hosting and execution

Design Characteristics:
- Inference isolated from control logic
- LAN-restricted exposure
- Host-level networking for reliability
- GPU persistence validated under load

---

### 3. Edge / Services Plane

**Purpose:** Device integrations and external interfaces.

**Example Workloads:**
- Robotics control (Vector / Wire-Pod)
- Automation services
- Peripheral integrations

Design Characteristics:
- Replaceable without impacting inference or control planes
- Experimental workloads isolated from core logic

---

## Operator Layer

Thin clients connect via secure shell and remote development tools.

- Windows workstation (thin client)
- macOS workstation (thin client)
- Admin workstation
- Diagnostic jump host

No core AI services run on operator devices.

---

## Architectural Principles

- Separation of inference and orchestration
- State externalized from models
- Explicit service ownership
- Failure isolation between planes
- Minimal exposed surface area
- Production-style observability

---

## Why This Matters

This architecture reflects how modern AI platforms are structured:

- Dedicated inference resources
- Independent control plane
- Stateful orchestration layer
- Tool-capable runtime
- Memory outside the model

AI Operator is intentionally designed for extensibility, reliability, and interview-grade technical clarity rather than demo simplicity.
