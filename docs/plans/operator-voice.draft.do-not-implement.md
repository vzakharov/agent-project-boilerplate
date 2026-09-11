> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Operator voice: a house rule for explaining things, and per-operator style entries

## The complaint this answers

From an adopter repo, the boss to the maintainer (translated):

> Can we put it somewhere hard in the instructions that agents speak plain human
> language and not techno-nerd? It's constantly the case that they write five
> pages and you can't tell what they were trying to say — they don't explain
> cause and effect. Just, like, "such-and-such function failed — the model did
> such-and-such". Why did it do that? What caused it? I keep having to
> 1. dig for the truth, 2. ask for it in plain words.

The attached transcript is the whole case in three turns:

| Turn | Operator asked | Agent answered |
| --- | --- | --- |
| 1 | "what's going on here? \<issue link\>" | "a real gallery-size failure… every validation error says *expected array to have ≤24 items*" — plus nine/fifteen/seven counts, UTC windows, and a note that the alert's wording is boilerplate |
| 2 | "can't you explain in simple human words what happened exactly step by step????" | the same facts, renumbered into steps, still ending at "the AI returned too many" |
| 3 | "why AI produced version with more than 24 photos???" | **the actual cause**: the gallery already held 24 photos, the edits attached more, and our prompt tells the model to keep the existing photos and put new ones in a gallery — but never says "when a gallery reaches 24, start another one" |

Turn 3 is a good answer. Nothing in it needed turn 1 or turn 2 to exist: the
page history and the prompt were both readable from the start. **The agent
stopped investigating when it had a quotable error string**, then spent its
report defending the completeness of the evidence rather than saying why the
thing happened.

So this is not only a register problem, and a rule that only says "use simpler
words" would not have produced turn 3. Two failures stack:

1. **Reporting a symptom as if it were a finding.** "Validation rejected the
   array" is what the system printed, not what happened. The report was finished
   before the cause was known.
2. **Speaking in the stack's nouns.** *Array*, *schema*, *validation*, *retry*
   — where the reader's nouns (*photos*, *gallery*, *the app tried again*) were
   available and exact.

The second, personal half of the request: the maintainer wants an agent who
returns a joke instead of deadpanning it, and that kind of preference varies per
person — it cannot be a house rule, and today it has nowhere to live that
survives a session.

## What this delivers

Four pieces. The first two are the house rule; the third is the personal half;
the fourth is registration.

### 1. `CLAUDE.md` § "Explaining things to people" — a new section after § "Language"

Always-loaded, short, and it states the rule as a **shape** rather than a mood,
so a violation is visible rather than a matter of taste:

- **The first sentence is the cause, in the reader's words.** Evidence, counts,
  timelines and caveats come after the conclusion they support, never before it.
- **Not knowing the cause is unfinished work, not a style constraint.** Go read
  the thing that would settle it — the data, the prompt, the history — before
  reporting. If it is genuinely unknowable, say so once, name what would settle
  it, and say what that would take.
- **Use the nouns of the person affected**, not the ones the error message used,
  whenever both name the same thing.
- **State the chain, not the steps.** Each step says why the next one followed;
  a numbered list with no *because* in it is the turn-2 failure, not the fix.
- **Length is not thoroughness.** A report that takes five screens to reach its
  point has failed even when every line in it is true.

Scope is stated by reference, not restated: this governs the **human-facing** and
**conversation** groups that § "Language" already partitions. Agent-facing prose
keeps `/tend-prose`'s rules, and commit/PR conventions are unchanged.

It closes with pointers to the two files below, and nothing else — the long
version lives in exactly one place.

### 2. A skill holding the long version and the on-demand pass

`/plainly` (name is question 2), mirroring how `/tend-prose` is the long version
of § "Writing things down":

- **Invoked bare at a bad answer**, it re-explains the previous answer as a
  causal chain in plain words — the thing the operator had to type
  "can't you explain in simple human words????" to get.
- **Invoked with a question**, it answers that question under the rule, including
  the investigation half: find the cause first.
- **It names the defects, so a human can throw one word at a bad report** the way
  `polar bear` already works for `/tend-prose`:

  | Defect | Tell |
  | --- | --- |
  | **Symptom-as-finding** | The report's headline is a quoted error string or a metric the system emitted |
  | **Buried lede** | Counts, windows, method notes or caveats before the conclusion |
  | **Untranslated nouns** | The stack's vocabulary where the domain's exists and is exact |
  | **Broken chain** | Steps in sequence with nothing saying why each one followed |
  | **Fog** | Uncertainty stated repeatedly and never resolved into "here's what would settle it" |
  | **Receipt** | A reply *about* what the person said, where the thing they said wanted an answer — a joke acknowledged instead of returned, an aside filed instead of engaged |

- **A worked before/after**, built from the transcript above with the product
  details generalized: the turn-1 answer, the turn-3 answer, and what the agent
  would have had to read to open with turn 3. This is the part that teaches;
  the defect list only gives it names.

**The sixth defect is the odd one, and it earns its place by being the only one
investigation cannot fix.** The other five are cured by knowing more — read the
history, find the cause, say it in the right nouns. *Receipt* is cured by
answering the thing that was actually said. It is the same move as the rest, at
the level of a conversation rather than a report: the agent narrates its
response instead of making it, and a narrated response feels attentive while
leaving the other person unanswered. Its tell is the register shift — a
neighboring sentence goes formal, or refers to the remark in the third person
("noted", "a fair point", "I'll take that on board").

