> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Open the PR at plan time, so the plan is reviewed like code

## Why

A plan file today rides an unpushed-to-no-PR branch until implementation
finishes. The operator can read it, but cannot review it the way they review
everything else: inline comments anchored to lines, threads that persist, a
diff view. Feedback therefore arrives as chat prose, which is a worse surface
than the one this project already uses for code.

Opening the draft PR at the end of the planning turn fixes that with no new
machinery: the plan file becomes a reviewable diff, review comments become the
revision channel, and `/handle` on that branch becomes "process plan feedback"
exactly as it is already "process code feedback" — the outcome being an edited
plan rather than edited source.

## The reordering

Today: `/issue` → `/pr <task>` → **stop** → `/plan` → (new session) `/implement`
→ `/pr` opens the PR → `/finalize`.

After: `/issue` → `/pr <task>` → rename → `/plan` writes and commits the plan →
**`/pr` continues and opens the draft PR** → `/squash-message` → handoff →
(review loop via `/handle`) → (new session) `/implement` → `/pr` **refreshes**
the PR → `/finalize`.

The gate in `/pr` Step 1a stops being *"STOP, go plan, come back later"* and
becomes *"detour through `/plan`, then continue"*. Everything after the detour —
push, create, body, squash proposal — runs in the same turn it runs in today,
just over a plan commit instead of over implementation commits.

## Design decisions

### `/pr` becomes a 2×2, not a new skill

The two conditions that already govern the skill — *were args passed?* and *does
a PR exist?* — become an explicit table, replacing the current prose gate:

