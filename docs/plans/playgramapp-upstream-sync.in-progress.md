# Sync agent infrastructure from `Playgramai/playgramapp`

## Context

This repo was extracted from `playgramapp` at `2280857` (2026-05-25 12:28 +03:00) and has not moved since — its only commits are the initial scaffold. Upstream has run ~250 commits touching `CLAUDE.md`, `.claude/`, and `scripts/` in the intervening 11 weeks.

The delta is not incremental polish. Upstream **decomposed the monolithic `/prep-merge`** into a family of composable skills and **introduced a plan-file lifecycle** that routes around a Claude Code web-session bug. Skill count went 5 → 34.

| | boilerplate (today) | playgramapp (today) |
|---|---|---|
| Skills | 5 | 34 |
| `.claude/rules/` | — | 9 path-scoped auto-loaded rule files |
| `CLAUDE.md` | 118 lines | 150 lines |
| `session-start.sh` | dep-install stub | dep-install + `gh` proxy shim |

### The structural change

`prep-merge` no longer exists upstream. What it did is now:

- **`/draft-pr`** — rename auto-branch → push → create draft PR → post squash proposal
- **`/finalize`** — gates → merge base → sweep working artifacts → ready → reconcile squash → verify → attest
- **`/squash-message`** — owns the squash title/body format and its sticky PR comment
- **`/qa-checklist`** — owns the PR body's QA section
- **`/branch-rename`**, **`/check-merge`**, **`/sync-branch`**, **`/watch-ci`** — the mechanical pieces, individually invocable

And a new front half:

- **`/plan`** — writes plans to `docs/plans/<slug>.draft.do-not-implement.md`; the filename is the approval gate. Asks questions as numbered prose rather than via `AskUserQuestion`.
- **`/implement`** — executes an approved plan, runs the quality passes, opens the draft PR.

