> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #48 — a `/tighten-docs` lens for prose that negates a removed thing

Closes #48. Export: `docs/issue/48/issue.md`.

## The defect

A change removes a thing the prose described; the reflex is to **negate the sentence in place** rather than delete it. The mention survives as its own denial — "copy is not a segment", "the mark is not generated" — and every later reader pays for a thing that is not there. The reviewer's idiom: *don't think about the polar bear.*

The current three lenses wave it through. Lens A's tells all point at prose that *describes how the code works*; a sentence about what the code does **not** contain passes each one and reads as a genuine constraint. Lens B has the right instinct — the sentence only serves a reader who remembers the previous draft — but the wrong trigger, since its tells are change verbs ("no longer", "used to") and a negated mention is written in clean present tense.

## Approach: a fourth lens, `absence` (alias `polar-bear`)

The issue leans toward a case under Lens A. This plan takes the other fork, because the structural criteria the skill already uses for what makes a lens all come out the same way:

- **Its own detection input.** Lenses A–C read only the *added* prose lines. This one needs the **removed** side of the diff — the deleted nouns are what you grep the post-change tree for. That is a new sub-step in Step 1, not a new bullet under Lens A.
- **Lens A's own keep-test doesn't fire on it**, as the issue says outright. Folding it in means bolting an escape clause onto a three-part test that the defect passes cleanly — the test stops being one test.
- **"Cuts live in Lens A" doesn't discriminate.** Lens B's fix block already ends in *Delete when the note carried no lasting information*; Lens C's already says *Delete entirely. This is a normal outcome.* Every lens cuts.
- **Single-lens mode is the payoff for the operator's ask.** `polar bear here` on a PR comment wants a targeted pass — `/tighten-docs polar-bear` — not the full existence sweep.
- **Its own report group** makes the count visible; folded under `Existence` the signal disappears into the other cuts.

Naming follows the established pattern exactly: the primary token names the dimension (`existence`, `durability`, `tightness` → `absence`), the alias names the defect (`narration`, `bloat` → `polar-bear`).

## Keeping the idiom usable as PR shorthand

The operator's ask is that a bare `polar bear` on a PR comment be understood by a `/handle`-ing agent. The mechanism is the **frontmatter `description`**: skill descriptions are loaded into every session's skill list, so the idiom is visible to an agent that has not opened the skill. So the description must carry the word `polar bear` in a form that reads as a routing signal, not just as colour. `CLAUDE.md` § "Writing things down" carries it too, being always-loaded, but the description is what does the work.

## The false-positive this lens must not create

This repo's prose is full of legitimate negative constraints — *"Dev artifacts go under gitignored `tmp/`, not as new `.gitignore` entries"*, *"Never create a new top-level doc"*. Those are constraints, not residue. The discriminator is the issue's test, and it has to be spelled out beside the tells or the lens over-deletes:

> Would a reader who had **never seen the previous version** need this sentence? A constraint answers a temptation that exists independently of the removal. Residue only prevents them from expecting something they had no reason to expect.

## Changes

### 1. `.claude/skills/tighten-docs/SKILL.md` — the substance

