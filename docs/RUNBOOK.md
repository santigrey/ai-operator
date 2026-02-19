# AI Operator Runbook

## Verify Platform

On CiscoKid:
- systemctl status orchestrator
- docker ps
- curl http://127.0.0.1:8000/docs
- curl http://192.168.1.152:11434/api/tags

---

## Restart Orchestrator
sudo systemctl restart orchestrator

---

## Check DB
docker ps | grep postgres

---

## Confirm Ollama Reachable
curl http://192.168.1.152:11434/api/tags
