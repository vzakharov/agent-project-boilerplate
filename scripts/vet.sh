#!/bin/bash
# Vet: the fast checks the agent runs before pushing review-ready work.
#
# ADOPTERS: this file exits non-zero until it runs your project's real checks —
# `exit 1` at the bottom, and it stays there until they are wired in. Exiting 0
# is correct only where there is no stack to check, as in the boilerplate, whose
# prose, shell and one tested module the calls below cover entirely. Over an
# unchecked stack that same exit is a false green: step 1 of `/finalize` passes,
# its attestation records a vet run, and nothing was compiled, linted or tested.
# A script that certifies without checking is worse than no script at all.
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
# The three lines below are not stack-specific. Replacing everything around them
# is what this file is for, so decide each on its own rather than sweeping it
# away with the stack:
#
#   check-skill-catalog.sh — asserts that every `@`-reference into
#     `.claude/skills/` resolves, and that no unhydrated stub stowed away. A
#     dangling reference fails silently: the agent follows the surviving prose
#     past the step it could not load. Dropping this line puts the check back on
#     the agent's memory, which is where it was when it went unrun.
#   check-squash-message.sh — holds the squash proposal to the rules
#     `/squash-message` states, passing quietly when a branch has no proposal.
#     Dropping it leaves nothing catching a proposal edited by hand or outgrown
#     by a later base merge.
#   test_authorship.py — the export's agent/human labelling, which `/handle`
#     reads to tell its own replies from an operator's. Run by path, never
#     through `unittest discover`: `scripts/` carries no `__init__.py`, and
#     discovery over a namespace package reports `Ran 0 tests ... OK` and exits
#     0 — the false green this file's whole note is about.
#
# See CLAUDE.md → Vetting for the contract.

set -euo pipefail

"$(dirname "$0")/check-skill-catalog.sh"
"$(dirname "$0")/check-squash-message.sh"
"$(dirname "$0")/test_authorship.py"

echo "vet: no stack-specific checks are configured; the checks above are the run." >&2
echo "vet: a project with a stack exits 1 here until its own checks are wired in" >&2
echo "     (see the ADOPTERS note at the top, and CLAUDE.md → Vetting)." >&2
exit 0
