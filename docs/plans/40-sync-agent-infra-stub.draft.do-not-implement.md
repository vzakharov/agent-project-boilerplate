> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# #40 — Decouple the boilerplate from a source repo

Issue export: `docs/issue/40/issue.md`. Closes #40.

This repo is the origin of the agent infrastructure its adopters run. `/sync-upstream`
is written as one link in a chain with a source above it, and
`.claude/skills/sync-upstream/upstream.json` names `Playgramai/playgramapp` —
now itself an adopter of this repo. Two adopters each naming the other as source
is a loop with no root. The change says this repo has no upstream, in the four
places that currently imply otherwise.

The skill's *procedure* is not the problem — an adopter needs exactly it. What
goes is the claim that this repo runs it.

## Decisions taken (open questions with recommendations are in § Open questions)

- The row lands in **G6**, disposition `adopt only if hydrating now`, per the issue.
- **`docs/catalog.md`'s `### G6 — Stack stubs` heading is left alone**, so its
  `#g6--stack-stubs` anchor keeps resolving from `ADOPTING.md` (two citations) and
  from within the catalog. The new row is bound to a *source repo* rather than a
  stack, so G6's intro gains one sentence carving that out instead of a rename.
- **The stub states its own delete-instead condition** — a repo taking a one-time
  snapshot with no intent to re-sync deletes the skill. G6's "Three of them tell
  you when to delete the skill outright instead" becomes four.
- **`CLAUDE.md` keeps a one-line index entry** under "Entry points and support",
  reworded to say it ships as a stub, *and* gains the name in § "Stubs awaiting
  hydration" (Seven → Eight). Dropping the bullet would leave the index with no
  statement of what the job is.

## Step 1 — Rename the directory

`git mv .claude/skills/sync-upstream .claude/skills/sync-agent-infra`

The name the skill's own `🏷️ Rename it if the name misleads in your repo` banner
already recommends, and what an adopter calls the job.

## Step 2 — Rewrite the skill as a G6 stub

`.claude/skills/sync-agent-infra/SKILL.md`.

**Both stub markers must be set together** — `scripts/check-skill-catalog.sh`
assertion 4 fails either way round. So in the same edit:

- `description:` opens with `STUB — not yet hydrated for this project.` and names
  what hydration means here.
- The body's first line is a `> ⚠️ **STUB.**` banner replacing *both* current
  banners (`🔁 REPOINT ON ADOPTION`, `🏷️ Rename it if the name misleads`). The
  banner names the one artifact to fill in — the watermark at
  `.claude/skills/sync-agent-infra/upstream.json` — and the delete-instead
  condition above.

**Hydration here is one file, not a procedure.** Unlike the other G6 stubs, every
step below the banner is usable as written; what is missing is the watermark. The
banner and the catalog row both say so, because "unhydrated stub" otherwise reads
as "no procedure".

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
- Steps 3, 6, 7, 8 and § "Add what the next sync teaches you".

**Drop:**

