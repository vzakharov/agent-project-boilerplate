> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #54 — the language decision joins the hydration set

Source: `docs/issue/54/issue.md`.

An adopting project routinely has human readers in one language and an
agent-facing instruction set in another, and nothing upstream tells it to decide
that. So the decision gets made implicitly, one file at a time, by whichever
session wrote that file. This change makes it an explicit hydration item —
hydrate-or-delete, exactly as the G6 stubs are — and separately generalizes the
one constraint that is upstream's regardless of anyone's answer: **a marker
another skill matches on literally is not yours to reword.**

## What ships

Six files, all prose. In this repo prose about the loop *is* the product, so per
`CLAUDE.md` § "Git conventions" every commit here is `feat:`, not `docs:`.

### 1. `CLAUDE.md` — two independent edits

They are separate because they have different lifetimes: one is the adopter's to
answer and delete, the other is nobody's to touch.

#### 1a. `## Language` — the hydration prompt, deletable

Placed after § "Writing things down" and before § "Working with skills": the
decision is about what prose gets written in, so it sits beside the section
governing whether prose gets written at all.

A stub blockquote in the voice of § "About this project" and § "Testing":

> _Replace this stub with this project's language decision — or, if the project
> is English throughout, **delete this section** and record that in
> `.claude/skills/sync-agent-infra/upstream.json`'s `declined` map._

Then the surface the answer has to cover, as a table — every adopter that has
drifted drifted by missing one row, and a prose list of six invites skimming:

| Surface | What it covers |
| --- | --- |
| Durable docs | `README.md` and whatever else a human reads to decide something, versus `CLAUDE.md`, `.claude/skills/**`, `.claude/rules/**` |
| Transient working artifacts | `docs/plans/`, `docs/issue/`, `docs/pr/` — these split from durable docs rather than following them |
| Commit and PR text | commit messages, PR titles and bodies |
| Skill-emitted prose | the bodies `/pr`, `/squash-message` and `/qa-checklist` write |
| Conversation | issue and PR comments, review replies, session replies |
| Code | comments, docstrings, identifiers |

Each row carries the one-line reasoning where the reasoning is not obvious from
the row: transient artifacts are swept before merge and read while they live by
the session working against them, which argues for the agent's language even
where the durable docs are not in it; commit and PR text is `git log` and review
surface, so it follows the human side; conversation follows the language it was
asked in rather than being fixed to one, since an exchange is not a standing
artifact.

**Deleting the section is a real answer, and the normal one.** A monolingual
project keeps nothing: a section reading "English throughout, no split" is worse
than no section, because it plants a question in every session that loads
`CLAUDE.md` for a project that has nothing to decide. So the disposition matches
the G6 stubs exactly — hydrate now, or delete — and the record of a deletion
goes where every other decline is recorded:

```json
"declined": {
  "CLAUDE.md § Language": "English throughout — revisit if we ship to a non-English market"
}
```

Phrased as a **condition in the present tense**, per `ADOPTING.md`'s existing
rule for that map, which is what makes the decision re-openable: the prompt
itself is gone from the tree (in a fork, `ADOPTING.md` goes with it), so
`/sync-agent-infra` re-offering an entry whose stated condition no longer holds
is the only path back to the question. A bare `"n/a"` there loses that.

#### 1b. `### Markers are not yours to reword` — inside § "Working with skills"

Not part of § "Language", and it survives that section's deletion, because it is
a property of how the skills are written rather than of anyone's language. Its
home is § "Working with skills", next to § "Adding or renaming a skill", which
already owns what happens when a skill's own strings move.

**Generalized past translation, which is what the new home buys.** Translating
`## QA Checklist` and renaming it to `## What to check` are the same defect: the
skill locates the section by matching its text, so either produces a *second*
section beside the one it could not find. The rule therefore reads as
reword-or-translate, and covers the English-only project that never reads
§ "Language" at all.

Three parts:

- The rule: a string another skill locates by matching its text is fixed — not
  reworded, not translated.
- The recognition test: if a skill finds a section by its heading rather than by
  position, that heading is a marker. This is what keeps the enumeration from
  being load-bearing, so a marker added later is covered without an edit here.
- The current instances, in one line: the `## Summary` and `## QA Checklist`
  headings `/qa-checklist` locates by text, the `Proposed squash title/body:`
  lead `/squash-message` Step 4 locates the same way, and the semantic commit
  prefixes.

### 2. `ADOPTING.md` — a shared-tail step

