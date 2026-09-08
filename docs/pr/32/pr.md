# PR #32: feat: give each loop skill one thing to own

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/32
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/pr-first-plan-review-28eed7
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-08T17:44:46Z
- **Updated:** 2026-09-08T22:27:20Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

Four moves, each **removing** a responsibility from a skill that acquired it by accident. The result is one job per skill: `/plan` owns plan content *and publishing it*, `/go` owns task entry and execution, `/pr` owns the PR object.

- **The draft PR opens at plan time**, over the plan commit — so the plan file is a reviewable diff, and `/handle` on that branch processes plan feedback the way it already processes code feedback.
- **`/plan` publishes its own plan.** The trigger belongs where the plan becomes pushed, so *every* entry into planning gets a PR — including a direct `/plan`, which CLAUDE.md names as the default entry for a new web session and which hanging this off `/pr`'s argument would have missed.
- **`/pr` stops taking a task argument.** Step 1a deletes outright, along with the most defensive prose in the tree, which existed only to guard an argument `/pr` had no business accepting. What remains is three modes over the PR object — one of them the duplicate-PR guard inverted into a **refresh**, since an existing PR is now the expected state at the end of implementation.
- **`/implement` becomes `/go`**, converging the command with the tokens `/plan`'s approval gate already listens for. The old path stays as a permanent redirect stub: the handoff block is a copyable command living in plan files and PR comments that outlive the rename.

One predicate carries the review loop — *implementation has begun iff `docs/plans/` holds a file that is not a draft* — which is what lets `/handle` tell plan review from code review without growing a third lane.

**This PR is its own first instance.** Branch renamed before the plan existed, PR opened over the plan commit, squash proposal posted as a comment, and every revision since has landed as a plan edit rather than a code change. The plan under `docs/plans/` is the thing to review.

## QA Checklist

- [ ] `catalog` — `bash scripts/check-skill-catalog.sh` passes: every `@.claude/skills/…` pointer resolves and every skill has exactly one `docs/catalog.md` row.
- [ ] `no-stale-implement` — `grep -rn "/implement\b"` returns only the redirect stub, the `*.draft.do-not-implement.md` lifecycle suffix, and deliberate historical references. 15 pointers and 50 prose mentions are in scope; the catalog check covers only the pointers.
- [ ] `stub-redirect` — a literal `/implement <branch>` still reaches `/go`, via the stub at the old path.
- [ ] `plan-publishes` — a bare `/plan` (no `/pr`, no `/issue`) ends with a pushed plan, a draft PR over the plan commit, a squash comment, and a handoff block carrying the PR URL.
- [ ] `pr-refresh` — `/pr` on a branch that already has a PR re-derives body and QA checklist from the real diff, re-runs `/squash-message`, creates nothing, and does **not** stop-and-report.
- [ ] `pr-no-task-arg` — `/pr <some task>` is no longer a valid shape; the operator is routed to `/plan` or `/go`.
- [ ] `go-target-vs-task` — `/go <existing-branch>` attaches; `/go <prose task>` runs planless. Disambiguated by `git ls-remote --heads origin <token>`, reusing `/from-branch` Step 1's check.
- [ ] `handle-plan-review` — `/handle <branch>` with a draft plan **and** unanswered feedback revises the plan, replies on GitHub, pushes, re-emits the handoff; it does **not** flip the plan file or touch source.
- [ ] `handle-regressions` — draft plan + no feedback is still a go-ahead; no draft plan + feedback is still the ordinary code-review lane.
- [ ] `qa-from-plan` — `/qa-checklist` Step 2 accepts an approved plan as input alongside `origin/<base>..HEAD`.
- [ ] `finalize-sweep` — `/finalize` still `git rm -r`s `docs/plans/` and `docs/remove-before-merging/`, so the add-then-delete pairs cancel in the squash and neither reaches `main`.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `catalog` | yes | yes | `scripts/check-skill-catalog.sh` |
| `no-stale-implement` | yes | no | One `grep`; the allowlist is the judgement half |
| `stub-redirect` | no | no | Behavioral |
| `plan-publishes` | no | no | Behavioral; the move that reaches the most-used entry |
| `pr-refresh` | no | no | Behavioral; exercised when `/go` closes this branch out |
| `pr-no-task-arg` | partially | no | `grep` the frontmatter; the routing is a read |
| `go-target-vs-task` | no | no | Behavioral; the one genuinely ambiguous input shape |
| `handle-plan-review` | no | no | Behavioral; verified by reviewing this PR and running `/handle` |
| `handle-regressions` | no | no | Behavioral; two regression checks on existing lanes |
| `qa-from-plan` | no | no | Prose contract |
| `finalize-sweep` | no | no | Behavioral; exercised at `/finalize` time |

