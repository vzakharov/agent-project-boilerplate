# PR #71: feat: give the plan-or-not call its own skill, and route /issue to it

- **State:** open
- **URL:** https://github.com/vzakharov/muthur/pull/71
- **Author:** @vzakharov (human)
- **Base ← Head:** main ← claude/task-skill-ukv536
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-12T14:26:37Z
- **Updated:** 2026-09-12T15:27:12Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The plan-or-not call gets its own front door: `/task <what to do>`.** The judgment — does this task need the operator's gate, a plan for the agent's own sake, or neither? — reached the agent only as prose (`plan or go: <task>`) routed through a section of `/plan`. `.claude/skills/plan/plan-or-go.md` becomes `.claude/skills/task/SKILL.md`, questions and outcomes unchanged, so it is a typeable slash command that loads on invocation instead of on every planning session. **The name is a noun on purpose:** skills trigger on description matching before their body loads, so a verb-named entry is readable as an instruction — an earlier draft called it `/lets`, which collides with `/plan`'s approval gate reading "let's implement" as a go-ahead. CLAUDE.md now rules those names out and points at naming a skill after its argument, which is what `/issue`, `/task` and `/pr` do.
- **`/issue` makes that same call instead of planning unconditionally.** It used to hand every issue to `/plan`, on the reasoning that filing an issue answers the call by itself. Filing one is evidence the work is worth *tracking*, which comes apart from worth *deliberating*: a two-row docs correction gets filed so a review doesn't lose it, not because anyone needs a page about it first. Step 4 now hands to `/task` like any other work. A split issue is the one exception — it skips the call and plans, since splitting only happens when the work is obviously beyond a single PR, which is the first question's first clause already satisfied.
- **Nothing threads a parameter to carry that.** The only thing downstream that wants the issue number is `/pr`'s `Closes #N`, which already infers one when no caller passed it; what that inference did not read is the branch, and `/issue` is the one caller that guarantees the number is in the slug. So `/pr` Step 4 reads the branch before the commits — which also settles the split case the explicit parameter existed for, the slug carrying the chosen child and never the parent.
- **Citations repointed**, so nothing states the old arrangement: CLAUDE.md's routing bullet and its skills list, `/go`'s planless entry, `/issue`'s frontmatter, end-state and chain, and the catalog (a new `/task` row in G2, `/plan`'s row losing the moved clause, `/go`'s and `/issue`'s gaining the new reference). The move also upgrades the `/go` → `/task` pointer into one `scripts/check-skill-catalog.sh` verifies, which a reference to a non-`SKILL.md` page was not.

## QA Checklist

- [ ] `invoke` — In a fresh session, type `/task <some small task>`. The turn opens by reporting the call and its reason, offers `plan` as the one-word override, and then runs one of the three outcomes rather than asking what to do.
- [ ] `prose-form` — Open a session with `plan or go: <task>`. It reaches the same skill and behaves identically to `/task`.
- [ ] `issue-small` — Run `/issue 72` (a two-row docs correction). It exports and commits the thread, then reaches the no-plan outcome and implements — no `docs/plans/` file, no handoff block — and the PR it opens ends with `Closes #72`, read off the `claude/72-…` branch slug with nothing passed to `/pr`.
- [ ] `issue-large` — Run `/issue` on a genuinely large issue. It still writes `docs/plans/<slug>.draft.do-not-implement.md`, publishes the draft PR, and ends at the `/go <branch>` handoff.
- [ ] `issue-split` — Run `/issue` on a split-worthy issue. After the split is approved it plans without re-asking whether a plan is needed, and the PR closes the chosen child rather than the parent umbrella.
- [ ] `mid-session` — Partway through an implementation session, say "let's also rename X". It is handled as an ordinary follow-up under `/plan`'s approval gate; the session does not load `/task` or re-decide whether the work needs a plan.
- [ ] `plan-unchanged` — Open a session with `plan: <task>`. It writes the draft plan file, publishes the draft PR, and ends with the handoff block, exactly as before.
- [ ] `catalog` — Run `./scripts/check-skill-catalog.sh`. It reports OK: `/task` has exactly one catalog row, and every `@`-reference added here resolves.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `invoke` | manual-only | — | Whether an agent reads the routing correctly is a judgment call, not an assertion |
| `prose-form` | manual-only | — | Same — it turns on description-matching by the harness |
| `issue-small` | manual-only | — | The change's whole point; only a real issue run exercises the call and the slug inference together |
| `issue-large` | manual-only | — | Regression check that the plan lane still reaches the handoff |
| `issue-split` | manual-only | — | Also checks the umbrella stays open, which no assertion can see |
| `mid-session` | manual-only | — | The collision the noun name removes; only a real session exercises it |
| `plan-unchanged` | manual-only | — | Regression check that removing the section changed nothing else in `/plan` |
| `catalog` | unit | ✅ | `scripts/check-skill-catalog.sh`, which `scripts/vet.sh` runs |

