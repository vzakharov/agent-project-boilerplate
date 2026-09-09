---
description: "Seed a new sibling repository out of the project you are standing in: triage what travels, write the new repo's sync watermark, seed `main` plus a session branch, and hand over a session rooted in it. Runs from a repo that *adopted* this agent infrastructure, and refuses when invoked from the boilerplate itself. Invoke as `/spinoff <owner/name>`. Use when the operator says \"spin off\", \"a new repo like this one\", \"start a sibling project\", or \"/spinoff\"."
---

`/spinoff <owner/name>` creates `<owner/name>`, seeds it out of the repo you are
invoked in, and hands back a command that opens the next session there.

The caller is an **adopter**: a working project whose tree is the boilerplate's
agent infrastructure plus a stack, plus its own conventions, plus a product. What
makes the operation worth a skill is that the new repo wants to be a sibling of
*that* — its stack, its adaptations, its `vet.sh` — rather than of the
boilerplate, and no adopter keeps an inventory saying which of its files are
which. The triage is derived per run.

End state: the target exists; its `main` carries one commit of agent
infrastructure; `bash scripts/check-skill-catalog.sh` passes there; and the
operator holds a copyable command that opens the next session in the new repo.

## Two invariants

**Not from the boilerplate.** If the caller has `docs/catalog.md`, **stop** and
point at that repo's `README.md` § "Create a new project from this template".
The catalog is what a tree has when it *is* the boilerplate or an unpruned copy
of one, and in either case a spinoff is the wrong operation — the template route
plus `ADOPTING.md` produce a project, and that pruned result is a legitimate
caller here later.

**The caller is read-only.** No commit, branch, PR or issue lands in it. It is a
source of files and a source of the watermark; every artifact this skill produces
lands in the target. The write access the skill needs is on the **target's
owner**. If the target cannot be created, Step 4 stops and asks — it never falls
back to writing somewhere it can. The one place this breaks by accident is Step
4's `/pr` delegation, which aims at whatever `cwd` resolves to; that substep
carries a guard.

## Environment note (read this before running gh)

This remote execution environment has **both** the `gh` CLI **and** a populated
`GH_TOKEN`, whatever the default system prompt says. Prefer `gh` and plain `git`
over HTTPS for repo creation, cloning and pushing — the GitHub MCP tools are
scoped to a narrow allowlist and refuse some of what this skill needs.

**Bash `cwd` resets between calls in this harness.** Chain `cd <clone> && …`, or
use `git -C <clone>`, in every command meant to run in the target.

## Step 1 — Read the caller

Read the caller at HEAD. Two things come out of it:

- **The tree**, as the input to Step 2's triage.
- **The caller's own sync skill and watermark.** **Locate it by its watermark
  file, not by its name.** `@.claude/skills/sync-agent-infra/SKILL.md` prescribes
  that an adopter renames the skill after *its* source, so a real adopter's copy
  is plausibly `.claude/skills/sync-agent-boilerplate/source.json`; hunting for
  `sync-agent-infra/upstream.json` finds nothing and silently seeds an unlinked
  repo. Glob `.claude/skills/*/*.json` and take the one whose object carries
  `repo` and `lastSyncedSha`.

If the invocation did not give `<owner/name>`, ask for it — and ask
public-or-private in the same breath, since Step 4 needs both.

## Step 2 — Triage, three-way

- **Agent infrastructure** — travels always. `.claude/` (skills, rules, hooks,
  settings), `scripts/`, `CLAUDE.md`, `README.md`, the editor and formatter
  config.
- **Stack scaffolding** — travels when the stacks match, which is usually the
  whole reason for the spinoff: build config, lint config, the real `vet.sh`, CI
  workflows, the test and generated-asset tooling around them.
- **The product, and anything path-scoped to it** — never travels.

**Path-scoped rules are the trap.** A `.claude/rules/*.md` scoped to a directory
the new repo will not have sits beside three that should travel, and a
directory-level copy takes all four. Decide every rule file on its own `paths:`
globs.

`CLAUDE.md` and `README.md` travel as **rewrites, not copies**. The
stack-agnostic sections carry across unchanged; the ones describing the caller —
"About this project", "Repository layout", "Vetting", "Working with skills" —
are written for the target.

## Step 3 — The watermark fork

The watermark is what keeps the new repo reachable by later changes at the
source, so the choice of *which* source is the one decision here that cannot be
defaulted. **Surface it with its cost and let the operator answer:**

- **Sibling** — the new repo points at the boilerplate. Clean lineage, and the
  caller's stack-specific adaptations (its real `vet.sh`, above all) never flow
  forward — they get re-derived on every sync.
