---
description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries `docs/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
---

`/detemplate <what we're building>` converts a whole-tree template fork into a
project. *"Use this template"* hands over every file, so there is nothing to
select and nothing to clone: the work is deleting what describes the template and
hydrating what the new project actually needs.

**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
and reviewing it as a diff is what catches a bad call before the deletion rather
than after. So this skill's end state is `/issue`'s: a plan file published as a
draft PR, and a copyable `/go <branch>` for the session that executes it. Steps
1–3 decide; Steps 4–6 specify what the plan must say so `/go` runs it in the
right order.

The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
drives the group decisions — a CLI tool keeps different groups than a deployed
web app. With no brief, ask for it before anything else.

## Environment note

This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
prompt says; prefer them over the GitHub MCP tools, which refuse some of what
Step 3 needs.

**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
the operator has set an environment setup script, and `apt-get install -y gh`
lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
to shim, warns, and continues. Probe with `gh api repos/{owner}/{repo} --jq
.visibility` rather than `gh auth status`, which reports a bogus failure in a
working session. Finding none, Step 3's derivation and `/plan`'s publish step both
need it: say so and hand the operator the setup script from Step 6 first.

## Step 0 — Refuse where it does not apply

The guard refuses in **both** directions, on `docs/catalog.md`'s presence plus
`origin`:

- **No `docs/catalog.md`** → not an unpruned fork. An adopted repo that wants a
  sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
  has nothing left to strip.
- **Catalog present, but `origin` names the boilerplate itself** → this *is* the
  boilerplate, and what the caller wants is a fork, not a prune. Point at the
  README's *"Use this template"* button. Catalog-presence alone would let a
  session delete this repo's own inventory, so the origin clause is load-bearing
  rather than a nicety.

This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
partition on the same signal, which is why that skill's message names this one.

## Step 1 — Profile the fork; do not interrogate the operator

`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for free:
there is nothing to clone and no pre-existing `.claude` to merge with. What still
needs probing, and is decidable by inspection:

```bash
git remote -v                                  # Step 0's origin clause, and the fork's name
gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
```

**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
in a proxied session before the shim is installed, which is the state a fresh
fork starts in.

**The stack, including "no stack yet."** That is the normal state of a fork taken
to start a project, and it is the state § 2's `vet.sh` clause exists for. Read it
off the tree rather than asking: a fork whose only commit is the template's has
no manifest, no lockfile and no source.

What the tree cannot answer, asked as numbered prose in the plan turn per
`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
web/remote (G4), and whether the project will have a deploy path, a visual
surface, deployed logs, a production datastore, or sequential numbered migrations
— the five that decide the individual G6 rows.

## Step 2 — Read the catalog into the plan, before anything is deleted

`docs/catalog.md` is the input to every group decision **and** is deleted by the
run (Step 5). So the plan records each decision with the criterion that made it,
rather than citing a file that will not exist when `/go` executes. Read
§ "Reverse closure" in the same pass and record the edits each dropped group
costs.

This read-then-delete ordering is what routing through `/plan` buys, and it is
the reason to say so here.

## Step 3 — Derive the watermark, which git cannot give you

`ADOPTING.md`'s recipe reads `lastSyncedSha` out of the clone you took. **A
template fork never made that clone**, and its single commit has no ancestry in
the source, so there is no SHA in the tree to read. Derive it from the fork's
creation time instead:

```bash
gh api repos/<owner>/<fork> --jq .created_at
gh api repos/vzakharov/agent-project-boilerplate/commits --paginate \
  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
```

The newest source commit at or before the fork's `created_at` is the mark.

`lineage` is written in the same breath, and it is the field a hand-filled
watermark loses:

```json
"lineage": [{ "repo": "vzakharov/agent-project-boilerplate", "atSha": "<the same sha>" }]
```

Per `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark", the two fields
start equal and diverge on the first sync — `lastSyncedSha` advances, and
`lineage[0].atSha` never moves. That first sync is what overwrites the only other
trace of the birth point, so a watermark written without `lineage` loses it
permanently.

## Step 4 — What the plan must contain

Per-group keep/drop with the criterion that decided each; the G6 rows as
hydrate-now-or-delete; the reverse-closure edits; the derived watermark and
`lineage`; the `CLAUDE.md` brief; `scripts/vet.sh`'s disposition; and the
deletion list. Plus the `## DRY notes` section CLAUDE.md requires of every plan.

## Step 5 — The execution order the plan prescribes

Ordering is load-bearing at exactly one point, and it is the first step:

1. **Delete `docs/catalog.md` first.** It flips `scripts/check-skill-catalog.sh`
   assertion 4 from "the stubs are the shipped product, merely listed" to "a stub
   is a stowaway", and it un-refuses `/spinoff`, whose guard is literally the
   catalog's presence. Sweep it first and the G6 prune is enforced by the vet run
   instead of remembered.