https://claude.ai/code/session_01XRx3cnhN5rkx4LpLRdDRBf

---

## Comments

### Comment by @vzakharov (agent) on 2026-09-12T14:27:29Z

[https://github.com/vzakharov/muthur/pull/71#issuecomment-5646501641](https://github.com/vzakharov/muthur/pull/71#issuecomment-5646501641)

Proposed squash title/body:

```
feat: give the plan-or-not call one home, and route /issue to it (pr #71)
```

```
The judgment an operator hands over when they don't want to pre-decide
whether work needs a plan — does this task need the operator's gate, a
plan for the agent's own sake, or neither? — reached the agent only as
prose routed through a section of /plan. As its own skill it is a
typeable slash command, it appears in the skills list where an operator
can find it, and it loads on invocation instead of on every planning
session. /task <what to do> runs the call it makes: plan and hand off,
plan and then implement, or implement with no plan at all.

/issue makes that same call now instead of planning unconditionally. It
had handed every issue to /plan on the reasoning that filing an issue
answers the call by itself, but filing one is evidence the work is
worth tracking, which comes apart from worth deliberating: a two-row
docs correction gets filed so a review doesn't lose it, not because
anyone needs a page about it first. A split issue is the exception and
still plans, splitting being the case where the work is already known
to be beyond one PR.

No parameter is threaded through the new route to carry the issue
number. The only thing downstream that wants it is /pr's Closes #N,
which already infers one when no caller passed it; what that inference
did not read is the branch, and /issue is the one caller that
guarantees the number leads the slug. /pr reads the branch before the
commits, which also settles the split case: the slug carries the chosen
child, never the parent umbrella.

Skills trigger on description matching before their body loads, so a
skill named after a word the loop already uses as a go-ahead fires on
prose that meant the token. CLAUDE.md now rules those names out and
points at naming a skill after its argument, which is what /issue,
/task and /pr do.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Review threads

### `docs/plans/issue-plan-call.draft.do-not-implement.md`:18 — resolved

```diff
@@ -0,0 +1,143 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Let `/issue` make the plan-or-not call
+
+## Why
+
+`/issue` hands every issue to `/plan`, unconditionally. The rationale currently
+on this branch says the issue's own existence answers the plan-or-not call —
+filing one costs something, so anything filed cleared the bar.
+
+That reads well and is wrong. Filing an issue is evidence the work is worth
+**tracking**, which is a different property from being worth **deliberating**.
+The two come apart constantly, and this repo's own backlog has the case:
+[#72](https://github.com/vzakharov/agent-project-boilerplate/issues/72) — "drop
+the working-artifact rows from the catalog's Never table" — is filed because it
+surfaced during a downstream review and would otherwise be lost, not because
+anyone needs a page about it before the two rows come out. Routing it through
+`/plan` buys a plan file, a draft PR, a handoff block and a second session, for
```

**@vzakharov (human)** — 2026-09-12T14:45:46Z

a draft PR is always the case though

**@vzakharov (agent)** — 2026-09-12T14:55:56Z

Right — both lanes end at `/pr` and both open a draft, so the PR was never part of the delta. Cost list is now the plan file, the handoff block and the second session, in 1edf8d3.

---

### `docs/plans/issue-plan-call.draft.do-not-implement.md`:46 — resolved

```diff
@@ -0,0 +1,143 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Let `/issue` make the plan-or-not call
+
+## Why
+
+`/issue` hands every issue to `/plan`, unconditionally. The rationale currently
+on this branch says the issue's own existence answers the plan-or-not call —
+filing one costs something, so anything filed cleared the bar.
+
+That reads well and is wrong. Filing an issue is evidence the work is worth
+**tracking**, which is a different property from being worth **deliberating**.
+The two come apart constantly, and this repo's own backlog has the case:
+[#72](https://github.com/vzakharov/agent-project-boilerplate/issues/72) — "drop
+the working-artifact rows from the catalog's Never table" — is filed because it
+surfaced during a downstream review and would otherwise be lost, not because
+anyone needs a page about it before the two rows come out. Routing it through
+`/plan` buys a plan file, a draft PR, a handoff block and a second session, for
+a change whose whole description is its title.
+
+So `/issue` should run the same two questions `/task` runs, once it has read the
+thread.
+
+## What this changes
+
+`/task` becomes the single home of the call, and both entry points reach it:
+`/task <what to do>` for untracked work, `/issue <n>` after its export and split
+steps. The questions are not restated in `/issue`.
+
+The obstacle is parameter threading. `/task`'s outcomes dispatch to `/plan` and
+`/go`, and issue work carries two things a bare task does not: `<issue>` (the
+number the eventual PR must close) and the export path
+(`docs/issue/<n>/issue.md`). Outcome 1 is already fine — `/plan` takes both from
+its caller today. **Outcome 2 is not**: `/go` § "Planless entry" enters with a
+task and nothing else, and its Step 4 loads `/pr` *with no args*, so `/pr`'s
+`<issue>` caller parameter never gets set and the PR opens without `Closes #N`.
+The issue then stays open after its own fix merges.
+
+### Step 1 — Give `/task` a caller-parameters section
+
+Add one to `.claude/skills/task/SKILL.md`, modelled on the one
+`@.claude/skills/pr/SKILL.md` already carries:
+
+- `<issue>` — the number the eventual PR must close. Passed through to whichever
+  outcome runs.
+- `<export>` — the issue export path, passed to `/plan` as context.
```

**@vzakharov (human)** — 2026-09-12T14:47:16Z

isn't it always the same though (deterministically derived from issue)?

**@vzakharov (agent)** — 2026-09-12T14:55:58Z

Yes — `docs/issue/<n>/issue.md` for the `<issue>` in hand, so anything holding the number holds the path. Dropped as a parameter in 1edf8d3; the DRY notes now say it is derived.

---

### `docs/plans/issue-plan-call.draft.do-not-implement.md`:57 — resolved

```diff
@@ -0,0 +1,143 @@
+> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.
+
+# Let `/issue` make the plan-or-not call
+
+## Why
+
+`/issue` hands every issue to `/plan`, unconditionally. The rationale currently
+on this branch says the issue's own existence answers the plan-or-not call —
+filing one costs something, so anything filed cleared the bar.
+
+That reads well and is wrong. Filing an issue is evidence the work is worth
+**tracking**, which is a different property from being worth **deliberating**.
+The two come apart constantly, and this repo's own backlog has the case:
+[#72](https://github.com/vzakharov/agent-project-boilerplate/issues/72) — "drop
+the working-artifact rows from the catalog's Never table" — is filed because it
+surfaced during a downstream review and would otherwise be lost, not because
+anyone needs a page about it before the two rows come out. Routing it through
+`/plan` buys a plan file, a draft PR, a handoff block and a second session, for
+a change whose whole description is its title.
+
+So `/issue` should run the same two questions `/task` runs, once it has read the
+thread.
+
+## What this changes
+
+`/task` becomes the single home of the call, and both entry points reach it:
+`/task <what to do>` for untracked work, `/issue <n>` after its export and split
+steps. The questions are not restated in `/issue`.
+
+The obstacle is parameter threading. `/task`'s outcomes dispatch to `/plan` and
+`/go`, and issue work carries two things a bare task does not: `<issue>` (the
+number the eventual PR must close) and the export path
+(`docs/issue/<n>/issue.md`). Outcome 1 is already fine — `/plan` takes both from
+its caller today. **Outcome 2 is not**: `/go` § "Planless entry" enters with a
+task and nothing else, and its Step 4 loads `/pr` *with no args*, so `/pr`'s
+`<issue>` caller parameter never gets set and the PR opens without `Closes #N`.
+The issue then stays open after its own fix merges.
+
+### Step 1 — Give `/task` a caller-parameters section
+
+Add one to `.claude/skills/task/SKILL.md`, modelled on the one
+`@.claude/skills/pr/SKILL.md` already carries:
+
+- `<issue>` — the number the eventual PR must close. Passed through to whichever
+  outcome runs.
+- `<export>` — the issue export path, passed to `/plan` as context.
+- Absent both (the bare `/task <what to do>` case), the outcomes behave exactly
+  as they do now, so the ordinary path reads as if the section weren't there.
+
+Then state in each of the three outcomes what it forwards.
+
+### Step 2 — Thread `<issue>` through `/go`'s planless entry
+
+In `.claude/skills/go/SKILL.md`:
+
+- § "Planless entry" gains `<issue>` as an optional caller parameter alongside
+  the task text.
```

**@vzakharov (human)** — 2026-09-12T14:48:34Z

just to pass to /pr, right? I'd hate to have our skills repeat the prose about how issues are handled multiple times

**@vzakharov (agent)** — 2026-09-12T14:56:08Z

Just to pass to `/pr`, yes — and your objection killed the step. Threading it would have put issue-handling prose in `/task` and `/go`, neither of which has any business knowing what an issue is, to move a number `/pr` can already work out. What landed instead is one clause in `/pr` itself: let its existing inference read the issue-number-leading branch slug that `/issue` mandates. One skill knows about issues, which is the arrangement you asked for. 1edf8d3

---

### `.claude/skills/issue/SKILL.md`:134 — resolved

```diff
@@ -131,7 +131,7 @@ Load and follow `@.claude/skills/plan/SKILL.md`, passing what the issue asks in
 
 `/plan`'s deliverable is the plan file, published as a draft PR by its § "Publishing the plan", and the copyable `/go <branch>` block. **That is normally where this run ends.** Do not implement here: `/go` runs in a later session and hands the finished work back to `/pr` to refresh.
 
-The **only** waiver is the operator explicitly saying no plan is needed, which routes to `@.claude/skills/go/SKILL.md` § "Planless entry". It is not this skill's to grant on its own judgement.
+The **only** waiver is the operator explicitly saying no plan is needed, which routes to `@.claude/skills/go/SKILL.md` § "Planless entry". It is not this skill's to grant on its own judgement — the plan-or-not call `@.claude/skills/task/SKILL.md` makes for untracked work is already answered here by the issue existing. Filing one costs something, so work that was worth filing cleared the bar the call tests for.
```

**@vzakharov (human)** — 2026-09-12T14:50:43Z

wait (this is the first comment alphabetically, but I created it after the ones on the new plan), but if /issue already has a path to hand it over to /go's planless entry, (I usually wrote smth like "/issue ... no plan"), means the absence or absence of an issue param for the go skill never played a role, it worked fine through agents' own judgment/deliberation?

**@vzakharov (agent)** — 2026-09-12T14:56:09Z

You are right, and the plan was wrong. `/pr` § "Caller parameters" says the explicit `<issue>` beats inference *for a split issue* — a stray parent reference in a commit body closing the umbrella — and nothing else; absent it, Step 4 infers from what the PR and commits reference. I quoted that line in the plan without following it through, and wrote "the PR opens without `Closes #N`" instead. So the waiver path worked because there was no gap to notice.

The one hole left is that the inference reads commits but not the branch, which is where `/issue` guarantees the number lives. That is now a one-clause change in `/pr` and the plan is two steps shorter: 1edf8d3

---

### `.claude/skills/task/SKILL.md`:14 — unresolved

```diff
@@ -11,7 +11,9 @@ The decision this skill makes, before any other: **does this task get a plan, an
 
 **The prompt is a conditional go-ahead.** It authorizes implementation *on condition that* the agent judges the operator's gate unnecessary, scoped to the task in that message and to that message alone.
 
-`/task <what to do>` is the invocation, and so is the prose it stands in for — `plan or go: <task>`, "plan this or just do it". It is the untracked-work sibling of `/issue`: same handover, a task in place of an issue number.
+`/task <what to do>` is the invocation, and so is the prose it stands in for — `plan or go: <task>`, "plan this or just do it". `/issue` is the other way in: it reads the thread first and then hands the work here, so the call is made once, in one place, whether or not the work is tracked. The mention stays bare rather than an `@`-reference — this skill ships to adopters who track no issues at all, and nothing here needs that file read.
```

**@vzakharov (human)** — 2026-09-12T15:26:20Z

> and so is the prose it stands in for — `plan or go: <task>`, "plan this or just do it"

these are polar bears -- no operator would normally write "plan or go" if this wasn't a lane of the /plan skill previously.

what I think though, is that any invocation that sounds like a directive rather than a question (e.g. "let's create ..." or even just simply "create ..." versus "what does our repo say about..."). This sounds pretty intuitive, right? Currently muthur provides no entry for requests that sound like "do this", and an adopting repo's agent would be at its own judgment as to what to do next (just work on the auto branch? invoke some skill?)

---

### `.claude/skills/task/SKILL.md`:29 — unresolved

```diff
@@ -24,6 +26,8 @@ Any one of these is a yes:
 
 None of these asks how important the change is. Importance is why the operator reviews the diff; the gate is for what reviewing a diff cannot undo.
 
+Nor does any of them ask how the task arrived. **A task that came in through `/issue` carries evidence that it is worth tracking, which is not evidence that it is large** — a two-row docs correction gets filed so it survives the review it surfaced in. Weigh the work described, not the formality of the thread describing it, or every issue plans and the call is decorative.
```

**@vzakharov (human)** — 2026-09-12T15:26:48Z

polar bear

---

## Timeline (status, references, and other events)

- **2026-09-12T14:50:45Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/muthur/pull/71#pullrequestreview-5186802965.
- **2026-09-12T15:09:19Z** @vzakharov renamed from «feat: give the plan-or-not call its own skill, /task» to «feat: give the plan-or-not call its own skill, and route /issue to it».
- **2026-09-12T15:27:12Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/muthur/pull/71#pullrequestreview-5186945235.
