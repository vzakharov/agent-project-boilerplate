> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #54 — the language decision joins the hydration set

Source: `docs/issue/54/issue.md`.

An adopting project routinely has human readers in one language and an
agent-facing instruction set in another, and nothing upstream tells it to decide
that. So the decision gets made implicitly, one file at a time, by whichever
session wrote that file. This change makes it an explicit hydration item —
alongside the G6 stubs and `scripts/vet.sh` — and states separately the one part
that is upstream's regardless of any adopter's answer: **a string another skill
matches on literally stays English.**

## What ships

Six files, all prose. In this repo prose about the loop *is* the product, so per
`CLAUDE.md` § "Git conventions" every commit here is `feat:`, not `docs:`.

### 1. `CLAUDE.md` — a new `## Language` section (the home)

Placed after § "Writing things down" and before § "Working with skills": the
decision is about what prose gets written in, so it belongs next to the section
that governs whether prose gets written at all.

Two parts, with different lifetimes:

**A stub blockquote — the hydration prompt.** Written in the same voice as
§ "About this project" and § "Testing":

> _Replace this stub with this project's language decision. A monolingual English
> team writes "English throughout" and is done — but write it, so the next
> session reads a decision rather than making one._

Then the surface the answer has to cover, as a table — because every adopter
that has drifted drifted by missing one row, and a prose list of six invites
skimming:

| Surface | What it covers |
| --- | --- |
| Durable docs | `README.md` and whatever else a human reads to decide something, versus `CLAUDE.md`, `.claude/skills/**`, `.claude/rules/**` |
| Transient working artifacts | `docs/plans/`, `docs/issue/`, `docs/pr/` — these split from durable docs rather than following them |
| Commit and PR text | commit messages, PR titles and bodies |
| Skill-emitted prose | the bodies `/pr`, `/squash-message` and `/qa-checklist` write |
| Conversation | issue and PR comments, review replies, session replies |
| Code | comments, docstrings, identifiers |

Each row carries the one-line reasoning the issue gives where the reasoning is
not obvious from the row — transient artifacts are swept before merge and read
while they live by the session working against them, which argues for the
agent's language even where the durable docs are not in it; commit and PR text
is `git log` and review surface, so it follows the human side; conversation
follows the language it was asked in rather than being fixed to one, since an
exchange is not a standing artifact.

The section states that the boilerplate does not pick a default, and cites
`vzakharov/ai-bookkeeper` as one filled-in instance (Russian human-facing prose,
English agent-facing prose, with the transient-artifact and conversation
carve-outs) — as a worked example, not the answer.

**A permanent subsection — `### Markers stay English`.** This one is not a
stub and is never replaced by an adopter's answer, because it is a property of
how the skills are written rather than of anyone's choice. It states the rule,
the recognition test, and what breaks:

- The rule: a string another skill locates by matching its text literally stays
  English, whatever the surrounding prose is.
- The recognition test: if a skill finds a section by its heading rather than by
  position, that heading is a marker. Translating one does not produce a
  translated section — it produces a *second* section beside the one the skill
  could not find.
- The current instances, named in one line: the `## Summary` and `## QA
  Checklist` headings `/qa-checklist` locates by text, the `Proposed squash
  title/body:` lead `/squash-message` Step 4 locates the same way, and the
  semantic commit prefixes.

The recognition test is what keeps the list from being the load-bearing part, so
a marker added later is covered by the rule without an edit here.

### 2. `ADOPTING.md` — a shared-tail step

A new § "Settle the language decision" in the shared tail, between § "Reconcile
`CLAUDE.md` rather than overwrite it" and § "Implement `scripts/vet.sh`" — the
tail's existing order runs prose, then vet, then stubs, and this is a prose
decision. Short, and it cites `CLAUDE.md` § "Language" as the home rather than
restating the surface table.

