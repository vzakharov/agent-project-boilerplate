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
# The `check-squash-message.sh` line below is not stack-specific: it measures the
# squash proposal against the caps `/squash-message` states, and passes quietly
# when a branch has no proposal. Replacing everything around it is what this file
# is for, so decide that line on its own — dropping it leaves nothing catching a
# proposal edited by hand or outgrown by a later base merge.
#
# See CLAUDE.md → Vetting for the contract.

set -euo pipefail

"$(dirname "$0")/check-squash-message.sh"

echo "TODO: implement vetting for this project (see CLAUDE.md → Vetting)." >&2
exit 1
