# PR #31: feat: enforce squash-message size caps in the vet run

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/31
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/squash-msg-caps-a0ibxe
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-08T12:30:19Z
- **Updated:** 2026-09-08T23:41:39Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- `scripts/check-squash-message.sh` turns the mechanically checkable part of the squash-message target into a check that fails: a one-line title of at most 80 chars, and a body of at most 50 lines wrapped at 72, exempting a line whose trimmed text is a single unwrappable token. All violations report together, naming the source, each value against its cap, and the over-width lines by number.
- The proposal is usually gone by vet time — `/finalize` sweeps `docs/remove-before-merging/` before a re-vet can run — so the source is a ladder rather than a path: an explicit argument, the worktree file, the `tmp/` fallback, `HEAD` with the sweep staged, then the last commit on this branch that deleted it. Finding nothing anywhere is normal and passes.
- Two enforcement points, catching different things. `/squash-message` step 3 measures the file it just tightened, which fails at authorship and is the only run `/finalize no vet` gets; `scripts/vet.sh` measures at land prep, which is what catches a proposal edited by hand or outgrown by a later base merge.
- `scripts/vet.sh` carries the `rewrite` disposition, so the call is the one line in it that must survive an adopter replacing the rest. Its own comment is the home for that; CLAUDE.md, ADOPTING.md and the catalog's closure note point at it.
- Deviation from the plan, worth a look: the plan bounded the history rung by resolving `refs/remotes/origin/HEAD` and falling back to the **full history** when it doesn't resolve. That ref is absent from the clones agent sessions get, and the fallback then picked up an unrelated branch's swept proposal from `main`'s history and failed this branch for someone else's words — reproduced on this branch during step 2. The base now tries the usual default-branch names after `origin/HEAD`, and an unresolvable base reports no proposal rather than searching everything.

## QA Checklist

- [ ] `no-proposal` — on a branch with no proposal anywhere, run `./scripts/vet.sh`; the check prints `no squash proposal on this branch` and exits 0, leaving vet to fail only on its own stub.
- [ ] `worktree` — write a within-caps proposal to `docs/remove-before-merging/squash-message.md`, run `./scripts/vet.sh`; the check reports `ok` and names the worktree as the source.
- [ ] `tmp-fallback` — remove that file, put the same proposal at `tmp/squash-message.md`, re-run; the check resolves to the `tmp/` path.
- [ ] `swept` — commit the proposal, then `git rm -r docs/remove-before-merging` and commit the sweep; re-run and confirm the check reads the file back out of history and still measures it.
- [ ] `title-cap` — push the title past 80 chars, or wrap it onto two lines; both fail, and the failure quotes the measured length.
- [ ] `body-caps` — push the body past 50 lines, or leave one prose line over 72 chars; both fail, and the width failure quotes the offending lines by body line number.
- [ ] `url-exempt` — put a bare 90-char URL on its own body line; it passes, and the reported widest line stays at or under 72.
- [ ] `foreign-sweep` — from a branch that never carried a proposal but whose base history holds one, run the check; it reports no proposal rather than measuring the other branch's words.
- [ ] `skill-gate` — run `/squash-message` on this PR and confirm step 3 measures the working file before anything is emitted.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `no-proposal` | integration | ❌ | Repo has no test harness; verified by hand this session via a throwaway `tmp/` script |
| `worktree` | integration | ❌ | Same — fixture file, assert exit 0 and the resolved source |
| `tmp-fallback` | integration | ❌ | Same |
| `swept` | integration | ❌ | Needs a scratch repo with a real commit history; the highest-value row to automate |
| `title-cap` | unit | ❌ | Pure parse/measure over a fixture; cheapest row to cover |
| `body-caps` | unit | ❌ | Same |
| `url-exempt` | unit | ❌ | Same |
| `foreign-sweep` | integration | ❌ | Scratch repo with a bare `origin`; guards the merge-base bound |
| `skill-gate` | manual-only | — | Whether a skill's prose is followed isn't assertable |

**Coverage gap:** every automatable row is uncovered. This repo ships no test harness and `scripts/vet.sh` is a stub, so the plan called for hand verification with fixtures under `tmp/`, which is what ran — 10 content fixtures and all 6 ladder rungs, all passing. A shipped harness for this script is a reasonable follow-up.

https://claude.ai/code/session_01LGj5icBbkMQjTpxLoHPP3Z

---

## Comments

### Comment by @vzakharov on 2026-09-08T12:31:17Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/31#issuecomment-5585166487](https://github.com/vzakharov/agent-project-boilerplate/pull/31#issuecomment-5585166487)