- `lastSyncedSha` as a live value — the field stays documented, this repo holds none.
- § "What this skill is for"'s bidirectional framing: `"Upstream" is relative to
  the repo you are standing in`, the three-link walk-through, and `For the
  boilerplate repo, the source is the application repo its infrastructure was
  extracted from`. With no upstream there is no direction left to relativize.
  What replaces it is the flat statement of the job: *pull the vendored agent
  infrastructure forward from the repo I took it from.*
- Step 1's "Stop and report if it is missing" framed as a runtime fault — a missing
  watermark in an unhydrated tree is the stub, not an error. Reword to read the
  watermark written at hydration.

The five `@`-references (`/dry`, `/tighten-docs`, `/pr`, `/override-gh`,
`/squash-message`) all survive, so assertion 1 stays satisfied.

## Step 3 — Remove `upstream.json`

`git rm .claude/skills/sync-upstream/upstream.json` (in the renamed directory).

The watermark is the adopter's to write, and § "The watermark" already documents
its structure with a worked example — so removal loses no documented contract. It
names a repo this one does not sync from and an `adopted` set describing nothing.

## Step 4 — Repoint every pointer

`bash scripts/check-skill-catalog.sh` catches a dangling `@`-reference but not a
stale prose mention, so the sweep is by grep. Sites, from
`grep -rn "sync-upstream\|upstream" --include='*.md' --include='*.sh' --include='*.json' .`:

| File | Line | Change |
| --- | --- | --- |
| `CLAUDE.md` | 163 | Index entry: rename, drop the "every link in the chain" framing, say it ships as a stub. |
| `CLAUDE.md` | 179 | § "Stubs awaiting hydration": Seven → Eight, add `/sync-agent-infra` to the list. |
| `README.md` | 7 | `**26 skills** (19 working out of the box, 7 stubs)` → the true counts: 28 skills, 20 working, 8 stubs. Already stale by two before this change. |
| `README.md` | 17 | Group table: the `**G0**` row goes with the group. |
| `README.md` | 23 | `Seven stack-bound stubs` → eight, seven of them stack-bound. |
| `README.md` | 79–81 | `later changes here come forward with /sync-upstream, pointed at this repo by your own upstream.json` → name `/sync-agent-infra` and say the adopter writes that watermark at hydration. |
| `ADOPTING.md` | 55 | `wrong for /sync-upstream` → `/sync-agent-infra`. |
| `ADOPTING.md` | 283–290 | § "Repoint the sync watermark" → § "Hydrate the sync stub": the adopter *writes* `.claude/skills/sync-agent-infra/upstream.json` and clears both stub markers. The "inheriting the clone's copy" warning goes — there is no copy to inherit. The JSON example's `"repo": "vzakharov/agent-project-boilerplate"` stays correct. |
| `ADOPTING.md` | 327 | `pulling later changes forward is just /sync-upstream — … Nothing further to install` → the same, once the stub is hydrated per the section above. |
| `ADOPTING.md` | 463 | Verification item 3 (`The watermark names your source`) → name the new path. |

`ADOPTING.md`'s § "Go through the G6 rows" (line ~275) already tells the adopter
to hydrate-or-delete each G6 row, so the new row is picked up by the existing
prose; it needs no new instruction beyond the § "Hydrate the sync stub" rewrite.

## Step 5 — `docs/catalog.md`

- **Delete `### G0 — The sync path`.** Both its rows leave (one moves, one is
  removed by Step 3), and its prose ("Adopting this group is what makes every
  later change at the source reachable. Skipping it leaves you with a snapshot.")
  was the group's whole rationale — it moves to the new G6 row's note, where it
  is the argument for hydrating rather than deleting. Also delete its row from the
  § "Groups" table.
- **Keep the `G1`–`G6` letters as they are.** Renumbering would churn every anchor
  and citation across `ADOPTING.md`, `README.md` and the catalog itself for no gain.
- **Add the row to G6**, with an accurate `Pulls in` — the current G0 row omits
  `/squash-message`, which Step 8 `@`-references:

  | Item | What it does | Requires | Pulls in | Disposition |
  | --- | --- | --- | --- | --- |
  | `/sync-agent-infra` | Pull the agent infrastructure forward from the repo you adopted it from: diff since the watermark, triage commit by commit, port what applies. | `gh`, `$GH_TOKEN`, git transport to the source repo; hydration (the watermark) | `/dry`, `/tighten-docs` (G1); `/pr`, `/squash-message` (G2); `/override-gh` (G4) | adopt only if hydrating now |

- **Move G0's `/pr` escape note** ("if you decline G2, strip that hand-off from the
  skill") into G6 alongside the row.
- **Delete the `.claude/skills/sync-upstream/upstream.json` row** (Step 3 removes
  the file, and assertion 3 requires every row's path to exist).
- **§ "Three dispositions, not two"**: `rewrite` now has one qualifying file, not
  two — `scripts/vet.sh`. Rewrite that paragraph, and move its "naming this
  disposition is what stops an adopter inheriting a watermark pointed at a repo it
  cannot read" clause to wherever the watermark's hydration is now stated.
- **Line 12** (`/sync-upstream`, on every run) → rename; that reader is the
  hydrated skill in an adopter's tree, which is still exactly who reads the catalog
  on every run.
- **Line 175** (`/override-gh` travels beyond G4) → `(G0)` becomes `(G6)`.
- **Line 279** (three skills *name* `scripts/vet.sh`) → rename the mention.
- **G6 intro**: one sentence carving out the new row as bound to a source repo
  rather than a stack, and "Three of them tell you when to delete the skill
  outright instead" → four.

## DRY notes

Nothing is extracted or newly shared; the change is a rename plus a
this-repo-has-no-source rewrite over prose that already exists once each.

- **The watermark's structure has exactly one home**, and this change preserves
  that: `.claude/skills/sync-agent-infra/SKILL.md` § "The watermark". The JSON in
  `ADOPTING.md` § "Hydrate the sync stub" is a filled-in example of an adopter's
  own values, not a second statement of the contract — the same relationship it has
  today. Deleting `upstream.json` removes the *instance*, not the schema, so no
  duplicate appears.
- **Group rationale is not duplicated into two groups.** G0's "skipping it leaves
  you with a snapshot" argument moves rather than being copied, so there is one
  place stating why an adopter hydrates this stub.
- **The skill count is stated in three places** (`README.md`'s prose and its G6
  table row, `CLAUDE.md` § "Stubs awaiting hydration") and this change touches all
  three. Not worth extracting: the numbers are prose in three documents with three
  audiences and no build step that could derive them, and
  `scripts/check-skill-catalog.sh` already enforces the invariant that actually
  matters (one catalog row per skill directory). It does not count stubs against a
  stated total, and adding that assertion is a separate change from this one — if
  the drift found here (26/19/7 against an actual 28/21/7) recurs, that is the
  fix, filed separately.
- **No new script.** The pointer sweep in Step 4 is a one-off grep, not a check
  worth codifying: assertion 1 already covers the failure mode that is silent, and
  a stale prose mention is visible in review.

## Verification

1. `bash scripts/check-skill-catalog.sh` exits `0`. It is the load-bearing check
   here: assertion 1 for the five surviving `@`-references and every renamed
   pointer, assertion 2 for the moved catalog row (a rename with a missed row
   fails as "no row" *and* the old row fails assertion 3), assertion 4 for the two
   stub markers agreeing.
2. `grep -rn "sync-upstream" --include='*.md' --include='*.sh' --include='*.json' .`
   returns nothing outside `docs/issue/40/`.
3. `grep -rn "upstream.json" .` resolves only to prose about the watermark an
   adopter writes — no reference to a file in this tree.
4. Every anchor cited across the docs still resolves: `#g6--stack-stubs`,
   `#three-dispositions-not-two`, `#closure-is-not-optional`. `#g0--the-sync-path`
   has no surviving citation once Step 5 is done — check with
   `grep -rn "g0--the-sync-path" .`
5. `./scripts/vet.sh` — a no-op in this repo, run by `/finalize` regardless.

## Open questions

Numbered for terse replies ("1a, 2-default"). The plan above is written with every
recommendation already in force, so silence is a valid resolution.

**1. `upstream.json`: remove, or keep as an empty placeholder?**

- **(a) Remove it — recommended, and the issue's stated preference.** A watermark
  is per-repo by definition and this repo has no source, so the file has no honest
  content. The structure stays documented in the skill.
- (b) Keep it with an empty `repo`, so the catalog has a path to name and an
  adopter has a file to edit rather than create. Costs a file that describes
  nothing and a catalog row asserting a `rewrite` disposition over a placeholder.

Step 3 and the `rewrite`-paragraph edit in Step 5 both change under (b).

**2. G0: delete the group, or keep it with the stub row in it?**

- **(a) Delete G0 and put the row in G6 — recommended, per the issue.** The row is
  a stub and G6 is the stubs group; "adopt only if hydrating now" is exactly G6's
  rule. G0 has no content left.
- (b) Keep G0, holding the one stub row, with its prose rewritten around
  hydrating the watermark. Argues that the sync path is a *group-level* decision
  ("always, unless you want a snapshot") rather than a per-row one, which G6's
  framing loses. Costs a group whose sole content is a stub, and keeps two places
  telling an adopter how to treat a stub.

**3. Anything worth keeping from the `🏷️ Rename it if the name misleads` banner?**

- **(a) Drop it entirely — recommended.** Once the shipped name *is*
  `/sync-agent-infra`, the banner's advice is already taken, and its rationale
  ("'Upstream' is a fork's vocabulary") is a note about a name that no longer
  exists here.
- (b) Keep a one-line version, since an adopter may still prefer
  `/sync-boilerplate` or their team's own word. Costs a banner arguing against the
  name the file already carries.
