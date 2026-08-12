# Adopt the donor's parallel check runner as `scripts/run-parallel.sh`

## What the donor has

`Playgramai/playgramapp` ships `scripts/run-parallel.py` (134 lines, stdlib-only Python 3) and calls it from three `package.json` scripts — `vet`, `fix`, and `ci:lint` — each handing it a list of pnpm script names:

```
vet = pnpm typegen && scripts/run-parallel.py typecheck format:fix lint:fix lint:fsd … test
```

Four behaviors make it worth adopting, all of them stack-independent:

1. **Fan out, then report once.** Every check runs concurrently; output is buffered per-check and printed *only* for the ones that failed, each line prefixed `[<name>]`. A green run prints `All passed.` and nothing else.
2. **Liveness while it waits.** Every 10s it prints which checks are still running, with elapsed seconds — so a long run is distinguishable from a hung one.
3. **Autofix detection.** It snapshots `git status --porcelain` before and after. If the run dirtied a previously-clean tree, it lists exactly which files changed, because autofix steps (`prettier --write`, `eslint --fix`) *pass* while rewriting files, and the easy mistake is committing without them and watching CI's check-only counterpart fail.
4. **Noise suppression.** Lines containing `✓` are dropped from failure output — passing-test lines from the runner that happened to be in the same log.

One thing does **not** transfer: it hardcodes `["pnpm", script]`, so it only ever runs pnpm scripts. A boilerplate that makes no stack assumption needs it to take commands.

## Why port it to shell rather than copy the Python

`scripts/vet.sh` is the most load-bearing entrypoint in the repo — `/finalize`, `/sync-branch` and `/watch-ci` all call it, and the catalog names it a non-optional member of G2. A parallel runner is only useful *inside* `vet.sh`, so adopting the Python file as-is would make `python3` a hard dependency of the core PR loop for every adopter, including Rust, Go and Node repos that have no other reason to have it.

The repo does already ship two Python scripts — `scripts/export-github-issue.py` and `scripts/pr-body.py` — but both sit on escapable paths (`/qa-checklist` in G2, `/issue` in G3) and the catalog records `python3 ≥3.9` per row precisely so an adopter can decline them. Vet is not escapable in the same way, so keeping it interpreter-free genuinely lowers the floor rather than moving a dependency around.

The port is also cheap in a way it wouldn't be for most Python scripts: the donor buffers output in memory and needs threads to do it, whereas shell gets buffering for free by redirecting each child to its own file. There are no arrays, no regex, no string formatting — the whole thing is fork, poll, `cat`.

**Target: `#!/bin/sh`, POSIX, no bashisms.** The repo's other shell scripts are `bash` because they need arrays and `[[ =~ ]]` (`scripts/lib/watch-tick-common.sh` is careful about macOS bash 3.2). This one needs neither, and `/bin/sh` exists in minimal containers where `bash` may not.

## Design

### Interface

```sh
scripts/run-parallel.sh <label=command> [<label=command> ...]
```

Each argument is one check. An argument containing `=` splits at the **first** `=`: left is the display label, right is the command, run via `sh -c`. An argument with no `=` is a bare command and labels itself.

```sh
scripts/run-parallel.sh lint='pnpm lint' typecheck='pnpm typecheck' test='pnpm test:unit'
scripts/run-parallel.sh 'cargo clippy --all-targets -- -D warnings' 'cargo test'
```

Splitting at the first `=` means a command with a leading environment assignment works when labelled (`test='CI=1 pnpm test'`) and misparses when bare (`CI=1 pnpm test` reads as label `CI`). That is a documented sharp edge, not a bug to engineer around — the usage that matters (`vet.sh`) labels everything.

A label containing anything outside `[A-Za-z0-9_.:-]` is a hard error naming the offending argument, since it is almost always an unquoted command rather than a label.

Exit status: `0` if every check passed, `1` if any failed or the arguments were unusable.

### Execution

Per check `i`, with label `L`:

```sh
( sh -c "$cmd" >"$dir/$L.log" 2>&1; echo $? >"$dir/$L.status.tmp"; mv "$dir/$L.status.tmp" "$dir/$L.status" ) &
```

The write-then-rename makes the status file's *existence* mean "complete", so the poller can never read a half-written code.

Rather than the donor's worker-plus-progress threads, the main process polls: `sleep 1`, count the `.status` files, print a `still running:` line every 10th second, break when all are present, then `wait` each recorded PID to reap. No background ticker means no trap, no orphan process, and no chance of leaking a `sleep` loop past the script's exit.

