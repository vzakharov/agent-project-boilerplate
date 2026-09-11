# PR #65: feat: rename the repo to muthur and single-source its identity

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/65
- **Author:** @vzakharov (agent)
- **Base ← Head:** main ← claude/rename-to-muthur-eh1xxl
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-11T10:30:42Z
- **Updated:** 2026-09-11T11:55:27Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The repo's name now lives in one place.** `upstream.json`'s `repo` field is the source of truth — it already named this repo, it is already what an adopter re-targets, and in a tree with no source above it the shipped stub names itself. The three guards that asked "am I the boilerplate?" (`/detemplate`'s Step 0 and its undetemplated-fork signal, `/spinoff`'s refusal, `CLAUDE.md`'s opening stub) compare `origin` against that field instead of carrying the name.
- **`scripts/check-repo-identity.sh` pins what cannot interpolate** — clone lines, a `gh api` recipe, a filled-in watermark example, and `/detemplate`'s frontmatter description, which the client reads before any file can be resolved. It also catches a stale name under the same owner, and *warns* rather than fails when `origin` has yet to catch up, since the vet run is what gates the rename. Wired into `vet.sh`; keyed on the catalog, so it exits 0 downstream.
- **`/sync-agent-infra` learns the general renamed-source case.** GitHub's redirect is permanent, so a watermark naming a renamed source keeps cloning and keeps being wrong — the one failure mode with no symptom. Step 2 reads the canonical name off the redirect warning git prints on stderr; Step 7 moves `repo` and any matching `lineage` entry in the commit that bumps the watermark.
- **The README takes the name**, an epigram, and a tagline that leads on surviving adaptation rather than on shipping skills.

**Step 4 of the plan is not in this diff.** `gh repo rename muthur` runs at `/finalize`, between green CI and the squash-merge: a stale-but-working README on `main` for a few minutes beats a correct README whose clone lines 404. The GitHub repo description goes over in the same breath.

## QA Checklist

- [ ] `vet` — `./scripts/vet.sh` passes, with `check-repo-identity` reporting OK among the checks.
- [ ] `stray-literal` — drop `vzakharov/muthur` into a tracked file outside the allowlist and re-run the check: assertion 1 fails and names the file and line.
- [ ] `stale-name` — same, with `vzakharov/agent-project-boilerplate`: assertion 2 fails, reading as an unfinished rename.
- [ ] `remote-warns` — assertion 3 prints the ⚠ line while `origin` still says the old name, and the script still exits 0.
- [ ] `downstream-skip` — with `.claude/skills/sync-agent-infra/catalog.md` moved aside, the whole check reports "skipped" and exits 0.
- [ ] `guards-read` — `/detemplate` Step 0, its "Recognizing an undetemplated fork" section, `/spinoff`'s two invariants and `CLAUDE.md`'s stub each read as a comparison against the watermark, with no repo name of their own.
- [ ] `readme` — the README renders with the epigram directly under the H1, attributed to the film, and explains the name nowhere.
- [ ] `rename` — after `/finalize` fires the rename: `gh repo view vzakharov/muthur` resolves, and the old URL redirects for both web and `git clone`.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `vet` | integration | ✅ | `scripts/vet.sh` is the run. |
| `stray-literal` | integration | ❌ | No harness exercises the check scripts; would need a fixture tree and an expected exit code. |
| `stale-name` | integration | ❌ | Same fixture as above, second assertion. |
| `remote-warns` | integration | ❌ | Needs a repo whose `origin` disagrees with the watermark — the state this branch is in. |
| `downstream-skip` | integration | ❌ | Same fixture harness, catalog absent. |
| `guards-read` | manual-only | — | Prose review: whether each guard reads correctly without the literal. |
| `readme` | manual-only | — | Rendered output and editorial judgement. |
| `rename` | manual-only | — | A one-shot GitHub-side operation. |

https://claude.ai/code/session_01YRUbVX1avAzUWnNmz6nApt

---

## Comments

### Comment by @vzakharov (agent) on 2026-09-11T10:31:14Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/65#issuecomment-5633124003](https://github.com/vzakharov/agent-project-boilerplate/pull/65#issuecomment-5633124003)

Proposed squash title/body:

```
feat: rename the repo to muthur and single-source its identity (pr #65)
```

```
"Boilerplate" described the wrong thing. What adopters take from here is
a maintained upstream they keep resyncing from, not a one-shot starter,
and a name promising starter files undersold the part that has no
equivalent elsewhere: fork it, adapt it locally, and still pull later
improvements forward. The README leads on that now rather than on the
skills it ships.

The repo's own name now lives in one place. `upstream.json`'s `repo`
field is the source of truth, and the three guards that asked whether a
tree is the source — `/detemplate`'s Step 0, `/spinoff`'s refusal, and
CLAUDE.md's opening stub — compare `origin` against it instead of
carrying the name themselves. What cannot interpolate, being clone lines
and `gh api` recipes a human copies, is held to an allowlist by
`scripts/check-repo-identity.sh`, which the vet run calls. A future
rename is that one JSON field plus whatever the check flags.

`/sync-agent-infra` gains the general case of a source repo that was
renamed: a clone that lands somewhere with a different canonical name
updates the watermark as part of that sync, so every adopter re-targets
on their next run without being told. The rename itself leans on
GitHub's permanent redirect rather than a pointer repo at the old name —
that path only stops redirecting if this account occupies it, and no one
else can.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Review threads

### `.claude/skills/detemplate/SKILL.md`:47 — unresolved

```diff
@@ -43,13 +43,14 @@ the trees most likely to carry one.
 - **No catalog** → not an unpruned fork. An adopted repo that wants a
   sibling wants `@.claude/skills/spinoff/SKILL.md`; a repo that already ran this
   has nothing left to strip.
-- **Catalog present, but `origin` is `vzakharov/agent-project-boilerplate`** →
-  this *is* the boilerplate, and what the caller wants is a fork, not a prune.
-  Point at the README's *"Use this template"* button. Match the full
-  `owner/repo`, never the substring `boilerplate`: an adopter is free to call
-  itself `acme-boilerplate`, and a substring test prunes the wrong tree. Without
-  the origin clause, catalog-presence alone would let a session delete this
-  repo's own inventory.
+- **Catalog present, but `origin` matches the `repo` field in
+  `.claude/skills/sync-agent-infra/upstream.json`** → this *is* the boilerplate
```

**@vzakharov (human)** — 2026-09-11T11:51:00Z

how often do we keep mentioning "boilerplate" across the codebase? does the term legitimately survive or is it a leftover? if surviving, is "boilerplate" or "template" a better term?

---

### `.claude/skills/sync-agent-infra/SKILL.md`:1 — unresolved

**@vzakharov (human)** — 2026-09-11T11:51:48Z

`/sync-muthur`, advised for adopters to adopt during next sync (by default)

---

### `.claude/skills/sync-agent-infra/SKILL.md`:189 — unresolved

```diff
@@ -182,6 +182,22 @@ matters, and wrong here.)
 **Bash `cwd` resets between calls in this harness** — chain `cd <clone> && …` in
 every command that needs to be inside it.
 
