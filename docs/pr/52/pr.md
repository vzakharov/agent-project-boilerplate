# PR #52: feat: #50 give the template-fork path a detemplating skill

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/52
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/50-detemplate-skill-20s9ih
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-10T11:02:40Z
- **Updated:** 2026-09-10T20:59:52Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **Adds `/detemplate`**, the lever the template-fork path was missing while every other stage of the loop had one (`/plan`, `/go`, `/finalize`, `/issue`, `/spinoff`). It takes the project brief as its argument and **routes through `/plan`** rather than acting directly, so the prune — a large, largely irreversible diff over a tree nobody has reviewed — is reviewed as a diff first. It **deletes itself last**, which is why nothing cites it as an `@`-reference: one would dangle afterwards in the tree of whoever just ran it.
- **The brief becomes the project's first issue.** A run deliberately writes no source, so without this the operator's description of what they are building survives only as a `CLAUDE.md` paragraph — a place to read it, not a place to work from. Step 5.5 files it through `/propose-issue` (skipped where the run drops G3), and Step 7 hands over a copyable `/issue #N <title>` for the session after this PR merges. A scarce brief makes a scarce issue: the step exists to *keep* what the operator said, not to interview them for more.
- **Recognizes a fork nobody has detemplated, and the frontmatter is what does the routing.** The section describing the mechanism is only read *after* the description has sent someone there, so the description names the **repository** rather than the situation: a tree whose `origin` is not `vzakharov/agent-project-boilerplate` while this description exists is a fork to route, and the boilerplate settles that against the working directory in its own system prompt at no round-trip. A run deletes the skill, so those really are the only two cases. Both guards match the full `owner/repo` and never the substring `boilerplate`, which would refuse a legitimate `acme-boilerplate`. `/spinoff`'s refusal splits by the same signal, and `CLAUDE.md`'s "About this project" stub carries the standing notice for a session that never reads the skill list.
- **`gh`'s absence becomes a litmus test for an unset environment setup script.** The session-start hook installs no `gh` — it shims one already on `PATH` — so where the setup script is unset or omits `apt-get install -y gh` there is nothing to shim, and every `gh`-dependent skill fails later, far from the cause. The hook now reports that into the session context (stdout, which Claude Code folds into context) naming what the operator must add and where, instead of a stderr line nobody reads. It needs no change to anyone's existing setup script, and `/override-gh` is the signal's home.
- **Converts the by-hand run's findings into procedure**: the load-bearing ordering that deletes the catalog **first** (flipping `check-skill-catalog.sh` assertion 4 to enforcing, and un-refusing `/spinoff`), `docs/img/`'s missing catalog row, the fork-side `lastSyncedSha` derivation git cannot give you, the absent `lineage` field, and per-group reverse closure as a new catalog section. Two dispositions are pre-decided rather than asked: `/implement` goes (a tree one commit old has no handoff block old enough to say it), and so does this skill.
- **The vet contract gains its missing clause and a single home.** `scripts/vet.sh` already exits `0`, so a stackless fork works today — but the rule was stated in **five** places, each telling an adopter to set `exit 1` with no exception for a repo that has no stack yet. A fork following that literally fails `/finalize` step 1 on every prose-only PR. `CLAUDE.md` § "Vetting" is now the home; the other four point at it, and it gains the **third stack-coupled site** no agent can move — the environment setup script, which a toolchain change leaves stale unless the report says what to paste in.
- **Open question 1 resolved on its recommendation (1a).** `/spinoff` Step 4 asserted a **non-zero** `vet.sh` on a seeded `main` that deliberately has no stack, which the clarified rule contradicts. It now asserts the honest pair: the script passes **and** names no stack-specific checks, with the invariant restated as what must not happen — the source repo's own `vet.sh` reaching `main`.
- `ADOPTING.md` § "Template fork" becomes a pointer at the skill, leaving the subset-adoption path whole for the agent that reads that file over the network with no skills installed. Its watermark recipe gains `lineage` and the fork-side SHA problem.
- Finding 7 — the G5/G2 grouping defect — is out of scope here; it is #49.

## QA Checklist

- [ ] `skill-reads` — read `.claude/skills/detemplate/SKILL.md` end to end and confirm the procedure is executable as written: Step 0's two-way refusal, Step 3's derivation, and Step 5's ordering with the catalog first, the issue at 5.5 and the self-deletion second-to-last
- [ ] `issue-handoff` — confirm the Step 5.5 / Step 7 pair reads right: the issue carries the brief without interviewing for more, is skipped where G3 is dropped, and the handover block is `/issue #N <title>` for a *fresh* session after merge
- [ ] `gh-litmus` — hide `gh` from `PATH` and run the hook (`PATH=<dir-without-gh> bash .claude/hooks/session-start.sh`): it prints the operator-facing notice, exits `0`, and does not block the session
- [ ] `frontmatter-routes` — confirm `/detemplate` appears in a fresh session's skill list and that its description, read cold, sends an agent in a non-boilerplate tree to § "Recognizing an undetemplated fork" — while costing an agent in *this* repo nothing but a glance at its own working directory
- [ ] `slug-exact` — `grep -rn 'boilerplate' .claude/skills/detemplate .claude/skills/spinoff CLAUDE.md` and confirm every guard matches the full `vzakharov/agent-project-boilerplate`, never the bare substring
- [ ] `spinoff-assert` — confirm the resolution of open question 1: `/spinoff` Step 4 now asserts `vet.sh` exits `0` while naming no stack-specific checks. Say if you wanted (b) or (c) instead
- [ ] `vet-agree` — `grep -rn 'exit 1\|exits `0`' CLAUDE.md ADOPTING.md .claude/skills/sync-agent-infra/catalog.md scripts/vet.sh` and confirm exactly one site states the rule (`CLAUDE.md` § "Vetting") and the rest point at it
- [ ] `vet-behavior` — `bash scripts/vet.sh` still exits `0` here; `git diff origin/main..HEAD -- scripts/vet.sh` touches only comments and `echo` strings, no control flow
- [ ] `no-dangle` — `grep -rn '@\.claude/skills/detemplate' .` returns nothing outside `docs/`, so the self-deletion cannot strand a pointer; `bash scripts/check-skill-catalog.sh` exits `0`
- [ ] `closure-counts` — spot-check the counts in the catalog's § "Reverse closure" against the tree: one `@`-reference into G6, six files of self-guarding bare-name prose, two live `@`-references to `watch-ci` in `/finalize`, two dead names in `/override-gh`
- [ ] `readme-route` — read `README.md` § "Create a new project from this template" and confirm the handover to `/detemplate <what you're building>` reads right for someone who has just clicked the template button

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `skill-reads` | manual-only | — | Judgement on whether a procedure is followable; no assertion expresses it |
| `issue-handoff` | manual-only | — | Same: the shape of a handover is a reading, not an assertion |
| `gh-litmus` | integration | ❌ | Runnable exactly as written, and run this session; nothing in the repo runs it on a schedule |
| `frontmatter-routes` | manual-only | — | The harness loads skills; nothing in-repo can assert a description triggers |
| `slug-exact` | unit | ❌ | Greppable, but the check is the grep in the item |
| `spinoff-assert` | manual-only | — | The plan's one open question, implemented on its recommendation — reversible on request |
| `vet-agree` | unit | ❌ | Greppable, but nothing asserts it — the check is the grep in the item |
| `vet-behavior` | unit | ✅ | `scripts/vet.sh` is itself the assertion; the diff is comment-only |
| `no-dangle` | unit | ✅ | `scripts/check-skill-catalog.sh` assertion 1, which the vet run calls |
| `closure-counts` | unit | ❌ | Greppable per group; assertion 1 catches a dangling `@`-reference either way |
| `readme-route` | manual-only | — | Doc-audience judgement for a reader who is not in the repo yet |

Closes #50

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01BNJ1X97QtmDGa6VoGSMLze