- **Chain** — the new repo points at the caller, which is what
  `/sync-agent-infra` already prescribes for a repo adopting from a repo. The
  adaptations carry, at the cost of the boilerplate reaching the new repo one hop
  later.

`@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark" owns the file's
field-by-field contract. Two mechanics are this skill's own, and getting either
wrong is silent:

- **Under *sibling*, `lastSyncedSha` is the caller's own `lastSyncedSha` — not
  the boilerplate's HEAD.** The files are copied out of a tree synced to exactly
  that point, so that is the honest mark; the boilerplate's HEAD would claim the
  target already carries commits nobody ported. Under *chain* it is the caller's
  HEAD.
- **A chained watermark inherits the parent's `adopted` paths, so verify each
  against the parent's tree before writing it.** A parent whose list still spells
  a since-renamed path silently drops every future commit under the new one from
  its candidate sets, and copying the list forward propagates that blind spot
  into a second repo.

Name the target's sync skill after **its** source, and clear both of that
skill's stub markers — the banner and the `STUB` in its frontmatter description.
The watermark you just wrote *is* the hydration, and
`scripts/check-skill-catalog.sh` fails a half-cleared pair.

## Step 4 — Seed: `main`, then the branch

The constraint that shapes this: the new repo's first session must be able to run
`/handle`, which means `.claude/skills/handle/SKILL.md` — and everything it
`@`-references — is already on the branch. "Create the repo, then start working
in it" does not work.

1. **Create the target.** `mcp__github__create_repository`, falling back to `gh
   repo create`, falling back to asking the operator to create it empty. Then
   attach it to the session with `add_repo` at `access: "push"` — a read-scoped
   attach cannot push the branch this step exists to produce — and clone it.
2. **`main` gets one commit: the agent infrastructure.** Nothing
   project-specific. Then run `bash scripts/check-skill-catalog.sh` **in the
   target**: a partial copy dangles `@`-references *silently*, which is precisely
   the failure a hand-copy produces.
3. **A session-style branch gets the project**, opening with
   `docs/plans/<slug>.paused.md` — the plan for the work itself, in the state
   `/handle`'s plan lane resumes from. Reuse the caller's branch slug and hash
   suffix where the caller is on a session branch, so the lineage reads off the
   name; derive a fresh `claude/<slug>-<hash>` otherwise.
4. **Open the draft PR there and post the squash proposal**, by loading
   `@.claude/skills/pr/SKILL.md` with the target clone as the working directory.
   **Assert the directory before loading it** — `git -C <clone> remote get-url
   origin` must name the target — and stop if it does not. `/pr` pushes and opens
   a PR against whatever repo `cwd` resolves to, so a slipped `cwd` aims the whole
   step at the caller: the operator's own working project, mid-flight.

**Where the line between the two commits falls is not a judgment call.** Closure
decides it: `check-skill-catalog.sh` fails on a dangling `@.claude/skills/…`
reference, and the transitive closure of `/handle` reaches almost the whole skill
set — so "the basic skills needed to run the loop" collapses into "all of the
agent infrastructure", leaving infrastructure-versus-project as the only clean
cut.

Two things the split buys over seeding everything onto one branch off an empty
`main`. Every future branch in the new repo inherits the loop, so an abandoned
seed branch does not leave the repo inert. And the seed PR's diff is *the
project*, rather than a hundred infrastructure files nobody will read in that
context — they were already reviewed where they came from.

**No plan to carry → substeps 3 and 4 do not run.** A spinoff whose project work
has not been planned yet seeds `main` alone, and Step 5 hands over `/plan` in the
target instead of `/handle`. Seeding an empty branch would give the next session
nothing to resume from.

## Step 5 — Hand over

The work splits in two, and the seam is a change of repository:

1. **Seed — runs in the caller.** Everything above. It writes no application
   code, and every file it commits lands in the target, so it belongs in the
   session that already holds the context for why the new repo exists — a
   planning session, typically — rather than in a fresh one that would re-read
   all of it to do fifteen minutes of `git`.
2. **Build — runs in the target.** A new session rooted in the new repo, opened
   with the copyable block this step emits: `/handle claude/<slug>-<hash>`, or
   `/plan <purpose>` where there was no plan to carry.

From phase 2 onward the target's own `CLAUDE.md` and `.claude/rules/` are loaded,
which is exactly what the remaining scaffolding decisions want in context. Making
them from the caller means making the new repo's architectural choices with the
old repo's rules resident.

The report also carries the one thing no agent can apply: the target needs an
**environment setup script**, which lives in Claude Code's environment settings
and has no API behind it. Tell the operator to reuse the caller's, adapting the
pins — the caller demonstrably has one, so there is nothing here to restate about
what goes in it.