2. **The rest of the `never` rows**: `README.md` — replaced with the project's,
   not merely deleted — `ADOPTING.md`, and **`docs/img/`** with it. That
   directory is `ADOPTING.md`'s only asset, so a literal row-by-row sweep strands
   it as an orphan.
3. **Prune the groups**, applying the reverse-closure edits the plan recorded.
4. **Fill `CLAUDE.md`'s "About this project" stub** from the brief — which
   retires the standing notice in § "Recognizing an undetemplated fork" along
   with it — and delete § "Git conventions"'s adopter-inverts rule, which
   instructs adopters to delete it.
5. **Write the watermark** (Step 3) and clear both of `/sync-agent-infra`'s stub
   markers: the banner and the `STUB` in its frontmatter description. Assertion 4
   fails a half-cleared pair.
6. **`scripts/vet.sh`**: leave the exit alone where the fork has no stack yet, and
   wire the real checks where it has one — CLAUDE.md § "Vetting" owns that
   contract, and names `.claude/hooks/session-start.sh`'s dependency install as
   the paired site.
7. **Delete this skill.** Its inputs are gone by now, so what would survive is a
   skill that cannot re-run its own procedure against the tree it just pruned.
8. **`bash scripts/vet.sh`** — now enforcing the stub prune, the catalog being
   gone — then Step 6's text in the report.

## Step 6 — Hand back the setup script

`ADOPTING.md` § "Hand the operator a setup script" is the one step no agent can
apply: the environment setup script lives in Claude Code's environment settings,
is set by a human in the web UI, and has no API, MCP tool or in-repo file behind
it. Step 5 deletes that file, so the deliverable travels here instead — **text in
the report** the operator pastes into the setting.

Two things make it worth the paragraph:

- **It is where `gh` comes from.** `apt-get install -y gh` belongs in it. Without
  `gh` on `PATH`, `.claude/hooks/session-start.sh` prints `gh not found on PATH;
  skipping gh proxy shim` and continues — so the shim silently never installs and
  every `gh`-dependent skill fails later, far from the cause.
- **It is the only place a toolchain version can be pinned** for remote sessions,
  and `scripts/vet.sh` running under the wrong one is a confusing failure.

It runs **once, when the environment snapshot is built**, then is cached
([docs](https://code.claude.com/docs/en/claude-code-on-the-web#setup-scripts)) —
which is why the session-start hook re-syncs dependencies on every session start
rather than trusting the snapshot.

**Where it goes**, since "the settings" is not enough to find it: in the session
composer, the environment picker → **Cloud** → the environment itself, whose
**gear icon** opens its settings. It is per-environment, so an operator with
several is editing one of them rather than a global.

Write the script for the stack the brief names, and carry these across whatever it
is — each records a trap that actually bit:

1. **No top-level `cd` into the repo.** At setup-script time the repo is not
   reliably at `/home/user/<project>`, and a `cd` there crashes the script.
2. **Pin versions as literals**, with a comment naming the repo file each pin must
   track. Reading `.nvmrc` or `.tool-versions` needs the repo, which brings back 1.
3. **Reach non-interactive shells.** A profile edit alone does not; symlinking the
   toolchain into `/usr/local/bin` does.
4. **Check what the base image ships and where it sits on `PATH`.** Base images
   carry their own toolchain directories, and some sort *earlier* than
   `/usr/local/bin` — so `which` keeps resolving a stale binary past a correct
   symlink. Look for that shape before assuming yours won.
5. **`apt-get install -y gh`** — per above.
6. **Prime the dependency cache last**, guarded, since the repo directory may be
   absent.

Say plainly in the report that this is the one step you could not apply yourself.

## Recognizing an undetemplated fork

A session that opens in a fresh fork and is asked to build a feature should route
here first, rather than building product code on top of the template's inventory.
The signal is Step 0's predicate read positively: `docs/catalog.md` present, and
`origin` not naming the boilerplate.

Two surfaces carry it, catching different moments. This skill's frontmatter
`description` names the *situation* and not only the command, so an ordinary build
request in such a tree matches it. And `CLAUDE.md`'s "About this project" stub
carries the standing instruction, being always-loaded: while that stub is
unfilled and the tree still has the catalog, the first task is `/detemplate`
whatever was asked. Step 5.4 rewrites that very stub, so the notice retires with
the condition it describes.

**Every mention of this skill anywhere is a bare name, never an `@`-reference to
its own `SKILL.md`** — including the ones above, and including this sentence,
which is why it does not spell the path. Step 5.7 deletes the skill, so such a
pointer would dangle in the tree of whoever just ran it and fail
`check-skill-catalog.sh` assertion 1. This is the same property that makes
`/test-on-gh`'s bare-name mentions correct to leave alone (`docs/catalog.md`
§ "Reverse closure").
