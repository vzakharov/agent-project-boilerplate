# PR #32: feat: give each loop skill one thing to own

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/32
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/pr-first-plan-review-28eed7
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-08T17:44:46Z
- **Updated:** 2026-09-09T00:51:40Z
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

**This PR is its own first instance.** Branch renamed before the plan existed, PR opened over the plan commit, squash proposal posted as a comment, the plan revised through four rounds of inline review, and implementation entered through `/handle` on the branch — the loop the plan describes, run once end to end before the diff that defines it.

## QA Checklist

- [x] `catalog` — `bash scripts/check-skill-catalog.sh` passes: every `@.claude/skills/…` pointer resolves and every skill has exactly one `docs/catalog.md` row.
- [x] `no-stale-implement` — `grep -rn "/implement\b"` returns only the redirect stub, the `*.draft.do-not-implement.md` lifecycle suffix, and deliberate historical references. 15 pointers and 50 prose mentions are in scope; the catalog check covers only the pointers.
- [ ] `stub-redirect` — a literal `/implement <branch>` still reaches `/go`, via the stub at the old path.
- [ ] `plan-publishes` — a bare `/plan` (no `/pr`, no `/issue`) ends with a pushed plan, a draft PR over the plan commit, a squash comment, and a handoff block carrying the PR URL.
- [ ] `pr-refresh` — `/pr` on a branch that already has a PR re-derives body and QA checklist from the real diff, re-runs `/squash-message`, creates nothing, and does **not** stop-and-report.
- [ ] `pr-no-task-arg` — `/pr <some task>` is no longer a valid shape; the operator is routed to `/plan` or `/go`.
- [ ] `go-target-vs-task` — `/go <existing-branch>` attaches; `/go <prose task>` runs planless; `/go <single token that does not resolve>` **stops and asks** rather than treating it as a task. A whitespace-free first argument is a target, confirmed by `/from-branch` Step 1's `git ls-remote --heads origin <token>`; anything carrying whitespace is a task. The rule lives in `/go` § "Argument shape" — the old § "Branch-name form" heading, renamed because the section now classifies tasks too.
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
| `pr-refresh` | no | no | Behavioral; exercised by the `/pr` call that wrote this body |
| `pr-no-task-arg` | partially | no | `grep` the frontmatter; the routing is a read |
| `go-target-vs-task` | no | no | Behavioral; three shapes, one of them a deliberate stop |
| `handle-plan-review` | no | no | Behavioral; leave a comment on the plan diff of the next planning PR |
| `handle-regressions` | no | no | Behavioral; two regression checks on existing lanes |
| `qa-from-plan` | no | no | Prose contract |
| `finalize-sweep` | no | no | Behavioral; exercised at `/finalize` time |

Prose-only change to `.claude/skills/` plus two pointer files. `scripts/vet.sh` is an unhydrated stub in this repo and there is no `.github/`, so `check-skill-catalog.sh` and the `grep` are the whole automatable gate.

https://claude.ai/code/session_01XUq5KMhf3B7bLSeXuxNmMS
https://claude.ai/code/session_01FAUK8YLwNU8Sy6wTVPQAcS