---
_Generated by [Claude Code](https://claude.ai/code)_

---

## Comments

### Comment by @vzakharov on 2026-09-10T11:03:11Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/52#issuecomment-5617647315](https://github.com/vzakharov/agent-project-boilerplate/pull/52#issuecomment-5617647315)

Proposed squash title/body:

```
feat: #50 give the template-fork path a detemplating skill (pr #52)
```

```
A fresh "Use this template" fork arrives carrying every skill except
the one that turns it into a project, so the operator composes that
prompt by hand while every other stage of the loop has a lever.

`/detemplate <brief>` is that lever, and it routes through `/plan`, so
the prune is reviewed as a diff before anything is deleted. Its
ordering is load-bearing at one point: the catalog goes first, which
flips `check-skill-catalog.sh` assertion 4 from listing the stubs to
enforcing their prune. The watermark is derived from the fork's
creation time, git having no ancestry where the single commit is
unrelated to the source. The run writes no source, so the brief is
filed as the project's first issue and handed back as `/issue #N`,
rather than surviving only as a `CLAUDE.md` paragraph. The skill
deletes itself last, so nothing cites it as an `@`-reference — one
would dangle in the tree of whoever just ran it. `ADOPTING.md`
§ "Template fork" becomes a pointer at it, and the catalog gains
per-group reverse-closure counts and the `docs/img/` row it lacked.

A session asked to build something in such a fork routes there first,
and the frontmatter is what routes it: naming the boilerplate's
literal `owner/repo` costs a reader nothing to check, where naming the
situation would need judgement. `/spinoff` refuses on the same signal,
splitting by it — the template button for the boilerplate,
`/detemplate` for an unpruned fork — and `CLAUDE.md`'s "About this
project" stub carries the notice for a session that never reads the
skill list. The run rewrites that stub, retiring the notice with it.

The vet contract gains its missing clause and a single home. Five
places told an adopter to make `scripts/vet.sh` exit 1 until it runs
real checks, with no exception for a repo that has no stack yet — so a
fork following that literally fails `/finalize` step 1 on every
prose-only PR. `CLAUDE.md` § "Vetting" states the rule once, adds the
environment setup script as the third site a stack change moves, and
the other four point at it. The one part of that site detecting itself
is `gh`: finding none to shim, the session-start hook now reports the
missing setup script into the session context instead of onto stderr.

Closes #50

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `.claude/skills/detemplate/SKILL.md`:13 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
```

**@vzakharov** — 2026-09-10T16:41:38Z

why not just "end state is `/plan`'s"? where does `/issue` come in any of this?

**@vzakharov** — 2026-09-10T17:51:57Z

Right — corrected to `/plan`'s. `/issue` was a slip; it ends at `/plan`, not the other way round. Though your next comment does bring `/issue` in for real, one stage later. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:10 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
```

**@vzakharov** — 2026-09-10T16:47:38Z

here's what I think though: the plan that this skill creates should also include filing an issue whose goal *is* to write the source.

Logic is: we don't want to mess detemplating with code writing, but we also don't want the operator's information provided to go lost. So the approximate sequence is, 

1- the operator types "/detemplate we're writing an automatic job search app"
2- detemplates creates a plan that includes detemplating per se, AND posting an issue
3- it detemplates
4- it posts the issue

the issue can we as detailed or as scarce as the user's request. If the information is scarce it doesn't try to get it just for the sake of writing *future* code. But if e.g. the user attaches a specs to what they're building, or if some further information is required for the sake of detemplating itself (filling CLAUDE.md, README, etc. -- maybe you will find other examples), then it's useful info to be put into that issue.

so then, after detemplating, the skill can give the operator a copypastable block along the lines of "after merging this PR, create a new session and type `/issue #N <issue title>`".

or maybe I'm overthinking it all, you let me know. real talk.


**@vzakharov** — 2026-09-10T17:52:09Z

Not overthinking — implemented as you described. Real talk on the one thing Id push back on and the one thing Id add:

The core of it is right and it fixes a real hole. A run deliberately writes no source, so without the issue the brief survives only as a `CLAUDE.md` paragraph — a place to read it, not a place to work from.

What Id push back on: nothing. The "dont interview them to pad it" clause is in, because thats where this would go wrong — an agent that treats the issue as a spec-gathering exercise turns a two-word brief into twenty questions.

What Id add: it needs one condition. Step 1 already probes whether the repo tracks work as issues (G3); where it doesnt, filing one is wrong, so the brief stays in `CLAUDE.md` and the report says so.

And the scarce-brief case composes better than you might expect: `/issue` already splits an over-broad issue when the scope demands, so "were writing an automatic job search app" as one issue is a legitimate input to the next session rather than a problem.

Landed as Step 5.5 (file it via `/propose-issue`) plus a new Step 7 that hands over `/issue #N <title>` for the session after this PR merges. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


**@vzakharov** — 2026-09-10T18:36:25Z

> whether the repo tracks work as issues

but it's a *new* repo, with *full* boilerplate copied. How can it work or not work with them? I'd say, it always does -- it's a different thing than when it's an existing repo with its own process. In this setup, to a degree, we can dictate the process (convention over configuration).

**@vzakharov** — 2026-09-10T20:00:38Z

Convinced, and it is worse than a preference — the probe was wrong. Step 1 ran `gh api repos/$R/issues?per_page=1 | length` to decide whether G3 travels, which on a tree one commit old always returns 0. So it concluded "this repo does not track work as issues" about the very repo Step 5.5 was about to file the first issue in.

Your framing is the fix: the fork has no process to discover, it inherits this one's. `ADOPTING.md` asks that question of a repo with a history of its own, and I carried the question across without noticing the premise did not.

So, convention over configuration:

- the probe is gone from Step 1, with a note saying why a count measures the fork's age rather than its intent;
- G3 travels by default and Step 5.5 files unconditionally;
- an operator who plans in Linear or Jira **declines G3 at plan review** — a decision they state, in a diff they are already reading, rather than one the step infers behind them;
- the catalog's G3 rule ("only if work is genuinely tracked as GitHub issues") keeps standing for a subset adopter and gains the fork's reversed default beside it.

4f9b91f

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:24 — unresolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
```

**@vzakharov** — 2026-09-10T16:49:12Z

`override-gh` is already present for exactly saying that -- do you think it's needed as belts and braces?

**@vzakharov** — 2026-09-10T17:52:21Z

Agreed, it was redundant — cut. `/override-gh`s description is in every sessions skill list, so the generic restatement bought nothing. What stays is the fork-specific half, which `/override-gh` does *not* cover: a fresh fork is the one place `gh` may genuinely be absent.

Same restatement exists in `/spinoff` and `/from-branch`. Left alone here to keep this PRs scope, but say the word and Ill sweep them. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:28 — unresolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
+
+**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
+the operator has set an environment setup script, and `apt-get install -y gh`
+lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
```

**@vzakharov** — 2026-09-10T16:50:53Z

doesn't the boilerplate provide the code pastable for operator in the setup script? can't there be a litmus test to see if it's not set and warn the operator? (This btw relates not just to this skill but generally running anything where override-gh is adopted.)

**@vzakharov** — 2026-09-10T17:52:22Z

Yes to both, and it turned out the litmus needs no setup-script change at all — `.claude/hooks/session-start.sh` is in-repo and already runs at session start.

It installs no `gh`; it shims one already on `PATH`. So "no `gh` to shim" *is* the litmus: the setup script is unset or missing `apt-get install -y gh`. It used to print that to stderr and continue, which reaches nobody. It now prints to stdout — Claude Code folds a SessionStart hooks stdout into the session context — naming what the operator must add and where, and telling the agent to relay it.

So no operator rewrites their script for the litmus to exist. As you say this is general, not `/detemplate`-specific: `/override-gh` is now its home ("absent that notice, `gh` is present and shimmed"), `ADOPTING.md` and the catalog point there, and `/detemplate` just points too. Verified by running the hook with `gh` hidden from `PATH`. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:141 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
+
+**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
+the operator has set an environment setup script, and `apt-get install -y gh`
+lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
+to shim, warns, and continues. Probe with `gh api repos/{owner}/{repo} --jq
+.visibility` rather than `gh auth status`, which reports a bogus failure in a
+working session. Finding none, Step 3's derivation and `/plan`'s publish step both
+need it: say so and hand the operator the setup script from Step 6 first.
+
+## Step 0 — Refuse where it does not apply
+
+The guard refuses in **both** directions, on a catalog's presence plus `origin`.
+Glob `.claude/skills/*/catalog.md` rather than testing the canonical
+`.claude/skills/sync-agent-infra/catalog.md`: an adopter renames that directory
+after *its* own source, so a fixed-path test misses a stray catalog in exactly
+the trees most likely to carry one.
+
+- **No catalog** → not an unpruned fork. An adopted repo that wants a
+  sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
+  has nothing left to strip.
+- **Catalog present, but `origin` names the boilerplate itself** → this *is* the
+  boilerplate, and what the caller wants is a fork, not a prune. Point at the
+  README's *"Use this template"* button. Without the origin clause,
+  catalog-presence alone would let a session delete this repo's own inventory.
+
+This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
+partition on the same signal, which is why that skill's message names this one.
+
+## Step 1 — Profile the fork; do not interrogate the operator
+
+`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for free:
+there is nothing to clone and no pre-existing `.claude` to merge with. What still
+needs probing, and is decidable by inspection:
+
+```bash
+git remote -v                                  # Step 0's origin clause, and the fork's name
+gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
+gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
+gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
+gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
+```
+
+**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
+in a proxied session before the shim is installed, which is the state a fresh
+fork starts in.
+
+**The stack, including "no stack yet."** That is the normal state of a fork taken
+to start a project, and the state `CLAUDE.md` § "Vetting"'s no-stack-yet clause
+exists for. Read it off the tree rather than asking: a fork whose only commit is
+the template's has no manifest, no lockfile and no source.
+
+What the tree cannot answer, asked as numbered prose in the plan turn per
+`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
+web/remote (G4), and whether the project will have a deploy path, a visual
+surface, deployed logs, a production datastore, or sequential numbered migrations
+— the five that decide the individual G6 rows.
+
+## Step 2 — Read the catalog into the plan, before anything is deleted
+
+The catalog is the input to every group decision **and** is deleted by the
+run (Step 5). So the plan records each decision with the criterion that made it,
+rather than citing a file that will not exist when `/go` executes. Read the
+catalog's § "Reverse closure" in the same pass and record the edits each dropped
+group costs.
+
+This read-then-delete ordering is what routing through `/plan` buys.
+
+## Step 3 — Derive the watermark, which git cannot give you
+
+`ADOPTING.md`'s recipe reads `lastSyncedSha` out of the clone you took. **A
+template fork never made that clone**, and its single commit has no ancestry in
+the source, so there is no SHA in the tree to read. Derive it from the fork's
+creation time instead:
+
+```bash
+gh api repos/<owner>/<fork> --jq .created_at
+gh api repos/vzakharov/agent-project-boilerplate/commits --paginate \
+  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
+```
+
+The newest source commit at or before the fork's `created_at` is the mark.
+
+`lineage` is written in the same breath, and it is the field a hand-filled
+watermark loses:
+
+```json
+"lineage": [{ "repo": "vzakharov/agent-project-boilerplate", "atSha": "<the same sha>" }]
+```
+
+Per `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark", the two fields
+start equal and diverge on the first sync — `lastSyncedSha` advances, and
+`lineage[0].atSha` never moves. That first sync is what overwrites the only other
+trace of the birth point, so a watermark written without `lineage` loses it
+permanently.
+
+## Step 4 — What the plan must contain
+
+Per-group keep/drop with the criterion that decided each; the G6 rows as
```

**@vzakharov** — 2026-09-10T16:54:29Z

btw, let's make ditching the `/implement` stub pre-decided, without asking the operator

**@vzakharov** — 2026-09-10T17:52:35Z

Done — Step 4 now pre-decides it, no question to the operator. The reasoning it states: the catalogs "ask the operator" is about a repo that *shipped* `/implement` under its own history and may have live handoff blocks saying it. A tree one commit old cannot have one, so there is nothing to redirect. Added the fork clause to the catalog bullet too, so the two do not disagree. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:148 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
+
+**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
+the operator has set an environment setup script, and `apt-get install -y gh`
+lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
+to shim, warns, and continues. Probe with `gh api repos/{owner}/{repo} --jq
+.visibility` rather than `gh auth status`, which reports a bogus failure in a
+working session. Finding none, Step 3's derivation and `/plan`'s publish step both
+need it: say so and hand the operator the setup script from Step 6 first.
+
+## Step 0 — Refuse where it does not apply
+
+The guard refuses in **both** directions, on a catalog's presence plus `origin`.
+Glob `.claude/skills/*/catalog.md` rather than testing the canonical
+`.claude/skills/sync-agent-infra/catalog.md`: an adopter renames that directory
+after *its* own source, so a fixed-path test misses a stray catalog in exactly
+the trees most likely to carry one.
+
+- **No catalog** → not an unpruned fork. An adopted repo that wants a
+  sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
+  has nothing left to strip.
+- **Catalog present, but `origin` names the boilerplate itself** → this *is* the
+  boilerplate, and what the caller wants is a fork, not a prune. Point at the
+  README's *"Use this template"* button. Without the origin clause,
+  catalog-presence alone would let a session delete this repo's own inventory.
+
+This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
+partition on the same signal, which is why that skill's message names this one.
+
+## Step 1 — Profile the fork; do not interrogate the operator
+
+`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for free:
+there is nothing to clone and no pre-existing `.claude` to merge with. What still
+needs probing, and is decidable by inspection:
+
+```bash
+git remote -v                                  # Step 0's origin clause, and the fork's name
+gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
+gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
+gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
+gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
+```
+
+**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
+in a proxied session before the shim is installed, which is the state a fresh
+fork starts in.
+
+**The stack, including "no stack yet."** That is the normal state of a fork taken
+to start a project, and the state `CLAUDE.md` § "Vetting"'s no-stack-yet clause
+exists for. Read it off the tree rather than asking: a fork whose only commit is
+the template's has no manifest, no lockfile and no source.
+
+What the tree cannot answer, asked as numbered prose in the plan turn per
+`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
+web/remote (G4), and whether the project will have a deploy path, a visual
+surface, deployed logs, a production datastore, or sequential numbered migrations
+— the five that decide the individual G6 rows.
+
+## Step 2 — Read the catalog into the plan, before anything is deleted
+
+The catalog is the input to every group decision **and** is deleted by the
+run (Step 5). So the plan records each decision with the criterion that made it,
+rather than citing a file that will not exist when `/go` executes. Read the
+catalog's § "Reverse closure" in the same pass and record the edits each dropped
+group costs.
+
+This read-then-delete ordering is what routing through `/plan` buys.
+
+## Step 3 — Derive the watermark, which git cannot give you
+
+`ADOPTING.md`'s recipe reads `lastSyncedSha` out of the clone you took. **A
+template fork never made that clone**, and its single commit has no ancestry in
+the source, so there is no SHA in the tree to read. Derive it from the fork's
+creation time instead:
+
+```bash
+gh api repos/<owner>/<fork> --jq .created_at
+gh api repos/vzakharov/agent-project-boilerplate/commits --paginate \
+  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
+```
+
+The newest source commit at or before the fork's `created_at` is the mark.
+
+`lineage` is written in the same breath, and it is the field a hand-filled
+watermark loses:
+
+```json
+"lineage": [{ "repo": "vzakharov/agent-project-boilerplate", "atSha": "<the same sha>" }]
+```
+
+Per `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark", the two fields
+start equal and diverge on the first sync — `lastSyncedSha` advances, and
+`lineage[0].atSha` never moves. That first sync is what overwrites the only other
+trace of the birth point, so a watermark written without `lineage` loses it
+permanently.
+
+## Step 4 — What the plan must contain
+
+Per-group keep/drop with the criterion that decided each; the G6 rows as
+hydrate-now-or-delete; the reverse-closure edits; the derived watermark and
+`lineage`; the `CLAUDE.md` brief; `scripts/vet.sh`'s disposition; and the
+deletion list. Plus the `## DRY notes` section CLAUDE.md requires of every plan.
+
+## Step 5 — The execution order the plan prescribes
+
+Ordering is load-bearing at exactly one point, and it is the first step:
+
+1. **Delete `.claude/skills/sync-agent-infra/catalog.md` first.** It flips `scripts/check-skill-catalog.sh`
+   assertion 4 from "the stubs are the shipped product, merely listed" to "a stub
+   is a stowaway", and it un-refuses `/spinoff`, whose guard is literally the
+   catalog's presence. Sweep it first and the G6 prune is enforced by the vet run
+   instead of remembered.
+2. **The rest of the `never` rows**: `README.md` — replaced with the project's,
+   not merely deleted — `ADOPTING.md`, and **`docs/img/`** with it. That
+   directory is `ADOPTING.md`'s only asset, so a literal row-by-row sweep strands
+   it as an orphan.
+3. **Prune the groups**, applying the reverse-closure edits the plan recorded.
+4. **Fill `CLAUDE.md`'s "About this project" stub** from the brief — which
+   retires the standing notice in § "Recognizing an undetemplated fork" along
+   with it — and delete § "Git conventions"'s adopter-inverts rule, which
+   instructs adopters to delete it.
+5. **Write the watermark** (Step 3) and clear both of `/sync-agent-infra`'s stub
+   markers: the banner and the `STUB` in its frontmatter description. Assertion 4
+   fails a half-cleared pair.
+6. **`scripts/vet.sh`**: leave the exit alone where the fork has no stack yet, and
```

**@vzakharov** — 2026-09-10T16:55:42Z

how would it have any stack if it's a fork of the boilerplate itself? or are you envisioning the situation when someone did some work on a forked template before realizing they should've detemplated?

**@vzakharov** — 2026-09-10T17:52:36Z

The second one — someone pushed a stack before realising they should have detemplated first. Rewritten to say so: leaving the exit alone is *the normal case* (a fork taken to start a project has no stack), and wiring real checks is the exception for a tree that already grew one. It read as an even split before, which it is not. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:191 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
+
+**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
+the operator has set an environment setup script, and `apt-get install -y gh`
+lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
+to shim, warns, and continues. Probe with `gh api repos/{owner}/{repo} --jq
+.visibility` rather than `gh auth status`, which reports a bogus failure in a
+working session. Finding none, Step 3's derivation and `/plan`'s publish step both
+need it: say so and hand the operator the setup script from Step 6 first.
+
+## Step 0 — Refuse where it does not apply
+
+The guard refuses in **both** directions, on a catalog's presence plus `origin`.
+Glob `.claude/skills/*/catalog.md` rather than testing the canonical
+`.claude/skills/sync-agent-infra/catalog.md`: an adopter renames that directory
+after *its* own source, so a fixed-path test misses a stray catalog in exactly
+the trees most likely to carry one.
+
+- **No catalog** → not an unpruned fork. An adopted repo that wants a
+  sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
+  has nothing left to strip.
+- **Catalog present, but `origin` names the boilerplate itself** → this *is* the
+  boilerplate, and what the caller wants is a fork, not a prune. Point at the
+  README's *"Use this template"* button. Without the origin clause,
+  catalog-presence alone would let a session delete this repo's own inventory.
+
+This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
+partition on the same signal, which is why that skill's message names this one.
+
+## Step 1 — Profile the fork; do not interrogate the operator
+
+`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for free:
+there is nothing to clone and no pre-existing `.claude` to merge with. What still
+needs probing, and is decidable by inspection:
+
+```bash
+git remote -v                                  # Step 0's origin clause, and the fork's name
+gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
+gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
+gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
+gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
+```
+
+**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
+in a proxied session before the shim is installed, which is the state a fresh
+fork starts in.
+
+**The stack, including "no stack yet."** That is the normal state of a fork taken
+to start a project, and the state `CLAUDE.md` § "Vetting"'s no-stack-yet clause
+exists for. Read it off the tree rather than asking: a fork whose only commit is
+the template's has no manifest, no lockfile and no source.
+
+What the tree cannot answer, asked as numbered prose in the plan turn per
+`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
+web/remote (G4), and whether the project will have a deploy path, a visual
+surface, deployed logs, a production datastore, or sequential numbered migrations
+— the five that decide the individual G6 rows.
+
+## Step 2 — Read the catalog into the plan, before anything is deleted
+
+The catalog is the input to every group decision **and** is deleted by the
+run (Step 5). So the plan records each decision with the criterion that made it,
+rather than citing a file that will not exist when `/go` executes. Read the
+catalog's § "Reverse closure" in the same pass and record the edits each dropped
+group costs.
+
+This read-then-delete ordering is what routing through `/plan` buys.
+
+## Step 3 — Derive the watermark, which git cannot give you
+
+`ADOPTING.md`'s recipe reads `lastSyncedSha` out of the clone you took. **A
+template fork never made that clone**, and its single commit has no ancestry in
+the source, so there is no SHA in the tree to read. Derive it from the fork's
+creation time instead:
+
+```bash
+gh api repos/<owner>/<fork> --jq .created_at
+gh api repos/vzakharov/agent-project-boilerplate/commits --paginate \
+  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
+```
+
+The newest source commit at or before the fork's `created_at` is the mark.
+
+`lineage` is written in the same breath, and it is the field a hand-filled
+watermark loses:
+
+```json
+"lineage": [{ "repo": "vzakharov/agent-project-boilerplate", "atSha": "<the same sha>" }]
+```
+
+Per `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark", the two fields
+start equal and diverge on the first sync — `lastSyncedSha` advances, and
+`lineage[0].atSha` never moves. That first sync is what overwrites the only other
+trace of the birth point, so a watermark written without `lineage` loses it
+permanently.
+
+## Step 4 — What the plan must contain
+
+Per-group keep/drop with the criterion that decided each; the G6 rows as
+hydrate-now-or-delete; the reverse-closure edits; the derived watermark and
+`lineage`; the `CLAUDE.md` brief; `scripts/vet.sh`'s disposition; and the
+deletion list. Plus the `## DRY notes` section CLAUDE.md requires of every plan.
+
+## Step 5 — The execution order the plan prescribes
+
+Ordering is load-bearing at exactly one point, and it is the first step:
+
+1. **Delete `.claude/skills/sync-agent-infra/catalog.md` first.** It flips `scripts/check-skill-catalog.sh`
+   assertion 4 from "the stubs are the shipped product, merely listed" to "a stub
+   is a stowaway", and it un-refuses `/spinoff`, whose guard is literally the
+   catalog's presence. Sweep it first and the G6 prune is enforced by the vet run
+   instead of remembered.
+2. **The rest of the `never` rows**: `README.md` — replaced with the project's,
+   not merely deleted — `ADOPTING.md`, and **`docs/img/`** with it. That
+   directory is `ADOPTING.md`'s only asset, so a literal row-by-row sweep strands
+   it as an orphan.
+3. **Prune the groups**, applying the reverse-closure edits the plan recorded.
+4. **Fill `CLAUDE.md`'s "About this project" stub** from the brief — which
+   retires the standing notice in § "Recognizing an undetemplated fork" along
+   with it — and delete § "Git conventions"'s adopter-inverts rule, which
+   instructs adopters to delete it.
+5. **Write the watermark** (Step 3) and clear both of `/sync-agent-infra`'s stub
+   markers: the banner and the `STUB` in its frontmatter description. Assertion 4
+   fails a half-cleared pair.
+6. **`scripts/vet.sh`**: leave the exit alone where the fork has no stack yet, and
+   wire the real checks where it has one — CLAUDE.md § "Vetting" owns that
+   contract, and names `.claude/hooks/session-start.sh`'s dependency install as
+   the paired site.
+7. **Delete this skill.** Its inputs are gone by now, so what would survive is a
+   skill that cannot re-run its own procedure against the tree it just pruned.
+8. **`bash scripts/vet.sh`** — now enforcing the stub prune, the catalog being
+   gone — then Step 6's text in the report.
+
+## Step 6 — Hand back the setup script
```

**@vzakharov** — 2026-09-10T16:57:00Z

ah, so here's where you right about it. I'm guessing we do need a litmus test, checked at the very beginning, and asked to rerun if not present. (Ideally we don't need to change the current setup script itself for the litmus to be present -- otherwise every operator will have to rewrite their script. Possible but better avoided.)

**@vzakharov** — 2026-09-10T17:52:38Z

This is where the previous thread landed — same fix, and it needs no change to anyones existing setup script. `.claude/hooks/session-start.sh` is in-repo, runs at session start, and finding no `gh` to shim now reports that into the session context instead of onto stderr. So the litmus is present for every adopter automatically, and the notice names the paste-able line and where the setting lives.

Not "rerun if not present", though: the hook still exits 0 and the session continues. Refusing to start would block work that needs no `gh` at all, and the setup script only takes effect on a restart anyway — so the agent is told to relay it before running anything `gh`-dependent, which is where it actually bites. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:219 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
+
+**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
+the operator has set an environment setup script, and `apt-get install -y gh`
+lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
+to shim, warns, and continues. Probe with `gh api repos/{owner}/{repo} --jq
+.visibility` rather than `gh auth status`, which reports a bogus failure in a
+working session. Finding none, Step 3's derivation and `/plan`'s publish step both
+need it: say so and hand the operator the setup script from Step 6 first.
+
+## Step 0 — Refuse where it does not apply
+
+The guard refuses in **both** directions, on a catalog's presence plus `origin`.
+Glob `.claude/skills/*/catalog.md` rather than testing the canonical
+`.claude/skills/sync-agent-infra/catalog.md`: an adopter renames that directory
+after *its* own source, so a fixed-path test misses a stray catalog in exactly
+the trees most likely to carry one.
+
+- **No catalog** → not an unpruned fork. An adopted repo that wants a
+  sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
+  has nothing left to strip.
+- **Catalog present, but `origin` names the boilerplate itself** → this *is* the
+  boilerplate, and what the caller wants is a fork, not a prune. Point at the
+  README's *"Use this template"* button. Without the origin clause,
+  catalog-presence alone would let a session delete this repo's own inventory.
+
+This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
+partition on the same signal, which is why that skill's message names this one.
+
+## Step 1 — Profile the fork; do not interrogate the operator
+
+`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for free:
+there is nothing to clone and no pre-existing `.claude` to merge with. What still
+needs probing, and is decidable by inspection:
+
+```bash
+git remote -v                                  # Step 0's origin clause, and the fork's name
+gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
+gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
+gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
+gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
+```
+
+**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
+in a proxied session before the shim is installed, which is the state a fresh
+fork starts in.
+
+**The stack, including "no stack yet."** That is the normal state of a fork taken
+to start a project, and the state `CLAUDE.md` § "Vetting"'s no-stack-yet clause
+exists for. Read it off the tree rather than asking: a fork whose only commit is
+the template's has no manifest, no lockfile and no source.
+
+What the tree cannot answer, asked as numbered prose in the plan turn per
+`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
+web/remote (G4), and whether the project will have a deploy path, a visual
+surface, deployed logs, a production datastore, or sequential numbered migrations
+— the five that decide the individual G6 rows.
+
+## Step 2 — Read the catalog into the plan, before anything is deleted
+
+The catalog is the input to every group decision **and** is deleted by the
+run (Step 5). So the plan records each decision with the criterion that made it,
+rather than citing a file that will not exist when `/go` executes. Read the
+catalog's § "Reverse closure" in the same pass and record the edits each dropped
+group costs.
+
+This read-then-delete ordering is what routing through `/plan` buys.
+
+## Step 3 — Derive the watermark, which git cannot give you
+
+`ADOPTING.md`'s recipe reads `lastSyncedSha` out of the clone you took. **A
+template fork never made that clone**, and its single commit has no ancestry in
+the source, so there is no SHA in the tree to read. Derive it from the fork's
+creation time instead:
+
+```bash
+gh api repos/<owner>/<fork> --jq .created_at
+gh api repos/vzakharov/agent-project-boilerplate/commits --paginate \
+  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
+```
+
+The newest source commit at or before the fork's `created_at` is the mark.
+
+`lineage` is written in the same breath, and it is the field a hand-filled
+watermark loses:
+
+```json
+"lineage": [{ "repo": "vzakharov/agent-project-boilerplate", "atSha": "<the same sha>" }]
+```
+
+Per `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark", the two fields
+start equal and diverge on the first sync — `lastSyncedSha` advances, and
+`lineage[0].atSha` never moves. That first sync is what overwrites the only other
+trace of the birth point, so a watermark written without `lineage` loses it
+permanently.
+
+## Step 4 — What the plan must contain
+
+Per-group keep/drop with the criterion that decided each; the G6 rows as
+hydrate-now-or-delete; the reverse-closure edits; the derived watermark and
+`lineage`; the `CLAUDE.md` brief; `scripts/vet.sh`'s disposition; and the
+deletion list. Plus the `## DRY notes` section CLAUDE.md requires of every plan.
+
+## Step 5 — The execution order the plan prescribes
+
+Ordering is load-bearing at exactly one point, and it is the first step:
+
+1. **Delete `.claude/skills/sync-agent-infra/catalog.md` first.** It flips `scripts/check-skill-catalog.sh`
+   assertion 4 from "the stubs are the shipped product, merely listed" to "a stub
+   is a stowaway", and it un-refuses `/spinoff`, whose guard is literally the
+   catalog's presence. Sweep it first and the G6 prune is enforced by the vet run
+   instead of remembered.
+2. **The rest of the `never` rows**: `README.md` — replaced with the project's,
+   not merely deleted — `ADOPTING.md`, and **`docs/img/`** with it. That
+   directory is `ADOPTING.md`'s only asset, so a literal row-by-row sweep strands
+   it as an orphan.
+3. **Prune the groups**, applying the reverse-closure edits the plan recorded.
+4. **Fill `CLAUDE.md`'s "About this project" stub** from the brief — which
+   retires the standing notice in § "Recognizing an undetemplated fork" along
+   with it — and delete § "Git conventions"'s adopter-inverts rule, which
+   instructs adopters to delete it.
+5. **Write the watermark** (Step 3) and clear both of `/sync-agent-infra`'s stub
+   markers: the banner and the `STUB` in its frontmatter description. Assertion 4
+   fails a half-cleared pair.
+6. **`scripts/vet.sh`**: leave the exit alone where the fork has no stack yet, and
+   wire the real checks where it has one — CLAUDE.md § "Vetting" owns that
+   contract, and names `.claude/hooks/session-start.sh`'s dependency install as
+   the paired site.
+7. **Delete this skill.** Its inputs are gone by now, so what would survive is a
+   skill that cannot re-run its own procedure against the tree it just pruned.
+8. **`bash scripts/vet.sh`** — now enforcing the stub prune, the catalog being
+   gone — then Step 6's text in the report.
+
+## Step 6 — Hand back the setup script
+
+`ADOPTING.md` § "Hand the operator a setup script" is the one step no agent can
+apply: the environment setup script lives in Claude Code's environment settings,
+is set by a human in the web UI, and has no API, MCP tool or in-repo file behind
+it. Step 5 deletes that file, so the deliverable travels here instead — **text in
+the report** the operator pastes into the setting.
+
+Two reasons it matters:
+
+- **It is where `gh` comes from.** `apt-get install -y gh` belongs in it. Without
+  `gh` on `PATH`, `.claude/hooks/session-start.sh` prints `gh not found on PATH;
+  skipping gh proxy shim` and continues — so the shim silently never installs and
+  every `gh`-dependent skill fails later, far from the cause.
+- **It is the only place a toolchain version can be pinned** for remote sessions,
+  and `scripts/vet.sh` running under the wrong one is a confusing failure.
+
+It runs **once, when the environment snapshot is built**, then is cached
+([docs](https://code.claude.com/docs/en/claude-code-on-the-web#setup-scripts)) —
+which is why the session-start hook re-syncs dependencies on every session start
+rather than trusting the snapshot.
+
+**Where it goes**, since "the settings" is not enough to find it: in the session
+composer, the environment picker → **Cloud** → the environment itself, whose
+**gear icon** opens its settings. It is per-environment, so an operator with
+several is editing one of them rather than a global.
+
+Write the script for the stack the brief names, and carry these across whatever it
```

**@vzakharov** — 2026-09-10T16:58:08Z

Yeah, again, at this point there's -- in the standard case -- no stack yet. But it's worth adding somewhere (not in this skill) for the agent to tell the user to change the setup script according to stack changes.

**@vzakharov** — 2026-09-10T17:52:45Z

Right, and that is now stated outside this skill. `CLAUDE.md` § "Vetting" already named `scripts/vet.sh` and the session-start hooks dependency install as the two sites that move when a stack lands; it now names the environment setup script as the third — the one no agent can move, so a toolchain change (new runtime, bumped pin, new system dependency, package-manager swap) is unfinished until the report says what the operator must add there.

`/detemplate` itself keeps only the no-stack case as normal, per the thread above. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:276 — resolved

```diff
@@ -0,0 +1,223 @@
+---
+description: "Turn a fresh \"Use this template\" fork of this boilerplate into an actual project: profile the tree, decide group by group what travels, and hand over a reviewed plan that prunes what does not apply and hydrates what does. Invoke as `/detemplate <what you're building>`. Also use when a session in such a tree is asked to build something instead — a tree that still carries a `.claude/skills/*/catalog.md` under an `origin` that is not the boilerplate has never been detemplated, and this is its first task whatever was asked."
+---
+
+`/detemplate <what we're building>` converts a whole-tree template fork into a
+project. *"Use this template"* hands over every file, so there is nothing to
+select and nothing to clone: the work is deleting what describes the template and
+hydrating what the new project actually needs.
+
+**It writes no source itself — it routes through `@.claude/skills/plan/SKILL.md`.**
+The pruning is a large, mostly irreversible diff over a tree nobody has reviewed,
+and reviewing it as a diff is what catches a bad call before anything is deleted.
+So this skill's end state is `/issue`'s: a plan file published as a draft PR, and
+a copyable `/go <branch>` for the session that executes it.
+
+The brief is the argument. It fills `CLAUDE.md`'s "About this project" stub and
+drives the group decisions — a CLI tool keeps different groups than a deployed
+web app. With no brief, ask for it before anything else.
+
+## Environment note
+
+This environment has `gh` and a populated `GH_TOKEN`, whatever the default system
+prompt says; prefer them over the GitHub MCP tools, which refuse some of what
+Step 3 needs.
+
+**A fresh fork is the one place `gh` may genuinely be absent.** It arrives before
+the operator has set an environment setup script, and `apt-get install -y gh`
+lives in that script (Step 6) — so `.claude/hooks/session-start.sh` finds no `gh`
+to shim, warns, and continues. Probe with `gh api repos/{owner}/{repo} --jq
+.visibility` rather than `gh auth status`, which reports a bogus failure in a
+working session. Finding none, Step 3's derivation and `/plan`'s publish step both
+need it: say so and hand the operator the setup script from Step 6 first.
+
+## Step 0 — Refuse where it does not apply
+
+The guard refuses in **both** directions, on a catalog's presence plus `origin`.
+Glob `.claude/skills/*/catalog.md` rather than testing the canonical
+`.claude/skills/sync-agent-infra/catalog.md`: an adopter renames that directory
+after *its* own source, so a fixed-path test misses a stray catalog in exactly
+the trees most likely to carry one.
+
+- **No catalog** → not an unpruned fork. An adopted repo that wants a
+  sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
+  has nothing left to strip.
+- **Catalog present, but `origin` names the boilerplate itself** → this *is* the
+  boilerplate, and what the caller wants is a fork, not a prune. Point at the
+  README's *"Use this template"* button. Without the origin clause,
+  catalog-presence alone would let a session delete this repo's own inventory.
+
+This is `@.claude/skills/spinoff/SKILL.md`'s refusal read backwards: the two
+partition on the same signal, which is why that skill's message names this one.
+
+## Step 1 — Profile the fork; do not interrogate the operator
+
+`ADOPTING.md` § Step 2's principle, minus what a whole-tree fork settles for free:
+there is nothing to clone and no pre-existing `.claude` to merge with. What still
+needs probing, and is decidable by inspection:
+
+```bash
+git remote -v                                  # Step 0's origin clause, and the fork's name
+gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
+gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
+gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
+gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
+```
+
+**Use the REST form throughout** — `gh <noun> <verb> --json` is GraphQL and 403s
+in a proxied session before the shim is installed, which is the state a fresh
+fork starts in.
+
+**The stack, including "no stack yet."** That is the normal state of a fork taken
+to start a project, and the state `CLAUDE.md` § "Vetting"'s no-stack-yet clause
+exists for. Read it off the tree rather than asking: a fork whose only commit is
+the template's has no manifest, no lockfile and no source.
+
+What the tree cannot answer, asked as numbered prose in the plan turn per
+`@.claude/skills/plan/SKILL.md` Part 2: whether sessions run on Claude Code
+web/remote (G4), and whether the project will have a deploy path, a visual
+surface, deployed logs, a production datastore, or sequential numbered migrations
+— the five that decide the individual G6 rows.
+
+## Step 2 — Read the catalog into the plan, before anything is deleted
+
+The catalog is the input to every group decision **and** is deleted by the
+run (Step 5). So the plan records each decision with the criterion that made it,
+rather than citing a file that will not exist when `/go` executes. Read the
+catalog's § "Reverse closure" in the same pass and record the edits each dropped
+group costs.
+
+This read-then-delete ordering is what routing through `/plan` buys.
+
+## Step 3 — Derive the watermark, which git cannot give you
+
+`ADOPTING.md`'s recipe reads `lastSyncedSha` out of the clone you took. **A
+template fork never made that clone**, and its single commit has no ancestry in
+the source, so there is no SHA in the tree to read. Derive it from the fork's
+creation time instead:
+
+```bash
+gh api repos/<owner>/<fork> --jq .created_at
+gh api repos/vzakharov/agent-project-boilerplate/commits --paginate \
+  --jq '.[] | [.sha, .commit.committer.date] | @tsv'
+```
+
+The newest source commit at or before the fork's `created_at` is the mark.
+
+`lineage` is written in the same breath, and it is the field a hand-filled
+watermark loses:
+
+```json
+"lineage": [{ "repo": "vzakharov/agent-project-boilerplate", "atSha": "<the same sha>" }]
+```
+
+Per `@.claude/skills/sync-agent-infra/SKILL.md` § "The watermark", the two fields
+start equal and diverge on the first sync — `lastSyncedSha` advances, and
+`lineage[0].atSha` never moves. That first sync is what overwrites the only other
+trace of the birth point, so a watermark written without `lineage` loses it
+permanently.
+
+## Step 4 — What the plan must contain
+
+Per-group keep/drop with the criterion that decided each; the G6 rows as
+hydrate-now-or-delete; the reverse-closure edits; the derived watermark and
+`lineage`; the `CLAUDE.md` brief; `scripts/vet.sh`'s disposition; and the
+deletion list. Plus the `## DRY notes` section CLAUDE.md requires of every plan.
+
+## Step 5 — The execution order the plan prescribes
+
+Ordering is load-bearing at exactly one point, and it is the first step:
+
+1. **Delete `.claude/skills/sync-agent-infra/catalog.md` first.** It flips `scripts/check-skill-catalog.sh`
+   assertion 4 from "the stubs are the shipped product, merely listed" to "a stub
+   is a stowaway", and it un-refuses `/spinoff`, whose guard is literally the
+   catalog's presence. Sweep it first and the G6 prune is enforced by the vet run
+   instead of remembered.
+2. **The rest of the `never` rows**: `README.md` — replaced with the project's,
+   not merely deleted — `ADOPTING.md`, and **`docs/img/`** with it. That
+   directory is `ADOPTING.md`'s only asset, so a literal row-by-row sweep strands
+   it as an orphan.
+3. **Prune the groups**, applying the reverse-closure edits the plan recorded.
+4. **Fill `CLAUDE.md`'s "About this project" stub** from the brief — which
+   retires the standing notice in § "Recognizing an undetemplated fork" along
+   with it — and delete § "Git conventions"'s adopter-inverts rule, which
+   instructs adopters to delete it.
+5. **Write the watermark** (Step 3) and clear both of `/sync-agent-infra`'s stub
+   markers: the banner and the `STUB` in its frontmatter description. Assertion 4
+   fails a half-cleared pair.
+6. **`scripts/vet.sh`**: leave the exit alone where the fork has no stack yet, and
+   wire the real checks where it has one — CLAUDE.md § "Vetting" owns that
+   contract, and names `.claude/hooks/session-start.sh`'s dependency install as
+   the paired site.
+7. **Delete this skill.** Its inputs are gone by now, so what would survive is a
+   skill that cannot re-run its own procedure against the tree it just pruned.
+8. **`bash scripts/vet.sh`** — now enforcing the stub prune, the catalog being
+   gone — then Step 6's text in the report.
+
+## Step 6 — Hand back the setup script
+
+`ADOPTING.md` § "Hand the operator a setup script" is the one step no agent can
+apply: the environment setup script lives in Claude Code's environment settings,
+is set by a human in the web UI, and has no API, MCP tool or in-repo file behind
+it. Step 5 deletes that file, so the deliverable travels here instead — **text in
+the report** the operator pastes into the setting.
+
+Two reasons it matters:
+
+- **It is where `gh` comes from.** `apt-get install -y gh` belongs in it. Without
+  `gh` on `PATH`, `.claude/hooks/session-start.sh` prints `gh not found on PATH;
+  skipping gh proxy shim` and continues — so the shim silently never installs and
+  every `gh`-dependent skill fails later, far from the cause.
+- **It is the only place a toolchain version can be pinned** for remote sessions,
+  and `scripts/vet.sh` running under the wrong one is a confusing failure.
+
+It runs **once, when the environment snapshot is built**, then is cached
+([docs](https://code.claude.com/docs/en/claude-code-on-the-web#setup-scripts)) —
+which is why the session-start hook re-syncs dependencies on every session start
+rather than trusting the snapshot.
+
+**Where it goes**, since "the settings" is not enough to find it: in the session
+composer, the environment picker → **Cloud** → the environment itself, whose
+**gear icon** opens its settings. It is per-environment, so an operator with
+several is editing one of them rather than a global.
+
+Write the script for the stack the brief names, and carry these across whatever it
+is — each records a trap that actually bit:
+
+1. **No top-level `cd` into the repo.** At setup-script time the repo is not
+   reliably at `/home/user/<project>`, and a `cd` there crashes the script.
+2. **Pin versions as literals**, with a comment naming the repo file each pin must
+   track. Reading `.nvmrc` or `.tool-versions` needs the repo, which brings back 1.
+3. **Reach non-interactive shells.** A profile edit alone does not; symlinking the
+   toolchain into `/usr/local/bin` does.
+4. **Check what the base image ships and where it sits on `PATH`.** Base images
+   carry their own toolchain directories, and some sort *earlier* than
+   `/usr/local/bin` — so `which` keeps resolving a stale binary past a correct
+   symlink. Look for that shape before assuming yours won.
+5. **`apt-get install -y gh`** — per above.
+6. **Prime the dependency cache last**, guarded, since the repo directory may be
+   absent.
+
+Say plainly in the report that this is the one step you could not apply yourself.
+
+## Recognizing an undetemplated fork
+
+A session that opens in a fresh fork and is asked to build a feature should route
+here first, rather than building product code on top of the template's inventory.
+The signal is Step 0's predicate read positively: a `.claude/skills/*/catalog.md`
+present, and `origin` not naming the boilerplate.
+
+Two surfaces carry it, catching different moments. This skill's frontmatter
+`description` names the *situation* and not only the command, so an ordinary build
+request in such a tree matches it. And `CLAUDE.md`'s "About this project" stub
+carries the standing instruction, being always-loaded: while that stub is
+unfilled and the tree still has the catalog, the first task is `/detemplate`
+whatever was asked. Step 5.4 rewrites that very stub, so the notice retires with
+the condition it describes.
+
+**Nothing anywhere `@`-references this skill's own `SKILL.md`** — every mention
+is a bare name, this sentence included. Step 5.7 deletes the skill, so such a
+pointer would dangle in the tree of whoever just ran it and fail
+`check-skill-catalog.sh` assertion 1 — the same property that makes
+`/test-on-gh`'s bare-name mentions correct to leave alone (the catalog's
+§ "Reverse closure").
```

**@vzakharov** — 2026-09-10T17:03:10Z

To read this, the agent needs to use the skill -- which won't be used unless the operator calls the skill -- in which case this prose is a no-op. But I like your using the frontmatter as a litmus test, what if we make the frontmatter scream: "if you see this skill description and this is not THE boilerplate repo, load this skill regardless and read para. Recognizing an undetemplated fork"

The risk ofc is that the agent working in the boilerplate repo *by intent* -- as we're doing now -- might be overly cautious and read this anyway, probably concluding the right thing, but spending an expensive round trip on that. Can we dogfood? Do you see it's the boilerplate repo in your basic system prompt, or do you need additional actions to figure out "where you are"?

**@vzakharov** — 2026-09-10T17:52:57Z

Dogfooded, and the answer is good: **yes, I can see it from the system prompt, no tool call.** This sessions prompt carries `Primary working directory: /home/user/agent-project-boilerplate` and a repository-scope line naming `vzakharov/agent-project-boilerplate`. So the boilerplate-by-intent case costs nothing — I read the description, check the path already in front of me, and move on. Worst case (a local session with an ambiguous cwd) it is one `git remote -v`, not a round trip to you.

That is what makes your version work, so the frontmatter now screams it — but keyed on the **repository**, not the situation:

> A run deletes this skill, so this description exists in exactly two places: the boilerplate itself, and a fork nobody has detemplated. If the repository you are in is not `vzakharov/agent-project-boilerplate`, load this skill and read § "Recognizing an undetemplated fork" before doing anything else, whatever you were asked.

Naming the repo rather than the situation is what keeps the false-positive cheap: "is this an undetemplated fork?" needs judgement, `owner/repo != literal` does not. And the self-deletion is what makes the premise hold — the description cannot exist in a detemplated tree, so those really are the only two cases.

You are right that the section itself was doing no routing work. It now says so and stops explaining itself: it is what gets read *after* the description sent someone there, which is why the description has to carry the trigger. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/spinoff/SKILL.md`:38 — unresolved

```diff
@@ -21,20 +21,30 @@ principle.
 
 End state: the target exists; its `main` carries the foundation's already-reviewed
 half, enough for a session there to run `/handle`, with `bash
-scripts/check-skill-catalog.sh` passing and `scripts/vet.sh` refusing to certify;
+scripts/check-skill-catalog.sh` passing and `scripts/vet.sh` passing over a tree
+that has no stack in it yet;
 a draft PR carries the rest, rewritten for the target; and the operator holds a
 copyable command that opens the next session in the new repo.
 
 ## Two invariants
 
-**Not from the boilerplate.** If the caller has a catalog — glob
-`.claude/skills/*/catalog.md`, don't test the canonical
+**Not from the boilerplate, and not from an unpruned fork of it.** If the caller
+has a catalog — glob `.claude/skills/*/catalog.md`, don't test the canonical
 `.claude/skills/sync-agent-infra/catalog.md`, since an adopter renames that
-directory after *its* own source — **stop** and point at that repo's `README.md`
-§ "Create a new project from this template". The catalog is what a tree has when
-it *is* the boilerplate or an unpruned copy of one, and in either case a spinoff
-is the wrong operation — the template route plus `ADOPTING.md` produce a project,
-and that pruned result is a legitimate caller here later.
+directory after *its* own source — **stop**. A spinoff is the wrong operation
+either way, but the two cases want different answers, so read `origin` before
+replying:
+
+- **`origin` names the boilerplate** → this *is* the boilerplate. Point at its
```

**@vzakharov** — 2026-09-10T17:03:50Z

is "the boilerplate" unambiguous enough? We sure a legit adopting project having "boilerplate" in its name won't get false-positived?

**@vzakharov** — 2026-09-10T17:53:08Z

Good catch — it was not unambiguous, and `acme-boilerplate` is exactly the false positive. Both guards now name the full `vzakharov/agent-project-boilerplate` and say outright to match `owner/repo`, never the substring `boilerplate`. `/detemplate` Step 0 gets the same clause, since the two partition on one signal and a mismatch there would be worse — it would prune the wrong tree rather than merely refuse. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/spinoff/SKILL.md`:299 — resolved

```diff
@@ -278,13 +290,17 @@ Three consequences, each stated by a check rather than by taste:
   both leaving it out and carrying it hydrated pass. Under a mismatched stack the
   absence is unconditional: a deploy lane for another language is not a starting
   point.
-- **`main`'s `vet.sh` exits non-zero**, per the contract its own header and the
-  caller's `CLAUDE.md` § "Vetting" already state. `main` has no stack yet, so the
-  honest script refuses to certify and PR #1 wires in the real checks. An exit-0
-  `vet.sh` there is the false green the boilerplate exists to prevent, sitting
-  unchallenged until PR #1 lands. **Do not weaken the caller's `vet.sh` to make
-  the seed pass** — the reduction is a *refusal to certify*, not a narrowed set
-  of checks that quietly passes.
+- **`main`'s `vet.sh` is the stub, and the stub exits `0`** — `main` has no stack
+  yet, so the loop's own checks are the whole run and they genuinely pass. That
+  is `CLAUDE.md` § "Vetting"'s no-stack-yet clause, and the assertion worth
+  making is the pair: the script passes **and** it names no stack-specific
+  checks. A non-zero exit here would be a `main` whose `/finalize` cannot pass
+  for a reason the contract calls legitimate.
+  **What must not happen is the caller's real `vet.sh` reaching `main`** —
```

**@vzakharov** — 2026-09-10T17:05:18Z

who's the "caller" again in this discourse? trying to figure out what this paragraph means.

**@vzakharov** — 2026-09-10T17:53:09Z

The adopter you invoked `/spinoff` from — defined 260 lines earlier, which is too far to carry. Rewritten to "the source repos own `vet.sh`", with the gloss "the working one you are standing in, which runs its lint, types and tests", so the sentence stands on its own.

The paragraph means: do not copy that script onto the new repos `main`. `main` has no stack yet, so a real `vet.sh` there would certify checks against code that does not exist — green, and meaningless, until PR #1 lands. Also dropped the trailing "the seed refuses nothing because it has nothing to refuse", which was making the same point a third time. 2c64122

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/detemplate/SKILL.md`:67 — unresolved

```diff
@@ -60,14 +64,21 @@ needs probing, and is decidable by inspection:
 git remote -v                                  # Step 0's origin clause, and the fork's name
 gh api "repos/$R" --jq .default_branch         # the trunk G2 assumes
 gh api "repos/$R" --jq .allow_squash_merge     # does the squash discipline apply?
-gh api "repos/$R/issues?per_page=1" --jq length        # is work tracked as issues? (G3)
 gh api "repos/$R/actions/workflows" --jq .total_count  # is there CI? (G5)
```

**@vzakharov** — 2026-09-10T20:49:22Z

again, no actions can be here for the same reason we removed issues: it's been just templated from the boilerplate repo. pls sweep for similar misunderstandings.

**@vzakharov** — 2026-09-10T20:59:37Z

Right, and worse than a repeat — this one is zero *structurally*, not just early: the boilerplate ships no `.github/` at all, so a template copy carries none and `actions/workflows` returns 0 in every fresh fork forever. The step read that as "no CI" and dropped G5 on a repo that has had no chance to have any.

The sweep, and the test it produced. A probe here **reads a setting, never a count**:

- `default_branch`, `allow_squash_merge` — kept. They have values on the fork's first day, chosen by whoever created it or inherited from their org's defaults, and they gate what the loop *may* do rather than describing what the repo has done.
- open issues (G3), registered workflows (G5) — both gone. Counts, zero for reasons about the fork's age, handed back as if they were your intent.

So G3 and G5 both travel by default now, declined at plan review. For G5 that costs a fork with no CI yet only the files: its skills wait for a workflow rather than requiring one.

Two more the sweep turned up, both fixed in the same commit:

- Step 6 still quoted the session-start hook's *old* stderr one-liner and called the missing shim silent — stale as of this PR's own hook change, which reports into the session context.
- `/spinoff`'s `main`-floor rule, which is your other comment — answered there.

Checked and left alone: Step 4's `/implement` disposition and Step 5.7's `vet.sh` clause already reason from the fork's age in the right direction, and the G4/G6 questions are asked as prose rather than probed.

930c660

---
_Generated by [Claude Code](https://claude.ai/code)_

---

### `.claude/skills/spinoff/SKILL.md`:305 — unresolved

```diff
@@ -296,11 +298,11 @@ Three consequences, each stated by a check rather than by taste:
   making is the pair: the script passes **and** it names no stack-specific
   checks. A non-zero exit here would be a `main` whose `/finalize` cannot pass
   for a reason the contract calls legitimate.
-  **What must not happen is the caller's real `vet.sh` reaching `main`** —
-  carried across, it certifies a stack that is not there yet, and the false green
-  sits unchallenged until PR #1 lands. The step's invariant is that PR #1 is
-  where the stack and its checks arrive together; the seed refuses nothing
-  because it has nothing to refuse.
+  **What must not happen is the source repo's own `vet.sh` reaching `main`** —
+  the working one you are standing in, which runs its lint, types and tests.
+  Carried across, it certifies a stack the target does not have yet, and the
+  false green sits unchallenged until PR #1 lands. The target's stack and the
+  checks over it arrive together, in PR #1, or not at all.
```

**@vzakharov** — 2026-09-10T20:53:22Z

So what happens then? The new repo's `main` always reds until pr1 lands?

**@vzakharov** — 2026-09-10T20:59:52Z

Yes — and that's the bug in the sentence: it names the wrong symptom. Carried across, the source's `vet.sh` doesn't certify a stack that isn't there, it *fails* on it — `pnpm lint` with no `package.json`, `cargo clippy` with no `Cargo.toml`. So the new repo's `main` reds from the moment it is seeded and every PR against it opens red until something lands the stack. No false green anywhere; the rule is right, the reason given for it wasn't.

Which also makes it the *same* defect as the bullet just above rather than a different one — a `main` whose `/finalize` cannot pass for a reason the contract calls legitimate — just reached from the other side. Rewritten to say that.

930c660

---
_Generated by [Claude Code](https://claude.ai/code)_

---

## Timeline (status, references, and other events)

- **2026-09-10T11:43:06Z** @vzakharov renamed from «feat: #50 plan a skill for the template-fork path» to «feat: #50 give the template-fork path a detemplating skill».
- **2026-09-10T17:08:15Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/52#pullrequestreview-5169852179.
- **2026-09-10T20:54:20Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/52#pullrequestreview-5172134176.
