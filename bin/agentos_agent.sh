#!/bin/zsh
# Persistent background agent — add to Login Items, not a LaunchAgent.
# Runs agentos_refresh.sh every 900 seconds with the full user session
# context required for iCloud Drive access.

REPO="/Users/jes/AI_Agent_OS"
LOG="$REPO/reports/launchagent.log"
INTERVAL=900

ts() { /bin/date -u "+[%Y-%m-%dT%H:%M:%SZ]"; }

echo "$(ts) AGENT start (pid=$$)" >> "$LOG"

while true; do
    /bin/zsh "$REPO/bin/agentos_refresh.sh"
    sleep "$INTERVAL"
done