Both exist because web/remote sessions re-emit stacked plan-mode and `AskUserQuestion` prompts after idling, silently losing answers ([anthropics/claude-code#72704](https://github.com/anthropics/claude-code/issues/72704)). That bug is environment-level, not Playgram-specific — the workaround belongs in a boilerplate aimed at web sessions.

## Scope

Import the project-agnostic surface; leave Playgram's stack behind. Each imported skill is de-playgrammed: `pnpm precommit` → `./scripts/gates.sh`, `pnpm gh:export` → `python3 scripts/export-github-issue.py`, and Railway/Drizzle/Weaviate/Mantine/Supabase references dropped rather than genericized into vagueness.

Skills fall into three dispositions: **imported working** (Tier A + B — usable the moment a project is bootstrapped), **imported as stubs** (Tier C — the shape and the durable concerns, awaiting hydration for the host stack), and **not imported**.

### Tier A — the core loop (replaces what's here)

| Skill | Disposition |
|---|---|
| `plan` | **new** — verbatim minus the CLAUDE.md cross-refs; keep the `## DRY notes` requirement (adding the matching CLAUDE.md principle) |
| `implement` | **new** — quality passes become `/dry` + `/tighten-docs` |
| `draft-pr` | **new** — drop the `Playgramai/playgramapp` hardcoding; read the repo from `git remote` |
| `branch-rename` | **new** — generic as-is |
| `finalize` | **new, replaces `prep-merge`** — see below |
| `squash-message` | **new** — generic as-is |
| `qa-checklist` | **new** — generic as-is |
| `check-merge` | **new** — keep generic base resolution (`baseRefName`); drop `staging`/`production`/`epic/*` lanes |
| `sync-branch` | **new** — generic as-is |
| `watch-ci` | **new** — GitHub Actions generic; drop release/hotfix/nightly lane names |
| `from-branch` | **update** — take upstream's deep-link parsing, PR-history skim, and `implement` dispatch; drop epic-slice detection |
| `issue` | **update** — take the video-attachment `ffmpeg` guidance and the "carry original reports into each sub-issue" section; **keep** our Python exporter |
| `prep-merge` | **delete** — superseded by `draft-pr` + `finalize` |

**`finalize` de-playgramming** is the largest single edit. Kept: the draft-PR pre-check, base resolution, two-shot rule, base-merge-then-look-for-overlap step, working-artifact sweep (`docs/issue/`, `docs/plans/`, `docs/remove-before-merging/`), ready-for-review, squash reconciliation, base-advanced deliberation, and the **attestation comment** — which is generic and load-bearing (a reviewer cannot otherwise tell a verified branch from an unverified one). Dropped: the integration-bucket dispatch and E2E reasoning (step 6), which are entirely `test-on-gh`/Vitest-specific. `pnpm precommit` → `./scripts/gates.sh` throughout.

### Tier B — quality and support

`tighten-docs`, `propose-issue`, and **`override-gh`**.

`override-gh` is nine lines and earns its place: this very session burned several turns concluding upstream was unreachable because the system prompt says "you do NOT have access to the `gh` CLI" while `gh` and `GH_TOKEN` were in fact present. A marker skill whose description contradicts that in the skills list is the cheapest possible fix.

### Tier C — imported as stubs

These cover needs almost every repo has, but every line of upstream's implementation is stack-bound. Import each as a **stub**: the durable shape plus the concerns that hold regardless of stack, explicitly marked as needing hydration for the host project. Same contract `scripts/gates.sh` already uses, so the pattern is established rather than invented.

`release`, `hotfix`, `preview`, `test-on-gh`, `log-review`, `readonly-probe`, `renumber-migration`.

**Stub shape** — each `SKILL.md` carries:

1. A frontmatter `description` that names the skill's job **and** states it is an unhydrated stub, so it reads correctly in the skills list.
2. A `> ⚠️ **STUB**` banner: what must be filled in before the skill is usable, and an instruction to delete the banner once hydrated.
3. **What this skill is for** — the universal shape, in one short section.
4. **Concerns that hold regardless of stack** — the substance. Distilled from upstream's working version, with every Playgram specific stripped:

| Stub | Agnostic concerns it carries |
|---|---|
| `release` | version scheme and whether the prefix is reserved; a notes file per version; whether merging *arms* a deploy or *ships* one; tag or no tag; which gate must be green before arming; who owns the version bump |
| `hotfix` | branch off the production ref, not the trunk; bypasses the normal promotion path; must be reconciled back into the trunk or the fix is lost on the next release; needs its own durable record; exists because "is the trunk safe to ship" is a question you can't always answer yes to |
| `preview` | judging appearance by reading code is the failure mode; mount the thing under test on a scratch route; boot against placeholder config so no secrets are needed; capture at several widths; keep the artifacts out of the merge |
| `test-on-gh` | some buckets can't run on the agent's machine (credentials, real services, browsers); dispatch to CI on the branch and block for the result; scope the dispatch to the branch diff; separate cheap-and-always from expensive-and-on-demand; a green local run says nothing about an undispatched bucket |
| `log-review` | a window since the last run; two outputs — a qualitative readout and health triage; dedupe into tracked issues instead of re-reporting; interactive vs unattended modes; care with PII when quoting |
| `readonly-probe` | ground the investigation in real deployed data rather than guesswork; enforce read-only at the transport (read-only transaction, replica, or scoped credential), never by convention; name the environment explicitly; commit the output so the reasoning is reviewable |
| `renumber-migration` | sequential numbers collide across in-flight branches; detect the fork; adopt the other branches' files so the sequence stays contiguous; renumber yours on top; re-parent any snapshot/checksum to the schema it actually lands on; never renumber a migration that has already run anywhere |

### Not imported

`weigh`, `synthesize`, `roundtable` (multi-model workflow) and `autopilot` (unattended backlog grooming) are fully stack-agnostic, so the stub treatment would have nothing to strip — they are all-or-nothing imports, and this sync leaves them out as a self-contained subsystem orthogonal to the PR loop. `update-docs`, `update-tests` and `fix-ci` are dropped from the import set. `watch-precommit` is folded into gates; `bootstrap-workflow-dispatch` is too narrow.

### Non-skill changes

1. **`.claude/hooks/session-start.sh`** — add the `gh` proxy shim (~35 lines, stack-independent, fixes `gh run watch` stalling behind the egress proxy). Dep-install stays a stub.
2. **`CLAUDE.md`** — port six principles that are stack-independent:
   - "When analysis keeps failing to explain a real bug, widen the frame — don't just deepen it"
   - "Comments describe the code's lasting contract, not the change that produced it"
   - "Dev artifacts go under gitignored `tmp/`, not as new `.gitignore` entries"
   - "Plans must include a `## DRY notes` section"
   - "Rename auto-generated remote/web branches early"
   - the "Plan mode & questions in web sessions" section, incl. the plan-file lifecycle
   Plus: rewrite the skills list, and replace the `prep-merge`-as-canonical-gates-caller wording with `finalize`.
3. **`.gitignore`** — add `tmp/`.
4. **`README.md`** — rewrite the skills table and the bootstrap checklist.
5. **`.claude/rules/`** — adopt the path-scoped auto-load mechanism with a `README.md` explaining it and no rule files (every upstream rule is Playgram-specific). The mechanism is what's reusable.

## Non-goals

- No `.claude/gh-repo.json` — upstream needs it to hardcode `playgramai/playgramapp`; a boilerplate should read `git remote`.
- No attempt to keep future syncs automatic. This is a one-time catch-up; a `sync-upstream` skill would be speculative.
- `scripts/gates.sh` and `session-start.sh`'s dep-install stay stubs.

## DRY notes

The imported skills cross-reference each other by `@.claude/skills/<name>/SKILL.md` path rather than restating steps — that is upstream's existing discipline and it is preserved, not re-derived. The de-playgramming edits are mechanical substitutions applied consistently across files; there is no shared abstraction to extract from them, and inventing a "gates command" indirection layer would be worse than the direct `./scripts/gates.sh` reference every skill already needs to name.

`draft-pr` and `finalize` both resolve the PR base and both touch the squash proposal — but they delegate to `/check-merge` and `/squash-message` respectively rather than duplicating, so the overlap is already factored upstream.

## Risks

- **Volume.** ~23 new files, several long. The PR will be large and hard to review line-by-line; it is a vendoring operation, and the review question is "is this the right set, correctly de-playgrammed" rather than "is each line right".
- **Untested cross-references.** Imported skills reference each other; a missed rename (e.g. a lingering `/prep-merge` link, or a Tier A skill delegating to a Tier B skill that wasn't imported) breaks a chain silently. Mitigated by a final grep for `prep-merge`, `pnpm `, `playgram`, and every skill name not in the imported set.
- **Stubs that read as working skills.** A stub whose description doesn't announce itself will get invoked and then half-followed against a project it was never hydrated for — worse than its absence. The banner and the description prefix are what prevent this, so they are not decoration; `scripts/gates.sh` exits `1` for the same reason, and the stubs should fail as loudly.
- **Character shift.** The boilerplate currently advertises "five project-agnostic skills". It becomes 20 — 13 working, 7 stubs. That is a deliberate change in what this template is.

## Implementation context

Durable notes for any session resuming this work (including after a context compaction).

**Upstream source.** Cloned at `/tmp/claude-0/-home-user-agent-project-boilerplate/d917fd19-3d24-54e7-9583-b0cd0ac9d7f6/scratchpad/up`, deepened to `--shallow-since=2026-05-01`. Upstream HEAD `6c1adca`; this repo's extraction point is `2280857` (2026-05-25 12:28 +03:00). If the clone is gone, re-create it — the GitHub REST API is scope-gated to this repo, but **git transport with `$GH_TOKEN` is not**:

```bash
git -c credential.helper='!f(){ echo "username=x-access-token"; echo "password=$GH_TOKEN"; };f' \
  clone https://github.com/Playgramai/playgramapp.git up
```

(`gh api` against `Playgramai/*` returns 403 in this session; `gh` against this repo works. `add_repo` refuses cross-owner adds.)

**Source paths.** Skills at `<up>/.claude/skills/<name>/SKILL.md`; hook at `<up>/.claude/hooks/session-start.sh`; upstream `CLAUDE.md` at `<up>/CLAUDE.md`.

**Substitutions applied to every imported file.**

| Upstream | Boilerplate |
|---|---|
| `pnpm precommit` | `./scripts/gates.sh` |
| `pnpm format:fix` | `./scripts/gates.sh` (no doc-only lane; drop the swap) |
| `pnpm test` | `./scripts/gates.sh` |
| `pnpm gh:export` | `python3 scripts/export-github-issue.py` |
| `Playgramai/playgramapp`, `.claude/gh-repo.json` | resolve from `git remote` |
| `epic/<slug>`, `staging`, `production` base lanes | generic `baseRefName` resolution only |
| `docs/DECISIONS_SUMMARY.md`, `docs/decisions/*` | "the project's decision docs" |
| Railway · Drizzle · Weaviate · Mantine · Supabase · Vitest · Playwright · LiteLLM · Bunny · Stripe | dropped, not genericized |
| `/test-on-gh` dispatch steps in `finalize` | dropped (step 6 integration/E2E reasoning) |

**Skill cross-reference closure** (verified against upstream; every arrow must resolve after import, or the chain breaks silently):

- `implement` → `draft-pr`, `dry`, `finalize`, `from-branch`, `plan`, `tighten-docs`
- `from-branch` → `check-merge`, `finalize`, `implement`, `plan`, `sync-branch`, ~~`test-on-gh`~~
- `plan` → `finalize`, `from-branch`, `implement`, `issue`, `tighten-docs`
- `draft-pr` → `branch-rename`, `finalize`, `implement`, `qa-checklist`, `squash-message`, ~~`test-on-gh`~~
- `squash-message` → `check-merge`, `draft-pr`, `finalize`, `tighten-docs`, ~~`hotfix`~~, ~~`release`~~
- `qa-checklist` → `draft-pr`, `finalize`, `issue`, ~~`test-on-gh`~~
- `branch-rename` → `draft-pr`; `tighten-docs` → `squash-message`; `dry` → none

Struck-through targets become **stubs**, so those references stay valid but must be reworded to point at a stub ("if you have hydrated `/test-on-gh`…") rather than assuming a working skill.

**Already verified identical to upstream:** `dry`, `explore` — no action needed.

## Execution order

1. `docs/plans/` lifecycle flip; `.gitignore` `tmp/`.
2. `.claude/rules/README.md`; `session-start.sh` gh shim.
3. Tier A skills, in dependency order: `branch-rename` → `squash-message` → `qa-checklist` → `check-merge` → `sync-branch` → `watch-ci` → `draft-pr` → `finalize` → `plan` → `implement`; then update `from-branch`, `issue`; delete `prep-merge`.
4. Tier B skills: `tighten-docs`, `propose-issue`, `override-gh`.
5. Tier C stubs, all seven.
6. `CLAUDE.md`, `README.md` — including a short section on the stub contract, so a project bootstrapping from this template knows which skills still need hydrating.
7. Cross-reference grep sweep.
8. `./scripts/gates.sh` is a stub that exits 1 by design — it cannot gate this PR. Note that explicitly in the PR body rather than pretending it ran.
