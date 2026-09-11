# PR #68: feat: let a session decide for itself whether a task needs a plan

- **State:** open
- **URL:** https://github.com/vzakharov/muthur/pull/68
- **Author:** @vzakharov (human)
- **Base ← Head:** main ← claude/plan-or-go-chjois
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-11T13:20:12Z
- **Updated:** 2026-09-11T13:24:58Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **`plan or go: <task>` is a third entry alongside `plan: <task>` and "no plan".** The operator declines to pre-decide whether the work warrants a plan, and the session makes that call itself — the words are a conditional go-ahead, scoped to that one message. Everywhere else the approval gate is untouched: no agent clears it by judging a plan unnecessary.
- **Two questions pick between three outcomes.** Question 1 — does the operator need to decide *before* the work exists? Yes for work far more expensive to produce than to describe, a fork with no recommendation, a step a review round cannot undo, or a scope that is itself the question. Question 2 — would writing the plan change what gets built? That is the value a plan has for the agent rather than for the gate, which is the axis the single "does this need approval?" question was missing.
- **The outcomes route to paths that already exist.** Q1 yes → the plan-and-hand-off path, unchanged. Q1 no, Q2 yes → the plan goes straight to `docs/plans/<slug>.in-progress.md`, no draft banner, published so the operator has a surface to interrupt on, then `/go` from its Step 2. Both no → `/go`'s planless entry.
- **The turn reports the call in its first sentence, with a one-word override.** On `plan`, the session stops, writes the plan for the whole task, and names the commits already on the branch rather than reverting them.
- **This branch is the dogfood.** It ran as outcome 2 — the deliverable is prose, so describing it and writing it cost the same, and nothing lands until this PR is reviewed. Question 2 was the near miss and the reason the middle outcome exists at all.

## QA Checklist

- [ ] `outcome-2` — open a fresh web session with `plan or go: <a small, single-file prose tweak>`; confirm the first sentence of the reply states the call and its reason, no `docs/plans/` file is written, and the turn ends at a draft PR.
- [ ] `outcome-1` — same, with a task carrying a fork you cannot recommend on (or a day of code); confirm the session writes `docs/plans/<slug>.draft.do-not-implement.md`, touches no source, and ends with the copyable `/go <branch>` block.
- [ ] `outcome-3` — same, with a multi-part change that has no operator-level fork; confirm the plan lands as `docs/plans/<slug>.in-progress.md` with no draft banner, its commit quotes the `plan or go` prompt, a draft PR appears *before* implementation starts, and implementation resumes at `/go` Step 2.
- [ ] `override` — while an outcome-2 run is in flight, reply `plan`; confirm the session stops, writes the plan for the whole task, names the commits already pushed, and reverts nothing.
- [ ] `gate-intact` — open a session with a plain task (no `plan or go` in the prompt); confirm it still opens a plan cycle and does not self-authorize implementation.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `outcome-2` | manual-only | — | Agent judgment in a live session; the observable is which artifacts the turn produces |
| `outcome-1` | manual-only | — | Same, inverted — the tell is a `.draft.do-not-implement.md` file and untouched source |
| `outcome-3` | manual-only | — | Same; also checks the skipped draft state and the early publish |
| `override` | manual-only | — | Needs a mid-run interjection, which nothing can stage |
| `gate-intact` | manual-only | — | Regression check that the new entry did not widen the default |

https://claude.ai/code/session_016vUo7e5vb6Y1B6NJgFSyYv

---

## Comments

### Comment by @vzakharov (agent) on 2026-09-11T13:20:46Z

[https://github.com/vzakharov/muthur/pull/68#issuecomment-5635040196](https://github.com/vzakharov/muthur/pull/68#issuecomment-5635040196)

Proposed squash title/body:

```
feat: let a session decide for itself whether a task needs a plan (pr #68)
```

```
`plan: <task>` and "no plan" were the only two entries, so whether a
task warranted a plan was the operator's call to make before they had
seen anyone work it. `plan or go: <task>` is the third entry, handing
that judgment to the session as a conditional go-ahead scoped to the
one message it appears in. Everywhere else the approval gate is
untouched: no agent clears it by deciding a plan would be overkill.

Two questions pick between three outcomes. The first asks whether the
operator needs to decide before the work exists — work far more
expensive to produce than to describe, a fork carrying no
recommendation, a step no review round can undo, or a scope that is
itself the question. The second asks whether writing the plan would
change what gets built, which is the value a plan has for the agent
rather than for the gate, and the axis a lone "does this need
approval?" test has nowhere to put. A yes to the first runs the
plan-and-hand-off path unchanged; a no with a yes to the second writes
the plan straight to `*.in-progress.md`, publishes it and keeps going;
two noes enter `/go`'s planless entry.

The turn reports its call in the first sentence with its reason, so
`plan` is a one-word reversal — which stops the run, writes the plan
for the whole task, and leaves the commits already pushed in place. The
skill owns the two questions and what each outcome runs; CLAUDE.md
carries the pointer and the scoping clause, where a session reads it
before loading anything.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Review threads

### `.claude/skills/plan/SKILL.md`:38 — unresolved

```diff
@@ -35,6 +35,47 @@ Plan mode is reached two ways, neither of which asks the agent: the operator swi
 
 **Exiting plan mode is not the go-ahead**, however the approval reads — it comes back as "you can now start coding", in accept-edits mode. It authorizes writing the plan file and nothing past it; the `do-not-implement` gate is untouched and still needs the token from § "The approval gate".
 
+## The `plan or go` entry
```

**@vzakharov (human)** — 2026-09-11T13:24:19Z

let's extract this to a colocated but separate md, mentioning it by reference so it doesn't take context unless it's a "plan or go" entry (which most of the time it won't be)

---

## Timeline (status, references, and other events)

- **2026-09-11T13:24:57Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/muthur/pull/68#pullrequestreview-5179127296.
