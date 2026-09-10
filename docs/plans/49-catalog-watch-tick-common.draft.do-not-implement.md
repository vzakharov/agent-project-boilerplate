> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #49 — split the repo resolver out of `watch-tick-common.sh` into G2

Issue export: `docs/issue/49/issue.md`

## The problem, restated from the code

`docs/catalog.md:213` files `scripts/lib/watch-tick-common.sh` under **G5 — CI &
landing**, but two scripts source it, in two different groups:

| Sourcing script | Group | Line |
| --- | --- | --- |
| `scripts/ci-watch-tick.sh` | G5 | `scripts/ci-watch-tick.sh:40` |
| `scripts/check-merge.sh` | G2 | `scripts/check-merge.sh:39` |

`scripts/check-merge.sh` is what `/check-merge` runs, and `/finalize` and
`/sync-branch` both reach it through `/check-merge`. So an adopter who takes G2
and declines G5 — the documented normal case for a repo with no CI — deletes the
file and the PR loop stops working at its landing step.

**The file is two things under one name.** Of its three functions, only one is
shared:

| Function | What it does | `check-merge.sh` | `ci-watch-tick.sh` |
| --- | --- | --- | --- |
| `wt_resolve_repo` | Sets `NWO` and `REPO_FLAG`, falling back to parsing the `origin` remote when `gh` cannot auto-detect the repo behind a sandboxed proxy. Guarantees `REPO_FLAG` is non-empty, since expanding an empty array under `set -u` errors on macOS's bash 3.2. | ✅ `:54` | ✅ `:48` |
| `wt_smart_sleep` | Sleeps `INTERVAL` minus the time already elapsed since the previous tick. | — | ✅ `:108` |
| `wt_reset_state` | Removes the state file for `--reset` and exits. | — | ✅ `:44` |

The two unshared functions are the tick machinery, and `check-merge.sh` is
architecturally the opposite of a tick loop — its own header declares it
"Stateless: it computes everything from git on each run (no baseline file)",
usage "run once". So the generic thing G2 needs is bundled into a file named,
prefixed (`wt_`) and documented after G5's polling loop.

The catalog row is wrong either way, and nothing machine-checks it:
`scripts/check-skill-catalog.sh` asserts that a row's path exists (assertion 3)
and that skills have exactly one row (assertion 2), but it greps
`@.claude/skills/…` pointers only — no script-to-script dependency is checked in
either language.

## Approach

Split the file along the seam that already exists in it. `wt_resolve_repo`
becomes `scripts/lib/gh-repo.sh` in **G2**, where its only unconditional caller
lives; `wt_smart_sleep` and `wt_reset_state` stay in
`scripts/lib/watch-tick-common.sh` under **G5**, which is what they are actually
for. `scripts/check-merge.sh` then sources one G2 file and nothing from G5, so a
G2-only adopter's PR loop is self-contained — which is what issue #49 is about.

`scripts/ci-watch-tick.sh` sources both, and its G5 row cites the new file
group-tagged as `scripts/lib/gh-repo.sh` (G2) — the form
`scripts/export-github-item.py`'s row already uses for `scripts/lib/github.py
(G2)`, and the catalog's established way to declare a cross-group script
dependency.

**Moving the row whole would leave that same G5→G2 arrow** (a G2-resident
`watch-tick-common.sh` is still what `ci-watch-tick.sh` sources), so the split
does not add a dependency direction — it removes the two functions a G2-only
adopter would otherwise carry and never call, and lets each file's name match
its group. See question 1 for the minimal alternative.

## Steps

1. **Create `scripts/lib/gh-repo.sh`** (G2) holding the repo resolver, moved
   verbatim from `scripts/lib/watch-tick-common.sh` with its comment block:
   - Rename `wt_resolve_repo` → `gh_resolve_repo`. The `wt_` prefix names the
     watch-tick loop; a file that no longer belongs to it should not keep it.
   - It reads `${WT_PROG:-watch-tick}` for its diagnostic prefix. Give the new
     file its own `${GH_REPO_PROG:-gh-repo}` rather than having a G2 file read a
     variable named for G5's loop, and set it in both callers alongside the
     `WT_PROG` each already sets.
   - Keep the header's two standing contracts, which are the reason the code
     reads the way it does: the file is **sourced, not executed** (the caller
     owns `set -euo pipefail`), and `REPO_FLAG` is **never left empty** because
     of the bash 3.2 `set -u` behavior.
2. **Trim `scripts/lib/watch-tick-common.sh`** to `wt_smart_sleep` and
   `wt_reset_state`, and narrow its header: it is the watch loop's helpers, with
   `scripts/ci-watch-tick.sh` its only caller. Drop `scripts/check-merge.sh`
   from the callers line.
3. **Repoint `scripts/check-merge.sh`**: source `scripts/lib/gh-repo.sh` instead
   of `watch-tick-common.sh`, update the `# shellcheck source=` directive above
   it, call `gh_resolve_repo`, and set `GH_REPO_PROG` (keeping `WT_PROG` only if
   something still reads it — it should not, so drop it and set `PROG` directly).
4. **Repoint `scripts/ci-watch-tick.sh`**: source both files, each with its own
   `# shellcheck source=` directive, call `gh_resolve_repo`, and set both prog
   variables. Its line-47 comment points at `watch-tick-common.sh` for the repo
   flag — repoint it at `gh-repo.sh`.
