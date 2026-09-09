> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #40 — Decouple the boilerplate from a source repo

Issue export: `docs/issue/40/issue.md`. Closes #40.

This repo is the origin of the agent infrastructure its adopters run. `/sync-upstream`
is written as one link in a chain with a source above it, and
`.claude/skills/sync-upstream/upstream.json` names `Playgramai/playgramapp` —
now itself an adopter of this repo. Two adopters each naming the other as source
is a loop with no root. The change says this repo has no upstream.

The skill's *procedure* is not the problem — an adopter needs exactly it. What
goes is the claim that this repo runs it.

## Step 1 — Rename the directory

`git mv .claude/skills/sync-upstream .claude/skills/sync-agent-infra`

The name the skill's own `🏷️ Rename it if the name misleads in your repo` banner
already recommends, and what an adopter calls the job.

## Step 2 — Rewrite the skill as a stub

`.claude/skills/sync-agent-infra/SKILL.md`.

**Both stub markers must be set together** — `scripts/check-skill-catalog.sh`
assertion 4 fails either way round. So in the same edit:

- `description:` opens with `STUB — not yet hydrated for this project.` and names
  the watermark as what hydration fills in.
- The body's first line is a `> ⚠️ **STUB.**` banner replacing *both* current
  banners (`🔁 REPOINT ON ADOPTION`, `🏷️ Rename it if the name misleads`).

The banner names the fields to fill in, that `repo` is already right, and the
delete-instead condition:

> ⚠️ **STUB.** This skill has no watermark to run on. Before it can be invoked,
> fill in `.claude/skills/sync-agent-infra/upstream.json`: `lastSyncedSha` (the
> source's HEAD when you cloned it), `lastSyncedAt`, and the real
> `adopted`/`declined` sets for your repo. `repo` already names the boilerplate,
> and needs changing only if you adopted from a repo that itself adopted from it.
> Delete this banner once you have, and drop `STUB` from the description above.
> If you took a one-time snapshot and do not intend to re-sync, delete the skill
> instead.

**Hydration here is a handful of JSON fields, not a procedure.** Unlike the other
stubs, every step below the banner is usable as written. The banner and the
catalog row both say so, because "unhydrated stub" otherwise reads as "no
procedure".

**Keep**, unchanged in substance:

- § "The watermark" — the JSON structure and the `adopted` / `declined` contract,
  including the `{path: note}` form, the "a declined path is not declined forever"
  rule, and the two `lastSyncedSha` rules (source HEAD, not last-taken; bump in the
  last commit).
- Both invariants: never sync the watermark file itself; judge the diff, not the
  commit message's "we".
- The Step 4 verdict table and "the source's fix may not be this repo's fix".
- Step 4a (new skills get offered, not taken).
- Step 5's apply-by-intent-not-by-patch rule.
- Step 2's clone recipe in full — the `clone -c` credential-helper trap, the
  blobless-partial-clone rationale, the `--depth` warning, the `cwd`-resets note.
  This is the highest-value paragraph in the file for an adopter and the one they
  would otherwise rediscover the hard way.
- Steps 1, 3, 6, 7, 8 and § "Add what the next sync teaches you". Step 1's
  stop-on-a-placeholder-`lastSyncedSha` check is what makes the shipped
  placeholder watermark safe to carry, so it stays exactly as written.

**Drop:**

- § "What this skill is for"'s bidirectional framing: `"Upstream" is relative to
  the repo you are standing in`, the three-link walk-through, and `For the
  boilerplate repo, the source is the application repo its infrastructure was
  extracted from`. With no upstream there is no direction left to relativize.
  What replaces it is the flat statement of the job: *pull the vendored agent
  infrastructure forward from the repo I took it from.*
- The `🏷️ Rename it` banner entirely. Once the shipped name *is*
  `/sync-agent-infra`, its advice is already taken and its rationale describes a
  name that no longer exists here.

The five `@`-references (`/dry`, `/tighten-docs`, `/pr`, `/override-gh`,
`/squash-message`) all survive, so assertion 1 stays satisfied.

## Step 3 — Rewrite `upstream.json` as the adopter's template

`.claude/skills/sync-agent-infra/upstream.json`, kept rather than removed, with
`repo` pre-pointed at this repo — correct for every adopter — and every per-repo
field a visible placeholder:

```json
{
  "repo": "vzakharov/agent-project-boilerplate",
  "lastSyncedSha": "<the source's HEAD at the moment you cloned it>",
  "lastSyncedAt": "<YYYY-MM-DD>",
  "adopted": ["<the paths you took — see the skill's § The watermark>"],
  "declined": {}
}
```

What this drops is the live state: `Playgramai/playgramapp` as `repo`, the
resolved `lastSyncedSha`, and the everything-case `adopted` set with its five
port notes. Those describe a source this repo does not have.

The placeholder `lastSyncedSha` is the tripwire, not a formality — the skill's
Step 1 stops on it, so an unhydrated tree cannot run a sync against a foreign
history. Nothing machine-checks the placeholder (see open question 3).

## Step 4 — Repoint every pointer

`bash scripts/check-skill-catalog.sh` catches a dangling `@`-reference but not a
stale prose mention, so the sweep is by grep. Sites, from
`grep -rn "sync-upstream\|upstream" --include='*.md' --include='*.sh' --include='*.json' .`:

| File | Line | Change |
| --- | --- | --- |
| `CLAUDE.md` | 163 | Index entry: rename, drop the "every link in the chain" framing, say it ships as a stub. |
| `CLAUDE.md` | 179 | § "Stubs awaiting hydration": Seven → Eight, add `/sync-agent-infra`, and carve it out — the section says "the procedure is inherently project-specific", which is false here: the procedure is universal and only the watermark is per-repo. |
| `README.md` | 7 | `**26 skills** (19 working out of the box, 7 stubs)` → the true counts: 28 skills, 20 working, 8 stubs. Already stale by two before this change. |
| `README.md` | 17 | `**G0**` row: say the sync path ships as a stub whose hydration is the watermark. |
| `README.md` | 23 | `Seven stack-bound stubs` stays accurate for G6 — the eighth stub is in G0, which line 17 now says. |
| `README.md` | 79–81 | `later changes here come forward with /sync-upstream, pointed at this repo by your own upstream.json` → name `/sync-agent-infra` and say the adopter fills the shipped watermark in. |
| `ADOPTING.md` | 55 | `wrong for /sync-upstream` → `/sync-agent-infra`. |
| `ADOPTING.md` | 283–290 | § "Repoint the sync watermark" → § "Hydrate the sync stub": fill in the placeholder fields *and* clear both stub markers. The "inheriting the clone's copy points your sync at a repo you cannot read" warning is now wrong — the shipped `repo` is right; what must not be inherited is the placeholder SHA. |
| `ADOPTING.md` | 327 | `pulling later changes forward is just /sync-upstream — … Nothing further to install` → the same, once hydrated per the section above. |
| `ADOPTING.md` | 463 | Verification item 3 (`The watermark names your source`) → name the new path, and check `lastSyncedSha` is no longer a placeholder. |

`ADOPTING.md` § "Go through the G6 rows" (~line 275) covers the G6 stubs only, so
the sync stub's hydrate-or-delete instruction stays in its own section — which is
what § "Hydrate the sync stub" becomes.

## Step 5 — `docs/catalog.md`

**G0 stays, holding both rows.** Its prose is rewritten around the stub: the sync
path ships unhydrated because this repo has no source, hydrating it is the
watermark, and skipping the group still leaves you with a snapshot. It cites G6's
hydrate-now-or-delete rule rather than restating it.

- The `/sync-upstream` row is renamed in place, with an accurate `Pulls in` — the
  current row omits `/squash-message`, which Step 8 `@`-references — and a
  `Requires` that names hydration:

  | Item | What it does | Requires | Pulls in | Disposition |
  | --- | --- | --- | --- | --- |
  | `/sync-agent-infra` | Pull the agent infrastructure forward from the repo you adopted it from: diff since the watermark, triage commit by commit, port what applies. | `gh`, `$GH_TOKEN`, git transport to the source repo; hydration (the watermark) | `/dry`, `/tighten-docs` (G1); `/pr`, `/squash-message` (G2); `/override-gh` (G4) | adopt |
  | `.claude/skills/sync-agent-infra/upstream.json` | The watermark: which repo you sync from, the SHA you last synced to, and what you adopted or declined. Ships pointed at this repo with the rest as placeholders. | — | — | **rewrite** |

- The § "Groups" table's G0 row gains the hydration clause.
- § "Three dispositions, not two" keeps `rewrite` at exactly two files, but its
  rationale changes: the shipped watermark now names a repo the adopter *can*
  read and which *is* their source, so what the disposition prevents is
  inheriting a placeholder SHA and a foreign `adopted` set — not a wrong repo.
- **Line 12** (`/sync-upstream`, on every run) → rename; that reader is the
  hydrated skill in an adopter's tree, which is still exactly who reads the
  catalog on every run.
- **Line 279** (three skills *name* `scripts/vet.sh`) → rename the mention.

Unchanged, because the row stays in G0: the G6 intro, its "three of them tell you
when to delete the skill outright instead", line 175's `/sync-upstream` **(G0)**
parenthetical (renamed, group unchanged), the § "Closure is not optional" bullet
`/override-gh` is pulled in by G0 and G3`, and every `#g0--the-sync-path` /
`#g6--stack-stubs` anchor.

## DRY notes

Nothing is extracted or newly shared; the change is a rename plus a
this-repo-has-no-source rewrite over prose that already exists once each.

- **The watermark's contract has exactly one home** and keeps it:
  `.claude/skills/sync-agent-infra/SKILL.md` § "The watermark". `upstream.json`
  is now an instance of that contract with placeholder values, and
  `ADOPTING.md` § "Hydrate the sync stub" is a worked filling-in of the same
  instance — the relationship all three have today. No new duplicate appears,
  and the JSON example in the skill stays the schema statement.
- **One risk this answer creates, and the mitigation:** a placeholder watermark
  and a documented schema are now two JSON blocks that must agree on field names.
  They already were (the skill's example vs. the live file), so the count is
  unchanged — but the skill's example is the one that may add a field, and the
  template must follow. Open question 3 is the machine-checked version of that
  coupling; without it, it is a review-time concern.
- **Group rationale is not duplicated.** G0's rewritten prose cites G6's
  hydrate-or-delete rule rather than restating it, so the rule has one home even
  though a stub now lives outside G6.
- **The skill count is stated in three places** (`README.md`'s prose and its G6
  table row, `CLAUDE.md` § "Stubs awaiting hydration") and this change touches
  two. Not worth extracting: the numbers are prose in two documents with
  different audiences and no build step that could derive them, and
  `scripts/check-skill-catalog.sh` already enforces the invariant that matters
  (one catalog row per skill directory). It does not count stubs against a stated
  total, and adding that assertion is a separate change — if the drift found here
  (26/19/7 against an actual 28/21/7) recurs, that is the fix, filed separately.
- **No new script.** The pointer sweep in Step 4 is a one-off grep, not a check
  worth codifying: assertion 1 already covers the failure mode that is silent, and
  a stale prose mention is visible in review.

## Verification

1. `bash scripts/check-skill-catalog.sh` exits `0`. It is the load-bearing check
   here: assertion 1 for the five surviving `@`-references and every renamed
   pointer, assertion 2 for the renamed catalog row (a rename with a missed row
   fails as "no row" *and* the old row fails assertion 3), assertion 3 for the
   `upstream.json` row's path, assertion 4 for the two stub markers agreeing.
2. Break each stub marker in turn and confirm assertion 4 fails with the matching
   message, then restore. Both directions, since the assertion has two.
3. `grep -rn "sync-upstream" --include='*.md' --include='*.sh' --include='*.json' .`
   returns nothing outside `docs/issue/40/`.
4. `python3 -c "import json;json.load(open('.claude/skills/sync-agent-infra/upstream.json'))"`
   parses, and `grep -c '<' ` on it shows the placeholders are visibly unfilled.
5. `grep -rn "Playgramai" .` returns nothing outside `docs/issue/40/`.
6. Every anchor cited across the docs still resolves: `#g0--the-sync-path`,
   `#g6--stack-stubs`, `#three-dispositions-not-two`, `#closure-is-not-optional`.
7. `./scripts/vet.sh` — a no-op in this repo, run by `/finalize` regardless.

## Resolved forks

- **`upstream.json` kept as a template**, `repo` pre-pointed at this repo so the
  one field every adopter shares arrives correct and the rest are theirs to fill.
  Ruled out: deleting the file (the issue's stated preference, and this plan's
  first recommendation) — it leaves the catalog with no path to name, makes the
  adopter create a file rather than edit one, and drops the `rewrite` disposition
  to a single qualifying file; and an empty `repo`, which throws away the one
  value that is knowable at ship time.
- **The `🏷️ Rename it if the name misleads` banner is dropped entirely**, its
  advice having been taken by the rename itself.

## Open questions

Answerable tersely. The plan above is written with every recommendation already in
force, so silence is a valid resolution.

**1. Does the row stay in G0, against the issue's §4 which moves it to G6?**

- **(a) Stay in G0 — recommended, and what this plan is written for.** Three
  reasons. The `upstream.json` row stays in the catalog now that the file does, so
  G0 is not empty and the question the issue was answering ("what's left of G0?")
  does not arise. G0 is a *group-level* decision — "do you want future updates at
  all?" — which is a different shape from G6's per-row hydrate-or-delete, and the
  group-level version is the one an adopter needs to answer first. And it is the
  cheaper diff: G6's intro, its delete-instead count, catalog line 175, the
  `/override-gh`-travels-beyond-G4 bullet and both anchors all stay put.
- (b) Move it to G6 per the issue, leaving G0 holding only the watermark row —
  a group named "the sync path" that does not contain the sync skill.
- (c) Move both rows to G6 and delete G0. Coherent, but it loses the group-level
  framing above, which is the objection that reopened this.

**2. Does `adopted` ship as a placeholder string, or as a plausible starter set?**

- **(a) Placeholder — recommended.** `["<the paths you took — see the skill's
  § The watermark>"]` is unmistakably unfilled, and the skill's § "The watermark"
  is one scroll away with a real example.
- (b) A starter set (`["CLAUDE.md", ".claude/", "scripts/"]`), which is closer to
  what most adopters end up with. Costs the tripwire: a plausible-looking value is
  one an adopter can leave standing without noticing, and `adopted` being wrong is
  silent — it under-filters the log rather than erroring.

**3. Machine-check the template's unhydrated state? (Beyond the issue.)**

- **(a) File it as a follow-up issue instead — recommended.** Assertion 4 already
  establishes the idiom this would use: `docs/catalog.md` present means the source
  repo, where `lastSyncedSha` **must** still be a placeholder; absent means an
  adopting tree, where it must **not** be. That is ~15 lines and it forecloses
  exactly the failure that produced #40 — a live watermark shipped from the
  source. But it is a new assertion in a script this issue does not otherwise
  touch, so it widens the PR on the agent's judgement rather than yours.
- (b) Fold it into this PR, since the decoupling and the check that keeps it
  decoupled are one thought.
