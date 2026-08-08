> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

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

`tighten-docs`, `propose-issue`, `update-tests`, `update-docs` (generalized from `DECISIONS_SUMMARY.md` to "the project's decision docs"), `fix-ci` (generic — drops `ci-failure-inspect.sh` and the Playwright console-log fetch), and **`override-gh`**.

`override-gh` is nine lines and earns its place: this very session burned several turns concluding upstream was unreachable because the system prompt says "you do NOT have access to the `gh` CLI" while `gh` and `GH_TOKEN` were in fact present. A marker skill whose description contradicts that in the skills list is the cheapest possible fix.

### Tier C — not imported

**Project-specific:** `hotfix`, `release`, `renumber-migration` (Drizzle), `preview` (Next.js + Mantine CSS), `test-on-gh` (Vitest buckets), `log-review` (Railway), `readonly-probe` (Supabase/Weaviate), `watch-precommit` (folded into gates).

**Deferred, not rejected** — `weigh`, `synthesize`, `roundtable` (the multi-model workflow) and `autopilot` (unattended backlog grooming). All four are genuinely project-agnostic, but they're a self-contained subsystem orthogonal to the PR loop, and `autopilot` additionally needs repo labels and a scheduled routine to mean anything. Better as a follow-up than bundled into a sync PR. `bootstrap-workflow-dispatch` is skipped as too narrow.

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

- **Volume.** ~20 new files, several long. The PR will be large and hard to review line-by-line; it is a vendoring operation, and the review question is "is this the right set, correctly de-playgrammed" rather than "is each line right".
- **Untested cross-references.** Imported skills reference each other; a missed rename (e.g. a lingering `/prep-merge` or `/test-on-gh` link) breaks a chain silently. Mitigated by a final grep for `prep-merge`, `pnpm `, `playgram`, and every skill name not in the imported set.
- **Character shift.** The boilerplate currently advertises "five project-agnostic skills". It becomes ~22. That is a deliberate change in what this template is, and is the main thing worth a second opinion — see question 1.

## Execution order

1. `docs/plans/` lifecycle flip; `.gitignore` `tmp/`.
2. `.claude/rules/README.md`; `session-start.sh` gh shim.
3. Tier A skills, in dependency order: `branch-rename` → `squash-message` → `qa-checklist` → `check-merge` → `sync-branch` → `watch-ci` → `draft-pr` → `finalize` → `plan` → `implement`; then update `from-branch`, `issue`; delete `prep-merge`.
4. Tier B skills.
5. `CLAUDE.md`, `README.md`.
6. Cross-reference grep sweep.
7. `./scripts/gates.sh` is a stub that exits 1 by design — it cannot gate this PR. Note that explicitly in the PR body rather than pretending it ran.