- **Frontmatter `description`**: extend from three defects to four, name the new one, and carry the `polar bear` idiom. Update the invocation line to `[existence | durability | tightness | absence]`.
- **Intro bullet list** (the three "equal weight" defects): add a fourth bullet — *Absence — text whose subject is a thing the change removed, surviving as its own denial.*
- **§ "Single-lens mode"**: add `absence` (alias `polar-bear`) to the token list and the example line; change "all three run" to four.
- **§ "When to use"**: add the trigger — the scoped work **removed** a module, file, field or concept that prose described.
- **Step 1**: add the removed-noun sub-step. After the diff range is fixed, collect what the diff deletes — identifiers, file paths, field and type names, named concepts — from removed lines (`git diff <range>`) and deleted files (`git diff --diff-filter=D --name-only <range>`). Grep each against the post-change tree; a name that survives **only inside prose** is a Lens D candidate. State that this sub-step is skipped when the scoped diff removes nothing, so the ordinary additive pass pays nothing for it. Also amend the standing "only added/changed prose lines are in scope" line, which currently forecloses reading the removed side at all.
- **Step 2**: new **Lens D — is it about a thing that isn't there?**, after Lens C. Carries: the grep tell; the negation-without-change-verbs tell (clean present tense, so Lens B misses it); the never-seen-the-previous-version test; and the constraint-vs-residue discriminator above, with a worked pair.
- **Step 3**: new **Absence** fix block. **Delete** is the default and the point — this is not a rewrite lens. The one exception: a mention carrying a live fact alongside the denial keeps the fact, phrased as what *is* there, and drops the denial (the issue's `public/aeapp-mark.svg` specimen). **Keep** a genuine negative constraint that passes the discriminator.
- **Step 5**: add an `Absence (n)` group to the report skeleton; the "all groups always appear, an empty one gets a sentence" rule extends to it unchanged.

Step 4 ("Do NOT touch") needs no edit: commit messages, PR bodies, plans and changelogs are already excluded, and those are exactly where naming a removal is correct.

### 2. `CLAUDE.md` — two repointings

- **§ "Writing things down"**: one line after *"When a convention changes, every place that states it changes with it"*, which covers repointing a citation but not the case where the right move is to stop stating it. Names the idiom so the always-loaded file carries it, and points at the skill as the home. One line, not a restatement of the lens.
- **§ "Working with skills"**, the `/tighten-docs` bullet: the parenthetical lens list `(existence, durability, tightness)` gains `absence`.

### 3. Citations that state the lens count

Adding a lens changes every place that states how many there are — CLAUDE.md's own rule.

- **`.claude/skills/go/SKILL.md:85`** — already stale: says `/tighten-docs` "carries **two halves of equal weight**" and reports "`Durability` and `Tightness` groups", against a skill that has had three lenses for some time. Correct it to the current four and the four report groups.
- **`.claude/skills/squash-message/SKILL.md:204`** — says only Lens B is inapplicable to a commit body. Lens D is inapplicable for the same reason: naming what a change removed is a commit message's job. Extend the sentence to both.
- **`.claude/skills/sync-agent-infra/catalog.md:115`** — the `/tighten-docs` row's summary describes the three lenses; add the fourth so the inventory doesn't drift. (`scripts/check-skill-catalog.sh` asserts the row exists, not its wording, so this is correctness rather than a check failing.)

`README.md:19` names the skill without describing its lenses — no change.

## Verification

- `./scripts/vet.sh` (runs `scripts/check-skill-catalog.sh`; no skill added or renamed, so this is a regression check).
- Read the four `@.claude/skills/tighten-docs/SKILL.md` citation sites back and confirm none still says "three" or "two halves".
- Self-apply: run the new Lens D over this branch's own diff. The change removes nothing, so the Step 1 sub-step should correctly no-op — which is the cheapest available test that the skip clause reads right.

## DRY notes

- **The lens itself is stated once.** `@.claude/skills/tighten-docs/SKILL.md` declares itself "the only home for these rules"; `CLAUDE.md` § "Writing things down" gets a **pointer plus the idiom**, not a copy of the tells or the test. The idiom appears in both places on purpose — it is a routing token, and a token has to be visible where the routing decision is made (the always-loaded file and the skill list) rather than only where it is defined.
- **No extraction is warranted for the four-lens structure.** Each lens's tells and fixes are prose in one file; there is no shared mechanism to factor. Lens D reuses the existing Step 1 scope, Step 3 fix-block shape, and Step 5 report shape rather than introducing a parallel structure — which is the whole reason to add it as a lens rather than as a free-standing check.
- **Sites 3 are citations, not duplicates.** `/go`, `/squash-message` and `catalog.md` each state the lens count or list for a local purpose (what a caller runs, which lens applies to a commit body, what the inventory row says). Collapsing them into a single reference would make each read worse at its own call site; keeping them in sync is what CLAUDE.md's repointing rule already asks for, and this plan does it.
- **The removed-noun collection is a procedure, not a script.** It could be a `scripts/` helper, but the noun list needs judgement at every step (which deleted identifiers are *concepts* the prose named), so a script would produce a list a human still has to filter. Prose in Step 1 is the right level.

## Open questions

Both carry a recommendation, and this plan is written with the recommendation in force — so silence is a valid resolution and the plan is implementable as it stands.

**1. Fourth lens, or a case under Lens A?**
- **(a) — recommended, and what this plan implements.** A fourth lens `absence` (alias `polar-bear`), with its own single-lens token, tells, fix block and report group. Reasons in § "Approach".
- (b) A named case under Lens A, as the issue leans. Keeps "three equal defects" intact across `CLAUDE.md`, `/go`, `README.md` and the catalog — but needs an escape clause bolted onto Lens A's three-part keep-test, loses single-lens invocability for the operator's `polar bear here` shorthand, and buries the count in the `Existence` group.

**2. Primary token name.**
- **(a) `absence` — recommended.** Matches the existing primaries, which name the dimension (`existence`, `durability`, `tightness`) and leave the defect to the alias (`narration`, `bloat`, → `polar-bear`).
- (b) `residue` as primary. More vivid about what the prose *is*, but it names the defect, so it belongs in the alias slot the idiom already occupies.
- (c) `polar-bear` as the primary token, with no abstract name. Maximally memorable and the operator's own word — but it is the only lens name that means nothing until you have heard the story, which is a bad property for the token that appears in the frontmatter's invocation line.
