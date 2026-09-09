# `/spinoff` — re-center the steps on the foundation, not the agent loop

A revision of the skill landed on this branch by
[PR #46](https://github.com/vzakharov/agent-project-boilerplate/pull/46), still
draft and still open, so it lands on the **same branch and the same PR**. Nothing
here is new work against [#43](https://github.com/vzakharov/agent-project-boilerplate/issues/43);
it finishes what that issue asked for in the steps that did not deliver it.

## The divergence

A spinoff takes the caller's **whole foundation** — how code there is organized —
and leaves the product behind. The agent loop is one component of that
foundation, not its spine. "Another repo like this one" means the layer
boundaries, the lint discipline, the build and deploy shape; the loop is what
makes those maintainable, not what is being copied.

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
| Step 4.2 | **`main` gets one commit: the agent infrastructure.** Nothing project-specific | The build config, the lint config and the CI workflows are neither of those — they have no home in the seed |
| Step 4's closure argument | Closure makes "infrastructure-versus-project the only clean cut" | An argument about the *skill graph* is used to settle where the *stack* lands, and silently re-collapses three buckets into two |
| Step 2, buckets 1–2 | Bucket 1 takes `scripts/` wholesale; bucket 2 separately names "the real `vet.sh`" | `vet.sh` is in both buckets, which is the seam the stack falls through |

Two further gaps, independent of the naming:

- **Bucket 2 is enumerated as config files**, and gated on *"travels when the
  stacks match"* with no account of what happens when they don't. Architecture
  that is a *convention* rather than a file has nowhere to go, and neither does a
  target that wants this repo's shape in another language.
- **"The product never travels" is absolute**, with no hatch for carrying a piece
  across as a starting template on request.

## The change

### 1. Name the thing that travels

Introduce **the foundation** in the intro, and use it wherever a downstream
sentence currently says "the agent infrastructure" and means more than that. The
foundation is the *triage's output*: what leaves the caller. Where each part of it
**lands** is a separate question, settled by § 4 on a different principle.

### 2. Step 2 — the criterion is about intent, not files

**Put stack scaffolding first.** It is the reason for the spinoff. Agent
infrastructure travels unconditionally and so needs less prose, not more.

**Replace the enumeration with a criterion.** A list of config filenames goes
stale against every stack the skill has not seen, and the boilerplate has no
stack of its own to privilege:

> Does this path encode **how code here is organized**, or **what this particular
> product is**? Organization travels. Identity does not.

**Then: does the target share this stack?** The answer changes the *form* the
organization travels in, and it is a real fork rather than an edge case — a
spinoff can legitimately be *"this repo, but in Python"*, where nothing
file-shaped can be copied at all:

- **Stacks match** → organization travels **as files**, rewritten for the target.
- **Stacks differ** → organization travels **as stated intent**, recorded in the
  target's plan: *"the caller separates layers thus, and forbids these import
  directions; establish the equivalent here."* The constraint travels; its
  expression does not.

This is what "foundation" has to mean for the skill to be honest. A layer
boundary is an architectural decision; an import-boundary lint rule is one
stack's way of writing it down. Under a matched stack you copy the writing-down;
under a mismatched one you carry the decision and re-express it. **Step 1 asks
for the target's stack** alongside `<owner/name>` and public-or-private when the
invocation did not say, because the whole of bucket 2 turns on it.

**Everything below is phrased stack-agnostically**, naming the *role* a path
plays, with ecosystems only as parenthetical examples. A rule written in one
ecosystem's nouns is unusable from the others — the defect this revision was
itself caught committing. The cases the criterion does not settle alone:

- **The directory skeleton and its import boundaries.** Under a matched stack the
  skeleton travels *empty* and the rule enforcing its direction travels *intact* —
  a layer boundary is architecture whether or not a single feature exists yet.
  Under a mismatched stack both become intent. This is the case the current
  enumeration misses most completely, since none of it is a config file.
- **Module-resolution aliases** are part of the boundary system, not decoration on
  it (wherever the stack declares them — a compiler or bundler path map, a
  workspace member list, a module path prefix).
- **The app shell and entry points** travel as a *reduction*: the routing and
  layout mechanism, not the pages inside it.
- **Design tokens** travel as a system; the brand values inside them are the
  operator's call; product copy never travels.
- **Deploy config travels as a rewrite, and is a footgun.** The mechanism (the
  publish workflow, the build output path) travels; the domain, the hostname
  file, and environment secrets never do. A copied domain declaration silently
  aims the new deployment at the caller's address.
- **The dependency *declaration* travels as a rewrite; the *resolved lockfile* is
  regenerated, not copied.** Every stack has both — a declared set with
  human-chosen constraints, and a machine-resolved pin of the whole graph. The
  declared set changes when product-only dependencies drop, so a copied resolution
  describes a graph that no longer exists. **Carry the deliberate constraints and
  regenerate the resolution**: bounds, overrides, replacements and patches are
  decisions someone made, and they are the part a regenerate loses silently.

**Fix the double-count.** `scripts/` does not travel wholesale: `vet.sh` is stack
scaffolding and travels as a rewrite, and the rest of `scripts/` is agent
infrastructure. `CLAUDE.md` and `README.md` already travel as rewrites; `vet.sh`
joins that list, which is where it belonged.

**The product hatch.** State the exception where the bucket is stated: a product
piece travels when the operator asks for it, under two constraints — it lands on
the **session branch, never on `main`**, and it is stripped of caller-specific
content (real copy, real routes, real data). Honored when named in the
invocation, **not asked on every run**: "unless requested otherwise" is the
language of an exception you invoke, not a prompt you answer.

### 3. Step 3 — no fork: the watermark always points at the root

**Delete the sibling-versus-chain fork.** The new repo's watermark points at the
**root boilerplate**, with `lastSyncedSha` taken from the caller's own
`lastSyncedSha` — never at the caller, and never the root's HEAD. This is a
simplification of the step, not an inversion of its recommendation: there is no
question to surface.

Two reasons, and the second is the decisive one:

- **Chains compose.** A sibling of a sibling of a sibling would make a sync walk
  the whole ancestry to reach the root, and every link multiplies the triage. A
  chained sync is a thing worth considering later; it is not worth paying for on
  every repo now.
- **A spun-off repo need not share the caller's stack at all** (§ 2). Pointing at
  a parent whose scaffolding you deliberately did not take buys nothing and costs
  the walk.

The known cost is accepted rather than argued away: improvements the caller makes
to its *own* adaptations never reach the new repo. **The stance, stated in the
skill in one line: once you've raised your kids, it's their own life to grow.**
The new repo inherits the caller's foundation as a starting state and then
diverges on its own.

**Record the lineage even though nothing reads it yet.** The watermark gains an
ordered `lineage` array holding the **whole ancestry, root first** — the repo
actually synced from leads, and each later entry is one hop further from it. Each
entry names an ancestor and its HEAD **at the moment the next link was created**:

```json
"lineage": [
  { "repo": "<owner>/<root>",   "atSha": "<root HEAD when the caller was born>" },
  { "repo": "<owner>/<caller>", "atSha": "<caller HEAD at this spinoff>" }
]
```

`/spinoff` **copies the caller's `lineage` and appends the caller**, so a
sibling-of-a-sibling carries every hop in birth order.

**`lineage[0]` names the same repo as `repo`, and that is not duplication —
the two SHAs are different facts.** `lastSyncedSha` is where the repo has synced
*to*, and it advances on every sync; `lineage[0].atSha` is where the repo started
*from*, and it never moves. Recording the birth point is the whole reason the
field earns its place: the first sync overwrites the only other trace of it.

**A gap means nobody wrote it down, not that no ancestor exists.** Watermarks
written by hand from `ADOPTING.md` have no `lineage`, so a spinoff from such a
caller can honestly record only `[{ caller, HEAD }]` — the caller's own birth
point is unrecoverable, and inventing one from `lastSyncedSha` would state a
falsehood. Absent stays valid, and `/spinoff` never fabricates a missing entry.
(Teaching `ADOPTING.md` to record a birth point would close the gap for future
adopters; it is out of scope here and worth an issue.)

The field is provenance, **not a second sync source** — the watermark's own note
that *"a repo with two sources would make this an array"* is about `repo`, and
conflating the two would make `/sync-agent-infra` start walking the chain, which
is exactly what this step declines to do. Writing it now is cheap and the
information is unrecoverable later: which repo a tree came from, at which commit,
is not something a future chained-sync feature could derive.

Surviving from the current step, reframed now that there is no fork:

- **`lastSyncedSha` is the caller's own `lastSyncedSha`, not the root's HEAD.**
  The files come from a tree synced to exactly that point, so that is the honest
  mark; the root's HEAD would claim the target already carries commits nobody
  ported. This stops being conditional and becomes the rule.
- **The target's `adopted` list derives from the caller's, restricted to paths
  that actually travelled — and the caller's list may spell paths that no longer
  exist, so verify each against the caller's tree before writing it.**
  [#40](https://github.com/vzakharov/agent-project-boilerplate/issues/40) is the
  live case: a list still naming a since-renamed path silently drops every future
  commit under the new one from its candidate sets, and copying it forward
  propagates the blind spot.

The target's sync skill is named after the **root**, which is also what the
caller's is named after — so it travels as a copy rather than a rename, and its
stub markers are cleared by the watermark written beside it.

### 4. Step 4 — split the seed by reviewedness, not by category

**`main` carries only what a session needs to run `/handle` in the new repo. Everything else is built in PR #1, as ordinary reviewed work.**

The principle is not *which bucket a path is in* but **whether it arrives already
reviewed**. Step 2 already sorts every travelling path into a **copy** or a
**rewrite**, and that is exactly the line needed:

- **Copies → `main`.** Reviewed where they came from, travelling unchanged:
  `.claude/skills/**`, the `.claude/rules/` that survived the triage, `scripts/`
  other than `vet.sh`, the editor config. This is precisely the `/handle` closure
  — `check-skill-catalog.sh`'s assertion 1 fails on a dangling `@`-reference, so
  satisfying it *is* "enough to run the loop".
- **Rewrites → PR #1.** New work written for a repo nobody has looked at yet:
  `CLAUDE.md`, `README.md`, `vet.sh`, the dependency declaration, the deploy
  config, the app shell reduction, the layer skeleton. Putting these on `main`
  lands the least-reviewed content through the one path that has no review.

So `main` is the caller's tree **reduced to what the boilerplate itself would
ship** — the loop, plus stubs where the caller had hydration — and PR #1 is the
hydration. That makes a spinoff structurally identical to an adoption, which is
the argument that it is right: the new repo passes through the same state every
adopter does and reaches its stack by the same reviewed path. Under a mismatched
stack (§ 2) it is also the *only* possible shape, since nothing stack-shaped can
be copied at all.

Consequences to write into the step:

- **The watermark is the one rewrite that lands on `main`, because an automated
  check couples it to a copy.** `check-skill-catalog.sh`'s assertion 4 requires a
  skill's stub markers to agree with its hydration state, and the sync skill's
  hydration *is* its watermark — so the skill file and its JSON must land
  together or `main` fails its own gate. An exception stated by a check, not by
  taste.
- **A stub the caller had hydrated is re-stubbed on `main` and re-hydrated in PR
  #1.** A hydrated `/release` encodes the *caller's* deploy setup, so it is a
  rewrite by the § 2 criterion even though it sits in `.claude/`. Per-target
  editability decides its home, not the directory. Under a mismatched stack this
  is unconditional — a deploy lane for another language is not a starting point.
- **`main`'s `vet.sh` must exit non-zero**, per the adopter contract its own
  header states and CLAUDE.md § "Vetting" repeats. `main` has no stack yet, so the
  honest script refuses to certify, and PR #1 wires in the real checks. **The gate
  is cheap and exact: assert `main`'s `vet.sh` exits non-zero.** An exit-0
  `vet.sh` on `main` is the false green the boilerplate exists to prevent, sitting
  unchallenged until PR #1 lands.
- **Do not weaken the caller's `vet.sh` to make the seed pass.** The step creates
  that pressure and yielding to it reproduces exactly the failure the boilerplate
  warns about. The reduction on `main` is a *refusal to certify*, not a narrowed
  set of checks that quietly passes.
- **Substep 3 stops saying "gets the project."** The target has no project yet.
  The branch carries the rewrites, the plan for the new product
  (`docs/plans/<slug>.paused.md`, the state `/handle`'s plan lane resumes from) —
  including, under a mismatched stack, the architectural intent § 2 records
  instead of files — and any product piece the operator asked to carry.
- **Retarget the closure paragraph.** It currently settles
  infrastructure-versus-project; it now justifies what goes on `main`
  specifically: closure over `/handle` is the floor, and the reason the floor
  cannot be carved smaller.

**Rejected:** putting the whole foundation on `main`, or splitting `main` by
provenance. Both land the stack unreviewed in the one place nothing reviews it,
and the stack is the half needing per-target adaptation.

## Open questions

**None.** All five are settled and folded in above: `main`'s contents (§ 4), the
stack-agnostic phrasing and the mismatched-stack mode (§ 2), the watermark and
its lineage (§ 3), the vet gate (§ 4), and the lineage entry shape (§ 3).

*Rejected along the way, in one line each:* putting the whole foundation on
`main`, or splitting `main` by provenance — both land the stack unreviewed. A
chained watermark — chains compose, and every link multiplies the triage.
Nearest-first lineage ordering, and a date beside each SHA — root-first puts the
repo actually synced from at the head and makes the write a plain append, and
`git log` in the ancestor already has the date.

## DRY notes

- **The seed split reuses a distinction the skill already draws.** § 4 does not
  invent a rule for what lands on `main`: it reads Step 2's existing
  copy-versus-rewrite sort, which was already there for `CLAUDE.md` and
  `README.md`. One concept doing two jobs, rather than a second concept to keep
  in agreement with the first.
- **`lineage`'s contract goes in `@.claude/skills/sync-agent-infra/SKILL.md`
  § "The watermark", which already owns the file field-by-field.** `/spinoff`
  writes the field and cites that section; it does not restate the shape. The one
  sentence `/spinoff` owns is the operation — prepend the caller to the caller's
  own array — because that is about spinning off, not about the file.
- **`lineage` is deliberately not folded into the existing multi-source note.**
  That note is about `repo` becoming an array for a repo that syncs from two
  places; `lineage` is provenance nothing syncs from. Merging them would invite
  exactly the chain-walking § 3 declines. Both live in the same section, stated
  as distinct.
- **`lineage[0].repo` restating `repo` is the one repetition here, and it is two
  facts rather than one.** `lastSyncedSha` moves with every sync; `atSha` is
  frozen at birth. The contract says so in the sentence that introduces the
  array, so a reader who spots the repeat finds the reason at the same place
  — which is the alternative to dropping the entry and losing the birth point.
- **This revision removes a duplication rather than adding one.** `vet.sh` is
  currently stated in two triage buckets; § 2 gives it one home and folds it into
  the same rewrites-not-copies list.
- **`main`'s vet gate cites the contract rather than restating it.**
  `scripts/vet.sh`'s header and CLAUDE.md § "Vetting" already own "an adopting
  project's vet exits non-zero until its real checks are wired in"; § 4 applies
  that rule to a new caller instead of writing a spinoff-specific one.
- **The criterion replaces an enumeration, which is why it does not duplicate
  `docs/catalog.md`.** The catalog carries per-file dispositions for *this* tree;
  the skill's premise is a caller that has no catalog. A criterion plus the cases
  it does not settle is the only form that survives a stack the skill has never
  seen — and the mismatched-stack mode makes a file list impossible in principle,
  not merely brittle.
- **`ADOPTING.md § Template fork` is deliberately not touched.** There the caller
  genuinely *is* the boilerplate: the loop is the whole payload, there is no stack
  to triage, and its step 2 prunes by catalog group — which works only because a
  catalog exists. § 4's "a spinoff passes through the same state an adopter does"
  is a claim about the *target's* history, not a shared procedure to extract.
- **Not extracted, on purpose: a shared "what travels" list between `/spinoff`
  and `ADOPTING.md`.** The two run against different inputs — one against a tree
  that has the catalog, one against a tree that by construction does not. The
  shared artifact would have to *be* the catalog, the one file guaranteed absent
  from a `/spinoff` caller.
- **No helper, type or script is added.** The triage is prose judgment, which is
  the skill's own stated reason for being a skill rather than a script.

## Scope of the change

| File | Change |
| --- | --- |
| `.claude/skills/spinoff/SKILL.md` | intro gains "the foundation"; end state and Steps 1–4 revised per § 1–4 |
| `.claude/skills/sync-agent-infra/SKILL.md` | § "The watermark" documents the optional `lineage` array, and that nothing syncs from it |
| `.claude/skills/sync-agent-infra/upstream.json` | ships `"lineage": []` — this repo is the root, and the empty array is how the shape is visible |
| `docs/catalog.md` | the `upstream.json` row's description gains the lineage |
| `docs/plans/43-spinoff-foundation.draft.do-not-implement.md` | this plan; flipped through its lifecycle as work proceeds |
| `docs/remove-before-merging/` | refresh the squash proposal — the branch's story changes materially |

**Scope grew with § 3**: adding a watermark field reaches the skill that owns the
watermark contract, the shipped instance of it, and the catalog row describing
that instance. Checked and still untouched: `CLAUDE.md`, `README.md`,
`ADOPTING.md`, `docs/catalog.md`'s `/spinoff` row and G0 intro, the skill
frontmatter, and every other skill.

## Verification

- `bash scripts/check-skill-catalog.sh` — exits 0; no dangling `@`-reference, one
  catalog row per skill, stub markers unchanged.
- `bash scripts/vet.sh` — the repo's own run, covering the squash proposal via
  `check-squash-message.sh`.
- `jq . .claude/skills/sync-agent-infra/upstream.json` — parses, and the new field
  matches the shape § "The watermark" documents.
- **Trace the three-generation example by hand** — root, an adopter, a spinoff of
  that spinoff — and confirm each `lineage` reads root-first in birth order, that
  `lineage[0].atSha` never equals a `lastSyncedSha` by construction, and that a
  caller with no `lineage` yields a one-entry array rather than a fabricated root.
- **Read Step 2 against a concrete tree** — `vzakharov/vovazakharov.com`, the case
  #43 cites — and confirm the criterion decides every path, including the domain
  declaration, the publish workflow, and the layer boundaries.
- **Then read it again against the same tree with the target's stack changed** —
  the *"this repo, but in Python"* case — and confirm every bucket-2 path has a
  stated destination as intent, with nothing silently copied.
- **Sort that tree into copies and rewrites** and confirm the copies plus the
  watermark pair satisfy `check-skill-catalog.sh` — that `main` is bootable for
  `/handle`, and that assertions 1 and 4 both hold there.
- **Grep the revised skill for ecosystem-specific nouns.** Rules name roles;
  filenames and tool names appear only inside parenthetical examples.
- **Confirm no sentence downstream of the intro still says "the agent
  infrastructure" where it means the foundation.**

## `/finalize` note

The plan tree is swept at squash, so both this file and the completed plan beside
it are deleted in the last commit before `gh pr ready` — nothing here reaches the
trunk.
