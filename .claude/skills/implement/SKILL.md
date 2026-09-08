---
description: Compatibility redirect — `/implement` is now `/go`. Invoke as `/implement` (or `/implement <branch>`); it forwards to the `go` skill unchanged. Kept because handoff blocks in older plan files and PR comments still say `/implement`.
---

`/implement` was renamed to `/go`. This path is a permanent redirect so a handoff
block written before the rename still resolves.

**Load and follow `@.claude/skills/go/SKILL.md`**, passing whatever arguments
`/implement` was invoked with. Do not act on the summary above — this file
carries no procedure of its own, and `/handle`'s Do-NOT names acting on a
one-line summary of a skill as the failure mode.

Adopting repos: `docs/catalog.md` states when this row is worth taking.
