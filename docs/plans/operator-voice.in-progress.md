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
page history and the prompt were both readable from the start. The report was
finished before its cause was known, and it was written in the stack's nouns —
*array*, *schema*, *validation*, *retry* — where the reader's nouns (*photos*,
*gallery*, *the app tried again*) were available and exact.

Two things about this transcript bound everything below:

- **It is not a Claude transcript** — it came from a different vendor's agent.
  The failure is not one lab's, and nothing shipped may imply it is.
- **It stays out of the shipped prose.** The screenshots live on
  [PR #64](https://github.com/vzakharov/agent-project-boilerplate/pull/64) for
  whoever needs them; this plan is swept by `/finalize` before the branch lands.
  What ships is phrased as **how to write**, never as how some agent once wrote
  — a rule that recounts a failure plants a polar bear (CLAUDE.md § "Writing
  things down"), and ages into a story about an incident nobody remembers.

The second, personal half of the request: the maintainer wants an agent who
returns a joke instead of deadpanning it, and that kind of preference varies per
person — it cannot be a house rule, and today it has nowhere to live that
survives a session.

## How the pieces are arranged

Everything lives in one skill directory, and `CLAUDE.md` reaches into it with a
single import line:

```text
.claude/skills/plainly/
├── SKILL.md       # the long version: defects, triggers, the pass itself
├── voice.md       # the short version — imported by CLAUDE.md, always loaded
├── operators.md   # per-person entries — imported by voice.md, always loaded
└── example.md     # the worked before/after — read on demand from SKILL.md
```

**The resident file is named for what it governs, and stays clear of `rule`.**
`.claude/rules/` is a live mechanism with a different contract — frontmatter,
`paths:` globs, loaded only when a session touches a matching file — so a
rule-named file that is unconditionally resident reads as one of those to anyone
scanning the tree. `voice.md` collides with nothing and says what is inside it.

Two mechanisms make this work, and they are **not** the same mechanism, which is
the thing to get right before writing a line of it
([docs](https://code.claude.com/docs/en/memory#import-additional-files)):

- **In `CLAUDE.md`, `@path` is a real import.** The file is expanded into
  context at launch, imports nest four hops deep, and **parsing skips code spans
  and fenced blocks**. Every existing `@` reference in this repo is written
  inside backticks — `` `@.claude/skills/tend-prose/SKILL.md` `` — which is
  exactly why § "Writing things down" can tell you to read that skill *sparingly*
  and mean it. So the one new reference must be **unbackticked**, and the
  house style around it makes that look like a typo: the line carries an HTML
  comment saying why, which `CLAUDE.md` strips before anything reaches context.
- **In a `SKILL.md`, `@path` imports nothing.** A skill's description is always
  in context, its body loads on invocation, and the files beside it load only
  when the agent reads them. This repo's `@`-reference-in-a-skill convention
  works because "load and follow" means the agent opens the file — a habit, not
  a loader. Good enough for `example.md`, which should not be resident.
  Not good enough for `operators.md`: a preference that only applies once
  someone invokes a skill is a preference that never applies, because the reply
  that deadpans your joke is a reply nobody invoked anything for. So
  `operators.md` is reached by import, from `voice.md`, and is resident.

**The import is about ownership, not cost.** The docs are explicit that splitting
a file out does not reduce what loads at launch. What it buys is what was asked
for: a topic large and separate enough to edit on its own, sitting next to the
skill that expands it, instead of growing inside `CLAUDE.md`.

## What this delivers

Four pieces. The first two are the house rule; the third is the personal half;
the fourth is registration.

### 1. `voice.md` — the always-loaded short version

Roughly 20 lines, stating the rule as a **shape** rather than a mood, so a
violation is visible rather than a matter of taste:

- **The first sentence is the cause, in the reader's words.** Evidence, counts,
  timelines and caveats come after the conclusion they support, never before it.
- **Not knowing the cause is unfinished work, not a style constraint.** Go read
  the thing that would settle it — the data, the prompt, the history — before
  reporting. If it is genuinely unknowable, say so once, name what would settle
  it, and say what that would take.
- **Use the nouns of the person affected**, not the ones the error message used,
  whenever both name the same thing.
- **State the chain, not the steps.** Every step says why the next one followed;
  a sequence with no *because* in it is a list, not an explanation.
- **Length is not thoroughness.** A report that takes five screens to reach its
  point has failed even when every line in it is true.
- **Frustration is a signal, and it is about you.** Repeated punctuation, caps,
  a re-asked question, "just tell me" — read it as a report that the last answer
  did not land. Do not answer it with more detail. Answer the question that was
  actually asked, from the cause, in shorter words.

Scope is stated by reference, not restated: this governs the **human-facing** and
**conversation** groups that `CLAUDE.md` § "Language" already partitions — so it
reaches chat replies *and* the GitHub prose a person reads to decide something:
PR bodies, issue comments, review replies. That is the surface the complaint came
from; the boss who could not tell what the agent meant was reading a thread, not
a session. Agent-facing prose keeps `/tend-prose`'s rules, and commit/PR
conventions are unchanged.

It ends with the identity line (piece 3) and a pointer to the skill, and nothing
else — the long version lives in exactly one place.

`CLAUDE.md` gains three lines: a short § "Explaining things to people" after
§ "Language", saying the topic lives with its skill, and the import.

### 2. `/plainly` — the long version and the on-demand pass

It mirrors how `/tend-prose` is the long version of § "Writing things down":

- **Invoked bare at an answer that did not land**, it re-explains the previous
  answer as a causal chain in plain words — the thing an operator otherwise has
  to ask for twice.
- **Invoked with a question**, it answers that question under the rule,
  including the investigation half: find the cause first.
- **Its description carries the identity trigger**, per piece 3, because a
  description is the one part of a skill that is always in context.
- **It names the defects, so one word can call out a bad report** the way
  `polar bear` already works for `/tend-prose`. These are tells to check a draft
  of your own against:

  | Defect | Tell |
  | --- | --- |
  | **Symptom-as-finding** | The headline is a quoted error string or a metric the system emitted |
  | **Buried lede** | Counts, windows, method notes or caveats before the conclusion |
  | **Untranslated nouns** | The stack's vocabulary where the domain's exists and is exact |
  | **Broken chain** | Steps in sequence with nothing saying why each one followed |
  | **Fog** | Uncertainty stated repeatedly and never resolved into "here's what would settle it" |
  | **Receipt** | A reply *about* what the person said, where the thing they said wanted an answer — a joke acknowledged instead of returned, an aside filed instead of engaged |

- **A worked before/after in `example.md`**: two answers to the same question —
  a thin one and a full one — and what the full one had read that the thin one
  had not. Invented domain, no vendor, no incident. This is the part that
  teaches; the table only gives it names.

**The sixth defect is the odd one, and it earns its place by being the only one
investigation cannot fix.** The other five are cured by knowing more — read the
history, find the cause, say it in the right nouns. *Receipt* is cured by
answering the thing that was actually said. It is the same move as the rest, at
the level of a conversation rather than a report: narrating a response instead
of making it, which feels attentive and leaves the other person unanswered. Its
tell is the register shift — a neighboring sentence goes formal, or refers to
the remark in the third person ("noted", "a fair point", "I'll take that on
board").

Where the personal half meets the house rule: **whether to return a joke at all
is an operator entry** — some people want the deadpan — but **acknowledging one
instead of either returning it or passing it by is a defect for everyone**. The
entry sets the register; this rule says don't hand someone a receipt in place of
a reply.

### 3. `operators.md` — per-person entries

One short section per person, a template block and no real people in the
boilerplate — adopters fill in their own.

An entry tunes **manner only**:

> **An entry cannot lower a bar.** It changes how an answer sounds, never what is
> in it, what gets reported, or which checks run. "Keep it short" does not
> license dropping the cause; "no need to flag small stuff" does not license a
> silent failure. A preference that would change substance is not an entry — it
> is a change to the house rule that everyone can see.

Entries are written by an operator about themself (or with their say-so), and
the growth mechanism sits where `CLAUDE.md` already says the loop is the agent's
to grow: **when someone states a standing preference about how you talk to them,
offer to write it into their entry.** That is how "I like it when you ping my
jokes back" becomes durable instead of dying with the session.

**Identity is resolved once, at the start of a session, and then known.** The
harness supplies it; when it does not, run the one lookup that settles it
(`git config user.email`) and carry the answer for the rest of the session
rather than re-deriving it per reply. No match against any entry means the house
rule alone, which is a complete instruction on its own. The instruction lives in
two places on purpose: in `voice.md`, which is resident, and in the skill's
**description**, which is the only part of a skill that is in context before
anyone invokes anything.

### 4. Registration

- Three rows in the catalog's **G1 — Prose & principles** — the skill, `voice.md`
  (`adopt`), and `operators.md` (**rewrite**, the way
  `sync-agent-infra/upstream.json` is: ships as a template, every adopter writes
  their own). G1 is where `CLAUDE.md`, `/dry` and `/tend-prose` already sit, and
  "always adopt, no stack assumptions, no GitHub" describes these exactly.
- `README.md`: the skill count (**30 → 31**, 22 → 23 working) and the G1 row's
  one-line summary.
- `ADOPTING.md` shared tail: a hydration step beside "Settle the language
  decision" — the house rule is adopt-as-is, only the operator entries are filled
  in. Same for `/detemplate`, which seeds the entry for whoever ran it if they
  state a preference during the run, and otherwise leaves the template.
- `./scripts/vet.sh` passes — it calls `check-skill-catalog.sh`, whose assertion
  2 wants exactly one catalog row per skill directory, and assertion 3 wants
  every path a row names to exist.

## Why this is worth always-loaded context

`CLAUDE.md` § "Writing things down" sets three tests, and new always-resident
prose has to pass all of them whichever file it sits in — an import does not
make it cheaper, only better placed:

1. **A constraint, not a description.** It constrains output shape.
2. **Not recoverable.** Nothing in the code says how to address a human.
3. **Getting it wrong breaks something nameable.** Three turns and an irritated
   boss to reach an answer that was available in one.

The cost is real and bounded — roughly 20 lines plus a few per operator, with
the long version paid for only when invoked. Putting everything in the skill
instead fails because the rule must apply to replies nobody invoked a skill for;
putting everything in the resident file costs every session a worked example and
a defect table that are reference material.

## Execution order

1. Create `.claude/skills/plainly/`; write `SKILL.md` (description carrying the
   identity trigger, defect table, the pass) and `example.md`.
2. Write `voice.md`, and `operators.md` with the template block and the
   manner-only guardrail.
3. Add `CLAUDE.md` § "Explaining things to people": the placement sentence and
   the unbackticked import, with the HTML comment guarding it.
4. Catalog rows, `README.md` counts, `ADOPTING.md` and `/detemplate` hydration.
5. Verify the import actually loads — `/context` lists it under memory files, or
   a fresh session can quote a line from `voice.md` it was never handed.
6. `./scripts/vet.sh`, then `/dry` and `/tend-prose`, then `/pr`.

## DRY notes

- **§ "Language"'s audience partition is reused by citation, not restated.** It
  already splits human-facing / agent-facing / conversation, and the rule needs
  exactly that split to say what it governs. Restating it would create the
  two-homes-one-constraint defect `CLAUDE.md` names in § "Writing things down".
- **`voice.md` is the short version and `SKILL.md` the long one, never both.**
  Same arrangement `/tend-prose` has with § "Writing things down": the defect
  table, the triggers and the worked example exist once each, and the resident
  file carries the rule and a pointer.
- **Not merged into `/tend-prose`, deliberately.** The overlap is one instinct
  (say it shorter) across two artifacts that share no mechanics: `/tend-prose`
  scopes itself with `git diff`, edits committed files, and runs at milestones;
  this rule applies to a reply that is never in a diff and has no pass to run
  it. A fifth lens would have to opt out of Steps 1, 3 and 5 of that skill —
  which is a separate skill wearing a borrowed name. The two cross-reference
  instead.
- **No new top-level doc.** Everything lands under `.claude/skills/plainly/`,
  plus three lines in a file that already exists — so § "Writing things down"'s
  ask-first rule does not arise.
- **The stub/hydration conventions are reused as-is** — `ADOPTING.md`'s shared
  tail, the catalog's G1 group and its `rewrite` disposition, `/detemplate`'s
  hydration pass. No new marker and no new mechanism; the operator entries are
  hydration in exactly the sense the language decision already is.
