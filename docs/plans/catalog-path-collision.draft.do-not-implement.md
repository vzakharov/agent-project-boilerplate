> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Move the catalog out of a path an adopter can own

## The problem

`docs/catalog.md` holds two jobs under a generic name.

- **Job A — the inventory.** One row per skill, script and file, read by
  `ADOPTING.md`'s reader and by `/sync-agent-infra` Step 4a from a fresh clone.
- **Job B — the sentinel.** Its presence is what says *this tree is the source
  repo, not an adopting one*. Three consumers key on that:
  - `scripts/check-skill-catalog.sh` — assertions 2–3 run only if the file
    exists, and assertion 4 **changes verdict** on it: catalog present → stubs
    are shipped inventory, reported and passed; absent → every unhydrated stub
    is a stowaway and fails.
  - `/spinoff` § "Two invariants" — present → refuse to run.
  - `/spinoff` Step 4's stub argument, which reasons from "the target has no
    `docs/catalog.md`".

`docs/catalog.md` is a name an adopting repo may already own, or add later: a
component catalog, a data catalog, a service catalog, a parts catalog. Nothing in
the adoption procedure would notice, because the collision arrives from the
adopter's side — the subset path never copies `docs/`, so there is no step at
which the two files meet and one of them wins.

What a false positive costs:

1. **The stub guard turns off.** Assertion 4 prints `N unhydrated stub(s),
   expected here` and exits `0` — the guard `ADOPTING.md` § Verify calls the
   reason "the G6 criterion is enforced rather than merely stated". A repo
   carrying `/release` written for somebody else's deploy path passes the vet
   run.
2. **Assertions 2–3 run against an unrelated table.** Every skill reports "has no
   row", and the obvious repair is to start writing skill rows into the product's
   catalog.
3. **`/spinoff` refuses a legitimate adopter**, citing a `README.md` section that
   does not exist in their repo.

## The decision

Move the file to **`.claude/skills/sync-agent-infra/catalog.md`** — namespaced
where nothing but this infrastructure can claim the path, and beside the sync
skill that reads it from a clone on every run.

The cost of that home is that the file now sits inside the one tree acquisition
copies wholesale, so it can ride along into a repo that must not have it. Three
things make that acceptable, in order of how much they carry:

- **A leaked copy announces itself on the first vet run.** The catalog carries a
  row for `ADOPTING.md`, a `never` disposition that guarantees no adopter has the
  file, plus a row per path any given adopter declined. Assertion 3 requires
  every row's path to exist, so a tree holding a catalog it should not have fails
  on rows it can never satisfy. `ADOPTING.md` § Verify and `/spinoff` Step 4.2
  both run the script, so the failure lands at the moment of the leak rather than
  at some later vet.
- **The copy steps exclude it by name.** `/spinoff` Step 4's "copies → `main`"
  bullet and `ADOPTING.md` Step 4's copy instruction both name
  `.claude/skills/**` as a unit; each gains the carve-out.
- **The file says so itself.** A banner at the top states that it describes the
  source repo, is never vendored, and should be deleted by anyone who finds it in
  a tree that adopted this infrastructure. It is the one home that a leaked copy
  is guaranteed to carry, and it heads off the misdiagnosis the loud failure
  invites: pruning the catalog's rows to match the local tree, which would leave
  the sentinel permanently wrong instead of removing it.

Presence still answers both questions with one file, and it stays sound down the
chain: a fork of this repo that keeps shipping stubs genuinely *has* a catalog,
which is the semantics assertion 4 wants.

## Alternatives considered

Two were ruled out. **Renaming in place** (`docs/agent-infra-catalog.md`) fixes
the collision by name alone and keeps the file out of every copy path, but leaves
the inventory in a directory that carries no signal about who owns it, and gives
up the co-location with the skill that reads it. **Keeping the path and verifying
the content** (a marker line the script checks before trusting the file) is a
three-line diff, but it only reaches the script: `/spinoff`'s refusal and
`/sync-agent-infra` Step 4a are prose, read by an agent doing a bare existence
test, so the check has to be restated in prose at each site — weaker than a path
that cannot be confused. **Splitting the sentinel from the inventory** (a
dedicated marker file or a `role` field) adds a file that must be pruned at
adoption time, and an omitted prune fails silently — reintroducing the defect
this change removes.

## Steps

1. `git mv docs/catalog.md .claude/skills/sync-agent-infra/catalog.md`.
2. Add the non-vendoring banner as the file's first block, above the `H1`.
3. `scripts/check-skill-catalog.sh` — the `CATALOG` constant, the header comments
   naming the path, and the `sources` list, which drops its explicit
   `docs/catalog.md` entry: the `find .claude` branch already covers the new
   location.
4. Carve the file out of the two wholesale copy steps: `/spinoff` Step 4's
   "copies → `main`" bullet, and `ADOPTING.md` Step 4's copy instruction.
5. Repoint the prose citations: `ADOPTING.md` (~15, including the anchor links,
   whose fragments survive unchanged), `README.md`, `CLAUDE.md` (×2), `/spinoff`
   (the § "Two invariants" refusal, its restatement in Step 1, and the Step 4
   stub argument), `/sync-agent-infra` Step 4a, and `/implement`'s adopter note.
6. Update the catalog's own row in § "Never" — its first column is the path, and
   assertion 3 checks that every row's path exists.
7. Confirm nothing is stranded: `grep -rn 'docs/catalog' .` returns nothing.
8. `bash scripts/vet.sh`.

**No tombstone.** `CLAUDE.md`'s tombstone rule exists so surviving citations
resolve; step 5 leaves none pointing at the old path, history citations still
resolve at their own SHAs, and `git log --follow` tracks the move. This is a
move, not a retirement.

## Risk: an adopter's next sync

A downstream repo's vendored `/sync-agent-infra` Step 4a still says the source's
inventory is at `docs/catalog.md`. That instruction is itself one of the things
their next sync ports, so the break is self-healing exactly one sync late — and
in the meantime the failure is "the file named there is not in the clone", read
by an agent that already holds the clone and can see the new name beside it.

Accept it, and make the squash subject name the move outright, so it reads as a
`translate` verdict during their Step 4 triage rather than as an internal
tidy-up.

## DRY notes

- **Nothing is added; a path literal moves.** It appears once as a shell constant
  (`CATALOG` in `check-skill-catalog.sh`) and roughly twenty-five times as prose
  citations across `ADOPTING.md`, `README.md`, `CLAUDE.md` and four skills.
- **The prose citations are not extractable, and shouldn't be.** A document that
  says "read the catalog" without naming the path costs its reader a lookup, and
  these documents are read by agents over the network from a clone. The
  duplication is the interface. No shared "path to the catalog" constant spans
  shell and Markdown in this repo, and inventing one would be net-negative for a
  literal that changes about once.
- **One citation loses its guard and one gains coverage.** Step 3 drops the
  `sources` entry because the `find .claude` branch subsumes it — a deduplication
  the move makes available, not a separate cleanup. Assertion 3 still asserts
  that every path named in a catalog row exists, which catches step 6 if it is
  forgotten. The remaining citations are unguarded prose, and step 7's grep is
  their check — a one-time completeness sweep, not a new invariant. Do **not**
  add a "no file mentions the old path" assertion: its subject stops existing the
  moment this commit lands.
