# Issue #48: docs: give /tighten-docs a lens for prose that negates a removed thing

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/issues/48
- **Author:** @vzakharov
- **Created:** 2026-09-10T01:08:49Z
- **Updated:** 2026-09-10T21:37:31Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## What `/tighten-docs` misses

When a change removes a thing the prose described, the reflex is to **negate the sentence in place** rather than delete it. The mention survives as its own denial, and every later reader pays for a thing that is not there.

Two specimens from one review round in a sibling repo, where a copy catalogue and a generated favicon were both removed:

```diff
-- **`shared/copy` is a catalogue, not a translation layer.** … `COPY` is the
-  parsed JSON and `fill()` substitutes the two `{placeholder}`s …
+- **Copy is not a segment.** Every string sits in the module that renders it …
+  so a catalogue would be indirection over one language at one address.
```

```diff
-| `src/shared/ui/aeapp-mark-paths.ts` | `app/icon.svg` | A favicon is fetched as
-  its own document … it carries both palettes itself. |
+**The mark is not generated.** `public/aeapp-mark.svg` is committed, and serves
+the page, the favicon and the Open Graph card as the same literal fills.
```

Both edits are locally reasonable — the old text was wrong and the new text is true. Both are also answers to a question no reader of the current tree would ask. The reviewer's phrasing for it: *don't think about the polar bear.*

## Why the existing lenses don't catch it

- **Lens A (existence)** owns it in principle — a sentence whose only content is that something is absent is not a constraint on the code. But every tell under it points at prose that *describes how the code works*; a sentence about what the code does **not** contain passes each one, and reads as a genuine constraint ("do not add a catalogue") rather than as residue.
- **Lens B (narration)** has the right instinct and the wrong trigger. Its tells are change verbs — "no longer", "used to", "migrated from" — and a negated mention carries none: it is written in clean present tense. Yet it fails Lens B's own test exactly as narration does, because *the reader who needs the sentence is the one who remembers the previous draft*.

So the defect sits in the seam and both lenses wave it through.

## Proposal

Either a fourth lens or a case under Lens A — I lean toward Lens A, since the verdict is always "cut it" and Lens A is where cuts already live, but the tells have to be spelled out because none of the current ones fire.

**The tell**: a sentence in the diff whose subject is a thing that does not appear anywhere in the tree after the change. Grep the removed nouns against the post-change source — a name that survives only inside prose is the signal.

**The test**: would a reader who had never seen the previous version need this sentence? If it only prevents them from expecting something they had no reason to expect, cut it.

**The fix** is a deletion, not a rewrite — which is what makes it worth naming separately from the "restate it positively" fixes elsewhere in the skill. The exception is a mention carrying a live fact along with the negation: keep the fact, phrased as what *is* there ("**One committed `public/aeapp-mark.svg` serves every consumer** …"), and drop the denial.

**Where it fits in the scope step**: the pass already reads the session's diff, which is what makes this detectable at all — the deleted side names the nouns to grep for. A cold read of the final tree cannot find it, because the sentence is self-consistent there.

## Also worth a line in `CLAUDE.md` § "Writing things down"

"When a convention changes, every place that states it changes with it" already covers repointing a citation. It does not cover the case where the right move is to stop stating it at all.

---

## Comments

### Comment by @vzakharov on 2026-09-10T21:37:31Z

[https://github.com/vzakharov/agent-project-boilerplate/issues/48#issuecomment-5625782309](https://github.com/vzakharov/agent-project-boilerplate/issues/48#issuecomment-5625782309)

I like the polar-bear idiom so keep it in some form or another, so a mere "polar bear here" on a pr comment is understood by a /handling agent

---

