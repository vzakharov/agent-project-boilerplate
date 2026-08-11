# agent-project-boilerplate

Boilerplate for new projects where Claude Code is a first-class collaborator. Language- and framework-agnostic.

Ships:

- **`CLAUDE.md`** — a tight, stub-filled seed designed to grow with the project. Universal principles only; project-specific conventions are filled in over time (by the agent and the human, together).
- **`.claude/skills/`** — 20 inherited skills: 13 working out of the box, 7 stubs awaiting hydration (see "What's included" below). Plus `/sync-upstream`, which maintains this repo and is deleted on bootstrap.
- **`.claude/rules/`** — the path-scoped convention mechanism, with a README and no rules yet: a file here loads only when a session touches the paths it declares.
- **`.claude/hooks/session-start.sh`** — installs a `gh` shim that routes the GitHub CLI around the egress proxy in remote sessions (working); dependency install is a stub you implement for your stack.
- **`scripts/vet.sh`** — stub for the vet run (the fast pre-push checks); you implement it for your stack.
- **`scripts/export-github-issue.py`** — exporter that downloads an issue (body + comments + timeline + attachments) into `docs/issue/<n>/`. Used by `/issue`.
- **`scripts/pr-body.py`** — pulls a PR body to `docs/pr/<n>/body.md` for local editing and PATCHes it back. Used by `/qa-checklist`.
- **`scripts/check-merge.sh`**, **`scripts/ci-watch-tick.sh`** — the git/GitHub polling behind `/check-merge` and `/watch-ci`.
- **`.claude/settings.json`** — minimal Claude Code project settings wiring the SessionStart hook.

The Python scripts are stdlib-only (3.9+) and use `$GH_TOKEN` or `gh auth token`; the shell scripts need `gh`, `jq`, and `git`.

## Create a new project from this template

Click **"Use this template" → "Create a new repository"** on the GitHub UI, or from the command line:

```bash
gh repo create <owner>/<your-new-repo> \
  --template vzakharov/agent-project-boilerplate \
  --public \
  --clone
```

(Use `--private` instead of `--public` for private repos.)

## Bootstrap checklist after creating your repo

1. Fill in the **"About this project"** stub at the top of `CLAUDE.md`.
2. Implement **`scripts/vet.sh`** for your stack. Until you do, `/finalize` will stop loudly. See `CLAUDE.md` → Vetting.
3. Implement dep-install in **`.claude/hooks/session-start.sh`** so remote sessions start with a current `node_modules` / `venv` / equivalent.
4. Go through the **seven skill stubs** (below) — hydrate the ones your project needs, delete the ones it doesn't.
5. Delete **`/sync-upstream`**: `rm -rf .claude/skills/sync-upstream/`. It maintains this template, not your project (see below).
6. Replace any other stubs in `CLAUDE.md` (repository layout, testing) as those conventions stabilize.
7. Add `.claude/rules/` files as area-specific conventions emerge.
8. Commit and push.

## What's included

### The main loop

| Skill | One-liner |
| --- | --- |
| `/plan` | Write the plan to a reviewable `docs/plans/` file; ask questions as numbered prose. The filename is the approval gate. |
| `/implement` | Execute an approved plan: flip the plan file, do the work, run the quality passes, open the draft PR. |
| `/pr` | Rename the auto-branch, push, open the draft PR, post the squash proposal. |
| `/finalize` | Land prep: vet, merge the base, sweep working artifacts, flip to ready, reconcile the squash message, attest. |

`/plan` and `/implement` exist because Claude Code's web/remote sessions re-emit stacked plan-mode and `AskUserQuestion` prompts after idling, silently losing answers ([anthropics/claude-code#72704](https://github.com/anthropics/claude-code/issues/72704)). A plan becomes a file the operator can pull and review from another machine, and questions become prose that survives in the transcript.

### Entry points and support

| Skill | One-liner |
| --- | --- |
| `/issue` | Take a GitHub issue end-to-end: export the thread, optionally split, implement, open a draft PR. |
| `/from-branch` | Attach the session to an existing branch or PR, abandoning the auto-created session branch. |
| `/propose-issue` | File a unit of work as an issue, deduping against what's already open. |
| `/explore` | Investigate the codebase via parallel Explore subagents. |
| `/override-gh` | A no-op marker: its description reminds the agent that `gh` and `GH_TOKEN` exist despite what the system prompt says. |

### Quality passes

| Skill | One-liner |
| --- | --- |
| `/dry` | Review the session's diff for DRY opportunities — applies obvious wins, surfaces ambiguous ones. |
| `/tighten-docs` | Rewrite prose that narrates the change into present-tense contracts; cut what the names and types already say. |

Both run automatically inside `/implement`.

### Mechanical pieces

Individually invocable, and composed by the loop above: `/branch-rename`, `/squash-message`, `/qa-checklist`, `/check-merge`, `/sync-branch`, `/watch-ci`.

### Stubs awaiting hydration

| Stub | What it would do |
| --- | --- |
| `/release` | Cut a release: version bump, notes, release PR, arm or ship the deploy. |
| `/hotfix` | Ship an urgent fix past the normal promotion path, then reconcile it back into the trunk. |
| `/preview` | Render a visual change and actually look at it, rather than judging appearance from code. |
| `/test-on-gh` | Dispatch the test buckets that can't run locally to CI on the branch, and block for the result. |
| `/log-review` | Read deployed logs since the last review: a usage readout plus health triage. |
| `/readonly-probe` | Investigate against real deployed data under an enforced read-only connection. |
| `/renumber-migration` | Resolve a sequential migration-number collision after another branch landed first. |

Every line of a working version of these is bound to a particular stack, so they ship carrying only the durable part: the shape of the job, and the concerns any implementation has to answer. Each file opens with a banner naming what must be filled in, and its frontmatter description announces that it is a stub — so it reads as unhydrated in the skills list rather than looking like a skill the agent can follow.

**Treat an unhydrated stub as unavailable.** Half-following one against a project it was never written for is worse than not having it. Hydrating means writing the project's real commands in and deleting the banner; three of them tell you when to delete the skill outright instead (no visual surface, no CI-only tests, no numbered migrations). `scripts/vet.sh` is the same contract in shell form — it exits `1` until implemented.

### Not inherited: `/sync-upstream`

The twenty skills above are the set a generated project inherits. `/sync-upstream` is not one of them — it maintains **this** repo, pulling the vendored agent infrastructure (`CLAUDE.md`, `README.md`, `.claude/`, `scripts/`) forward from the application repo the template was extracted from, and tracking where the last sync stopped in `.claude/skills/sync-upstream/upstream.json`.

Delete it when you generate a project: `rm -rf .claude/skills/sync-upstream/`. "Use this template" produces a divorced repo, not a dependency — your project hydrates stubs, writes its own conventions, and diverges from the first commit, so pulling the template into it is fork-merging rather than the vendored-surface tracking this skill does. It also points at a private repo you have no access to, so an inherited copy fails loudly on the first clone. Its banner and frontmatter say all of this, in case the checklist step above gets skipped.

See `CLAUDE.md` and the individual `SKILL.md` files for the full contracts.