Proposed squash title/body:

```
feat: enforce squash-message size caps in the vet run (pr #31)
```

```
`/squash-message` states the target for the permanent `git log` record
as prose — a one-line title, a body hard-wrapped at ~72 — and its
tighten pass is an agent reading its own output. This settles the part
of that target a machine can settle.

`scripts/check-squash-message.sh` measures the proposal's two fenced
blocks: the title is one line of at most 80 chars, the body at most 50
lines and 72 wide, exempting a line whose trimmed text is a single
unwrappable token. One run reports every violation, naming the source,
each value against its cap, and the over-width lines by number. The
caps bind every lane, the release lane included; a project needing more
room edits its own copy of the script.

The proposal is usually gone by vet time, since `/finalize` sweeps
`docs/remove-before-merging/` before a re-vet can run, so the source is
a ladder: an explicit argument, the worktree file, the `tmp/` fallback,
`HEAD` with the sweep staged, then the last commit on this branch that
deleted it — bounded to the merge base, so another branch's swept
proposal is never measured as this one's. Finding nothing is normal
wherever no PR-opening lane has run, and passes.

Two gates catch different things. `/squash-message` step 3 fails at
authorship and is the only run `/finalize no vet` gets; `scripts/vet.sh`
catches a proposal edited by hand or outgrown by a later base merge.
Since `vet.sh` is a `rewrite`, an adopter decides that one line on its
own — the comment above it is the home for what dropping it costs, and
ADOPTING.md and the catalog point at it.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `scripts/check-squash-message.sh`:1 — unresolved

**@vzakharov** — 2026-09-08T23:16:12Z

idea (not to edit yet, just to weigh in): what if this script actually does the wrapping itself, so agents can just write continuous-line prose (barring paragraph breaks), and it wraps them, AND indicates which part overflows, if any (so agents know what to cut)? how hard would it be given that it's just a .sh (which begs the question of whether it should stay being a .sh)

**@vzakharov** — 2026-09-08T23:25:32Z

Weighed, not touched.

Worth doing, but split in two, because the two gates can't both wrap. At vet time the proposal is usually being read back out of a commit — the sweep already ran — so there's nothing to write to; that gate stays a read-only measurement. Wrapping only works at authorship, where `/squash-message` step 3 has the file in hand. So it'd be a `--wrap` mode the skill calls, with vet's invocation unchanged.

One thing argues for it beyond convenience: if agents write continuous prose, the raw line count stops meaning anything, so the check has to wrap internally before it can count against the 50-line cap. It computes the wrap either way — emitting it is nearly free.

"Which part overflows" gets sharper as a result. After wrapping, the only thing left to cut is the line budget, and the script can say "wraps to 63 lines, 13 over; paragraphs 3 and 6 are the longest, at 14 and 12" — mechanical, and actionable in a way "body is 63 lines, cap 50" isn't.

On staying `.sh`: `fold -s -w 72` is the whole wrapper, so the easy version is a few lines. The cost is markdown awareness — don't wrap inside a fence, preserve a list item's hanging indent, leave the single-token exemption alone. Tractable in sh, but that's the point where it stops being *obviously* tractable. I'd keep it sh for now: `vet.sh` is the one entrypoint every adopter must have, so a check it calls shouldn't raise the floor to python3 (`export-github-item.py` can, since only `/issue` and `/handle` reach it). And the migration stays cheap later — the wrap half would live at the authorship gate only, where the floor argument doesn't apply, so it could move on its own.

Want me to file it?

---
_Generated by [Claude Code](https://claude.ai/code)_


**@vzakharov** — 2026-09-08T23:40:38Z

-w 72 would wrap the title (which we admitted can be 80 by definition) too?

---

### `scripts/vet.sh`:15 — resolved

```diff
@@ -11,7 +11,17 @@
 # Parallel, printing only what failed (worth it once the serial run is the wait):
 #   exec scripts/run-parallel.sh lint='pnpm lint' typecheck='pnpm typecheck' test='pnpm test:unit'
 #
