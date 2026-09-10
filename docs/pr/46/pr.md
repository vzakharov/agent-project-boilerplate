# PR #46: feat: add /spinoff, centred on the caller's foundation

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/46
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/43-spinoff-skill-h0k4tc
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-09T21:58:22Z
- **Updated:** 2026-09-10T00:08:42Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

**`/spinoff <owner/name>` — a hydrated G0 skill that stands in a working project and fires a new repo out of it.** Both halves of the branch are now implemented: the skill, and the revision that re-centred its steps on the caller's *foundation* rather than on the agent loop.

- **The direction this infrastructure never served.** Everything else is written from the adopter's side, pulling: `ADOPTING.md` is read over the network by the repo taking it on, `docs/catalog.md` is the inventory it selects from, `/sync-agent-infra` keeps that selection current. Nothing served the source's side — standing in a real project and seeding a sibling of *it*, meaning its stack and its adaptations rather than the boilerplate's.
- **What travels is named: the foundation.** The skill's intro always said the right thing, and every step below it reached for "the agent infrastructure" — the only name on offer — dropping the stack each time it did. The foundation is the triage's output; where each part of it *lands* is Step 4's separate question.
- **The triage is a criterion, not an enumeration**: *does this path encode how code here is organized, or what this particular product is?* A filename list goes stale against every stack the skill has not seen, and the boilerplate has no stack of its own to privilege. A second fork decides the **form** — under a matched stack organization travels as files, under a mismatched one as **stated intent** in the target's plan, since a spinoff can legitimately be *"this repo, but in Python"*. A layer boundary is the architectural decision; an import-boundary lint rule is one stack's way of writing it down.
- **No directory travels wholesale, `.claude/` and `scripts/` included.** Reading the criterion against a real adopter tree broke three directory-level claims: a session-start hook is half loop and half stack (a proxy shim beside a dependency install), a formatter config is stack-bound, and `scripts/` mixes asset renderers with the loop's own scripts. The general rule replaces all three, and a file that is half loop and half stack splits rather than picking a side.
- **The watermark always points at the root**, with `lastSyncedSha` taken from the caller's own. Chains compose — a sibling of a sibling of a sibling would make a sync walk the whole ancestry, every link multiplying the triage. The known cost is accepted rather than argued away: *once you've raised your kids, it's their own life to grow.* Ancestry is still **recorded**, in a new optional `lineage` array held **root first**, whose contract lands in the skill that owns the watermark field-by-field. It is provenance, **not** a second sync source.
- **The seed splits by reviewedness, not by category.** `main` takes the **copies** — reviewed where they came from, and exactly the `/handle` closure `check-skill-catalog.sh` assertion 1 enforces. The **rewrites** go through PR #1 as ordinary reviewed work, so `main` reduces to what the boilerplate itself would ship and a spinoff is structurally identical to an adoption. Under a mismatched stack that is also the only possible shape.
- **The re-stub rule inverted under test.** `main` carries no `docs/catalog.md`, and without one assertion 4 reads a stub as a stowaway to hydrate or delete rather than as shipped inventory — so re-stubbing a caller-hydrated skill onto `main` is the *one* disposition that fails `main`'s own gate, while both omitting it and carrying it hydrated pass. Verified by assembling the copies-only set from a real adopter and running the gate over it three ways. That also generalizes the watermark exception, which is not the only one: assertion 1 ties the same knot wherever a travelling skill `@`-references a caller-hydrated stub, as `/bootstrap-workflow-dispatch` does `/test-on-gh`.
- **The vet gate is a refusal, not a weakening.** `main` has no stack, so the honest `vet.sh` refuses to certify and PR #1 wires in the real checks. The check is that `main`'s `vet.sh` exits **non-zero**, and the named trap is the pressure to weaken the caller's script until the seed passes.
- **Adopter-only, by refusal.** The skill stops when it finds `docs/catalog.md` in the caller — the tell that a tree is this repo or an unpruned copy of it. That leaves the boilerplate → new-project direction where it already worked (*"Use this template"* + `ADOPTING.md § Template fork`), so those stay untouched and the fork footguns never arise. The **caller stays read-only** — no commit, branch, PR or issue lands there — and the `/pr` delegation asserts the target clone's `origin` before loading, since `/pr` aims at whatever `cwd` resolves to and Bash `cwd` resets between calls in this harness.

**Scope cut against #43, [recorded on the issue](https://github.com/vzakharov/agent-project-boilerplate/issues/43#issuecomment-5609608316).** The issue also names this repo as a caller and asks for `ADOPTING.md § Template fork` to be deleted. That caller is dropped, so the deletion is off and the issue's `## What /spinoff replaces` section is superseded. Its DRY argument survives inverted — template fork and `/spinoff` are one procedure each for two operations, not two for one.

## QA Checklist