Logs live in `tmp/run-parallel/` per CLAUDE.md ("dev artifacts go under gitignored `tmp/`") — no new `.gitignore` entry. The directory is removed and recreated at startup so a stale log can never be mistaken for this run's. Two concurrent invocations would therefore fight over it; that is out of scope, and the header says so.

### Reporting

- **All passed** → `All passed.` and exit 0.
- **Any failed** → for each failing check, its log with every line prefixed `[L] `, `✓` lines filtered out, then a `Failed: a, b` summary line.
- Each failing check's line block ends with the full log path. That is the escape hatch for the `✓` filter: the console view is condensed, the file on disk is verbatim, so no flag is needed to see what was dropped.
- Autofix detection carries over as-is: capture `git status --porcelain` before and after, and if a previously-clean tree is now dirty, list the changed lines under an explanation of why (an autofix step rewrote them and still exited 0). Degrades silently to "no check" outside a git work tree.

## Wiring

`scripts/vet.sh` stays a stub that exits 1 — this plan does not hydrate it, and must not, since the whole point of the stub is that only the adopter knows their commands. What changes is that its comment block gains the fan-out form alongside the existing serial examples, so an adopter sees the option at the moment they implement it:

```sh
# Serial:
#   pnpm lint && pnpm typecheck && pnpm test:unit
# Parallel, failures-only output:
#   exec scripts/run-parallel.sh lint='pnpm lint' typecheck='pnpm typecheck' test='pnpm test:unit'
```

Three prose surfaces name the same thing and must agree:

- **`CLAUDE.md` → Vetting** — one sentence after the existing examples: the checks may be fanned out with `scripts/run-parallel.sh`, which prints only what failed.
- **`ADOPTING.md` → "Implement `scripts/vet.sh`"** — the same pointer beside its four per-stack examples.
- **`docs/catalog.md` → G2** — a new row, disposition `adopt`, requires `sh` (and `git`, for the autofix check only), sited next to `scripts/vet.sh` since that is its intended caller. `scripts/check-skill-catalog.sh` asserts one row per *skill*; a script row is free-form, but the script gets run to confirm.

## Recording the divergence for `/sync-upstream`

The port is a deliberate local divergence from a file that still exists upstream, so the next sync must not offer `scripts/run-parallel.py` as an unmade decision. `upstream.json`'s `declined` map is path → why-not and is exactly the right record:

```json
"declined": {
  "scripts/run-parallel.py": "ported to POSIX sh as scripts/run-parallel.sh — vet.sh is not escapable, so it must not require python3"
}
```

A future upstream commit touching the Python original then lands on the skill's **skip (not adopted)** triage row, where the recorded reason is re-tested rather than assumed — which is the correct treatment: an improvement to the orchestration logic is worth reading and porting by hand, and the reason for not taking the file verbatim keeps holding regardless.

## Verification

There is no test framework here to hang a test off (`vet.sh` is a stub by design), so verification is a handful of real invocations, run from `tmp/`:

- Mixed pass/fail — confirm only the failing check's log is printed, prefixed, and that `Failed:` names it and the exit status is 1.
- All-pass — confirm `All passed.`, no log output, exit 0.
- A check sleeping past 10s — confirm the `still running:` line appears with elapsed seconds and names only the unfinished check.
- A check that writes a tracked file — confirm the autofix reminder fires and lists it, and that it stays quiet when the tree was already dirty beforehand.
- A `✓`-containing failing log — confirm those lines are suppressed and the printed log path shows them.
- Bad arguments (no args; a label with a space) — confirm each fails loudly with a usable message.
- `sh scripts/run-parallel.sh …` under `dash` if available, to catch an accidental bashism.

## DRY notes

- **Nothing is shared with `scripts/lib/watch-tick-common.sh`.** That library is sourced by the two watch-tick scripts and exists to share `gh` repo resolution and tick-state handling; it is `bash`, and it has no overlap with fork/poll/report. Routing this script through it would force `bash` on the one script that has a reason to be POSIX, in exchange for sharing zero lines.
- **The autofix `git status --porcelain` check is not extracted.** `/pr` and `/finalize` also read `git status --porcelain`, but they read it *in prose as an agent instruction*, not as code — there is no existing helper to reuse and no second code caller to justify creating one.
- **The Python original is not kept alongside the shell port.** Two implementations of one orchestrator is the duplication most likely to drift, and the shell version is a strict superset of the Python one's interface (arbitrary commands vs. pnpm script names). The Python file is not copied into this repo at all; its absence is recorded in `upstream.json` rather than as a deleted file.
- **`vet.sh` keeps its serial examples.** The parallel form is added *beside* them, not in place of them: a two-check vet run has nothing to gain from fan-out, and presenting one form as the only form would make the stub prescriptive about something the adopter should decide.
