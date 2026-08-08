---
description: >-
  Review the prose you added in recent work — code comments, docstrings, and
  Markdown — against two equal defects: it narrates the change instead of stating
  the code's lasting contract ("no longer parsed", "now also sets X", "migrated
  from Y"), and it spends more words than it informs — restating what the name,
  signature, and types already say, or stretching a real point over four lines.
  Rewrites and cuts in place. Invoke as: /tighten-docs [optional focus guidance]
---

You are reviewing prose _you_ recently added — code comments, docstrings, and
Markdown (skill bodies, `docs/`, READMEs) — for two defects that carry
**equal weight**:

- **Narration** — text that describes the change relative to the previous
  intra-PR step rather than the code's durable behaviour. CLAUDE.md: "Comments
  describe the code's lasting contract, not the change that produced it."
- **Bloat** — text that spends more words than it informs: it restates what the
  function name, signature, and types already convey, or stretches a real point
  past the length it needs. CLAUDE.md's docstring rule: document only the
  non-obvious contract (side effects, runtime constraints, cross-boundary
  coupling, don't-change-this traps).

The output is **edits, not a report**. Fix the clear cases in place; only ask
about genuinely ambiguous ones.

## When to use

- After an autonomous run (several commits since the operator last engaged),
  before handing back — both defects accumulate step-to-step.
- Any time you notice a comment reads like a diff note, or a docstring restates
  its own signature.
- Skip if recent work added no prose (pure logic/test edits with no new comments).

## Step 1: Scope to what you added since the operator last engaged

In order:

1. **Uncommitted changes**: `git diff HEAD` + untracked files (`git status --short`).
2. **Commits since upstream / since the operator's last turn**: `git log --oneline @{u}..HEAD`, or the SHA range the session summary names. `git diff <range>` is the scope.
3. **Nothing matches** → tell the user there's nothing to review and stop.

Only the **added/changed** prose lines are in scope — don't rewrite pre-existing
comments you didn't touch.

## Step 2: Read each added prose line and ask both questions

A line can fail either check, or both. Work through the diff **once**, applying
both lenses to each comment — not one traversal per lens.

### Lens A — is it narration?

A line is narration when it only makes sense to a reader who knows the previous
step. Tells:

- Change verbs anchored to the past: **"no longer"**, **"now also"**, **"used to"**,
  **"previously"**, **"migrated from"**, **"this used to…"**, **"as of this change"**, **"renamed from"**.
- **"for now" / "temporarily" / "once X lands"** — situational hedges that go stale.
- References to a prior step, ticket, or version as if the reader is watching the diff.

The test: **would this sentence still be true and useful to someone reading the
final code a year from now, with no memory of the edit?** If it only informs
"what changed", it's narration.

### Lens B — is it bloat?

A line is bloat when it costs a reader more than it tells them — either they
already had the fact from the name, signature, and types, or the fact is real
but buried in twice the prose it needs. Tells:

- **Restates the signature** — names the params or return type, or paraphrases the
  function name (`/** Fetches the user by id. */` over `fetchUserById(id: string)`).
- **Narrates the next lines of code** — "Loop over the items and set the flag",
  "If the list is empty we skip".
- **Restates a type's or enum's members** in prose sitting next to the declaration.
- **Ceremony** — "This function is responsible for…", "Helper that…", "Note that…"
  wrapped around one actual fact.
- **A docstring block on something that crosses no boundary** — the contract is
  already obvious from name + types, so the block is decoration.
- **Length**: **> 4 lines** is almost certainly too much; find the one or two facts
  that aren't self-evident and keep only those. Even exactly 4 is too much unless
  it's a proper docstring block on a function/class/etc. **A good inline clarification
  fits ~2 lines.** The point is often real and the prose still too long:
  - "We await this before returning, because otherwise the transaction may still be
    open by the time the caller commits, which can deadlock under concurrent writes."
    → "Await before returning — an open transaction here deadlocks concurrent writes."
  - "It's worth noting that this cache can only be used on the server, since the key
    includes the workspace id and the browser bundle has no access to it."
    → "Server-only: the cache key needs the workspace id."
- **Markdown**: an added paragraph that re-explains what the adjacent bullet or code
  block already shows; a "Note:" restating the rule directly above it.

## Step 3: Fix

**Narration:**

- **Rephrase to a present-tense property** when the underlying fact is durable:
  "The emoji is no longer parsed" → "Nothing parses the emoji." "Now also sets
  `x`" → "Sets `x`."
- **Delete** when the note carried no lasting information beyond the change
  itself ("Migrated from the old helper", "Renamed for clarity").
- **Keep** genuine forward-references to still-pending work (e.g. "§F2 is
  deferred") and durable rationale phrased in the present ("kept in sync by
  hand because…"). These are contracts, not changelog.

**Bloat:**

- **Cut to the non-obvious facts** — the side effect, the runtime constraint, the
  coupling, the trap. Drop every clause the name and types already carry.
- **Downgrade a docstring block to a one-line inline comment inside the function**
  when its only real purpose is a don't-break-this warning — CLAUDE.md says the
  dev editing the code will see it there, and that's enough.
- **Delete entirely.** This is a normal outcome and often the right one; a comment
  the code already makes true earns nothing by being shortened.
- If you can't say it in ~2 lines, question whether the **code** should be clearer
  rather than the comment longer.

When both lenses fire on one comment, resolve bloat first — deciding it shouldn't
exist saves you from carefully rewording it.

## Step 4: Do NOT touch

- **Commit messages and PR bodies** — narrating the change is their job.
- **`docs/plans/*.md`** — transient by nature, swept at finalize.
- **`docs/remove-before-merging/squash-message.md`** — a commit body, and transient
  by nature.
- **CHANGELOG / release-notes files** — a dated record of changes is the point.
- **Deliberately thorough reference prose** — a decision doc or rules file that
  spends paragraphs on rationale is doing its job. Length carrying rationale the
  reader can't get elsewhere is not bloat; length carrying nothing is.

## Step 5: Report + commit

Report the two classes **separately, each with a count**, one bullet per fix
(`file:line` + before → after in a few words):

```
Durability (2)
- src/foo.ts:14 — "no longer parsed" → "Nothing parses the emoji."
- …

Tightness (3)
- src/bar.ts:8 — 7-line docstring → 2 lines (dropped param restatement)
- src/baz.ts:31 — deleted (signature says it)
- …
```

Both groups always appear; **an empty one gets a sentence saying why** rather
than silence ("nothing added was over-documented" is a real outcome).

Then commit the edits (on a feature branch, just commit — the vet run happens at
milestones via `/finalize`, not per commit).
