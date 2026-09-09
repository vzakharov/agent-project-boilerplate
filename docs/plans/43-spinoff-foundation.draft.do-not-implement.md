> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# `/spinoff` — re-center the steps on the foundation, not the agent loop

A revision of the skill landed on this branch by
[PR #46](https://github.com/vzakharov/agent-project-boilerplate/pull/46), still
draft and still open, so it lands on the **same branch and the same PR**. Nothing
here is new work against [#43](https://github.com/vzakharov/agent-project-boilerplate/issues/43);
it finishes what that issue asked for in the steps that did not deliver it.

## The divergence

A spinoff takes the caller's **whole foundation** — how code there is organized —
and leaves the product behind. The agent loop is one component of that
foundation, not its spine. "Another repo like this one" means the lint rules, the
build config, the directory skeleton and its import boundaries, the deploy
mechanism; the loop is what makes those maintainable, not what is being copied.

**The skill's intro already says this.** It reads: *"The new repo wants to be a
sibling of that — its stack, its adaptations, its real `vet.sh` — rather than of
the boilerplate."* And Step 2's triage is genuinely three-way, with stack
scaffolding as its own travelling bucket.

**The steps below it do not deliver it**, because there is no *name* for the
thing that travels. Every downstream sentence reaches for "the agent
infrastructure" — the only name on offer — and each time it does, the stack falls
out:

| Where | What it says | What falls out |
| --- | --- | --- |
| End state | `main` carries one commit of **agent infrastructure**; `check-skill-catalog.sh` passes there | The stack is not part of the success criterion at all |
| Step 4.2 | **`main` gets one commit: the agent infrastructure.** Nothing project-specific | `package.json`, `tsconfig`, the lint config, `.github/workflows/` are neither of those — they have no home in the seed |
| Step 4's closure argument | Closure makes "infrastructure-versus-project the only clean cut" | An argument about the *skill graph* is used to settle where the *stack* lands, and silently re-collapses three buckets into two |
| Step 2, buckets 1–2 | Bucket 1 takes `scripts/` wholesale; bucket 2 separately names "the real `vet.sh`" | `vet.sh` is in both buckets, which is the seam the stack falls through |

Two further gaps, independent of the naming:

- **Bucket 2 is enumerated as config files** — "build config, lint config, the
  real `vet.sh`, CI workflows, the test and generated-asset tooling". Architecture
  that is a *convention* rather than a file is absent: the directory skeleton and
  the import boundaries that enforce it, module-resolution aliases, the app shell,
  design tokens, the deploy target, and the dependency-declaration call.
- **"The product never travels" is absolute**, with no hatch for carrying a piece
  across as a starting template on request.

**Checked and found already correct, so untouched:** `docs/catalog.md`'s G0 row
and intro, `CLAUDE.md`'s § "Working with skills" line, `README.md`'s G0
group-table line, and the skill's own frontmatter. All four describe the skill as
"triage what travels" / "seed a new sibling repo" — direction-neutral, and true
under either reading. The narrow framing is confined to the skill body.

## The change

### 1. Name the thing that travels

Introduce **the foundation** — the union of the two travelling buckets — in the
intro, and use it wherever a downstream sentence currently says "the agent
infrastructure" and means more than that. The foundation is the *triage's output*:
what leaves the caller. Where each part of it **lands** is a separate question,
settled by § 4 on a different principle.

### 2. Step 2 — re-order, and give bucket 2 a criterion

**Put stack scaffolding first.** It is the reason for the spinoff. Agent
infrastructure travels unconditionally and so needs less prose, not more.

**Replace the enumeration with a criterion**, because a list of config filenames
goes stale against every stack the skill has not seen:

> Does this file say **how code here is organized**, or **what this particular
> product is**? Organization travels. Identity does not.

**Everything below is written stack-agnostically**, naming the *role* a file
plays and giving examples across ecosystems in parentheses. The boilerplate has
no stack, and a rule phrased in one ecosystem's nouns is unusable from the other
ecosystems it was meant to serve — the defect this revision was itself caught
committing. Then name only the cases the criterion does not settle on its own:

- **The directory skeleton and its import boundaries.** The skeleton travels
  *empty*; the rule that enforces its direction travels *intact* — a layer
  boundary is architecture whether or not a single feature exists yet. This is the
  case the current enumeration misses most completely, since none of it is a
  config file: it is a convention, expressed partly as empty directories and
  partly as whatever the stack uses to enforce direction (an import-boundary lint
  rule, a module visibility declaration, a build-graph constraint).
- **Module-resolution aliases** travel: they are part of the boundary system, not
  decoration on it. (Wherever the stack declares them — a compiler or bundler
  path map, a workspace member list, a module path prefix.)
- **The app shell and entry points** travel as a *reduction* — the routing and
  layout mechanism, not the pages inside it. The genuinely hard call, and the one
  worth stating rather than leaving to taste.
- **Design tokens** travel as a system; the brand values inside them are the
  operator's call; product copy never travels.
- **Deploy config travels as a rewrite, and is a footgun.** The mechanism (the
  publish workflow, the build output path) travels; the domain, the hostname file,
  and environment secrets never do. A copied domain declaration silently aims the
  new deployment at the caller's address.
- **The dependency *declaration* travels as a rewrite; the *resolved lockfile* is
  regenerated, not copied.** Every stack has both — a declared set with
  human-chosen constraints, and a machine-resolved pin of the whole graph. The
  declared set changes when product-only dependencies drop, so a copied resolution
  describes a graph that no longer exists. **Carry forward the deliberate
  constraints and regenerate the resolution**: version bounds, overrides,
  replacements and patches are decisions someone made, and they are the part a
  regenerate loses silently.

**Fix the double-count.** `scripts/` does not travel wholesale: `vet.sh` is stack
scaffolding and travels as a rewrite, and the rest of `scripts/` is agent
infrastructure. `CLAUDE.md` and `README.md` already travel as rewrites; `vet.sh`
joins that list, which is where it belonged.

**The product hatch.** State the exception where the bucket is stated: a product
piece travels when the operator asks for it, under two constraints — it lands on
the **session branch, never on `main`**, and it is stripped of caller-specific
content (real copy, real routes, real data). Honored when named in the
invocation, **not asked on every run**: "unless requested otherwise" is the
language of an exception you invoke, not a prompt you answer, and the skill
already spends one question on public-or-private.

### 3. Step 3 — invert the fork's presentation

Present **chain first, as the recommended answer.** The premise of a spinoff is
inheriting the caller's foundation, and *sibling* severs exactly that: under it
the caller's real `vet.sh`, its lint config and its layer boundaries are
unreachable by every future sync and get re-derived each time.

Keep *sibling* available, and add the redirect it implies: an operator who wants
the loop but **not** this stack is probably describing a template fork off the
boilerplate rather than a spinoff, and the skill should say so.

**The skill carries a worked example**, because the fork is the one place a
caller has to reason about three repos at once and the abstract statement does
not land. Root `R` (this boilerplate), caller `C` (an adopter, whose watermark
points at `R`), new repo `N`:

- **Sibling** — `N` points at `R`. `N` and `C` become siblings. `N`'s syncs pull
  loop changes from `R` directly, and never see anything `C` invented itself: `C`
  improves its lint config, `N` never hears about it.
- **Chain** — `N` points at `C`. `N`'s syncs pull everything that landed at `C`,
  including `R`'s changes that `C` already absorbed *and* `C`'s own stack work. A
  fix made at `R` reaches `N` only after `C` syncs it — one hop later, and never
  at all if `C` is never synced again.

State the trade in that form: **sibling trades the caller's adaptations for
first-hop access to the root; chain trades a hop for the adaptations.** A
watermark pointing at both is not offered — `/sync-agent-infra`'s watermark holds
one `repo`, so it would be a change to *that* contract, and it doubles the triage
work on every sync.

The two SHA mechanics are correct and load-bearing — which `lastSyncedSha` is
honest under each answer, and verifying an inherited `adopted` list against the
parent's tree. They stay as written, including the [#40](https://github.com/vzakharov/agent-project-boilerplate/issues/40)
citation.

### 4. Step 4 — split the seed by reviewedness, not by category

**`main` carries only what a session needs to run `/handle` in the new repo. Everything else is built in PR #1, as ordinary reviewed work.**

The principle is not *which bucket a file is in* but **whether it arrives already
reviewed**. Step 2 already sorts every travelling path into a **copy** or a
**rewrite**, and that distinction is exactly the one needed:

- **Copies → `main`.** They were reviewed where they came from and travel
  unchanged: `.claude/skills/**`, `.claude/rules/` that survived the triage,
  `scripts/` other than `vet.sh`, the editor config. This is precisely the
  `/handle` closure — `check-skill-catalog.sh`'s assertion 1 fails on a dangling
  `@`-reference, so satisfying it *is* "enough to run the loop".
- **Rewrites → PR #1.** A rewrite is new work written for a repo nobody has
  looked at yet: `CLAUDE.md`, `README.md`, `vet.sh`, the dependency declaration,
  the deploy config, the app shell reduction, the layer skeleton. Putting these on
  `main` would land the least-reviewed content in the repo through the one path
  that has no review.

So `main` is the caller's tree **reduced to what the boilerplate itself would
ship** — the loop, plus stubs where the caller had hydration — and PR #1 is the
hydration. That makes a spinoff structurally identical to an adoption, which is
the argument that it is right: the new repo passes through the same state every
adopter does, and reaches its stack by the same reviewed path.

Consequences to write into the step:

- **A stub the caller had hydrated is re-stubbed on `main` and re-hydrated in PR
  #1.** A hydrated `/release` encodes the *caller's* deploy setup, so it is a
  rewrite by the § 2 criterion, not a copy — even though it sits in `.claude/`.
  Category does not decide this; per-target editability does.
- **`main`'s `vet.sh` must exit non-zero**, per the adopter contract its own
  header states and CLAUDE.md § "Vetting" repeats. `main` has no stack yet, so the
  honest script is one that refuses to certify — and PR #1 wires in the real
  checks ported from the caller. **The gate is therefore cheap and exact: assert
  `main`'s `vet.sh` exits non-zero.** An exit-0 `vet.sh` sitting on `main` is the
  false green the boilerplate exists to prevent, and it would sit there
  unchallenged until PR #1 lands.
- **Do not weaken the caller's `vet.sh` to make the seed pass.** Naming this is
  the point: the step creates the pressure, and yielding to it reproduces exactly
  the failure the boilerplate warns about. The reduction on `main` is a *refusal
  to certify*, not a narrowed set of checks that quietly passes.
- **Substep 3 stops saying "gets the project."** The target has no project yet.
  The branch carries the rewrites, the plan for the new product
  (`docs/plans/<slug>.paused.md`, the state `/handle`'s plan lane resumes from),
  and any product piece the operator asked to carry.
- **Retarget the closure paragraph.** It currently settles
  infrastructure-versus-project. It now justifies what goes on `main`
  specifically: closure over `/handle` is the floor, and the reason the floor
  cannot be carved smaller.

**Rejected:** putting the whole foundation on `main` as one commit, or splitting
`main` into two commits by provenance. Both land the stack unreviewed in the one
place nothing reviews it, and the stack is the half that needs per-target
adaptation — a copied deploy target aimed at the caller's domain is the worked
example of why that matters.

## Open questions

**Q1 (`main`'s contents), Q2 (dependency declarations) and Q4 (the vet gate) are
settled** and folded into § 2 and § 4 above. One remains.

**3. Invert the watermark recommendation to chain-by-default?** § 3 above is
written with (a) in force, including the worked example, so silence resolves it.

- **(a) Yes — chain recommended, sibling the deliberate exception with its
  redirect to a template fork. — recommended.** The premise of a spinoff is
  inheriting the caller's foundation, and sibling severs it.
- (b) Keep it undefaulted as today, improving only the framing, the cost
  statement and the worked example.

## DRY notes

- **The seed split reuses a distinction the skill already draws.** § 4 does not
  invent a rule for what lands on `main`: it reads Step 2's existing
  copy-versus-rewrite sort, which was already there for `CLAUDE.md` and
  `README.md`. One concept doing two jobs, rather than a second concept that has
  to be kept in agreement with the first.
- **This revision removes a duplication rather than adding one.** `vet.sh` is
  currently stated in two triage buckets; § 2 gives it one home (stack
  scaffolding, travelling as a rewrite) and folds it into that same
  rewrites-not-copies list.
- **`main`'s vet gate cites the contract rather than restating it.**
  `scripts/vet.sh`'s own header and CLAUDE.md § "Vetting" already own "an adopting
  project's vet exits non-zero until its real checks are wired in"; § 4 applies
  that existing rule to a new caller instead of writing a spinoff-specific one.
- **The criterion replaces an enumeration, which is why it does not duplicate
  `docs/catalog.md`.** The catalog carries per-file dispositions for *this* tree;
  the skill's whole premise is a caller that has no catalog, so there is nothing
  to look the answer up in. A criterion plus the cases it does not settle is the
  only form that survives contact with a stack the skill has never seen.
- **`ADOPTING.md § Template fork` is deliberately not touched and does not
  duplicate this.** There the caller genuinely *is* the boilerplate: the agent
  infrastructure is the whole payload, there is no stack to triage, and its step 2
  prunes by catalog group — which works only because a catalog exists. Same words,
  different operation. § 4's "a spinoff passes through the same state an adopter
  does" is a claim about the *target's* history, not a shared procedure to extract.
- **Not extracted, on purpose: a shared "what travels" list between `/spinoff`
  and `ADOPTING.md`.** Forcing one is net-negative because the two run against
  different inputs — one against a tree that has the catalog, one against a tree
  that by construction does not. The shared artifact would have to *be* the
  catalog, which is the one file guaranteed absent from a `/spinoff` caller.
- **Step 3's home stays where it is.** `@.claude/skills/sync-agent-infra/SKILL.md`
  § "The watermark" remains the owner of the watermark file's field-by-field
  contract; § 3 changes only which answer is recommended and cites rather than
  restates.
- **New prose is confined to one file.** No helper, type or script is added: the
  triage is prose judgment, and there is nothing in it a script could execute —
  which is the skill's own stated reason for being a skill.

## Scope of the change

| File | Change |
| --- | --- |
| `.claude/skills/spinoff/SKILL.md` | intro gains "the foundation"; end state, Steps 2, 3, 4 revised per § 1–4 |
| `docs/plans/43-spinoff-foundation.draft.do-not-implement.md` | this plan; flipped through its lifecycle as work proceeds |
| `docs/remove-before-merging/` | refresh the squash proposal — the branch's story changes materially |

Untouched, having been checked: `docs/catalog.md`, `CLAUDE.md`, `README.md`,
`ADOPTING.md`, the skill's frontmatter, and every other skill.

## Verification

- `bash scripts/check-skill-catalog.sh` — exits 0; no dangling `@`-reference from
  the revised skill, its one catalog row intact, stub markers unchanged.
- `bash scripts/vet.sh` — the repo's own run, which covers the squash proposal's
  format via `check-squash-message.sh`.
- **Read Step 2 against a concrete tree** — `vzakharov/vovazakharov.com`, the
  worked case #43 cites — and confirm the criterion plus its named cases decide
  every path in it, including the domain declaration, the publish workflow, and
  the layer boundaries.
- **Sort that same tree into copies and rewrites** and confirm the copies alone
  satisfy `check-skill-catalog.sh` assertion 1 — that `main` really is bootable
  for `/handle` without any rewrite.
- **Grep the revised skill for stack-specific nouns.** No ecosystem's filenames
  or tool names outside a parenthetical example; the rules themselves name roles.
- **Confirm no sentence downstream of the intro still says "the agent
  infrastructure" where it means the foundation.** That substitution is the whole
  divergence.

## `/finalize` note

The plan tree is swept at squash, so both this file and the completed plan beside
it are deleted in the last commit before `gh pr ready` — nothing here reaches the
trunk.
