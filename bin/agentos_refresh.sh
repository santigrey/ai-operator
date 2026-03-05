#!/bin/zsh

REPO="/Users/jes/AI_Agent_OS"
LOG="$REPO/reports/launchagent.log"
ERR="$REPO/reports/launchagent.run.stderr.log"
LOCK="$REPO/reports/.refresh.lock"
TIMEOUT_SECS=300
STALE_SECS=1800

ts() { /bin/date -u "+[%Y-%m-%dT%H:%M:%SZ]"; }
log() { echo "$(ts) $*" >> "$LOG"; }

# --- Lock cleanup on exit ---
_cleanup() {
  [[ -f "$LOCK" ]] && rm -f "$LOCK"
}
trap '_cleanup' EXIT INT TERM

# --- Stale-lock check ---
if [[ -f "$LOCK" ]]; then
  lock_age=$(( $(/bin/date +%s) - $(/usr/bin/stat -f %m "$LOCK") ))
  if (( lock_age >= STALE_SECS )); then
    log "WARN stale lock removed (age=${lock_age}s): $LOCK"
    rm -f "$LOCK"
  else
    log "SKIP refresh (lock exists: $LOCK)"
    exit 0
  fi
fi

# --- Acquire lock ---
echo $$ > "$LOCK"

log "START refresh"

cd "$REPO" || { log "END refresh (rc=1 cd-failed)"; exit 1; }

PYTHON=/opt/homebrew/bin/python3
CMD=($PYTHON "$REPO/agentctl.py" refresh --root "/Users/jes/Library/Mobile Documents/com~apple~CloudDocs/AI")
rc=0

if [[ -x /usr/bin/timeout ]]; then
  /usr/bin/timeout "$TIMEOUT_SECS" "${CMD[@]}" >> "$LOG" 2>> "$ERR"
  rc=$?
  if (( rc == 124 )); then
    log "END refresh (rc=timeout)"
    exit 124
  fi
else
  # Portable fallback: background pid + watchdog
  "${CMD[@]}" >> "$LOG" 2>> "$ERR" &
  py_pid=$!

  (
    sleep "$TIMEOUT_SECS"
    if kill -0 "$py_pid" 2>/dev/null; then
      kill -TERM "$py_pid" 2>/dev/null
      sleep 2
      kill -KILL "$py_pid" 2>/dev/null
    fi
  ) &
  watchdog_pid=$!

  wait "$py_pid"
  rc=$?
  # Kill watchdog if python finished in time
  kill "$watchdog_pid" 2>/dev/null
  wait "$watchdog_pid" 2>/dev/null

  if (( rc == 143 || rc == 137 )); then
    log "END refresh (rc=timeout)"
    exit 124
  fi
fi

log "END refresh (rc=$rc)"
exit $rc
