# PR #57: feat: #48 add a negation lens and rename the pass /tend-prose

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/57
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/48-tighten-docs-polar-bear-1zzzif
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-10T21:41:45Z
- **Updated:** 2026-09-11T01:13:07Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The defect.** When a change removes a thing the prose described, the reflex is to negate the sentence in place rather than delete it. The mention survives as its own denial — "copy is not a segment", "the mark is not generated" — and every later reader pays for a thing that is not there. The reviewer's idiom: *don't think about the polar bear.*
- **Why the existing lenses miss it.** The existence lens's tells all point at prose that *describes how the code works*, which a sentence about what the code does **not** contain passes cleanly — it even reads as a genuine constraint. The durability lens has the right instinct (the sentence only serves a reader who remembers the previous draft) but the wrong trigger, since its tells are change verbs and a negated mention is written in clean present tense.
- **A fourth lens, `negation`** (alias `polar bear`), rather than the issue's lean toward a case under the existence lens. It is the only lens that reads the **removed** side of the diff: a new Step 1 sub-step collects the nouns the change deleted and greps them against the post-change tree, and a name surviving only inside prose is the candidate. The sub-step is skipped when the diff removes nothing, so additive work pays nothing for the lens. Step 3's fix is deletion, with an exception for a mention carrying a live fact.
- **The test is whether the sentence is what put the subject in the reader's head** — with it gone, would the subject have crossed their mind at all? That framing is mechanically checkable and is the polar bear itself, where "would a reader need this sentence" invites an argument about need.
- **Guards against over-deletion.** This repo's prose is full of legitimate negative constraints, so the lens carries a constraint-vs-residue discriminator with a worked pair: a constraint's subject is something the reader reaches for anyway, so it crosses their mind with or without the sentence.
- **The four lenses spell TEND** — Tightness, Existence, Negation, Durability — and the skill's intro lists them in that order. With the three shipped names fixed, the fourth letter was the only free one, and `N` the only choice yielding a word that describes the pass. `negation` is also the better name on its own: it is the issue's framing, and unlike `absence` it does not read as `existence`'s antonym, which would make two of four lenses sound like opposites in one list. TEND is the memory aid; the run order is existence-first and the skill says so where it names the acronym.
- **The lenses are numbered 1–4, not lettered.** `A`–`D` read as the initials of TEND, so "lens D" was ambiguous between the fourth lens and durability. The numbers are the order Step 2's sections come in, and spell nothing.
- **The pass no longer reports.** Step 5 is the commit alone. A per-lens count of what was fixed gave the operator nothing to act on, and the edits — plus the commit body that carries their reasons — are what outlives the session. `/go` stops describing the pass on its behalf for the same reason: it loads the skill and runs the full sweep, and the agent gets the rest from the skill.
- **`/tighten-docs` becomes `/tend-prose`.** The old name was wrong twice over, and the fourth lens made the first worse: "tighten" names one lens specifically, though two of the four produce nothing but deletions; and "docs" is not the word the skill's own description or `CLAUDE.md` uses for what it reads — both already say *prose*. **No redirect stub** — the `/implement` → `/go` precedent doesn't transfer, since `/implement` earned its stub by appearing in copyable handoff blocks, whereas this pass is reached through `@.claude/skills/…` pointers from `/go` and `/handle` that this PR repoints. A stub would cost a permanent line in every session's skill list to serve a mistyping that already fails legibly.
- **Repoints every site that names the skill or counts its lenses** — 16 references across 8 files. `/go`'s Step 3 was already stale before this change (it described "two halves" and two report groups against a three-lens skill) and now names neither, pointing at the skill instead, since a copy of that list is what went stale. `/squash-message` **claims** the negation lens rather than excusing itself from it: a body drafted while the branch still did some non-obvious thing, and kept after the branch dropped it, denies something no reader of the squashed commit would have raised — the lens reaches a squash body through the stale draft, not the diff. Only narration stays inapplicable there, narrating the change being a commit message's job. `CLAUDE.md` § "Writing things down" gains the convention its repointing rule doesn't cover — when a convention goes away, stop stating it rather than negating it in place — and carries the idiom so the always-loaded file holds the routing token.
- **The lens caught two polar bears in this PR's own diff.** `/go` Step 3 justified not enumerating the lenses by pointing at the enumeration this branch had just deleted (`14f8c30`; the clause is gone entirely now). And the new lens table denied a mapping between the numbers and the TEND bullets that only the discarded letters ever invited (`19f0a7f`). Both were subjects no later reader would have raised.

