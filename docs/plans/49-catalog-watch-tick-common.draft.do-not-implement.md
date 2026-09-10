> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #49 — move `scripts/lib/watch-tick-common.sh` into G2

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

The file's own header already names both callers ("Shared helpers for the
merge/CI check scripts (`scripts/ci-watch-tick.sh`, `scripts/check-merge.sh`)"),
so the code is honest and only the catalog row is wrong. Nothing machine-checks
this: `scripts/check-skill-catalog.sh` asserts that a catalog row's path exists
(assertion 3) and that skills have exactly one row (assertion 2), but it greps
`@.claude/skills/…` pointers only — no script-to-script dependency is checked in
either language.

## Approach

Move the row into G2 and cite it from both directions, using the form the
catalog already uses for its one other cross-group script dependency —
`scripts/export-github-item.py`'s row, which lists `scripts/lib/github.py (G2)`
group-tagged in **Requires**. Groups partition the inventory (`docs/catalog.md`
§ "How to read a row"), so the file can only live in one, and G2 is the group
that cannot do without it.

Docs-only. No script, skill or shell behavior changes.

## Steps

1. **Move the row from G5 to G2** in `docs/catalog.md`.
   - Delete `docs/catalog.md:213` from the G5 table.
   - Add it to the G2 table, placed next to `scripts/check-merge.sh` (its G2
     caller) rather than at the end, so the pair reads together.
   - Rewrite **What it does** so it stops implying a single caller family:
     currently "Shared shell helpers for the watch-tick scripts", which reads as
     G5-only. Replace with wording that names both jobs — the repo-resolution
     fallback (`wt_resolve_repo`, needed wherever `gh` cannot auto-detect the
     remote behind a proxy), the elapsed-aware sleep, and state-file reset —
     phrased as the shared plumbing behind `scripts/check-merge.sh` and
     `scripts/ci-watch-tick.sh`. Keep **Requires** `bash`, **Pulls in** `—`,
     **Disposition** `adopt`.
2. **Declare the dependency from `scripts/check-merge.sh`'s row**
   (`docs/catalog.md:130`): add `scripts/lib/watch-tick-common.sh` to its
   **Requires** cell, untagged (same group).
3. **Declare it from `scripts/ci-watch-tick.sh`'s G5 row**
   (`docs/catalog.md:212`): add `scripts/lib/watch-tick-common.sh` (G2) to its
   **Requires** cell, group-tagged — exactly the `export-github-item.py` form.
4. **Fix the G5 group blurb in `README.md:22`**, which reads "`/watch-ci`, and
   its polling scripts" (plural). After the move G5 carries one polling script;
   make it singular so the README and the catalog agree on what the group
   contains.
5. **Check nothing else asserts the old grouping.** `ADOPTING.md`'s three G5
   mentions (lines 92, 128, 183) are about CI detection and the proxy, not about
   this file, so they stand — re-grep to confirm rather than assuming.
6. **Run `bash scripts/check-skill-catalog.sh`** to confirm the row's path still
   resolves after the move (assertion 3) and no skill row was disturbed.

## What this plan deliberately does not do

- **No new machine check** for script-to-script dependencies. The issue rules
  this out and the code agrees: a missing `source` target fails immediately and
  by name, so the failure is loud, and the one other cross-group script
  dependency in the tree is already declared correctly. A checker here would be
  scope creep against a mechanism that works.
- **No file rename.** See question 1.

## Open questions

1. **Rename the file to drop the `watch-tick` prefix?** After the move, a G2
   adopter who declines G5 holds `scripts/lib/watch-tick-common.sh` with no
   watch-tick script in the tree — the name points at a caller they do not have.
   A rename (e.g. `scripts/lib/gh-common.sh`) would touch both sourcing scripts
   and their `# shellcheck source=` directives.
   - **(a) Don't rename — recommended, and the plan is written this way.** The
     mismatch is cosmetic and self-correcting on read: the file's header names
     both callers in its first two lines, and the function prefix (`wt_`) would
     have to move too or the rename buys only half the clarity. It also churns
     every adopter's tree at the next `/sync-agent-infra` for no behavior
     change.
   - (b) Rename in the same PR, `wt_` prefix included — a bigger, code-touching
     diff for a naming improvement the issue did not ask for.
2. **Add a fifth bullet to `docs/catalog.md` § "Closure is not optional"?** That
   list states four closure facts "counter-intuitive enough to state outright",
   and "a file named `watch-tick-*` is a G2 requirement" arguably qualifies.
   - **(a) No — recommended, and the plan is written this way.** After step 3
     both rows carry the dependency in the column built for it, which is where a
     reader looking at either script finds it. The closure list earns its
     entries by covering things a row cannot say; this is not one.
   - (b) Yes — one sentence, for an adopter skimming groups rather than rows.

## DRY notes

- **Reused, not invented:** the cross-group citation form already exists in the
  catalog (`scripts/export-github-item.py` → `scripts/lib/github.py (G2)`). This
  change makes a second row use it rather than introducing a convention.
- **The duplication this creates is wanted.** After step 3 the dependency is
  stated in three places: the file's own header comment, and the **Requires**
  cell of each sourcing script's row. These are not copies of one fact for one
  audience — the header serves someone editing the shell, and each row serves an
  adopter deciding whether to copy that one script. The catalog's row format is
  per-item by construction, so a shared "see the other row" pointer would be
  worse than the restatement.
- **No shared abstraction is extracted, and none should be.** The tempting one is
  a machine check that every `source`d path is declared in the sourcing script's
  catalog row. Two script-to-script dependencies exist in the whole tree and one
  is already correct, so the checker would be more code than the thing it
  checks, in a repo where the loop is the product.
- **One home per statement, per CLAUDE.md § "Writing things down".** The group
  membership is stated in `docs/catalog.md` only; `README.md:22`'s group blurb is
  a pointer, which is why step 4 repoints it instead of leaving it half-right.

## Verification

- `bash scripts/check-skill-catalog.sh` passes.
- `grep -n "watch-tick-common" docs/catalog.md` shows the row under G2 and a
  citation in each of the two sourcing scripts' rows.
- The G5 table has three rows; the G2 table has one more than before.
- No file outside `docs/catalog.md` and `README.md` is modified (plus this
  plan and the issue export, both swept at finalize).
