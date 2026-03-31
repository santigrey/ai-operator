#!/usr/bin/env python3
"""
homelab_mcp — Project Ascension MCP Server
Runs on CiscoKid (192.168.1.10), port 8001.
"""

import json
import os
import subprocess
import uuid
from typing import Optional

import psycopg2
import requests
import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict

load_dotenv('/home/jes/control-plane/.env')

DB_HOST       = "127.0.0.1"
DB_PORT       = 5432
DB_NAME       = "controlplane"
DB_USER       = "admin"
DB_PASS       = os.getenv('POSTGRES_PASSWORD', 'adminpass')
OLLAMA_URL    = "http://192.168.1.152:11434"
EMBED_MODEL   = "mxbai-embed-large"
SSH_USER      = "jes"
SSH_KEY       = "/home/jes/.ssh/id_ed25519"
ALLOWED_HOSTS = {
    "beast":    "192.168.1.152",
    "ciscokid": "192.168.1.10",
    "slimjim":  "192.168.1.40",
    "kalipi":   "192.168.1.254",
}

mcp = FastMCP("homelab_mcp", host="0.0.0.0")

def db_connect():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)

def get_embedding(text: str) -> list:
    r = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": EMBED_MODEL, "prompt": text[:500]}, timeout=60)
    r.raise_for_status()
    return r.json()["embedding"]

def ssh_run(host: str, command: str, timeout: int = 30) -> dict:
    ip = ALLOWED_HOSTS[host]
    result = subprocess.run(
        ["ssh", "-i", SSH_KEY, "-o", "StrictHostKeyChecking=no", "-o", "ConnectTimeout=10", f"{SSH_USER}@{ip}", command],
        capture_output=True, text=True, timeout=timeout
    )
    return {"host": host, "command": command, "stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "exit_code": result.returncode}

class SSHRunInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    host: str = Field(..., description="Target host: beast, ciscokid, slimjim, or kalipi")
    command: str = Field(..., description="Shell command to run", min_length=1, max_length=500)
    timeout: Optional[int] = Field(default=30, description="Timeout in seconds", ge=1, le=120)

class MemorySearchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    query: str = Field(..., description="Natural language search query", min_length=1, max_length=500)
    top_k: Optional[int] = Field(default=5, description="Number of results", ge=1, le=20)

class MemoryStoreInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    content: str = Field(..., description="Text content to store", min_length=1, max_length=2000)
    source: Optional[str] = Field(default="mcp", description="Source label")

class FileReadInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    host: str = Field(..., description="Target host name")
    path: str = Field(..., description="Absolute file path", min_length=1)

@mcp.tool(name="homelab_ssh_run", annotations={"readOnlyHint": False, "destructiveHint": False})
async def homelab_ssh_run(params: SSHRunInput) -> str:
    """Execute a shell command on a homelab node via SSH. Allowed hosts: beast, ciscokid, slimjim, kalipi."""
    if params.host not in ALLOWED_HOSTS:
        return json.dumps({"error": f"Unknown host '{params.host}'. Allowed: {list(ALLOWED_HOSTS.keys())}"})
    try:
        return json.dumps(ssh_run(params.host, params.command, params.timeout), indent=2)
    except subprocess.TimeoutExpired:
        return json.dumps({"error": f"Timed out after {params.timeout}s"})
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool(name="homelab_memory_search", annotations={"readOnlyHint": True, "destructiveHint": False})
async def homelab_memory_search(params: MemorySearchInput) -> str:
    """Semantic similarity search against pgvector memory table on CiscoKid."""
    try:
        embedding = get_embedding(params.query)
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT source, content, 1-(embedding <=> %s::vector) AS sim FROM memory ORDER BY embedding <=> %s::vector LIMIT %s", (embedding, embedding, params.top_k))
        rows = cur.fetchall()
        cur.close(); conn.close()
        return json.dumps({"query": params.query, "results": [{"rank": i+1, "source": r[0], "content": (r[1] or "")[:200], "similarity": round(float(r[2]), 4)} for i, r in enumerate(rows)]}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool(name="homelab_memory_store", annotations={"readOnlyHint": False, "destructiveHint": False})
async def homelab_memory_store(params: MemoryStoreInput) -> str:
    """Store a new entry in pgvector memory table on CiscoKid."""
    try:
        embedding = get_embedding(params.content)
        conn = db_connect()
        cur = conn.cursor()
        row_id = str(uuid.uuid4())
        cur.execute("INSERT INTO memory (id, source, content, embedding, embedding_model) VALUES (%s, %s, %s, %s::vector, %s)", (row_id, params.source, params.content, embedding, EMBED_MODEL))
        conn.commit(); cur.close(); conn.close()
        return json.dumps({"status": "stored", "id": row_id, "source": params.source})
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool(name="homelab_file_read", annotations={"readOnlyHint": True, "destructiveHint": False})
async def homelab_file_read(params: FileReadInput) -> str:
    """Read a file from any homelab node via SSH."""
    if params.host not in ALLOWED_HOSTS:
        return json.dumps({"error": f"Unknown host '{params.host}'"})
    try:
        result = ssh_run(params.host, f"cat {params.path}")
        if result["exit_code"] != 0:
            return json.dumps({"error": result["stderr"]})
        return json.dumps({"host": params.host, "path": params.path, "content": result["stdout"]}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.tool(name="homelab_agent_status", annotations={"readOnlyHint": True, "destructiveHint": False})
async def homelab_agent_status() -> str:
    """Get current status of Agent OS services: orchestrator, ollama, pgvector."""
    status = {}
    try:
        r = requests.get("http://127.0.0.1:8000/healthz", timeout=5)
        status["orchestrator"] = "up" if r.status_code == 200 else f"degraded ({r.status_code})"
    except Exception:
        status["orchestrator"] = "down"
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM memory")
        status["pgvector"] = f"up — {cur.fetchone()[0]} memory rows"
        cur.close(); conn.close()
    except Exception as e:
        status["pgvector"] = f"error: {e}"
    try:
        result = ssh_run("beast", "curl -s http://127.0.0.1:11434/api/tags | python3 -c \"import sys,json; d=json.load(sys.stdin); print(len(d.get('models',[])), 'models')\"", timeout=10)
        status["ollama"] = result["stdout"] if result["exit_code"] == 0 else f"unreachable: {result['stderr']}"
    except Exception as e:
        status["ollama"] = f"error: {e}"
    return json.dumps(status, indent=2)

if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app(), host="0.0.0.0", port=8001)
