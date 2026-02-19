# AI Operator Architecture

## Logical Planes

### Control Plane — CiscoKid (192.168.1.10)
- FastAPI Orchestrator (systemd)
- PostgreSQL
- pgvector
- Docker
- Netdata

Responsibilities:
- Memory
- State
- Orchestration
- Tool execution

Ports:
- 8000 (LAN)
- 5432 (LAN)

---

### Inference Plane — TheBeast (192.168.1.152)
- Tesla T4
- Ollama (11434)
- Open WebUI (8080)

Responsibilities:
- LLM reasoning
- Embeddings
- Model hosting

---

### Edge Plane — SlimJim (192.168.1.40)
- Wire-Pod
- Robotics / automation

---

### Operator Layer
- Cortez (thin client)
- jesair (thin client)
- Mac mini (admin anchor)
- KaliPi (192.168.1.254)