5. **Update `docs/catalog.md`**:
   - Add a `scripts/lib/gh-repo.sh` row to the **G2** table next to
     `scripts/check-merge.sh`, describing the proxy-aware repo resolution rather
     than "shared helpers". **Requires** `bash`, **Pulls in** `—`,
     **Disposition** `adopt`.
   - Add it to `scripts/check-merge.sh`'s **Requires** cell, untagged (same
     group).
   - Keep `scripts/lib/watch-tick-common.sh` in **G5**, rewriting its
     description to the two tick helpers it now holds.
   - Add both `scripts/lib/watch-tick-common.sh` and `scripts/lib/gh-repo.sh`
     (G2) to `scripts/ci-watch-tick.sh`'s **Requires** cell, the second
     group-tagged.
6. **Check `README.md:22`.** Its G5 blurb reads "`/watch-ci`, and its polling
   scripts" — still true after the split (`ci-watch-tick.sh` plus
   `watch-tick-common.sh`), so leave it. Re-read it rather than assuming.
7. **Verify nothing else asserts the old shape.** `ADOPTING.md`'s three G5
   mentions (lines 92, 128, 183) are about CI detection and the proxy, not this
   file. Re-grep for `watch-tick` and `wt_resolve_repo` across the tree to catch
   any prose citation the four file edits missed.
8. **Run the checks**: `bash scripts/check-skill-catalog.sh` (both new paths
   resolve, no skill row disturbed) and `./scripts/vet.sh`. Then exercise both
   scripts for real — see Verification.

## What this plan deliberately does not do

- **No new machine check** for script-to-script dependencies. The issue rules
  this out and the code agrees: a missing `source` target fails immediately and
  by name, so the failure is loud, and the one other cross-group script
  dependency in the tree is already declared correctly. A checker here would be
  more code than the thing it checks.
- **No behavior change.** Every function keeps its body; this is a move, two
  renames and four re-pointings. Any diff hunk that changes what a function
  *does* is out of scope.

## Open questions

1. **Split, or just move the row?** The split is a code change on an issue that
   asked for a catalog fix, so the minimal alternative stays on the table.
   - **(a) Split — recommended, and the plan is written this way.** It fixes the
     cause rather than the label: a G2-only adopter gets a self-contained PR
     loop instead of a file named and prefixed after a loop they declined, with
     two functions they never call. Both options leave `ci-watch-tick.sh`
     depending on a G2 file, so the split costs no dependency the move avoids.
   - (b) Move the row whole into G2 and cite it group-tagged from
     `ci-watch-tick.sh`'s row, changing no code. Smaller diff, no churn in
     adopters' trees at the next `/sync-agent-infra`, and it does close #49 —
     the catalog would then be accurate. The cost is that the accurate statement
     is "the PR loop requires `watch-tick-common.sh`", which reads as a catalog
     error every time someone meets it.
2. **Add a fifth bullet to `docs/catalog.md` § "Closure is not optional"?** That
   list states four closure facts "counter-intuitive enough to state outright" —
   `/plan` travelling with G2, `scripts/vet.sh` not being optional within it,
   `/finalize` reaching conditionally into G3 and G5, and `/override-gh` being
   pulled in by G0 and G3. Its bar is a **group-level** surprise a per-item row
   cannot express.
   - **(a) No — recommended, and the plan is written this way.** Under the split
     each file's name matches its group, so there is no surprise left to state:
     `scripts/ci-watch-tick.sh`'s **Requires** cell carries the one cross-group
     fact, in the column built for it.
   - (b) Yes — one sentence. This only earns its place under option 1(b), where
     the counter-intuitive thing (a `watch-tick-*` file inside the PR loop)
     survives the fix.

## DRY notes

- **The split is the DRY call, and it goes the other way from the usual one.**
  `wt_resolve_repo` is genuinely shared — two callers, one implementation, and
  it stays that way. What is *not* shared is the file around it, and bundling
  unshared code with shared code is what made the catalog row unanswerable. The
  extraction reduces what the G2 caller must take to what it actually uses.
- **Reused, not invented:** the cross-group citation form already exists
  (`scripts/export-github-item.py` → `scripts/lib/github.py (G2)`), and
  `scripts/lib/` is already where shared script plumbing lives, in both
  languages. No new convention.
- **Not extracted: a third lib for the prog-prefix pattern.** Both libs will
  read a `${…_PROG:-default}` for diagnostics — two lines of the same shape. A
  shared helper for that would be a file to hold a parameter default, and it
  would re-create the cross-group coupling this plan removes.
- **Not extracted: a checker** asserting every `source`d path is declared in the
  sourcing script's catalog row. Three script-to-script dependencies exist in
  the whole tree after this change, all declared; the checker would outweigh
  them.
- **One home per statement, per CLAUDE.md § "Writing things down".** Each
  function's contract stays in its file's header, the group membership stays in
  `docs/catalog.md`, and `README.md`'s blurb stays a pointer — step 6 checks it
  still points true rather than restating it.

## Verification

- `bash scripts/check-skill-catalog.sh` and `./scripts/vet.sh` pass.
- `bash -n` on all three shell files, and `shellcheck` if available — the
  `# shellcheck source=` directives must name the files actually sourced.
- **`scripts/check-merge.sh` runs on this branch** and reports against the PR's
  base, proving the extracted resolver works through the session proxy — the
  case `wt_resolve_repo`'s fallback exists for, and the one a unit test would
  not cover.
- **`scripts/ci-watch-tick.sh --reset` runs** without an unbound-variable or
  missing-function error, proving both sources land and `wt_reset_state`
  survived the trim.
- `grep -rn "wt_resolve_repo\|watch-tick-common" .` returns only
  `scripts/ci-watch-tick.sh`, `scripts/lib/watch-tick-common.sh` and their
  catalog rows — no stale citation anywhere else.