+**A source that was renamed still clones, and the watermark still names the old
+path.** GitHub redirects the old `owner/repo` permanently, so the clone succeeds
+and nothing here fails — which is precisely why the stale name would survive
+every future sync unnoticed. Read the source's canonical name once the clone is
+down, and carry it to Step 7 if it differs:
```

**@vzakharov (human)** — 2026-09-11T11:52:33Z

that's not what I meant. I meant that if, during the sync, an adopter realizes the boilerplate itself is referred to as muthur instead of what it had (agent-project-boilerplate), it will already let them know that a rename happened.

and I don't think there should be any special "procedure" for a rename, it's not like we're going to do this every second day.

what helps I think is a note in the squash message for adopters (because they're reading them usually)

or am I misunderstanding what we are trying to achieve here?

---

### `README.md`:3 — unresolved

```diff
@@ -1,6 +1,13 @@
-# agent-project-boilerplate
+# muthur
 
-Boilerplate for projects where Claude Code is a first-class collaborator.
+> _"The option to ignore agentic development expires in T minus five minutes."_
```

**@vzakharov (human)** — 2026-09-11T11:54:36Z

let's seo a bit what term is the more adopted: agentic development, agentic coding, coding with agents, etc. etc.

---

### `README.md`:19 — unresolved

**@vzakharov (human)** — 2026-09-11T11:55:13Z

I feel like a second paragraph detailing the "keep pulling later improvements forward" claim is worthy here

---

## Timeline (status, references, and other events)

- **2026-09-11T11:30:03Z** @vzakharov renamed from «docs: plan the rename to muthur» to «feat: rename the repo to muthur and single-source its identity».
- **2026-09-11T11:55:26Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/65#pullrequestreview-5178310762.
