# PR #57: feat: #48 add a negation lens and rename the pass /tend-prose

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/57
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/48-tighten-docs-polar-bear-1zzzif
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-10T21:41:45Z
- **Updated:** 2026-09-11T00:53:05Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The defect.** When a change removes a thing the prose described, the reflex is to negate the sentence in place rather than delete it. The mention survives as its own denial — "copy is not a segment", "the mark is not generated" — and every later reader pays for a thing that is not there. The reviewer's idiom: *don't think about the polar bear.*
- **Why the existing lenses miss it.** Lens A's tells all point at prose that *describes how the code works*, which a sentence about what the code does **not** contain passes cleanly — it even reads as a genuine constraint. Lens B has the right instinct (the sentence only serves a reader who remembers the previous draft) but the wrong trigger, since its tells are change verbs and a negated mention is written in clean present tense.
- **A fourth lens, `negation`** (alias `polar bear`), rather than the issue's lean toward a case under Lens A. It is the only lens that reads the **removed** side of the diff: a new Step 1 sub-step collects the nouns the change deleted and greps them against the post-change tree, and a name surviving only inside prose is the candidate. The sub-step is skipped when the diff removes nothing, so additive work pays nothing for the lens. Step 3's fix is deletion, with an exception for a mention carrying a live fact; Step 5 gains its report group.
- **The test is whether the sentence is what put the subject in the reader's head** — with it gone, would the subject have crossed their mind at all? That framing is mechanically checkable and is the polar bear itself, where "would a reader need this sentence" invites an argument about need.
- **Guards against over-deletion.** This repo's prose is full of legitimate negative constraints, so the lens carries a constraint-vs-residue discriminator with a worked pair: a constraint's subject is something the reader reaches for anyway, so it crosses their mind with or without the sentence.
- **The four lenses spell TEND** — Tightness, Existence, Negation, Durability — and the skill's intro lists them in that order. With the three shipped names fixed, the fourth letter was the only free one, and `N` the only choice yielding a word that describes the pass. `negation` is also the better name on its own: it is the issue's framing, and unlike `absence` it does not read as `existence`'s antonym, which would make two of four lenses sound like opposites in one list. TEND is the memory aid; the run order is existence-first and the skill says so where it names the acronym.
- **`/tighten-docs` becomes `/tend-prose`.** The old name was wrong twice over, and the fourth lens made the first worse: "tighten" names Lens C specifically, though two of the four lenses produce nothing but deletions; and "docs" is not the word the skill's own description or `CLAUDE.md` uses for what it reads — both already say *prose*. **No redirect stub** — the `/implement` → `/go` precedent doesn't transfer, since `/implement` earned its stub by appearing in copyable handoff blocks, whereas this pass is reached through `@.claude/skills/…` pointers from `/go` and `/handle` that this PR repoints. A stub would cost a permanent line in every session's skill list to serve a mistyping that already fails legibly.
- **Repoints every site that names the skill or counts its lenses** — 16 references across 8 files. `/go`'s Step 3 was already stale before this change (it described "two halves" and two report groups against a three-lens skill) and now names neither, pointing at the skill instead, since a copy of that list is what went stale. `/squash-message` gains Lens D beside Lens B as inapplicable to a commit body, both for one reason: naming what a change took away is a commit message's job. `CLAUDE.md` § "Writing things down" gains the convention its repointing rule doesn't cover — when a convention goes away, stop stating it rather than negating it in place — and carries the idiom so the always-loaded file holds the routing token.
- **The lens caught a polar bear in this PR's own diff.** `/go` Step 3 explained why it no longer enumerates the lenses by pointing at the enumeration this branch had just deleted — a subject no later reader would have raised. It now states the trap in the present tense instead.

## QA Checklist

