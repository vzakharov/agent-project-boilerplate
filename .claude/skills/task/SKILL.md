---
description: >-
  Take a task and decide for yourself whether it needs a plan before the work
  exists, then run that call end to end — plan and hand off, plan and then
  implement, or implement with no plan at all. Invoke as `/task <what to do>`;
  the prose forms `plan or go: <task>` and "plan this or just do it" are the
  same invocation. The prompt is a conditional go-ahead scoped to that one task.
---

The decision this skill makes, before any other: **does this task get a plan, and does the plan block on the operator?** Two questions pick between three outcomes.

**The prompt is a conditional go-ahead.** It authorizes implementation *on condition that* the agent judges the operator's gate unnecessary, scoped to the task in that message and to that message alone.

`/task <what to do>` is the invocation, and so is the prose it stands in for — `plan or go: <task>`, "plan this or just do it". `/issue` is the other way in: it reads the thread first and then hands the work here, so the call is made once, in one place, whether or not the work is tracked. The mention stays bare rather than an `@`-reference — this skill ships to adopters who track no issues at all, and nothing here needs that file read.

**Anything a caller passes beyond the task — an `<issue>`, an export path — rides through unchanged to whichever outcome runs, and is never read here:** this skill knows what a task is and nothing else, and what the extras mean belongs to the skills at either end of them.

## Question 1 — does the operator need to decide before the work exists?

Any one of these is a yes:

- **The work costs far more to produce than to describe.** The plan is a page, the work is a day, and a wrong direction is caught for the price of the page.
- **A fork carries no recommendation** — the exception in `@.claude/skills/plan/SKILL.md` Part 2. Guess wrong and most of the work is wasted; the plan is what makes the choice the operator's.
- **A review round comes too late.** The step is irreversible or outward-facing, or later work builds on it before the PR is read.
- **The scope is itself the question** — you would be deciding *what* the task is, not just how to do it.

None of these asks how important the change is. Importance is why the operator reviews the diff; the gate is for what reviewing a diff cannot undo.

Nor does any of them ask how the task arrived. **A task that came in through `/issue` carries evidence that it is worth tracking, which is not evidence that it is large** — a two-row docs correction gets filed so it survives the review it surfaced in. Weigh the work described, not the formality of the thread describing it, or every issue plans and the call is decorative.

## Question 2 — would writing it down change what you build?

A plan is also how an agent gets its own head straight, and that value needs no operator:

- several parts whose order matters, or edits that only make sense landing together;
- a live reuse call — the mandatory `## DRY notes` is the forcing function, and it earns the file whenever "shared or duplicated?" has a real answer to argue;
- a shape you would otherwise discover halfway through, after building the first half against a different one.

The test: if you can hold the whole change in your head and name every file it touches, the file buys nothing.

## The three outcomes

1. **Plan and hand off** — Question 1 said yes. `@.claude/skills/plan/SKILL.md` Parts 1–3 run unchanged, ending at the handoff block.
2. **Go** — both said no, so the diff is the plan. Enter `@.claude/skills/go/SKILL.md` § "Planless entry" with the task.
3. **Plan, then go** — Question 1 no, Question 2 yes. Write the plan straight to `docs/plans/<slug>.in-progress.md`, no draft banner, in a commit quoting the `/task` prompt and naming the call; publish it through `@.claude/skills/pr/SKILL.md` so the operator has a surface to interrupt on; then run `/go` from its Step 2. The draft state is skipped rather than flipped, because nothing here awaits approval — writing the file was the agent's own call and the conditional go-ahead already cleared the work.

**Report the call in the first sentence of the turn, with its reason and the override**: "Doing this directly rather than planning it — *reason*. Say `plan` and I'll write one instead." That costs the operator one word to reverse, and puts the judgment on the record in the turn that acted on it.

**On that override, stop where you are.** Write the plan for the whole task and name the commits that already exist, so the operator reviews it knowing what is built. Leave those commits in place; reverting work nobody asked you to revert costs more than the work does.

**When a call is close the two questions break opposite ways.** A close Question 1 goes to the operator — being wrong toward the gate costs a round trip, being wrong past it costs them reviewing work that should not exist. A close Question 2 writes the file — it is cheap, and `/finalize` sweeps it either way.

**The pull is toward outcome 2**, which starts producing this turn and bills its cost later, to whoever reads the result. Weigh it against that round trip rather than against the appetite to start.