+# The `check-squash-message.sh` line below is the one check here that is not
+# stack-specific, so it must survive the rewrite this file is meant to get: keep
```

**@vzakharov** — 2026-09-08T23:16:25Z

"must" is too strong a word here

**@vzakharov** — 2026-09-08T23:25:14Z

Softened — `vet.sh`'s comment states the consequence instead of a duty now: "Replacing everything around it is what this file is for, so decide that line on its own — dropping it leaves nothing catching a proposal edited by hand or outgrown by a later base merge." 5b8a711

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `ADOPTING.md`:269 — resolved

```diff
@@ -263,6 +263,11 @@ loop stopping loudly — it is a
 [`rewrite`](docs/catalog.md#three-dispositions-not-two) rather than a choice, for
 [the reason the catalog gives](docs/catalog.md#closure-is-not-optional).
 
+**Keep the `scripts/check-squash-message.sh` line** when you replace the rest —
+it is the one check in the file that isn't stack-specific, and the comment above
+it in `vet.sh` says why. Bodies that genuinely need more room than its caps allow
+are a matter of editing the constants in your copy of that script.
```

**@vzakharov** — 2026-09-08T23:17:02Z

I wouldn't say it's always a matter of that. E.g., in the playgram app, it would take to figure out if it's a release commit, and only then lax the caps. So I'd say implement any additional needed mechanics on top of that.

**@vzakharov** — 2026-09-08T23:25:15Z

Fair. The ADOPTING sentence carrying that claim is gone entirely, and the two places the claim still lives — the script header and `/squash-message` step 3 — now say "edit your copy" rather than "raise the constant", naming the release case as the one that has to work out a commit *is* a release before it can widen anything. 5b8a711

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `ADOPTING.md`:266 — resolved

```diff
@@ -263,6 +263,11 @@ loop stopping loudly — it is a
 [`rewrite`](docs/catalog.md#three-dispositions-not-two) rather than a choice, for
 [the reason the catalog gives](docs/catalog.md#closure-is-not-optional).
 
+**Keep the `scripts/check-squash-message.sh` line** when you replace the rest —
```

**@vzakharov** — 2026-09-08T23:17:25Z

Again, it's their choice -- we can't and oblige them.

**@vzakharov** — 2026-09-08T23:25:16Z

Right — imperative dropped. It reads: "One line in `vet.sh` — the call to `scripts/check-squash-message.sh` — is not stack-specific, so decide it separately rather than sweeping it away with the rest; the comment above it says what dropping it costs." 5b8a711

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `CLAUDE.md`:33 — resolved

```diff
@@ -29,6 +29,8 @@ go vet ./... && go test -short ./...                # Go
 
 The checks may also be fanned out with `scripts/run-parallel.sh lint='…' typecheck='…' test='…'`, which prints output only for the ones that failed.
 
+One line in `vet.sh` is **not** yours to replace: the call to `scripts/check-squash-message.sh`, which holds the squash proposal to the size caps `@.claude/skills/squash-message/SKILL.md` states. Carry it through the rewrite; the comment above the call says why.
+
```

**@vzakharov** — 2026-09-08T23:19:10Z

third time we mention it, and it might lead adopting agents to believe it's like the most important thing ever -- it's not. I'd frankly limit myself to a comment in vet.sh alone (adopters will on their own decide how to "adopt" or "decline" check-squash-message) -- but see if you think it's still worth keeping in ADOPTING (not here)

**@vzakharov** — 2026-09-08T23:25:31Z

Gone from CLAUDE.md.

On ADOPTING — I'd keep it, cut to one sentence pointing at the `vet.sh` comment. That step is the one moment an adopter is actually deciding what to do with the file's contents, and a check other skills call vanishing silently is worth the one clause. Everything explanatory stays in the comment they're looking at while they do it.

There was a fourth mention you didn't flag, too: the catalog's closure note restated the whole consequence, so that's a pointer now as well. 5b8a711

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `scripts/check-squash-message.sh`:10 — unresolved

```diff
@@ -4,10 +4,10 @@
 # over. The skill's Step 3 is an agent reading its own output; this is the part
 # of that target a machine can settle.
 #
-# An adopter whose bodies genuinely need more room edits the constants below.
-# There is deliberately no env override: the only lane that would want one is a
-# hydrated release lane, and a hatch in the boilerplate teaches reaching for it
-# instead of tightening.
+# There is deliberately no env override: a hatch in the boilerplate teaches
+# reaching for it instead of tightening. An adopter needing more room edits this
+# copy — raising a constant below, or adding what the case needs, the way a
+# release lane must first work out that a commit is a release.
```

**@vzakharov** — 2026-09-08T23:41:13Z

any adopter besides playgram (which is not an adopter anyway) will be confused by the random mention of a release lane here.

---

## Timeline (status, references, and other events)

- **2026-09-08T23:19:27Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/31#pullrequestreview-5147966046.
- **2026-09-08T23:41:39Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/31#pullrequestreview-5148139260.
