#!/usr/bin/env python3

import json
import os
from datetime import datetime

STATE_PATH = os.path.join("data", "agent_state.json")


def load_state():
    if not os.path.exists(STATE_PATH):
        raise FileNotFoundError("State file not found.")
    with open(STATE_PATH, "r") as f:
        return json.load(f)


def main():
    state = load_state()
    print("=== Agent OS ===")
    print(f"Project: {state['project']}")
    print(f"Canonical Repo: {state['canonical_repo']}")
    print(f"Command Center: {state['command_center']}")
    print(f"Status: {state['status']}")
    print(f"Last Updated: {state['last_updated']}")
    print("=================")


if __name__ == "__main__":
    main()
