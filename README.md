# agent-project-boilerplate

Boilerplate for projects where Claude Code is a first-class collaborator.
Language- and framework-agnostic.

What it is: a `CLAUDE.md` seed carrying only conventions that hold regardless of
stack, **26 skills** (19 working out of the box, 7 stubs awaiting hydration) that
compose into a plan → implement → PR → land loop, the path-scoped `.claude/rules/`
mechanism, a SessionStart hook that makes `gh` work in remote sessions, and the
scripts behind it all.

Per-item descriptions live in **[`docs/catalog.md`](docs/catalog.md)** — one row
per skill, script and file, grouped so you can tell how much of it you need:

| Group | What it covers |
| --- | --- |
| **G0** | The sync path — how you pull later changes forward. |
| **G1** | Prose & principles: `CLAUDE.md`, `.claude/rules/`, `/dry`, `/tighten-docs`, `/explore`. |
| **G2** | The PR loop: `/plan`, `/implement`, `/pr`, `/finalize` and the mechanical pieces they compose. |
| **G3** | Issue & backlog: `/issue`, `/propose-issue`, `/audit-github-backlog`. |
| **G4** | Remote-session plumbing — the `gh` shim that makes the rest work on the web. |
| **G5** | CI & landing: `/watch-ci` and its polling scripts. |
| **G6** | Seven stack-bound stubs — hydrate the ones you need, delete the rest. |

The Python scripts are stdlib-only (3.9+) and use `$GH_TOKEN` or `gh auth token`;
the shell scripts need `gh`, `jq`, and `git`.

## Why `/plan` and `/implement` exist

Claude Code's web/remote sessions re-emit stacked plan-mode and `AskUserQuestion`
prompts after idling, silently losing answers
([anthropics/claude-code#72704](https://github.com/anthropics/claude-code/issues/72704)).
So a plan becomes a file the operator can pull and review from another machine,
and questions become prose that survives in the transcript.

## Getting it

Two routes. Both are documented in **[`ADOPTING.md`](ADOPTING.md)**, which owns
the procedure end to end.

### Create a new project from this template

Click **"Use this template" → "Create a new repository"** in the GitHub UI, or:

```bash
gh repo create <owner>/<your-new-repo> \
  --template vzakharov/agent-project-boilerplate \
  --public \
  --clone
```

(Use `--private` for private repos.) Then follow
[`ADOPTING.md` § Template fork](ADOPTING.md#template-fork) to prune what doesn't
apply and hydrate what does.

### Adopt into an existing repo

Paste this into an agent session in the target repo:

```
Adopt the agent infrastructure from https://github.com/vzakharov/agent-project-boilerplate
into this repo: clone it somewhere temporary, read ADOPTING.md, and follow it.
```

The agent selects a subset against your repo's actual shape — most of the criteria
are decidable by inspection, so it should need little from you beyond whether
your sessions run on the web and what your deploy/test surface looks like.

Either way, later changes here come forward with `/sync-upstream`, pointed at this
repo by your own `upstream.json`. The infrastructure is adoptable **and**
re-syncable; a fork is not a dead end.

## More

`CLAUDE.md` carries the conventions themselves, and each
`.claude/skills/*/SKILL.md` carries its own full contract.