---
_Generated by [Claude Code](https://claude.ai/code)_

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
longer "execute an approved plan" but every shape of starting work.
Which shape is read off the argument by whitespace alone: one bare token
is a branch to attach to, confirmed by ls-remote and stopping to ask
when it does not resolve, and anything with a space in it is a task to
do. Testing for whitespace rather than for ref syntax is what keeps
fix-sidebar-scroll from being implemented as a sentence. The old path
stays as a redirect stub, because the handoff block is a
copyable command living in plan files and PR comments that outlive the
rename — permanent here, and offered downstream only to a repo that
shipped /implement, whose operator decides whether the compatibility is
worth the extra row. Two things deliberately keep the old word: the
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

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:73 — resolved

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

**@vzakharov** — 2026-09-08T22:31:39Z

Agreed — dropped the constraint. The proposal now composes with `(pr #tbd)` and the number lands at whatever run next touches the comment; `/squash-message` § "When to (re)run" already counts a changed `(pr #N)` as a refresh trigger, and `/finalize` Step 5 is what guarantees no `#tbd` reaches the trunk. 12c993c

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:113 — resolved

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

**@vzakharov** — 2026-09-08T22:31:45Z

Fair — the parenthetical named one example and skipped the answer. The caller list below is now a caller-to-mode table, and it answers this directly: after move 1 nothing that went through `/plan` reaches create-from-commits, and everything that deliberately skipped planning does — planless `/go`, `sync-upstream` ports, a PR a rename closed, `/finalize` on a PR-less branch, bare mid-session `/pr`. So it is the planless lane's PR-open, not a leftover. 12c993c

---
_Generated by [Claude Code](https://claude.ai/code)_

**@vzakharov** — 2026-09-08T22:55:01Z

I was asking about "/pr, PR exists" row -- did we understand each other?

**@vzakharov** — 2026-09-08T22:55:57Z

No, we did not — I read it as anchored on the row above and answered for `no PR`. Answering the row you asked about:

**Refresh is where planned work always lands.** After move 1 the PR exists from plan time, so every `/pr` call downstream of a plan finds one. The dominant instance is `/go` Step 4 at the end of implementation — the same call that *opens* the PR today. The second is `/go` § "Planless entry" attaching to a branch that already has a PR, which `implement/SKILL.md:35` already describes and today resolves as a stop. Third is a bare mid-session `/pr` where the PR predates the newer commits.

Correcting the table too: I had pinned planless-entry and bare `/pr` to **create**, and both actually reach either mode depending on the branch. 0f124ce

---
_Generated by [Claude Code](https://claude.ai/code)_

**@vzakharov** — 2026-09-08T22:59:13Z

Worth auditing, and it shrank the mode. Of the three jobs I had hung on refresh, two were already owned elsewhere: `/squash-message` § "When to (re)run" already fires on implementation pushes (with `/finalize` Step 5 as backstop), and `/qa-checklist` Steps 1 and 3 already edit an existing body.

What is left is one thing only `/pr` can do: **the body at plan time is a forecast.** Step 4 writes the Summary from the branch and delegates the QA section; with no diff yet, both come from the plan. By the end of `/go` there is a diff and the body still says what the change was *going to* be. That is Step 4's own composition over a different input, so refresh needs `gh pr edit` in place of `gh pr create` and nothing else — the clause at `pr/SKILL.md:102` already carries the mechanic.

So: one downstream caller, one reason. The alternative is `/go` Step 4 calling `/qa-checklist` directly and the Summary staying a forecast on a merged PR — the plan now names that and keeps the call. 7fa9012

---
_Generated by [Claude Code](https://claude.ai/code)_

**@vzakharov** — 2026-09-08T23:01:45Z

**Outcome, for the record:** settled on keeping the one downstream call.

- `/go` Step 4 still invokes `/pr`, and the reason is the body — composed from the plan at open time, reconciled against the real diff at the end of implementation.
- Refresh mode narrowed to that: `gh pr edit` in place of `gh pr create`, Step 4 otherwise unchanged. It no longer claims a `/squash-message` trigger (that skill's own re-run rule owns it) or its own checklist write (`/qa-checklist` Steps 1 and 3 own that).
- The caller table now reads modes off the branch, with planless entry and bare mid-session `/pr` correctly listed as reaching either mode rather than pinned to create.

Landed across 0f124ce and 7fa9012.

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:154 — resolved

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

**@vzakharov** — 2026-09-08T22:31:51Z

You're right, and the failure mode you name is the decisive part. Shape is now the classifier and resolution only confirms it: a first token containing a `/` (or `#NNN`, or a PR URL) is a target, `ls-remote` confirms, and a **ref-shaped token that does not resolve stops and asks** rather than being reinterpreted as a task — wrong-repo paste being exactly the case where implementing a branch name as a task is the worst available response. Same reasoning as § "Branch-name form"'s canary. 12c993c

---
_Generated by [Claude Code](https://claude.ai/code)_

**@vzakharov** — 2026-09-08T22:59:44Z

> a first token containing a / (or #NNN, or a PR URL) is a target

anything that 'looks like a branch, walks like a branch'; in other words, anything that doesn't look like a coherent task to implement. The sources of confusion you originally mentioned included fix-sidebar-scroll, but no one writes a task with dashes. A counterargument would be "but it could be one word", but a single word is also never plausibly an actual task the operator asked ("/go sidebar" makes no sense)

**@vzakharov** — 2026-09-08T23:07:39Z

Agreed, and the wider test is now the rule. Shape still classifies, but at its full width: **a single whitespace-free first argument is a target** — `claude/foo-a1b2`, `fix-sidebar-scroll`, `sidebar`, `#NNN`, a PR URL alike — confirmed by `ls-remote`, and **stopping and asking when it doesn't resolve**. An argument carrying whitespace is a task. Ref syntax is no longer something the rule has to recognise.

Your one-word counterargument is what closes it: `/go sidebar` names a subject, not a job, so there is no shape a real task takes that this misreads — the `/`-only test bought nothing and cost the `fix-sidebar-scroll` case. 497e666

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `docs/plans/pr-first-plan-review.draft.do-not-implement.md`:159 — resolved

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

**@vzakharov** — 2026-09-08T22:31:56Z

Added — the section is now § "Notes for adopters", and the stub is "permanent here, conditional downstream". Both of your cases are stated: never adopted `/implement` → take `go` alone and put the stub path in `declined` (no downstream caller to redirect); already adopted it → the redirect is a question for the operator, not a default, with either answer recorded in `upstream.json`. The criteria live in `docs/catalog.md` because that is the file `/sync-upstream` Step 4a reads out of the source clone, so they reach the adopting agent by construction. 12c993c

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/go/SKILL.md`:1 — unresolved

**@vzakharov** — 2026-09-09T00:41:31Z

as we keep implement, git tracks this as a new file rather than a move of the previous one -- can you create and give me a commit where I can track the changes (e.g. temporarily rename `implement` to `implement_` so I can review, then rename back once I'm done; or maybe there's a better way)?

---

### `.claude/skills/plan/SKILL.md`:60 — unresolved

```diff
@@ -18,37 +19,46 @@ None of the value above depends on that bug, so fixing it upstream does not reti
 
 ## Part 1 — Plan instead of plan mode
 
-A `/plan` session's deliverable is the **pushed plan file**, not code. The operator reviews it from another machine, often hours later, and begins implementation in a **different** session via `/implement <branch>` (`@.claude/skills/implement/SKILL.md` routes that through `/from-branch`, which attaches to the branch and finds the plan under `docs/plans/`) — the handoff works because the plan file rides the branch. So a plan turn ends in a handoff, not a continuation; same-session implementation is the rare exception.
+A `/plan` session's deliverable is the **plan file on a draft PR**, not code. The operator reviews it from another machine, often hours later, and begins implementation in a **different** session via `/go <branch>` (`@.claude/skills/go/SKILL.md` routes that through `/from-branch`, which attaches to the branch and finds the plan under `docs/plans/`) — the handoff works because the plan file rides the branch. So a plan turn ends in a handoff, not a continuation; same-session implementation is the rare exception.
 
 Do **exactly what you would do in plan mode** — same research, same rigor, same "don't touch code until approved" discipline. The _only_ difference is where the plan goes and how it's approved:
 
-- Instead of presenting the plan via `ExitPlanMode`, **write it to `docs/plans/<branch-slug>.draft.do-not-implement.md`** (one file per session; name it after the current branch's task slug, or the issue number when working an issue — e.g. `docs/plans/1234.draft.do-not-implement.md`). The `.draft.do-not-implement.md` suffix is load-bearing: it is the on-disk marker that this plan has **not** been approved, visible in every `ls`, tool-call path, and `git status` so you can't drift past the gate without noticing. This directory is **not** gitignored on purpose: **commit and push it** so the operator can pull and review the plan from another machine. Follow the repo's usual plan-content expectations, including the `## DRY notes` section CLAUDE.md requires.
+- Instead of presenting the plan via `ExitPlanMode`, **write it to `docs/plans/<branch-slug>.draft.do-not-implement.md`** (one file per session; name it after the current branch's task slug, or the issue number when working an issue — e.g. `docs/plans/1234.draft.do-not-implement.md`). The slug comes off the branch, so a harness auto-branch is renamed **before** the plan file is written, per CLAUDE.md § "Git conventions" — rename afterwards and the file keeps a slug naming nothing. The `.draft.do-not-implement.md` suffix is load-bearing: it is the on-disk marker that this plan has **not** been approved, visible in every `ls`, tool-call path, and `git status` so you can't drift past the gate without noticing. This directory is **not** gitignored on purpose: it rides the branch so the operator can pull and review the plan from another machine. Follow the repo's usual plan-content expectations, including the `## DRY notes` section CLAUDE.md requires.
 - **Make line 1 of the file a banner** that restates the gate:
   ```
   > ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
   ```
-- Then **end the turn with the handoff block** (§ "Handing off" below) and stop — do not start implementing.
-- **The in-session path is the exception, not the default.** If a literal go-ahead token does arrive in _this_ session, "The approval gate" below governs it unchanged — and on approval you hand off to `@.claude/skills/implement/SKILL.md`, whose Step 1 performs the flip that unlocks source edits (`git mv` the plan to `docs/plans/<branch-slug>.in-progress.md`, drop the draft banner, quote the go-ahead in the commit) as its first action, before any source edit. That flip is the on-record receipt that approval was given, so don't front-run it here; the mechanics live in `/implement` to avoid two copies drifting apart. The gate is exactly as strict on this path as on any other; it just fires rarely.
+- Then **commit it and publish it** (§ "Publishing the plan" below), **end the turn with the handoff block** (§ "Handing off") and stop — do not start implementing.
+- **The in-session path is the exception, not the default.** If a literal go-ahead token does arrive in _this_ session, "The approval gate" below governs it unchanged — and on approval you hand off to `@.claude/skills/go/SKILL.md`, whose Step 1 performs the flip that unlocks source edits (`git mv` the plan to `docs/plans/<branch-slug>.in-progress.md`, drop the draft banner, quote the go-ahead in the commit) as its first action, before any source edit. That flip is the on-record receipt that approval was given, so don't front-run it here; the mechanics live in `/go` to avoid two copies drifting apart. The gate is exactly as strict on this path as on any other; it just fires rarely.
 
-### Handing off — end the plan turn with a copyable `/implement` block
+### Publishing the plan
+
+Once the plan file is committed, invoke `@.claude/skills/pr/SKILL.md` with no args — load and follow it; do **not** inline-copy its steps. Its plan-open mode is what a branch carrying one plan commit and no PR reaches. `/pr` owns the `gh` mechanics; `/plan` owns only the decision to publish.
+
+The trigger lives here rather than in `/pr` because this is where a plan becomes pushed, so **every** entry into planning gets a PR. CLAUDE.md § "Plan mode & questions in web sessions" names a bare `/plan` as the default entry for a new web session — more common than `/issue` — and hanging PR-creation off `/pr` would leave exactly that entry on a PR-less branch.
+
+### Handing off — end the plan turn with a copyable `/go` block
 
 Get the branch with `git branch --show-current` and substitute the real name. Introduce the block with wording that **names the new session** — `To implement — start a new session with:`, or an unmistakable equivalent. That lead-in is what carries the session model to the operator; a bare "To implement:" reads as an offer to do it here, which is the misreading the block exists to remove. Emit the command in a fenced block containing **only** the command — no language tag, nothing else inside the fence — so it can be copied verbatim:
 
 ````
 ```
-/implement claude/add-usage-charts-k3n2af
+/go claude/add-usage-charts-k3n2af
 ```
 ````
 
 - Emit it at the end of **every** turn that leaves the plan in a reviewable, complete state — the turn that first writes the plan, and any later turn that revises or collapses it (Part 3). One block per turn, as the last thing in the reply.
+- **Print the PR URL alongside it**, outside the fence — the plan is published by the time the block goes out, and the URL is where the operator reads and comments on it.
 - **Open questions don't hold the block back when they carry recommendations.** Part 2 requires every fork to name a recommended option _and_ the plan file to be written with that option already in force, so implementing it unanswered is the same as adhering to the recommendations. Emit the block alongside the questions: an answer that differs revises the plan, and silence is a valid resolution. Hold the block only for a fork with no recommendation, where the plan has nothing executable to say until the operator picks — handing over a command to implement a genuinely unresolved fork invites implementing the wrong one.
 - **Never** close a plan turn with "Want me to implement it?", "Shall I proceed?", "Ready for me to start?", or any equivalent. Two reasons: the plan session does not implement, so there is nothing to ask; and a turn that ends on that question trains the agent to read the operator's _next_ message as an answer to it, so a correction ("actually, do X instead") gets taken as assent and code starts getting written. The handoff block is the structural fix that the approval gate's "a suggestion is a plan revision" and Part 3's "picking an option is not a signal to implement" can only exhort.
-- The block is built for a session that does not exist yet, which is why the lead-in names it. Pasting it back into _this_ session is a recognizable mistake with its own guard — see `@.claude/skills/implement/SKILL.md` § "Branch-name form" for the canary that catches it.
+- The block is built for a session that does not exist yet, which is why the lead-in names it. Pasting it back into _this_ session is a recognizable mistake with its own guard — see `@.claude/skills/go/SKILL.md` § "Argument shape" for the canary that catches it.
 
 ### The approval gate
 
 **Only start implementing when the operator's message literally contains a go-ahead token** — "go ahead", "let's go ahead", "implement", "let's implement", or an unmistakable equivalent ("ship it", "do it", "proceed", "lgtm go"). Until such a token arrives, you are still in the planning conversation, no matter how the exchange evolves.
 
+**Both a suggestion and a go-ahead can arrive as PR review comments**, now that the plan is published. That changes the channel, not the test: a review comment proposing a different approach is a plan revision, one carrying a go-ahead token unlocks implementation, and `@.claude/skills/handle/SKILL.md` Step 2 is what routes each.
```

**@vzakharov** — 2026-09-09T00:45:53Z

no, let's not do this. a signal to start implementing should always come via a `/go` (or a `/handle` where no unanswered feedback is present). Opening this door (to allow implementing from code review) leaves room for mis-interpretation by the agent.

---

### `.claude/skills/squash-message/SKILL.md`:26 — unresolved

```diff
@@ -21,6 +21,11 @@ and the per-file steps mixed in with the things worth remembering — hence the
 mandatory tighten pass in Step 3. Never print or post a draft that hasn't been
 through it.
 
+The first reader reaches it earlier than merge time: `/plan` publishes the PR
+over the plan commit, so the proposal composed there is **the plan as it would
+be recorded** — a much shorter second read of the same decision, in front of the
```

**@vzakharov** — 2026-09-09T00:49:38Z

we need to make sure the squash message is phrase "as if this was already implemented" -- otherwise we risk veering into squash messages like "we have this plan and once it's done it will do this and that" -- which is obviously not what we want

---

## Timeline (status, references, and other events)

- **2026-09-08T18:23:01Z** @vzakharov renamed from «docs: open the PR at plan time so plans get reviewed like code» to «feat: give each loop skill one thing to own».
- **2026-09-08T22:27:20Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/32#pullrequestreview-5147580260.
- **2026-09-09T00:51:40Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/32#pullrequestreview-5148490928.
