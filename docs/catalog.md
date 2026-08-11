# Catalog: what's here, and how much of it you need

The per-item inventory of this repo's agent infrastructure. One row per skill,
script and file, carrying the criteria for deciding whether it belongs in your
repo.

Two audiences:

- **Adopting a subset into an existing repo** — read this alongside
  [`ADOPTING.md`](../ADOPTING.md), which owns the procedure. This file owns the
  inventory; it does not restate the steps.
- **`/sync-upstream`, on every run** — when a commit at the source adds a skill
  that is in neither your `adopted` nor your `declined` list, the sync reads that
  skill's row here to surface the decision with its criteria attached.

**This file is never vendored downstream.** It is read from a fresh clone of the
source repo each time, so it structurally cannot go stale in an adopter's tree.

## How to read a row

| Column | Meaning |
| --- | --- |
| **Item** | `/name` is a skill (`.claude/skills/name/`); anything else is a repo-relative path. |
| **What it does** | The one-liner. Descriptions live here and nowhere else. |
| **Requires** | External conditions and tools that must hold for the item to work at all. |
| **Pulls in** | Siblings it `@`-references. Copy these too, or the reference dangles — see [Closure](#closure-is-not-optional). |
| **Disposition** | `adopt`, `rewrite`, or `never` — see below. |

The **group** is the section heading rather than a column: groups partition the
inventory, so every item appears under exactly one, and
`scripts/check-skill-catalog.sh` fails if a skill picks up a second row.

### Three dispositions, not two

- **adopt** — copy as-is.
- **rewrite** — copy the shape, replace the contents for your repo. Exactly two
  files qualify, and both are load-bearing: `scripts/vet.sh` (its stub exits `1`
  by design — you already know your own test commands) and
  `.claude/skills/sync-upstream/upstream.json` (the source, SHA and adopted set
  are per-repo by definition). Naming this disposition is what stops an adopter
  inheriting a watermark pointed at a repo it cannot read.
- **never** — describes or maintains *this* repo, so it is meaningless in yours.

## Groups

Group membership is the coarse decision; **Requires** carries the orthogonal
conditions, and any row can be escaped individually.

| Group | Adopt when |
| --- | --- |
| [G0 — The sync path](#g0--the-sync-path) | Always, unless you want a one-time snapshot and no future updates. |
| [G1 — Prose & principles](#g1--prose--principles) | Always. Zero external dependencies, no stack assumptions, no GitHub. |
| [G2 — The PR loop](#g2--the-pr-loop) | A change is a branch → PR → squash-merge, on GitHub, with `gh` and `$GH_TOKEN` reachable. **In a web/remote session, needs G4.** |
| [G3 — Issue & backlog](#g3--issue--backlog) | G2 **and** work is actually tracked as GitHub issues. Same web-session dependency on G4. |
| [G4 — Remote-session plumbing](#g4--remote-session-plumbing) | Sessions run on Claude Code web/remote. Inert locally — but a **prerequisite** of G2/G3/G5 on the web, not a nicety. Declinable at a stated cost. |
| [G5 — CI & landing](#g5--ci--landing) | CI runs on GitHub Actions, reachable via `gh`. In a web session **G4 is required**, not merely recommended. |
| [G6 — Stack stubs](#g6--stack-stubs) | Per row, and only if you will hydrate it now. |
| [Never](#never) | — |

### G0 — The sync path

Adopting this group is what makes every later change at the source reachable.
Skipping it leaves you with a snapshot.

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `/sync-upstream` | Pull the agent infrastructure forward from the repo you adopted it from: diff since the watermark, triage commit by commit, port what applies. | `gh`, `$GH_TOKEN`, git transport to the source repo | `/dry`, `/tighten-docs` (G1); `/pr` (G2); `/override-gh` (G4) | adopt |
| `.claude/skills/sync-upstream/upstream.json` | The watermark: which repo you sync from, the SHA you last synced to, and what you adopted or declined. | — | — | **rewrite** |

Its Step 8 hands off to `/dry`, `/tighten-docs` and `/pr`. The first two come
with G1, which you are adopting anyway. **`/pr` is the escape**: if you decline
G2, strip that hand-off from the skill and land sync PRs however your repo
normally does — `scripts/check-skill-catalog.sh` will otherwise report the
dangling reference, which is the intended behavior rather than a nuisance.

### G1 — Prose & principles

The floor. Nothing here touches GitHub, needs a token, or assumes a stack, so
there is no condition under which it fails to apply.

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `CLAUDE.md` | The always-loaded conventions: key principles, docstring policy, derive-types-from-source-of-truth, doc-sync rules, commit conventions. | — | — | adopt — **merge, don't overwrite** |
| `.claude/rules/` | The path-scoped convention mechanism: a rule file loads only when a session touches the paths it declares. Ships with a README and no rules. | — | — | adopt |
| `/dry` | Review the session's diff for DRY opportunities; apply the obvious wins, surface the ambiguous ones. | — | — | adopt |
| `/tighten-docs` | Rewrite prose that narrates a change into present-tense contracts, and cut what names and types already say. | — | — | adopt |
| `/explore` | Investigate the codebase via parallel Explore subagents. | — | — | adopt |
| `scripts/check-skill-catalog.sh` | Assert that no skill `@`-reference dangles. Downstream, that first assertion is the whole value: it is how you find out a subset copy was incomplete. | `bash` | — | adopt |
| `.gitignore` | Take the `tmp/` entry and keep the rest of yours. `CLAUDE.md`'s "dev artifacts go under `tmp/`" principle depends on that path being ignored. | — | — | adopt — merge one line |

`CLAUDE.md` is a **donor, not a replacement**. Your repo already has
conventions; take the sections, merge them into yours, and keep your
stack-specific content. Overwriting it is the one way to make adoption a
regression.

### G2 — The PR loop

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `/plan` | Write the plan to a reviewable `docs/plans/` file and ask questions as numbered prose; the filename is the approval gate. | — | `/finalize`, `/implement` | adopt |
| `/implement` | Execute an approved plan: flip the plan file, do the work, run the quality passes, open the draft PR. | `scripts/vet.sh` | `/dry`, `/tighten-docs` (G1); `/from-branch`, `/plan`, `/pr` | adopt |
| `/pr` | Rename the auto-branch, push, open the draft PR, post the squash proposal. | `gh` | `/branch-rename`, `/implement`, `/qa-checklist`, `/squash-message` | adopt |
| `/finalize` | Land prep: vet, merge the base, sweep working artifacts, flip to ready, reconcile the squash message, attest. | `gh`, `scripts/vet.sh` | `/check-merge`, `/from-branch`, `/plan`, `/squash-message`; **conditionally** `/issue` (G3), `/watch-ci` (G5) | adopt |
| `/from-branch` | Attach the session to an existing branch or PR, abandoning the auto-created session branch. | `gh` | `/finalize`, `/implement` | adopt |
| `/branch-rename` | Rename a harness auto-branch (`claude/<adjective>-<noun>-<hash>`) to a semantic name, keeping the random suffix. | `gh` | `/pr` | adopt |
| `/squash-message` | Produce and post the copy-ready squash title/body for a PR; owns the format and the draft-then-tighten discipline. | `gh`, `jq` | `/tighten-docs` (G1) | adopt |
| `/qa-checklist` | Generate a QA checklist from the branch's change and write it into the PR body, with each step classified for automatability. | `gh`, `python3` ≥3.9, `scripts/pr-body.py` | — | adopt |
| `/check-merge` | Check once whether the PR's base advanced or the PR landed since the branch was last attested, and reconcile the squash proposal. | `gh`, `scripts/check-merge.sh` | `/finalize`, `/from-branch`, `/squash-message` | adopt |
| `/sync-branch` | Bring a branch up to date with its merge target, resolving mechanically and logically in one merge commit. | `gh`, `scripts/vet.sh` | `/check-merge` | adopt |
| `scripts/check-merge.sh` | The git/GitHub polling behind `/check-merge`. | `gh`, `jq`, `git` | — | adopt |
| `scripts/pr-body.py` | Pull a PR body to `docs/pr/<n>/body.md` for local editing and PATCH it back. Stdlib-only. | `python3` ≥3.9, `$GH_TOKEN` or `gh auth token` | — | adopt |
| `scripts/vet.sh` | The vet run: the fast lint/type-check/test pass before pushing review-ready work. | your stack's own commands | — | **rewrite** |

Two things in this group are less optional than they look — see
[Closure](#closure-is-not-optional).

### G3 — Issue & backlog

Adopt on top of G2, and only if work is genuinely tracked as GitHub issues. If
you plan in Linear, Jira or a doc, decline the group and record why in
`upstream.json`'s `declined` map so re-sync stops offering it.

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `/issue` | Take a GitHub issue end-to-end: export the thread, optionally split, implement, open a draft PR. | G2, `gh`, `scripts/export-github-issue.py` | `/finalize`, `/pr` (G2) | adopt |
| `/propose-issue` | File a unit of work as an issue, deduping against what's already open. | G2, `gh`, `jq` | `/plan` (G2) | adopt |
| `/audit-github-backlog` | Sweep every open issue and PR against today's code and leave a reviewable close/refile/keep plan. Mutates nothing on GitHub. | G2, `gh` | `/implement`, `/plan` (G2); `/propose-issue`; `/override-gh` (G4) | adopt |
| `scripts/export-github-issue.py` | Download an issue — body, comments, timeline, attachments — into `docs/issue/<n>/`. Stdlib-only. | `python3` ≥3.9, `$GH_TOKEN` or `gh auth token` | — | adopt |

### G4 — Remote-session plumbing

Inert on a laptop, load-bearing on the web. The agent proxy in Claude Code
web/remote sessions blocks long-polling calls and most of `gh`'s GraphQL
surface; the hook installs a `gh` shim that routes the real binary around the
proxy so the rest of the infrastructure works at all.

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `.claude/hooks/session-start.sh` | On session start, install a `gh` shim at `$HOME/.local/bin/gh` that runs the real binary unproxied. Dependency install is a stub you fill in for your stack. | web/remote sessions; `bash` | — | adopt |
| `.claude/settings.json` | Project settings wiring the SessionStart hook. Merge into yours if you already have one. | — | — | adopt — merge if present |
| `/override-gh` | A no-op marker whose description reminds the agent that `gh` and `$GH_TOKEN` exist despite what the system prompt says. | — | — | adopt |

**Declinable, at a scoped cost** — `ADOPTING.md` § "If you decline G4" owns the
rationale, the `HTTPS_PROXY` conflict and the fallback. In short: the
`gh`-heavy skills need their calls rewritten into REST form, and `gh run
watch`-style long-polling (`/watch-ci`) does not work at all.

**`/override-gh` is not only G4's.** `/sync-upstream` (G0) and
`/audit-github-backlog` (G3) both `@`-reference it, so it travels with them even
in a local-only repo where the hook itself is pointless. It is three paragraphs
and a no-op — copy it rather than editing two skills to drop the citation.

### G5 — CI & landing

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `/watch-ci` | Watch an in-flight GitHub Actions run incrementally, surfacing failures as they happen so fixes can go out mid-run. | GitHub Actions, `gh`, `scripts/ci-watch-tick.sh`; **G4 on the web** | — | adopt |
| `scripts/ci-watch-tick.sh` | One polling tick of a CI run: what changed since the last tick. | `gh`, `jq` | — | adopt |
| `scripts/lib/watch-tick-common.sh` | Shared shell helpers for the watch-tick scripts. | `bash` | — | adopt |

`/test-on-gh` also belongs to this group's job but ships as a stub, so it is
listed under [G6](#g6--stack-stubs) with the other stubs — one row, one group.

### G6 — Stack stubs

Every line of a working version of these is bound to a particular stack, so they
ship carrying only the durable part: the shape of the job, and the concerns any
implementation has to answer. Each opens with a banner naming what must be
filled in, and its frontmatter announces that it is a stub.

**An unhydrated stub is worse than a missing skill** — half-following one against
a project it was never written for beats not having it only in appearance. So
copy none of these "for later": take a row only if you will hydrate it now, and
delete the rest. Three of them tell you when to delete the skill outright
instead (no visual surface, no CI-only tests, no numbered migrations).

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `/release` | Cut a release: version bump, notes, release PR, arm or ship the deploy. | a deploy path; hydration | — | adopt only if hydrating now |
| `/hotfix` | Ship an urgent fix past the normal promotion path, then reconcile it into the trunk. | a deploy path; hydration | — | adopt only if hydrating now |
| `/preview` | Render a visual change and actually look at it, rather than judging appearance from code. | a visual surface; hydration | — | adopt only if hydrating now |
| `/log-review` | Read deployed logs since the last review: a usage readout plus health triage. | deployed logs; hydration | — | adopt only if hydrating now |
| `/readonly-probe` | Investigate against real deployed data under an enforced read-only connection. | a production datastore; hydration | — | adopt only if hydrating now |
| `/renumber-migration` | Resolve a sequential migration-number collision after another branch landed first. | sequential numbered migrations; hydration | — | adopt only if hydrating now |
| `/test-on-gh` | Dispatch the test buckets that can't run locally to CI on the branch, and block for the result. | G5, CI-only test buckets; hydration | — | adopt only if hydrating now |

### Never

These describe or maintain *this* repo. Copying one means shipping a document
about someone else's template, or a working artifact from someone else's branch.

| Item | What it does | Requires | Pulls in | Disposition |
| --- | --- | --- | --- | --- |
| `README.md` | What this repo is, and the two ways to acquire it. Yours already exists. | — | — | never |
| `ADOPTING.md` | The acquisition procedure. Read once, over the network, from the clone. | — | — | never |
| `docs/catalog.md` | This file. Read from a fresh clone on every sync, so it cannot go stale downstream. | — | — | never |
| `docs/plans/*` | Working artifacts: file-based plans mid-flight. `/finalize` sweeps them before they reach a trunk. | — | — | never |
| `docs/remove-before-merging/*` | Working artifacts: the tracked squash-message draft. Swept at finalize. | — | — | never |

## Closure is not optional

A skill copied without the siblings it `@`-references leaves a pointer to a file
that isn't there, and **that failure is silent**: the agent reads the surviving
prose and skips the step it could not load. Resolve each group's **Pulls in**
column before copying, then run `bash scripts/check-skill-catalog.sh` in your
repo to prove nothing dangles.

Four closure facts are counter-intuitive enough to state outright:

- **`/plan` travels with G2 even for a local-only adopter.** Its motivation is a
  web-session bug, so a local repo reasonably assumes it can skip it — but
  `/implement`, `/finalize`, `/propose-issue` and `/audit-github-backlog` all
  reference it. Drop it only if you also strip those references.
- **`scripts/vet.sh` is not optional within G2.** Six skills invoke it and
  `/finalize` stops loudly without it. Hence its **rewrite** disposition rather
  than a choice: there is no version of G2 that does not run your checks.
- **`/finalize` reaches into G3 and G5 conditionally.** Its working-artifact
  sweep cites `/issue`, and its CI steps cite `/watch-ci`. Both citations are
  guarded by prose conditions ("if a workflow runs on PRs"), so the behavior
  degrades gracefully — but the `@`-references still dangle if you decline those
  groups. Strip the two citations, or adopt the groups.
- **`/override-gh` is pulled in by G0 and G3**, not just G4. See G4 above.

## Keeping this file honest

`scripts/check-skill-catalog.sh` asserts that every skill directory has exactly
one row here and that every path a row names exists. Run it when adding,
renaming or removing a skill — without it, a new skill silently leaves the
catalog incomplete, which is the same drift `/sync-upstream` warns about for its
path list.