| | no PR | PR exists |
|---|---|---|
| **args** | **open mode**: rename → `/plan` → push → create draft → squash → handoff | continued work with a task → `/implement` § "Planless entry", then **refresh** |
| **no args** | open from the commits already on the branch (today's mid-session path, and where the `no plan` waiver lands) | **refresh mode**: re-derive body and QA checklist from the real diff, re-run `/squash-message`, create nothing |

Refresh mode is not new machinery — it is today's `<pre-created PR>` caller
parameter and the `gh pr edit` branch of Step 5, promoted from exception to
ordinary path.

### Revert the duplicate-PR guard (Step 1b)

`gh pr view … → stop and report` becomes `gh pr view … → refresh mode`.

The guard is carrying three jobs today, and only the first survives the
reordering intact:

1. Turning `gh pr create`'s refusal of a second open PR for the same head→base
   into an actionable message. Still needed — refresh mode simply is the
   actionable outcome.
2. Making `/implement` Step 4 and `/handle` → `/implement` § "Planless entry"
   idempotent when they land on a branch that already has a PR
   (`implement/SKILL.md:35` names this explicitly). This **inverts**: an
   existing PR becomes the expected state at the end of implementation, and the
   right response is to fill it in, not to decline.
3. Steering an operator who meant `/finalize` toward it. Survives as a line in
   refresh mode's report, not as a stop.

### The QA checklist is written from the plan

At PR-open time there is no diff, but there is an approved statement of what
will be delivered — which is what a QA checklist is derived from anyway.
`/qa-checklist` Step 2 gains the plan as an accepted input alongside
`origin/<base>..HEAD`, and refresh mode re-derives it against the real diff so
the forecast is reconciled with what actually shipped.

This keeps the derivation single-sourced in `/qa-checklist`; only its *input*
gains a second shape.

### The squash message is the plan condensed

`/squash-message` needs no change to its "created once, when the PR opens" rule
— that sentence stays literally true, the moment just moves earlier. Two edits:

- Step 1 "Gather" learns that a branch carrying only a plan commit has the plan
  as its input, not `git log`.
- The skill's opening gains the reason this is worth doing early: at plan time
  the proposal is *the plan as it would be recorded*, condensed to the size of a
  commit message — a second, much shorter read of the same decision, in front of
  the operator before any code exists.

**One ordering constraint, unchanged:** the title carries a `(pr #N)` suffix, so
the proposal cannot be composed before the PR number exists. The squash file
therefore lands in the push immediately *after* creation, within the same turn —
which is exactly why `/pr` Step 6 already sits where it does. From the
operator's side both files are on the PR when they first open it.

### "Still planning" is a property of `docs/plans/`, not of the invocation

The single new predicate this change introduces:

> **Implementation has begun** iff `docs/plans/` holds at least one file that is
> not `*.draft.do-not-implement.md` — that is, any `*.in-progress.md`,
> `*.paused.md` or `*.completed.md`.

Its home is `@.claude/skills/plan/SKILL.md` § "Plan file lifecycle", which
already owns the state machine; every other site cites it.

The predicate is deliberately broader than the case that motivates it. The
common shape is a branch carrying nothing but a draft plan and a squash message,
where "are we still planning?" is obvious. The broad form also handles the mixed
branch — one plan completed, then paused, then a follow-up draft opened, with a
review that touches both the new plan file and the shipped code. A draft plan
being present is the tell that the branch is back in planning, whatever else sits
beside it.

### `/handle` gets a condition, not a third lane

`/handle` Step 2 currently declares both lanes firing at once to be an abnormal
state and stops. Under this change it is the *normal* state of a plan under
review, so the stop is replaced by a reading:

- **Draft plan present + unanswered feedback** → the feedback is review *of the
  plan*. Stay in plan mode: revise the plan file, reply on GitHub per CLAUDE.md
  § "GitHub comments", push, re-emit the handoff block. Do **not** flip the plan
  file, do **not** touch source.
- **No draft plan + unanswered feedback** → today's review lane, unchanged.
- **Draft plan + no unanswered feedback** → today's plan lane, unchanged: the
  invocation is the go-ahead.

That last bullet is why no third lane is needed. `/handle` remains a go-ahead by
default; only the conjunction above suspends it. The sentence at
`handle/SKILL.md:17` gains that one exception rather than being rewritten.

### The approval gate gains a channel, not a rule

`@.claude/skills/plan/SKILL.md` § "The approval gate" already draws the right
distinction — *a suggestion is a plan revision; only a go-ahead token unlocks
implementation*. It only needs to learn that both can now arrive as PR review
comments. No change to what counts as either.

## Files

**Substantive:**

| File | Change |
|---|---|
| `.claude/skills/pr/SKILL.md` | Step 1a gate becomes a detour; Steps 1b/4/5 get the 2×2 mode table; Step 6 unchanged |
| `.claude/skills/plan/SKILL.md` | Caller-opens-the-PR parameter; predicate home in § "Plan file lifecycle"; approval gate gains the review-comment channel |
| `.claude/skills/handle/SKILL.md` | Step 2 both-lanes stop → plan-review reading; go-ahead sentence gains its exception |
| `.claude/skills/implement/SKILL.md` | Step 4 refreshes rather than opens; § "Planless entry" bullet on Step 1b updated |
| `.claude/skills/qa-checklist/SKILL.md` | Step 2 accepts the plan as input; the two `/pr`-composes-at-creation notes (lines 10, 22) |
| `.claude/skills/squash-message/SKILL.md` | Step 1 gather-from-plan; opening gains the plan-condensed rationale |
| `.claude/skills/issue/SKILL.md` | End state, the chain line (line 7), Step 4's "do not open the PR here" |

**Pointers:**

| File | Change |
|---|---|
| `CLAUDE.md` | `/pr` main-loop bullet; § "Plan mode & questions in web sessions" (the PR is the review surface); "rename … right after the first commit" → before it |
| `docs/catalog.md` | `/pr`, `/plan`, `/implement`, `/handle`, `/issue` rows |

`.claude/skills/check-merge/SKILL.md:54` ("posted when `/pr` opened the PR")
needs no edit — it stays true. `.claude/skills/branch-rename/SKILL.md` needs no
edit either; the reordering only makes its existing "rename before any PR is
opened" advice load-bearing earlier.

Verification is `bash scripts/check-skill-catalog.sh`, which asserts every
`@.claude/skills/…` pointer resolves and every skill has exactly one catalog row.

## DRY notes

- **QA-checklist derivation** stays single-sourced in `/qa-checklist` Step 2.
  `/pr` keeps delegating by reference in both modes; what gains a second shape is
  that step's input, not a second copy of the rules.
- **Squash-message format and discipline** stay single-sourced in
  `/squash-message`. `/pr` Step 6 keeps delegating.
- **The handoff block format** stays in `/plan` § "Handing off". `/pr` cites it
  and appends the PR URL rather than restating the block.
- **The "implementation has begun" predicate** is the one genuinely new shared
  fact, and it would otherwise be stated in three places (`/handle` Step 2,
  `/handle`'s go-ahead sentence, `/plan`'s approval gate). One home in `/plan`
  § "Plan file lifecycle"; the other two cite it. This is CLAUDE.md § "Writing
  things down" — *if the same constraint is stated in two places, one of them is
  the home and the other is a pointer*.
- **No shared "PR mode" abstraction.** The three modes are a table inside `/pr`,
  not a fourth skill. Extracting them would add a load hop and a file for zero
  reuse — `/implement` and `/finalize` each touch exactly one cell of the table
  and reach it through `/pr` already.

## Open questions

**1. `[no ci]` on plan-phase commits — in scope, or filed separately?**
`/squash-message` Step 5 says to add `[no ci]` only on a **non-draft** PR, which
implies draft PRs don't burn CI runs. That is not true in general: GitHub Actions
`pull_request` workflows fire on draft PRs by default; suppressing them takes an
explicit `if: github.event.pull_request.draft == false`. Under this change a
branch spends much longer in draft, so any adopter with PR workflows pays for
every plan-phase push.
It is moot for this repo — there is no `.github/` here at all — which is why the
recommendation is **(a) file it separately** rather than (b) widen this PR to fix
that sentence and add `[no ci]` guidance to plan-phase commits. *(a) is in force
in this plan.*

**2. Does bare `/pr` on a PR-less branch still open from commits?**
Recommendation: **yes, unchanged** — it is the documented mid-session wrap-up
path (a session that started as brainstorming and produced commits without a
plan), and it is where `/pr`'s own `no plan` waiver lands after `/implement`
§ "Planless entry" finishes. *In force in this plan.*
