# Issue #43: A skill for spinning off a sibling repo from an adopter, not just adopting into one

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/issues/43
- **Author:** @vzakharov
- **Created:** 2026-09-09T20:21:12Z
- **Updated:** 2026-09-09T21:51:16Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## The direction that's missing

Everything here is written from the **adopter's** point of view, pulling:
`ADOPTING.md` is read once over the network by the repo taking the
infrastructure on, `docs/catalog.md` is the inventory it selects from, and
`/sync-agent-infra` keeps the selection current afterwards.

There is no counterpart for the **source's** point of view, pushing — for
standing in a repo and firing a new one out of it. That has two callers, and
both are real today:

- **From this repo.** Today that is the *"Use this template"* path: fork, then
  prune and hydrate inside the fork. It works, but it is the long way round —
  every decision is made after every file has already landed.
- **From an adopter.** Once you have built a real project on this
  infrastructure, the recurring next move is *I want another repo like this
  one* — not like the boilerplate, like **this repo**, with its stack, its
  adaptations and its conventions. There is nothing for this at all.

The closest analogy is `npx create-*`, except the template is not a published
package: it is whatever repo the skill is called from, at HEAD, minus what does
not apply.

## What `/spinoff` replaces, so nothing is stated twice

`ADOPTING.md`'s `## Template fork` section is the same operation done by hand,
and it must **go entirely** rather than coexist with the skill — two procedures
for one operation drift, and the fork path is the one that will rot, being the
one nobody re-reads. Its four steps are exactly what the skill does, moved
before the copy instead of after it:

| `## Template fork` step             | Becomes                                                                    |
| ----------------------------------- | ---------------------------------------------------------------------------- |
| Delete the `never` rows             | Never copied in the first place                                            |
| Prune the groups you don't need     | The triage below, run against `docs/catalog.md` — same criteria, no deletes |
| Fill in the `CLAUDE.md` stub        | Written for the target as part of the seed commit                          |
| Implement dep-install in the hook   | Same, or left as the stub it already is with the target's stack unknown     |

So the top-of-file *"pick the one that matches how you got here"* split changes
shape: **adopt into an existing repo** stays (the target pre-exists with its own
history — genuinely different), and **template fork** is replaced by a pointer
to `/spinoff`. `docs/catalog.md` is untouched and gains a row; the skill is one
of its consumers, alongside `/sync-agent-infra`.

## The triage, when the caller is an adopter

Called from here, the catalog answers everything. Called from an adopter it
cannot: that tree is a superset — the boilerplate's files, plus stack
scaffolding (`tsconfig`, `eslint/`, a real `vet.sh` instead of the stub), plus
project-specific `.claude/rules/`, plus the product — and no adopter is going to
maintain a catalog of its own.

So the triage is derived per run, and it is three-way:

- **Agent infrastructure** — travels always.
- **Stack scaffolding** — travels when the stacks match, which is usually the
  whole reason you are doing this.
- **Product, and anything path-scoped to it** — never travels. Path-scoped
  rules are the trap: a `.claude/rules/*.md` scoping a directory the new repo
  will not have sits beside three that should travel, and gets copied wholesale.

That per-path judgment is what makes this a skill rather than a script.

## The mechanism: what lands on `main`, what lands on the branch

The constraint that shapes it: the new repo's first session must be able to run
`/handle`, which means `.claude/skills/handle/SKILL.md` — and everything it
`@`-references — has to be **on the branch already**. "Create the repo, then
start working in it" does not work.

The split that falls out:

- **`main` gets one commit: the agent infrastructure.** `.claude/` (skills,
  rules, hook, settings), `scripts/`, the `CLAUDE.md` written for the target,
  `README.md`, and the editor/format config. Nothing project-specific.
- **A session-style branch (`claude/<slug>-<hash>`) gets the project**, opening
  with `docs/plans/<slug>.paused.md` — the plan for the work itself, in the
  state `/handle`'s plan lane resumes from — plus its own draft PR and squash
  proposal.

Two things this buys over seeding everything onto the branch off an empty
`main`. Every future branch in the new repo has the loop, not just the seeded
one — so an abandoned seed branch does not leave the repo inert. And the seed
PR's diff is *the project*, not a hundred infrastructure files no one will read
in that context; it was already reviewed where it came from.

