# #48 — a fourth lens for prose that negates a removed thing, and `/tend-prose`

Closes #48. Export: `docs/issue/48/issue.md`.

## The defect

A change removes a thing the prose described; the reflex is to **negate the sentence in place** rather than delete it. The mention survives as its own denial — "copy is not a segment", "the mark is not generated" — and every later reader pays for a thing that is not there. The reviewer's idiom: *don't think about the polar bear.*

The current three lenses wave it through. Lens A's tells all point at prose that *describes how the code works*; a sentence about what the code does **not** contain passes each one and reads as a genuine constraint. Lens B has the right instinct — the sentence only serves a reader who remembers the previous draft — but the wrong trigger, since its tells are change verbs ("no longer", "used to") and a negated mention is written in clean present tense.

## Approach: a fourth lens, `negation` (alias `polar-bear`)

The issue leans toward a case under Lens A. This plan takes the other fork, because the structural criteria the skill already uses for what makes a lens all come out the same way:

- **Its own detection input.** Lenses A–C read only the *added* prose lines. This one needs the **removed** side of the diff — the deleted nouns are what you grep the post-change tree for. That is a new sub-step in Step 1, not a new bullet under Lens A.
- **Lens A's own keep-test doesn't fire on it**, as the issue says outright. Folding it in means bolting an escape clause onto a three-part test that the defect passes cleanly — the test stops being one test.
- **"Cuts live in Lens A" doesn't discriminate.** Lens B's fix block already ends in *Delete when the note carried no lasting information*; Lens C's already says *Delete entirely. This is a normal outcome.* Every lens cuts.
- **Single-lens mode is the payoff for the operator's ask.** `polar bear here` on a PR comment wants a targeted pass — `/tend-prose polar-bear` — not the full existence sweep.
- **Its own report group** makes the count visible; folded under `Existence` the signal disappears into the other cuts.

### `negation`, not `absence`

`absence` reads as the **antonym of `existence`**, so a list containing both invites the reader to work out how two opposite-sounding lenses differ before they can use either. `negation` names what the prose does — the issue's own framing, *the sentence survives as its own denial* — and sits at no such angle to the other three. It also avoids a second misreading: a lens called "absence" sounds like it flags **missing** documentation, the opposite of what it finds.

## The rename: `/tighten-docs` → `/tend-prose`

Two things in the old name are wrong, and the fourth lens makes the first one worse:

- **"Tighten" names one of the four lenses.** Tightness is Lens C. Calling the whole pass by it implies trimming is the job, when the skill's own Step 3 says deletion "is the most common outcome and it is a clean one" — and two of the four lenses (existence, negation) produce nothing but deletions. **Tend** covers all four: cut what shouldn't be there, rewrite what narrates, delete what denies, trim what sprawls.
- **"Docs" is not the word this repo uses for what the skill reads.** The skill's own description already says *"Review the prose you added in recent work — code comments, docstrings, and Markdown"*, and `CLAUDE.md` § "Writing things down" opens *"Prose costs context on every session that loads it"*. The name is the outlier, and "docs" actively misdirects toward the `docs/` tree.

The bonus is that **TEND stops being a mnemonic and becomes the name**: Tightness, Existence, Negation, Durability, tended. An acronym that merely spells a word is a peg; one that spells the verb in the skill's own name is a structure.

**This is not the aesthetic swap `CLAUDE.md` § "Key principles" rules out**, and the distinction matters because the same principle is what rejects `PARE` below. `PARE` would rename working lens tokens *to buy an acronym*. This renames a skill whose name became inaccurate when the skill grew a fourth lens — a concrete problem with the name, which is exactly the bar that principle sets.

**Costs, all bounded:**

