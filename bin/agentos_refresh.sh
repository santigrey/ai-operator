#!/bin/zsh
set -euo pipefail

LOG="/Users/jes/AI_Agent_OS/reports/launchagent.log"
ERR="/Users/jes/AI_Agent_OS/reports/launchagent.run.stderr.log"

ts() { /bin/date -u "+[%Y-%m-%dT%H:%M:%SZ]"; }

echo "$(ts) START refresh" >> "$LOG"

# Run and capture stdout+stderr
{
  cd /Users/jes/AI_Agent_OS || exit 1
  /opt/homebrew/bin/python3 /Users/jes/AI_Agent_OS/agentctl.py refresh --root "/Users/jes/Library/Mobile Documents/com~apple~CloudDocs/AI"
} >> "$LOG" 2>> "$ERR"

rc=$?
echo "$(ts) END refresh (rc=$rc)" >> "$LOG"
exit $rc
