#!/bin/bash
# SessionStart hook for Claude Code remote sessions.
#
# Remote/web sessions sometimes resume with a stale dependency tree if the
# lockfile advanced since the environment snapshot was built. This hook is
# the place to re-sync dependencies so sessions boot consistent.
#
# Remote-only by design: local dev sessions exit immediately, so running
# `claude` against your working tree won't reinstall on every launch.
#
# TODO (new project): implement dependency install for your stack, e.g.
#   pnpm install --frozen-lockfile     # Node / pnpm
#   poetry install --sync              # Python / poetry
#   cargo fetch                        # Rust
#   go mod download                    # Go
#
# Until the install line is implemented this hook no-ops cleanly.

set -euo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

# TODO: install dependencies for your stack
