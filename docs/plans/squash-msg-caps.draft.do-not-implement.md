> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Enforce squash-message size caps in the vet run

## Why

`@.claude/skills/squash-message/SKILL.md` states the target for the permanent
`git log` record as prose — "three paragraphs, four at the outside", a one-line
title, a body hard-wrapped at ~72 — and nothing measures it. A draft that lands
over the target is exactly what that skill's Step 3 exists to catch, and Step 3 is
an agent reading its own output. The caps below turn the mechanically checkable
part of that target into a check that fails.

Three caps, all on the proposal's copy-pasteable text:

- **Title: 80 chars.** One line; the format's mandatory ` (pr #N)` suffix eats
  ~10 of it, which is why it isn't the body's own 72.
- **Body: 50 lines.** Four paragraphs wrapped at 72 plus the `Closes #N` and
  `Co-authored-by:` trailers land near 30; 50 is a ceiling only a body that
  stopped being a record reaches.
- **Body: 72 chars per line**, making the skill's existing wrap rule real. One
  exemption, for the case that can't be satisfied: a line holding a single
  unwrappable token (a URL, a long path) — no interior whitespace — passes at any
  length.

The caps bind every lane. A project whose bodies genuinely need more room changes
the defaults in its own copy; there is no in-tree escape hatch (see the note under
DRY).

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
6. Nothing anywhere → print that there is no proposal to check and exit `0`.

Rung 5 is bounded to `<merge-base>..HEAD` (merge base against
`refs/remotes/origin/HEAD`, falling back to the full history when that ref doesn't
resolve) so that in a repo which merges rather than squashes, a *different*
branch's swept proposal — still in the base's history — can't be picked up and
measured as this branch's.

Rungs 4 and 5 reuse the recipe `/squash-message` Step 2 already states for
restoring a swept file. Same mechanic, different job — see DRY notes.

**Why rung 6 passes rather than fails.** A missing proposal is normal wherever no
PR-opening lane has run yet: `/finalize`'s pre-check opens the draft PR itself and
then vets at step 1, while `/squash-message` runs at step 5 — so a branch arriving
via `/from-branch` or `/handle` legitimately has nothing on disk at vet time.
`/sync-branch` vets a branch that may have no PR at all, and an ad hoc
`./scripts/vet.sh` mid-implementation has none either. Existence is guaranteed by
the flow, not by this check: `/finalize` step 5 invokes `/squash-message`
unconditionally, and that skill creates-or-restores the file. The check reports
which source it resolved to, so an absence is visible in the vet output rather
than silent.

## Behavior

Parse the two fenced blocks (` ``` ` at column 0) out of whichever source the
ladder picked:

- **Title** = block 1. Fail if its line exceeds the char cap, or if the block
  holds more than one non-blank line — a squash title is one line, and a wrapped
  one pastes as a broken title.
- **Body** = block 2, trailing blank lines trimmed. Fail if the line count exceeds
  the line cap, or if any line exceeds the width cap (unwrappable single tokens
  exempt).
- **Fewer than two fenced blocks** → fail. A proposal whose body can't be located
  is not pasteable; passing quietly would be the silent-swallow this repo's
  principles rule out.

Every cap is measured in one run and all violations are reported together, with
the source the ladder resolved to, each measured value against its cap, and the
over-width body lines quoted by number. Failures point at `/squash-message`
Step 3 as the fix.

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

1. Write `scripts/check-squash-message.sh` — the ladder, the parse, the three
   caps. `chmod +x`.
2. Verify it by hand against each rung: the worktree file, a `tmp/` fallback, a
   staged deletion, a committed deletion, and no proposal at all. Fabricate the
   fixtures under `tmp/`.
3. Wire `scripts/vet.sh` — the call plus a header comment saying this is the one
   check in the file that is not stack-specific and must survive the rewrite.
4. Wire `/squash-message`: the mandatory Step 3 run, the caps stated in the format
   rules and in the Step 3 target where the prose target already lives, and the
   release-body sentence in Step 3 reconciled — the cap binds that lane too, so it
   no longer reads as exempt.
5. Propagate to adopters: ADOPTING.md § "Implement `scripts/vet.sh`" keeps the
   line; `docs/catalog.md` gets a G2 row for the script, `scripts/vet.sh`'s row
   gains it under **Pulls in**, and the closure note for vet.sh says the call
   survives the rewrite.
6. `bash scripts/check-skill-catalog.sh`, then `/dry` and `/tighten-docs`, then
   `/pr`.

## DRY notes

- **The numbers live in two places, deliberately.** The script holds them (it is
  what fails), `/squash-message` states them (it is what an agent authors
  against). Neither can delegate to the other — a shell constant can't teach and a
  skill can't measure. CLAUDE.md § Vetting and ADOPTING.md **point** at them and
  state no number, per "when a convention changes, every place that states it
  changes with it".
- **The history-recovery recipe is duplicated once, on purpose.**
  `/squash-message` Step 2 restores a swept file *to edit and re-commit*; the
  script reads a swept file *to measure*, in `sh`, with no branch to write back
  to. Extracting a shared helper would mean a script the skill shells out to for
  one `git show`, and would put the restore path — which the agent has to reason
  about while deciding whether the file it holds is the live one — behind a
  layer. They stay separate, each citing the same mechanic.
- **No env overrides for the caps.** Considered and rejected: the only caller that
  would want one is a hydrated release lane, that lane is a stub here, and shipping
  the hatch in the boilerplate teaches adopters to reach for it instead of
  tightening. An adopter who needs different numbers edits the constants — a
  visible, reviewable change in their own tree.
- **Not folded into `scripts/run-parallel.sh`.** That is a runner for checks, not
  a check; the new script is one of the things it would be handed.
- **Not inlined in `scripts/vet.sh`** — see "Where the check has to live": inlining
  it in a `rewrite`-disposition file is what would make it not propagate.
- Nothing else in the tree parses the proposal's fenced blocks, so the parse is
  new code with no existing home to route through.
