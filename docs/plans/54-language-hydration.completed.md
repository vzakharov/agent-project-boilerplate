# #54 — the language decision joins the hydration set

Source: `docs/issue/54/issue.md`.

An adopting project routinely has human readers in one language and an
agent-facing instruction set in another, and nothing upstream tells it to decide
that. So the decision gets made implicitly, one file at a time, by whichever
session wrote that file. This change makes it an explicit hydration item, exactly
as the G6 stubs are — but a narrow one: **the adopter answers one line, and the
two groups nobody should be asked about are stated for them.**

## What ships

Six files, all prose. In this repo prose about the loop *is* the product, so per
`CLAUDE.md` § "Git conventions" every commit here is `feat:`, not `docs:`.

### 1. `CLAUDE.md` — a new `## Language` section

Placed after § "Writing things down" and before § "Working with skills": the
decision is about what prose gets written in, so it sits beside the section
governing whether prose gets written at all.

A stub blockquote in the voice of § "About this project" and § "Testing", asking
for the one thing that varies:

> _Replace this stub with the language your team reads — one line. "English" is
> an answer, not a step you skipped._

Then three groups, of which only the first is a question:

- **Human-facing — the decision.** `README.md` and anything else a person reads
  to decide something, commit subjects and bodies, PR titles and bodies, and the
  plans and issue exports published for review. It takes the language **the
  team** reads, which is not automatically the one a given session runs in.
- **Agent-facing — English.** `CLAUDE.md`, `.claude/skills/**`,
  `.claude/rules/**`, and code. The skills cite each other's headings and match
  some strings literally, so translating them breaks the loop rather than
  localizing it.
- **Conversation — the language the exchange opened in.** Session replies, issue
  and PR comments, review replies. No standing artifact, so each follows the
  person asking.

The last two are stated rather than asked, and a session settles them by reading
the section. They remain overridable — a team that wants its skills in its own
language writes that here — but an override is a decision someone makes, not a
blank left open.

**The section is fill-only, not deletable.** Groups 2 and 3 live in it, so an
English-only project writes "English" on the first line and keeps the rest: it is
where a session reads the two defaults off. That is what makes it unlike a G6
stub, which has nothing left once its answer is "no".

### 2. `ADOPTING.md` — a shared-tail step

A new § "Settle the language decision" between § "Reconcile `CLAUDE.md` rather
than overwrite it" and § "Implement `scripts/vet.sh`" — the tail runs prose,
then vet, then stubs, and this is a prose decision. It cites `CLAUDE.md`
§ "Language" as the home rather than restating the groups, says the answer is one
line, and notes that the section stays in the tree even when that answer is
"English".

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
  it a question; all-English makes it a confirmation — which the plan **states
  either way**, never leaves inferred, since an operator whose team reads
  something other than the brief's language has one place to say so.
- **Step 4 (what the plan must contain)** gains the language answer, next to
  `scripts/vet.sh`'s disposition.
- **Step 5 (execution order)** — item 4 already fills `CLAUDE.md`'s "About this
  project" stub from the brief, and replaces § "Language"'s stub in the same
  breath with the one-line answer.

### 4. `.claude/skills/spinoff/SKILL.md` — the sibling re-decides

`CLAUDE.md` is already a rewrite in the travel triage. One clause where that
list appears: the caller's language decision is a candidate default for the
sibling, not an inheritance — a sibling can serve a different audience than the
repo it was pushed out of — so the target re-decides that one line rather than
copying it across.

### 5. `.claude/skills/sync-agent-infra/catalog.md` — keep G1 accurate

Two edits, no new rows:

- The `CLAUDE.md` row's "What it does" lists the file's sections; add the
  language decision.
- The G1 prose paragraph after the table, which owns the donor-not-replacement
  note, gains a sentence: § "Language" is hydrated rather than merged — one line
  naming the language the team reads, the rest of the section holding whatever
  the project.

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
- **A worked example naming a repo.** The three groups carry the content; a
  citation would date the section to whoever reported it, and the improvement is
  general.
- **A machine check that the stub was replaced.** `check-skill-catalog.sh`
  asserting the blockquote is gone would mirror assertion 4's stub-marker check,
  but it would have to be keyed on the catalog's absence to avoid failing in this
  repo — where the stub is the shipped state — putting a second copy of
  `/detemplate` Step 0's predicate in a script with no other reason to know about
  forks. The sibling stubs (§ "About this project", § "Repository layout",
  § "Testing") are enforced by prose alone, and this one is too.
- **Any language split in this repo's own tree.** The boilerplate is
  English-only, and its § "Language" ships stubbed exactly as § "About this
  project" does. Carrying a split here would stop it being a decision.

## Resolved forks

- **No repo is named as the reporting example.** A citation would date the
  section to whoever reported it; the improvement is general.

**Reversed at PR review, and what shipped instead.** Two of the three forks above
were decided the other way once the section was on the page:

- **The six-surface table is gone; three groups replace it**, and only one of
  them is a question. Human-facing prose takes the team's language; agent-facing
  files are English; conversation follows the exchange it opened in. The last two
  are stated rather than asked — overridable by a project, but never a blank left
  open — so what the operator answers is one line.
- **§ "Language" is fill-only, not deletable.** With groups 2 and 3 living in it,
  the section has to be there for a session to read them off; an English-only
  project writes "English" and keeps it. That retires the `declined`-map route,
  which existed only to record the deletion.
- **§ "Markers are not yours to reword" is not added at all.** An agent minded to
  reword a marker greps for it, and the translation case it guarded is now
  covered structurally: agent-facing files are English, so the strings the skills
  match are never translated in the first place.

## DRY notes

- **The three groups are stated once**, in `CLAUDE.md` § "Language".
  `ADOPTING.md`, `/detemplate` and the catalog cite that section rather than
  restating a group of it — the discipline § "Vetting" already holds, where
  `scripts/vet.sh`, `ADOPTING.md` and the catalog all point at one home for the
  exit rule instead of each carrying a copy.
- **The byte-counting caveat is stated once**, in `ADOPTING.md`, the one file
  where the issue link can legitimately live. Not duplicated into `CLAUDE.md`,
  where it would travel into adopters' trees and outlive #53.
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
- `grep -n '^## Language' CLAUDE.md` returns one line.
- Read § "Language" cold as an operator and check that exactly one thing is being
  asked. The failure the issue names is drift on the surfaces nobody answered
  for; the failure this section's own review named is asking about surfaces that
  should never have been a question.
- Read it again as a session, and check groups 2 and 3 are usable without asking
  anyone anything — they are the two-thirds of this that must never reach the
  operator.