- [ ] `skill-reads` — read `.claude/skills/spinoff/SKILL.md` end to end and confirm all five steps are followable by an agent that has never seen #43
- [ ] `criterion` — confirm *"what does this path encode"* decides more paths than an enumeration would, and that the six named cases are the ones it genuinely can't settle
- [ ] `worked-tree` — run the criterion against a concrete adopter (`vzakharov/vovazakharov.com`, the case #43 cites) and confirm it decides every path, including the domain declaration, the publish workflow, and the layer boundaries
- [ ] `cross-stack` — read the same tree again with the target's stack changed (*"this repo, but in Python"*) and confirm every scaffolding path has a stated destination **as intent**, with nothing silently copied
- [ ] `per-path` — confirm "no directory travels wholesale" is the right generalization, and that splitting a half-loop/half-stack file beats assigning it to one bucket
- [ ] `stack-agnostic` — grep the skill for ecosystem-specific nouns; the rules should name roles, with filenames and tool names only inside parenthetical examples
- [ ] `copy-rewrite` — confirm copy-vs-rewrite really is the right seam for `main`-vs-PR #1, and that it does not misfile anything in a tree you know
- [ ] `handle-floor` — sort a real adopter's tree into copies and rewrites and confirm the copies **alone** satisfy `check-skill-catalog.sh` assertion 1, so `main` is bootable for `/handle` without any rewrite
- [ ] `restub` — confirm that omitting a caller-hydrated stub from `main` (rather than re-stubbing it) is right, that per-target editability is the criterion, and that the assertion-1 exception for an `@`-referenced stub is stated clearly enough to act on
- [ ] `vet-refusal` — confirm "`main`'s `vet.sh` exits non-zero" is the correct gate, and that reduce-to-a-refusal vs. weaken-until-it-passes is a distinction the step states clearly enough to hold
- [ ] `lineage-trace` — trace three generations by hand (root → adopter → spinoff of that spinoff) and confirm each array reads root-first in birth order, and that a caller with no `lineage` yields a one-entry array rather than a fabricated root
- [ ] `lineage-repeat` — confirm `lineage[0].repo` restating `repo` reads as two facts, not a duplication, at the place the contract introduces the array — including that the two SHAs coincide until the first sync and diverge after
- [ ] `lineage-not-a-source` — confirm `lineage` reads unmistakably as provenance rather than as a second sync source, so a later reader doesn't teach `/sync-agent-infra` to walk it
- [ ] `watermark-pair` — confirm the watermark landing on `main` beside its skill is justified by `check-skill-catalog.sh` assertion 4, not smuggled in as a convenience
- [ ] `refusal-gate` — confirm `docs/catalog.md`-present is the right test: it catches this repo and unpruned copies, and clears a pruned adopter that legitimately wants to spin off
- [ ] `cwd-guard` — confirm the `git -C <clone> remote get-url origin` assertion sits *before* `/pr` is loaded, and that the read-only invariant points at it
- [ ] `companions` — confirm `CLAUDE.md`, `README.md`, `ADOPTING.md` and the frontmatter really are direction-neutral, so leaving them untouched is right
- [ ] `catalog-closure` — `bash scripts/check-skill-catalog.sh` exits 0 with all four assertions passing
- [ ] `scope-cut` — confirm dropping the from-this-repo caller is a decision you want recorded against #43 rather than a narrowing to revisit

| Item | Automatable | Covered? | Notes |
| --- | --- | --- | --- |
| `skill-reads` | manual-only | — | Judging whether a procedure is followable is the review itself |
| `criterion` | manual-only | — | Whether a criterion generalizes is the review itself |
| `worked-tree` | manual-only | — | Needs a real adopter tree; no fixture stands in for one |
| `cross-stack` | manual-only | — | The mode exists precisely because no file list can cover it |
| `per-path` | manual-only | — | A judgment about where a seam belongs, against a tree you know |
| `stack-agnostic` | manual-only | — | A grep finds candidates; deciding whether a noun is a role or an ecosystem is reading |
| `copy-rewrite` | manual-only | — | Whether a seam misfiles anything needs a real tree in mind |
| `handle-floor` | unit | ✅ | `check-skill-catalog.sh` over the copies-only set — run in-session against `vovazakharov.com`, exits 0 |
| `restub` | unit | ✅ | Same harness: correctly re-stubbed fails assertion 4, omitted passes — both verified in-session |
| `vet-refusal` | unit | ⚠️ | The exit code is checkable; whether the prose prevents the weakening is not |
| `lineage-trace` | unit | ⚠️ | `jq` proves it parses; birth-order semantics are a reading call |
| `lineage-repeat` | manual-only | — | A DRY judgment about whether two SHAs are two facts |
| `lineage-not-a-source` | manual-only | — | Guarding against a future misreading — prose is the only lever |
| `watermark-pair` | unit | ✅ | `check-skill-catalog.sh` assertion 4 is the thing being cited |
| `refusal-gate` | manual-only | — | Needs judgment about which trees should and shouldn't qualify |
| `cwd-guard` | manual-only | — | Reading prose for an ordering; the runtime version is the guard itself |
| `companions` | manual-only | — | Assertions 2–3 prove rows exist, not that surrounding prose is right |
| `catalog-closure` | unit | ✅ | `scripts/check-skill-catalog.sh`, which `scripts/vet.sh` runs at `/finalize` |
| `scope-cut` | manual-only | — | A scope decision against the issue's stated intent |

Closes #43

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Bh7LU2QCZ4CoaPayBq3XN4

---
_Generated by [Claude Code](https://claude.ai/code)_


---

## Comments

### Comment by @vzakharov on 2026-09-09T21:58:49Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/46#issuecomment-5609313168](https://github.com/vzakharov/agent-project-boilerplate/pull/46#issuecomment-5609313168)

Proposed squash title/body:

```
feat: #43 add /spinoff for seeding a sibling repo (pr #46)
```

```
The agent infrastructure was written entirely from the adopter's
side, pulling: ADOPTING.md is read over the network by the repo
taking it on, docs/catalog.md is the inventory it selects from,
and /sync-agent-infra keeps that selection current. Nothing served
the source's side — standing in a working project and firing a new
one out of it, which is the recurring next move once a real
project runs on this infrastructure. "Another repo like this one"
means that repo's foundation, not the boilerplate's.

/spinoff <owner/name> is that operation, hydrated, in G0. What
travels is the caller's foundation — how code there is organized —
and a criterion decides it rather than a file list, which would go
stale against every stack the skill has not seen: does this path
encode how code here is organized, or what this particular product
is. A second fork decides the form it travels in, since a spinoff
can legitimately be "this repo, but in Python": under a matched
stack organization travels as files, under a mismatched one as
stated intent in the target's plan, because a layer boundary is
the architectural decision and an import-boundary lint rule is
one stack's way of writing it down. No directory travels
wholesale — .claude/ and scripts/ both mix the loop with the
stack, and a session-start hook is half of each.

The seed splits by reviewedness. main takes the copies, which
arrived reviewed and are exactly the /handle closure that
check-skill-catalog.sh enforces; the rewrites go through PR #1 as
ordinary reviewed work, rather than landing the least-reviewed
content through the one path nothing reviews. main therefore
reduces to what the boilerplate itself would ship, which makes a
spinoff structurally identical to an adoption, and its vet.sh
refuses to certify instead of being weakened until the seed
passes. A caller-hydrated stub is omitted rather than re-stubbed:
absent a catalog, a stub is the one disposition that fails main's
own gate.

The watermark always points at the root, because chains compose —
a sibling of a sibling would make a sync walk the whole ancestry,
every link multiplying the triage. Ancestry is recorded instead,
in a new root-first lineage array that is provenance and never a
second sync source. The skill runs from adopters only, refusing
when docs/catalog.md is present, which keeps the
boilerplate-to-project direction where the template fork already
served it; and it keeps the caller read-only, asserting the target
clone's origin before /pr is delegated to, since /pr aims at
whatever cwd resolves to.

Closes #43

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `docs/remove-before-merging/squash-message.md`:1 — unresolved

**@vzakharov** — 2026-09-10T00:07:15Z

while we're at it, let's bring the squash body caps to 40 (riding along in this pr although unrelated)

---

### `CLAUDE.md`:161 — unresolved

```diff
@@ -158,6 +158,7 @@ This project ships a set of Claude Code skills under `.claude/skills/`. Invoke t
 
 - **`/issue`** — export and read a GitHub issue, split it when the scope demands, then hand the work to `/plan`.
 - **`/from-branch`** — attach the session to an existing branch or PR, abandoning the auto-created session branch.
+- **`/spinoff`** — seed a new sibling repo out of the project you are standing in, and hand over a session rooted in it. **Adopters only**: it refuses from this repo, where the route to a new project is the README's template button.
```

**@vzakharov** — 2026-09-10T00:08:29Z

where is the part that refuses? might've missed it

---

## Timeline (status, references, and other events)

- **2026-09-09T22:31:50Z** @vzakharov renamed from «feat: plan a /spinoff skill for seeding a sibling repo from a caller» to «feat: add /spinoff, a hydrated G0 skill for seeding a sibling repo».
- **2026-09-09T22:42:07Z** @vzakharov renamed from «feat: add /spinoff, a hydrated G0 skill for seeding a sibling repo» to «feat: add /spinoff, plus a plan re-centering it on the foundation».
- **2026-09-09T23:23:20Z** @vzakharov renamed from «feat: add /spinoff, plus a plan re-centering it on the foundation» to «feat: add /spinoff, centred on the caller's foundation».
- **2026-09-10T00:08:41Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/46#pullrequestreview-5161181259.
