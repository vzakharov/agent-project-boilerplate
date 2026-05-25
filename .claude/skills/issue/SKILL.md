---
description: Take on a GitHub issue end-to-end — read the thread, split when scope demands it, implement, then open a draft PR.
---

## Step 1 — Read the issue

Use the GitHub CLI to load the full thread:

```bash
gh issue view <issue-number-or-url> --comments
```

For metadata (labels, assignees, linked PRs, etc.):

```bash
gh issue view <issue-number-or-url> --json title,body,labels,assignees,state,comments,url
```

If the issue references screenshots, mockups, or other attachments, save them locally to `docs/issue/<n>/attachments/` so they survive context handoffs. This directory is **optional** — only create it if you actually need to stash files. `prep-merge` cleans it up before the squash if it exists.

If `gh` auth fails or the repo isn't accessible, **stop and report** — do not start solving the task from the title alone.

## Step 2 — Splitting (high-scope)

### When splitting is even on the table

The bar for splitting is high. Do **not** split because:

- the issue mentions several files (most do)
- you can imagine a "phase 1 / phase 2" framing (most things admit one)
- decomposition feels tidy

Default to taking the issue as-is. Only split when the size is obviously beyond a single PR and the seams between sub-tasks are real, not invented. **Genuinely large** means multiple unrelated subsystems, weeks of work, or distinct deliverables that ship independently — not "many files" or a tidy phase breakdown.

For **truly** large work, you only need the **next** slice to be manageable in this run (something you can plan and ship in one branch/PR). Sub-issues you park in the backlog may themselves stay large — they are placeholders and ordering hints, not mini-specs. You do **not** owe a full implementation DAG or per-child plans up front: spell out the **immediate** work in detail, and give a **coarse** view of what follows.

How you handle an issue that **does** meet the bar depends on how the session was launched — **plan mode** vs **direct mode**.

### If the issue is split-worthy

**Plan mode** (session expects a written plan and an approval step): Do **not** ask for a separate split-only approval before the plan. **Include splitting inside the plan** — concrete sub-issue titles + one-line scope each, dependency order, which sub-issue you implement **first** in this branch, and that **after plan approval** you will create those sub-issues (each body references the parent with `Part of #<parent>`), comment on the parent listing them and the ordering, then execute (starting with the chosen first sub-issue or the parent, as the plan says). One approval gate covers both what to build and how issues are split.

**Direct mode** (editable session, no product plan gate): Propose the split in the thread (titles + one-line scope each, dependency order) and **ask the user to approve before creating** any sub-issues. If they approve:

1. Create one sub-issue per sub-task with a clear title, body, and a reference to the parent (`Part of #<parent>`).
2. Comment on the parent issue listing the sub-issues and the chosen ordering.
3. Pick the **most logical first sub-issue** and continue with it for the rest of the run.

### If the issue is not split-worthy

Say so in the written plan (plan mode) or briefly in the thread (direct mode) and take it as-is — no split subsection.

## Step 3 — Implement

**Branch name:** include the issue number **and** a short kebab-case slug (at most **three words**) that says what the change is about, e.g. `issue/847-fix-sidebar-scroll` or `issue/12-add-oauth-callback`.

Do the work the issue (and any written plan or thread agreement) calls for: branch, commits, product and test changes per repo conventions and the surrounding codebase. This skill does not spell out implementation detail — the issue thread, agreed plan, and project norms are the source of truth.

If you stashed anything under `docs/issue/<n>/` (Step 1), commit it to the branch alongside your first code commit. Keeping it on the branch lets any agent that resumes mid-task (after a context wipe, a handoff, or a parallel session) re-read the context without re-fetching. It does **not** end up on `main` — `prep-merge` deletes the directory in the last commit before `gh pr ready`, so the add-then-delete pair cancels out in the squash.

## Step 4 — Open a draft PR and report

Push your branch and open a **draft** PR (not ready for review). Draft is mandatory: a ready PR kicks off heavy CI before the user has looked at the change, which wastes time and compute.

Title: conventional-commit style, `<type>: #<issue-number> <subject>`. Body: short summary (2-3 paragraphs max) and a line that auto-closes the issue when merged — `Closes #<n>` for feature/refactor-style work, `Fixes #<n>` for bugfixes.

**Report to the user with a clickable PR link.** Summarize what's in the PR and stop.

## Step 5 — What comes next

The user will typically follow this with `@.claude/skills/prep-merge/SKILL.md` when they're ready to land the change. In one sentence: prep-merge runs the local gates (`./scripts/gates.sh`), merges latest `main`, deletes `docs/issue/<n>/` (if present) in the final pre-ready commit, flips the PR to ready, drafts a squash title/body for the user to approve, and watches CI through to green — it does not merge for you. **Do not read that skill file now**; just be aware it's the next step so you don't duplicate its work (in particular: do **not** delete `docs/issue/<n>/` yourself, do **not** run local gates, and do **not** flip to ready unless the user explicitly asks).