Where the personal half meets the house rule: **whether to return a joke at all
is an operator entry** — some people want the deadpan — but **acknowledging one
instead of either returning it or passing it by is a defect for everyone**. The
entry sets the register; this rule says don't hand someone a receipt in place of
a reply.

### 3. Per-operator entries

A single `.claude/operators.md` (shape is question 3) with one short section per
person, read at session start when the file exists, plus a template block and no
real people in the boilerplate — adopters fill in their own.

An entry tunes **manner only**:

> **An entry cannot lower a bar.** It changes how an answer sounds, never what is
> in it, what gets reported, or which checks run. "Keep it short" does not
> license dropping the cause; "no need to flag small stuff" does not license a
> silent failure. A preference that would change substance is not an entry — it
> is a change to `CLAUDE.md` that everyone can see.

Entries are written by an operator about themself (or with their say-so), and
the growth mechanism is stated where CLAUDE.md already says the file is the
agent's to grow: **when someone states a standing preference about how you talk
to them, offer to write it into their entry.** That is how "I like it when you
ping my jokes back" becomes durable instead of dying with the session.

Resolution is one line: match the session's operator (the identity the harness
supplies, else `git config user.email`) against the entries; no match means the
house rule alone, which is a complete instruction on its own.

### 4. Registration

- One catalog row per new item in **G1 — Prose & principles** (`/plainly`,
  `.claude/operators.md`), which is where CLAUDE.md, `/dry` and `/tend-prose`
  already sit — "always adopt, no stack assumptions, no GitHub" describes these
  exactly. `scripts/check-skill-catalog.sh` assertion 2 requires the skill row.
- `README.md`: the skill count (**30 → 31**, 22 → 23 working) and the G1 row's
  one-line summary.
- `ADOPTING.md` shared tail: a hydration step beside "Settle the language
  decision" — the house rule is adopt-as-is, only the operator entries are filled
  in. Same for `/detemplate`, which seeds the entry for whoever ran it if they
  state a preference during the run, and otherwise leaves the template.
- `scripts/vet.sh` passes (it calls the catalog check).

## Why this is worth always-loaded context

`CLAUDE.md` § "Writing things down" sets three tests, and a new always-resident
section has to pass all of them:

1. **A constraint, not a description.** It constrains output shape.
2. **Not recoverable.** Nothing in the code says how to address a human.
3. **Getting it wrong breaks something nameable.** The transcript above: three
   turns and an irritated boss to reach an answer that was available in one.

The cost is real and bounded — roughly 20 lines resident, with the long version
paid for only when invoked. The alternative of putting everything in the skill
fails because the rule must apply to replies nobody invoked a skill for; the
alternative of putting everything in `CLAUDE.md` costs every session the worked
example and the defect table, which are reference material.

## Open questions

Recommendations are already in force in the plan above, so it is implementable as
written; an answer that differs is a revision.

1. **Shape.** (a) `CLAUDE.md` section + skill for the long version *(recommended
   — it is exactly the `/tend-prose` split, and the split exists because the two
   halves have different trigger conditions)*; (b) `CLAUDE.md` section only,
   no skill; (c) skill only.
2. **Skill name.** (a) `/plainly` *(recommended — it is what an operator would
   type at a bad answer)*; (b) `/explain`; (c) `/tend-report`.
3. **Per-operator storage.** (a) one `.claude/operators.md`, section per person
   *(recommended — a few lines each, so a team's whole file costs less than one
   skill load, and nothing has to match filenames to identities)*; (b) one file
   per operator under `.claude/operators/` with a `matches:` frontmatter key, read
   selectively; (c) drop the per-operator half and ship the house rule alone.
4. **Reach.** (a) the house rule governs chat replies **and** human-facing GitHub
   prose — PR bodies, issue and review comments *(recommended — the boss reads
   the issue thread, not the session)*; (b) chat replies only.

## Execution order

1. Write `CLAUDE.md` § "Explaining things to people".
2. Write the skill (frontmatter description, defect table, worked before/after).
3. Write `.claude/operators.md` with the template block and the manner-only
   guardrail; add the "offer to write it down" line to `CLAUDE.md`.
4. Catalog rows, `README.md` counts, `ADOPTING.md` and `/detemplate` hydration.
5. `./scripts/vet.sh`, then `/dry` and `/tend-prose`, then `/pr`.

## DRY notes

- **§ "Language"'s audience partition is reused by citation, not restated.** It
  already splits human-facing / agent-facing / conversation, and the new section
  needs exactly that split to say what it governs. Restating it would create the
  two-homes-one-constraint defect CLAUDE.md names in § "Writing things down".
- **The long version goes in the skill and nowhere else**, the same arrangement
  `/tend-prose` has with § "Writing things down". `CLAUDE.md` carries the rule
  and a pointer; the defect table and the worked example exist once.
- **Not merged into `/tend-prose`, deliberately.** The overlap is one instinct
  (say it shorter) across two artifacts that share no mechanics: `/tend-prose`
  scopes itself with `git diff`, edits committed files, and runs at milestones;
  this rule applies to a reply that is never in a diff and has no pass to run
  it. A fifth lens would have to opt out of Steps 1, 3 and 5 of that skill —
  which is a separate skill wearing a borrowed name. The two cross-reference
  instead.
- **No new top-level doc.** `CLAUDE.md` § "Writing things down" requires asking
  first and arguing the "don't" side; everything here lands under `.claude/` or
  in files that already exist, so the question does not arise.
- **The stub/hydration conventions are reused as-is** — `ADOPTING.md`'s shared
  tail, the catalog's G1 group, `/detemplate`'s hydration pass. No new marker
  and no new mechanism; the operator entries are hydration in exactly the sense
  the language decision already is.
