> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Give the catalog a collision-proof path

## The problem

`docs/catalog.md` holds two jobs under one generic name.

- **Job A — the inventory.** One row per skill, script and file, read by
  `ADOPTING.md`'s reader and by `/sync-agent-infra` Step 4a from a fresh clone.
- **Job B — the sentinel.** Its presence is what says *this tree is the source
  repo, not an adopting one*. Three consumers key on that:
  - `scripts/check-skill-catalog.sh` — assertions 2–3 run only if the file
    exists, and assertion 4 **changes verdict** on it: catalog present → stubs
    are shipped inventory, reported and passed; absent → every unhydrated stub
    is a stowaway and fails.
  - `/spinoff` § "Not from the boilerplate" — present → refuse to run.
  - `/spinoff` Step 4's stub argument, which reasons from "the target has no
    `docs/catalog.md`".

`docs/catalog.md` is a name an adopting repo may already own, or add later: a
component catalog, a data catalog, a service catalog, a parts catalog. Nothing in
the adoption procedure would notice, because the collision arrives from the
adopter's side — the subset path never copies `docs/`, so there is no step at
which the two files meet and one of them wins.

What a false positive costs, worst first:

1. **The stub guard turns off, silently.** Assertion 4 prints `N unhydrated
   stub(s), expected here` and exits `0`. That guard is what `ADOPTING.md`
   § Verify calls the reason "the G6 criterion is enforced rather than merely
   stated". A repo carrying `/release` written for somebody else's deploy path
   now passes the vet run.
2. **Assertions 2–3 run against an unrelated table.** Loud, but it points the
   wrong way: every skill reports "has no row in docs/catalog.md", and the
   obvious repair is to start writing skill rows into the product's catalog.
3. **`/spinoff` refuses a legitimate adopter**, citing a `README.md` section that
   does not exist in their repo.

## The decision

Rename the file to **`docs/agent-infra-catalog.md`** — collision-proof by name,
still in `docs/`, still one file doing both jobs.

`docs/` is load-bearing here, and it is the reason not to move the file into a
skill directory. **No acquisition path copies `docs/`**, so the catalog's absence
downstream is structural rather than a step someone has to remember. That
property is what makes the sentinel trustworthy, and it survives the rename
untouched.

## Alternatives considered

**Under `.claude/skills/sync-agent-infra/` — the suggestion this plan answers.**
Rejected for one footgun: it makes the sentinel *vendorable by accident*. A skill
directory is the middle of the one tree every acquisition path copies wholesale —
`/spinoff` Step 4 puts `.claude/skills/**` on the target's `main` in a single
commit, and a subset adopter copies chosen skill directories with whatever is
inside them. The catalog rides along, the target reads as "the source repo", and
failure mode 1 above ships *from our own procedure* rather than by coincidence.
`/spinoff` Step 4's argument that a re-stubbed skill is "the single disposition
that fails the gate" stops holding at the same moment. It is patchable — "copy
`.claude/skills/**`, except this one file" — but a copy rule with a carve-out is
precisely what a mechanical `cp -r` misses.

Ownership is the second reason. The catalog's first audience is `ADOPTING.md`'s
reader, who may legitimately decline the sync skill (`ADOPTING.md` sanctions
deleting it outright for a one-time snapshot). Filing the inventory inside that
skill says the sync owns it; the sync is one of its two readers.

**`.claude/catalog.md`.** Avoids the skill-directory drag and is unmistakably
agent-owned, but sits one `cp -r .claude` from the same problem, and puts a
prose document that humans read in the config tree.

**Keep the path, verify the content.** Have the script confirm the file is *our*
catalog — a marker comment, or its `H1` — before treating it as the sentinel. A
three-line diff with no citation churn, and it fully fixes consumer 1. It does
not fix the other two, which are **prose**: `/spinoff`'s refusal is an agent
reading "if the caller has `docs/catalog.md`, stop" and running a bare existence
test. Restating a content check in prose is weaker than a name that cannot be
confused in the first place, and it leaves `ADOPTING.md`'s links reading — from
the adopter's chair — as though `docs/catalog.md` were a generic thing.

**Split the sentinel from the inventory** (a dedicated marker file, or a `role`
field, saying "this is the source repo"). Not worth it. Once the path cannot
collide, presence is a sound proxy for the question, and it stays sound down the
chain: a fork of this repo that keeps shipping stubs genuinely *has* a catalog,
which is the semantics assertion 4 wants. A second marker is one more file to
prune at adoption time, and an omitted prune fails **silently** — reintroducing
the exact defect this change removes.

## Steps

1. `git mv docs/catalog.md docs/agent-infra-catalog.md`.
2. `scripts/check-skill-catalog.sh` — the `CATALOG` constant, the entry in the
   `sources` list, and the three header comments that name the path.
3. Repoint the prose citations: `ADOPTING.md` (~15, including the anchor links,
   which survive the rename unchanged), `README.md`, `CLAUDE.md` (×2),
   `/spinoff` (the § "Two invariants" refusal, its restatement in Step 1, and the
   Step 4 stub argument), `/sync-agent-infra` Step 4a, and `/implement`'s
   adopter note.
4. Update the catalog's own row in § "Never" — its first column is the path, and
   assertion 3 checks that every row's path exists.
5. Confirm nothing is stranded: `grep -rn 'docs/catalog' .` returns nothing.
6. `bash scripts/vet.sh`.

**No tombstone.** `CLAUDE.md`'s tombstone rule exists so surviving citations
resolve; step 3 leaves none pointing at the old path, history citations still
resolve at their own SHAs, and `git log --follow` tracks the move. This is a
rename, not a retirement.

## Risk: an adopter's next sync

A downstream repo's vendored `/sync-agent-infra` Step 4a still says the source's
inventory is at `docs/catalog.md`. That instruction is itself one of the things
their next sync ports, so the break is self-healing exactly one sync late — and
in the meantime the failure is "the file named there is not in the clone", read
by an agent that already holds the clone and can see the new name beside it.

Accept it, and make the squash subject name the rename outright, so it reads as a
`translate` verdict during their Step 4 triage rather than as an internal
tidy-up.

## DRY notes

- **Nothing is added; a path literal moves.** It appears once as a shell constant
  (`CATALOG` in `check-skill-catalog.sh`, plus the `sources` list entry) and
  roughly twenty-five times as prose citations across `ADOPTING.md`, `README.md`,
  `CLAUDE.md` and four skills.
- **The prose citations are not extractable, and shouldn't be.** A document that
  says "read the catalog" without naming the path costs its reader a lookup, and
  these documents are read by agents over the network from a clone. The
  duplication is the interface. No shared "path to the catalog" constant spans
  shell and Markdown in this repo, and inventing one would be net-negative for a
  literal that changes about once.
- **The existing check already covers the one citation that matters.** Assertion
  3 asserts that every path named in a catalog row exists, which catches step 4
  if it is forgotten. The remaining citations are unguarded prose, and step 5's
  grep is their check — a one-time completeness sweep, not a new invariant. Do
  **not** add a "no file mentions the old path" assertion: its subject stops
  existing the moment this commit lands.
