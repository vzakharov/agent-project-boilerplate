> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Give each loop skill one thing to own

## Why

A plan file rides a PR-less branch until implementation finishes. The operator
can read it, but cannot review it the way they review everything else in this
project: no inline comments, no threads, no diff view. Feedback arrives as chat
prose instead — a worse surface than the one already in use for code.

Fixing that means opening the draft PR at plan time. Pulling on it turns up
three more places where a skill is doing a job that belongs to a neighbour, and
they are cheaper to fix together than separately: each one is *removing* a
responsibility from a skill that acquired it by accident.

## The four moves

1. **The draft PR opens at plan time**, over the plan commit, so the plan file is
   a reviewable diff and `/handle` on that branch processes plan feedback the way
   it already processes code feedback.
2. **`/plan` publishes its own plan.** The trigger is "a plan exists and is
   pushed", which is `/plan`'s event — so *every* entry into `/plan` gets a PR,
   not just the ones that arrived through `/pr`.
3. **`/pr` stops accepting a task argument.** New work is `/plan`; unplanned work
   is `/go` (below). `/pr` is left owning the PR object alone.
4. **`/implement` becomes `/go`**, which is what the approval gate has been
   listening for all along.

Together they reassign three ownerships:

| Skill | Owns |
|---|---|
| `/plan` | plan content — the file, the questions, the approval gate, the lifecycle names — **and publishing it** |
| `/go` | task entry and execution — every shape of "start working" |
| `/pr` | the PR object — create vs. refresh, title, body, base, draft state |

## Move 1 — the PR opens at plan time

Today: `/issue` → `/pr <task>` → **stop** → `/plan` → (new session) `/implement`
→ `/pr` opens the PR → `/finalize`.

After: `/issue` → `/plan` → plan committed → **`/plan` opens the draft PR** →
`/squash-message` → handoff → (review loop via `/handle`) → (new session) `/go`
→ `/pr` **refreshes** → `/finalize`.

Everything after the plan commit — push, create, body, squash proposal — runs in
the same turn it runs in today, over a plan commit instead of implementation
commits.

### The QA checklist is written from the plan

At PR-open time there is no diff, but there is a statement of what will be
delivered — which is what a QA checklist is derived from anyway. `/qa-checklist`
Step 2 gains the plan as an accepted input alongside `origin/<base>..HEAD`, and
refresh mode re-derives it against the real diff so the forecast is reconciled
with what shipped. The derivation stays single-sourced; only its input gains a
second shape.

### The squash message is the plan condensed

At plan time the proposal is *the plan as it would be recorded* — a second, much
shorter read of the same decision, in front of the operator before any code
exists. `/squash-message` needs two edits: Step 1 "Gather" learns that a branch
carrying only a plan commit has the plan as its input rather than `git log`, and
the opening gains that rationale.

Its "created once, when the PR opens" rule needs no change — the sentence stays
true, the moment just moves earlier.

**One ordering constraint:** the title carries a `(pr #N)` suffix, so the
proposal cannot be composed before the PR number exists. The squash file lands in
the push immediately *after* creation, within the same turn — which is why `/pr`
Step 6 already sits where it does. From the operator's side both files are on the
PR when they first open it.

## Move 2 — `/plan` publishes

`/plan` gains a final step: hand to `/pr` in **plan-open mode** to rename, push,
create the draft, compose the body, and invoke `/squash-message`. Then emit the
handoff block, now carrying the PR URL.

Putting the trigger here rather than in `/pr` is what makes the change reach the
common case. CLAUDE.md § "Plan mode & questions in web sessions" names `/plan` as
the default entry for a new web session — more common than `/pr <task>` or
`/issue`. Hanging PR-creation off `/pr`'s argument would leave that entry with a
PR-less branch, giving the least benefit to the most-used path.

`/pr` still owns the `gh` mechanics; `/plan` owns only the decision to publish.

## Move 3 — `/pr` takes no task argument

`/pr`'s Step 1a — the plan gate — **deletes entirely**. Both of its branches move
out:

- `/pr <task>` → `/plan`, which now publishes (move 2).
- `/pr <task> no plan` → `/go <task>`. This was already a longer spelling of the
  same thing: Step 1a's waiver routes to `/implement` § "Planless entry", whose
  first line is *"A caller skill may enter here with a **task** in place of a
  plan."* The change makes that front door operator-facing.

Step 1a is the longest and most defensive prose in the tree — *"the **only**
waiver is…"*, *"not because the task looks small, well-specified, or like a tweak
to existing work"* — and all of it exists to guard an argument `/pr` has no
business accepting. Remove the argument and the guard has nothing to guard.

What remains is a no-args skill with three modes:

| Invocation | Behavior |
|---|---|
| **plan-open** (caller: `/plan`) | rename → push → create draft → body from the plan → `/squash-message` |
| **`/pr`, no PR** | open from the commits already on the branch (the mid-session wrap-up: a session that started as brainstorming and produced commits) |
| **`/pr`, PR exists** | **refresh**: re-derive body and QA checklist from the real diff, re-run `/squash-message`, create nothing |

