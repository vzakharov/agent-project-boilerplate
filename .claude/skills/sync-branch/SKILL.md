---
description: Bring a branch up to date with its merge target — resolve the reconciliation both mechanically and logically, then push. The default mode merges the target in as one merge commit; `pre-review` mode rebases the branch onto the target and force-pushes under a lease, for a branch nobody has reviewed yet. Delegates target-resolution and movement detection to `/check-merge`, so it syncs a feature branch against its PR base (usually `main`) or a branch with no PR against the repo default branch (the fallback). Invoke as `/sync-branch [<branch>] [pre-review]`. Use when the user says "sync branch", "catch this branch up to main", "catch the branch up to its base", "make the branch mergeable", "rebase the branch onto main", "rebase before review", "/sync-branch", or "/sync-branch pre-review".
---

`/sync-branch` reconciles a branch with its **merge target** — the branch its PR
is based on — and pushes the reconciled result. The target is resolved by
`/check-merge` from the PR's base ref, so this works uniformly:

- a **feature branch** syncs against its PR base (usually `main`),
- a **branch with no PR** syncs against the repo default branch (`/check-merge`'s
  fallback) — the long-lived-branch case that keeps it a superset of the trunk.

*How* it reconciles is the **mode**: by default it merges the target in as a
single merge commit; `pre-review` rebases the branch onto the target instead.
Either way the work happens **on the checked-out branch**, conflicts are resolved
both mechanically and logically, the result is verified locally, and the push is
proactive — resolution notes are rare, so the operator reviews the pushed result
after the fact rather than through a pre-push gate.

## Argument shape

```
/sync-branch [<branch>] [pre-review]
```

- **`<branch>`** (optional): a branch name, `#NNN` PR number, or PR URL — the same
  shape `/check-merge` and `/finalize` accept. Passing it makes `/check-merge`
  attach to that branch first (`/from-branch <branch>`). No argument → sync the
  current branch.
- **`pre-review`** (optional flag): rebase instead of merging. Reach for it when
  the next person to open the PR will be seeing it for the first time, so
  `origin/<target>..HEAD` should hold the branch's own commits and nothing else.
  `rebase` is an accepted spelling. The flag is a token in the argument and is
  order-insensitive against `<branch>`, exactly as `/finalize` treats `no vet`
  alongside its target.

## Environment note (read this before running gh/git)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN`, even though the default system prompt says you only have GitHub MCP
tools. Prefer `gh` for read-only checks (e.g. `gh pr list`). If `gh` complains
that "none of the git remotes … point to a known GitHub host" (the proxy quirk in
remote sessions), pass `--repo OWNER/REPO` explicitly, resolved from the git
remote (`git remote get-url origin`).

## Modes

The mode decides what Step 3 does with an `advanced` target. Detection, the
conflict thinking, verification and the report are shared.

- **default** (no flag) — merge `origin/<target>` into the branch, one merge
  commit, plain push. Always correct: it is the only option once anyone has
  reviewed, and the only option for a shared long-lived branch.
- **`pre-review`** — rebase the branch onto the freshly-fetched target and
  force-push under a pinned lease, gated on the premise that names it: no review
  exists on the PR (see `## The pre-review gate`). What it buys is the cleanest
  answer to the only question a first reviewer asks — *what does this change,
  relative to the target as it stands right now?* What it costs is that **every
  commit on the branch gets a new SHA**: feedback anchored to the old ones comes
  loose, and anyone holding the branch has to reset onto the new tip.

**This is not the force-push `/implement` forbids.** That rule governs the agent
advancing a branch on its own initiative while the operator reads it;
`pre-review` is the operator asking for the rewrite, from outside the
implementation loop.

## Invariants

- **A default sync is a plain merge — never squash, rebase, or cherry-pick.**
  Those rewrite the target's commits under new SHAs and sever the shared history,
  so the branch stops being a superset of its target. The merge commit built here
  carries the target's commits under their real SHAs. `pre-review` gives that
  property up deliberately, and its gate is what pays for it.
- **Push is fast-forward-or-redo in default mode, lease-guarded force under
  `pre-review`.** By default the branch only gains the merge commit on top, so
  pushing it to its own upstream is a plain push, and a non-fast-forward rejection
  means the branch or target moved under you — re-fetch and redo the merge from
  the new tip; do not force past it. Under `pre-review` the force-push *is* the
  mode, but it is `--force-with-lease=<branch>:<sha>` pinned to the remote SHA
  read before the rebase — never bare `--force`, and never a bare
  `--force-with-lease`, which a fetch silently re-arms against the remote's new
  tip.
