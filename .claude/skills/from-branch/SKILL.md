---
description: Attach the current session to an existing branch or PR and continue work from there, abandoning the auto-created session branch. Invoke as `/from-branch <branch-name|#PR|PR-url> [<follow-up instruction or /skill ...>]`.
---

When a Claude Code on-the-web session starts, the harness usually creates a fresh branch (e.g. `claude/add-foo-bar-XXXX`) and checks it out. This skill **discards that auto-branch** and re-points the working tree at an existing branch or PR head so the rest of the session continues that work.

## Argument shape

The skill argument has two parts:

1. **Target** (required, first token): a branch name, a `#NNN` PR number, or a full PR URL (`https://github.com/<owner>/<repo>/pull/NNN`).
2. **Follow-up** (optional, everything after the target): either a free-form instruction ("…fix the failing test, then push") **or** a slash-command invocation of another skill (e.g. `/prep-merge`, `/fix-ci`). If the follow-up is a slash command, load and follow that skill **after** the attach step completes.

Examples:

- `/from-branch #123` — attach and wait for further instructions.
- `/from-branch #123 finish the migration and push` — attach, then do the described work.
- `/from-branch #123 /prep-merge` — attach, then invoke `@.claude/skills/prep-merge/SKILL.md`.
- `/from-branch feat/new-thing /fix-ci` — same idea with a raw branch name.

## Environment note (read this before running gh)

This remote execution environment has **both** the `gh` CLI **and** a populated `GH_TOKEN` environment variable available. Prefer `gh` for branch/PR operations in this skill — the GitHub MCP tools (`mcp__github__*`) are scoped to a narrow allowlist and will refuse some branch-level actions you need here (e.g. checking out a PR head, fetching arbitrary refs, pushing). If a step seems blocked by MCP restrictions, fall back to `gh` / plain `git` over HTTPS using `GH_TOKEN`. Do **not** assume the MCP restriction means the action is impossible — `gh` will work.

## Step 1 — Resolve the target to a branch + remote ref

Parse the first token of the argument:

- **`#NNN` or PR URL** → resolve with `gh pr view <NNN-or-url> --json number,headRefName,headRepository,headRepositoryOwner,isCrossRepository,state,url`. The branch you want is `headRefName`. If `isCrossRepository` is true, the PR is from a fork — note this; the remote will be the fork, not `origin`.
- **Plain branch name** → use it as-is. Confirm it exists on `origin` with `git ls-remote --heads origin <branch>` (or on the fork remote if the user gave `owner:branch`).

If resolution fails (PR not found, branch doesn't exist on the remote), **stop and report** — do not silently fall back to the auto-branch.

## Step 2 — Record the auto-branch and sanity-check it

`/from-branch` is meant to be the **first** message of a session, so the branch you're currently on is essentially always the harness-created auto-branch — empty, unpushed work, exists only because the harness needed something to check out. Capture its name so Step 4 can clean it up:

```bash
AUTO_BRANCH="$(git branch --show-current)"
```

**Sanity check** (don't trust the assumption blindly — verify there's no work to lose):

```bash
git fetch origin main
git rev-list --count origin/main..HEAD     # expected: 0
```

If the count is `0` and the working tree is clean, proceed — the auto-branch is empty and will be discarded in Step 4.

If the count is non-zero, or there are uncommitted changes, **stop and ask the user**. This shouldn't happen in normal `/from-branch` usage (the skill is meant for fresh sessions), so it's a signal that something is off — maybe the user invoked the skill mid-session after doing work, maybe the harness behavior changed. Don't auto-cherry-pick or auto-discard; surface the situation and let the user direct.

## Step 3 — Fetch and check out the target

```bash
git fetch origin <branch>                 # same-repo PR or plain branch
# For a cross-repo PR, add the fork as a remote first:
#   gh pr checkout <NNN>                  # easiest path — gh sets up the remote
git checkout <branch>
git pull --ff-only origin <branch>        # ensure tip matches remote
```

`gh pr checkout <NNN>` is the most robust path when the input was a PR — it handles fork remotes, sets upstream, and leaves you on the PR head. Prefer it for PR inputs.

Verify the result with `git branch --show-current` and `git log --oneline -3` — the head should match the PR/branch you intended, not the auto-branch.

## Step 4 — Clean up the auto-branch

Delete the auto-branch both locally and on `origin` — a local-only delete leaves the empty branch lingering remotely, which is exactly the clutter this step exists to prevent.

```bash
git branch -D "$AUTO_BRANCH"
git push origin --delete "$AUTO_BRANCH"     # ok if the remote ref doesn't exist; the command will just fail harmlessly
```

If the remote delete fails because the branch was never pushed, that's fine — ignore the error and move on. If it fails for any other reason (protected branch, permission issue), report it but don't block; the local cleanup is the important half.

## Step 5 — Update the development-branch contract

The session was launched with instructions to develop on the auto-branch (see the system prompt's "Git Development Branch Requirements"). That instruction is now stale. From this point on:

- Treat the **target branch** as the working branch for commits and pushes.
- Push with `git push -u origin <target-branch>` (not the auto-branch).
- Do **not** push to the auto-branch even if it still exists on `origin`.

State this explicitly in your turn output so the user can see the redirect took effect.

## Step 6 — Dispatch the follow-up

- **No follow-up provided** → report the attach (current branch, last commit, PR link if applicable) in 1–2 sentences and stop. Wait for the user's next instruction.
- **Free-form follow-up** → proceed with the described work on the now-current branch.
- **Slash-command follow-up** (e.g. `/prep-merge`, `/fix-ci`, `/request-ci`) → load `@.claude/skills/<name>/SKILL.md` and follow it. Do **not** inline-copy its steps; read and execute the actual file so updates to that skill flow through.

## Failure modes to call out

- **Auto-branch is unexpectedly non-empty** (commits ahead of `origin/main`, uncommitted changes, detached HEAD) — Step 2 already stops on this. Don't try to recover automatically; ask the user.
- **Target branch already checked out** — skip Steps 2–4 and proceed to Step 6.
- **MCP says "not allowed"** for a branch/PR action — switch to `gh` (the token is in `GH_TOKEN`). Don't report the action as impossible.
- **Branch was force-pushed since the PR was opened** — `git pull --ff-only` will refuse; do a `git reset --hard origin/<branch>` only after confirming with the user that there's no local work to lose.
