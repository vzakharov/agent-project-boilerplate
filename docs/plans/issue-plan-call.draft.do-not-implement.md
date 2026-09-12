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
`/plan` buys a plan file, a handoff block and a second session, for a change
whose whole description is its title. The PR is not part of that cost: both
lanes end at `/pr`, and both open a draft.

So `/issue` should run the same two questions `/task` runs, once it has read the
thread.

## What this changes

`/task` becomes the single home of the call, and both entry points reach it:
`/task <what to do>` for untracked work, `/issue <n>` after its export and split
steps. The questions are not restated in `/issue`.

**No parameter threading comes with it.** `/plan` already takes `<issue>` and the
export path from its caller, and `/go` needs neither: the only thing downstream
that wants the number is `/pr`'s `Closes #N`, and `@.claude/skills/pr/SKILL.md`
§ "Caller parameters" already resolves that by inference when no caller passed
one. Explicit beats inference **only for a split issue**, where a stray parent
reference in a commit body would close the umbrella — and under Step 1 a split
issue never reaches the planless lane, because it skips the call and plans.

What that inference does not read is the branch, and `/issue` is the one caller
that guarantees the issue number is in it. Step 3 closes that, in `/pr`.

### Step 1 — Replace `/issue` Step 4's unconditional handover

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

### Step 2 — Two lines in `.claude/skills/task/SKILL.md`

- **Forwarding.** One sentence: whatever the caller passed beyond the task —
  an `<issue>`, an export path — is forwarded unchanged to whichever outcome
  runs, and this skill reads none of it. No `## Caller parameters` section: the
  bare `/task <what to do>` case has nothing to forward, and a section would
  put issue-handling prose in a skill that has no business knowing what an
  issue is.
- **Calibration**, near Question 1: a filed issue is evidence the work is
  **trackable**, not that it is **large**. Without it the agent over-weights the
  formality of arriving through `/issue` and plans everything anyway, which is
  today's behaviour reached by a longer route.

### Step 3 — Let `/pr`'s issue inference read the branch slug

`@.claude/skills/pr/SKILL.md` Step 4 closes on "the caller's `<issue>` when one
was passed, and otherwise any issue the PR or a commit references". Add the
branch to that fallback, consulted before the commit scan: an issue-number-
leading slug (`claude/847-fix-sidebar-scroll-<hash>`), which `/issue` § "Branch
name" mandates for every branch it opens.

This is what makes the planless lane safe for issue work without threading a
parameter through two skills to reach it. A commit that happens to mention the
issue is incidental; the slug is put there by the skill that knows the answer.

### Step 4 — Repoint what states the old arrangement

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
- **`/task` forwards, it never interprets.** One sentence, no parameter list —
  so the skill acquires no notion of an issue, an export path, or what a PR
  closes. A `## Caller parameters` section here would have to be mirrored in
  `/go` to reach `/pr`, which is three skills carrying prose about issue
  handling to move a number that `/pr` can already work out for itself.
- **`Closes #N` stays `/pr`'s alone.** Step 3 widens an inference that skill
  already owns rather than adding a second route to the same fact; every
  statement about what a PR closes stays in the file that composes the body.
- **The export path is derived, not passed.** It is `docs/issue/<n>/issue.md`
  for the `<issue>` in hand, so anything that has the number has the path.
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

This plan is written assuming **(a)**. Under (b) nothing in Steps 1–4 changes —
only which branch they land on.

## QA

- `/issue` on a small issue (#72 is the live case) reaches the no-plan outcome,
  and the PR it opens carries `Closes #72` — inferred from the branch slug, with
  nothing passed.
- `/issue` on a large issue still writes a plan file and ends at the `/go`
  handoff, with `Closes #N` coming from `/plan`'s explicit `<issue>` as it does
  today.
- A split issue plans without re-running the call, so the explicit `<issue>`
  still wins wherever a parent reference could otherwise close the umbrella.
- `/task <what to do>` with no issue behind it behaves exactly as before.
- `./scripts/check-skill-catalog.sh` stays green.
