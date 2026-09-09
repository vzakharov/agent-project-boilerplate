> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# `/spinoff` — fire a new repo out of the one you are standing in

Closes [#43](https://github.com/vzakharov/agent-project-boilerplate/issues/43).

Add a hydrated `/spinoff <owner/name>` skill in **G0**, and delete
`ADOPTING.md`'s `## Template fork` section — plus the README route that points at
it — in its favour. Everything here is prose and shell; there is no stack to
touch.

## What is missing today

The infrastructure is written entirely from the **adopter's** side, pulling:
`ADOPTING.md` is read once over the network by the repo taking it on,
`docs/catalog.md` is the inventory it selects from, and `/sync-agent-infra` keeps
that selection current. Nothing serves the **source's** side, pushing — standing
in a repo and firing a new one out of it. Two callers want that, and both are
real:

- **From this repo.** Today's answer is *"Use this template"*: fork, then prune
  and hydrate inside the fork. Every decision is made after every file has
  already landed.
- **From an adopter.** Once a real project runs on this infrastructure, the
  recurring next move is *another repo like **this** one* — its stack, its
  adaptations, its conventions — not like the boilerplate. Nothing serves it.

## Scope of the change

| File | Change |
| --- | --- |
| `.claude/skills/spinoff/SKILL.md` | new — the skill, shipped hydrated |
| `ADOPTING.md` | delete `## Template fork`; rework the two-ways-in split and the shared-tail heading |
| `README.md` | replace the template-fork route with the `/spinoff` route; bump the skill count |
| `docs/catalog.md` | one G0 row, and a G0 intro that names both directions |
| `CLAUDE.md` | one line in § "Working with skills" |

## The skill

### Argument and end state

`/spinoff <owner/name>` — the target repository to create. End state: the target
exists, `main` carries one commit of agent infrastructure, `check-skill-catalog.sh`
passes there, and the operator holds a copyable command that opens the next
session in the new repo.

### Step 1 — Read the caller

The skill's input is the repo it is invoked from, at HEAD. Two shapes, and the
skill reads which it is standing in rather than being told:

- **`docs/catalog.md` present** → the caller is this boilerplate (or something
  that kept the catalog). The catalog answers the triage outright: its `never`
  rows are what does not travel, and its group rows are the rest.
- **absent** → the caller is an adopter. Its tree is a superset — the
  boilerplate's files, plus stack scaffolding (`tsconfig`, `eslint/`, a real
  `vet.sh` instead of the stub), plus project-specific `.claude/rules/`, plus the
  product — and no adopter maintains a catalog of its own. The triage is derived
  per run, per Step 2.

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
skills") are written for the target. From this repo that is the same edit the
old `## Template fork` step 3 asked for, moved before the copy.

That per-path judgment is what makes this a skill rather than a script.

### Step 3 — The watermark fork, surfaced with its cost

`upstream.json` is the whole point of the link. Two defensible answers:

- **Sibling** — the new repo points at this boilerplate. Clean lineage; the
  caller's stack-specific adaptations (its real `vet.sh`, above all) never flow
  forward and get re-derived on every sync.
- **Chain** — the new repo points at the caller, which is what
  `/sync-agent-infra` already prescribes for a repo adopting from a repo. The
  adaptations carry, at the cost of the boilerplate reaching the new repo one hop
  later.

The skill **surfaces the choice with its cost and does not default it**. It is
live only for the adopter caller; called from here, the target's source is this
repo and there is nothing to ask.

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

**No plan to carry → step 3 and 4 do not run.** A spinoff whose project work has
not been planned yet seeds `main` alone and hands over `/plan` in the target
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

### `ADOPTING.md`

`## Template fork` is the same operation done by hand, and it **goes entirely**
rather than coexisting with the skill: two procedures for one operation drift,
and the fork path is the one that rots, being the one nobody re-reads. Its four
steps are what the skill does, moved before the copy instead of after it:

| `## Template fork` step | Becomes |
| --- | --- |
| Delete the `never` rows | Never copied in the first place |
| Prune the groups you don't need | Step 2's triage against `docs/catalog.md` — same criteria, no deletes |
| Fill in the `CLAUDE.md` stub | Written for the target as part of the seed commit |
| Implement dep-install in the hook | Same, or left as the stub it is with the target's stack unknown |

So the top-of-file *"pick the one that matches how you got here"* split changes
shape rather than disappearing: **adopt into an existing repo** stays — the
target pre-exists with its own history, which is genuinely a different
operation — and **template fork** becomes a pointer to `/spinoff`. With one mode
left, `## Shared tail (both modes)` loses its parenthetical and the "Both
converge on…" line goes with the split it described.

The tail's own content is untouched: an adopter still merges `CLAUDE.md`,
rewrites `vet.sh`, hydrates or deletes the G6 stubs, hydrates the sync stub, and
gets handed the setup script.

### `README.md`

§ "Create a new project from this template" is the route that sends readers to
the deleted section, so it is replaced rather than repointed: open a session on
this repo (or a clone of it) and run `/spinoff <owner/name>`. The `gh repo create
--template` recipe goes with it — the skill creates the repo, so a
pre-created template fork is a tree the skill would have to reconcile with rather
than a head start.

The count in the opening paragraph moves from **28 skills (20 working, 8 stubs)**
to **29 (21 working, 8 stubs)**.

### `docs/catalog.md`

One G0 row, `adopt`:

