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
  the import boundaries that enforce it (FSD layers being the worked case), path
  aliases, the app shell, design tokens, the deploy target, and the
  manifest-versus-lockfile call.
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
intro, and use it in the end state and Step 4. This is the whole fix for three of
the four rows above: those sentences say "agent infrastructure" because that was
the only name available.

End state becomes: the target exists; its `main` carries one commit of **the
foundation**; `check-skill-catalog.sh` passes there and `scripts/vet.sh` has been
run with its result interpreted (§ 4); and the operator holds a copyable command.

### 2. Step 2 — re-order, and give bucket 2 a criterion

**Put stack scaffolding first.** It is the reason for the spinoff. Agent
infrastructure travels unconditionally and so needs less prose, not more.

**Replace the enumeration with a criterion**, because a list of config filenames
goes stale against every stack the skill has not seen:

> Does this file say **how code here is organized**, or **what this particular
> product is**? Organization travels. Identity does not.

Then name only the cases the criterion does not settle on its own:

- **The directory skeleton and its import boundaries.** The skeleton travels
  *empty*; the rule that enforces its direction travels *intact* — an FSD layer
  boundary is architecture whether or not a single feature exists yet. This is the
  case the current enumeration misses most completely, since none of it is a
  config file.
- **Path aliases** (`tsconfig` `paths`, bundler resolve config) travel: they are
  part of the boundary system, not decoration on it.
- **The app shell and entry points** travel as a *reduction* — the routing and
  layout mechanism, not the pages inside it. The genuinely hard call, and the one
  worth stating rather than leaving to taste.
- **Design tokens** travel as a system; the brand values inside them are the
  operator's call; product copy never travels.
- **Deploy config travels as a rewrite, and is a footgun.** The mechanism (the
  pages workflow, the build output path) travels; the domain, `CNAME`, and
  environment secrets never do. A copied `CNAME` silently aims the new site at the
  caller's domain.
- **The manifest travels as a rewrite; the lockfile is regenerated, not copied.**
  The dependency set changes when product-only deps drop, so a copied lock pins
  resolutions for a manifest that no longer matches. **Carry forward any explicit
  pin, override or resolution block** — that is where deliberate version decisions
  live, and regenerating loses them silently.

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

The two SHA mechanics are correct and load-bearing — which `lastSyncedSha` is
honest under each answer, and verifying an inherited `adopted` list against the
parent's tree. They stay as written, including the [#40](https://github.com/vzakharov/agent-project-boilerplate/issues/40)
citation.

### 4. Step 4 — give the foundation a home, and gate it

- **Substep 2 becomes "`main` gets one commit: the foundation."** Both travelling
  buckets, nothing product-specific.
- **Add the stack-side gate.** After `check-skill-catalog.sh`, run
  `bash scripts/vet.sh` in the target and **report the result with its
  interpretation**:
  - **Red for a reason you can name** (no dependencies installed, no source tree
    yet) is the expected honest outcome, and becomes the **first work item of the
    paused plan**.
  - **Green is the suspicious outcome** and must be explained. A vet that passes
    over a tree with no source is precisely the false green `scripts/vet.sh`'s own
    header exists to prevent — `/finalize` step 1 passes and its attestation
    records a run that checked nothing.
  - **Do not weaken the target's `vet.sh` to make the seed green.** Naming this is
    the point: the step creates the pressure, and yielding to it reproduces the
    exact failure the boilerplate warns about. Note too that
    `check-skill-catalog.sh` skips assertions 2–3 downstream (no `docs/catalog.md`
    there, by design), so absent this gate the only automated check in a
    freshly-seeded repo covers the skill graph and nothing else.
- **Substep 3 stops saying "gets the project."** The target has no project yet.
  It carries the plan for the new product — `docs/plans/<slug>.paused.md`, the
  state `/handle`'s plan lane resumes from — plus any product piece the operator
  asked to carry.
- **Retarget the closure paragraph.** It currently settles
  infrastructure-versus-project; it should settle foundation-versus-product. The
  closure argument keeps doing its own work (it is why you cannot carve a subset of
  the skills), and the re-centering adds a **second, independent** reason for the
  same two-commit split: `main` must be able to run the target's own vet, which it
  cannot if the stack is on a branch. Two independent justifications, not a
  replacement for one.

## Open questions

Each carries a recommendation, and the plan above is written **with the
recommended option in force** — so it is implementable as written and silence
resolves it. Answer tersely (e.g. "1a, 2b, 3-default").

**1. Does `main`'s foundation commit stay one commit, or split in two** —
boilerplate-derived, then caller-derived?

- **(a) One commit. — recommended.** Under chain-by-default both halves come from
  the same source, and the watermark already records provenance.
- (b) Two commits, making the boundary readable in the target's `git log`. Worth
  something under *sibling*, where only the first half is covered by
  `lastSyncedSha`. Coupled to Q3: if you keep the fork undefaulted, (b) gets
  stronger.

**2. The lockfile — regenerate or copy?**

- **(a) Regenerate, carrying forward explicit pins and overrides. —
  recommended.** The manifest changes, so a copied lock is either stale or gets
  rewritten on first install; the pins are the part that encodes real decisions.
- (b) Copy, then prune. Preserves the caller's *tested* resolutions, which matters
  if it pinned around a known-bad version — but that case is what carrying the pin
  block covers.

**3. Invert the watermark recommendation to chain-by-default?**

- **(a) Yes — chain recommended, sibling the deliberate exception with its
  redirect. — recommended.**
- (b) Keep it undefaulted as today, improving only the framing and the cost
  statement.

**4. Does the target's `vet.sh` result gate the hand-over, or only get reported?**

- **(a) Reported with interpretation; red-for-a-known-reason becomes the paused
  plan's first item. — recommended.** Green needs installed dependencies and a
  shell that lints — phase-2 work, and it needs the environment setup script that
  has no API behind it.
- (b) Gate it: no hand-over until vet is green in the target. Stronger guarantee,
  but it pulls most of phase 2 into the seed.

## DRY notes

- **This revision removes a duplication rather than adding one.** `vet.sh` is
  currently stated in two triage buckets; § 2 gives it one home (stack
  scaffolding, travelling as a rewrite) and folds it into the existing
  rewrites-not-copies list beside `CLAUDE.md` and `README.md` — an existing
  mechanism reused, not a new one.
- **The criterion replaces an enumeration, which is why it does not duplicate
  `docs/catalog.md`.** The catalog carries per-file dispositions for *this* tree;
  the skill's whole premise is a caller that has no catalog, so there is nothing
  to look the answer up in. A criterion plus the cases it does not settle is the
  only form that survives contact with a stack the skill has never seen.
- **`ADOPTING.md § Template fork` is deliberately not touched and does not
  duplicate this.** There the caller genuinely *is* the boilerplate: the agent
  infrastructure is the whole payload, there is no stack to triage, and its step 2
  prunes by catalog group — which works only because a catalog exists. Same words,
  different operation.
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
  every path in it, including the `CNAME`, the pages workflow, and the layer
  boundaries.
- **Confirm no sentence downstream of the intro still says "the agent
  infrastructure" where it means the foundation.** That substitution is the whole
  divergence; grep for it.

## `/finalize` note

The plan tree is swept at squash, so both this file and the completed plan beside
it are deleted in the last commit before `gh pr ready` — nothing here reaches the
trunk.
