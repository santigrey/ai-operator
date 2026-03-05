#!/usr/bin/env python3

import argparse
import json
import os
import shlex
from datetime import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.join(BASE_DIR, "data", "agent_state.json")
SNAPSHOT_PATH = os.path.join(BASE_DIR, "data", "last_scan.json")
MAX_MD_BYTES = 50 * 1024
DEFAULT_TIMELINE_MAX_ROWS = 300
INDEX_CONTENT_BYTES = 8 * 1024

PG_HOST = "192.168.1.10"
PG_PORT = 5432
PG_USER = "admin"
PG_PASSWORD = "adminpass"
PG_DBNAME = "controlplane"


def load_state():
    if not os.path.exists(STATE_PATH):
        raise FileNotFoundError("State file not found: data/agent_state.json")
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def load_last_scan():
    if not os.path.exists(SNAPSHOT_PATH):
        return None, {}
    with open(SNAPSHOT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("timestamp"), {it["path"]: it for it in data.get("files", [])}


def save_last_scan(items, timestamp, root):
    os.makedirs(os.path.dirname(SNAPSHOT_PATH), exist_ok=True)
    with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
        json.dump({"timestamp": timestamp, "root": os.path.abspath(root), "files": items}, f)


def compute_delta(prev_files, curr_items):
    curr_by_path = {it["path"]: it for it in curr_items}
    prev_paths = set(prev_files.keys())
    curr_paths = set(curr_by_path.keys())
    added = [curr_by_path[p] for p in sorted(curr_paths - prev_paths)]
    deleted = [prev_files[p] for p in sorted(prev_paths - curr_paths)]
    modified = [
        {"path": p, "prev": prev_files[p], "curr": curr_by_path[p]}
        for p in sorted(curr_paths & prev_paths)
        if (curr_by_path[p]["mtime_epoch"] != prev_files[p]["mtime_epoch"]
            or curr_by_path[p]["bytes"] != prev_files[p]["bytes"])
    ]
    return {"added": added, "modified": modified, "deleted": deleted}


def format_delta_markdown(delta, prev_ts, curr_ts, root):
    added = delta["added"]
    modified = delta["modified"]
    deleted = delta["deleted"]

    lines = []
    lines.append("# Delta Report")
    lines.append("")
    lines.append(f"- Root: `{os.path.abspath(root)}`")
    lines.append(f"- Previous snapshot: `{prev_ts or 'none (first run)'}`")
    lines.append(f"- Generated (UTC): `{curr_ts}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| | Count |")
    lines.append("|---|---:|")
    lines.append(f"| Added | {len(added)} |")
    lines.append(f"| Modified | {len(modified)} |")
    lines.append(f"| Deleted | {len(deleted)} |")
    lines.append("")

    lines.append(f"## Added ({len(added)})")
    lines.append("")
    if added:
        lines.append("| Path | Size (bytes) |")
        lines.append("|---|---:|")
        for it in added:
            lines.append(f"| `{it['path']}` | {it['bytes']} |")
    else:
        lines.append("*(none)*")
    lines.append("")

    lines.append(f"## Modified ({len(modified)})")
    lines.append("")
    if modified:
        lines.append("| Path | Bytes | mtime |")
        lines.append("|---|---|---|")
        for it in modified:
            bp, bc = it["prev"]["bytes"], it["curr"]["bytes"]
            mp, mc = it["prev"]["mtime_epoch"], it["curr"]["mtime_epoch"]
            b_str = f"{bp} → {bc}" if bp != bc else str(bc)
            m_str = f"{mp} → {mc}" if mp != mc else str(mc)
            lines.append(f"| `{it['path']}` | {b_str} | {m_str} |")
    else:
        lines.append("*(none)*")
    lines.append("")

    lines.append(f"## Deleted ({len(deleted)})")
    lines.append("")
    if deleted:
        lines.append("| Path | Size (bytes) |")
        lines.append("|---|---:|")
        for it in deleted:
            lines.append(f"| `{it['path']}` | {it['bytes']} |")
    else:
        lines.append("*(none)*")
    lines.append("")

    return "\n".join(lines)


def utc_now_iso():
    # Use timezone-aware UTC to avoid utcnow deprecation warnings in newer Python versions
    try:
        from datetime import UTC  # Python 3.11+
        return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def touch_state_timestamp(state):
    state["last_updated"] = utc_now_iso()
    return state


def log(message: str):
    print(message, flush=True)


def listdir_sorted(path: str, verbose: bool = True):
    if verbose:
        log(f"ENTER dir: {path}")
    return sorted(os.listdir(path))


def cmd_status(_args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    print("=== Agent OS ===")
    print(f"Project: {state.get('project')}")
    print(f"Canonical Repo: {state.get('canonical_repo')}")
    print(f"Command Center: {state.get('command_center')}")
    print(f"Status: {state.get('status')}")
    print(f"Last Updated: {state.get('last_updated')}")
    print("=================")


def should_skip_dir(dirname: str) -> bool:
    return dirname in {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".DS_Store",
        "site-packages",
        ".mypy_cache",
        ".pytest_cache",
        "dist",
        "build",
    }


def walk_repo(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]

        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir = ""

        for fn in sorted(filenames):
            if fn == ".DS_Store":
                continue
            full = os.path.join(dirpath, fn)
            try:
                st = os.stat(full)
                mtime_epoch = int(st.st_mtime)
                if mtime_epoch < 946684800:
                    # Ignore invalid/pre-2000 timestamps to avoid skewed oldest/newest reports.
                    continue
                yield {
                    "path": os.path.join(rel_dir, fn) if rel_dir else fn,
                    "bytes": st.st_size,
                    "mtime_epoch": mtime_epoch,
                }
            except OSError:
                continue


def format_inventory_markdown(items, root: str):
    lines = []
    lines.append("# Inventory Report")
    lines.append("")
    lines.append(f"- Root: `{os.path.abspath(root)}`")
    lines.append(f"- Generated (UTC): `{utc_now_iso()}`")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("| Path | Size (bytes) | Modified (epoch) |")
    lines.append("|---|---:|---:|")

    for it in items:
        lines.append(f"| `{it['path']}` | {it['bytes']} | {it['mtime_epoch']} |")

    lines.append("")
    return "\n".join(lines)


def cmd_scan(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    items = list(walk_repo(root))
    md = format_inventory_markdown(items, root)

    out_path = os.path.join("reports", "inventory.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"OK: wrote {out_path} ({len(items)} files)")


def _folder_bucket(path: str) -> str:
    # Bucket by top-level folder if present, else "(root)"
    parts = [p for p in path.split(os.sep) if p]
    return parts[0] if len(parts) >= 2 else "(root)"


def _read_project_markdown_corpus(project_path: str, verbose: bool = True) -> str:
    chunks = []
    try:
        entries = listdir_sorted(project_path, verbose=verbose)
    except OSError:
        return ""

    for name in entries:
        full = os.path.join(project_path, name)
        if not os.path.isfile(full):
            continue
        if not name.lower().endswith(".md"):
            continue
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as f:
                chunks.append(f.read(MAX_MD_BYTES))
        except OSError:
            continue

    return "\n".join(chunks).lower()


def classify_project_name(name: str):
    lname = name.lower()
    if any(k in lname for k in ("vector", "server", "infra", "ascension")):
        return "AI Infra", "name:vector/server/infra/ascension"
    if any(k in lname for k in ("agent", "operator", "architect")):
        return "Agents", "name:agent/operator/architect"
    if any(k in lname for k in ("career", "training", "resume")):
        return "Career", "name:career/training/resume"
    if "venice" in lname:
        return "Venice", "name:venice"
    if "playground" in lname:
        return "Playgroud", "name:playground"
    return "Notes", "name:default"


def classify_project(project_name: str, project_path: str, verbose: bool = True):
    lname = project_name.lower()
    if any(k in lname for k in ("career", "training", "resume")):
        return "Career", "name:career_override"

    corpus = _read_project_markdown_corpus(project_path, verbose=verbose)

    # Content-based signals take priority over name-based rules.
    for k in ("docker", "kubernetes", "infrastructure", "cluster", "homelab", "server"):
        if k in corpus:
            return "AI Infra", f"content:{k}"
    for k in ("agent", "orchestration", "llm", "rag", "vector database"):
        if k in corpus:
            return "Agents", f"content:{k}"
    if "venice" in corpus:
        return "Venice", "content:venice"
    for k in ("experiment", "playground", "prototype"):
        if k in corpus:
            return "Playgroud", f"content:{k}"

    return classify_project_name(project_name)


CANONICAL_FOLDERS = ["AI_Infra", "Agents", "Career", "Venice", "Playground", "Notes"]


def category_to_folder(category: str) -> str:
    mapping = {
        "AI Infra": "AI_Infra",
        "Agents": "Agents",
        "Career": "Career",
        "Venice": "Venice",
        "Playgroud": "Playground",
        "Playground": "Playground",
        "Notes": "Notes",
    }
    return mapping.get(category, "Notes")


def cmd_restructure(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    root_entries = listdir_sorted(root)
    existing_dirs = {
        name for name in root_entries if os.path.isdir(os.path.join(root, name))
    }
    mkdir_needed = [name for name in CANONICAL_FOLDERS if name not in existing_dirs]

    move_cmds = []
    for entry in root_entries:
        project_path = os.path.join(root, entry)
        if not os.path.isdir(project_path) or should_skip_dir(entry):
            continue
        if entry in CANONICAL_FOLDERS:
            continue

        category, _reason = classify_project(entry, project_path)
        category_folder = category_to_folder(category)
        dst = os.path.join(root, category_folder, entry)
        move_cmds.append(
            f"mv {shlex.quote(project_path)} {shlex.quote(dst)}"
        )

    plan_lines = ["#!/bin/bash", "set -e"]
    for folder in mkdir_needed:
        plan_lines.append(f"mkdir -p {shlex.quote(os.path.join(root, folder))}")
    plan_lines.extend(move_cmds)
    plan_lines.append("")

    plan_path = os.path.join("reports", "restructure_plan.sh")
    with open(plan_path, "w", encoding="utf-8") as f:
        f.write("\n".join(plan_lines))

    if not args.dry_run:
        for folder in mkdir_needed:
            os.makedirs(os.path.join(root, folder), exist_ok=True)
        for cmd in move_cmds:
            os.system(cmd)

    print(f"OK: wrote {plan_path}")
    print(f"Moves: {len(move_cmds)}")


def format_timeline_markdown(items, root: str, max_rows: int):
    # Sort newest -> oldest
    items_sorted = sorted(items, key=lambda x: x["mtime_epoch"], reverse=True)

    hot = Counter()
    for it in items:
        hot[_folder_bucket(it["path"])] += 1

    lines = []
    lines.append("# Timeline Report")
    lines.append("")
    lines.append(f"- Root: `{os.path.abspath(root)}`")
    lines.append(f"- Generated (UTC): `{utc_now_iso()}`")
    lines.append("")

    lines.append("## Top hot folders (by file count)")
    lines.append("")
    lines.append("| Folder | Files |")
    lines.append("|---|---:|")
    for folder, cnt in hot.most_common(20):
        lines.append(f"| `{folder}` | {cnt} |")
    lines.append("")

    lines.append(f"## Newest files (top {max_rows})")
    lines.append("")
    lines.append("| Modified (epoch) | Size (bytes) | Path |")
    lines.append("|---:|---:|---|")
    for it in items_sorted[:max_rows]:
        lines.append(f"| {it['mtime_epoch']} | {it['bytes']} | `{it['path']}` |")
    lines.append("")
    return "\n".join(lines)


def cmd_timeline(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    items = list(walk_repo(root))
    md = format_timeline_markdown(items, root, max_rows=args.max_rows)

    out_path = os.path.join("reports", "timeline.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"OK: wrote {out_path} ({len(items)} files scanned, showing {min(args.max_rows, len(items))})")


def collect_project_stats(root: str, skip_project_names=None, verbose: bool = True):
    projects = []
    skip_names = set(skip_project_names or [])

    for entry in listdir_sorted(root, verbose=verbose):
        project_path = os.path.join(root, entry)
        if not os.path.isdir(project_path) or should_skip_dir(entry):
            continue
        if entry in skip_names:
            continue

        file_count = 0
        oldest = None
        newest = None

        for dirpath, dirnames, filenames in os.walk(project_path):
            dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]
            for fn in filenames:
                if fn == ".DS_Store":
                    continue
                full = os.path.join(dirpath, fn)
                try:
                    st = os.stat(full)
                except OSError:
                    # Skip files that vanish or cannot be stat-ed.
                    continue

                file_count += 1
                mtime = int(st.st_mtime)
                if mtime < 946684800:
                    continue
                if oldest is None or mtime < oldest:
                    oldest = mtime
                if newest is None or mtime > newest:
                    newest = mtime

        category, reason = classify_project(entry, project_path, verbose=verbose)
        projects.append(
            {
                "project": entry,
                "category": category,
                "reason": reason,
                "file_count": file_count,
                "oldest": oldest if oldest is not None else 0,
                "newest": newest if newest is not None else 0,
                "abs_path": os.path.abspath(project_path),
            }
        )

    projects.sort(key=lambda x: x["newest"], reverse=True)
    return projects


def format_projects_markdown(projects):
    lines = []
    lines.append("# Project Summary")
    lines.append("| Project | Category | File Count | Oldest (epoch) | Newest (epoch) |")
    lines.append("|---|---|---:|---:|---:|")

    for p in projects:
        lines.append(
            f"| `{p['project']}` | `{p['category']}` | {p['file_count']} | {p['oldest']} | {p['newest']} |"
        )

    lines.append("")
    return "\n".join(lines)


def format_overview_markdown(projects):
    lines = []
    lines.append("# Project Overview")
    lines.append("")
    lines.append("## Evolution timeline (projects by start date)")
    lines.append("")
    lines.append("| Project | Category | Reason | File Count | Oldest (epoch) | Newest (epoch) | Absolute Path |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for p in sorted(projects, key=lambda x: x["oldest"]):
        lines.append(
            f"| `{p['project']}` | `{p['category']}` | `{p['reason']}` | {p['file_count']} | {p['oldest']} | {p['newest']} | `{p['abs_path']}` |"
        )

    lines.append("")
    lines.append("## Current activity (projects by latest update)")
    lines.append("")
    lines.append("| Project | Category | Reason | File Count | Oldest (epoch) | Newest (epoch) | Absolute Path |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for p in sorted(projects, key=lambda x: x["newest"], reverse=True):
        lines.append(
            f"| `{p['project']}` | `{p['category']}` | `{p['reason']}` | {p['file_count']} | {p['oldest']} | {p['newest']} | `{p['abs_path']}` |"
        )

    lines.append("")
    return "\n".join(lines)


def cmd_projects(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    projects = collect_project_stats(root)
    md = format_projects_markdown(projects)

    out_path = os.path.join("reports", "projects.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"OK: wrote {out_path} ({len(projects)} projects)")


def cmd_overview(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    projects = collect_project_stats(root)
    md = format_overview_markdown(projects)

    out_path = os.path.join("reports", "overview.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"OK: wrote {out_path} ({len(projects)} projects)")


def _format_overview_tables_only(projects):
    lines = []
    lines.append("### Evolution timeline (projects by start date)")
    lines.append("")
    lines.append("| Project | Category | Reason | File Count | Oldest (epoch) | Newest (epoch) | Absolute Path |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for p in sorted(projects, key=lambda x: x["oldest"]):
        lines.append(
            f"| `{p['project']}` | `{p['category']}` | `{p['reason']}` | {p['file_count']} | {p['oldest']} | {p['newest']} | `{p['abs_path']}` |"
        )

    lines.append("")
    lines.append("### Current activity (projects by latest update)")
    lines.append("")
    lines.append("| Project | Category | Reason | File Count | Oldest (epoch) | Newest (epoch) | Absolute Path |")
    lines.append("|---|---|---|---:|---:|---:|---|")
    for p in sorted(projects, key=lambda x: x["newest"], reverse=True):
        lines.append(
            f"| `{p['project']}` | `{p['category']}` | `{p['reason']}` | {p['file_count']} | {p['oldest']} | {p['newest']} | `{p['abs_path']}` |"
        )
    lines.append("")
    return "\n".join(lines)


def build_overview_all_markdown(root: str, verbose: bool = True):
    lines = []
    lines.append("# Project Overview (All Categories)")
    lines.append("")

    categories_written = 0
    total_projects = 0
    for category in CANONICAL_FOLDERS:
        category_path = os.path.join(root, category)
        if not os.path.isdir(category_path):
            continue

        projects = collect_project_stats(category_path, skip_project_names={"Inbox"}, verbose=verbose)
        categories_written += 1
        total_projects += len(projects)

        lines.append(f"## Category: {category}")
        lines.append("")
        lines.append(_format_overview_tables_only(projects))

    return "\n".join(lines), total_projects, categories_written


def cmd_overview_all(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    md, total_projects, categories_written = build_overview_all_markdown(root)

    out_path = os.path.join("reports", "overview_all.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(
        f"OK: wrote {out_path} ({total_projects} projects across {categories_written} categories)"
    )


def cmd_refresh(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    prev_ts, prev_files = load_last_scan()
    curr_ts = utc_now_iso()

    items = list(walk_repo(root))

    inventory_md = format_inventory_markdown(items, root)
    inventory_path = os.path.join("reports", "inventory.md")
    with open(inventory_path, "w", encoding="utf-8") as f:
        f.write(inventory_md)

    timeline_md = format_timeline_markdown(items, root, max_rows=DEFAULT_TIMELINE_MAX_ROWS)
    timeline_path = os.path.join("reports", "timeline.md")
    with open(timeline_path, "w", encoding="utf-8") as f:
        f.write(timeline_md)

    overview_all_md, total_projects, categories_written = build_overview_all_markdown(root, verbose=args.verbose)
    overview_all_path = os.path.join("reports", "overview_all.md")
    with open(overview_all_path, "w", encoding="utf-8") as f:
        f.write(overview_all_md)

    delta = compute_delta(prev_files, items)
    delta_md = format_delta_markdown(delta, prev_ts, curr_ts, root)
    delta_path = os.path.join("reports", "delta.md")
    with open(delta_path, "w", encoding="utf-8") as f:
        f.write(delta_md)

    save_last_scan(items, curr_ts, root)

    print(f"OK: wrote {inventory_path} ({len(items)} files)")
    print(
        f"OK: wrote {timeline_path} ({len(items)} files scanned, showing {min(DEFAULT_TIMELINE_MAX_ROWS, len(items))})"
    )
    print(
        f"OK: wrote {overview_all_path} ({total_projects} projects across {categories_written} categories)"
    )
    print(
        f"OK: wrote {delta_path} (+{len(delta['added'])} ~{len(delta['modified'])} -{len(delta['deleted'])})"
    )


def cmd_delta(args):
    state = load_state()
    state = touch_state_timestamp(state)
    save_state(state)

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    os.makedirs("reports", exist_ok=True)

    prev_ts, prev_files = load_last_scan()
    curr_ts = utc_now_iso()
    items = list(walk_repo(root))

    delta = compute_delta(prev_files, items)
    delta_md = format_delta_markdown(delta, prev_ts, curr_ts, root)
    delta_path = os.path.join("reports", "delta.md")
    with open(delta_path, "w", encoding="utf-8") as f:
        f.write(delta_md)

    save_last_scan(items, curr_ts, root)

    print(
        f"OK: wrote {delta_path} (+{len(delta['added'])} ~{len(delta['modified'])} -{len(delta['deleted'])})"
    )


def _pg_connect():
    import psycopg2
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASSWORD,
        dbname=PG_DBNAME,
    )


def _ensure_schema(conn):
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS agent_os")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agent_os.documents (
                file_path   TEXT PRIMARY KEY,
                category    TEXT,
                project     TEXT,
                content     TEXT,
                embedding   vector(384),
                file_mtime  TIMESTAMPTZ,
                indexed_at  TIMESTAMPTZ DEFAULT now()
            )
        """)
    conn.commit()


def _path_to_category_project(rel_path: str):
    parts = rel_path.replace("\\", "/").split("/")
    category = parts[0] if len(parts) >= 1 else ""
    project = parts[1] if len(parts) >= 2 else ""
    return category, project


def cmd_index(args):
    from sentence_transformers import SentenceTransformer

    root = args.root
    if not os.path.isdir(root):
        raise SystemExit(f"Root does not exist or is not a directory: {root}")

    print("Loading embedding model...", flush=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    items = list(walk_repo(root))
    total = len(items)
    print(f"Indexing {total} files from {os.path.abspath(root)}", flush=True)

    conn = _pg_connect()
    _ensure_schema(conn)

    for i, item in enumerate(items, 1):
        rel_path = item["path"]
        abs_path = os.path.join(root, rel_path)
        category, project = _path_to_category_project(rel_path)

        content = ""
        try:
            with open(abs_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(INDEX_CONTENT_BYTES).replace("\x00", "")
        except OSError:
            pass

        vec = model.encode(content or rel_path).tolist()
        vec_str = "[" + ",".join(str(v) for v in vec) + "]"

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO agent_os.documents
                    (file_path, category, project, content, embedding, file_mtime)
                VALUES (%s, %s, %s, %s, %s::vector, to_timestamp(%s))
                ON CONFLICT (file_path) DO UPDATE SET
                    category   = EXCLUDED.category,
                    project    = EXCLUDED.project,
                    content    = EXCLUDED.content,
                    embedding  = EXCLUDED.embedding,
                    file_mtime = EXCLUDED.file_mtime,
                    indexed_at = now()
            """, (rel_path, category, project, content, vec_str, item["mtime_epoch"]))
        conn.commit()

        print(f"Indexed {i}/{total}: {rel_path}", flush=True)

    conn.close()
    print(f"OK: indexed {total} files into agent_os.documents", flush=True)


def cmd_search(args):
    from sentence_transformers import SentenceTransformer

    print("Loading embedding model...", flush=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    vec = model.encode(args.query).tolist()
    vec_str = "[" + ",".join(str(v) for v in vec) + "]"

    conn = _pg_connect()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT file_path, category, project, file_mtime,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM agent_os.documents
            ORDER BY embedding <=> %s::vector
            LIMIT 5
        """, (vec_str, vec_str))
        rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No results.")
        return

    print(f"\nTop {len(rows)} results for: {args.query!r}\n")
    for rank, (file_path, category, project, file_mtime, similarity) in enumerate(rows, 1):
        print(f"  {rank}. [{similarity:.3f}] {file_path}")
        print(f"       category={category}  project={project}")
    print()


def build_parser():
    p = argparse.ArgumentParser(prog="agentctl", description="Agent OS runner (foundation)")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="Print current state + update last_updated")
    p_status.set_defaults(func=cmd_status)

    p_scan = sub.add_parser("scan", help="Scan a root folder and generate reports/inventory.md")
    p_scan.add_argument("--root", default=".", help="Root folder to scan (default: current dir)")
    p_scan.set_defaults(func=cmd_scan)

    p_timeline = sub.add_parser("timeline", help="Generate reports/timeline.md (newest files + hot folders)")
    p_timeline.add_argument("--root", required=True, help="Root folder to scan")
    p_timeline.add_argument("--max-rows", type=int, default=DEFAULT_TIMELINE_MAX_ROWS, help="Max rows in newest-files table (default: 300)")
    p_timeline.set_defaults(func=cmd_timeline)

    p_projects = sub.add_parser("projects", help="Generate reports/projects.md (top-level project summary)")
    p_projects.add_argument("--root", required=True, help="Root folder containing top-level project folders")
    p_projects.set_defaults(func=cmd_projects)

    p_overview = sub.add_parser("overview", help="Generate reports/overview.md (timeline + current activity)")
    p_overview.add_argument("--root", required=True, help="Root folder containing top-level project folders")
    p_overview.set_defaults(func=cmd_overview)

    p_overview_all = sub.add_parser("overview-all", help="Generate reports/overview_all.md across canonical category folders")
    p_overview_all.add_argument("--root", required=True, help="Canonical AI root containing category folders")
    p_overview_all.set_defaults(func=cmd_overview_all)

    p_refresh = sub.add_parser("refresh", help="Generate inventory, timeline, overview_all, and delta reports")
    p_refresh.add_argument("--root", required=True, help="Canonical AI root containing category folders")
    p_refresh.add_argument("--verbose", action="store_true", help="Verbose traversal logging")
    p_refresh.set_defaults(func=cmd_refresh)

    p_delta = sub.add_parser("delta", help="Generate reports/delta.md (new/modified/deleted since last scan)")
    p_delta.add_argument("--root", required=True, help="Root folder to scan")
    p_delta.set_defaults(func=cmd_delta)

    p_restructure = sub.add_parser("restructure", help="Generate (or apply) category-based project move plan")
    p_restructure.add_argument("--root", required=True, help="Root folder containing top-level project folders")
    p_restructure.add_argument("--dry-run", action="store_true", help="Write plan only, do not move anything")
    p_restructure.set_defaults(func=cmd_restructure)

    p_index = sub.add_parser("index", help="Embed all files and upsert into PostgreSQL agent_os.documents")
    p_index.add_argument("--root", required=True, help="Canonical AI root containing category folders")
    p_index.set_defaults(func=cmd_index)

    p_search = sub.add_parser("search", help="Semantic search across indexed files (top 5)")
    p_search.add_argument("--query", required=True, help="Search query text")
    p_search.set_defaults(func=cmd_search)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