> `/spinoff` — Seed a new sibling repo out of the repo you are standing in:
> triage what travels, write the target's watermark, and hand over a session in
> it. Requires `gh`, `$GH_TOKEN`, repo-creation rights. Pulls in `/pr` (G2).

G0's intro gains a sentence naming both directions — `/sync-agent-infra` pulls
later changes in, `/spinoff` pushes a new repo out — since the group is now the
whole source-and-target relationship rather than just the sync half. Unlike
`/sync-agent-infra`, `/spinoff` **ships hydrated**: there is no per-repo state to
fill in, because its input is the repo it is invoked from.

### `CLAUDE.md`

One line under § "Working with skills" → "Entry points and support", after
`/from-branch`.

## Work items

- [ ] Write `.claude/skills/spinoff/SKILL.md` with the frontmatter description,
      the five steps above, and the `@`-references to `/pr` and
      `/sync-agent-infra` § "The watermark".
- [ ] Delete `ADOPTING.md` § "Template fork"; rework the two-ways-in split and
      the shared-tail heading.
- [ ] Replace `README.md` § "Create a new project from this template"; bump the
      skill count.
- [ ] Add the `docs/catalog.md` G0 row and extend the G0 intro.
- [ ] Add the `CLAUDE.md` skill-list line.
- [ ] `bash scripts/check-skill-catalog.sh` — the new skill needs exactly one
      catalog row and no dangling references.
- [ ] `/dry`, `/tighten-docs`, then `/pr`.

## DRY notes

- **The watermark's JSON shape is cited, not restated.** `/spinoff` writes a
  `upstream.json`-shaped file, and `@.claude/skills/sync-agent-infra/SKILL.md`
  § "The watermark" already owns the field-by-field contract, including the
  `{path: note}` entry form and why `declined` reasons are written as present-tense
  conditions. The skill states only what is *its own*: which SHA is honest under
  each of the two fork answers, and the #40 inherited-`adopted` trap. A second
  copy of the schema would be the first thing to drift.
- **The PR furniture is delegated, not reimplemented.** Opening the target's
  draft PR and posting its squash proposal is `@.claude/skills/pr/SKILL.md`'s
  job, loaded with the target clone as cwd. The only thing `/spinoff` contributes
  is that cwd — worth one explicit sentence, since Bash `cwd` resets between
  calls in this harness.
- **Closure is asserted, not re-derived.** `scripts/check-skill-catalog.sh`
  already knows what a complete copy looks like; the skill runs it in the target
  rather than carrying its own list of what `/handle` reaches.
- **The triage criteria are cited when the catalog exists and derived when it
  does not** — that asymmetry is the skill's actual content, not a duplication.
  From this repo, `docs/catalog.md`'s groups and `never` rows *are* the answer,
  so the skill points at them. From an adopter there is nothing to point at, so
  the three-way rule is stated once, here.
- **`ADOPTING.md`'s deleted section is not moved, it is replaced.** The four
  steps do not reappear anywhere as prose; each is absorbed into a step the skill
  already performs, and the mapping table lives in the PR/squash record rather
  than in a surviving doc. Keeping the table in `ADOPTING.md` would leave the
  fork procedure legible enough to follow by hand, which is the drift the
  deletion exists to prevent.
- **No tombstone.** CLAUDE.md § "Writing things down" requires one for a retired
  *doc*; this retires a section of a living file, whose history `git log -p
  ADOPTING.md` already resolves, and the two surviving citations are both
  rewritten in the same change rather than left dangling.
- **Not extracted: a shared "seed a repo" helper between `/spinoff` and
  `ADOPTING.md`.** They now describe opposite operations — one creates a target
  from a source, the other merges a source into a pre-existing target — and the
  only thing they still share is the environment-setup-script deliverable, which
  is two sentences in one and a subsection in the other because the callers know
  different amounts.

## Open questions

**1. The skill's name.** The issue leaves it open.

- **(a) `/spinoff`** *(recommended, and written into this plan)* — the issue's own
  leading name, reads as a verb from either caller, and collides with nothing.
- (b) `/seed-repo` — names the mechanism (`main` gets a seed commit) but reads
  like it operates on the current repo.
- (c) `/fork-out` — accurate about direction, but "fork" already means something
  specific on GitHub that this is not.

**2. Does the *"Use this template"* button survive in `README.md`?**

- **(a) No — replaced entirely by the `/spinoff` route** *(recommended, and
  written into this plan)*. The issue's argument against two procedures for one
  operation applies to the README as much as to `ADOPTING.md`, and with
  `## Template fork` gone the button leads to a fork with no documented next
  step.
- (b) Keep it as a secondary route for someone who wants the files without an
  agent session — at the cost of the fork path being back, undocumented.

Both carry recommendations, so the plan is implementable as written; an answer
that differs is a revision, and silence means the recommendations stand.

## Explicitly out of scope

- **Hydrating `/sync-agent-infra`.** It stays a stub here; this repo has no
  source above it. `/spinoff` writing a hydrated watermark *into a target* is not
  the same thing.
- **#40's rename.** This plan cites it as the cautionary case and makes
  `/spinoff` robust to it (Step 1 finds the sync skill by its watermark file, not
  its name); fixing the rename itself is that issue's.
- **Making the `gh`-heavy skills proxy-safe** ([#6](https://github.com/vzakharov/agent-project-boilerplate/issues/6)).
  The target inherits whatever the caller has.