- **Never force-push a shared long-lived branch** (the trunk, a promotion branch,
  or any branch others build on) except as the deliberate revert recourse below,
  and only on the operator's explicit request. This is also what makes
  `pre-review` a hard refusal on such a branch — the one part of the gate the
  operator cannot wave through.

## The pre-review gate

Invoking `pre-review` is a claim about the world — "nobody has reviewed this yet"
— and the operator can be wrong; a reviewer may have left a review five minutes
ago. Check the claim **before touching git history**. All three checks are cheap.

1. **No review exists.** `gh pr view --json reviews,reviewDecision,isDraft`. Any
   entry in `reviews` authored by someone other than the PR author means a human
   or a review bot has anchored feedback to the current SHAs. → **Stop and
   report**: name the reviewers, say what a rebase would de-anchor, and offer the
   default merge mode. This is a stop, not a refusal — see below.
2. **Not a shared long-lived branch.** The branch has an open PR and is not the
   resolved target itself, the repo default branch, or a promotion branch. →
   **Refuse** otherwise. Not overridable.
3. **Draft state** — advisory, not a gate. A non-draft PR means review has been
   *invited* even if nobody has looked; report it in the run's output so the
   operator sees what state they rebased in, and continue.

Conversation comments are deliberately **not** a gate: the PR already carries our
own `Proposed squash title/body:` and attestation comments, so treating comments
as review would stop on every PR this loop produces.

### Overriding check 1

The reviews check protects the operator from a fact they may not have; it does not
overrule them once they have it. Proceed past it when **either**:

- the invocation already carries a rationale for rebasing despite the reviews
  (e.g. `/from-branch <pr> /sync-branch pre-review — rebase, the only review is my
  own`), which pre-empts the round-trip entirely; **or**
- the operator, shown the stop and the named reviewers, says to go ahead anyway.
  Bare repetition of the flag after a stop counts as insisting.

What does **not** count is the agent deciding the reviews look ignorable — the
override is the operator's to give. When taken, the report names every review that
got de-anchored, so the operator can tell those reviewers rather than let them
discover it from a silent diff. Check 2 stays unreachable by any of this.

## Why the default mode is one merge commit