Prose-only change to `.claude/skills/` plus two pointer files. `scripts/vet.sh` is an unhydrated stub in this repo and there is no `.github/`, so `check-skill-catalog.sh` and the `grep` are the whole automatable gate.

https://claude.ai/code/session_01XUq5KMhf3B7bLSeXuxNmMS


---

## Comments

### Comment by @vzakharov on 2026-09-08T17:45:20Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/32#issuecomment-5589397832](https://github.com/vzakharov/agent-project-boilerplate/pull/32#issuecomment-5589397832)

Proposed squash title/body:

```
feat: give each loop skill one thing to own (pr #32)
```

```
A plan file rode a PR-less branch until implementation finished, so the
operator could read it but could not review it the way they review
everything else here: no inline comments, no threads, no diff view.
Fixing that meant opening the draft PR at plan time, and pulling on it
turned up three more places where a skill was doing a neighbour's job.
Each is now a responsibility removed rather than added.

/plan publishes its own plan. The draft PR opens over the plan commit,
making the plan a reviewable diff, and the trigger sits in /plan because
that is where the plan becomes pushed — so every entry into planning
gets a PR, not only the ones that arrived through /pr. That leaves /pr
with no reason to take a task argument: new work is /plan, unplanned
work is /go, and Step 1a's plan gate deletes outright along with the
defensive prose that existed only to guard an argument /pr should never
have accepted. What remains is three modes over the PR object, one of
them the old duplicate-PR guard inverted into a refresh: an existing PR
is the expected state at the end of implementation, so it gets filled
in rather than declined. The QA checklist and squash proposal are
written from the plan at open time and reconciled against the real diff
at refresh, which keeps both derivations single-sourced and only gives
one of them a second input shape.

/implement becomes /go, converging the command with the vocabulary
/plan's approval gate already listens for, and the skill it names is no
longer "execute an approved plan" but every shape of starting work. The
old path stays as a permanent redirect stub, because the handoff block
is a copyable command living in plan files and PR comments that outlive
the rename. Two things deliberately keep the old word: the
*.draft.do-not-implement.md suffix, where it is a warning rather than a
command, and /from-branch's follow-up keywords, which gain "go" instead
of trading it.

One predicate carries the review loop: implementation has begun iff
docs/plans/ holds a file that is not a draft. It lets /handle read a
draft plan plus unanswered feedback as review of the plan — revise,
reply, push, hand off again — while the same feedback without a draft
plan stays the ordinary code-review lane, and a draft plan without
feedback stays an ordinary go-ahead. That is why no third lane appears.
It is defined once, in /plan's plan-file lifecycle section; anyone
restating it elsewhere has created the drift the arrangement prevents.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:73 — unresolved

```diff
@@ -0,0 +1,294 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Give each loop skill one thing to own
+
+## Why
+
+A plan file rides a PR-less branch until implementation finishes. The operator
+can read it, but cannot review it the way they review everything else in this
+project: no inline comments, no threads, no diff view. Feedback arrives as chat
+prose instead — a worse surface than the one already in use for code.
+
+Fixing that means opening the draft PR at plan time. Pulling on it turns up
+three more places where a skill is doing a job that belongs to a neighbour, and
+they are cheaper to fix together than separately: each one is *removing* a
+responsibility from a skill that acquired it by accident.
+
+## The four moves
+
+1. **The draft PR opens at plan time**, over the plan commit, so the plan file is
+   a reviewable diff and `/handle` on that branch processes plan feedback the way
+   it already processes code feedback.
+2. **`/plan` publishes its own plan.** The trigger is "a plan exists and is
+   pushed", which is `/plan`'s event — so *every* entry into `/plan` gets a PR,
+   not just the ones that arrived through `/pr`.
+3. **`/pr` stops accepting a task argument.** New work is `/plan`; unplanned work
+   is `/go` (below). `/pr` is left owning the PR object alone.
+4. **`/implement` becomes `/go`**, which is what the approval gate has been
+   listening for all along.
+
+Together they reassign three ownerships:
+
+| Skill | Owns |
+|---|---|
+| `/plan` | plan content — the file, the questions, the approval gate, the lifecycle names — **and publishing it** |
+| `/go` | task entry and execution — every shape of "start working" |
+| `/pr` | the PR object — create vs. refresh, title, body, base, draft state |
+
+## Move 1 — the PR opens at plan time
+
+Today: `/issue` → `/pr <task>` → **stop** → `/plan` → (new session) `/implement`
+→ `/pr` opens the PR → `/finalize`.
+
+After: `/issue` → `/plan` → plan committed → **`/plan` opens the draft PR** →
+`/squash-message` → handoff → (review loop via `/handle`) → (new session) `/go`
+→ `/pr` **refreshes** → `/finalize`.
+
+Everything after the plan commit — push, create, body, squash proposal — runs in
+the same turn it runs in today, over a plan commit instead of implementation
+commits.
+
+### The QA checklist is written from the plan
+
+At PR-open time there is no diff, but there is a statement of what will be
+delivered — which is what a QA checklist is derived from anyway. `/qa-checklist`
+Step 2 gains the plan as an accepted input alongside `origin/<base>..HEAD`, and
+refresh mode re-derives it against the real diff so the forecast is reconciled
+with what shipped. The derivation stays single-sourced; only its input gains a
+second shape.
+
+### The squash message is the plan condensed
+
+At plan time the proposal is *the plan as it would be recorded* — a second, much
+shorter read of the same decision, in front of the operator before any code
+exists. `/squash-message` needs two edits: Step 1 "Gather" learns that a branch
+carrying only a plan commit has the plan as its input rather than `git log`, and
+the opening gains that rationale.
+
+Its "created once, when the PR opens" rule needs no change — the sentence stays
+true, the moment just moves earlier.
+
+**One ordering constraint:** the title carries a `(pr #N)` suffix, so the
+proposal cannot be composed before the PR number exists. The squash file lands in
+the push immediately *after* creation, within the same turn — which is why `/pr`
```

**@vzakharov** — 2026-09-08T22:19:47Z

I think it needlessly complicates the process; we can just open with (pr #tbd) and change it at any next editing stage

---

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:113 — unresolved

```diff
@@ -0,0 +1,294 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Give each loop skill one thing to own
+
+## Why
+
+A plan file rides a PR-less branch until implementation finishes. The operator
+can read it, but cannot review it the way they review everything else in this
+project: no inline comments, no threads, no diff view. Feedback arrives as chat
+prose instead — a worse surface than the one already in use for code.
+
+Fixing that means opening the draft PR at plan time. Pulling on it turns up
+three more places where a skill is doing a job that belongs to a neighbour, and
+they are cheaper to fix together than separately: each one is *removing* a
+responsibility from a skill that acquired it by accident.
+
+## The four moves
+
+1. **The draft PR opens at plan time**, over the plan commit, so the plan file is
+   a reviewable diff and `/handle` on that branch processes plan feedback the way
+   it already processes code feedback.
+2. **`/plan` publishes its own plan.** The trigger is "a plan exists and is
+   pushed", which is `/plan`'s event — so *every* entry into `/plan` gets a PR,
+   not just the ones that arrived through `/pr`.
+3. **`/pr` stops accepting a task argument.** New work is `/plan`; unplanned work
+   is `/go` (below). `/pr` is left owning the PR object alone.
+4. **`/implement` becomes `/go`**, which is what the approval gate has been
+   listening for all along.
+
+Together they reassign three ownerships:
+
+| Skill | Owns |
+|---|---|
+| `/plan` | plan content — the file, the questions, the approval gate, the lifecycle names — **and publishing it** |
+| `/go` | task entry and execution — every shape of "start working" |
+| `/pr` | the PR object — create vs. refresh, title, body, base, draft state |
+
+## Move 1 — the PR opens at plan time
+
+Today: `/issue` → `/pr <task>` → **stop** → `/plan` → (new session) `/implement`
+→ `/pr` opens the PR → `/finalize`.
+
+After: `/issue` → `/plan` → plan committed → **`/plan` opens the draft PR** →
+`/squash-message` → handoff → (review loop via `/handle`) → (new session) `/go`
+→ `/pr` **refreshes** → `/finalize`.
+
+Everything after the plan commit — push, create, body, squash proposal — runs in
+the same turn it runs in today, over a plan commit instead of implementation
+commits.
+
+### The QA checklist is written from the plan
+
+At PR-open time there is no diff, but there is a statement of what will be
+delivered — which is what a QA checklist is derived from anyway. `/qa-checklist`
+Step 2 gains the plan as an accepted input alongside `origin/<base>..HEAD`, and
+refresh mode re-derives it against the real diff so the forecast is reconciled
+with what shipped. The derivation stays single-sourced; only its input gains a
+second shape.
+
+### The squash message is the plan condensed
+
+At plan time the proposal is *the plan as it would be recorded* — a second, much
+shorter read of the same decision, in front of the operator before any code
+exists. `/squash-message` needs two edits: Step 1 "Gather" learns that a branch
+carrying only a plan commit has the plan as its input rather than `git log`, and
+the opening gains that rationale.
+
+Its "created once, when the PR opens" rule needs no change — the sentence stays
+true, the moment just moves earlier.
+
+**One ordering constraint:** the title carries a `(pr #N)` suffix, so the
+proposal cannot be composed before the PR number exists. The squash file lands in
+the push immediately *after* creation, within the same turn — which is why `/pr`
+Step 6 already sits where it does. From the operator's side both files are on the
+PR when they first open it.
+
+## Move 2 — `/plan` publishes
+
+`/plan` gains a final step: hand to `/pr` in **plan-open mode** to rename, push,
+create the draft, compose the body, and invoke `/squash-message`. Then emit the
+handoff block, now carrying the PR URL.
+
+Putting the trigger here rather than in `/pr` is what makes the change reach the
+common case. CLAUDE.md § "Plan mode & questions in web sessions" names `/plan` as
+the default entry for a new web session — more common than `/pr <task>` or
+`/issue`. Hanging PR-creation off `/pr`'s argument would leave that entry with a
+PR-less branch, giving the least benefit to the most-used path.
+
+`/pr` still owns the `gh` mechanics; `/plan` owns only the decision to publish.
+
+## Move 3 — `/pr` takes no task argument
+
+`/pr`'s Step 1a — the plan gate — **deletes entirely**. Both of its branches move
+out:
+
+- `/pr <task>` → `/plan`, which now publishes (move 2).
+- `/pr <task> no plan` → `/go <task>`. This was already a longer spelling of the
+  same thing: Step 1a's waiver routes to `/implement` § "Planless entry", whose
+  first line is *"A caller skill may enter here with a **task** in place of a
+  plan."* The change makes that front door operator-facing.
+
+Step 1a is the longest and most defensive prose in the tree — *"the **only**
+waiver is…"*, *"not because the task looks small, well-specified, or like a tweak
+to existing work"* — and all of it exists to guard an argument `/pr` has no
+business accepting. Remove the argument and the guard has nothing to guard.
+
+What remains is a no-args skill with three modes:
+
+| Invocation | Behavior |
+|---|---|
+| **plan-open** (caller: `/plan`) | rename → push → create draft → body from the plan → `/squash-message` |
+| **`/pr`, no PR** | open from the commits already on the branch (the mid-session wrap-up: a session that started as brainstorming and produced commits) |
+| **`/pr`, PR exists** | **refresh**: re-derive body and QA checklist from the real diff, re-run `/squash-message`, create nothing |
```

**@vzakharov** — 2026-09-08T22:22:05Z

in which points of our flow does this (legitimately) happen?

---

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:154 — unresolved

```diff
@@ -0,0 +1,294 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Give each loop skill one thing to own
+
+## Why
+
+A plan file rides a PR-less branch until implementation finishes. The operator
+can read it, but cannot review it the way they review everything else in this
+project: no inline comments, no threads, no diff view. Feedback arrives as chat
+prose instead — a worse surface than the one already in use for code.
+
+Fixing that means opening the draft PR at plan time. Pulling on it turns up
+three more places where a skill is doing a job that belongs to a neighbour, and
+they are cheaper to fix together than separately: each one is *removing* a
+responsibility from a skill that acquired it by accident.
+
+## The four moves
+
+1. **The draft PR opens at plan time**, over the plan commit, so the plan file is
+   a reviewable diff and `/handle` on that branch processes plan feedback the way
+   it already processes code feedback.
+2. **`/plan` publishes its own plan.** The trigger is "a plan exists and is
+   pushed", which is `/plan`'s event — so *every* entry into `/plan` gets a PR,
+   not just the ones that arrived through `/pr`.
+3. **`/pr` stops accepting a task argument.** New work is `/plan`; unplanned work
+   is `/go` (below). `/pr` is left owning the PR object alone.
+4. **`/implement` becomes `/go`**, which is what the approval gate has been
+   listening for all along.
+
+Together they reassign three ownerships:
+
+| Skill | Owns |
+|---|---|
+| `/plan` | plan content — the file, the questions, the approval gate, the lifecycle names — **and publishing it** |
+| `/go` | task entry and execution — every shape of "start working" |
+| `/pr` | the PR object — create vs. refresh, title, body, base, draft state |
+
+## Move 1 — the PR opens at plan time
+
+Today: `/issue` → `/pr <task>` → **stop** → `/plan` → (new session) `/implement`
+→ `/pr` opens the PR → `/finalize`.
+
+After: `/issue` → `/plan` → plan committed → **`/plan` opens the draft PR** →
+`/squash-message` → handoff → (review loop via `/handle`) → (new session) `/go`
+→ `/pr` **refreshes** → `/finalize`.
+
+Everything after the plan commit — push, create, body, squash proposal — runs in
+the same turn it runs in today, over a plan commit instead of implementation
+commits.
+
+### The QA checklist is written from the plan
+
+At PR-open time there is no diff, but there is a statement of what will be
+delivered — which is what a QA checklist is derived from anyway. `/qa-checklist`
+Step 2 gains the plan as an accepted input alongside `origin/<base>..HEAD`, and
+refresh mode re-derives it against the real diff so the forecast is reconciled
+with what shipped. The derivation stays single-sourced; only its input gains a
+second shape.
+
+### The squash message is the plan condensed
+
+At plan time the proposal is *the plan as it would be recorded* — a second, much
+shorter read of the same decision, in front of the operator before any code
+exists. `/squash-message` needs two edits: Step 1 "Gather" learns that a branch
+carrying only a plan commit has the plan as its input rather than `git log`, and
+the opening gains that rationale.
+
+Its "created once, when the PR opens" rule needs no change — the sentence stays
+true, the moment just moves earlier.
+
+**One ordering constraint:** the title carries a `(pr #N)` suffix, so the
+proposal cannot be composed before the PR number exists. The squash file lands in
+the push immediately *after* creation, within the same turn — which is why `/pr`
+Step 6 already sits where it does. From the operator's side both files are on the
+PR when they first open it.
+
+## Move 2 — `/plan` publishes
+
+`/plan` gains a final step: hand to `/pr` in **plan-open mode** to rename, push,
+create the draft, compose the body, and invoke `/squash-message`. Then emit the
+handoff block, now carrying the PR URL.
+
+Putting the trigger here rather than in `/pr` is what makes the change reach the
+common case. CLAUDE.md § "Plan mode & questions in web sessions" names `/plan` as
+the default entry for a new web session — more common than `/pr <task>` or
+`/issue`. Hanging PR-creation off `/pr`'s argument would leave that entry with a
+PR-less branch, giving the least benefit to the most-used path.
+
+`/pr` still owns the `gh` mechanics; `/plan` owns only the decision to publish.
+
+## Move 3 — `/pr` takes no task argument
+
+`/pr`'s Step 1a — the plan gate — **deletes entirely**. Both of its branches move
+out:
+
+- `/pr <task>` → `/plan`, which now publishes (move 2).
+- `/pr <task> no plan` → `/go <task>`. This was already a longer spelling of the
+  same thing: Step 1a's waiver routes to `/implement` § "Planless entry", whose
+  first line is *"A caller skill may enter here with a **task** in place of a
+  plan."* The change makes that front door operator-facing.
+
+Step 1a is the longest and most defensive prose in the tree — *"the **only**
+waiver is…"*, *"not because the task looks small, well-specified, or like a tweak
+to existing work"* — and all of it exists to guard an argument `/pr` has no
+business accepting. Remove the argument and the guard has nothing to guard.
+
+What remains is a no-args skill with three modes:
+
+| Invocation | Behavior |
+|---|---|
+| **plan-open** (caller: `/plan`) | rename → push → create draft → body from the plan → `/squash-message` |
+| **`/pr`, no PR** | open from the commits already on the branch (the mid-session wrap-up: a session that started as brainstorming and produced commits) |
+| **`/pr`, PR exists** | **refresh**: re-derive body and QA checklist from the real diff, re-run `/squash-message`, create nothing |
+
+Every one of `/pr`'s seven callers is already a no-args caller: `/go` Step 4,
+`branch-rename:27` (recreate a PR a rename killed), `finalize:13` (no-PR branch →
+draft), `sync-upstream:260` (ported commits, no plan), a hydrated `/release` and
+`/hotfix` per `squash-message:40`, and the bare mid-session form.
+
+### Revert the duplicate-PR guard
+
+`gh pr view … → stop and report` becomes refresh mode. The guard carries three
+jobs today and only the first survives intact:
+
+1. Turning `gh pr create`'s refusal of a second open PR for the same head→base
+   into an actionable message. **Survives** — refresh mode is the actionable
+   outcome.
+2. Making `/go` Step 4 and `/handle` → `/go` § "Planless entry" idempotent when
+   they land on a branch that already has a PR (`implement/SKILL.md:35` names
+   this). **Inverts**: an existing PR becomes the expected end state, and the
+   right response is to fill it in.
+3. Steering an operator who meant `/finalize`. **Survives** as a line in refresh
+   mode's report, not as a stop.
+
+## Move 4 — `/implement` → `/go`
+
+`git mv .claude/skills/implement .claude/skills/go`, plus a stub at the old path.
+
+The rename converges the command with vocabulary already in the tree: `/plan`
+§ "The approval gate" lists the tokens it accepts — *"go ahead", "let's go
+ahead", "implement", "ship it", "do it", "proceed", "lgtm go"*. Under moves 2 and
+3 the skill stopped meaning "execute an approved plan" and became the universal
+go-ahead (bare = same-session, `<branch>` = attach and go, `<task>` = planless
+go). `/go` is the word that gate is already listening for.
+
+### Argument disambiguation
+
+`/go` takes three argument shapes, and two can collide: a terse `/go
+fix-sidebar-scroll` could be a branch or a task. The rule reuses a check
+`/from-branch` Step 1 already runs:
+
+> A first token that resolves to an existing branch or PR
+> (`git ls-remote --heads origin <token>`, or a `#NNN`/PR URL) is a **target**.
+> Anything else is a **task**.
```

**@vzakharov** — 2026-09-08T22:25:03Z

I'd say the chance of an actual task an operator sends looking like a branch (or vice-versa) is exceedingly small, especially given that branches are virtually always claude/something (ok, maybe cursor/something or codex/something). Checking that a branch doesn't exist and concluding "oh, this must be a task then" is worse than stopping and asking (example: the operator accidentally sent the session prompt tied to a different repo)

---

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:159 — unresolved

```diff
@@ -0,0 +1,294 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Give each loop skill one thing to own
+
+## Why
+
+A plan file rides a PR-less branch until implementation finishes. The operator
+can read it, but cannot review it the way they review everything else in this
+project: no inline comments, no threads, no diff view. Feedback arrives as chat
+prose instead — a worse surface than the one already in use for code.
+
+Fixing that means opening the draft PR at plan time. Pulling on it turns up
+three more places where a skill is doing a job that belongs to a neighbour, and
+they are cheaper to fix together than separately: each one is *removing* a
+responsibility from a skill that acquired it by accident.
+
+## The four moves
+
+1. **The draft PR opens at plan time**, over the plan commit, so the plan file is
+   a reviewable diff and `/handle` on that branch processes plan feedback the way
+   it already processes code feedback.
+2. **`/plan` publishes its own plan.** The trigger is "a plan exists and is
+   pushed", which is `/plan`'s event — so *every* entry into `/plan` gets a PR,
+   not just the ones that arrived through `/pr`.
+3. **`/pr` stops accepting a task argument.** New work is `/plan`; unplanned work
+   is `/go` (below). `/pr` is left owning the PR object alone.
+4. **`/implement` becomes `/go`**, which is what the approval gate has been
+   listening for all along.
+
+Together they reassign three ownerships:
+
+| Skill | Owns |
+|---|---|
+| `/plan` | plan content — the file, the questions, the approval gate, the lifecycle names — **and publishing it** |
+| `/go` | task entry and execution — every shape of "start working" |
+| `/pr` | the PR object — create vs. refresh, title, body, base, draft state |
+
+## Move 1 — the PR opens at plan time
+
+Today: `/issue` → `/pr <task>` → **stop** → `/plan` → (new session) `/implement`
+→ `/pr` opens the PR → `/finalize`.
+
+After: `/issue` → `/plan` → plan committed → **`/plan` opens the draft PR** →
+`/squash-message` → handoff → (review loop via `/handle`) → (new session) `/go`
+→ `/pr` **refreshes** → `/finalize`.
+
+Everything after the plan commit — push, create, body, squash proposal — runs in
+the same turn it runs in today, over a plan commit instead of implementation
+commits.
+
+### The QA checklist is written from the plan
+
+At PR-open time there is no diff, but there is a statement of what will be
+delivered — which is what a QA checklist is derived from anyway. `/qa-checklist`
+Step 2 gains the plan as an accepted input alongside `origin/<base>..HEAD`, and
+refresh mode re-derives it against the real diff so the forecast is reconciled
+with what shipped. The derivation stays single-sourced; only its input gains a
+second shape.
+
+### The squash message is the plan condensed
+
+At plan time the proposal is *the plan as it would be recorded* — a second, much
+shorter read of the same decision, in front of the operator before any code
+exists. `/squash-message` needs two edits: Step 1 "Gather" learns that a branch
+carrying only a plan commit has the plan as its input rather than `git log`, and
+the opening gains that rationale.
+
+Its "created once, when the PR opens" rule needs no change — the sentence stays
+true, the moment just moves earlier.
+
+**One ordering constraint:** the title carries a `(pr #N)` suffix, so the
+proposal cannot be composed before the PR number exists. The squash file lands in
+the push immediately *after* creation, within the same turn — which is why `/pr`
+Step 6 already sits where it does. From the operator's side both files are on the
+PR when they first open it.
+
+## Move 2 — `/plan` publishes
+
+`/plan` gains a final step: hand to `/pr` in **plan-open mode** to rename, push,
+create the draft, compose the body, and invoke `/squash-message`. Then emit the
+handoff block, now carrying the PR URL.
+
+Putting the trigger here rather than in `/pr` is what makes the change reach the
+common case. CLAUDE.md § "Plan mode & questions in web sessions" names `/plan` as
+the default entry for a new web session — more common than `/pr <task>` or
+`/issue`. Hanging PR-creation off `/pr`'s argument would leave that entry with a
+PR-less branch, giving the least benefit to the most-used path.
+
+`/pr` still owns the `gh` mechanics; `/plan` owns only the decision to publish.
+
+## Move 3 — `/pr` takes no task argument
+
+`/pr`'s Step 1a — the plan gate — **deletes entirely**. Both of its branches move
+out:
+
+- `/pr <task>` → `/plan`, which now publishes (move 2).
+- `/pr <task> no plan` → `/go <task>`. This was already a longer spelling of the
+  same thing: Step 1a's waiver routes to `/implement` § "Planless entry", whose
+  first line is *"A caller skill may enter here with a **task** in place of a
+  plan."* The change makes that front door operator-facing.
+
+Step 1a is the longest and most defensive prose in the tree — *"the **only**
+waiver is…"*, *"not because the task looks small, well-specified, or like a tweak
+to existing work"* — and all of it exists to guard an argument `/pr` has no
+business accepting. Remove the argument and the guard has nothing to guard.
+
+What remains is a no-args skill with three modes:
+
+| Invocation | Behavior |
+|---|---|
+| **plan-open** (caller: `/plan`) | rename → push → create draft → body from the plan → `/squash-message` |
+| **`/pr`, no PR** | open from the commits already on the branch (the mid-session wrap-up: a session that started as brainstorming and produced commits) |
+| **`/pr`, PR exists** | **refresh**: re-derive body and QA checklist from the real diff, re-run `/squash-message`, create nothing |
+
+Every one of `/pr`'s seven callers is already a no-args caller: `/go` Step 4,
+`branch-rename:27` (recreate a PR a rename killed), `finalize:13` (no-PR branch →
+draft), `sync-upstream:260` (ported commits, no plan), a hydrated `/release` and
+`/hotfix` per `squash-message:40`, and the bare mid-session form.
+
+### Revert the duplicate-PR guard
+
+`gh pr view … → stop and report` becomes refresh mode. The guard carries three
+jobs today and only the first survives intact:
+
+1. Turning `gh pr create`'s refusal of a second open PR for the same head→base
+   into an actionable message. **Survives** — refresh mode is the actionable
+   outcome.
+2. Making `/go` Step 4 and `/handle` → `/go` § "Planless entry" idempotent when
+   they land on a branch that already has a PR (`implement/SKILL.md:35` names
+   this). **Inverts**: an existing PR becomes the expected end state, and the
+   right response is to fill it in.
+3. Steering an operator who meant `/finalize`. **Survives** as a line in refresh
+   mode's report, not as a stop.
+
+## Move 4 — `/implement` → `/go`
+
+`git mv .claude/skills/implement .claude/skills/go`, plus a stub at the old path.
+
+The rename converges the command with vocabulary already in the tree: `/plan`
+§ "The approval gate" lists the tokens it accepts — *"go ahead", "let's go
+ahead", "implement", "ship it", "do it", "proceed", "lgtm go"*. Under moves 2 and
+3 the skill stopped meaning "execute an approved plan" and became the universal
+go-ahead (bare = same-session, `<branch>` = attach and go, `<task>` = planless
+go). `/go` is the word that gate is already listening for.
+
+### Argument disambiguation
+
+`/go` takes three argument shapes, and two can collide: a terse `/go
+fix-sidebar-scroll` could be a branch or a task. The rule reuses a check
+`/from-branch` Step 1 already runs:
+
+> A first token that resolves to an existing branch or PR
+> (`git ls-remote --heads origin <token>`, or a `#NNN`/PR URL) is a **target**.
+> Anything else is a **task**.
+
+The § "Branch-name form" canary is unaffected — it fires on *bare* `/go` as a
+session's first prompt, which stays distinct from `/go <anything>`.
+
+### The stub is permanent, and it says "load and follow"
```

**@vzakharov** — 2026-09-08T22:26:06Z

I'd say we should put somewhere that adopters should only take it if they've already taken implement before (i.e. those are not new adopters), in other cases they should just take "go" wholesale; and even existing adopters should ask the operator to decide whether to keep backwards comp or not

---

## Timeline (status, references, and other events)

- **2026-09-08T18:23:01Z** @vzakharov renamed from «docs: open the PR at plan time so plans get reviewed like code» to «feat: give each loop skill one thing to own».
- **2026-09-08T22:27:20Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/32#pullrequestreview-5147580260.
