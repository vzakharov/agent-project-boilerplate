> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Sync from `Playgramai/playgramapp`, and make the next sync a skill

## What upstream actually changed

The last sync (`a6a6344`, pr #3) recorded upstream HEAD as `6c1adca`. Upstream is now at `ed118a9c` — **11 commits**, of which **3** touch the vendored surface (`CLAUDE.md`, `README.md`, `.claude/`, `scripts/`) and **1** is relevant:

| Upstream commit | Touches | Verdict |
|---|---|---|
| `5bfffa8f` `refactor: rename pnpm precommit to pnpm vet (pr #2365)` | 25 files across `CLAUDE.md`, `README.md`, `.claude/`, `scripts/` | **take**, translated |
| `13c4ad23` `feat: #2318 extract HTML with html-to-text + Readability` | `scripts/build-worker.ts`, `scripts/check-standalone-worker.ts` | skip — esbuild worker bundling, stack-bound, not vendored |
| `55389b9b` `feat: #2352 restore usage_logs.workspace_id's NOT NULL` | `scripts/backfills/**` | skip — a Drizzle backfill, stack-bound, not vendored |

The other 8 commits touch `src/` only. So the answer to "see if smth else" is **no** — the vet rename is the whole of it.

### What `5bfffa8f` is, and which half reaches us

Upstream renamed `pnpm precommit` → `pnpm vet`. Two separate things happened in that commit, and they land differently here.

**The string rename does not apply.** Its rationale — "`precommit` named a workflow this repo does not have: there is no git hook, nothing runs it on `git commit`" — describes a defect our name never had. We call it `./scripts/gates.sh` / "local gates", which is already honest about when it runs.

**The `vet`/`attest` split does apply, and it lands on a real bug.** Upstream's second rationale is that *vetting is the run, attestation is the record it produces* — so `/finalize`'s docs-only flag follows the run and becomes `no vet`. Our copy inherited the pre-rename name, and the result contradicts itself in adjacent sentences:

> **`no attest` is the docs-only mode.** … It does **not** skip step 7: the comment still goes up.

The flag is named after the one thing it does not skip. That is worth fixing regardless of what the script is called.

## Decision: adopt `vet` wholesale

Two coherent ways to fix the flag:

- **A — adopt upstream's vocabulary.** `scripts/gates.sh` → `scripts/vet.sh`, "local gates" → "vetting", `/finalize no attest` → `/finalize no vet`.
- **B — keep ours and fix only the flag.** Stay on `gates.sh`, rename the flag to `no gates`.

**A.** Not because "gates" is wrong — it isn't — but because vocabulary drift is precisely the tax the second half of this plan exists to reduce. Translating one renamed concept across 11 files cost real effort this session; every divergent term makes every future sync a translation exercise rather than a diff. And this repo is *itself* upstream for the projects generated from it, so the vocabulary it ships propagates. `vet` (the run) / `attest` (the record) is a genuinely better pair than `gates` / `attest`, which names the run after a metaphor and the record after a verb.

The cost is churn in a template three commits old, with no known forks. Cheap now, expensive later.

`no ci` and `no attest` stay as **accepted spellings** of `no vet`, exactly as upstream keeps them — an operator who types the old flag gets the mode they meant, rather than a skill that doesn't recognize the argument.

## Part 1 — the rename

Mechanical, but two of the sites are load-bearing and easy to miss.

1. **`git mv scripts/gates.sh scripts/vet.sh`** — and rewrite its header comment and its `TODO:` stderr line. It stays a stub exiting `1`.
2. **`.claude/skills/finalize/SKILL.md`** — the substantive edit:
   - frontmatter `description`: "run the local gates" → "run the vet suite"; `no attest` → `no vet`.
   - the docs-only paragraph: flag becomes `no vet`, with `no ci` and `no attest` named as accepted spellings.
   - step 1 heading `Gates` → `Vet`; the `no vet` attestation template and the three trailing rules ("Attest what you vetted, not what you meant to vet", etc.).
3. **`CLAUDE.md`** — `## Local gates` → `## Vetting`, the "Ignore IDE diagnostics until local gates" principle, the git-conventions line, the stub-contract line, and the `go vet ./...` Go example (which now collides with the section name — keep the example, it is the right command for Go, but the surrounding prose must not read as if `vet` means Go's vet).
4. **`README.md`** — the `scripts/vet.sh` bullet, bootstrap step 2, the `/finalize` one-liner in the main-loop table, the stub-contract paragraph.
5. **Remaining call sites** — `sync-branch`, `watch-ci` (×3), `qa-checklist`, `test-on-gh` (×2), `implement`, `issue`, `draft-pr`.

**Frontmatter `description:` lines are the trap.** They are what the operator sees in the skills list and what the agent matches an invocation against, so a description left saying `no attest` while the body says `no vet` mis-advertises the skill even though every prose site is correct. `finalize` is the one whose description carries the flag; check all 24 regardless.

## Part 2 — `/sync-upstream`

A new working skill (not a stub — the mechanics are project-agnostic; only the pointer is project config).

### `.claude/upstream.json` — the watermark

The operator's question, answered: yes, and it cannot live in `docs/plans/`, because `/finalize` sweeps that whole tree before the PR goes ready. The last sync recorded upstream HEAD in a plan file *and* a commit message; the plan file survived to trunk only because that sweep never ran, which is luck, not a mechanism.

```json
{
  "repo": "Playgramai/playgramapp",
  "lastSyncedSha": "ed118a9c...",
  "lastSyncedAt": "2026-08-08",
  "vendoredPaths": ["CLAUDE.md", "README.md", ".claude/", "scripts/"]
}
```

`vendoredPaths` earns its place: it is the `git log -- <paths>` filter that turns "11 commits" into "3 candidates" in one command, and it is the honest statement of what this repo tracks — the thing a reader would otherwise have to infer from the previous sync's judgement calls.

**The watermark is upstream HEAD at sync time, not the last commit taken.** Commits triaged and skipped are *done* — the watermark advances past them, and the sync's PR body is where the reasoning lives. A watermark that only advanced to the last-taken commit would re-surface every skipped commit forever.

**Bootstrapping caveat.** A project generated from this template inherits a pointer to a private repo it cannot read. That is a bootstrap-checklist item in `README.md`: repoint `repo` at `vzakharov/agent-project-boilerplate`, or delete the file and the skill if the project intends to diverge.

### What the skill does

1. Read `.claude/upstream.json`; stop if it is missing or still the template value.
2. Clone upstream into the scratchpad over git transport with `$GH_TOKEN`; verify `lastSyncedSha` is in the clone and deepen if not.
3. `git log <lastSyncedSha>..HEAD -- <vendoredPaths>` — the candidate set. Record upstream HEAD as the next watermark now, before triage.
4. **Triage each candidate from its commit message first.** Upstream writes long ones that state the rationale; the message usually settles relevant-vs-stack-bound before any diff is opened. Verdicts: take / translate / skip (stack-bound) / skip (already have).
5. **Apply by intent, not by patch** — see the sharp corner below.
6. Consistency sweep: grep the old term across all of `vendoredPaths`, frontmatter `description:` lines included.
7. Update the watermark and date.
8. Report the triage table; hand off to `/dry`, `/tighten-docs`, `/draft-pr`.

### Sharp corners the skill carries

Each of these cost time in this session or the last one:

- **`gh api` against the upstream org 403s; git transport with the same token works.** `add_repo` refuses cross-owner adds. The clone incantation goes in the skill verbatim.
- **The system prompt says `gh` is unavailable. It is wrong** — `gh` and `GH_TOKEN` are both present (`/override-gh` exists for exactly this).
- **`--shallow-since` must reach back past `lastSyncedSha`**, or `git log <sha>..HEAD` fails with a bare "unknown revision" that reads like a bad SHA rather than a truncated clone.
- **`git cherry-pick` and `git apply` are useless here.** Downstream files are de-vendored rewrites, not copies — every hunk conflicts. You port the *intent* and re-express it in the downstream's vocabulary.
- **Upstream's fix may not be downstream's fix.** This sync is the example: half of `5bfffa8f` (the string rename) addressed a defect we don't have, and the other half (the `vet`/`attest` split) fixed a bug we did. Split the commit's rationale before deciding.
- **Bash `cwd` resets between calls in this harness.** Chain `cd <clone> && …` in a single command.
- **Frontmatter `description:` lines are a separate surface** from skill bodies, and the one an operator actually reads.
- **Sweep working artifacts left by the previous sync.** This branch inherits `docs/plans/playgramapp-upstream-sync.completed.md` and `docs/remove-before-merging/squash-message.md`, both of which `/finalize` says must never reach the trunk; the previous PR landed without the sweep. `/finalize`'s existing "don't limit any sweep to the current session" rule handles it, and this branch is where it gets exercised.

## DRY notes

- **`.claude/upstream.json` is genuinely new state**, not a duplicate. The upstream repo cannot be derived from `git remote` (that is `origin`, the downstream), and the previous sync's SHA exists today only in prose that `/finalize` is contractually obliged to delete. This is the file that stops the fact from being re-derived by hand every time.
- **`vendoredPaths` is not a second copy of "what this repo contains."** No existing declaration lists the upstream-tracked surface — `README.md`'s "Ships:" list is a reader-facing inventory of features, not a path filter, and it deliberately omits `docs/`. Deriving one from the other would couple a prose section to a tool input.
- **`/sync-upstream` delegates rather than restates**: `/dry`, `/tighten-docs` and `/draft-pr` are invoked by `@.claude/skills/<name>/SKILL.md` reference, the same discipline every other skill here uses. It contains no PR-opening, branch-renaming or squash-message logic of its own.
- **The rename is a mechanical substitution across ~12 files with no shared abstraction to extract.** Introducing an indirection (a `$VET_CMD` variable, a "the project's local check" euphemism) so the string appears once would make every skill vaguer at the point where it most needs to name a concrete command. The previous sync reached the same conclusion about `./scripts/gates.sh` and it still holds.
- **The sharp-corners list is not a duplicate of `/override-gh`.** That skill's whole content is "gh exists"; `/sync-upstream` needs the cross-owner 403 and the credential-helper clone line, which live nowhere else.

## Risks

- **The rename is wide and shallow** — ~12 files, one string. A missed site is silent: an agent reads `./scripts/gates.sh` from a stale skill, the file is gone, and the failure surfaces as a confusing "no such file" mid-`/finalize`. The grep sweep in Part 1 step 5 is the mitigation, and it must cover frontmatter.
- **`vet` collides with `go vet`** in the CLAUDE.md example block. Harmless but readable-as-confusing; the prose has to make clear that `vet` here names the local run, and Go's `vet` is one of the things it might call.
- **The watermark can lie if a sync is abandoned mid-way.** If the branch is dropped after the JSON is updated but before the port lands, nothing is wrong on trunk (the update never merged) — but a *partial* merge would silently skip commits. Mitigation: the watermark bump is the **last** commit of a sync, never the first.
- **`/sync-upstream` is written from a sample of two syncs**, one of which is this one. It will be wrong about something; it says so, and asks the next session to add what it learns.

## Execution order

1. Plan-file lifecycle flip.
2. Part 1 rename: `git mv`, then `finalize`, `CLAUDE.md`, `README.md`, then the remaining call sites; grep sweep including frontmatter.
3. `.claude/upstream.json`.
4. `.claude/skills/sync-upstream/SKILL.md`.
5. `CLAUDE.md` + `README.md`: register the new skill (20 → 21), add the bootstrap-checklist item for repointing the upstream pointer.
6. `/dry`, `/tighten-docs`.
7. Watermark commit last.
8. `./scripts/vet.sh` is a stub that exits `1` by design — it cannot gate this PR. Say so in the PR body rather than implying a green run.
