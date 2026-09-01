# `/sync-branch pre-review` — sync by rebasing while the branch is still unreviewed

## Problem

`/sync-branch` has exactly one strategy, stated as a hard invariant:

> **A sync is a plain merge — never squash, rebase, or cherry-pick.**

That invariant is correct once a human has started reviewing: rebasing rewrites
the branch's commits under new SHAs, which detaches review comments from the
diff they were written against and invalidates any checkout the reviewer has.

But it is *costly* before review starts. A merge-synced branch's history
interleaves the target's commits with its own, so a reviewer opening it for the
first time reads the branch's work through merge commits it didn't author. A
rebased branch gives the cleanest possible answer to the only question a first
reviewer asks — *what does this change, relative to `main` as it stands right
now?* — because `origin/<target>..HEAD` is then exactly the branch's own
commits, replayed onto the current target and nothing else.

So the strategy should follow the review state, and today it can't.

## Approach

Add a second mode to `/sync-branch`, selected by an explicit flag:

```
/sync-branch [<branch>] [pre-review]
```

- **default (no flag)** — today's behavior, unchanged: one merge commit, plain
  push. This stays the default because it is always safe.
- **`pre-review`** — rebase the branch onto the freshly-fetched target and
  force-push with a lease. Gated on the premise that gives the mode its name
  actually holding: **no review exists on the PR**. `rebase` is accepted as an
  alias, mirroring how `/finalize` accepts `no ci` / `no attest` for `no vet`.

The flag is a token in the argument, order-insensitive against the optional
`<branch>` target, exactly as `/finalize` treats `no vet` alongside its target.

**The premise is checked, not taken on the invocation's word.** Invoking the
mode is a claim about the world ("nobody has reviewed this yet"), and the
operator can be wrong — a reviewer may have left a review five minutes ago. So
the mode opens with a gate that checks it and stops by default. The gate is
overridable, because the operator sometimes knows something the API doesn't (the
review is their own, or the reviewer asked for the rebase) — but the override is
theirs to give, not the agent's to assume.

## Files to change

### 1. `.claude/skills/sync-branch/SKILL.md` — the substance