Every one of `/pr`'s seven callers is already a no-args caller: `/go` Step 4,
`branch-rename:27` (recreate a PR a rename killed), `finalize:13` (no-PR branch →
draft), `sync-upstream:260` (ported commits, no plan), a hydrated `/release` and
`/hotfix` per `squash-message:40`, and the bare mid-session form.

### Revert the duplicate-PR guard

`gh pr view … → stop and report` becomes refresh mode. The guard carries three
jobs today and only the first survives intact:

1. Turning `gh pr create`'s refusal of a second open PR for the same head→base
   into an actionable message. **Survives** — refresh mode is the actionable
   outcome.
2. Making `/go` Step 4 and `/handle` → `/go` § "Planless entry" idempotent when
   they land on a branch that already has a PR (`implement/SKILL.md:35` names
   this). **Inverts**: an existing PR becomes the expected end state, and the
   right response is to fill it in.
3. Steering an operator who meant `/finalize`. **Survives** as a line in refresh
   mode's report, not as a stop.

## Move 4 — `/implement` → `/go`

`git mv .claude/skills/implement .claude/skills/go`, plus a stub at the old path.

The rename converges the command with vocabulary already in the tree: `/plan`
§ "The approval gate" lists the tokens it accepts — *"go ahead", "let's go
ahead", "implement", "ship it", "do it", "proceed", "lgtm go"*. Under moves 2 and
3 the skill stopped meaning "execute an approved plan" and became the universal
go-ahead (bare = same-session, `<branch>` = attach and go, `<task>` = planless
go). `/go` is the word that gate is already listening for.

### Argument disambiguation

`/go` takes three argument shapes, and two can collide: a terse `/go
fix-sidebar-scroll` could be a branch or a task. The rule reuses a check
`/from-branch` Step 1 already runs:

> A first token that resolves to an existing branch or PR
> (`git ls-remote --heads origin <token>`, or a `#NNN`/PR URL) is a **target**.
> Anything else is a **task**.

The § "Branch-name form" canary is unaffected — it fires on *bare* `/go` as a
session's first prompt, which stays distinct from `/go <anything>`.

### The stub is permanent, and it says "load and follow"

`.claude/skills/implement/SKILL.md` survives as a redirect to
`@.claude/skills/go/SKILL.md`. It is load-bearing rather than courtesy: `/plan`'s
handoff block is a **copyable command pasted into a fresh session**, so every
in-flight branch whose plan file or PR comment already carries `/implement
<branch>` is a live user of the old name — and those comments outlive the
rename indefinitely. A description-only alias does not cover a literal
`/implement`, since the slash command is the directory name.

It keeps the "load and follow" imperative for the reason `/handle`'s Do-NOT
gives: *acting on a referenced skill from the one-line summary this file gives
it* is the named failure, and a stub is nothing but a one-line summary.

### Two things the rename must not touch

- **The plan lifecycle suffix `*.draft.do-not-implement.md` stays.** That
  "implement" is plain English on a tripwire, not a command reference — the
  warning stands however the skill is named, and `*.do-not-go.md` would be
  strictly worse as one.
- **`/from-branch` Step 6's follow-up keywords** (`implement` / `execute`) gain
  `go` rather than losing the old ones. This is prose matching, not a pointer, so
  `check-skill-catalog.sh` cannot catch it.

### A note for adopters

`/go` reads ambiguously in a Go project, and this is a stack-agnostic
boilerplate. `docs/catalog.md`'s row gets a line saying the name is a local
choice, not a contract — adopters should rename it to whatever their
language or framework leaves unambiguous, and `check-skill-catalog.sh` will
verify the pointers after they do.

## Files

**Substantive:**

| File | Change |
|---|---|
| `.claude/skills/implement/` → `.claude/skills/go/` | `git mv`; frontmatter; § "Branch-name form" gains the target-vs-task rule; § "Planless entry" becomes operator-facing; Step 4 refreshes rather than opens |
| `.claude/skills/implement/SKILL.md` (new) | permanent redirect stub |
| `.claude/skills/pr/SKILL.md` | Step 1a deletes; the three-mode table; Step 1b guard → refresh; frontmatter loses the task argument |
| `.claude/skills/plan/SKILL.md` | final publish step; handoff block gains the PR URL; predicate home in § "Plan file lifecycle"; approval gate gains the review-comment channel |
| `.claude/skills/handle/SKILL.md` | Step 2 both-lanes stop → plan-review reading; go-ahead sentence gains its exception |
| `.claude/skills/qa-checklist/SKILL.md` | Step 2 accepts the plan as input; the two `/pr`-composes-at-creation notes (lines 10, 22) |
| `.claude/skills/squash-message/SKILL.md` | Step 1 gather-from-plan; opening gains the plan-condensed rationale |
| `.claude/skills/issue/SKILL.md` | End state; the chain line (line 7); Step 4 hands to `/plan`, not `/pr` |
| `.claude/skills/from-branch/SKILL.md` | Step 6 keyword list gains `go`; pointers |

