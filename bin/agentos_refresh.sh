#!/bin/zsh

REPO="/Users/jes/AI_Agent_OS"
LOG="$REPO/reports/launchagent.log"
ERR="$REPO/reports/launchagent.run.stderr.log"
LOCK="$REPO/reports/.refresh.lockdir"
TIMEOUT_SECS=600
STALE_SECS=1800
CLOUD_ROOT="/Users/jes/Library/Mobile Documents/com~apple~CloudDocs/AI"
PREFLIGHT_SECS=15

ts() { /bin/date -u "+[%Y-%m-%dT%H:%M:%SZ]"; }
log() { echo "$(ts) $*" >> "$LOG"; }

# --- Lock cleanup on exit ---
_cleanup() {
  [[ -d "$LOCK" ]] && rm -rf "$LOCK"
}
trap '_cleanup' EXIT INT TERM

# --- Stale-lock check ---
if [[ -d "$LOCK" ]]; then
  lock_age=$(( $(/bin/date +%s) - $(/usr/bin/stat -f %m "$LOCK") ))
  if (( lock_age >= STALE_SECS )); then
    log "WARN stale lock removed (age=${lock_age}s): $LOCK"
    rm -rf "$LOCK"
  else
    log "SKIP refresh (lock exists: $LOCK)"
    exit 0
  fi
fi

# --- Acquire lock atomically (mkdir is atomic) ---
if ! mkdir "$LOCK" 2>/dev/null; then
  log "SKIP refresh (lock exists: $LOCK)"
  exit 0
fi
echo $$ > "$LOCK/pid"

log "START refresh"

cd "$REPO" || { log "END refresh (rc=1 cd-failed)"; exit 1; }

# --- Pre-flight: verify iCloud root is accessible (stalls in launchd without GUI session) ---
/bin/ls "$CLOUD_ROOT" >/dev/null 2>&1 &
_ls_pid=$!
( sleep "$PREFLIGHT_SECS"; kill "$_ls_pid" 2>/dev/null ) &
_ls_guard=$!
wait "$_ls_pid" 2>/dev/null
_ls_rc=$?
kill "$_ls_guard" 2>/dev/null
wait "$_ls_guard" 2>/dev/null
if (( _ls_rc != 0 )); then
  log "END refresh (rc=icloud-unavailable)"
  exit 1
fi

PYTHON=/opt/homebrew/bin/python3
CMD=($PYTHON "$REPO/agentctl.py" refresh --root "$CLOUD_ROOT")
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