- 16 references across 8 files, 5 of which this plan already edits. The dangling-pointer risk `CLAUDE.md` warns is **silent** is covered: `scripts/check-skill-catalog.sh` runs inside `./scripts/vet.sh` and asserts both that `@.claude/skills/<name>/SKILL.md` pointers resolve and that every skill has exactly one catalog row. The rename is mechanically guarded, so the vet run is the proof rather than a careful read.
- **Scope.** This grows the PR beyond the issue as filed, but the two are entangled: the name is wrong *because* of the fourth lens, and both edit the same eight files. Splitting means either landing #48 under a name already known to be wrong, or a follow-up PR that walks the same sites again.

**No redirect stub at the old name.** The `/implement` → `/go` precedent does not transfer: `/implement` earned its stub because it appears in **copyable handoff blocks** that `/plan` hands operators verbatim, so the old name kept arriving from outside the repo. This skill is almost never operator-launched — its callers are `/go` Step 3 and `/handle`, which reach it through `@.claude/skills/…` pointers that this plan repoints and `scripts/check-skill-catalog.sh` verifies. The two exposures that remain are both acceptable:

- An operator typing `/tighten-docs` from muscle memory gets "no such skill" — an immediate, legible failure, not silently wrong behaviour.
- Adopting repos port the rename through `/sync-agent-infra`, which triages commit by commit, so the rename lands as a visible commit and their own catalog check catches anything they miss.

Against that, a stub costs a **permanent line in every session's skill list**, since descriptions are always loaded — the standing context tax `CLAUDE.md` § "Writing things down" exists to refuse. `/implement` pays it for a reason; a second stub without one is the kind of prose that should not exist.

**The branch keeps its name.** `claude/48-tighten-docs-polar-bear-1zzzif` is now slightly stale, but renaming a branch that already has a PR closes that PR (`@.claude/skills/branch-rename/SKILL.md` § "Caveat"), and a stale slug is cheaper than a replacement PR over the same diff.

## Keeping the idiom usable as PR shorthand

The operator's ask is that a bare `polar bear` on a PR comment be understood by a `/handle`-ing agent. The mechanism is the **frontmatter `description`**: skill descriptions are loaded into every session's skill list, so the idiom is visible to an agent that has not opened the skill. So the description must carry the word `polar bear` in a form that reads as a routing signal, not just as colour. `CLAUDE.md` § "Writing things down" carries it too, being always-loaded, but the description is what does the work.

## The false-positive this lens must not create

This repo's prose is full of legitimate negative constraints — *"Dev artifacts go under gitignored `tmp/`, not as new `.gitignore` entries"*, *"Never create a new top-level doc"*. Those are constraints, not residue. The discriminator is the issue's test, and it has to be spelled out beside the tells or the lens over-deletes:

> Would a reader who had **never seen the previous version** need this sentence? A constraint answers a temptation that exists independently of the removal. Residue only prevents them from expecting something they had no reason to expect.

## Changes

### 1. `git mv .claude/skills/tighten-docs .claude/skills/tend-prose`

Do the move first, so every later edit lands in the file at its final path.

### 2. `.claude/skills/tend-prose/SKILL.md` — the substance