## QA Checklist

- [ ] `description-carries-idiom` — open a fresh session and check the skill list: the `/tend-prose` description names the polar-bear idiom, so an agent that has not opened the skill can route a bare `polar bear here` PR comment to it
- [ ] `single-lens` — run `/tend-prose negation` and `/tend-prose polar bear` on a branch; confirm only that lens runs
- [ ] `no-report` — run the full `/tend-prose` and confirm it ends at the commit: edits applied, reasons in the commit body, no per-lens tally printed into the session
- [ ] `negation-in-squash` — draft a squash body for a branch that dropped a scope item mid-flight, and confirm `/squash-message` cuts the sentence denying the dropped thing rather than keeping it as a decision record
- [ ] `removed-noun-step` — run the full `/tend-prose` on a branch whose diff **deletes** a module or field, and confirm Step 1 produces the removed-noun list and greps it against the post-change tree
- [ ] `no-op-skip` — run the full `/tend-prose` on a purely additive branch and confirm the removed-noun sub-step skips instead of grepping an empty list. Not exercised on this branch: the rename makes this diff a removing one, so the sub-step ran (see `self-applied` below)
- [ ] `self-applied` — the pass ran over this branch's own diff. The removed nouns were `tighten-docs`, "three lenses" and "two halves of equal weight"; each survives only in the working artifacts `/finalize` sweeps. It found one live polar bear in `/go` Step 3, which is fixed in `14f8c30`
- [ ] `constraint-survives` — point the lens at `CLAUDE.md`'s own negative constraints (dev artifacts go in `tmp/`, never create a top-level doc) and confirm the discriminator keeps them
- [ ] `live-fact-exception` — check a negated mention that carries a real fact is rewritten to state the fact positively, not deleted wholesale
- [ ] `citations-consistent` — `grep -rn "tighten-docs"` yields **zero** hits outside the working artifacts `/finalize` sweeps and this branch's own name; with no redirect stub, anything left is a real dangling reference. No site outside those artifacts still says "three lenses", "two halves of equal weight", or `Lens A`–`Lens D`
- [ ] `vet` — `./scripts/vet.sh` passes, including `scripts/check-skill-catalog.sh`

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `description-carries-idiom` | manual-only | — | Whether an agent recognizes the idiom from the description alone is a judgment call |
| `single-lens` | manual-only | — | Requires running the skill and judging which lens it applied |
| `no-report` | manual-only | — | Observable only by running the pass |
| `negation-in-squash` | manual-only | — | Needs a branch that dropped a scope item after its draft was written |
| `removed-noun-step` | manual-only | ✅ | Ran on this branch's own diff; candidates all resolved to swept artifacts |
| `no-op-skip` | manual-only | — | Needs an additive branch; this one removes |
| `self-applied` | manual-only | ✅ | `14f8c30` |
| `constraint-survives` | manual-only | — | The discriminator is a judgment call by construction |
| `live-fact-exception` | manual-only | — | Same |
| `citations-consistent` | unit | ✅ | `scripts/check-skill-catalog.sh` passes; grep is clean. The "three lenses" wording has no harness |
| `vet` | unit | — | `/finalize`'s step 1 |

Closes #48

https://claude.ai/code/session_01C7JZwFRWDumnfueoRuk4Ax

