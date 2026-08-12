---
description: >-
  Execute an already-approved plan end-to-end: implement it, then run the
  mandatory quality passes (/dry, /tighten-docs) and open
  a draft PR. Built to follow the /plan file-based stand-in, but also works with
  a plain approved plan. Invoke as `/implement` (or `/implement <branch>` to
  attach to an existing branch first).
---

This skill is the **execution phase** — what you do once a plan has the operator's go-ahead. It assumes approval already happened: invoking `/implement` (or reaching it via the `/plan` approval gate, or `/from-branch … implement`) **is** the go-ahead, so there's no plan cycle to open here. If you're mid-planning and the operator hasn't approved yet, that gate lives in `@.claude/skills/plan/SKILL.md` — resolve it there first, don't start coding.

Because that approval is an assumption, Step 1 puts it on the record: a `git mv` out of `*.draft.do-not-implement.md` whose commit message quotes the operator's literal go-ahead. Done retroactively it records nothing, so it precedes the first source edit rather than following it as cleanup.

## Branch-name form

`/implement <some/branch>` is shorthand for `/from-branch <some/branch> /implement` — attach to that existing branch, then run this skill. Load `@.claude/skills/from-branch/SKILL.md` and follow it to attach (it re-points the working tree and discards the auto-branch), then continue from Step 1 below. If no branch token was passed, `/implement` runs against the current branch as-is.

The branch form is the **normal** entry point, not an edge case: it is the command a `/plan` session hands the operator at the end of its turn, so implementation usually starts in a session that has to attach before it can do anything (see `@.claude/skills/plan/SKILL.md` § "Handing off").

**Canary — a well-formed handoff is a branch token in a session's first user prompt; every other shape is a copy that didn't land intact.** The block exists to _open_ a session on a branch this one is not on, so it goes wrong in two mirrored ways: it lands in a session that already exists (a branch token where it does not belong), or it arrives stripped of its branch (nothing to attach to).

- **`/implement <branch>` as the session's first user prompt, naming a branch other than the current one** is the intended cross-session path — attach as documented, no question.
- **Any other `/implement <branch>` → stop and ask** whether they meant to implement here or in a fresh session. That covers both wrong-box tells: the branch is already the current one (dead weight — usually a reflex copy right after reading the plan), or an earlier user prompt in this session means the block was pasted into a session with a life of its own. Do not attach, do not flip the plan file, do not touch source until they answer. Without this the already-checked-out tell is invisible: `@.claude/skills/from-branch/SKILL.md` § "Failure modes to call out" says "Target branch already checked out — skip Steps 2–4 and proceed to Step 6", so the attach degrades into a silent no-op and implementation just starts.
- **Bare `/implement` mid-session → no canary, no question.** That is the ordinary same-session go-ahead: the plan was made here and its context is in the conversation. Proceed straight to Step 1.
- **Bare `/implement` as the session's first user prompt → establish what there is to implement before proceeding.** A session that has done nothing yet holds no plan in conversation, so the only implementable thing is a plan file on the branch already checked out. On a harness auto-branch, or with `docs/plans/` empty, the block was copied without its branch token — **ask which branch**, rather than reporting "no plan found" and sending the operator after the wrong problem. A plan file sitting on a non-auto branch (a session opened straight onto the feature branch) is legitimate — proceed to Step 1.

Asking costs one round-trip. The point is that the operator makes the call knowingly, rather than discovering afterwards that the session they meant to keep as a clean planning record started writing code.

## Planless entry

A caller skill may enter here with a **task** in place of a plan — `@.claude/skills/from-branch/SKILL.md` Step 6's free-form follow-up, and `@.claude/skills/pr/SKILL.md` Step 1a's "no plan" waiver. In that mode:

- **Step 1 is already satisfied** — the caller's task text is the plan. Start at Step 2; do not go looking under `docs/plans/`, and do not ask which plan to implement.
- **Step 3 runs unchanged** — its passes are the reason this entry exists. The trailing `git mv` to `*.completed.md` is a no-op with no plan file.
- **Step 4 runs unchanged.** A branch that already has a PR — the normal `/from-branch` case — stops at `/pr`'s own Step 1b pre-check, which reports the existing PR rather than opening a duplicate.
- **The § "Branch-name form" canary does not apply.** It reads _user-typed_ prompts for a handoff block that lost its branch or landed in a session with a life of its own; a skill-to-skill dispatch already holding the task is neither.

Planless is not gateless: locating a plan is the only thing this entry skips.

## Step 1 — Locate the plan

The primary target is a `/plan` stand-in file:

- `ls docs/plans/*.md`. A `/plan` session writes exactly one and sweeps it at finalize, so **one file** is the normal case → read it fully; that's the plan.
- **More than one, or none** → don't guess; ask which plan to implement (numbered prose, per `@.claude/skills/plan/SKILL.md`). More than one means an earlier session forgot to sweep — list the candidates. None means either the file was never written or this is the rare plain-approved-plan case where the plan lives in the conversation (native plan mode / agreed in chat) — ask the operator which, and let them point you at it. Never author a fresh plan in this mode.

**A plan that still lists open questions is implementable when they carry recommendations.** `/plan` writes the recommended option into the plan as its single approach (`@.claude/skills/plan/SKILL.md` § Part 2), so the file is executable exactly as it stands and unanswered questions mean the recommendations hold. Implement it as written, and say in your turn which recommendations you took so the operator can correct any of them. Stop and ask only for a fork the plan text leaves genuinely open — no recommendation, nothing executable to fall back on.

The plan file's name encodes its lifecycle state (see `@.claude/skills/plan/SKILL.md` § "Plan file lifecycle"). Act on it **before writing any code**:

- `*.draft.do-not-implement.md` — not yet cleared. Reaching this skill **is** the go-ahead (the operator invoked `/implement`, approved at `/plan`'s gate, or launched `/from-branch … implement`), so **`git mv` it to `*.in-progress.md` as your first action**. In the **same commit**, also **delete the line-1 ⛔ draft banner** — once the file is `in-progress`, a banner that still says "DO NOT IMPLEMENT" contradicts its own state — and quote the operator's literal go-ahead in the commit message (e.g. `chore: begin implementing <slug> (go-ahead: "…")`). Do this before editing source — a file still named `do-not-implement`, or still carrying the banner, means you have not been cleared, and writing the go-ahead out verbatim is the moment to catch a misread. When the plain-approved-plan case has no file at all, there's nothing to flip; the operator's in-chat go-ahead stands.
- `*.in-progress.md` — already flipped (resumed work) → just continue.
- `*.completed.md` — implementation already finished → don't silently re-run; report and ask.

## Step 2 — Implement

Work through the plan on the current branch. Follow the plan as approved; if reality forces a material deviation, note it to the operator rather than silently reshaping scope.

Commit/push discipline is already governed by CLAUDE.md — don't reinvent it here:

- Commit and push proactively after each meaningful unit of work (CLAUDE.md "Git conventions" — feature branch in a remote/web env; the operator reviews from another machine and only sees pushed work).
- **Never force-push.** The operator may be following the branch as you work and needs the sequence of changes to read cleanly; force-pushing rewrites that history out from under them. Only ever advance the branch with new commits.
- Conventional-commit subjects; descriptive bodies.
- **Do not** run `./scripts/vet.sh` per commit on a feature branch — that's `/finalize`'s job once the operator has reviewed.

## Step 3 — Mandatory quality passes

These run **every time**, in order, and override any contrary "wrap up after implementing" instinct. Each is a real pass over the just-written diff, not a rubber stamp — and each commits its own edits.

1. **`/dry`** — did new duplication the plan didn't foresee creep in during implementation? Plans are written before the code exists, so WETness that wasn't visible at planning time often surfaces only now. Load `@.claude/skills/dry/SKILL.md` and run it over this session's diff: apply the obvious wins, surface the ambiguous calls.
2. **`/tighten-docs`** — load `@.claude/skills/tighten-docs/SKILL.md` and run it over the prose you added. It carries **two halves of equal weight**: rewriting edit-narration into present-tense contracts, and cutting prose back to the non-obvious contract at the length that contract takes. Its report is split into `Durability` and `Tightness` groups. Commit this pass's edits.

Then **`git mv` the plan to `docs/plans/<slug>.completed.md`** and commit — implementation and its quality passes are done. (`/finalize` sweeps the whole `docs/plans/` tree at squash regardless, so this flip is just the honest end-state marker for an operator watching the branch.)

## Step 4 — Draft PR

Implementing an approved plan is itself the operator's request for a PR, so it satisfies the system prompt's "don't open a PR unless asked" gate. Load `@.claude/skills/pr/SKILL.md` and follow it (it pushes and opens the draft with a derived title/body).

The **only** exception is an explicit "no PR" from the operator (e.g. `/implement, no PR`) — then stop after Step 3 and report.

## Do NOT

- Re-open a plan cycle or re-edit the plan file per code change — it's a transient artifact `/finalize` sweeps (see `@.claude/skills/plan/SKILL.md`). Leave it as the approved snapshot (under its `.in-progress.md` name); only refresh it when the operator specifically asks — e.g. so a fresh session can pick up the work from an up-to-date plan.
- Run the vet suite, mark the PR ready, dispatch a CI-only bucket, or attest — those are `/finalize`.
- Skip either Step-3 pass because the diff "looks clean." They're mandatory.
