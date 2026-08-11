> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Downstream entry point: adopting from this boilerplate, and re-syncing later

## The problem

This repo is reachable today by exactly one route: GitHub's **"Use this template"**, which produces a whole-repo fork. An agent in an **already-existing** repo, told "take in what you need from that boilerplate," has nothing to read. It will `cp -r .claude/ scripts/` wholesale and get: seven stubs that read as working skills, `/sync-upstream` pointed at a private repo it cannot clone, a `README.md` describing someone else's template, and two stale `docs/plans/*.completed.md` working artifacts. Then it has no way to pull the next month of changes forward.

Three deliverables, in dependency order:

1. **An adoption entry point** — a document an outside agent reads *before* it has copied anything, carrying per-group adoption criteria it can mostly evaluate against its own repo without asking a human.
2. **A downstream re-sync skill** — `/sync-boilerplate`, the mirror of `/sync-upstream`, which the adopting repo copies into itself. The procedural core the two directions share is extracted once and referenced by both.
3. **A line a human pastes** into another repo's agent session to start the whole thing.

## Current state that constrains the design

- `/sync-upstream` today **denies** the downstream direction exists: "It runs in one direction only… It is not a way for a project generated from this template to pull the template's later changes back in… Don't invoke it for that." `README.md` ¶96–101 says the same ("divorced repo, not a dependency"). Both statements become wrong the moment `/sync-boilerplate` lands, so reconciling them is part of this work, not follow-up.
- This repo is **public** (`vzakharov/agent-project-boilerplate`, template, default branch `main`). So the downstream clone needs no credential helper — but it does need full history to resolve `lastSyncedSha..HEAD`. That is a genuine parameter of the shared clone step, not a copy of it.
- The skills are **densely cross-referenced** — 15 of 26 `@`-reference at least one sibling. `scripts/vet.sh` is referenced by six skills and `/plan` by four. A subset copy that ignores the closure leaves dangling `@.claude/skills/x/SKILL.md` pointers, which fail silently: the agent follows the surviving prose and skips the step it can't load.

## Doc DRY: which file owns what

Three documents, three non-overlapping jobs. Every fact lives in exactly one of them, and the other two link.

| File | Owns | Audience |
|---|---|---|
| `README.md` | What this repo is and why; the two acquisition entry points, one line each; links out. Stays short. | A human evaluating the repo. |
| `ADOPTING.md` | The **acquisition procedure**, for both modes — template fork and subset-adoption into an existing repo. | An agent, once, over the network. |
| `docs/catalog.md` | The **inventory**: one row per skill/script/file, with criteria. | Both, plus `/sync-boilerplate` on every run. |

This resolves four existing duplications rather than adding to them:

- README's **"Ships:"** bullets and its two **"What's included"** tables are per-item descriptions → they become group headings plus a catalog pointer. The catalog's columns are a superset of what those tables carried.
- README's **"Bootstrap checklist after creating your repo"** is the template-fork half of the acquisition procedure, and it shares four of its steps with subset-adoption (reconcile `CLAUDE.md`, implement `vet.sh`, hydrate-or-delete the stubs, initialize the sync watermark). Keeping it in README means maintaining that overlap in two files, so `ADOPTING.md` grows a **§ Template fork** and README keeps only the `gh repo create --template` line plus a pointer at it.
- README's **"Not inherited: `/sync-upstream`"** section is a per-item adoption criterion → the catalog's "Never adopt" row, with README keeping one sentence of framing.
- README's **"treat an unhydrated stub as unavailable"** paragraph is the G6 adoption criterion → the catalog, cited from `ADOPTING.md`'s hydrate-or-delete step.

`ADOPTING.md` does not restate what a skill does — it cites catalog rows. The catalog does not restate procedure — it names groups and conditions.

## Deliverable 1 — `ADOPTING.md` (root) + `docs/catalog.md`

**`ADOPTING.md`** is the acquisition procedure, at the repo root so it is visible in GitHub's file list and fetchable at a stable raw URL. It is read once, over the network, and is **never copied downstream**. It opens by branching on mode: **§ Template fork** (short — the fork already gave you every file, so the work is pruning and hydration) and **§ Adopt into an existing repo** (the steps below). The two sections share the tail, so the shared steps are written once and the mode sections converge on them.

Its steps, for the subset-adoption mode:

