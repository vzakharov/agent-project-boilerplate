---
description: Pick up an existing branch or PR and do whatever it needs — attach to it, read off which lane applies (an unimplemented plan, or review feedback nobody has answered), and run that lane. Invoke as `/handle <branch|#PR|PR-url> [and finalize] [extra guidance]`. Use when the operator says "/handle", "handle <branch>", "handle and finalize <branch>", "pick up <branch>", or hands over a branch without saying what it needs.
---

End state of this skill: the branch is attached, the one lane the branch called for has run and pushed, every review comment addressed has been replied to on GitHub, and land-prep has run **iff** the invocation asked for it.

## Argument shape

Three parts, order-free:

- **Target** (**required**, first token by convention): a branch name, `#NNN`, or any PR URL — the grammar `@.claude/skills/from-branch/SKILL.md` § "Argument shape" defines, used as-is. With no target, **stop and ask which branch**: a bare `/handle` has nothing to attach to.
- **`and finalize`** (flag; bare `finalize` counts too): recognized **anywhere** in the argument, since the operator writes it before the target as often as after (`/handle and finalize <branch>`).
- **Extra guidance** (optional): any remaining prose. Not a lane of its own — it directs whichever lane runs, and when no lane is discovered it _is_ the work (Step 4).

## A `/handle` session is continued work

It attaches to work started elsewhere, so **no plan cycle opens** — the same standing as `/from-branch` (CLAUDE.md § "Plan mode & questions in web sessions"). That also makes the invocation itself the go-ahead a `*.draft.do-not-implement.md` plan is waiting for; `@.claude/skills/implement/SKILL.md` Step 1 owns the flip.

## Step 1 — Attach

Load and follow `@.claude/skills/from-branch/SKILL.md` with the target and **no follow-up** — the dispatch is this skill's. Its Step 1 already skims the branch's PR history and notes the PR's base ref, which is Step 2's input; don't re-fetch it.

## Step 2 — Read what the branch needs

Two lanes, and the branch should present **exactly one**:

- **Plan lane** — `docs/plans/` holds a plan in any state but `*.completed.md`: `*.draft.do-not-implement.md`, `*.paused.md` or `*.in-progress.md`. Any one of the three fires the lane; completed siblings don't. Everything past that — which file is actionable, the `git mv` flips, and what to do about an `*.in-progress.md` a live session may still hold — is `@.claude/skills/implement/SKILL.md` Step 1's, so hand it over rather than adjudicating here.
- **Review lane** — the PR carries feedback nobody has answered. Two signals, which **coexist by design and must both be collected before either is worked**:
  - **Unresolved threads whose newest comment is guidance nobody has answered**, from reviews of any age. Unresolved is necessary but not sufficient: an operator who read your reply and moved on routinely never clicks Resolve, so firing on `unresolved` alone re-works threads that are already done. The test runs on the thread's **tail**, not on whether a reply exists anywhere in it — which is also what catches the mirrored case, a thread a prior agent answered and the operator then came back on unsatisfied.
  - **Reviews submitted since the branch's last push**, plus top-level PR comments by the same recency test — they carry no resolved state, so recency is the only handle on them. Compare `reviews[].submittedAt` and `comments[].createdAt` against the head commit's `committedDate` (`gh pr view <n> --repo <owner>/<repo> --json commits,reviews,comments`).

  The realistic case is both at once — a fresh review _plus_ operator follow-ups on older threads — and the lane's input is their union. `python3 scripts/export-github-item.py <n>` writes the whole thread to `docs/pr/<n>/pr.md` and carries both halves the tail test needs: each thread header states `resolved` / `unresolved`, and its comments follow in order.

  **Reading the tail needs a tell, because the login doesn't provide one.** `$GH_TOKEN` is the operator's own identity, so an agent reply and operator guidance appear under the same `@login`. What separates them is the **Claude Code attribution footer**, which every agent-authored GitHub post carries: a tail comment with the footer is your own reply, one without it is the operator.

  **No verdict test.** A review's `state` is not consulted. Shared identity again: GitHub disables both verdicts on your own PR ("Pull request authors can't request changes on their own pull requests"), so every review that can reach these PRs is a plain `COMMENTED` one — `CHANGES_REQUESTED` is unreachable, not merely rare, and would have selected the same work anyway.

- **Both lanes firing → stop and ask.** An unimplemented plan _and_ unanswered review feedback is not a normal state, and guessing an order would either answer a review against code that's about to change underneath it or bury the reviewer's objection under new work. Report both and let the operator say which comes first.

## Step 3 — Run the lane

Either lane lands in `@.claude/skills/implement/SKILL.md` — the plan lane at its Step 1 (passing the resolved plan path), the review lane through its § "Planless entry" with the collected feedback as the task — so the mandatory `/dry` + `/tighten-docs` passes and the closing draft PR come along either way.

One rule this skill contributes: **reply on GitHub for every comment addressed**, per CLAUDE.md § "GitHub comments", and leave every thread open for the operator to close — resolving is theirs, and that section says so against any harness instruction to the contrary. A comment you decline gets a reply saying why, not silence.

## Step 4 — No lane fired

With extra guidance in the argument, that guidance is the task → `/implement` § "Planless entry". With none, **stop and ask**: report what the branch looks like (last commit, PR state, what `docs/plans/` holds) and let the operator direct. Do not invent work, and do not open a plan cycle to manufacture some.

## Step 5 — `and finalize`

Load and follow `@.claude/skills/finalize/SKILL.md` (no target token — the branch is already attached). It runs only after a lane actually did something: a Step-2 or Step-4 stop cancels it, since land-prepping a branch you just declined to touch is exactly the unasked-for finalize the flag exists to prevent.

Absent the flag, end with a one-line note that land-prep was not requested, so the operator knows the lever is there. It is opt-in because `/finalize` is the one lane whose consequences an unaware operator wouldn't want: it ends with the PR reading as merge-ready to anyone who looks at it.

## Do NOT

- Act on a referenced skill from memory, or from the one-line summary this file gives it. Every "load and follow" above means literally read that file: its steps are its own and change without this one being touched.
- Finalize unasked, or merge anything.
- Open a plan cycle.