**Pointers** — 15 `@…/implement/SKILL.md` references and 50 literal `/implement`
mentions across nine files. The pointers are caught by the catalog check; the
prose is not, so it is swept by hand:

| File | Change |
|---|---|
| `CLAUDE.md` | main-loop bullets (`/pr` demoted to "Mechanical pieces"); § "Plan mode & questions in web sessions"; "rename … right after the first commit" → before it |
| `docs/catalog.md` | rows for `go` (new), `implement` (stub), `pr`, `plan`, `handle`, `issue`; the adopter note |
| `.claude/skills/audit-github-backlog/SKILL.md` | three `/implement` mentions |

`check-merge:54` and `branch-rename/SKILL.md` need no edit — both stay true.

Verification is `bash scripts/check-skill-catalog.sh`, plus
`grep -rn "/implement\b"` returning only the stub, the lifecycle suffix, and
deliberate historical references.

## DRY notes

- **The "implementation has begun" predicate** is the one genuinely new shared
  fact, and it would otherwise be stated in three places (`/handle` Step 2,
  `/handle`'s go-ahead sentence, `/plan`'s approval gate). One home in `/plan`
  § "Plan file lifecycle", which already owns the state machine; the other two
  cite it. This is CLAUDE.md § "Writing things down" — *if the same constraint is
  stated in two places, one of them is the home and the other is a pointer.*
- **QA-checklist derivation** stays single-sourced in `/qa-checklist` Step 2, and
  **squash-message format** in `/squash-message`. `/pr` keeps delegating to both
  by reference in every mode. What gains a second shape is `/qa-checklist`'s
  *input*, not a copy of its rules.
- **The handoff block format** stays in `/plan` § "Handing off". `/pr` plan-open
  mode does not restate it — `/plan` emits it, since `/plan` ends that turn.
- **The target-vs-task check** reuses `/from-branch` Step 1's existing
  `git ls-remote` resolution rather than adding a parallel one. `/go` cites it.
- **No shared "PR mode" abstraction.** The three modes are a table inside `/pr`,
  not a fourth skill. Extracting them would add a load hop for zero reuse — every
  caller touches exactly one cell and reaches it through `/pr` already.
- **The stub is a pointer, not a fork.** It carries no procedure of its own, so
  there is nothing in it to drift from `/go`.

## The predicate

> **Implementation has begun** iff `docs/plans/` holds at least one file that is
> not `*.draft.do-not-implement.md` — that is, any `*.in-progress.md`,
> `*.paused.md` or `*.completed.md`.

Home: `@.claude/skills/plan/SKILL.md` § "Plan file lifecycle".

It is deliberately broader than the case that motivates it. The common shape is a
branch carrying nothing but a draft plan and a squash message, where "are we
still planning?" is obvious. The broad form also handles the mixed branch — one
plan completed, then paused, then a follow-up draft opened, with a review
touching both the new plan and the shipped code. A draft plan being present is
the tell that the branch is back in planning, whatever sits beside it.

## `/handle` gets a condition, not a third lane

`/handle` Step 2 currently calls both lanes firing at once abnormal and stops.
Under move 1 that is the *normal* state of a plan under review, so the stop
becomes a reading:

- **Draft plan + unanswered feedback** → the feedback is review *of the plan*.
  Stay in plan mode: revise the plan file, reply on GitHub per CLAUDE.md
  § "GitHub comments", push, re-emit the handoff block. Do **not** flip the plan
  file, do **not** touch source.
- **No draft plan + unanswered feedback** → today's review lane, unchanged.
- **Draft plan + no unanswered feedback** → today's plan lane, unchanged: the
  invocation is the go-ahead.

That last bullet is why no third lane is needed. `/handle` stays a go-ahead by
default; only the conjunction suspends it, so `handle/SKILL.md:17` gains one
exception rather than being rewritten.

`/plan` § "The approval gate" already draws the right distinction — *a suggestion
is a plan revision; only a go-ahead token unlocks implementation*. It only needs
to learn that both can arrive as PR review comments. No change to what counts as
either.

## Open questions

**1. `[no ci]` on plan-phase commits — in scope, or filed separately?**
`/squash-message` Step 5 says to add `[no ci]` only on a **non-draft** PR, which
implies draft PRs don't burn CI runs. That is false in general: GitHub Actions
`pull_request` workflows fire on draft PRs by default; suppressing them takes an
explicit `if: github.event.pull_request.draft == false`. Under move 1 a branch
sits in draft far longer, so any adopter with PR workflows pays for every
plan-phase push.
Moot for this repo — there is no `.github/` here — which is why the
recommendation is **(a) file it separately** rather than (b) widen this PR.
*(a) is in force in this plan.*
