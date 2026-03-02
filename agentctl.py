#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime

STATE_PATH = os.path.join("data", "agent_state.json")


def load_state():
    if not os.path.exists(STATE_PATH):
        raise FileNotFoundError("State file not found: data/agent_state.json")
    with open(STATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def utc_now_iso():
    # Use timezone-aware UTC to avoid utcnow deprecation warnings in newer Python versions
    try:
        from datetime import UTC  # Python 3.11+
        return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        # Fallback: still produce UTC-ish timestamp without raising
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def touch_state_timestamp(state):
    state["last_updated"] = utc_now_iso()
    return state


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
    return dirname in {".git", "__pycache__", ".venv", "node_modules", ".DS_Store"}


def walk_repo(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        # Prune unwanted dirs
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
                yield {
                    "path": os.path.join(rel_dir, fn) if rel_dir else fn,
                    "bytes": st.st_size,
                    "mtime_epoch": int(st.st_mtime),
                }
            except FileNotFoundError:
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


def build_parser():
    p = argparse.ArgumentParser(prog="agentctl", description="Agent OS runner (foundation)")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="Print current state + update last_updated")
    p_status.set_defaults(func=cmd_status)

    p_scan = sub.add_parser("scan", help="Scan a root folder and generate reports/inventory.md")
    p_scan.add_argument("--root", default=".", help="Root folder to scan (default: current dir)")
    p_scan.set_defaults(func=cmd_scan)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
