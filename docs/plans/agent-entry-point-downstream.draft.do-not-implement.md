> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Downstream entry point: adopting from this boilerplate, and re-syncing later

## The problem

This repo is reachable today by exactly one route: GitHub's **"Use this template"**, which produces a whole-repo fork. An agent in an **already-existing** repo, told "take in what you need from that boilerplate," has nothing to read. It will `cp -r .claude/ scripts/` wholesale and get: seven stubs that read as working skills, a `/sync-upstream` pointed at a private repo it cannot clone, a `README.md` describing someone else's template, and two stale `docs/plans/*.completed.md` working artifacts. Then it has no way to pull the next month of changes forward.

Three deliverables, in dependency order:

1. **An adoption entry point** — a document an outside agent reads *before* it has copied anything, carrying per-group adoption criteria it can mostly evaluate against its own repo without asking a human.
2. **A re-sync path that works from any repo** — `/sync-upstream` generalized so that "upstream" means whatever the repo's own watermark says, rather than this repo's private source.
3. **A line a human pastes** into another repo's agent session to start the whole thing.

## Current state that constrains the design

- `/sync-upstream` today **denies** the downstream direction exists: "It runs in one direction only… It is not a way for a project generated from this template to pull the template's later changes back in… Don't invoke it for that." `README.md` ¶96–101 says the same ("divorced repo, not a dependency"). Both become wrong under Deliverable 2, so reconciling them is part of this work, not follow-up.
- This repo is **public** (`vzakharov/agent-project-boilerplate`, template, default branch `main`); its own upstream is private. **Verified this session:** the token credential helper is a no-op against a public clone and the blobless lazy blob fetch still resolves, so one clone recipe covers both — no public/private branch in the procedure.
- The skills are **densely cross-referenced** — 15 of 26 `@`-reference at least one sibling. `scripts/vet.sh` is referenced by six skills and `/plan` by four. A subset copy that ignores the closure leaves dangling `@.claude/skills/x/SKILL.md` pointers, which fail silently: the agent follows the surviving prose and skips the step it can't load.

### What a fresh web session can actually do (measured, not assumed)

The adopting agent runs in a repo with **no `gh` shim installed** — that shim is the thing being adopted. So the procedure may only use capabilities a vanilla proxied session has. Probed this session by calling `/usr/bin/gh` directly with the proxy left in place, which reproduces that condition:

| Probe | Result |
|---|---|
| `git clone --depth 1 <public repo>`, no token, **repo outside the session's scope** | works — verified against `jqlang/jq` as well as this repo |
| `gh api repos/{owner}/{repo}/…` (REST), incl. `--jq` | works |
| `gh auth status` | **misleading failure**: "Failed to log in to github.com using token (GH_TOKEN)" alongside "Active account: true" |
| `gh repo view --json`, `gh pr list`, `gh issue list` (GraphQL) | `HTTP 403: This GraphQL query is not enabled for this session — only the pinned set of PR-review operations is served. Use REST via gh api repos/{owner}/{repo}/... instead.` |

Four consequences, each of which changes the design:

1. **Step 0 is safe.** Cloning this repo is plain unauthenticated git and is not gated on session repo scope, so the entry point cannot fail at the door. It must be `git clone`, never `gh repo clone`.
2. **`gh auth status` must never be the "is `gh` usable?" probe.** It reports failure in a session where `gh` REST works fine — an agent trusting it would conclude it has no GitHub access and abandon or downgrade the adoption for no reason. The honest probe is a REST call: `gh api repos/{owner}/{repo} --jq .visibility`.
3. **The whole profiling step is written in REST forms**, so it needs no shim, no hook, and no bypass. A GraphQL 403 during profiling is then not a blocker but a *finding* — it is the diagnostic signature of a proxied web session, i.e. positive evidence that G4 is needed. The error text names its own workaround.
4. **G4 stops being optional plumbing for anyone in a web session** — see the group table. The adopted skills use GraphQL-flavored `gh` freely (`gh pr view --json`, `gh pr list`, `gh issue list`), so without the shim they 403 on first use. An adopter would discover this only when their first `/pr` failed.

### The one place adoption can legitimately stall

Installing the hook means installing a shim that runs `gh` under `env -u HTTPS_PROXY`. A remote agent's own default guidance tells it **never to unset `HTTPS_PROXY`**, so an adopting agent may well refuse — reasonably, since from where it sits the request looks like being asked to defeat an egress control. `ADOPTING.md` must therefore:

- carry the rationale (the proxy's policy blocks long-polling and most GraphQL; `gh` talks only to GitHub hosts; the hook is checked-in, reviewable configuration owned by the repo, and leaves the proxy in force for everything else), and
- **name the conflict explicitly** rather than hoping it goes unnoticed, so the agent can see it is a known trade-off rather than a smuggled instruction, and
- state the fallback plainly: **adoption never hard-depends on the shim.** G4 can be declined, `ADOPTING.md`'s own steps are proxy-safe REST throughout, and the cost of declining is scoped and stated — the `gh`-heavy skills need their calls in REST form, and `gh run watch`-style long-polling (`/watch-ci`) does not work at all.

The last point is why the fallback is designed in rather than bolted on: an agent that refuses at this step should still finish the adoption, minus G4, and say what it skipped.

## Doc DRY: which file owns what

Three documents, three non-overlapping jobs. Every fact lives in exactly one of them, and the other two link.

| File | Owns | Audience |
|---|---|---|
| `README.md` | What this repo is and why; the two acquisition entry points, one line each; links out. Stays short. | A human evaluating the repo. |
| `ADOPTING.md` | The **acquisition procedure**, for both modes — template fork and subset-adoption into an existing repo. | An agent, once, over the network. |
| `docs/catalog.md` | The **inventory**: one row per skill/script/file, with criteria and disposition. | Both, plus `/sync-upstream` on every run. |

This resolves four existing duplications rather than adding to them:

- README's **"Ships:"** bullets and its two **"What's included"** tables are per-item descriptions → they become group headings plus a catalog pointer. The catalog's columns are a superset of what those tables carried.
- README's **"Bootstrap checklist after creating your repo"** is the template-fork half of the acquisition procedure, and it shares four of its steps with subset-adoption (reconcile `CLAUDE.md`, implement `vet.sh`, hydrate-or-delete the stubs, repoint the sync watermark). Keeping it in README means maintaining that overlap in two files, so `ADOPTING.md` grows a **§ Template fork** and README keeps only the `gh repo create --template` line plus a pointer at it.
- README's **"Not inherited: `/sync-upstream`"** section is **deleted outright**, not moved — Deliverable 2 makes the skill inherited, so the section describes a rule that no longer exists.
- README's **"treat an unhydrated stub as unavailable"** paragraph is the G6 adoption criterion → the catalog, cited from `ADOPTING.md`'s hydrate-or-delete step.

`ADOPTING.md` does not restate what a skill does — it cites catalog rows. The catalog does not restate procedure — it names groups, conditions, and dispositions.

## Deliverable 1 — `ADOPTING.md` (root) + `docs/catalog.md`

**`ADOPTING.md`** is the acquisition procedure, at the repo root so it is visible in GitHub's file list and fetchable at a stable raw URL. It is read once, over the network, and is **never copied downstream**. It opens by branching on mode: **§ Template fork** (short — the fork already gave you every file, so the work is pruning and hydration) and **§ Adopt into an existing repo** (the steps below). The two converge on a shared tail, so the four common steps are written once.

Its steps, for the subset-adoption mode:

1. **Clone this repo somewhere temporary** — `git clone --depth 1` into the session scratchpad or `tmp/`. Plain git, never `gh repo clone`: verified to work unauthenticated and out-of-scope, so it is the one step that cannot fail on session configuration. (Shallow is right here and wrong for `/sync-upstream`; see DRY notes.)
2. **Profile the target repo, don't interrogate the human — and use only proxy-safe probes.** Most adoption criteria are decidable by inspection: `git remote -v` (GitHub?), `python3 -V` / `command -v jq` (script prerequisites), `ls .github/workflows` (CI?), and for anything needing the API, the REST form `gh api repos/{owner}/{repo}/…` — `…/issues?per_page=1` for "are issues used to track work?", `… --jq .squash_merge_allowed` for "does the squash-message discipline apply?", `… --jq .visibility` as the capability probe standing in for the unreliable `gh auth status`. **No `gh <noun> <verb> --json` forms at this step**; they are GraphQL and 403 in a vanilla web session. Only what the repo cannot answer gets asked: whether sessions run on Claude Code web/remote, and whether the project has a deploy path, a visual surface, or numbered migrations.
3. **If this is a web/remote session, settle G4 before anything else is copied.** Either adopt it (`session-start.sh` + `settings.json`, then install the shim for the current session so the remaining steps and the newly-adopted skills have a working `gh`) or decline it and record the scoped cost. Doing this first is what stops an adopter finishing the whole procedure and then discovering `/pr` 403s. The rationale, the `HTTPS_PROXY` conflict and the decline path are all spelled out here — see "The one place adoption can legitimately stall" above.
4. **Pick groups from the catalog**, resolve each group's dependency closure, copy.
5. **Reconcile `CLAUDE.md` rather than overwrite it.** The adopting repo already has conventions. Take the sections, merge into theirs, keep their stack-specific content — the boilerplate's `CLAUDE.md` is a seed, and downstream it is a donor.
6. **Rewrite the two "rewrite, don't copy" files** (below): point `scripts/vet.sh` at lint/test commands the target repo already has, and write `upstream.json` for this repo rather than inheriting the one in the clone.
7. **Verify**: run `scripts/check-skill-catalog.sh` to prove no `@`-reference dangles, confirm the copied skills appear in the session's skill list, confirm no unhydrated stub was taken silently, confirm `/sync-upstream` names *this* repo's source, and — if G4 was adopted — confirm one GraphQL-flavoured call now succeeds, since that is the assertion the shim exists to make true.

**`docs/catalog.md`** is the single per-item inventory: one row per skill/script/file, with columns *what it does* · *group* · *requires* · *pulls in* · *disposition*. It is the file a human or agent reads to answer "how much of this do I need," and the file `/sync-upstream` consults when a **new** skill appears at the source. It is **read from the clone on every sync, never vendored downstream** — so it structurally cannot go stale in an adopter's tree.

### Three dispositions, not two

Adoption is not copy-or-skip. Each row carries one of:

- **adopt** — copy as-is.
- **rewrite** — copy the shape, replace the contents for this repo. Exactly two files: `scripts/vet.sh` (its stub exits 1 by design; an adopting repo already knows its own test commands) and `.claude/skills/sync-upstream/upstream.json` (the source, SHA and adopted set are per-repo by definition). Naming this disposition is what stops an adopter inheriting a watermark pointed at a repo it cannot read.
- **never** — describes or maintains the source repo, so it is meaningless downstream.

### The groups

Groups **partition** the inventory; *requires* carries the orthogonal conditions. Adoption is a group-level decision with per-row escapes.

| Group | Contents | Adopt when |
|---|---|---|
| **G0 — The sync path** | `/sync-upstream` (adopt) + `upstream.json` (**rewrite**) | Always, unless you want a one-time snapshot and no future updates. |
| **G1 — Prose & principles** | `CLAUDE.md` (key principles, docstrings, derived types, doc-sync), `.claude/rules/` mechanism, `/dry`, `/tighten-docs`, `/explore` | Always. Zero external dependencies, no stack assumptions, no GitHub. |
| **G2 — The PR loop** | `/plan`, `/implement`, `/pr`, `/finalize`, `/branch-rename`, `/squash-message`, `/qa-checklist`, `/check-merge`, `/sync-branch`, `/from-branch`, `scripts/check-merge.sh`, `scripts/pr-body.py`, `scripts/vet.sh` (**rewrite**) | A change is a branch → PR → squash-merge, on GitHub, with `gh` + `$GH_TOKEN` reachable. Needs `python3` ≥3.9 and `jq`. **In a web/remote session, needs G4** — these skills call GraphQL-flavoured `gh` and 403 without the shim. |
| **G3 — Issue & backlog** | `/issue`, `/propose-issue`, `/audit-github-backlog`, `scripts/export-github-issue.py` | G2 **and** work is actually tracked as GitHub issues. Same web-session dependency on G4. |
| **G4 — Remote-session plumbing** | `.claude/hooks/session-start.sh`, `.claude/settings.json`, `/override-gh` | Sessions run on Claude Code web/remote. Inert locally, so a local-only repo skips it — but it is a **prerequisite of G2/G3/G5**, not a nicety, for anyone running on the web. Declinable at a stated cost. |
| **G5 — CI & landing** | `/watch-ci`, `scripts/ci-watch-tick.sh`, `scripts/lib/watch-tick-common.sh`, `/test-on-gh` (stub) | CI runs on GitHub Actions, reachable via `gh`. In a web session **G4 is required, not merely recommended**: the long-polling `gh run watch` path is what the proxy blocks hardest. |
| **G6 — Stack stubs** | `/release`, `/hotfix` (deploy path) · `/preview` (visual surface) · `/log-review` (deployed logs) · `/readonly-probe` (production datastore) · `/renumber-migration` (sequential numbered migrations) · `/test-on-gh` (tests that can't run locally) | Per row, and only if you will hydrate it now. An unhydrated stub is worse than a missing skill — copy none of these "for later." |
| **Never** | `README.md` · `ADOPTING.md` · `docs/catalog.md` · `docs/plans/*` · `docs/remove-before-merging/*` | These describe or maintain *this* repo. |

Two closure findings the catalog must state explicitly, because they are counter-intuitive:

- **`/plan` travels with G2 even for a local-only adopter.** Its motivation is the web-session bug (G4), but `/implement`, `/finalize`, `/propose-issue` and `/audit-github-backlog` reference it. Drop it only if you also strip those references.
- **`scripts/vet.sh` is not optional within G2.** Six skills invoke it; `/finalize` stops loudly without it. Hence its **rewrite** disposition rather than a choice.

## Deliverable 2 — one universal `/sync-upstream`, parameterized by its watermark

**The name was already right.** "Upstream" is relative to the repo you are standing in; only the body and the JSON were parochial. So there is no second skill and no extracted core — the skill *is* the shared procedure, and everything that differs between directions is data in `upstream.json`: which repo, from which SHA, over which paths. In this repo it means "sync from the private app repo." In an adopting repo, the same file means "sync from the boilerplate."

That makes the chain — private app repo → this repo → an adopting repo → whatever adopts from *that* — one operation applied repeatedly: *pull vendored agent infrastructure forward from the repo I took it from.* Each link differs only in its watermark.

### What changes in the skill

- **The banner flips from delete to repoint.** "🧹 DELETE ON BOOTSTRAP" becomes "🔁 REPOINT ON ADOPTION," because deleting was only ever necessary to stop an adopter inheriting a watermark naming a private repo. Rewriting the JSON fixes that properly and leaves the repo with a working sync path. This is the fix for the README's current dead end, where a template fork has no route back to the template.
- **`vendoredPaths` → `adopted`.** Same field, generalized: any granularity, directory or file. This repo's value is the degenerate everything-case (`CLAUDE.md`, `README.md`, `.claude/`, `scripts/`); an adopting repo's is a real subset. Renamed because "vendored" describes one particular link's relationship, while "adopted" is true of every link.
- **`declined` is added** — a map of path → why-not. It is what keeps re-sync quiet: without it, every sync re-offers every skill the repo already refused. It records the *reason*, so a sync can notice when the reason has stopped being true.
- **Two verdicts join the existing four**, both universal rather than downstream-only: `skip (not adopted)` — the path is in `declined` or in neither list; `skip (diverged locally)` — this repo rewrote the file for its own stack, so the source's edit is advice at best.
- **New skills get offered, not taken.** A commit adding a skill in neither list is a decision the sync surfaces with the catalog row's criteria attached, and the answer is written into `adopted` or `declined` so it is asked exactly once. Taking one re-runs the closure check, since a new skill can reference a sibling this repo declined.
- **The clone becomes unconditional** — one recipe, credential helper always present, per the verification above. The existing `clone -c` placement trap, the "don't reach for `--depth`" warning, the scratchpad-not-the-repo rule (the token lands in `.git/config` in the clear) and the Bash-cwd-resets note all survive unchanged.

```json
{
  "repo": "<owner>/<repo>",
  "lastSyncedSha": "<source HEAD at the last sync>",
  "lastSyncedAt": "<YYYY-MM-DD>",
  "adopted": ["CLAUDE.md", ".claude/skills/pr/", "scripts/check-merge.sh"],
  "declined": { ".claude/skills/issue/": "we track work in Linear, not GitHub issues" }
}
```

A repo with two sources would make this an array; nothing here precludes that, and nothing here builds it.

### Two invariants the universal form makes visible

Both are hardcoded in the skill rather than left to the watermark, because they hold at every link:

- **Never sync the watermark file itself.** This trap is invisible under a two-skill design and sharp under one: `upstream.json` lives inside `.claude/`, which is inside `adopted`, so a naive sync overwrites the adopting repo's watermark with the source's — silently repointing its sync at a repo it cannot clone and resetting `lastSyncedSha` to a foreign history. The failure surfaces one sync later, as an unresolvable SHA. Exclude it unconditionally.
- **Judge the diff, not the commit message's "we".** In a chain, commits arrive that the source itself took from *its* upstream, written in a third repo's vocabulary. Read them for intent; never let "we do X here" settle whether X applies to you. The existing "apply by intent, not by patch" rule already points this way, but the chain is what makes it load-bearing.

## Deliverable 3 — the human-oriented line

Lands in `README.md` under a new **"Adopt into an existing repo"** section (alongside the existing template-fork path), and is repeated inside `ADOPTING.md` so it can be copied from either:

```
Adopt the agent infrastructure from https://github.com/vzakharov/agent-project-boilerplate into this repo: clone it somewhere temporary, read ADOPTING.md, and follow it.
```

Prose rather than a shell one-liner on purpose — it names the repo and the file and lets the agent choose its fetch mechanism (clone, raw fetch, MCP), which survives an environment where any one of those is blocked. The follow-up line, once installed, is just `/sync-upstream` — the same command this repo already uses, which is the point.

## Deliverable 4 (supporting) — `scripts/check-skill-catalog.sh`

One small script, three assertions:

1. Every `@.claude/skills/<name>/SKILL.md` reference across `.claude/` and `CLAUDE.md` resolves to a file that exists. **This is the check that makes subset-copying safe**, and it is the one assertion that still works downstream.
2. Every `.claude/skills/*/` directory has a row in `docs/catalog.md`.
3. Every path named in a catalog row exists.

Assertions 2–3 skip cleanly when `docs/catalog.md` is absent (the downstream case), so the same script is useful at every link in the chain. Its value here is anti-drift: without it, adding a skill silently leaves the catalog incomplete — the same failure mode `/sync-upstream` already warns about for its path list. `CLAUDE.md` gains a line saying to run it when adding or renaming a skill.

## Consistency sweep (part of the work, not follow-up)

- `README.md`: reduced to its owned scope per "Doc DRY" — what/why, the two acquisition lines, links out. The **"Not inherited: `/sync-upstream`"** section is deleted; the skill is now inherited and repointed. Counts become 21 inherited skills (14 working + 7 stubs) with no exclusions. Bootstrap checklist moves to `ADOPTING.md` § Template fork, its step 5 becoming "repoint `upstream.json`" instead of "delete the skill."
- `CLAUDE.md`: same deletion in **"Not part of the inherited set"**; `/sync-upstream` moves into the skills index proper, described as the universal re-sync path; the `check-skill-catalog.sh` line.
- `/sync-upstream/SKILL.md`: the banner, the one-direction paragraph, the field rename, the two invariants, the unconditional clone.
- Grep `vendoredPaths`, "one direction", "delete this skill", "divorced" across the repo — frontmatter `description:` lines included, since `/sync-upstream`'s description currently opens with "BOILERPLATE MAINTENANCE ONLY — delete this skill…".

## Out of scope (noted, not done)

**Making the `gh`-heavy skills proxy-safe.** The measured findings above mean that in a web session the adopted skills need G4's shim, because they call GraphQL-flavoured `gh` (`gh pr view --json`, `gh pr list`, `gh issue list`). Rewriting those call sites into the REST forms that work through the proxy would make G4 genuinely optional and remove the one step where an adopting agent may refuse — but it touches roughly ten skills, changes behaviour in *this* repo as much as downstream, and is judged on its own merits rather than as a rider on an adoption entry point. So this branch documents the dependency and the decline path instead of removing the dependency. `/implement` files it as an issue (via `/propose-issue`, so it dedupes) and links it from `ADOPTING.md`'s G4 section, so an adopter who hits the refusal finds the tracking thread rather than a dead end.

**Stale working artifacts on `main`.** `docs/plans/*.completed.md` (two files) and `docs/remove-before-merging/squash-message.md` are tracked on `main`, contrary to the working-artifact conventions that say `/finalize` sweeps them. They are why the catalog needs a "never" row for `docs/`. Cleaning them up is a separate change; this branch's own `/finalize` sweep will remove the `docs/plans/` tree, which incidentally takes the two stale files with it — worth confirming at finalize rather than assuming.

## DRY notes

**Not extracted — unified.** The earlier shape of this plan had a shared `vendor-sync-core.md` plus two thin skills (`/sync-upstream`, `/sync-boilerplate`). Making the skill universal is strictly DRYer: three files collapse to one, the cross-reference disappears, and the direction becomes data. It also *deletes* doctrine — the delete-on-bootstrap rule and both "not inherited" sections go away rather than getting reworded. The test it passes: after unification there is no residual per-direction fork. The two candidates both dissolved — the private/public clone split (verified to be a no-op distinction) and "diverged locally" (a verdict every link needs, not a downstream special case).

**Deliberately not shared** — the two clone recipes. `ADOPTING.md` uses `git clone --depth 1`; `/sync-upstream` uses a blobless, no-checkout, **full-history** clone. They look similar and are not interchangeable: shallow is correct for first contact (only the working tree matters) and *breaks* re-sync, where `lastSyncedSha` becomes unreachable and fails as a bare "unknown revision" that reads like a bad SHA. The skill's existing warning against `--depth` is the durable record of why, and it is one more reason `ADOPTING.md`'s clone must not be described as "the same clone, shallower."

**Extracted, not duplicated** — the prose the new docs would otherwise restate from `README.md`. The three-way split in "Doc DRY" is the mechanism: skill one-liners move to `docs/catalog.md`, the post-acquisition checklist to `ADOPTING.md`, README keeps framing and links. Net effect is that this change **removes** more duplication than it introduces rather than adding a third file paraphrasing the first two. The failure mode designed out is per-item drift: a skill gains a flag, and today three files claim to describe it.

**Deliberately duplicated, once** — the human-oriented kickoff line appears in both `README.md` and `ADOPTING.md`. Two sentences, it is the thing a human copies, and both files are where they will look; a pointer would cost more than the copy. Nothing derives from it, so it cannot drift silently.

**Deliberately not merged** — the two acquisition modes stay separate sections converging on a shared tail, rather than one parameterized procedure. Their tails are identical (the four steps named above, written once) but their heads are genuinely different work: a fork starts with every file present and prunes; an adopting repo starts with none and selects. Collapsing them into one branchy procedure would make both harder to follow.

**Reused, not rebuilt** — the group/condition vocabulary comes from what the skills already declare (their `@`-references and the `gh`/`jq`/`python3` calls in their bodies), and `check-skill-catalog.sh` derives the closure from those same references rather than from a hand-maintained dependency list. A hand-written adjacency table would be exactly the "hand-written duplicate whose shape tracks another declaration" `CLAUDE.md` forbids.

## Verification

- `bash scripts/check-skill-catalog.sh` exits 0 on this repo, and non-zero when a reference is deliberately broken in a scratch copy.
- **The universal skill is exercised in both directions before landing**: read `/sync-upstream` against this repo's own watermark (its existing job, unchanged), then against a hand-written watermark naming this repo as the source, and confirm each step is executable as written with no direction-specific gap.
- The never-sync-the-watermark invariant is checked by construction: with `.claude/` in `adopted`, confirm the procedure as written excludes `upstream.json` rather than relying on the operator noticing.
- Every group in the catalog resolves to a closed set: for each group, the union of its rows' `pulls in` is contained in that group plus its stated prerequisite groups.
- `ADOPTING.md`'s profiling commands each run in this environment and produce the shape of answer the doc claims — **and each is re-run against `/usr/bin/gh` with the proxy left in place**, since that, not the shimmed session, is the environment an adopting agent will be in. Any probe that only works shimmed is a bug in the doc.
- No step before the G4 decision uses a GraphQL-flavoured `gh` call, and `gh auth status` appears nowhere as a capability probe.
- The G4 decline path is walked end-to-end: the procedure completes with G4 refused, and reports what was skipped rather than failing.
- Every skill directory and every `scripts/` file appears in exactly one catalog group with exactly one disposition — no orphans.
- Grep confirms no surviving claim that the downstream direction is unsupported, and none that `/sync-upstream` should be deleted.
- **No per-item description survives in two of `README.md` / `ADOPTING.md` / `docs/catalog.md`.** Read the three back-to-back: each skill name appears with a description exactly once, each acquisition step exactly once. Bare cross-references don't count.
- `README.md` after the reduction still answers, on its own, "what is this and how do I get it" — the pointers replace detail, not the through-line.