1. **Clone this repo somewhere temporary** — `git clone --depth 1` into the session scratchpad or `tmp/`. Public, so no token. (Shallow is right here and wrong for `/sync-boilerplate`; see DRY notes.)
2. **Profile the target repo, don't interrogate the human.** Most adoption criteria are decidable by inspection, and the doc says so as commands: `git remote -v` (GitHub?), `gh auth status` (is `gh` usable?), `python3 -V` / `command -v jq` (script prerequisites), `ls .github/workflows` (CI?), `gh issue list --limit 1` (are issues used to track work?), `gh repo view --json squashMergeAllowed` (does the squash-message discipline apply?). Only what the repo cannot answer gets asked: whether sessions run on Claude Code web/remote, and whether the project has a deploy path, a visual surface, or numbered migrations.
3. **Pick groups from the catalog**, resolve each group's dependency closure, copy.
4. **Reconcile `CLAUDE.md` rather than overwrite it.** The adopting repo already has conventions. Take the sections, merge into theirs, and keep their stack-specific content — the boilerplate's `CLAUDE.md` is a seed, and downstream it is a donor.
5. **Point `scripts/vet.sh` at commands that already exist** in the target repo (its lint/test/typecheck), instead of copying the stub that exits 1. An adopting repo, unlike a fresh one, already has the answer.
6. **Install `/sync-boilerplate` and write its watermark** — `lastSyncedSha` = the SHA just cloned, `adopted` = what was taken, `declined` = what was refused *and why*.
7. **Verify**: run `scripts/check-skill-catalog.sh` to prove no `@`-reference dangles, confirm the copied skills appear in the session's skill list, and confirm no unhydrated stub was taken silently.

**`docs/catalog.md`** is the single per-item inventory: one row per skill/script/file, with columns *what it does* · *group* · *requires* · *pulls in* · *skip if*. It is the file a human or agent reads to answer "how much of this do I need," and the file `/sync-boilerplate` consults when a **new** skill appears upstream. It is **read from the clone on every sync, never vendored downstream** — so it structurally cannot go stale in an adopter's tree.

### The groups (the "criterion per group" the task asks for)

Groups **partition** the inventory; the *requires* column carries the orthogonal conditions. Adoption is a group-level decision with per-row escapes.

| Group | Contents | Adopt when |
|---|---|---|
| **G0 — The sync path** | `/sync-boilerplate` + its watermark | Always, unless you want a one-time snapshot and no future updates. |
| **G1 — Prose & principles** | `CLAUDE.md` (key principles, docstrings, derived types, doc-sync), `.claude/rules/` mechanism, `/dry`, `/tighten-docs`, `/explore` | Always. Zero external dependencies, no stack assumptions, no GitHub. |
| **G2 — The PR loop** | `/plan`, `/implement`, `/pr`, `/finalize`, `/branch-rename`, `/squash-message`, `/qa-checklist`, `/check-merge`, `/sync-branch`, `/from-branch`, `scripts/check-merge.sh`, `scripts/pr-body.py`, `scripts/vet.sh` | A change is a branch → PR → squash-merge, on GitHub, with `gh` + `$GH_TOKEN` reachable. Needs `python3` ≥3.9 and `jq`. |
| **G3 — Issue & backlog** | `/issue`, `/propose-issue`, `/audit-github-backlog`, `scripts/export-github-issue.py` | G2 **and** work is actually tracked as GitHub issues. |
| **G4 — Remote-session plumbing** | `.claude/hooks/session-start.sh`, `.claude/settings.json`, `/override-gh` | Sessions run on Claude Code web/remote — the `gh` shim exists for that egress proxy, and is inert locally. |
| **G5 — CI & landing** | `/watch-ci`, `scripts/ci-watch-tick.sh`, `scripts/lib/watch-tick-common.sh`, `/test-on-gh` (stub) | CI runs on GitHub Actions, reachable via `gh`. |
| **G6 — Stack stubs** | `/release`, `/hotfix` (deploy path) · `/preview` (visual surface) · `/log-review` (deployed logs) · `/readonly-probe` (production datastore) · `/renumber-migration` (sequential numbered migrations) · `/test-on-gh` (tests that can't run locally) | Per row, and only if you will hydrate it now. An unhydrated stub is worse than a missing skill — copy none of these "for later." |
| **Never adopt** | `.claude/skills/sync-upstream/` (+ `upstream.json`) · `README.md` · `ADOPTING.md` · `docs/catalog.md` · `docs/plans/*` · `docs/remove-before-merging/*` | These describe or maintain *this* repo. `/sync-upstream` points at a private repo an adopter cannot clone. |

Two closure findings the catalog must state explicitly, because they are counter-intuitive:

- **`/plan` travels with G2 even for a local-only adopter.** Its motivation is the web-session bug (G4), but `/implement`, `/finalize`, `/propose-issue` and `/audit-github-backlog` reference it. Drop it only if you also strip those references.
- **`scripts/vet.sh` is not optional within G2.** Six skills invoke it; `/finalize` stops loudly without it. It is the one G2 file an adopter should *rewrite* rather than copy.

## Deliverable 2 — `/sync-boilerplate`, and the extracted core

New skill directory `.claude/skills/sync-boilerplate/`:

- **`vendor-sync-core.md`** — the direction-agnostic procedure, moved out of `/sync-upstream` verbatim where possible: the blobless full-history clone into the scratchpad (with the `clone -c` vs `git -c` trap, the "don't reach for `--depth`" warning, and the Bash-cwd-resets note), building the candidate set from `lastSyncedSha..HEAD` plus the unfiltered pass that catches surfaces the path list doesn't name yet, triage-from-the-commit-message-first with the verdict table, apply-by-intent-not-by-patch, the frontmatter-inclusive consistency sweep, the watermark discipline (`lastSyncedSha` is source HEAD at sync time, **not** the last commit taken; bump it in the sync's *last* commit), and report-every-candidate-including-skips. The credential helper becomes a documented conditional: required for a private source, omitted for a public one.
- **`SKILL.md`** — supplies only what is direction-specific: source = this repo, watermark = `boilerplate.json`, path filter = the `adopted` list, and the four downstream-only concerns below.
- The watermark's shape is described in prose (as `/sync-upstream` does for `upstream.json`); **no template file ships**, since this repo is not downstream of itself and a stray `boilerplate.json` here would read as if it were.