**Where the line falls is not a judgment call, which is worth stating outright:**
closure decides it. `check-skill-catalog.sh` fails on a dangling
`@.claude/skills/…` reference, and the transitive closure of `/handle` reaches
almost the whole skill set — so "the basic skills needed to run the loop"
collapses to "all of the agent infrastructure", and the only clean cut left is
infrastructure-vs-project. A partial copy dangles references **silently**, which
is precisely the failure mode a hand-copy produces; the skill should run
`check-skill-catalog.sh` in the target before handing it over.

## The two phases, and which repo each runs in

The skill's output is a handoff, not a finished repo, and the seam is a change
of repository:

1. **Seed — runs in the caller.** Create the target, push the two commits above,
   open the draft PR there, post the squash proposal. This phase is plumbing: it
   writes no application code, and every file it commits lands in the target.
   It belongs in the session that already holds the context for why the new repo
   exists — a planning session, typically — rather than in a fresh one that
   would re-read all of it to do fifteen minutes of `git`.
2. **Build — runs in the target.** A new session rooted in the new repo, opened
   with `/handle claude/<slug>-<hash>`, which finds the paused plan and resumes
   from it.

The reason the seam is where it is: from phase 2 onward the target's own
`CLAUDE.md` and `.claude/rules/` are loaded, which is exactly what the
scaffolding decisions want in context. Doing them from the caller means making
the new repo's architectural choices with the *old* repo's rules resident.

## The watermark fork the skill must force

`upstream.json` is the whole point of the link, and there are two defensible
answers with different costs:

- **Sibling** — point the new repo at this boilerplate. Clean lineage, but the
  parent's stack-specific adaptations (its real `vet.sh`, above all) never flow
  forward, and get re-derived on every sync.
- **Chain** — point it at the parent, which `/sync-agent-infra` already
  prescribes ("A repo that adopts this skill from *here* should re-point
  `upstream.json` at this repo and rename the skill after its own source"). The
  adaptations carry, at the cost of the boilerplate reaching the new repo one
  hop later.

Both are right in different situations, so the skill's job is to **surface the
choice with its cost**, not to default it silently — and then to write the
watermark, the `adopted`/`declined` sets and the skill's own name accordingly.
When the caller is this repo the question does not arise; it is only live for
the adopter case. #40's rename is a live example of what the chain gets wrong
when left alone: a parent whose `adopted` list still spells
`.claude/skills/sync-upstream/` silently drops every future commit under the new
path from its candidate sets.

## Concrete instance

This came out of doing it by hand. `vzakharov/vovazakharov.com` (an adopter) is
spinning off a second static site that wants the same architecture:
https://github.com/vzakharov/vovazakharov.com/pull/38 — the plan's "Target
architecture" table and its two phases are, in effect, this skill's output
written out longhand for one case. The parts that were real work were the
three-way triage and the watermark decision; the rest was mechanical.

## Shape

`/spinoff <owner/name>` (naming open — `/seed-repo`, `/fork-out`) — belongs in
**G0** beside the sync path, being the same relationship viewed from the other
end, and needs its own `docs/catalog.md` row. It ships hydrated, unlike
`/sync-agent-infra`: there is no per-repo state to fill in, because its input is
the repo it is invoked from.

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Comments

### Comment by @vzakharov on 2026-09-09T21:51:16Z

[https://github.com/vzakharov/agent-project-boilerplate/issues/43#issuecomment-5609236161](https://github.com/vzakharov/agent-project-boilerplate/issues/43#issuecomment-5609236161)

Revised the body on three counts, all raised in review:

- **`/spinoff` from this repo is now a first-class caller**, not a footnote — and with it the DRY consequence: `ADOPTING.md`'s `## Template fork` section is deleted outright and replaced by a pointer to the skill, with a table mapping each of its four steps onto what the skill does instead. Two procedures for one operation drift, and the fork path is the one nobody re-reads.
- **The bootstrapping constraint now states its mechanism** rather than just the constraint: `main` takes one commit of agent infrastructure, the session-style branch takes the project and its paused plan. Added why the line falls exactly there — closure. `check-skill-catalog.sh` plus the transitive closure of `/handle` collapses "the basic skills needed to run the loop" into "all of the agent infrastructure", so infrastructure-vs-project is the only clean cut available.
- **Added the two-phase execution model**: seed runs in the caller, build runs in the target via `/handle`. The seam is a change of repository because from phase 2 onward the target's own `CLAUDE.md` and rules are loaded — which is precisely what the scaffolding decisions need in context.

---
_Generated by [Claude Code](https://claude.ai/code)_

---

