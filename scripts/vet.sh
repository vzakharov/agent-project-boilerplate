#!/bin/bash
# Vet: the fast checks the agent runs before pushing review-ready work.
#
# ADOPTERS: this file exits non-zero until it runs your project's real checks —
# `exit 1` at the bottom, and it stays there until they are wired in. Exiting 0
# is correct only where there is no stack to check, as in the boilerplate, whose
# prose and shell the call below covers entirely. Over an unchecked stack that
# same exit is a false green: step 1 of `/finalize` passes, its attestation
# records a vet run, and nothing was compiled, linted or tested. A script that
# certifies without checking is worse than no script at all.
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

echo "vet: no stack-specific checks are configured; the checks above are the run." >&2
echo "vet: a project with a stack exits 1 here until its own checks are wired in" >&2
echo "     (see the ADOPTERS note at the top, and CLAUDE.md → Vetting)." >&2
exit 0
