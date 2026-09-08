> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Enforce squash-message size caps in the vet run

## Why

`@.claude/skills/squash-message/SKILL.md` states the target for the permanent
`git log` record as prose — "three paragraphs, four at the outside", title in one
line — and nothing measures it. A draft that lands over the target is exactly
what that skill's Step 3 exists to catch, and Step 3 is an agent reading its own
output. The caps below turn the two mechanically checkable halves of the target
into a check that fails.

Two caps, both on the proposal's copy-pasteable text:

- **Body: 50 lines**, counted inside the second fenced block. Four paragraphs
  hard-wrapped at ~72 chars plus the `Closes #N` and `Co-authored-by:` trailers
  land near 30; 50 is a ceiling that only a body which stopped being a record
  reaches.
- **Title: 78 chars**, the whole first fenced block. The format's mandatory
  ` (pr #N)` suffix eats ~10 of it, which is why this isn't the body's own ~72.

## Where the check has to live

`scripts/vet.sh` carries the **rewrite** disposition
(`docs/catalog.md` § "Three dispositions, not two") — every adopter replaces its
contents with their own stack's commands. So a check written *inside* vet.sh does
not propagate: it is precisely the text adopters delete. The check therefore ships
as its own `adopt`-as-is file that vet.sh calls in one line, and the propagation
work is making that line survive the rewrite (vet.sh's own comment header,
ADOPTING.md's vet section, a catalog row, CLAUDE.md § Vetting).

`scripts/check-squash-message.sh`, POSIX `sh`, `git` its only dependency — same
floor argument `scripts/run-parallel.sh` makes in its header: the one entrypoint
every adopter must have cannot add an interpreter or a `jq`/`gh` prerequisite.

## The trick: the file is usually gone by vet time

The proposal's working file is `docs/remove-before-merging/squash-message.md`, and
`/finalize` sweeps that whole tree at the end of step 6 — so a re-vet inside the
base-advanced deliberation (step 6 → step 2 → step 1) runs with the file deleted
and the deletion already committed. The check must read the proposal from wherever
it currently is, which is a ladder, not a path:

1. An explicit path argument, if one was passed (what `/squash-message` uses on
   the file it just wrote — no history involved).
2. `docs/remove-before-merging/squash-message.md` in the worktree.
3. `tmp/squash-message.md` in the worktree — the untracked fallback
   `/squash-message` Step 2 composes into on a branch no PR-opening lane ran on.
4. `git show HEAD:docs/remove-before-merging/squash-message.md` — the sweep staged
   or in progress but not yet committed.
5. The last commit **on this branch** that deleted the path:
   `git log --diff-filter=D -1 --format=%H <merge-base>..HEAD -- <path>`, read back
   as `git show <sha>^:<path>`. This is the swept-and-committed case, and it is the
   one the caps have to survive.
6. Nothing anywhere → print that there is no proposal to check and exit `0`. A
   branch with no PR lane has nothing to measure, and a vet run is not the place
   to demand one.

Rung 5 is bounded to `<merge-base>..HEAD` (merge base against
`refs/remotes/origin/HEAD`, or `$SQUASH_BASE_REF` when a caller knows better,
falling back to the full history when neither resolves) so that in a repo which
merges rather than squashes, a *different* branch's swept proposal — still in the
base's history — can't be picked up and measured as this branch's.

Rungs 4 and 5 reuse the recipe `/squash-message` Step 2 already states for
restoring a swept file. Same mechanic, different job — see DRY notes.

## Behavior

Parse the two fenced blocks (` ``` ` at column 0) out of whichever source the
ladder picked:

- **Title** = block 1. Fail if any non-blank line exceeds the char cap, or if the
  block holds more than one non-blank line — a squash title is one line, and a
  wrapped one pastes as a broken title.
- **Body** = block 2, trailing blank lines trimmed. Fail if the line count exceeds
  the cap.
- **Fewer than two fenced blocks** → fail. A proposal whose body can't be located
  is not pasteable; passing quietly would be the silent-swallow this repo's
  principles rule out.

Failures name the source the ladder resolved to, the measured value against the
cap, and point at `/squash-message` Step 3 as the fix. Both caps are checked in
one run, so a proposal over on both hears about both.

`SQUASH_MAX_BODY_LINES` and `SQUASH_MAX_TITLE_CHARS` override the defaults. The
escape hatch is not decoration: `/squash-message` Step 3 already exempts a release
body from the paragraph cap ("a paragraph per product area"), so a hydrated
`/release` lane raises the ceiling for its own run rather than the check going
wrong about it.

## Enforcement points

Two, and they catch different things:

- **`/squash-message` Step 3**, run on the file just tightened, before anything is
  emitted. Fails at authorship, where the fix is a rewrite that is already in
  hand — and covers `/finalize no vet`, where step 1 never runs but step 5 always
  does.
- **`scripts/vet.sh`**, at land prep. This is the gate that catches a proposal
  edited by hand, or tightened before a later base merge grew it, and the reason
  the ladder above needs its history rungs.

## Steps

1. Write `scripts/check-squash-message.sh` — the ladder, the parse, both caps, the
   env overrides. `chmod +x`.
2. Verify it by hand against each rung: the worktree file, a `tmp/` fallback, a
   staged deletion, a committed deletion, and no proposal at all. Fabricate the
   fixtures under `tmp/`.
3. Wire `scripts/vet.sh` — the call plus a header comment saying this is the one
   check in the file that is not stack-specific and must survive the rewrite.
4. Wire `/squash-message` Step 3 — the mandatory run, plus the two caps in the
   format rules and the Step 3 target where the prose target already lives.
5. Propagate to adopters: ADOPTING.md § "Implement `scripts/vet.sh`" keeps the
   line; `docs/catalog.md` gets a G2 row for the script, `scripts/vet.sh`'s row
   gains it under **Pulls in**, and the closure note for vet.sh says the call
   survives the rewrite.
6. `bash scripts/check-skill-catalog.sh`, then `/dry` and `/tighten-docs`, then
   `/pr`.

## DRY notes

- **The numbers live in two places, deliberately.** The script holds them as
  defaults (it is what fails), `/squash-message` holds them as prose (it is what
  an agent authors against). Neither can delegate to the other — a shell default
  can't teach and a skill can't measure. CLAUDE.md § Vetting and ADOPTING.md
  **point** at them and state no number, per "when a convention changes, every
  place that states it changes with it".
- **The history-recovery recipe is duplicated once, on purpose.**
  `/squash-message` Step 2 restores a swept file *to edit and re-commit*; the
  script reads a swept file *to measure*, in `sh`, with no branch to write back
  to. Extracting a shared helper would mean a script the skill shells out to for
  one `git show`, and would put the restore path — which the agent has to reason
  about while deciding whether the file it holds is the live one — behind a
  layer. They stay separate, each citing the same mechanic.
- **Not folded into `scripts/run-parallel.sh`.** That is a runner for checks, not
  a check; the new script is one of the things it would be handed.
- **Not inlined in `scripts/vet.sh`** — see "Where the check has to live": inlining
  it in a `rewrite`-disposition file is what would make it not propagate.
- Nothing else in the tree parses the proposal's fenced blocks, so the parse is
  new code with no existing home to route through.

## Open questions

Recommendations are already in force above; answers revise the plan.

1. **Title cap.** (a) **78** — recommended, and the number you named; the
   ` (pr #N)` suffix makes the body's ~72 cramped. (b) 72, literally the body's
   own wrap. (c) something else.
2. **Body line width.** (a) **Don't check it** — recommended; the wrap is stated
   as "~72" for a reason, and a long path or URL in a body is not a defect worth
   failing a vet run over. (b) Check it at the title's number too.
3. **Env overrides.** (a) **Keep them** — recommended; the release lane's
   exemption already exists in prose and needs somewhere to land. (b) Hard caps,
   no override.
4. **Enforcement points.** (a) **Both** — recommended; vet.sh alone leaves
   `no vet` docs-only PRs uncapped. (b) `vet.sh` only.
5. **No proposal found.** (a) **Exit 0 with a note** — recommended. (b) Fail: a
   branch reaching land prep with no proposal is itself the defect.