```json
{
  "repo": "vzakharov/agent-project-boilerplate",
  "lastSyncedSha": "<boilerplate HEAD at the last sync>",
  "lastSyncedAt": "<YYYY-MM-DD>",
  "adopted": [".claude/skills/pr/", "scripts/check-merge.sh", "…"],
  "declined": { ".claude/skills/issue/": "we track work in Linear, not GitHub issues" }
}
```

`declined` is the downstream-only invention and the reason re-sync stays quiet: without it, every sync re-offers every skill the repo already refused. It records the *reason*, so a sync can notice when the reason stopped being true.

Downstream-only concerns in `SKILL.md`, on top of the core:

- **Two extra verdicts.** `skip (not adopted)` — the path is in `declined`, or in neither list. `skip (diverged locally)` — the adopter rewrote this file for their stack, so upstream's edit is advice at best; say what was skipped and why.
- **New skills get offered, not taken.** A commit adding a skill that is in neither `adopted` nor `declined` is a decision the sync surfaces with the catalog row's criteria attached — and whichever way it goes, the answer is written into `adopted` or `declined` so it is asked exactly once.
- **Taking a new skill re-runs the closure check**, because a newly-adopted skill can reference a sibling the repo declined.
- **The "never adopt" rows are never candidates**, even when a commit touches them.

`/sync-upstream` is then rewritten to reference the core, keeping only its own direction-specific material — plus its "downstream direction is not supported" paragraph replaced by a pointer at `/sync-boilerplate`.

## Deliverable 3 — the human-oriented line

Lands in `README.md` under a new **"Adopt into an existing repo"** section (alongside the existing template-fork path), and is repeated inside `ADOPTING.md` so it can be copied from either:

```
Adopt the agent infrastructure from https://github.com/vzakharov/agent-project-boilerplate into this repo: clone it somewhere temporary, read ADOPTING.md, and follow it.
```

Prose rather than a shell one-liner on purpose — it names the repo and the file and lets the agent choose its fetch mechanism (clone, raw fetch, MCP), which survives an environment where any one of those is blocked. The follow-up line, once installed, is just `/sync-boilerplate`.

## Deliverable 4 (supporting) — `scripts/check-skill-catalog.sh`

One small script, three assertions:

1. Every `@.claude/skills/<name>/SKILL.md` reference across `.claude/` and `CLAUDE.md` resolves to a file that exists. **This is the check that makes subset-copying safe**, and it is the one assertion that still works downstream.
2. Every `.claude/skills/*/` directory has a row in `docs/catalog.md`.
3. Every path named in a catalog row exists.

Assertions 2–3 skip cleanly when `docs/catalog.md` is absent (the downstream case), so the same script is useful in both repos. Its value here is anti-drift: without it, adding a skill to this repo silently leaves the catalog incomplete — the same failure mode `/sync-upstream` already warns about for `vendoredPaths`. `CLAUDE.md` gains a line saying to run it when adding or renaming a skill.

## Consistency sweep (part of the work, not follow-up)