It carries the one thing that cannot go in `CLAUDE.md`: **the byte-counting
caveat.** `scripts/check-squash-message.sh` measures with `${#line}`, so the
80-column title and 72-column body caps roughly halve for any non-Latin script
and `vet.sh` rejects a correctly wrapped message — tracked as
[#53](https://github.com/vzakharov/agent-project-boilerplate/issues/53). It goes
here and not in `CLAUDE.md` because `ADOPTING.md` is a `never` row that is never
copied into an adopter's tree, so the issue link resolves to the one thread that
will say whether the gap is still open — the same reasoning § "Known gaps"
already gives for #6. A note in `CLAUDE.md` would land in the adopter's tree as
an issue of theirs, and would go stale silently when #53 lands.

### 3. `.claude/skills/detemplate/SKILL.md` — probe, then ask

Per the issue's comment: the run must ask the operator what they expect if there
is any indication non-English applies anywhere.

- **Step 1 (profile the fork)** gains language to the list of what the tree
  cannot answer and is therefore asked as numbered prose in the plan turn. The
  probe is stated with it, because unlike the five G6 questions this one has
  evidence available: the language of the brief the operator passed to
  `/detemplate`, the language they are writing to the session in, and whether
  the brief describes a product for a non-English market. Any of those
  non-English makes the question mandatory; all-English makes it a confirmation
  the plan states rather than asks.
- **Step 4 (what the plan must contain)** gains the language answer to its list,
  next to `scripts/vet.sh`'s disposition.
- **Step 5 (execution order)** — item 4 already fills `CLAUDE.md`'s "About this
  project" stub from the brief; it gains § "Language" in the same breath, since
  both are stubs the brief answers and both are edits to the same file.

### 4. `.claude/skills/spinoff/SKILL.md` — the sibling re-decides

`CLAUDE.md` is already a rewrite in the travel triage. One clause added where
that list appears: the caller's § "Language" answer is a candidate default for
the sibling, not an inheritance — a sibling can serve a different audience than
the repo it was pushed out of, and the § "Markers stay English" subsection
travels unchanged either way.

### 5. `.claude/skills/sync-agent-infra/catalog.md` — keep G1 accurate

Two small edits, no new rows:

- The `CLAUDE.md` row's "What it does" lists the file's sections; add the
  language decision to that list.
- The G1 prose paragraph after the table, which owns the donor-not-replacement
  note, gains a sentence: § "Language" is the one section in that file an
  adopter hydrates rather than merges, and § "Markers stay English" inside it is
  the part that is not theirs to change.

No catalog row is added, so `scripts/check-skill-catalog.sh` assertion 3 (one
row per skill) is unaffected — this change adds no skill.

### 6. `README.md` — one word of disambiguation

Line 4 reads "Language- and framework-agnostic", meaning programming language.
With a `## Language` section now in `CLAUDE.md` about natural language, that
line acquires a second reading. Narrow it to "Stack-agnostic" — same claim, no
collision. This is the whole of the README change; the hydration prompt itself
is not README material.

## Deliberately not in scope

- **Fixing #53.** Separable, as the issue says, and it is a shell-arithmetic
  change to one script with no overlap with this diff. This plan states the
  caveat where an adopter will hit it and leaves the fix to its own PR. An
  adopter answering the prompt with a non-Latin script is blocked on their first
  `/finalize` until #53 lands, which is worth saying in the report.
- **A machine check that the stub was hydrated.** `check-skill-catalog.sh`
  asserting the blockquote is gone would mirror assertion 4's stub-marker check,
  but it would have to be keyed on the catalog's absence to avoid failing in this
  repo — where the stub is the shipped state — and that is a second copy of
  `/detemplate` Step 0's predicate in a script that has no other reason to know
  about forks. The existing stubs (§ "About this project", § "Repository layout",
  § "Testing") are enforced by prose alone; this one matches them.
- **Any language split in this repo's own tree.** The boilerplate is
  English-only and its § "Language" ships stubbed, exactly as § "About this
  project" does. Carrying a split here would stop it being a decision.

## Open questions

Each has a recommendation, and the plan above is written with the recommended
option already in force — so silence resolves them.

1. **Does "English throughout" fill the stub or delete the section?**
   (a) **Fills it** *(recommended)* — a one-line answer, and the section stays
   so § "Markers stay English" keeps its home and a later session reads a
   decision rather than an absence. (b) Deletes the stub blockquote and keeps
   the marker subsection. (c) Deletes the whole section, mirroring the
   hydrate-or-delete rule for G6 stubs — rejected in the plan above because the
   marker invariant is not the adopter's to delete.

2. **Does the marker subsection enumerate today's markers?**
   (a) **Rule + recognition test + the three current instances in one line**
   *(recommended)* — concrete enough to act on, and the recognition test carries
   the weight so a marker added later needs no edit here. (b) Rule and
   recognition test only, no enumeration — shorter, but a reader has to derive
   the list from three skills. (c) Enumerate, and add a pointer at each marker
   site in `/qa-checklist` and `/squash-message` — rejected: three copies of one
   constraint is the drift this repo's own doc rules name, and `CLAUDE.md` is
   always loaded, so a session writing either body already has the rule.

3. **`vzakharov/ai-bookkeeper` cited by name, or described anonymously?** (a)
   **By name** *(recommended)* — the issue offers it as a citable instance, and a
   named repo is checkable. (b) Described without the link, since the reference
   points out of an adopter's tree at a repo they cannot read if it is private.
   If (b), the example collapses to two sentences of shape with no link.

## DRY notes

- **The surface table is stated once**, in `CLAUDE.md` § "Language".
  `ADOPTING.md`, `/detemplate` and the catalog cite that section rather than
  restating any row of it — the same discipline § "Vetting" already holds, where
  `scripts/vet.sh`, `ADOPTING.md` and the catalog all point at one home for the
  exit rule instead of each carrying a copy.
- **The marker invariant is stated once**, in the same section, and no pointer is
  added at the marker sites (question 2c). Its recognition test exists precisely
  so the enumeration is not the load-bearing half — the alternative, registering
  each new marker in a central list, is a second thing to keep in sync.
- **The byte-counting caveat is stated once**, in `ADOPTING.md`, which is where
  the issue link can legitimately live. It is not duplicated into `CLAUDE.md`,
  where it would travel into adopters' trees and outlive #53.
- **No shared abstraction is extracted for "hydration item."** The three of them
  — G6 stubs, `scripts/vet.sh`, and now the language decision — are already
  linked by citation rather than by a shared mechanism, and each has a different
  enforcement story: the stubs are checked by `check-skill-catalog.sh` assertion
  4, `vet.sh` by its own exit contract, and this one by prose. A "hydration
  checklist" doc collecting all three would be a new top-level doc whose only
  content is pointers, and would immediately be a fourth place that goes stale
  when any of the three moves. `ADOPTING.md`'s shared tail already *is* that
  checklist, in the one place an adopter reads sequentially, which is why the new
  step goes there and nowhere else.
- **`/detemplate` and `ADOPTING.md` genuinely duplicate here, and that is
  pre-existing and correct.** The fork route and the subset route ask the same
  question of different trees, and the skill's copy differs at the point that
  matters: it has the brief's language as evidence, where `ADOPTING.md`'s reader
  has a repo with a history of its own to inspect. The two copies are each
  written to their own reader rather than one hedged statement covering both —
  the same split `/detemplate`'s § "Template fork" pointer already makes for the
  watermark, `vet.sh`'s exit, and the catalog's ordering.

## Verification

No stack, so the vet run is the two built-in checks:

- `bash scripts/vet.sh` exits 0 (`check-skill-catalog.sh` — no reference is
  added or removed, so assertion 1 is unchanged, and no skill is added, so
  assertion 3 is unchanged).
- `grep -c 'Language' CLAUDE.md` confirms one section, not two.
- Read § "Language" cold and check the six surfaces are each decidable from it —
  the failure mode the issue names is an adopter answering "the docs are in X"
  and drifting on transient artifacts or conversation.