A new § "Settle the language decision" between § "Reconcile `CLAUDE.md` rather
than overwrite it" and § "Implement `scripts/vet.sh`" — the tail runs prose,
then vet, then stubs, and this is a prose decision. It cites `CLAUDE.md`
§ "Language" as the home rather than restating the surface table, and states the
hydrate-or-delete disposition with the `declined` entry as the deletion's
receipt.

It also carries the one thing that cannot go in `CLAUDE.md`: **the byte-counting
caveat.** `scripts/check-squash-message.sh` measures with `${#line}`, so the
80-column title and 72-column body caps roughly halve for any non-Latin script
and `vet.sh` rejects a correctly wrapped message — tracked as
[#53](https://github.com/vzakharov/agent-project-boilerplate/issues/53). It goes
here because `ADOPTING.md` is a `never` row, never copied into an adopter's
tree, so the issue link resolves to the one thread that will say whether the gap
is still open — the same reasoning § "Known gaps" already gives for #6. In
`CLAUDE.md` it would land in the adopter's tree as an issue of theirs and go
stale silently when #53 lands.

### 3. `.claude/skills/detemplate/SKILL.md` — probe, then ask

Per the issue's comment: the run must ask the operator what they expect if there
is any indication non-English applies anywhere.

- **Step 1 (profile the fork)** gains language to the list of what the tree
  cannot answer and is therefore asked as numbered prose in the plan turn. The
  probe is stated with it, because unlike the five G6 questions this one has
  evidence available: the language of the brief passed to `/detemplate`, the
  language the operator writes to the session in, and whether the brief
  describes a product for a non-English market. Any of those non-English makes
  the question mandatory; all-English makes it a confirmation the plan states
  rather than asks.
- **Step 4 (what the plan must contain)** gains the language answer, next to
  `scripts/vet.sh`'s disposition.
- **Step 5 (execution order)** — item 4 already fills `CLAUDE.md`'s "About this
  project" stub from the brief, and gains § "Language" in the same breath: fill
  it, or delete it. Item 6 already writes the watermark, so the `declined` entry
  a deletion needs lands there, in the file that step is already opening.

### 4. `.claude/skills/spinoff/SKILL.md` — the sibling re-decides

`CLAUDE.md` is already a rewrite in the travel triage. One clause where that
list appears: the caller's language decision is a candidate default for the
sibling, not an inheritance — a sibling can serve a different audience than the
repo it was pushed out of — and **the caller's `CLAUDE.md` may carry no
§ "Language" at all**, which is itself an answer (English throughout) rather
than an omission to copy. § "Working with skills"'s marker rule travels
unchanged either way, being no part of the decision.

### 5. `.claude/skills/sync-agent-infra/catalog.md` — keep G1 accurate

Two edits, no new rows:

- The `CLAUDE.md` row's "What it does" lists the file's sections; add the
  language decision.
- The G1 prose paragraph after the table, which owns the donor-not-replacement
  note, gains a sentence: § "Language" is the one section in that file an
  adopter hydrates **or deletes** rather than merges, recording a deletion in
  `upstream.json`'s `declined` map.

No catalog row is added, so `scripts/check-skill-catalog.sh` assertion 3 (one
row per skill) is unaffected — this change adds no skill.

### 6. `README.md` — one word of disambiguation

Line 4 reads "Language- and framework-agnostic", meaning programming language.
With a `## Language` section now in `CLAUDE.md` about natural language, that
line acquires a second reading. Narrow it to "Stack-agnostic" — same claim, no
collision. That is the whole README change; the prompt itself is not README
material.

## Deliberately not in scope

- **Fixing #53.** Separable, as the issue says, and a shell-arithmetic change to
  one script with no overlap with this diff. The plan states the caveat where an
  adopter will hit it and leaves the fix to its own PR. An adopter answering with
  a non-Latin script is blocked on their first `/finalize` until #53 lands, which
  is worth saying in the report.
- **A worked example naming a repo.** The surface table and its per-row
  reasoning carry the content; a citation would date the section to whoever
  reported it, and the improvement is general.
- **A machine check that the prompt was settled.** `check-skill-catalog.sh`
  asserting the stub blockquote is gone would mirror assertion 4's stub-marker
  check, but it would have to be keyed on the catalog's absence to avoid failing
  in this repo — where the stub is the shipped state — putting a second copy of
  `/detemplate` Step 0's predicate in a script with no other reason to know
  about forks. The `declined` entry is the receipt instead, and the sibling
  stubs (§ "About this project", § "Repository layout", § "Testing") are
  enforced by prose alone.
- **Any language split in this repo's own tree.** The boilerplate is
  English-only, and its § "Language" ships stubbed exactly as § "About this
  project" does. Carrying a split here would stop it being a decision.

## Open question

One left; the two resolved forks are collapsed above. The plan is written with
the recommendation in force, so silence resolves it.

**Does § "Markers are not yours to reword" name today's markers, or only teach
how to spot one?** The rule and the recognition test are in either version; the
question is only whether four concrete instances are listed beneath them.

- (a) **Rule, recognition test, and the four instances in one line**
  *(recommended)*. There are four, they have been stable, and a reader who has
  just been told "some headings are matched literally" wants to know which ones
  without opening three skills. The recognition test carries the durability, so
  the list going out of date costs nothing structural.
- (b) Rule and recognition test only. Nothing to keep in sync, but every reader
  re-derives the list, and the one who does it wrong translates a marker.

Rejected in the same fork: adding a pointer at each marker site in
`/qa-checklist` and `/squash-message` instead of one enumeration. Three copies
of one constraint is the drift this repo's own doc rules name, and `CLAUDE.md`
is always loaded, so a session writing either body already has the rule.

## DRY notes

- **The surface table is stated once**, in `CLAUDE.md` § "Language".
  `ADOPTING.md`, `/detemplate` and the catalog cite that section rather than
  restating a row of it — the discipline § "Vetting" already holds, where
  `scripts/vet.sh`, `ADOPTING.md` and the catalog all point at one home for the
  exit rule instead of each carrying a copy.
- **The marker rule is stated once**, in § "Working with skills", and no pointer
  is added at the marker sites. Its recognition test exists precisely so the
  enumeration is not the load-bearing half; the alternative — registering each
  new marker centrally — is a second thing to keep in sync.
- **Splitting 1a from 1b is the opposite of duplication.** They read as one
  topic and have to live apart: 1a is deleted by most adopters, 1b by none. Kept
  in one section, the deletion takes the invariant with it, and the projects most
  likely to delete (English-only) are exactly the ones the reword half still
  binds.
- **The byte-counting caveat is stated once**, in `ADOPTING.md`, the one file
  where the issue link can legitimately live. Not duplicated into `CLAUDE.md`,
  where it would travel into adopters' trees and outlive #53.
- **The deletion receipt reuses `upstream.json`'s `declined` map** rather than
  introducing a record of its own. `ADOPTING.md` already requires a decision
  recorded there either way (G4), already requires the reason phrased as a
  present-tense condition, and `/sync-agent-infra` already re-offers an entry
  whose condition stopped holding — which is the whole mechanism a re-openable
  language decision needs. A new field, or a comment in `CLAUDE.md` saying the
  section was considered and dropped, would be a second record with none of that
  behavior.
- **No shared abstraction is extracted for "hydration item."** The three — G6
  stubs, `scripts/vet.sh`, and now this — are linked by citation rather than by a
  mechanism, and each has its own enforcement story: assertion 4, the exit
  contract, and the `declined` map. A doc collecting all three would be a new
  top-level doc whose only content is pointers, stale the moment any of them
  moves. `ADOPTING.md`'s shared tail already *is* that checklist, in the one
  place an adopter reads sequentially, which is why the new step goes there and
  nowhere else.
- **`/detemplate` and `ADOPTING.md` genuinely duplicate here, and that is
  pre-existing and correct.** The fork route and the subset route ask the same
  question of different trees, and the skill's copy differs where it matters: it
  has the brief's language as evidence, where `ADOPTING.md`'s reader has a repo
  with a history of its own to inspect. Each is written to its own reader rather
  than one hedged statement covering both — the split that file's § "Template
  fork" pointer already makes for the watermark, `vet.sh`'s exit, and the
  catalog's ordering.

## Verification

No stack, so the vet run is the two built-in checks:

- `bash scripts/vet.sh` exits 0 (no reference added or removed, so assertion 1
  is unchanged; no skill added, so assertion 3 is unchanged).
- `grep -n '^## Language' CLAUDE.md` returns one line, and the marker subsection
  sits under § "Working with skills", not under it.
- Read § "Language" cold and check the six surfaces are each decidable from it —
  the failure the issue names is an adopter answering "the docs are in X" and
  then drifting on transient artifacts or conversation.
- Read § "Markers are not yours to reword" as an English-only adopter and check
  it still binds. If it only makes sense to someone translating, it is in the
  wrong voice for its new home.
