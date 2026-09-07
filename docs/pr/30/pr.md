# PR #30: docs: sync agent infrastructure forward from the source repo

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/30
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/sync-upstream-pw07cy
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-07T11:07:19Z
- **Updated:** 2026-09-07T19:23:01Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **Ported `/handle`** — one front-end over the branch-continuation invocations an operator previously assembled by hand: attach, read off whether the branch carries an unimplemented plan or unanswered review feedback, run that lane, and land-prep only when `and finalize` appears anywhere in the argument. It owns only the fork — attaching defers to `/from-branch`, both lanes land in `/implement`, land-prep defers to `/finalize`.
- **The plan-file lifecycle gains `*.paused.md`.** `*.in-progress.md` was doing two incompatible jobs — marking a plan a session holds right now, and marking one a later session should resume — so two agents could land on the same plan and branch, each overwriting the other's commits. It is now a claim and nothing else; a session told to stop partway records what is done and what is left and releases the plan as `*.paused.md`. `/implement` Step 1 also stopped to ask on any `docs/plans/*.md` count but one, so a plan carried across sessions blocked on an unambiguous branch; only actionable suffixes count now.
- **`/tighten-docs` gains a third lens** ahead of the two it had — whether the prose should exist at all — with the ordered homes (call-site comment, docstring, rule, colocated README, runbook), the rule-vs-README test, and a single-lens mode so one defect can be chased alone. CLAUDE.md's doc-sync bullets become a short § "Writing things down" that states the threshold and names the skill as the long version, since a rule loads in full every time its glob matches.
- **The PR export now carries each review thread's resolved state** (`— resolved` / `— unresolved` / `— resolution unknown` in the thread header). It is the one fact no REST comment payload holds, so it comes from a GraphQL `reviewThreads` read keyed by every comment id in the thread — `/handle`'s review lane needs it, and "not resolved" and "not known" are different inputs to that selection.
- **Two more CLAUDE.md rules and a `/preview` concern ride along**: file reads and edits stay on `Read`/`Edit`/`Write` in every permission mode (auto mode drops the per-edit prompt, and `cat`/`sed`/heredoc drift costs the web UI's session log its skimmable diffs), and a hydrated `/preview` has to shoot every colour scheme the app serves rather than inherit the VM's OS preference.
- **Watermark advanced** `dd0632d` → `2e6902f3`, with `.github/` recorded as declined and the two TypeScript exporter modules recorded as ported-by-hand, so neither comes back as an open question.

### Triage — every candidate in `dd0632d..2e6902f3` touching an adopted path

| Commit | Verdict | Reasoning |
|---|---|---|
| `2e6902f30` add `/handle` | **take + translate** | `/handle`, the `*.paused.md` lifecycle and the `Read`/`Edit`/`Write` rule apply as-is. Its `scripts/gh-export/` half is translated by hand into the Python exporter. Its "never resolve a thread" rule was already ported (#26). |
| `e6be119ca` retire the decision docs | **translate (partial)** | The existence lens, the ordered homes, the rule-vs-README test and the short CLAUDE.md section port. The `docs/decisions/` retirement itself, the eleven new stack-specific rules and the deletion of an `update-docs` skill this repo never had do not. |
| `779746ec3` tokenise dark-only hairlines | **translate (small)** | Stack-bound in substance, but the trap generalises: an app that picks its scheme from an explicit attribute serves one default whatever the machine prefers, so `/preview` names the concern. |
| `691d3d5b9` optional-with-guard integration credentials | **skip (stack-bound)** | Only `scripts/env-preflight/` and the source's env registry. |
| `79c8dcb06` confirm CRM signup delivery | **skip (stack-bound)** | A Loops setup script and a CRM diagnostics report. |
| `145f87f09` alert on swallowed metering failures | **skip (stack-bound)** | The source's `scripts/ci/` nightly-alert plumbing, tied to its own workflows. |
| `ee5084e9a` keep the deep-research turn | **skip (stack-bound)** | The adopted-path half is a Railway per-environment log-reachability note in a stub this repo ships unhydrated. |

The unfiltered log was also skimmed for agent infrastructure landing somewhere `adopted` does not name; the only such path was `.github/workflows/`, now recorded in `declined`.

## QA Checklist

- [ ] `export-resolved` — `python3 scripts/export-github-item.py 25` from a scratch directory; every review-thread header in `docs/pr/25/pr.md` ends in `— resolved`, matching what the PR page shows.
- [ ] `export-unresolved` — same against a PR carrying an open thread; that thread's header reads `— unresolved` while resolved siblings still read `— resolved`.
- [ ] `export-issue` — run it against an issue number; the export is unchanged and no review section (or GraphQL call) appears.
- [ ] `label-fallback` — with a thread absent from the resolution map, the header reads `— resolution unknown` rather than defaulting to open.
- [ ] `catalog` — `bash scripts/check-skill-catalog.sh` reports OK: `/handle` has exactly one catalog row and no `@`-reference dangles.
- [ ] `handle-lanes` — `/handle` on a branch holding a draft plan runs the plan lane; on a PR with an unanswered thread, the review lane; with both present, it stops and asks instead of guessing an order.
- [ ] `paused-plan` — a session told to stop partway leaves `docs/plans/<slug>.paused.md`, and a later `/implement` continues from it instead of asking which plan to run; an `*.in-progress.md` still stops and asks.
- [ ] `watermark` — re-running `/sync-upstream` against this watermark surfaces zero candidates.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `export-resolved` | integration | ❌ | Mock the REST + GraphQL boundary, assert the header suffix per thread. This repo ships no test runner by design — `scripts/vet.sh` is the stub each adopting project rewrites — so every automatable row here is uncovered on purpose. |
| `export-unresolved` | integration | ❌ | Same fixture with `isResolved: false`. |
| `export-issue` | integration | ❌ | Issue payload → no `## Review threads` section and no GraphQL request. |
| `label-fallback` | unit | ❌ | `resolution_label` over an empty map → `resolution unknown`; over a non-root id → that thread's verdict. |
| `catalog` | unit | ❌ | The script *is* the check; a test would assert its exit code on a seeded dangling reference. |
| `handle-lanes` | manual-only | — | Agent-behavior branch on a live branch and PR; no assertion short of a human reading the transcript. |
| `paused-plan` | manual-only | — | Same: the lifecycle is enforced by prose an agent follows, not by code. |
| `watermark` | manual-only | — | Needs a clone of the source repo and a real triage pass. |

https://claude.ai/code/session_01NXJmidsm8VyZg5HGNL89qr

---

## Comments

### Comment by @vzakharov on 2026-09-07T11:08:43Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/30#issuecomment-5569711503](https://github.com/vzakharov/agent-project-boilerplate/pull/30#issuecomment-5569711503)

Proposed squash title/body:

```
feat: add /handle, pause-able plans and resolved-thread export (pr #30)
```

```
The agent infrastructure here is vendored from the repo it was
extracted from, and /sync-upstream is what keeps that link live
rather than a snapshot. Of the seven commits touching an adopted
path since the last watermark, four were the source's own stack —
env preflight, a CRM diagnostic, its nightly-alert plumbing, its
Railway log scoping — and three carried something portable.

/handle is a front-end over continuing an existing branch: it
attaches, reads off whether the branch holds an unimplemented plan
or unanswered review feedback, and runs that lane, with land-prep
opt-in via `and finalize` anywhere in the argument. It owns only
the fork — /from-branch attaches, both lanes land in /implement,
/finalize land-preps. The plan lifecycle gains `*.paused.md` to
make the plan lane readable: `*.in-progress.md` meant both "a
session holds this now" and "resume here", so two sessions could
claim one plan and overwrite each other's commits. It is a claim
only, released as `*.paused.md` by a session told to stop partway,
and /implement counts only actionable suffixes instead of stopping
to ask on every sibling.

/tighten-docs gains a lens ahead of its two — whether the prose
should exist at all — carrying the ordered homes and the
rule-vs-README test, plus a single-lens mode; CLAUDE.md keeps only
the threshold and names the skill as the long version, since a rule
loads in full every time its glob matches. The PR export now labels
each review thread resolved, unresolved or resolution-unknown, read
from GraphQL because no REST comment payload carries it and keyed
by every comment id in the thread, which /handle's review lane
selects on. Two conventions ride along: reads and edits stay on
Read/Edit/Write in every permission mode, and a hydrated /preview
shoots every colour scheme the app serves rather than inheriting
the machine's.

The watermark advances to source HEAD rather than the last commit
taken, so the four skipped commits stay skipped; `.github/` is
recorded as declined and the two TypeScript exporter modules as
ported-by-hand, so neither comes back as an open question.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01NXJmidsm8VyZg5HGNL89qr
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `docs/remove-before-merging/squash-message.md`:14 — unresolved

```diff
@@ -0,0 +1,52 @@
+Proposed squash title/body:
+
+```
+feat: add /handle, pause-able plans and resolved-thread export (pr #30)
+```
+
+```
+The agent infrastructure here is vendored from the repo it was
+extracted from, and /sync-upstream is what keeps that link live
+rather than a snapshot. Of the seven commits touching an adopted
+path since the last watermark, four were the source's own stack —
+env preflight, a CRM diagnostic, its nightly-alert plumbing, its
+Railway log scoping — and three carried something portable.
+
```

**@vzakharov** — 2026-09-07T19:12:08Z

doesn't pass the existence check :)

**@vzakharov** — 2026-09-07T19:23:01Z

Reading this as: the tracked working file shouldn't exist at all. Its content is a verbatim copy of the `Proposed squash title/body:` comment — the thing you actually paste at merge — and a file created only to be `git rm`'d before it can reach the trunk is squarely the "written somewhere nothing reaches" case. The one benefit claimed for it (a live doc a later session edits rather than recomposing) the comment already provides, and Step 4 knows how to find that comment.

Holding off because the fix is wider than deleting the file, and it reverses the `/tighten-docs` Step 4 exemption you wrote on main ("a commit body, and transient by nature"). Removing the mechanism means: `/squash-message` Step 2 loses the "which file: presence decides" block (`tmp/` becomes the only working surface, seeded from the existing comment when there is one), Step 4 loses the "tracked file is proof the proposal exists" exception, Step 5's three-way cleanup collapses to one; `/finalize` steps 3 and 6 lose the deferred-sweep rationale, though the tree itself stays for `/preview` screenshots and `/readonly-probe` output; `/tighten-docs` drops the exemption row; `docs/catalog.md`'s row is reworded.

Confirm and I'll do that. If you meant only "don't commit this file on this branch", say so and I'll just drop it.

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `scripts/export-github-item.py`:1 — unresolved

**@vzakharov** — 2026-09-07T19:12:51Z

no, let's split. not necessary the same way as the source (although I'm guessing this would make further mapping easier), but in _some_ way to make every module digestible.

**@vzakharov** — 2026-09-07T19:22:39Z

Split in 092cc1c. Six modules under `scripts/gh_export/`, boundaries drawn on this port's own seams rather than the source's: `cli` (argument parsing), `api` (REST + GraphQL over `lib.github.fetch`, plus the thread-resolution query), `attachments` (discovery, download, link rewriting), `markdown` (the header and comment sections every export carries), `reviews` (the PR-only threads), `timeline`. Largest is 147 lines; the entrypoint keeps its path — six skills and `docs/catalog.md` name it — and is now orchestration only.

Verified no behavior change: the export of PR #30, PR #26 and issue #27 is byte-identical before and after, run from the repo root and from an unrelated working directory. The `scripts/gh-export/` watermark note now records that our boundaries differ, so a future port doesn't expect a same-named file.

---
_Generated by [Claude Code](https://claude.ai/code)_


---

## Timeline (status, references, and other events)

- **2026-09-07T19:13:13Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/30#pullrequestreview-5134762863.