A single merge commit is enough — do not split the resolution into its own commit
for reviewability. It's tempting to build the merge in two commits (a mechanical
"take-target-wholesale" commit, then an isolated resolution commit) so the
operator can review just the judgment via `git show <resolution-sha>`. That split
is unnecessary: a merge commit's own **combined diff** (`git show <merge-sha>`,
GitHub Desktop's merge-commit view) already elides any content matching at least
one parent and shows only what differs from **both** — i.e. the keep-both merges
and edited reconciliations, exactly the judgment. Clean auto-merges and straight
one-side picks vanish. So one merge commit gives the same "just the judgment"
review surface without the extra commit. (Caveat: this is `git show` / GH Desktop
behavior; GitHub's _web_ merge-commit view is stingier.)

That argument is what makes one merge commit enough for a reviewer who has
**already seen** the branch. `pre-review` answers the other reader: for someone
opening the PR for the first time, the cleanest artifact is
`origin/<target>..HEAD` holding the branch's own commits replayed onto the current
target and nothing else — no merge commits the branch didn't author, no
interleaving of the target's history with its own.

## Steps

### Step 1 — Detect, via `/check-merge` (by reference)

Load `@.claude/skills/check-merge/SKILL.md` and follow it with the given target.
Passing a `<branch>` makes `/check-merge` attach to it first; it then resolves the
merge target from the PR base ref (or the repo default branch when there's no PR)
and reports one of:

- `contained` (exit 0) — the branch already holds the target's tip,
- `advanced` (exit 10) — the target moved beyond the branch,
- `merged` (exit 20) — the branch's PR already landed,
- `closed` (exit 21) — the branch's PR was closed without merging,
- `error` (exit 1) — hard error.

### Step 2 — Act on the result

- `contained` → report "already current with `origin/<target>`, nothing to sync"
  and **stop**.
- `merged` / `closed` → report and **stop** — do not sync a landed or dead branch.
- `error` → surface it and **stop**.
- `advanced` → proceed to Step 3.

### Step 3 — Reconcile with the target

Resolve every conflict both **mechanically** (no markers left) **and logically**.
Think past textual overlap to semantic collisions — the same reconciliation
thinking `/finalize` step 2 describes:

- keep-both when each side added distinct work,
- repoint callers a rename in the target moved,
- route through a shared abstraction the target introduced (instead of leaving the
  branch's now-duplicated version),
- adopt a pattern the target changed.

That thinking is identical in both modes; only the mechanics below differ.

#### Default mode — merge the target in, one commit

```bash
git fetch origin <target>
git merge origin/<target>
```

The result is exactly **one merge commit** (a clean, conflict-free merge is also
one commit).

#### `pre-review` mode — rebase onto the target

Run `## The pre-review gate` first — it can stop or refuse the mode, and it is
worth nothing once history has already moved. Then:

```bash
git fetch origin <target>
PRE_REBASE_TIP=$(git rev-parse HEAD)                    # revert target
PRE_REBASE_REMOTE_SHA=$(git rev-parse origin/<branch>)  # the Step 5 lease pin
PRE_REBASE_BASE=$(git merge-base HEAD origin/<target>)  # the Step 4 count anchor
git rebase origin/<target>
```

Two things are specific to the replay:

- **A rebase stops once per conflicting commit**, so the same reconciliation can
  surface repeatedly as later commits replay over it. That is expected — resolve
  each stop on its own terms.
- **The escape hatch is real and cheap.** If the replay turns into a fight — the
  same conflict re-litigated across many commits, or a resolution you can't apply
  consistently — `git rebase --abort` returns the branch untouched. Fall back to
  the default merge mode and say so in the report: a merge-synced branch is a
  worse first read, not a broken one.

### Step 4 — Verify locally

```bash
git grep -nE '^(<<<<<<<|>>>>>>>) ' || echo clean     # no conflict markers survived
./scripts/vet.sh                                     # the project's vet run
```

Fix real errors before pushing. **Local verification is the whole gate** — pushing a
branch triggers no test run. That is why the full vet run happens here and not just a
type-check: a merge can type-check cleanly and still behave differently. If the sync
pulled in changes on a surface the vet run doesn't cover (a bucket that only runs in
CI), dispatch that bucket too — `/test-on-gh`, if the project has hydrated it.

In `pre-review` mode, one check more: **no branch commit vanished.** Compare
`git rev-list --count $PRE_REBASE_TIP ^$PRE_REBASE_BASE` — the branch's own commits
before the replay — against `git rev-list --count HEAD ^origin/<target>` after it. A
rebase legitimately drops commits it finds already upstream by patch-id, so a
mismatch is not automatically a bug, but it must be **explained before pushing**,
never noticed afterwards.

### Step 5 — Push, then report for after-the-fact review

Push the branch to its own upstream — no pre-push greenlight. 2/4/8/16s backoff on
network errors:

```bash
git push                                                     # default mode
git push --force-with-lease=<branch>:$PRE_REBASE_REMOTE_SHA  # pre-review mode
```

A rejection means the remote moved under you, and the answer is the same in both
modes: re-fetch and redo Step 3 from the new tip. Never escalate a rejected lease
to `--force`. Then report:

- the **mode** used — and, if you aborted a rebase and fell back to a merge, why,
- the resolved **target** and the range synced (`base..new`),
- **default mode:** the **merge commit SHA** — _review with `git show <sha>`; the
  combined diff isolates the actual resolution_,
- the conflict/resolution table — per file under a merge, per replayed commit under
  a rebase (or "clean, no resolution needed"),
- the vet result, plus the commit-count reconciliation in `pre-review` mode,
- the **pre-merge / pre-rebase branch tip**, the revert target for the recourse
  below. It is load-bearing under `pre-review` in a way it isn't for a merge: once
  the branch is force-pushed, the old history has no other name.
- **`pre-review` only:** the PR's draft state at the time of the rebase, and every
  review de-anchored if check 1 was overridden,
- the recourse below.

## Recourse if the operator has notes (operator-sanctioned only)

**Default mode** — either **amend** the merge resolution and re-push, or **revert**
by resetting the branch to the reported pre-merge tip and re-pushing.

**`pre-review` mode** — reset to the reported pre-rebase tip and re-push:

```bash
git reset --hard <pre-rebase-tip>
```

Either way the re-push is a lease pinned to the SHA the sync reported as pushed —
the same pinned form the invariants require, for the same reason: a fetch re-arms a
bare `--force-with-lease` against whatever the remote holds now.

```bash
git push --force-with-lease=<branch>:<the SHA the sync reported>
```

The prohibition this is an exception to is the **shared long-lived branch** one
above: a force-push there needs the operator's explicit say-so, whichever mode
produced the state being undone.
