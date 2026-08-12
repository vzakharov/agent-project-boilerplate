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
# Parallel, printing only what failed — worth it once the checks are slow
# enough that running them one after another is the wait:
#   exec scripts/run-parallel.sh lint='pnpm lint' typecheck='pnpm typecheck' test='pnpm test:unit'
#
# See CLAUDE.md → Vetting for the contract.

echo "TODO: implement vetting for this project (see CLAUDE.md → Vetting)." >&2
exit 1