- [ ] `description-carries-idiom` — open a fresh session and check the skill list: the `/tend-prose` description names the polar-bear idiom, so an agent that has not opened the skill can route a bare `polar bear here` PR comment to it
- [ ] `single-lens` — run `/tend-prose negation` and `/tend-prose polar bear` on a branch; confirm only that lens runs and only its group is reported
- [ ] `removed-noun-step` — run the full `/tend-prose` on a branch whose diff **deletes** a module or field, and confirm Step 1 produces the removed-noun list and greps it against the post-change tree
- [ ] `no-op-skip` — run the full `/tend-prose` on a purely additive branch and confirm the removed-noun sub-step skips instead of grepping an empty list. Not exercised on this branch: the rename makes this diff a removing one, so the sub-step ran (see `self-applied` below)
- [ ] `self-applied` — the pass ran over this branch's own diff. The removed nouns were `tighten-docs`, "three lenses" and "two halves of equal weight"; each survives only in the working artifacts `/finalize` sweeps. It found one live polar bear in `/go` Step 3, which is fixed in `14f8c30`
- [ ] `constraint-survives` — point the lens at `CLAUDE.md`'s own negative constraints (dev artifacts go in `tmp/`, never create a top-level doc) and confirm the discriminator keeps them
- [ ] `live-fact-exception` — check a negated mention that carries a real fact is rewritten to state the fact positively, not deleted wholesale
- [ ] `citations-consistent` — `grep -rn "tighten-docs"` yields **zero** hits outside the working artifacts `/finalize` sweeps and this branch's own name; with no redirect stub, anything left is a real dangling reference. No site still says "three lenses" or "two halves of equal weight"
- [ ] `vet` — `./scripts/vet.sh` passes, including `scripts/check-skill-catalog.sh`

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `description-carries-idiom` | manual-only | — | Whether an agent recognizes the idiom from the description alone is a judgment call |
| `single-lens` | manual-only | — | Requires running the skill and judging which lens it applied |
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
Lens A's tells all point at prose describing how the code works, which
a sentence about what the code does not contain passes cleanly, and
Lens B's tells are change verbs that a clean present-tense negation
never trips.

The pass gains a fourth lens, `negation` (alias `polar bear`), with its
own tell, test, fix and report group. It is the only lens that reads
the removed side of the diff: Step 1 collects the nouns the change
deleted and greps them against the post-change tree, and a name
surviving only inside prose is the candidate. The fix is deletion
rather than rewriting, except where a mention carries a live fact
alongside the denial — then the fact stays, phrased as what is there.
The test asks whether the sentence is what put its subject in the
reader's head: with it gone, would the subject have crossed their mind
at all? A constraint's subject would, which is what keeps the lens off
the legitimate negative rules a codebase is properly full of.

`/tighten-docs` becomes `/tend-prose`, whose four lenses spell TEND —
Tightness, Existence, Negation, Durability — as a memory aid, not the
run order. The old name was wrong twice over: "tighten" named Lens C
specifically, though two of the four lenses produce nothing but
deletions, and "docs" was never the word the skill or CLAUDE.md used
for what it reads. No redirect stub holds the old name: the pass is
reached through skill pointers rather than typed, so every caller is
repointed and the catalog check proves it. The polar-bear idiom sits
in the frontmatter description, which every session loads, so an agent
that has not opened the skill still resolves a bare "polar bear here"
on a PR comment to the pass that handles it.

Closes #48

Co-authored-by: Claude <noreply@anthropic.com>
```

---
_Generated by [Claude Code](https://claude.ai/code)_

---

## Review threads

### `.claude/skills/go/SKILL.md`:85 — unresolved

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

---

### `.claude/skills/squash-message/SKILL.md`:207 — unresolved

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

---

### `.claude/skills/tend-prose/SKILL.md`:14 — unresolved

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

---

### `.claude/skills/tend-prose/SKILL.md`:31 — unresolved

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

---

### `.claude/skills/tend-prose/SKILL.md`:61 — unresolved

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

---

### `.claude/skills/tend-prose/SKILL.md`:319 — unresolved

```diff
@@ -226,14 +318,17 @@ sentence.
 
 ## Step 5: Report + commit
```

**@vzakharov** — 2026-09-11T00:52:35Z

as clarified above, reporting in the session is not needed (let's see if you'll add a polar bear here;-)

including the report in the commit body is fine ofc but I guess the agent would anyway

---

## Timeline (status, references, and other events)

- **2026-09-11T00:17:42Z** @vzakharov renamed from «feat: #48 add a /tighten-docs lens for negated-removal prose» to «feat: #48 add a negation lens and rename the pass /tend-prose».
- **2026-09-11T00:53:04Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/57#pullrequestreview-5173789260.
