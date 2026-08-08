#!/usr/bin/env bash
# Shared helpers for the merge/CI check scripts
# (scripts/ci-watch-tick.sh, scripts/check-merge.sh).
#
# This file is meant to be SOURCED, not executed — it defines functions and
# does not set shell options (the sourcing script owns `set -euo pipefail`).
#
# Callers must have `REPO_ROOT` in scope and may set `WT_PROG` (defaults to
# "watch-tick") to prefix diagnostic messages with the script's name.

# Resolve the gh repo. gh auto-detects from the git remote, which fails when the
# remote points at a sandboxed proxy URL (e.g. cloud agent VMs). Fall back to
# parsing the `origin` remote ourselves. Sets globals NWO ("owner/repo") and
# REPO_FLAG (array, always `-R owner/repo` — never left empty: expanding an empty
# array with `"${REPO_FLAG[@]}"` under `set -u` is an "unbound variable" error on
# the bash 3.2 that ships with macOS, so callers can rely on it being populated).
wt_resolve_repo() {
  local prog="${WT_PROG:-watch-tick}"
  REPO_FLAG=()
  NWO=""
  if NWO="$(gh repo view --json nameWithOwner --jq '.nameWithOwner' 2>/dev/null)" && [[ -n "$NWO" && "$NWO" != "null" ]]; then
    REPO_FLAG=(-R "$NWO")
    return 0  # gh auto-detected the repo
  fi
  local origin_url
  origin_url="$(git remote get-url origin 2>/dev/null || true)"
  if [[ "$origin_url" =~ github\.com[:/]([^/]+)/([^/]+?)(\.git)?/?$ ]]; then
    NWO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
    REPO_FLAG=(-R "$NWO")
  fi
  if [[ -z "$NWO" ]]; then
    echo "${prog}: cannot determine OWNER/REPO — gh could not detect it and 'origin' is not a github.com remote." >&2
    exit 1
  fi
}

# Sleep for INTERVAL seconds, minus any time already elapsed since the previous
# tick — so a tick fired after the agent spent minutes working doesn't double
# the wait. Reads INTERVAL from the environment (the caller's default).
# Arg 1: the previous tick's ISO-8601 timestamp ("" on the first tick).
wt_smart_sleep() {
  local last_tick_at="${1:-}"
  local now_epoch sleep_secs last_epoch elapsed
  now_epoch="$(date -u +%s)"
  sleep_secs="$INTERVAL"
  if [[ -n "$last_tick_at" ]]; then
    last_epoch="$(date -u -d "$last_tick_at" +%s 2>/dev/null || echo 0)"
    elapsed=$(( now_epoch - last_epoch ))
    if (( elapsed >= INTERVAL )); then
      sleep_secs=0
    else
      sleep_secs=$(( INTERVAL - elapsed ))
    fi
  fi
  if (( sleep_secs > 0 )); then
    sleep "$sleep_secs"
  fi
}

# Remove the state file (used by the `--reset` flag) and exit. Use when the
# agent gave up mid-watch and the next watch needs a clean slate.
# Arg 1: path to the state file.
wt_reset_state() {
  local state_file="$1"
  local prog="${WT_PROG:-watch-tick}"
  if [[ -f "$state_file" ]]; then
    rm "$state_file"
    echo "${prog}: state file removed (${state_file})."
  else
    echo "${prog}: no state file to remove."
  fi
  exit 0
}
