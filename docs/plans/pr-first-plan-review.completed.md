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

**The `(pr #N)` suffix imposes no ordering.** The proposal composes with `(pr
#tbd)` when the number isn't known yet, and the real number lands at whatever
run next touches the comment. `/squash-message` § "When to (re)run" already
counts *"the PR being recreated under a different `(pr #N)`"* as a refresh
trigger, so filling in a placeholder rides a path that exists; `/finalize`
Step 5's reconciliation is what guarantees no `#tbd` reaches the trunk. Step 1
"Gather" gains the placeholder as its answer to a missing `gh pr view` number
rather than a precondition to wait on.

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
| **`/pr`, no PR** | open from the commits already on the branch |
| **`/pr`, PR exists** | **refresh**: re-compose the body against the real diff — Step 4 unchanged, `gh pr edit` in place of `gh pr create` |

`/pr` has eight callers under this plan — the seven it has today plus `/plan`'s
publish step — and all of them already invoke it with no args. Which mode each
reaches is decided by the branch, not by the caller:

| Caller | Mode |
|---|---|
| `/plan`'s publish step | **plan-open** — by construction there is no PR yet |
| `/go` Step 4 after a plan | **refresh** — `/plan` opened the PR at plan time |
| `/go` Step 4 via § "Planless entry" | **refresh** on an attached branch that has a PR (`implement/SKILL.md:35`'s case), **create** on one that doesn't |
| bare mid-session `/pr` | **refresh** where the PR predates the newer commits, **create** where brainstorming produced the branch's first PR-worthy state |
| `branch-rename:27` (a rename closed the PR) | **create** — the head ref is gone, so the PR is too |
| `finalize:13` (land prep on a PR-less branch) | **create** |
| `sync-upstream:260` (ported commits, no plan) | **create** |
| a hydrated `/release` / `/hotfix` per `squash-message:40` | either, per lane |

Create-from-commits is the planless lane's PR-open rather than a leftover:
nothing that went through `/plan` reaches it, and everything that deliberately
skipped planning does.

### Why `/go` still calls `/pr` when `/plan` already opened the PR

Because the body composed at plan time is a **forecast**, and the body is `/pr`'s
field. `/pr` Step 4 writes the Summary from the branch's commits and delegates
the QA section to `/qa-checklist`; at plan time both are written from the plan,
because there is no diff yet. By the end of `/go` there is one, and the body
still describes what the change was *going to* be. Reconciling it is the same
Step 4 composition against a different input — which is why refresh is a mode of
`/pr` and not new machinery, and why Step 5 needs only `gh pr edit` where it
would otherwise `gh pr create` (a clause `pr/SKILL.md:102` already carries for
its pre-created case).

**Refresh's own work is the body, and nothing more.** The two other jobs it
would be natural to hang here already belong elsewhere:

- **`/squash-message` re-runs itself.** Its § "When to (re)run" fires on any push
  that changes what the permanent record should say, which implementation pushes
  do, and `/finalize` Step 5 backstops it. Refresh cites that rule; it does not
  own a trigger.
- **`/qa-checklist` already edits an existing body** — its Steps 1 and 3 exist
  for exactly that, and refresh reaches them the way the operator does.

So the choice is narrow: either `/go` Step 4 keeps its single `/pr` line and the
Summary gets reconciled, or it calls `/qa-checklist` directly and the Summary —
the one section written entirely before the code existed — stays a forecast on a
merged PR. **This plan keeps the call.**

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

`/go` takes three argument shapes, and two of them are separated by shape alone:
**a task is prose, a target is a token.** No operator writes the work they want
done as a single whitespace-free string — not `fix-sidebar-scroll`, because
nobody hyphenates a sentence, and not `sidebar`, because a bare noun names a
subject rather than a job. So the classifier does not have to recognise ref
syntax, and must not narrow itself to it:

> A first argument that is a **single whitespace-free token** — `claude/foo-a1b2`,
> `fix-sidebar-scroll`, `sidebar`, `#NNN`, a PR URL — is a **target**. Confirm it
> with `/from-branch` Step 1's `git ls-remote --heads origin <token>`; if it does
> not resolve, **stop and ask**. An argument carrying whitespace is a **task**.

Testing for whitespace rather than for a `/` is what keeps the stop-and-ask
reachable: a `/`-shaped test reads `fix-sidebar-scroll` as a task and implements
it as one, which is the outcome the rule exists to prevent.

A token that fails to resolve must **not** fall through to "task". The likely
cause is a handoff block pasted into a session opened on the wrong repository,
and implementing a branch name as if it were a task description is the worst
available response — worse than one round-trip. This is § "Branch-name
form"'s reasoning applied to the argument: a handoff that did not land intact
gets a question, not a guess.

That canary is otherwise unaffected — it fires on *bare* `/go` as a session's
first prompt, which stays distinct from `/go <anything>`.

### The stub is permanent here, conditional downstream

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

Permanent applies to **this** repo, where `/implement` was the shipped name. For
a repo adopting from here the stub is conditional — see § "Notes for adopters".

### Two things the rename must not touch

- **The plan lifecycle suffix `*.draft.do-not-implement.md` stays.** That
  "implement" is plain English on a tripwire, not a command reference — the
  warning stands however the skill is named, and `*.do-not-go.md` would be
  strictly worse as one.
- **`/from-branch` Step 6's follow-up keywords** (`implement` / `execute`) gain
  `go` rather than losing the old ones. This is prose matching, not a pointer, so
  `check-skill-catalog.sh` cannot catch it.

### Notes for adopters

Two adopter-facing lines, both living in `docs/catalog.md` because that is the
file `@.claude/skills/sync-upstream/SKILL.md` Step 4a reads out of the source
clone when it offers a new skill path — so criteria written there reach the
adopting agent by construction.

**The name `/go` is a local choice, not a contract.** It reads ambiguously in a
Go project, and this is a stack-agnostic boilerplate. Adopters should rename it
to whatever their language or framework leaves unambiguous;
`check-skill-catalog.sh` verifies the pointers after they do.

**The `implement` stub is offered on a criterion, not adopted by default.** It
only carries value where `/implement` was already the shipped name, which is
exactly where a live handoff block might still say it. Its catalog row states
both cases:

- **Never adopted `/implement`** → take `go` alone and put
  `.claude/skills/implement/` in `declined`. There is no downstream caller to
  redirect, and the stub would be a permanent extra row in the skills list
  standing in for a name the repo never had.
- **Already adopted `/implement`** → the redirect is a real question rather than
  a default. Ask the operator whether the backwards compatibility is worth that
  extra row, and record either answer in `upstream.json` so Step 4a's "the
  question does not come back" holds.

## Files

**Substantive:**

| File | Change |
|---|---|
| `.claude/skills/implement/` → `.claude/skills/go/` | `git mv`; frontmatter; § "Branch-name form" becomes § "Argument shape" and gains the target-vs-task rule with its stop-and-ask (the old heading no longer covers a section that classifies tasks too); § "Planless entry" becomes operator-facing; Step 4 refreshes rather than opens |
| `.claude/skills/implement/SKILL.md` (new) | redirect stub; one line naming it a compatibility shim for repos that shipped `/implement` |
| `.claude/skills/pr/SKILL.md` | Step 1a deletes; the three-mode table; Step 1b guard → refresh; frontmatter loses the task argument |
| `.claude/skills/plan/SKILL.md` | final publish step; handoff block gains the PR URL; predicate home in § "Plan file lifecycle"; approval gate gains the review-comment channel |
| `.claude/skills/handle/SKILL.md` | Step 2 both-lanes stop → plan-review reading; go-ahead sentence gains its exception |
| `.claude/skills/qa-checklist/SKILL.md` | Step 2 accepts the plan as input; the two `/pr`-composes-at-creation notes (lines 10, 22) |
| `.claude/skills/squash-message/SKILL.md` | Step 1 gather-from-plan, and `(pr #tbd)` as its answer to an unknown number; opening gains the plan-condensed rationale |
| `.claude/skills/issue/SKILL.md` | End state; the chain line (line 7); Step 4 hands to `/plan`, not `/pr` |
| `.claude/skills/from-branch/SKILL.md` | Step 6 keyword list gains `go`; pointers |

**Pointers** — 15 `@…/implement/SKILL.md` references and 50 literal `/implement`
mentions across nine files. The pointers are caught by the catalog check; the
prose is not, so it is swept by hand:

| File | Change |
|---|---|
| `CLAUDE.md` | main-loop bullets (`/pr` demoted to "Mechanical pieces"); § "Plan mode & questions in web sessions"; "rename … right after the first commit" → before it |
| `docs/catalog.md` | rows for `go` (new), `implement` (stub), `pr`, `plan`, `handle`, `issue`; both adopter notes per § "Notes for adopters" |
| `.claude/skills/audit-github-backlog/SKILL.md` | three `/implement` mentions |
| `README.md` | the G2 group row, the § "Why /plan and /implement exist" heading and its handoff line |

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
  *input*, not a copy of its rules — and `/squash-message`'s **re-run trigger**
  stays its own, cited by refresh mode rather than restated there.
- **The handoff block format** stays in `/plan` § "Handing off". `/pr` plan-open
  mode does not restate it — `/plan` emits it, since `/plan` ends that turn.
- **The target-vs-task check** reuses `/from-branch` Step 1's existing
  `git ls-remote` resolution rather than adding a parallel one — as the
  confirmation step behind `/go`'s shape test, whose failure is a stop. `/go`
  cites it; the resolution itself stays in one place.
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
is a plan revision; only a go-ahead token unlocks implementation*. It gains one
restriction on the channel: a review comment is always the revision half, never
the go-ahead, so the only thing that unlocks source edits is an invocation —
`/go`, or a `/handle` finding no unanswered feedback. Review prose has too many
ways to read as assent for an agent to arbitrate.

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
