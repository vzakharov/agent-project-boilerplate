# `/spinoff` — fire a sibling repo out of an adopter

Closes [#43](https://github.com/vzakharov/agent-project-boilerplate/issues/43).

Add a hydrated `/spinoff <owner/name>` skill in **G0**. It runs **only from an
adopter**, never from this repo, and refuses when it finds itself here.
Everything is prose and shell; there is no stack to touch.

## What is missing today

The infrastructure is written entirely from the **adopter's** side, pulling:
`ADOPTING.md` is read once over the network by the repo taking it on,
`docs/catalog.md` is the inventory it selects from, and `/sync-agent-infra` keeps
that selection current. Nothing serves the **source's** side, pushing.

The case that wants it: once a real project runs on this infrastructure, the
recurring next move is *another repo like **this** one* — its stack, its
adaptations, its conventions — not like the boilerplate. Nothing serves that at
all. `vzakharov/vovazakharov.com` spinning off a second static site
([its PR #38](https://github.com/vzakharov/vovazakharov.com/pull/38)) is the
worked instance the issue cites, and the parts that were real work there were the
three-way triage and the watermark decision; the rest was mechanical.

## The scope cut: adopter-only

**#43 also names this repo as a caller, and this plan drops that.** The skill
serves one direction — adopter → sibling — and the boilerplate → new-project
direction stays where it is, as *"Use this template"* plus
`ADOPTING.md § Template fork`.

Why the cut is right rather than merely smaller:

- **The footguns all live on the dropped side.** Serving this repo means a
  stranger clones or template-forks the boilerplate to have somewhere to invoke
  the skill from, which is a fork in the fork list and a `/pr` step one slipped
  `cwd` away from a PR on somebody else's repository. Nothing on the adopter side
  has that shape: the caller is the invoker's own project.
- **It leaves one procedure per operation, which is what the issue actually
  wanted.** #43 argues `## Template fork` must go because two procedures for one
  operation drift. Under this cut they are not one operation: a template fork
  turns a copy of the boilerplate into a project, `/spinoff` derives a new repo
  from a working one. Neither can stand in for the other, so neither rots against
  the other.
- **The dropped caller was the weaker of the two anyway.** From here the triage is
  a catalog lookup, which `ADOPTING.md` already covers. The judgment the skill
  exists for — deciding per path what travels out of a tree nobody has an
  inventory of — only arises from an adopter.

**Consequence to carry:** #43's `## What /spinoff replaces` section and its
four-row mapping table are superseded, and the issue body will read as partly
unimplemented. Worth a comment on the issue when this lands, so the next reader
does not go looking for the deletion.

## Scope of the change

| File | Change |
| --- | --- |
| `.claude/skills/spinoff/SKILL.md` | new — the skill, shipped hydrated |
| `docs/catalog.md` | one G0 row, and a G0 intro naming both directions |
| `README.md` | skill count only |
| `CLAUDE.md` | one line in § "Working with skills" |

`ADOPTING.md` is untouched.

## The skill

### Argument and end state

`/spinoff <owner/name>` — the target repository to create. End state: the target
exists, `main` carries one commit of agent infrastructure, `check-skill-catalog.sh`
passes there, and the operator holds a copyable command that opens the next
session in the new repo.

### Two invariants, stated before the steps

**Not from the boilerplate.** `docs/catalog.md` present in the caller → stop and
point at `README.md`'s template route. One test, and it is the honest one: the
catalog is what a tree has when it *is* this repo or an unpruned copy of it, and
in either case a spinoff is the wrong operation — prune and hydrate first, and
the pruned result is a legitimate caller later. Refusing here is also what keeps
the fork-and-PR footguns off the board entirely.

**The caller is read-only.** No commit, branch, PR or issue lands there; the
caller is a source of files and a source of the watermark, and every artifact
lands in the target. The write access the skill needs is on the **target's
owner** — creating the repo and pushing to it. If the target cannot be created,
Step 3 stops and asks; it never falls back to writing somewhere it can. The one
place this could break by accident is Step 3's `/pr` delegation, which runs
against whatever `cwd` holds while Bash `cwd` resets between calls in this
harness — so that step carries a guard.

### Step 1 — Read the caller

The skill's input is the repo it is invoked from, at HEAD: an adopter, whose tree
is a superset of the boilerplate's — those files, plus stack scaffolding
(`tsconfig`, `eslint/`, a real `vet.sh` instead of the stub), plus
project-specific `.claude/rules/`, plus the product. No adopter maintains a
catalog of its own, so the triage is derived per run rather than looked up.

Also read here: the caller's own sync skill and watermark. **Locate it by its
watermark file, not by name.** `/sync-agent-infra` itself prescribes that an
adopter renames the skill after its own source, so a real adopter's copy is
plausibly `.claude/skills/sync-agent-boilerplate/source.json` — hunting for
`sync-agent-infra/upstream.json` finds nothing and silently seeds an unlinked
repo. Glob `.claude/skills/*/*.json` and read the one whose object carries
`repo` and `lastSyncedSha`.

### Step 2 — Triage, three-way

- **Agent infrastructure** — travels always. `.claude/` (skills, rules, hooks,
  settings), `scripts/`, `CLAUDE.md`, `README.md`, the editor/format config.
- **Stack scaffolding** — travels when the stacks match, which is usually the
  whole reason for the spinoff: build config, lint config, the real `vet.sh`,
  CI workflows, the generated-styles/test tooling around them.
- **Product, and anything path-scoped to it** — never travels.

**Path-scoped rules are the trap, and the skill says so outright.** A
`.claude/rules/*.md` scoping a directory the new repo will not have sits beside
three that should travel, and a directory-level copy takes all four. Every rule
file is decided on its own `paths:` globs.

`CLAUDE.md` and `README.md` travel as **rewrites, not copies**: the
stack-agnostic sections carry across unchanged, and the ones describing the
caller ("About this project", "Repository layout", "Vetting", "Working with
skills") are written for the target.

That per-path judgment is what makes this a skill rather than a script.

### Step 3 — The watermark fork, surfaced with its cost

The watermark is the whole point of the link. Two defensible answers, and the
skill **surfaces the choice with its cost rather than defaulting it**:

- **Sibling** — the new repo points at the boilerplate. Clean lineage; the
  caller's stack-specific adaptations (its real `vet.sh`, above all) never flow
  forward and get re-derived on every sync.
- **Chain** — the new repo points at the caller, which is what
  `/sync-agent-infra` already prescribes for a repo adopting from a repo. The
  adaptations carry, at the cost of the boilerplate reaching the new repo one hop
  later.

Two mechanics the skill writes out, because getting either wrong is silent:

- **`lastSyncedSha` under *sibling* is the caller's own `lastSyncedSha`, not the
  boilerplate's HEAD.** The files are being copied from a tree synced to exactly
  that point, so that is the honest mark; the boilerplate's HEAD would claim the
  target already carries commits nobody ported. Under *chain* it is the caller's
  HEAD.
- **A chained watermark inherits the parent's `adopted` paths, so verify them
  against the parent's tree before writing them.** [#40](https://github.com/vzakharov/agent-project-boilerplate/issues/40)
  is the live example: a parent whose `adopted` list still spells
  `.claude/skills/sync-upstream/` silently drops every future commit under the
  renamed path from its candidate sets, and copying that list forward propagates
  the blind spot into a second repo.

The skill also names the target's sync skill after **its** source and clears both
stub markers, since the watermark it just wrote is the hydration.

### Step 4 — Seed: `main`, then the branch

The constraint that shapes this: the new repo's first session must be able to run
`/handle`, which means `.claude/skills/handle/SKILL.md` — and everything it
`@`-references — has to be on the branch already. "Create the repo, then start
working in it" does not work.

1. **Create the target.** `mcp__github__create_repository`, falling back to
   `gh repo create`, falling back to asking the operator to create it empty. Ask
   public-or-private in the same breath as `<owner/name>` if the invocation did
   not say. Then attach with `add_repo` at `access: "push"` — a read-scoped
   attach cannot push the branch this step exists to produce — and clone it.
2. **`main` gets one commit: the agent infrastructure.** Nothing
   project-specific. Then run `bash scripts/check-skill-catalog.sh` **in the
   target**: a partial copy dangles `@`-references *silently*, which is precisely
   the failure mode a hand-copy produces.
3. **A session-style branch gets the project**, opening with
   `docs/plans/<slug>.paused.md` — the plan for the work itself, in the state
   `/handle`'s plan lane resumes from. Reuse the caller's branch slug and hash
   suffix when the caller is on a session branch, so the lineage reads off the
   name; derive a fresh `claude/<slug>-<hash>` otherwise.
4. **Open the draft PR there and post the squash proposal** by loading
   `@.claude/skills/pr/SKILL.md` with the target clone as the working directory.
   **Assert the directory before loading it** — `git -C <clone> remote get-url
   origin` must name the target — and stop if it does not. `/pr` pushes and
   opens a PR against whatever repo `cwd` resolves to, so a slipped `cwd` aims
   the whole step at the caller: the operator's own working project, mid-flight.

**Where the line between the two commits falls is not a judgment call, and the
skill says so.** Closure decides it: `check-skill-catalog.sh` fails on a dangling
`@.claude/skills/…` reference, and the transitive closure of `/handle` reaches
almost the whole skill set — so "the basic skills needed to run the loop"
collapses to "all of the agent infrastructure", and infrastructure-vs-project is
the only clean cut left.

Two things this buys over seeding everything onto one branch off an empty `main`.
Every future branch in the new repo inherits the loop, so an abandoned seed
branch does not leave the repo inert. And the seed PR's diff is *the project*,
not a hundred infrastructure files nobody will read in that context — they were
already reviewed where they came from.

**No plan to carry → substeps 3 and 4 do not run.** A spinoff whose project work
has not been planned yet seeds `main` alone and hands over `/plan` in the target
instead of `/handle`. Seeding an empty branch would give phase 2 nothing to
resume from.

### Step 5 — Hand over

Two phases, and the seam is a change of repository:

1. **Seed — runs in the caller.** Everything above. It writes no application
   code, and every file it commits lands in the target, so it belongs in the
   session that already holds the context for why the new repo exists — a
   planning session, typically — rather than in a fresh one that would re-read
   all of it to do fifteen minutes of `git`.
2. **Build — runs in the target.** A new session rooted in the new repo, opened
   with the copyable block this step emits: `/handle claude/<slug>-<hash>`, or
   `/plan <purpose>` where there was no plan to carry.

The reason the seam is where it is: from phase 2 onward the target's own
`CLAUDE.md` and `.claude/rules/` are loaded, which is exactly what the
scaffolding decisions want in context. Making them from the caller means making
the new repo's architectural choices with the *old* repo's rules resident.

The report also carries the one thing no agent can apply: the **environment setup
script**, which lives in Claude Code's environment settings and has no API behind
it. The skill's line here is short because the caller demonstrably has one
already — it tells the operator to reuse the caller's environment setup script
for the target's environment, adapting the pins, rather than restating what goes
in it.

## Companion edits

### `docs/catalog.md`

One G0 row, `adopt`:

> `/spinoff` — Seed a new sibling repo out of the adopter you are standing in:
> triage what travels, write the target's watermark, and hand over a session in
> it. Requires `gh`, `$GH_TOKEN`, repo-creation rights on the target's owner.
> Pulls in `/pr` (G2).

G0's intro gains a sentence naming both directions — `/sync-agent-infra` pulls
later changes in, `/spinoff` pushes a new repo out — since the group is now the
whole source-and-target relationship rather than just the sync half.

It also states the thing that reads as a defect otherwise: **both G0 skills are
inert in this repo, for the same structural reason.** This tree is the root — no
source above it to sync from, and not an adopter, so nothing to spin off from
either. `/sync-agent-infra` ships as a stub for want of a watermark; `/spinoff`
ships hydrated but refuses here. Downstream both work.

### `README.md`

Only the count in the opening paragraph: **28 skills (20 working, 8 stubs)** →
**29 (21 working, 8 stubs)**. Both acquisition routes stay exactly as they are —
the template button still creates a project from this repo, and
`ADOPTING.md § Template fork` is still its next step.

### `CLAUDE.md`

One line under § "Working with skills" → "Entry points and support", after
`/from-branch`. It says adopter-only, since a reader scanning that list is
otherwise going to try it here.

## Work items

- [ ] Write `.claude/skills/spinoff/SKILL.md`: frontmatter description (naming
      the adopter-only constraint), the refusal gate, the five steps, and the
      `@`-references to `/pr` and `/sync-agent-infra` § "The watermark".
- [ ] Add the `docs/catalog.md` G0 row and extend the G0 intro.
- [ ] Bump the `README.md` skill count.
- [ ] Add the `CLAUDE.md` skill-list line.
- [ ] `bash scripts/check-skill-catalog.sh` — exactly one `/spinoff` row, no
      dangling references, and the new skill must not trip assertion 4 (it ships
      hydrated, so no banner and no `STUB` in the description).
- [ ] Comment on #43 recording that the from-this-repo caller was cut and why.
- [ ] `/dry`, `/tighten-docs`, then `/pr`.

## DRY notes

- **The watermark's JSON shape is cited, not restated.**
  `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark" already owns the
  field-by-field contract, including the `{path: note}` entry form and why
  `declined` reasons are written as present-tense conditions. `/spinoff` states
  only what is *its own*: which SHA is honest under each fork answer, and the #40
  inherited-`adopted` trap. A second copy of the schema would be the first thing
  to drift.
- **The PR furniture is delegated, not reimplemented.** Opening the target's
  draft PR and posting its squash proposal is `@.claude/skills/pr/SKILL.md`'s
  job, loaded with the target clone as cwd. The only thing `/spinoff` contributes
  is that cwd and the assertion guarding it.
- **Closure is asserted, not re-derived.** `scripts/check-skill-catalog.sh`
  already knows what a complete copy looks like; the skill runs it in the target
  rather than carrying its own list of what `/handle` reaches.
- **The three-way triage is stated once, here, and has no counterpart to share
  with.** The adopter-only cut is what makes this clean: with the from-this-repo
  caller gone, the skill never needs the catalog-lookup form of the same
  decision, so there is no second expression of it to keep in step.
- **`ADOPTING.md` and `/spinoff` are not two statements of one procedure**, which
  is the DRY question #43 raised and this cut answers. They describe different
  operations over different inputs — a copy of the boilerplate becoming a
  project, versus a working project deriving a new repo — and share only the
  environment-setup-script deliverable, which is two sentences in one and a
  subsection in the other because the callers know different amounts. Forcing a
  shared home would mean writing prose that is true of both and specific to
  neither.
- **No tombstone, because nothing is retired.** `ADOPTING.md` keeps every
  section it has.

## Settled

*The skill is named `/spinoff`.* `/seed-repo` reads as though it operates on the
current repo, and `/fork-out` collides with what "fork" already means on GitHub.

*It runs from adopters only.* Serving this repo too was carried through two
earlier drafts — first deleting `ADOPTING.md § Template fork` outright per #43,
then keeping the README button as a "launcher" fork you invoke the skill from.
Both were rejected as more machinery than the original intent (clone a sibling
repo) justifies, and the launcher variant additionally invited stray forks and
PRs against the boilerplate.

## Explicitly out of scope

- **Hydrating `/sync-agent-infra`.** It stays a stub here; this repo has no
  source above it. `/spinoff` writing a hydrated watermark *into a target* is not
  the same thing.
- **#40's rename.** This plan cites it as the cautionary case and makes
  `/spinoff` robust to it (Step 1 finds the sync skill by its watermark file, not
  its name); fixing the rename itself is that issue's.
- **Making the `gh`-heavy skills proxy-safe** ([#6](https://github.com/vzakharov/agent-project-boilerplate/issues/6)).
  The target inherits whatever the caller has.