- **Frontmatter `description`**: extend from three defects to four, name the new one, and carry the `polar bear` idiom. Update the invocation line to `/tend-prose [existence | durability | tightness | negation]`.
- **Intro bullet list** (the three "equal weight" defects): add a fourth bullet — *Negation — text whose subject is a thing the change removed, surviving as its own denial.* Name the TEND acronym here, with the not-the-run-order caveat below.
- **§ "Single-lens mode"**: add `negation` (alias `polar-bear`) to the token list and the example line; change "all three run" to four. Note that `negation` and Durability's existing alias `narration` sit three characters apart, and keep primaries and aliases visually distinct enough in the list that the two never have to be told apart at a glance.
- **§ "When to use"**: add the trigger — the scoped work **removed** a module, file, field or concept that prose described.
- **Step 1**: add the removed-noun sub-step. After the diff range is fixed, collect what the diff deletes — identifiers, file paths, field and type names, named concepts — from removed lines (`git diff <range>`) and deleted files (`git diff --diff-filter=D --name-only <range>`). Grep each against the post-change tree; a name that survives **only inside prose** is a Lens D candidate. State that this sub-step is skipped when the scoped diff removes nothing, so the ordinary additive pass pays nothing for it. Also amend the standing "only added/changed prose lines are in scope" line, which currently forecloses reading the removed side at all.
- **Step 2**: new **Lens D — is it about a thing that isn't there?**, after Lens C. Carries: the grep tell; the negation-without-change-verbs tell (clean present tense, so Lens B misses it); the never-seen-the-previous-version test; and the constraint-vs-residue discriminator above, with a worked pair.
- **Step 3**: new **Negation** fix block. **Delete** is the default and the point — this is not a rewrite lens. The one exception: a mention carrying a live fact alongside the denial keeps the fact, phrased as what *is* there (the issue's `public/aeapp-mark.svg` specimen). **Keep** a genuine negative constraint that passes the discriminator. Restate here that the resolution order is existence-first, not TEND order.
- **Step 5**: add a `Negation (n)` group to the report skeleton; the "all groups always appear, an empty one gets a sentence" rule extends to it unchanged.

Step 4 ("Do NOT touch") needs no edit: commit messages, PR bodies, plans and changelogs are already excluded, and those are exactly where naming a removal is correct.

### 3. `CLAUDE.md` — three repointings

- **§ "Writing things down"**: one line after *"When a convention changes, every place that states it changes with it"*, which covers repointing a citation but not the case where the right move is to stop stating it. Names the idiom so the always-loaded file carries it, and points at the skill as the home. One line, not a restatement of the lens.
- **§ "Writing things down"**, the "Read the long version sparingly" paragraph: repoint `@.claude/skills/tighten-docs/SKILL.md` → `@.claude/skills/tend-prose/SKILL.md`.
- **§ "Working with skills"**, the `/tighten-docs` bullet: rename to `/tend-prose`, and the parenthetical lens list `(existence, durability, tightness)` gains `negation`. Also the "Key principles" bullet on comments describing the lasting contract, which names the skill as the pass that enforces it.

### 4. Citations that name the skill or state the lens count

Adding a lens changes every place that states how many there are, and the rename changes every place that names it — `CLAUDE.md`'s own repointing rule, applied to itself.

- **`.claude/skills/go/SKILL.md`** — the frontmatter description and Step 3 item 2. The latter is already stale: it says `/tighten-docs` "carries **two halves of equal weight**" and reports "`Durability` and `Tightness` groups", against a skill that has had three lenses for some time. Correct it to four lenses and four report groups, under the new name.
- **`.claude/skills/squash-message/SKILL.md`** — says only Lens B is inapplicable to a commit body. Lens D is inapplicable for the same reason: naming what a change removed is a commit message's job. Extend the sentence to both, and repoint the skill name.
- **`.claude/skills/plan/SKILL.md`** and **`.claude/skills/handle/SKILL.md`** — each names the skill once, in a list of consumers and in the lane hand-off respectively. Repoint only.
- **`.claude/skills/sync-agent-infra/SKILL.md`** — names the skill in its Step 8 hand-off. Repoint only.
- **`.claude/skills/sync-agent-infra/catalog.md`** — the `/tighten-docs` row becomes the `/tend-prose` row, with the fourth lens in its summary, and every other row citing the skill in its "composes" column is repointed. The row count is unchanged, so `scripts/check-skill-catalog.sh`'s one-row-per-skill assertion is what catches a half-done rename.
- **`README.md`** — the G1 group row names the skill.

## Verification

- `./scripts/vet.sh` — now genuinely load-bearing rather than a regression check: `scripts/check-skill-catalog.sh` is what proves no `@.claude/skills/…` pointer was left dangling by the move, and that the renamed skill has exactly one catalog row.
- `grep -rn "tighten-docs"` over the tree: **zero** surviving hits outside the working artifacts `/finalize` sweeps (`docs/plans/`, `docs/issue/`, `docs/remove-before-merging/`) and this branch's own name. With no redirect stub, any hit left is a real dangling reference.
- Confirm the four lens names still spell TEND after the final wording pass, and that no site lists only three.
- Self-apply: run the new Lens D over this branch's own diff. The change removes nothing, so the Step 1 sub-step should correctly no-op — which is the cheapest available test that the skip clause reads right.

## DRY notes

- **The lens itself is stated once.** `@.claude/skills/tend-prose/SKILL.md` declares itself "the only home for these rules"; `CLAUDE.md` § "Writing things down" gets a **pointer plus the idiom**, not a copy of the tells or the test. The idiom appears in both places on purpose — it is a routing token, and a token has to be visible where the routing decision is made (the always-loaded file and the skill list) rather than only where it is defined.
- **The TEND acronym has one home**, the skill's intro beside the four bullets. `CLAUDE.md`'s lens list stays a bare enumeration — spelling the acronym out in the always-loaded file would be a second copy of a memory aid that costs context on every session and informs none of them.
- **The old name gets no second home.** Declining the redirect stub is a DRY call as much as a context one: a stub is a file whose whole content is a pointer to another skill, and every such file is one more thing that can fall out of step with what it points at. `/implement` accepts that cost because copyable handoff blocks keep sending operators the old name; nothing sends them this one.
- **No extraction is warranted for the four-lens structure.** Each lens's tells and fixes are prose in one file; there is no shared mechanism to factor. Lens D reuses the existing Step 1 scope, Step 3 fix-block shape, and Step 5 report shape rather than introducing a parallel structure — which is the whole reason to add it as a lens rather than as a free-standing check.
- **The citation sites are citations, not duplicates.** `/go`, `/squash-message`, `/plan`, `/handle`, `/sync-agent-infra`, `catalog.md` and `README.md` each name the skill for a local purpose. Collapsing them into a single reference would make each read worse at its own call site; keeping them in sync is what `CLAUDE.md`'s repointing rule already asks for, and this plan does it.
- **The removed-noun collection is a procedure, not a script.** It could be a `scripts/` helper, but the noun list needs judgement at every step (which deleted identifiers are *concepts* the prose named), so a script would produce a list a human still has to filter. Prose in Step 1 is the right level.

## Resolved: the lens name and the acronym

`negation` was chosen over `absence`, `imprint`/`imaginary`/`illusion`, and a `permanence`/`restraint` pair, for the reasons in § "`negation`, not `absence`" and § "The rename". What the rejected options cost: `absence` spells DATE, a word that describes nothing the skill does, and reads as `existence`'s antonym; the `I`-names spell EDIT, the best word available, but every occupant of that slot is either vaguer than `negation` (`imprint`) or implies the prose is inaccurate when its defect is being accurate and useless (`imaginary`, `illusion`); `permanence` + `restraint` spells PARE, whose meaning is exact, but it renames two working lens tokens purely to buy an acronym.

## Open questions

Carries a recommendation, and this plan is written with the recommendation in force — so silence is a valid resolution and the plan is implementable as it stands.

**1. Fourth lens, or a case under Lens A?**
- **(a) — recommended, and what this plan implements.** A fourth lens `negation` (alias `polar-bear`), with its own single-lens token, tells, fix block and report group. Reasons in § "Approach".
- (b) A named case under Lens A, as the issue leans. Keeps "three equal defects" intact across `CLAUDE.md`, `/go`, `README.md` and the catalog — but needs an escape clause bolted onto Lens A's three-part keep-test, loses single-lens invocability for the operator's `polar bear here` shorthand, buries the count in the `Existence` group, and gives up both the acronym and the rename that follows from it.
