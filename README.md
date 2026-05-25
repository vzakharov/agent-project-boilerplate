# agent-project-boilerplate

Boilerplate for new projects where Claude Code is a first-class collaborator. Language- and framework-agnostic.

Ships:

- **`CLAUDE.md`** — a tight, stub-filled seed designed to grow with the project. Universal principles only; project-specific conventions are filled in over time (by the agent and the human, together).
- **`.claude/skills/`** — five project-agnostic skills (see "What's included" below).
- **`.claude/hooks/session-start.sh`** — stub for installing dependencies in remote sessions; you implement it for your stack.
- **`scripts/gates.sh`** — stub for "local gates" (fast pre-push checks); you implement it for your stack.
- **`scripts/export-github-issue.py`** — ready-to-use exporter that downloads an issue (body + comments + timeline + attachments) into `docs/issue/<n>/`. Used by `/issue`. Python 3.9+ stdlib only; uses `$GH_TOKEN` or `gh auth token`.
- **`.claude/settings.json`** — minimal Claude Code project settings wiring the SessionStart hook.

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
2. Implement **`scripts/gates.sh`** for your stack. Until you do, `prep-merge` will stop loudly. See `CLAUDE.md` → Local gates.
3. Implement dep-install in **`.claude/hooks/session-start.sh`** so remote sessions start with a current `node_modules` / `venv` / equivalent.
4. Replace any other stubs in `CLAUDE.md` (repository layout, testing) as those conventions stabilize.
5. Commit and push.

## What's included

| Skill          | One-liner                                                                                          |
| -------------- | -------------------------------------------------------------------------------------------------- |
| `/issue`       | Take a GitHub issue end-to-end: read the thread, optionally split, implement, open a draft PR.    |
| `/prep-merge`  | Land prep: run local gates, merge `main`, flip to ready, draft squash title/body, watch CI.       |
| `/from-branch` | Attach the current session to an existing branch or PR, abandoning the auto-created session branch. |
| `/explore`     | Investigate the codebase via parallel Explore subagents.                                          |
| `/dry`         | Review the session's diff for DRY opportunities — applies obvious wins, surfaces ambiguous ones.  |

See `CLAUDE.md` and the individual `SKILL.md` files for the full contracts.