- `README.md`: reduced to its owned scope per "Doc DRY" above — what/why, the two acquisition lines, links out. Inherited-skill counts change (20 → 21; 13 working → 14) wherever they survive the reduction. The bootstrap checklist moves to `ADOPTING.md` § Template fork, where its step 5 becomes "delete `/sync-upstream`, **and** initialize `/sync-boilerplate`'s watermark" — which is also the fix for the README's current claim that a template fork has no way back to the template.
- `CLAUDE.md`: `/sync-boilerplate` added to the skills index; "Not part of the inherited set" reworded so `/sync-upstream` is still the one delete-on-bootstrap file while the downstream direction now has a home; the `check-skill-catalog.sh` line.
- `/sync-upstream`: the one-direction paragraph, and its steps that now live in the core.
- Grep `vendoredPaths` and "one direction" across the repo, frontmatter `description:` lines included.

## Out of scope (noted, not done)

`docs/plans/*.completed.md` (two files) and `docs/remove-before-merging/squash-message.md` are tracked on `main`, contrary to the working-artifact conventions that say `/finalize` sweeps them. They are why the catalog needs a "never adopt" row for `docs/`. Cleaning them up is a separate change; this branch's own `/finalize` sweep will remove the `docs/plans/` tree, which incidentally takes the two stale files with it — worth confirming at finalize rather than assuming.

## DRY notes

**Genuinely shared, extracted once** — the vendored-sync procedure. It is currently one copy (`/sync-upstream`) about to become two, and the duplicate would be ~60 lines of hard-won operational detail (the `clone -c` placement trap alone cost a debugging session, per its own prose). `vendor-sync-core.md` holds it; both `SKILL.md`s reference it and contribute only source, watermark, path filter, and direction-specific verdicts. Placing the core **inside the new skill's directory** is deliberate and matches the task's framing: `/sync-upstream` is deleted on bootstrap while `/sync-boilerplate` is adopted, so the surviving file must own the shared text. Precedent for a non-`SKILL.md` support file in a skill directory: `.claude/skills/audit-github-backlog/analyst-rules.md`.

**Deliberately not shared** — the two clone commands. `ADOPTING.md` uses `git clone --depth 1` with no credentials; the core uses a blobless, no-checkout, **full-history** clone with an optional credential helper. They look similar and are not interchangeable: shallow is correct for first contact (only the working tree matters) and *breaks* re-sync (`lastSyncedSha` is unreachable, failing as a bare "unknown revision" that reads like a bad SHA). Forcing one helper would either give first-contact a clone it doesn't need or give re-sync one that cannot work. The core's warning against `--depth` is the durable record of why.

**Extracted, not duplicated** — the prose the new docs would otherwise restate from `README.md`. The three-way split in "Doc DRY" above is the mechanism: skill one-liners move to `docs/catalog.md`, the post-acquisition checklist moves to `ADOPTING.md`, and README keeps framing and links. Net effect is that this change **removes** more duplication from the repo than it introduces, rather than adding a third file that paraphrases the first two. The failure mode being designed out is per-item drift: a skill gains a flag, and today three files claim to describe it.

**Deliberately duplicated, once** — the human-oriented kickoff line appears in both `README.md` and `ADOPTING.md`. It is two sentences, it is the thing a human copies, and both files are places they will look for it; a pointer would cost more than the copy. Nothing derives from it, so it cannot drift silently.

**Deliberately not merged** — the two acquisition modes stay separate sections rather than one parameterized procedure. They share the tail (the four steps named above, written once and converged on) but their heads are genuinely different work: a fork starts with every file present and prunes, an adopting repo starts with none and selects. Collapsing them into one branchy procedure would make both harder to follow than the shared-tail form.

**Reused, not rebuilt** — the group/condition vocabulary comes from what the skills already declare (their `@`-references and the `gh`/`jq`/`python3` calls in their bodies), and `check-skill-catalog.sh` derives the closure from those same references rather than from a hand-maintained dependency list. A hand-written adjacency table would be exactly the "hand-written duplicate whose shape tracks another declaration" `CLAUDE.md` forbids.

## Verification

- `bash scripts/check-skill-catalog.sh` exits 0 on this repo, and exits non-zero when a reference is deliberately broken in a scratch copy.
- Every group in the catalog resolves to a closed set: for each group, the union of its rows' `pulls in` is contained in that group plus its stated prerequisite groups.
- `ADOPTING.md`'s profiling commands each run in this environment and produce the shape of answer the doc claims.
- Every skill directory and every `scripts/` file appears in exactly one catalog group, "Never adopt" included — no orphans.
- Grep confirms no surviving claim that the downstream direction is unsupported.
- **No per-item description survives in two of `README.md` / `ADOPTING.md` / `docs/catalog.md`.** Check by reading the three back-to-back: each skill name should appear with a description exactly once, and each acquisition step exactly once. A skill name may of course appear as a bare cross-reference.
- `README.md` after the reduction still answers, on its own, "what is this and how do I get it" — the pointers replace detail, not the through-line.