---
_Generated by [Claude Code](https://claude.ai/code)_

---

## Comments

### Comment by @vzakharov on 2026-09-10T21:42:19Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/57#issuecomment-5625831053](https://github.com/vzakharov/agent-project-boilerplate/pull/57#issuecomment-5625831053)

Proposed squash title/body:

```
feat: #48 add a negation lens and rename the pass /tend-prose (pr #57)
```

```
When a change removes something the prose described, the reflex is to
negate the sentence in place rather than delete it, and the mention
survives as its own denial. Every later reader then pays for a thing
that is not there. The existing lenses sit either side of the defect:
the existence lens's tells all point at prose describing how the code
works, which a sentence about what the code does not contain passes
cleanly, and the durability lens's tells are change verbs that a clean
present-tense negation never trips.

The pass gains a fourth lens, `negation` (alias `polar bear`), with its
own tell, test and fix. It is the only lens that reads the removed side
of the diff: Step 1 collects the nouns the change deleted and greps them
against the post-change tree, and a name surviving only inside prose is
the candidate. The fix is deletion, except where a mention carries a
live fact alongside the denial — the fact then stays, phrased as what
is there. The test asks whether the sentence is what put its subject in
the reader's head: with it gone, would the subject have crossed their
mind at all? A constraint's subject would, which is what keeps the lens
off the legitimate negative rules a codebase is full of.

`/tighten-docs` becomes `/tend-prose`, whose four lenses spell TEND —
Tightness, Existence, Negation, Durability — as a memory aid, not the
run order. The old name was wrong twice over: "tighten" named one lens
specifically, though two of the four produce nothing but deletions, and
"docs" was never the word the skill or CLAUDE.md used for what it reads.
No redirect stub holds the old name: the pass is reached through skill
pointers rather than typed, so every caller is repointed and the catalog
check proves it. The polar-bear idiom sits in the frontmatter
description, which every session loads, so an agent that has not opened
the skill still resolves a bare "polar bear here" on a PR comment to the
pass that handles it.

The pass also stops printing a per-lens report at the end of a run. The
counts gave the operator nothing to act on; the edits and the commit
body that carries their reasons are what outlives the session.

Closes #48

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `.claude/skills/go/SKILL.md`:85 — resolved

```diff
@@ -82,7 +82,7 @@ Commit/push discipline is already governed by CLAUDE.md — don't reinvent it he
 These run **every time**, in order, and override any contrary "wrap up after implementing" instinct. Each is a real pass over the just-written diff, not a rubber stamp — and each commits its own edits.
 
 1. **`/dry`** — did new duplication the plan didn't foresee creep in during implementation? Plans are written before the code exists, so WETness that wasn't visible at planning time often surfaces only now. Load `@.claude/skills/dry/SKILL.md` and run it over this session's diff: apply the obvious wins, surface the ambiguous calls.
-2. **`/tighten-docs`** — load `@.claude/skills/tighten-docs/SKILL.md` and run it over the prose you added. It carries **two halves of equal weight**: rewriting edit-narration into present-tense contracts, and cutting prose back to the non-obvious contract at the length that contract takes. Its report is split into `Durability` and `Tightness` groups. Commit this pass's edits.
+2. **`/tend-prose`** — load `@.claude/skills/tend-prose/SKILL.md` and run it over the prose you added. Its lenses carry **equal weight** and it reports a group per lens. Don't enumerate them here — a copy of that list goes stale the next time a lens is added, and this caller has no way to notice. Run the full sweep rather than naming one. Commit this pass's edits.
```

**@vzakharov** — 2026-09-11T00:42:04Z

acually... I don't think the reporting part is needed; it's not that it gives the operator anything actionable. Let's ride along removing the report.

Also, ironically, I think we describe what the skill does here, the agent will get what they need in the skill itself.

**@vzakharov** — 2026-09-11T00:59:18Z

Done — both halves. The report is gone from the skill (Step 5 is now just the commit), and this item no longer says anything about what the pass does: load it, run the full sweep. The "don't enumerate the lenses here" warning went too — it was itself a description of the skill, kept alive by a mistake that is no longer in the tree. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/squash-message/SKILL.md`:207 — resolved

```diff
@@ -201,10 +201,11 @@ intermediate steps and "added a test for it"; process meta; benefit padding; and
 the linked issue's own symptom and repro re-filed here, which `Closes #N` already
 points at.
 
-This is `@.claude/skills/tighten-docs/SKILL.md`'s **Lens A (existence)** and
-**Lens C (bloat)** applied to a commit body. Only its Lens B (narration) is
-inapplicable — narrating the change is a commit message's whole job, which is why
-that skill's Step 4 excludes commit messages and PR bodies from its own sweep.
+This is `@.claude/skills/tend-prose/SKILL.md`'s **Lens A (existence)** and
+**Lens C (bloat)** applied to a commit body. Its Lens B (narration) and Lens D
+(negation) are both inapplicable, for one reason: naming what the change did and
+what it took away is a commit message's whole job. That is why that skill's Step
```

**@vzakharov** — 2026-09-11T00:43:17Z

I wouldn't say so for negation. A usual case is: we decide to do something non-obvious (the polar bear), the agent writes a squash message, then we decide to NOT do something, it negates that something no one would've thought of if it wasn't there in the first place -- exactly the case we want to avoid

**@vzakharov** — 2026-09-11T00:59:19Z

You're right, and the case you describe is sharper than anything in the skill — the draft is written while the branch still does the non-obvious thing, and survives the decision to drop it. So the squash body carries a bear the diff can't show.

Rewrote it: lenses 1, 3 and 4 apply to a commit body, only lens 2 (narration) is inapplicable, plus a short paragraph on how lens 4 reaches a squash body through the stale draft rather than the diff. `/tend-prose` Step 4 still excludes commit bodies from its own sweep — `/squash-message` is where that pass lives, and it's loaded whenever a body is written. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/tend-prose/SKILL.md`:14 — resolved

```diff
@@ -1,32 +1,45 @@
 ---
 description: >-
   Review the prose you added in recent work — code comments, docstrings, and
-  Markdown — against three equal defects: it should not exist at all (a
+  Markdown — against four equal defects: it should not exist at all (a
   description of how the code works, recoverable by reading it, or written
   somewhere nothing reaches), it narrates the change instead of stating the
   code's lasting contract ("no longer parsed", "now also sets X", "migrated from
-  Y"), and it spends more words than it informs — restating what the name,
-  signature, and types already say, or stretching a real point over four lines.
-  Rewrites, moves and cuts in place. Invoke as: /tighten-docs [existence |
-  durability | tightness] [optional focus guidance] — naming one lens runs only
-  that lens.
+  Y"), it spends more words than it informs — restating what the name,
+  signature, and types already say, or stretching a real point over four lines —
+  and it denies a thing the change removed, so the mention survives as its own
+  denial ("copy is not a catalogue"). That last one is the **polar bear**: a bare
+  "polar bear here" on a PR comment asks for this pass. Rewrites, moves and cuts
+  in place. Invoke as: /tend-prose [existence | durability | tightness |
+  negation] [optional focus guidance] — naming one lens runs only that lens.
```

**@vzakharov** — 2026-09-11T00:45:07Z

ironically, I think this can be tightened

**@vzakharov** — 2026-09-11T00:59:27Z

Tightened. Each defect is now named by its lens token with one clause of gloss instead of a parenthetical of examples, which also makes the invocation's argument list redundant — so that collapsed to `[lens]` too. 14 lines to 10, and the polar-bear routing token stays. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/tend-prose/SKILL.md`:31 — resolved

```diff
@@ -1,32 +1,45 @@
 ---
 description: >-
   Review the prose you added in recent work — code comments, docstrings, and
-  Markdown — against three equal defects: it should not exist at all (a
+  Markdown — against four equal defects: it should not exist at all (a
   description of how the code works, recoverable by reading it, or written
   somewhere nothing reaches), it narrates the change instead of stating the
   code's lasting contract ("no longer parsed", "now also sets X", "migrated from
-  Y"), and it spends more words than it informs — restating what the name,
-  signature, and types already say, or stretching a real point over four lines.
-  Rewrites, moves and cuts in place. Invoke as: /tighten-docs [existence |
-  durability | tightness] [optional focus guidance] — naming one lens runs only
-  that lens.
+  Y"), it spends more words than it informs — restating what the name,
+  signature, and types already say, or stretching a real point over four lines —
+  and it denies a thing the change removed, so the mention survives as its own
+  denial ("copy is not a catalogue"). That last one is the **polar bear**: a bare
+  "polar bear here" on a PR comment asks for this pass. Rewrites, moves and cuts
+  in place. Invoke as: /tend-prose [existence | durability | tightness |
+  negation] [optional focus guidance] — naming one lens runs only that lens.
 ---
 
 You are reviewing prose _you_ recently added — code comments, docstrings, and
-Markdown (skill bodies, `docs/`, READMEs) — for three defects that carry
+Markdown (skill bodies, `docs/`, READMEs) — for four defects that carry
 **equal weight**:
 
-- **Existence** — text that should not have been written: a description of how
+- **T**ightness — text that spends more words than it informs: it
+  restates what the function name, signature, and types already convey, or
+  stretches a real point past the length it needs. CLAUDE.md's docstring rule:
+  document only the non-obvious contract (side effects, runtime constraints,
+  cross-boundary coupling, don't-change-this traps).
+- **E**xistence — text that should not have been written: a description of how
   the code works rather than a constraint on it, something a reader recovers from
   the code itself, or a real constraint filed where nothing will load it.
-- **Narration** — text that describes the change relative to the previous
-  intra-PR step rather than the code's durable behaviour. CLAUDE.md: "Comments
-  describe the code's lasting contract, not the change that produced it."
-- **Bloat** — text that spends more words than it informs: it restates what the
-  function name, signature, and types already convey, or stretches a real point
-  past the length it needs. CLAUDE.md's docstring rule: document only the
-  non-obvious contract (side effects, runtime constraints, cross-boundary
-  coupling, don't-change-this traps).
+- **N**egation — text whose subject is a thing the change
+  removed, surviving as its own denial: "copy is not a catalogue", "the mark is
+  not generated". It is written in clean present tense, so it reads as a
```

**@vzakharov** — 2026-09-11T00:46:24Z

I think the examples make it more confusing than without them here. let's leave this for the detailed description. "surviving as its own denial instead of being removed altogether" would do

**@vzakharov** — 2026-09-11T00:59:28Z

Used your phrasing verbatim. The examples live in the Lens 4 section, which is where a reader who wants them is already going. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/tend-prose/SKILL.md`:65 — unresolved

```diff
@@ -36,19 +49,35 @@ home for these rules.
 
 ## Single-lens mode
 
-The argument may **name one lens** — `existence`, `durability` (alias
-`narration`), or `tightness` (alias `bloat`) — optionally followed by focus
-guidance: `/tighten-docs durability`, `/tighten-docs tightness src/db`.
-Then run **only** that lens: skip the other two in Step 2, apply only its fixes
+The argument may **name one lens**, optionally followed by focus guidance:
+`/tend-prose durability`, `/tend-prose tightness src/db`, `/tend-prose polar
+bear`.
+
+| Lens | Primary      | Alias         |
+| ---- | ------------ | ------------- |
+| A    | `existence`  | —             |
+| B    | `durability` | `narration`   |
+| C    | `tightness`  | `bloat`       |
+| D    | `negation`   | `polar bear`  |
+
+`negation` and `narration` are three characters apart and name **different**
+lenses — say `polar bear` for D, which is how the request arrives from a PR
+comment anyway.
```

**@vzakharov** — 2026-09-11T00:47:58Z

what is this supposed to mean? who is "say" addressed to?

**@vzakharov** — 2026-09-11T00:59:29Z

It was addressed to nobody, which is the actual defect — the skill talks to the agent, and the agent parses whatever argument arrives rather than choosing a word for it. Whoever "say" could have meant (you, writing the PR comment) isn't reading this file.

Now it's an instruction the agent can act on: the two tokens name different lenses, 2 and 4, so read the argument against the table rather than from memory. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

**@vzakharov** — 2026-09-11T01:04:27Z

I still don't understand, sorry: why is it supposed to read arguments at all? I'm not sure the paragraph survives existence check. Maybe it's even a polar bear.

---

### `.claude/skills/tend-prose/SKILL.md`:61 — resolved

```diff
@@ -36,19 +49,35 @@ home for these rules.
 
 ## Single-lens mode
 
-The argument may **name one lens** — `existence`, `durability` (alias
-`narration`), or `tightness` (alias `bloat`) — optionally followed by focus
-guidance: `/tighten-docs durability`, `/tighten-docs tightness src/db`.
-Then run **only** that lens: skip the other two in Step 2, apply only its fixes
+The argument may **name one lens**, optionally followed by focus guidance:
+`/tend-prose durability`, `/tend-prose tightness src/db`, `/tend-prose polar
+bear`.
+
+| Lens | Primary      | Alias         |
+| ---- | ------------ | ------------- |
+| A    | `existence`  | —             |
+| B    | `durability` | `narration`   |
+| C    | `tightness`  | `bloat`       |
+| D    | `negation`   | `polar bear`  |
```

**@vzakharov** — 2026-09-11T00:48:36Z

having letters A-B-C-D conflicting with T-E-N-D is confusing (is D for the last one in the list, or for Durability?). let's use lens 1/2/3/4 instead

**@vzakharov** — 2026-09-11T00:59:39Z

Renumbered 1–4 throughout — the table, the Step 2 headings, the cross-references, the resolve order (1, 4, 2, 3), and `/squash-message`'s citations. The numbers are Step 2's section order, so the only list that spells anything is the TEND one, and nothing collides with it. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/tend-prose/SKILL.md`:319 — resolved

```diff
@@ -226,14 +318,17 @@ sentence.
 
 ## Step 5: Report + commit
```

**@vzakharov** — 2026-09-11T00:52:35Z

as clarified above, reporting in the session is not needed (let's see if you'll add a polar bear here;-)

including the report in the commit body is fine ofc but I guess the agent would anyway

**@vzakharov** — 2026-09-11T00:59:40Z

Report gone — Step 5 is the commit, and single-lens mode no longer promises a group.

On the bait: the sentence that could have been the bear is the intro's **"The output is edits, not a report"**, and I kept it deliberately. It passes the discriminator: an agent told to *review* prose reaches for a report whether or not a report step ever existed here, so it guards a live temptation rather than answering a deleted draft. Residue is the sentence nobody would have thought of without it.

I did catch one of my own in the same pass, though. I had written that the new lens numbers "have nothing to do with the TEND bullets above" — which denies a mapping that only the letters ever invited, and the letters are what this commit removes. Cut to the positive half: the numbers are Step 2's section order. 19f0a7f

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/go/SKILL.md`:85 — unresolved

```diff
@@ -82,7 +82,7 @@ Commit/push discipline is already governed by CLAUDE.md — don't reinvent it he
 These run **every time**, in order, and override any contrary "wrap up after implementing" instinct. Each is a real pass over the just-written diff, not a rubber stamp — and each commits its own edits.
 
 1. **`/dry`** — did new duplication the plan didn't foresee creep in during implementation? Plans are written before the code exists, so WETness that wasn't visible at planning time often surfaces only now. Load `@.claude/skills/dry/SKILL.md` and run it over this session's diff: apply the obvious wins, surface the ambiguous calls.
-2. **`/tend-prose`** — load `@.claude/skills/tend-prose/SKILL.md` and run it over the prose you added. Its lenses carry **equal weight** and it reports a group per lens. Don't enumerate them here — a copy of that list goes stale the next time a lens is added, and this caller has no way to notice. Run the full sweep rather than naming one. Commit this pass's edits.
+2. **`/tend-prose`** — load `@.claude/skills/tend-prose/SKILL.md` and run it over the prose you added, as a full sweep rather than a single named lens.
```

**@vzakharov** — 2026-09-11T01:05:17Z

> as a full sweep rather than a single named lens.

polar bear (lol)

---

### `.claude/skills/squash-message/SKILL.md`:215 — unresolved

```diff
@@ -201,13 +201,18 @@ intermediate steps and "added a test for it"; process meta; benefit padding; and
 the linked issue's own symptom and repro re-filed here, which `Closes #N` already
 points at.
 
-This is `@.claude/skills/tend-prose/SKILL.md`'s **Lens A (existence)** and
-**Lens C (bloat)** applied to a commit body. Its Lens B (narration) and Lens D
-(negation) are both inapplicable, for one reason: naming what the change did and
-what it took away is a commit message's whole job. That is why that skill's Step
-4 excludes commit messages and PR bodies from its own sweep.
-
-Four things a draft reaches for fail Lens A, however well written:
+This is `@.claude/skills/tend-prose/SKILL.md`'s **lens 1 (existence)**, **lens 3
+(bloat)** and **lens 4 (negation)** applied to a commit body. Only its lens 2
+(narration) is inapplicable — narrating the change is a commit message's whole
+job, which is why that skill's Step 4 excludes commit messages and PR bodies from
+its own sweep.
+
+**Lens 4 reaches a squash body through the draft, not the diff.** A branch that
+tried something non-obvious and then dropped it leaves a draft written while the
+thing was still there; kept, the body denies something no reader of the squashed
+commit would otherwise have considered, and the log carries that bear forever.
+
+Four things a draft reaches for fail lens 1, however well written:
```

**@vzakharov** — 2026-09-11T01:08:41Z

let's mention lenses by names not numbers here and, by the way, I believe Durability applies here too: 
1- we did something 
2- we put it in the squash message
3- we changed ti
4- we put "changed this to that" in the squash message, instead of just saying what it became ultimately

I think it also reveals a defect in our definition of Durability, because it can have two interpretations: a) describing something added *along the way*, b) describing a change against a previous state.

In the skill we only describe a), but sometimes (not in a squash message) b) is a defect too: for example, you introduce a PR, and it changes smth, and the docstrings say "this does now that". Interestingly, the skill has been working fine for weeding those out all along -- I'm guessing its description somewhere mentions that without noticing the mismatch between the two sublenses of durability.

---

### `.claude/skills/tend-prose/SKILL.md`:9 — unresolved

```diff
@@ -1,17 +1,14 @@
 ---
 description: >-
   Review the prose you added in recent work — code comments, docstrings, and
-  Markdown — against four equal defects: it should not exist at all (a
-  description of how the code works, recoverable by reading it, or written
-  somewhere nothing reaches), it narrates the change instead of stating the
-  code's lasting contract ("no longer parsed", "now also sets X", "migrated from
-  Y"), it spends more words than it informs — restating what the name,
-  signature, and types already say, or stretching a real point over four lines —
-  and it denies a thing the change removed, so the mention survives as its own
-  denial ("copy is not a catalogue"). That last one is the **polar bear**: a bare
-  "polar bear here" on a PR comment asks for this pass. Rewrites, moves and cuts
-  in place. Invoke as: /tend-prose [existence | durability | tightness |
-  negation] [optional focus guidance] — naming one lens runs only that lens.
+  Markdown — against four equal defects: **existence** (it should not have been
+  written at all), **durability** (it narrates the change instead of the code's
+  lasting contract), **tightness** (it spends more words than it informs), and
+  **negation** (it denies a thing the change removed, so the mention survives as
+  its own denial). That last one is the **polar bear**: a bare "polar bear here"
+  on a PR comment asks for this pass. Rewrites, moves and cuts in place. Invoke
```

**@vzakharov** — 2026-09-11T01:09:16Z

I wouldn't single out the polar bear here; just include the alias for every defect -- then whenever it's mentioned, the agent will reach for the skill

---

### `.claude/skills/tend-prose/SKILL.md`:64 — unresolved

```diff
@@ -55,19 +51,19 @@ bear`.
 
 | Lens | Primary      | Alias         |
 | ---- | ------------ | ------------- |
-| A    | `existence`  | —             |
-| B    | `durability` | `narration`   |
-| C    | `tightness`  | `bloat`       |
-| D    | `negation`   | `polar bear`  |
+| 1    | `existence`  | —             |
+| 2    | `durability` | `narration`   |
+| 3    | `tightness`  | `bloat`       |
+| 4    | `negation`   | `polar bear`  |
 
-`negation` and `narration` are three characters apart and name **different**
-lenses — say `polar bear` for D, which is how the request arrives from a PR
-comment anyway.
+The numbers are the order Step 2's sections come in. `narration` and `negation`
+are three characters apart and name **different** lenses — 2 and 4 — so read the
+argument against this table rather than from memory.
 
-Then run **only** that lens: skip the other three in Step 2, apply only its fixes
-in Step 3, and report only its group in Step 5. This is the mode for "I just saw
-archaeological narration in there", and for a bare `polar bear here` on a PR
-comment — a targeted pass, not the full sweep.
+Then run **only** that lens: skip the other three in Step 2 and apply only its
+fixes in Step 3. This is the mode for "I just saw archaeological narration in
```

**@vzakharov** — 2026-09-11T01:12:02Z

btw "archaeology" is also one way we talk about non-durable prose, but it's actually a THIRD meaning: something that goes too much into describing how we came up with something, in a document that is *meant* to describe changes. But I don't think this meaning should be part of this skill. First, this is an operator's call, it would be too hard for an agent too judge how much is too much; second, we use it only when the document is by definition describing change that was meant to be there.

All of this is just context -- no need to describe it hear lest it becomes a polar bear (I'm talking in rhymes now), but let's remove any mentions of "archaeology" here and throughout the skill

---

### `.claude/skills/tend-prose/SKILL.md`:319 — unresolved

```diff
@@ -313,36 +309,11 @@ line that is about to go.
   reader can't get elsewhere is not bloat; length carrying nothing is. But that
   describes a colocated `README.md`, opened on purpose, not a
   `.claude/rules/*.md` file: **a rule's length is a budget**, because it loads in
-  full every time its glob matches. Paragraphs of rationale in a rule are a Lens
-  A finding — the orientation belongs in a README the rule links to.
+  full every time its glob matches. Paragraphs of rationale in a rule are a lens
+  1 finding — the orientation belongs in a README the rule links to.
 
-## Step 5: Report + commit
+## Step 5: Commit
 
-Report the four classes **separately, each with a count**, one bullet per fix
-(`file:line` + before → after in a few words):
-
-```
-Existence (2)
-- src/foo.ts:22 — deleted (describes what the next three lines do)
-- .claude/rules/bar.md:40 — moved to src/bar/README.md (orientation, not an obligation)
-
-Negation (1)
-- src/copy/README.md:3 — deleted ("copy is not a catalogue"; the catalogue went with this change)
-
-Durability (2)
-- src/foo.ts:14 — "no longer parsed" → "Nothing parses the emoji."
-- …
-
-Tightness (3)
-- src/bar.ts:8 — 7-line docstring → 2 lines (dropped param restatement)
-- src/baz.ts:31 — deleted (signature says it)
-- …
-```
-
-All four groups always appear; **an empty one gets a sentence saying why** rather
-than silence ("nothing added was over-documented" is a real outcome, and so is
-"the diff removed nothing, so Lens D had no candidates"). In single-lens mode,
-only that lens's group is reported.
-
-Then commit the edits (on a feature branch, just commit — the vet run happens at
-milestones via `/finalize`, not per commit).
+Commit the edits, with the fixes and their reasons in the body. On a feature
+branch that is the whole step — the vet run happens at milestones via
+`/finalize`, not per commit.
```

**@vzakharov** — 2026-09-11T01:12:54Z

is that last sentence legitimate or a polar bear too? (Damn, now I see the cursed thing everywhere too.)

---

## Timeline (status, references, and other events)

- **2026-09-11T00:17:42Z** @vzakharov renamed from «feat: #48 add a /tighten-docs lens for negated-removal prose» to «feat: #48 add a negation lens and rename the pass /tend-prose».
- **2026-09-11T00:53:04Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/57#pullrequestreview-5173789260.
- **2026-09-11T01:13:06Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/57#pullrequestreview-5173949495.
