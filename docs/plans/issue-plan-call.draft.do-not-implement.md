> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Let `/issue` make the plan-or-not call

## Why

`/issue` hands every issue to `/plan`, unconditionally. The rationale currently
on this branch says the issue's own existence answers the plan-or-not call —
filing one costs something, so anything filed cleared the bar.

That reads well and is wrong. Filing an issue is evidence the work is worth
**tracking**, which is a different property from being worth **deliberating**.
The two come apart constantly, and this repo's own backlog has the case:
[#72](https://github.com/vzakharov/agent-project-boilerplate/issues/72) — "drop
the working-artifact rows from the catalog's Never table" — is filed because it
surfaced during a downstream review and would otherwise be lost, not because
anyone needs a page about it before the two rows come out. Routing it through
`/plan` buys a plan file, a draft PR, a handoff block and a second session, for
a change whose whole description is its title.

So `/issue` should run the same two questions `/task` runs, once it has read the
thread.

## What this changes

`/task` becomes the single home of the call, and both entry points reach it:
`/task <what to do>` for untracked work, `/issue <n>` after its export and split
steps. The questions are not restated in `/issue`.

The obstacle is parameter threading. `/task`'s outcomes dispatch to `/plan` and
`/go`, and issue work carries two things a bare task does not: `<issue>` (the
number the eventual PR must close) and the export path
(`docs/issue/<n>/issue.md`). Outcome 1 is already fine — `/plan` takes both from
its caller today. **Outcome 2 is not**: `/go` § "Planless entry" enters with a
task and nothing else, and its Step 4 loads `/pr` *with no args*, so `/pr`'s
`<issue>` caller parameter never gets set and the PR opens without `Closes #N`.
The issue then stays open after its own fix merges.

### Step 1 — Give `/task` a caller-parameters section

Add one to `.claude/skills/task/SKILL.md`, modelled on the one
`@.claude/skills/pr/SKILL.md` already carries:

- `<issue>` — the number the eventual PR must close. Passed through to whichever
  outcome runs.
- `<export>` — the issue export path, passed to `/plan` as context.
- Absent both (the bare `/task <what to do>` case), the outcomes behave exactly
  as they do now, so the ordinary path reads as if the section weren't there.

Then state in each of the three outcomes what it forwards.

### Step 2 — Thread `<issue>` through `/go`'s planless entry

In `.claude/skills/go/SKILL.md`:

- § "Planless entry" gains `<issue>` as an optional caller parameter alongside
  the task text.
- Step 4 passes it on to `/pr` rather than calling with no args.

Both are additive: a planless entry with no `<issue>` keeps today's behaviour.

### Step 3 — Replace `/issue` Step 4's unconditional handover

`.claude/skills/issue/SKILL.md` Step 4 becomes a handover to
`@.claude/skills/task/SKILL.md`, passing the issue's one-line ask, the export
path, and `<issue>`. What stays in `/issue`, because it is `/issue`'s and not
the call's: the `<issue>` resolution rule (the chosen child when split, never
the parent), the branch-slug requirement, "don't paraphrase the issue back at
yourself", and the reporting line.

The waiver paragraph — the one this branch just added — goes. It says the call
is not this skill's to make, which is the thing being changed; leaving a negated
version behind would be a polar bear.

**One rule is new here, and it belongs in `/issue` rather than `/task`:** a
split issue skips the call and plans. Step 3 only splits when the work is
"obviously beyond a single PR", which is Question 1's first clause already
satisfied — so re-asking it wastes a judgment that is made.

### Step 4 — Calibrate `/task` for what a filed issue means

One line in `.claude/skills/task/SKILL.md`, near Question 1: a filed issue is
evidence the work is **trackable**, not that it is **large**. Without it the
agent over-weights the formality of arriving through `/issue` and plans
everything anyway, which is today's behaviour reached by a longer route.

### Step 5 — Repoint what states the old arrangement

- `/task`'s frontmatter and opening call it "the untracked-work sibling of
  `/issue`". That framing dies with this change — they are not siblings, one
  calls the other.
- `/issue`'s frontmatter says it hands work "over to `/plan`".
- `/issue`'s End-state line and its `/issue` → `/plan` → … chain.
- CLAUDE.md § "Working with skills" describes `/issue` as handing to `/plan`.
- The catalog's `/issue` and `/task` rows.

## DRY notes

- **The two questions stay in exactly one place** — `.claude/skills/task/SKILL.md`.
  `/issue` reaches them by `@`-reference, never by restatement. This is the whole
  point of the change: the alternative (copying the questions into `/issue` with
  issue-flavoured wording) is two homes for one rule, which CLAUDE.md § "Writing
  things down" names as the finding rather than the fix.
- **The caller-parameters pattern is reused, not invented.** `/pr` already has a
  § "Caller parameters" with `<base>`, `<issue>` and the plan; `/task`'s copies
  its shape and its "a bare invocation takes the defaults" framing. No shared
  file is extracted for it — the two lists differ in content and each is four
  lines, so a common home would cost a load to save nothing.
- **`<issue>` threading is a pass-through, not a new concept.** `/pr` already
  accepts it and already prefers it over inference; this plan only extends the
  chain that reaches it (`/task` → `/go` → `/pr`) so the planless lane can carry
  what the planned lane already does.
- **The split → always-plan rule lives in `/issue`, not `/task`.** It is about
  the split, which is `/issue`'s alone; `/task` has no notion of one. Putting it
  in `/task` would make that skill know about a caller's internals.

## Open question

**1. Does this land on PR #71 or a follow-up?**

- **a. On #71 (recommended).** The branch already carries the line this change
  reverses, so landing separately means `main` briefly states a rule we have
  disavowed; `/issue` referencing `/task` only exists on this branch, so a
  follow-up would have to be stacked on it or wait; and the two halves are one
  idea — the call gets a home, and both entry points use it. PR #71's title
  widens to cover both.
- **b. A follow-up PR, stacked on this branch.** Keeps #71 as the narrower
  "extract the skill" change and reviews the `/issue` routing on its own. Costs
  a stacked base and a second review cycle, and leaves the disavowed line in the
  squash record of #71.

This plan is written assuming **(a)**. Under (b) nothing in Steps 1–5 changes —
only which branch they land on.

## QA

- `/issue` on a small issue (#72 is the live case) reaches the no-plan outcome,
  and the PR it opens carries `Closes #72`.
- `/issue` on a large issue still writes a plan file and ends at the `/go`
  handoff.
- A split issue plans without re-running the call.
- `/task <what to do>` with no issue behind it behaves exactly as before.
- `./scripts/check-skill-catalog.sh` stays green.
