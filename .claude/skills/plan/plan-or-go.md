# The `plan or go` entry

The decision `@.claude/skills/plan/SKILL.md` § "The `plan or go` entry" routes here to make, before any other: **does this task get a plan, and does the plan block on the operator?**

**The prompt is a conditional go-ahead.** It authorizes implementation *on condition that* the agent judges the operator's gate unnecessary, scoped to the task in that message and to that message alone.

## Question 1 — does the operator need to decide before the work exists?

Any one of these is a yes:

- **The work costs far more to produce than to describe.** The plan is a page, the work is a day, and a wrong direction is caught for the price of the page.
- **A fork carries no recommendation** — the exception in the skill's Part 2. Guess wrong and most of the work is wasted; the plan is what makes the choice the operator's.
- **A review round comes too late.** The step is irreversible or outward-facing, or later work builds on it before the PR is read.
- **The scope is itself the question** — you would be deciding *what* the task is, not just how to do it.

None of these asks how important the change is. Importance is why the operator reviews the diff; the gate is for what reviewing a diff cannot undo.

## Question 2 — would writing it down change what you build?

A plan is also how an agent gets its own head straight, and that value needs no operator:

- several parts whose order matters, or edits that only make sense landing together;
- a live reuse call — the mandatory `## DRY notes` is the forcing function, and it earns the file whenever "shared or duplicated?" has a real answer to argue;
- a shape you would otherwise discover halfway through, after building the first half against a different one.

The test: if you can hold the whole change in your head and name every file it touches, the file buys nothing.

## The three outcomes

1. **Plan and hand off** — Question 1 said yes. The skill's Parts 1–3 run unchanged, ending at the handoff block.
2. **Go** — both said no, so the diff is the plan. Enter `@.claude/skills/go/SKILL.md` § "Planless entry" with the task.
3. **Plan, then go** — Question 1 no, Question 2 yes. Write the plan straight to `docs/plans/<slug>.in-progress.md`, no draft banner, in a commit quoting the `plan or go` prompt and naming the call; publish it through `@.claude/skills/pr/SKILL.md` so the operator has a surface to interrupt on; then run `/go` from its Step 2. The draft state is skipped rather than flipped, because nothing here awaits approval — writing the file was the agent's own call and the conditional go-ahead already cleared the work.

**Report the call in the first sentence of the turn, with its reason and the override**: "Doing this directly rather than planning it — *reason*. Say `plan` and I'll write one instead." That costs the operator one word to reverse, and puts the judgment on the record in the turn that acted on it.

**On that override, stop where you are.** Write the plan for the whole task and name the commits that already exist, so the operator reviews it knowing what is built. Leave those commits in place; reverting work nobody asked you to revert costs more than the work does.

**When a call is close the two questions break opposite ways.** A close Question 1 goes to the operator — being wrong toward the gate costs a round trip, being wrong past it costs them reviewing work that should not exist. A close Question 2 writes the file — it is cheap, and `/finalize` sweeps it either way.

**The pull is toward outcome 2**, which starts producing this turn and bills its cost later, to whoever reads the result. Weigh it against that round trip rather than against the appetite to start.
