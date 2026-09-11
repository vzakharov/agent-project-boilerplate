# PR #63: feat: let /finalize merge its own PR when the run was uneventful

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/63
- **Author:** @vzakharov (human)
- **Base ← Head:** main ← claude/finalize-and-merge-fdb5r3
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-11T08:21:47Z
- **Updated:** 2026-09-11T08:45:46Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **`/finalize and merge` delegates the merge click, conditionally.** A new step 8 squash-merges the PR itself — but only when the run's whole effect on the branch was the working-artifact sweep and whatever a tool's own fixer rewrote, and every check it ran passed the first time it ran. Standing down is an ordinary outcome of the flag, not a failure of it.
- **The gate is a per-step list plus a residual clause.** What breaks it: a detached `HEAD` or a PR created in the same turn; a vet failure the agent authored the fix for; a base-merge conflict, an applied dedup, or incoming commits that interact; a red CI run (including one that "cleared itself"); a substantively rewritten squash proposal; a `/check-merge` that is not `contained`; the two-shot rule engaging; unanswered review feedback; a misapplied `no vet`. No enumeration over a procedure that grows steps stays exhaustive, so the predicate governs: if the run made you decide anything, stand down.
- **The merge reuses the record step 5 settled** — title and body read back from the PR comment rather than recomposed — and treats a GitHub refusal (branch protection, a pending required check, an un-mergeable head) as a stand-down rather than something to route around. No `--admin`, `--auto` or `--delete-branch`.
- **`/handle` does not forward the flag.** A lane produces work in the same turn that carries the flag, so `/handle <branch> and merge` is written before the diff it would land exists. `/handle` reads it as `and finalize` and reports that the merge was held, naming the one command that lands it once the operator has looked. `/finalize` states the test behind that rule, since any future caller faces it: the flag is only ever the operator's to type, on work that already exists.

## QA Checklist

- [ ] `verdicts` — read step 8's stand-down list against the last few PRs merged on this repo (`git log --oneline main`) and confirm each would have been classified the way you'd want: which would have auto-merged, which would have stopped.
- [ ] `holdback` — read `/handle` § "Argument shape" and confirm an operator typing `handle <branch> and merge` gets land-prep plus a report naming `/finalize <branch> and merge`, not a merge.
- [ ] `catalog` — `scripts/check-skill-catalog.sh` exits 0 (every `@`-reference added here resolves; the new `/finalize` → `/handle` pointer is the one at risk).
- [ ] `live` — run `/finalize and merge` on a real branch and confirm the verdict matches what the run actually did, and that a stand-down reports the condition, its step, and what would clear it.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `verdicts` | manual-only | — | The gate is a judgment procedure; whether its verdicts match the operator's intent is what's under review |
| `holdback` | manual-only | — | Same — the question is whether the rule reads unambiguously to an agent following it |
| `catalog` | unit | ✅ | `scripts/check-skill-catalog.sh`, already inside the vet run |
| `live` | manual-only | — | Needs a real PR and a real run to exercise |

https://claude.ai/code/session_01Ww5MkKvXmTbY5LvZDyF4sX

---

## Comments

### Comment by @vzakharov (agent) on 2026-09-11T08:22:18Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/63#issuecomment-5631577084](https://github.com/vzakharov/agent-project-boilerplate/pull/63#issuecomment-5631577084)

Proposed squash title/body:

```
feat: gate an agent-driven PR merge on an uneventful finalize (pr #63)
```

```
Landing a reviewed branch cost a round-trip the run had often already
earned its way past: /finalize would vet, merge the base, sweep, attest
— and then stop, for an operator to copy the squash message and click
merge, including on runs that had turned up nothing to decide.

`/finalize and merge` delegates that click, conditionally. A new step 8
merges only when the run's whole effect on the branch was the
working-artifact sweep and whatever a tool's own fixer rewrote, and
every check it ran passed the first time it ran. A per-step list names
what breaks that — a base-merge conflict or an applied dedup, a failure
the agent authored the fix for, a rewritten squash proposal, a
/check-merge that is not `contained`, unanswered review feedback — and
a residual clause carries the rest, since no enumeration over a
procedure that grows steps stays exhaustive. Standing down is an
ordinary outcome of the flag rather than a failure of it, reported with
the condition that fired and what would clear it. The merge itself
reuses the record step 5 settled instead of recomposing it, and reads a
GitHub refusal as a stand-down rather than something to route around.

/handle does not forward the flag. A lane produces work in the same
turn that carries it, so `/handle <branch> and merge` was written
before the diff it would land existed; land-prep runs and the report
names the one command that lands it once the operator has looked. That
is the question any future caller faces, so /finalize states it: the
flag is only ever the operator's to type, on work that already exists.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Review threads

### `.claude/skills/handle/SKILL.md`:13 — unresolved

```diff
@@ -10,6 +10,7 @@ Three parts, order-free:
 
 - **Target** (**required**, first token by convention): a branch name, `#NNN`, or any PR URL — the grammar `@.claude/skills/from-branch/SKILL.md` § "Argument shape" defines, used as-is. With no target, **stop and ask which branch**: a bare `/handle` has nothing to attach to.
 - **`and finalize`** (flag; bare `finalize` counts too): recognized **anywhere** in the argument, since the operator writes it before the target as often as after (`/handle and finalize <branch>`).
+- **`and merge`** (`@.claude/skills/finalize/SKILL.md`'s flag): read as `and finalize`, and **not forwarded**. A lane produces work in this turn, so the operator wrote `and merge` before the thing it would merge existed — the one case where their instruction cannot be about the diff it lands. Land-prep as asked, then say plainly in the report that the merge was held and that `/finalize <branch> and merge` is one command away once they have looked: an operator who skips the diff should be skipping it knowingly.
```

**@vzakharov (human)** — 2026-09-11T08:45:12Z

polar bear? or belts and braces? (also, if kept, it's four parts not three, in the preamble to the list)

---

## Timeline (status, references, and other events)

- **2026-09-11T08:45:46Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/63#pullrequestreview-5176636511.
