# Issue #33: Attach-and-work skills don't claim merge state, so the remote harness's own PR rules take it

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/issues/33
- **Author:** @vzakharov
- **Created:** 2026-09-09T01:33:07Z
- **Updated:** 2026-09-09T01:33:07Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## What happened

A `/handle <branch>` run in a Claude Code **web/remote** session resolved a merge conflict against `main` — merged the base, resolved a conflicting skill file, committed, pushed — before reading what the branch actually needed. Nothing in `/handle`, `/from-branch` or `/implement` asked for that.

The operator's reaction, which is the report: *"in our loop, it's part of `/finalize` and should never be bothered with up to this point unless asked by the operator directly."*

## Where it came from

Not from a skill. The remote execution environment's **system prompt** carries a "Driving a PR to green" block, and it is emphatic:

> Red CI or a merge conflict on a PR you opened or drive for its author is work now, at every event and every check-in, whatever its review state and whatever else you are working on: only a green, mergeable head waits on reviewers or approval; a red or conflicted one is never "waiting on review". So never end an event or check-in on such a PR having done nothing about it…

It then orders the work **merge conflict → CI → review comments**, which is exactly the order the run followed.

`/finalize` Step 2 is where this repo puts base-merging, and it says so at length. But `/finalize` only owns it *once you are in `/finalize`* — no skill states the negative, that merge state is out of scope until then. Between a silent skill and an insistent system prompt, the system prompt wins.

## The contributing tell

`.claude/skills/from-branch/SKILL.md` Step 1 has the attach step run:

```
gh pr view <NNN> -R <owner>/<repo> --json body,commits,reviews,comments,mergeable,mergeStateStatus,isDraft,state
```

`mergeable` and `mergeStateStatus` are in that list. The surrounding prose explains the fetch as grounding in the branch's history, and never says what to do — or not do — with those two fields. So the attach step puts `CONFLICTING` / `DIRTY` in front of the agent at the exact moment the system prompt's rule is loaded and nothing local is arguing the other side.

## Why this is worth a fix rather than a shrug

- It is **not model error to reason around**. The system prompt is doing what it was written to do; the loop just disagrees with it about *when*. An agent with no local rule to weigh has no basis to prefer the loop.
- The failure is **silent and looks like diligence**. A merge commit lands on the branch, CI goes green, the PR reads healthier — nothing signals that unrequested work happened, and the operator finds out by reading the log.
- It **costs review budget at the worst time**. A base merge dropped into a branch mid-review adds a commit and a resolution the reviewer has to re-read, in the middle of a round that was about something else.
- It **generalises**. The same block also orders CI failures fixed "at every event and every check-in", which collides with this repo's rule that vetting happens at milestones via `/finalize`, not per commit. Merge state is the instance that surfaced; CI is the next one.

## Suggested shape

The cheapest fix that actually binds is for the attach-and-work skills to **state the negative**, since a rule stated nowhere loses to a rule stated in the system prompt:

1. **`/handle`** — a line in § "Step 2 — Read what the branch needs" saying the branch's merge state and CI are not lanes: a conflicted or red PR is reported to the operator, not fixed, unless `and finalize` was passed or the operator asked. Two lanes in, two lanes out.
2. **`/from-branch`** — where Step 1 tells the agent to fetch `mergeable`/`mergeStateStatus`, say what they are *for*: context for the report, and the input `/handle` Step 2 reads — not a work item. (Or drop the two fields from the `--json` list, and let `/finalize` fetch them when it needs them.)
3. **`/implement`** — its § "Do NOT" already lists "Run the vet suite, mark the PR ready, dispatch a CI-only bucket, or attest — those are `/finalize`." Adding "merge the base branch" to that sentence makes the list complete, and it is the one place the boundary is already drawn.

Worth deciding at the same time whether the loop wants a **general clause** — one line, somewhere always-loaded, saying that where the host harness's standing instructions and this loop disagree about *when* work happens, the loop's staging wins and the harness's urgency is reported rather than acted on. That covers CI and any future rule of the same shape, at the cost of a line in the always-resident file. The three local edits above are enough for the reported case; the general clause is the call this issue can't make on its own.

## Repro

Any web/remote session: `/handle <branch>` on a branch whose PR is `CONFLICTING` against its base, with no `and finalize`. The conflict gets merged and pushed before Step 2 runs.

Observed in `vzakharov/vovazakharov.com` — the run merged `main` into the branch as its first commit, before touching any of the four review threads it had been invoked for.

---