**Frontmatter `description`.** It currently promises "a single merge commit" as
the skill's definition. Rewrite so the two modes are both visible to skill
selection, and add the trigger phrases that should reach the new mode
("rebase the branch onto main", "rebase before review", "/sync-branch
pre-review").

**Opening prose.** The lede describes the merge as the skill's identity. Restate
it as: the skill reconciles a branch with its merge target; *how* it reconciles
is the mode, and the default is a merge.

**`## Argument shape`.** Add the flag with its alias, its order-insensitivity,
and a one-line statement of when to reach for it.

**New section: `## Modes`.** The decision surface, placed before the invariants
so the invariants can be scoped against it:

- *default* — always correct; the only option once anyone has reviewed, and the
  only option for a shared long-lived branch.
- *pre-review* — legible-first-diff mode. Preconditions, the rewrite it
  performs, and what it costs (every branch SHA changes; anyone holding the
  branch must reset).
- **One line disambiguating this from `/implement`'s "never force-push".** That
  rule governs the agent advancing a branch on its own initiative while the
  operator reads it; `pre-review` is the operator asking for the rewrite, from
  outside the implementation loop. Stating it here rather than editing
  `/implement` keeps the clarification on the mode that needs it — see "Not in
  scope" for why the reverse costs more.

**`## Invariants` — scope the existing ones per mode rather than deleting them.**
This is the delicate edit: the "never rebase" line is load-bearing for the
default path and must not weaken there. Rewrite the three invariants as:

- *A default sync is a plain merge* — never squash, rebase or cherry-pick under
  the default mode; the rationale (the branch stays a superset of its target
  under the target's real SHAs) is unchanged and still stated. `pre-review`
  deliberately does not preserve that property, and its gate is what pays for it.
- *Push is fast-forward-or-redo in default mode; lease-guarded force in
  `pre-review`* — a non-fast-forward rejection under default still means re-fetch
  and redo, never force. Under `pre-review` the force-push is the mode, but it is
  `--force-with-lease` pinned to the pre-rebase remote SHA
  (`--force-with-lease=<branch>:<sha>`), never bare `--force` and never a bare
  lease — the pinned form is what keeps the guard meaningful after a fetch.
- *Never force-push a shared long-lived branch* — unchanged, and now doubles as a
  hard refusal condition for `pre-review`: the mode is for a feature branch with
  a PR, not the trunk, a promotion branch, or anything others build on. This one
  is **not** overridable by the operator in-flight; it is the invariant the
  override below explicitly does not reach.

**New section: `## The pre-review gate`.** Three checks, run before touching git
history. All are cheap; the first is the one with judgment in it:

1. **No review exists** — `gh pr view --json reviews,reviewDecision,isDraft`. Any
   entry in `reviews` authored by someone other than the PR author means a human
   (or a review bot) has anchored feedback to the current SHAs. → **Stop and
   report**: name the reviewers and what a rebase would de-anchor, and offer the
   default merge mode. This is a stop, not a hard refusal — see the override
   below.
2. **Not a shared long-lived branch** — the branch has an open PR and is not the
   resolved target itself, the repo default branch, or a promotion branch. →
   **Refuse** otherwise. Not overridable.
3. **Draft state** — advisory only, not a gate. A non-draft PR means review has
   been *invited* even if nobody has looked; report it in the run's output so the
   operator sees what state they rebased in, and continue.

Conversation comments are deliberately **not** a gate: the PR already carries our
own `Proposed squash title/body:` and attestation comments, so treating comments
as review would stop on every PR the loop itself produced.

**Sub-section: `### Overriding check 1`.** The reviews check protects the
operator from a fact they may not have; it does not overrule them once they have
it. Proceed past it when **either**:

- the invocation already carries a rationale for rebasing despite the reviews
  (e.g. `/from-branch <pr> /sync-branch pre-review — rebase, the only review is
  my own`), which pre-empts the round-trip entirely; **or**
- the operator, shown the stop and the named reviewers, says to go ahead anyway.

Bare repetition of the flag after a stop counts as insisting. What does **not**
count is the agent deciding the reviews look ignorable — the override is the
operator's to give. When taken, the report must name every review that got
de-anchored, so the operator can tell those reviewers rather than discovering it
from a silent diff. Check 2 stays unreachable by any of this.

**`## Steps` — branch Step 3 onward by mode.** Steps 1–2 (`/check-merge`
delegation, act on the result) are mode-independent and stay as they are.

- **Step 3 becomes mode-split.** Default keeps `git fetch` + `git merge` verbatim.
  `pre-review` gets its own procedure:

  ```bash
  git fetch origin <target>
  PRE_REBASE_TIP=$(git rev-parse HEAD)              # revert target, and the lease pin
  git rebase origin/<target>
  ```

  with the conflict guidance carried over — resolve **mechanically and logically**,
  the same semantic-collision thinking the merge path already describes (keep-both,
  repoint callers a rename moved, route through a shared abstraction the target
  introduced, adopt a changed pattern). Two things are new to the rebase path and
  need saying:
  - **A rebase stops once per conflicting commit**, so the same reconciliation can
    surface repeatedly as later commits replay over it. That is expected — resolve
    each stop on its own terms.
  - **The escape hatch is real and cheap**: if the replay turns into a fight
    (the same conflict re-litigated across many commits, or a resolution you can't
    make consistently), `git rebase --abort` returns the branch untouched. Fall
    back to the default merge mode and say so in the report — a merge-synced branch
    is a worse first-read, not a broken one.

- **Step 4 (verify) gains one rebase-specific check** on top of the existing
  no-conflict-markers grep and `./scripts/vet.sh`: **no branch commit vanished.**
  Compare `git rev-list --count <PRE_REBASE_TIP> ^<old target tip>` against
  `git rev-list --count HEAD ^origin/<target>`. Rebase legitimately drops commits
  it finds already upstream by patch-id, so a mismatch is not automatically a
  bug — but it must be *explained* before pushing, never noticed afterward.

- **Step 5 (push) becomes mode-split.** Default keeps the plain `git push`.
  `pre-review` pushes:

  ```bash
  git push --force-with-lease=<branch>:<PRE_REBASE_REMOTE_SHA>
  ```

  where the pin is the remote's SHA read *before* the rebase. A rejected lease
  means the remote branch moved under you — re-fetch and redo the rebase from the
  new tip; do not escalate to `--force`.

- **The report gains the pre-review shape**: the mode used, the resolved target and
  range, the **pre-rebase tip** (the revert target — load-bearing here in a way it
  isn't for a merge, since the old history is otherwise unreachable), the
  per-commit conflict/resolution table, the vet result, the draft-state advisory,
  any reviews de-anchored by an override, and the recourse.

**`## Why one merge commit keeps reviewability`.** Keep it as-is and re-title it
so it reads as the default mode's rationale rather than the skill's — then add a
short counterpart paragraph for `pre-review`: the combined-diff argument is what
makes *one merge commit* enough for a reviewer who has already seen the branch;
the rebase argument is about a reviewer who has **not**, for whom the cleanest
artifact is `origin/<target>..HEAD` containing the branch's commits and nothing
else.

**`## Recourse if the operator has notes`.** The existing revert recipe becomes the
default mode's. Add the `pre-review` one — `git reset --hard <pre-rebase-tip>`
then `git push --force-with-lease` — and note that this mode is *already* a
sanctioned force-push, so the "only sanctioned force-push here" line moves to
being about the shared-branch prohibition rather than a blanket count.

### 2. `docs/catalog.md` — the `/sync-branch` row

The "What it does" cell currently ends at "in one merge commit", which is now
only the default. Rewrite the one-liner to cover both modes. Requires and Pulls
in are unchanged (`gh`, `scripts/vet.sh`; `/check-merge`) — the gate uses the
`gh` that is already declared.

### 3. Verification

`bash scripts/check-skill-catalog.sh` — no skill is added or renamed, so this is
a regression check that the edits didn't dangle an `@`-reference or disturb the
one-row-per-skill invariant. `./scripts/vet.sh` is a stub in this repo (exits
`1`), so this diff is docs-only and lands via `/finalize no vet`.

## Explicitly not in scope

- **`/implement` is not edited.** Its unqualified "never force-push" cannot
  actually collide with this mode: `/implement` never invokes `/sync-branch`
  (only `/from-branch` and the operator do), and the rule is scoped to its own
  Step 2 loop — the agent advancing a branch while the operator reads it — which
  `pre-review` sits outside by construction. Editing it would also give
  `/implement` a new **Pulls in** edge on `/sync-branch` in `docs/catalog.md`
  that every adopter then has to resolve. The residual case (a session that ran
  `/implement` still holding its text in context when a sync is later requested)
  is handled by the one disambiguating line in `## Modes` above, which adds no
  cross-skill reference.
- **`/finalize` Step 2 stays a merge.** By the time `/finalize` runs, the branch
  is being flipped to ready and is about to be reviewed or merged — the moment
  rebasing stops being cheap. Adding a rebase path there would put the rewrite
  at the worst possible point in the lifecycle.
- **`/check-merge` is untouched.** It detects movement and hands back; the
  strategy is the enclosing flow's call, which is exactly the seam this change
  uses.
- **No auto-detection.** The mode is not inferred from "PR is draft and has no
  reviews". Silently force-pushing because a heuristic fired is a surprise the
  operator can't undo from the report alone; the flag keeps the rewrite an
  explicit, attributable act. (See the rejected-options note below.)

## DRY notes

- **The conflict-resolution guidance is genuinely shared and must not be
  duplicated.** Both modes need the same "resolve mechanically *and* logically"
  thinking — keep-both, repoint moved callers, route through a new shared
  abstraction, adopt a changed pattern. The plan keeps that as **one** block of
  prose in Step 3, stated once above the mode split, with only the
  rebase-specific additions (per-commit replay, the `--abort` escape) sitting
  under the `pre-review` branch. Restating the four bullets under each mode is
  the obvious wrong turn here: it is the part most likely to be edited later, so
  a copy would drift first.
- **Target resolution and movement detection are already extracted** into
  `/check-merge`, and this change reuses them untouched. Both modes enter at the
  same Step 1 and act on the same five outcomes; the mode only decides what
  Step 3 does with an `advanced` result. No new detection logic is written.
- **The verification step is shared, with one addition, not forked.** Step 4's
  marker grep and `./scripts/vet.sh` are identical in both modes; only the
  commit-count check is `pre-review`-only. Keeping Step 4 as one section with a
  single conditional line beats two near-identical verify sections.
- **The force-push rule is stated once, in `/sync-branch`, not mirrored into
  `/implement`.** Two copies of a force-push policy in two skills is exactly the
  duplication that drifts, and the mirror would buy a catalog edge for a
  collision that cannot occur — see "Not in scope".
- **The `gh` review lookup is not extracted into a script.** It is one
  `gh pr view --json reviews,reviewDecision,isDraft` call used at exactly one
  call site. `scripts/check-merge.sh` exists because its logic is multi-step,
  exit-code-encoded, and invoked from three skills; a single `gh` call with a
  stop attached has none of those properties, and giving it a script would add a
  file, a catalog row and an adoption decision to buy nothing.
- **No shared "modes" abstraction across skills.** `/finalize` (`no vet`),
  `/squash-message` (`update-only`), `/branch-rename` (`force`) and now
  `/sync-branch` (`pre-review`) all take a flag token, but they are prose
  documents, not code — the reuse available is a consistent *convention*, which
  this plan follows deliberately (flag token, order-insensitive against the
  optional target, aliases listed inline), not a factored-out mechanism.

## Rejected alternatives

**Auto-detecting the mode** (rebase whenever the PR is draft with no reviews,
merge otherwise) was considered and dropped: it makes the destructive path the
implicit one, and the heuristic's inputs can change between the check and the
push. **`rebase` as the canonical flag name** was dropped because it names the
mechanism rather than the condition that makes the mechanism safe, and the
condition is the part an agent needs to check — it survives as an alias. **A hard,
un-overridable refusal when reviews exist** was dropped because the operator
sometimes holds a fact the API doesn't (the review is their own, the reviewer
asked for the rebase); the stop-then-override shape keeps the protection without
making the agent the final word.
