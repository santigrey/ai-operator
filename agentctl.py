#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime
from collections import Counter

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


def _folder_bucket(path: str) -> str:
    # Bucket by top-level folder if present, else "(root)"
    parts = [p for p in path.split(os.sep) if p]
    return parts[0] if len(parts) >= 2 else "(root)"


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


def collect_project_stats(root: str):
    projects = []

    for entry in sorted(os.listdir(root)):
        project_path = os.path.join(root, entry)
        if not os.path.isdir(project_path) or should_skip_dir(entry):
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

        # Keep project rows even if currently empty
        projects.append(
            {
                "project": entry,
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
    lines.append("| Project | File Count | Oldest (epoch) | Newest (epoch) |")
    lines.append("|---|---:|---:|---:|")

    for p in projects:
        lines.append(
            f"| `{p['project']}` | {p['file_count']} | {p['oldest']} | {p['newest']} |"
        )

    lines.append("")
    return "\n".join(lines)


def format_overview_markdown(projects):
    lines = []
    lines.append("# Project Overview")
    lines.append("")
    lines.append("## Evolution timeline (projects by start date)")
    lines.append("")
    lines.append("| Project | File Count | Oldest (epoch) | Newest (epoch) | Absolute Path |")
    lines.append("|---|---:|---:|---:|---|")
    for p in sorted(projects, key=lambda x: x["oldest"]):
        lines.append(
            f"| `{p['project']}` | {p['file_count']} | {p['oldest']} | {p['newest']} | `{p['abs_path']}` |"
        )

    lines.append("")
    lines.append("## Current activity (projects by latest update)")
    lines.append("")
    lines.append("| Project | File Count | Oldest (epoch) | Newest (epoch) | Absolute Path |")
    lines.append("|---|---:|---:|---:|---|")
    for p in sorted(projects, key=lambda x: x["newest"], reverse=True):
        lines.append(
            f"| `{p['project']}` | {p['file_count']} | {p['oldest']} | {p['newest']} | `{p['abs_path']}` |"
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
    p_timeline.add_argument("--max-rows", type=int, default=300, help="Max rows in newest-files table (default: 300)")
    p_timeline.set_defaults(func=cmd_timeline)

    p_projects = sub.add_parser("projects", help="Generate reports/projects.md (top-level project summary)")
    p_projects.add_argument("--root", required=True, help="Root folder containing top-level project folders")
    p_projects.set_defaults(func=cmd_projects)

    p_overview = sub.add_parser("overview", help="Generate reports/overview.md (timeline + current activity)")
    p_overview.add_argument("--root", required=True, help="Root folder containing top-level project folders")
    p_overview.set_defaults(func=cmd_overview)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
