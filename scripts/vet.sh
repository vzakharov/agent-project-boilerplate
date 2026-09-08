#!/bin/bash
# Vet: the fast checks the agent runs before pushing review-ready work.
#
# Wire these up for your stack (lint, type-check, format-check, fast tests).
# Serial:
#   pnpm lint && pnpm typecheck && pnpm test:unit
#   cargo clippy --all-targets -- -D warnings && cargo test
#   ruff check . && mypy . && pytest -q
#   go vet ./... && go test -short ./...
#
# Parallel, printing only what failed (worth it once the serial run is the wait):
#   exec scripts/run-parallel.sh lint='pnpm lint' typecheck='pnpm typecheck' test='pnpm test:unit'
#
# The `check-squash-message.sh` line below is the one check here that is not
# stack-specific, so it must survive the rewrite this file is meant to get: keep
# it when you replace everything around it. It measures the squash proposal
# against the caps `/squash-message` states, and passes quietly on a branch that
# has no proposal yet.
#
# See CLAUDE.md → Vetting for the contract.

set -euo pipefail

"$(dirname "$0")/check-squash-message.sh"

echo "TODO: implement vetting for this project (see CLAUDE.md → Vetting)." >&2
exit 1
