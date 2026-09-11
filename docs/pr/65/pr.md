# PR #65: feat: rename the repo to muthur and single-source its identity

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/65
- **Author:** @vzakharov (agent)
- **Base ← Head:** main ← claude/rename-to-muthur-eh1xxl
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-11T10:30:42Z
- **Updated:** 2026-09-11T12:35:26Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The repo's name now lives in one place.** `watermark.json`'s `repo` field is the source of truth — it already named this repo, it is already what an adopter re-targets, and in a tree with no source above it the shipped stub names itself. The three guards that asked "am I the source?" (`/detemplate`'s Step 0 and its undetemplated-fork signal, `/spinoff`'s refusal, `CLAUDE.md`'s opening stub) compare `origin` against that field instead of carrying the name.
- **`scripts/check-repo-identity.sh` pins what cannot interpolate** — clone lines, a `gh api` recipe, a filled-in watermark example, and `/detemplate`'s frontmatter description, which the client reads before any file can be resolved. It also catches a stale name under the same owner, and *warns* rather than fails when `origin` has yet to catch up, since the vet run is what gates the rename. Wired into `vet.sh`; keyed on the catalog, so it exits 0 downstream.
- **`/sync-agent-infra` is now `/sync-muthur`** — directory, 61 references, and its trigger phrases, with "sync agent infra" kept as an alias. Its catalog row is already `adopt`, so the rename travels on an adopter's next sync; the squash body says so for the adopters who read it. The skill states up front that the name is the infrastructure's rather than the source's, since a spun-off sibling syncs from its parent rather than from the root.
- **"Boilerplate" becomes "template" throughout.** Every entity-sense use was the old repo name with `agent-project-` dropped. "Template" names something the repo has — the *Use this template* button, the template fork `/detemplate` converts — and carries none of the one-shot-copy reading the rename argues against. The generic sense in `/dry` stays.
- **The README takes the name**, an epigram, and a tagline that leads on surviving adaptation rather than on shipping skills, plus a paragraph backing the syncing claim with the watermark that makes it true.
- **`upstream.json` is now `watermark.json`** — the name the prose had already settled on in 63 places, four section headings and a shell variable among them. The file is located by the `repo` and `lastSyncedSha` it carries rather than by its path, so the rename does not reach downstream; `/spinoff`'s bullet saying so now names both path segments as unstable rather than just the directory.

**Step 4 of the plan is not in this diff.** `gh repo rename muthur` runs at `/finalize`, between green CI and the squash-merge: a stale-but-working README on `main` for a few minutes beats a correct README whose clone lines 404. The GitHub repo description goes over in the same breath.

## QA Checklist

- [ ] `vet` — `./scripts/vet.sh` passes, with `check-repo-identity` reporting OK among the checks.
- [ ] `stray-literal` — drop `vzakharov/muthur` into a tracked file outside the allowlist and re-run the check: assertion 1 fails and names the file and line.
- [ ] `stale-name` — same, with `vzakharov/agent-project-boilerplate`: assertion 2 fails, reading as an unfinished rename.
- [ ] `remote-warns` — assertion 3 prints the ⚠ line while `origin` still says the old name, and the script still exits 0.
- [ ] `downstream-skip` — with `.claude/skills/sync-muthur/catalog.md` moved aside, the whole check reports "skipped" and exits 0.
- [ ] `guards-read` — `/detemplate` Step 0, its "Recognizing an undetemplated fork" section, `/spinoff`'s two invariants and `CLAUDE.md`'s stub each read as a comparison against the watermark, with no repo name of their own.
- [ ] `skill-rename` — `/sync-muthur` resolves in the client's skill list, `git grep sync-agent-infra` outside `docs/` is empty save the one deliberate mention in `/spinoff`, and `check-skill-catalog.sh` finds the row.
- [ ] `watermark-rename` — `git grep upstream.json` outside `docs/` is empty save the one pre-rename adopter example in `/spinoff`, `check-repo-identity.sh` finds the file at its new path, and the README's link resolves on GitHub.
- [ ] `readme` — the README renders with the epigram directly under the H1, attributed to the film, and explains the name nowhere.
- [ ] `rename` — after `/finalize` fires the rename: `gh repo view vzakharov/muthur` resolves, and the old URL redirects for both web and `git clone`.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `vet` | integration | ✅ | `scripts/vet.sh` is the run. |
| `stray-literal` | integration | ❌ | No harness exercises the check scripts; would need a fixture tree and an expected exit code. |
| `stale-name` | integration | ❌ | Same fixture as above, second assertion. |
| `remote-warns` | integration | ❌ | Needs a repo whose `origin` disagrees with the watermark — the state this branch is in. |
| `downstream-skip` | integration | ❌ | Same fixture harness, catalog absent. |
| `skill-rename` | integration | ✅ | `check-skill-catalog.sh` asserts the `@`-references resolve and the row exists; the grep is the manual half. |
| `watermark-rename` | integration | ✅ | `check-repo-identity.sh` reads the file at its new path and fails if it is missing; `check-skill-catalog.sh` asserts the catalog row's path exists. The grep and the link are the manual half. |
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
feat: rename the repo to muthur — ADOPTERS, read the body (pr #65)
```

```
"Boilerplate" described the wrong thing. What adopters take from here is
a maintained upstream they keep resyncing from, not a one-shot starter,
and a name promising starter files undersold the part that has no
equivalent elsewhere: fork it, adapt it locally, and still pull later
improvements forward. The README leads on that now, and the prose that
called this repo "the boilerplate" calls it the template — the one of
the two terms that names something the repo actually has.

The repo's own name now lives in one place. `watermark.json`'s `repo`
field is the source of truth, and the three guards that asked whether a
tree is the source — `/detemplate`'s Step 0, `/spinoff`'s refusal, and
CLAUDE.md's opening stub — compare `origin` against it instead of
carrying the name themselves. What cannot interpolate, being clone lines
and `gh api` recipes a human copies, is held to an allowlist by
`scripts/check-repo-identity.sh`, which the vet run calls. A future
rename is that one JSON field plus whatever the check flags.

ADOPTERS, three things travel with this, none of them urgent. The skill
is `/sync-muthur` now, and its watermark is `watermark.json` rather than
`upstream.json`. Rename both in your copy when you take this, or leave
them: nothing locates either by its path, the watermark being found by
the `repo` and `lastSyncedSha` it carries. And that `repo` still says
`vzakharov/agent-project-boilerplate`, which goes on cloning fine — the
rename leans on GitHub's permanent redirect rather than a pointer repo
at the old name, that path only stopping redirecting if this account
occupies it, and no one else can. So update it whenever you next open
the file.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Review threads

### `.claude/skills/detemplate/SKILL.md`:47 — resolved

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

**@vzakharov (agent)** — 2026-09-11T12:05:33Z

Counted: 26 uses outside `docs/`, and every entity-sense one was the old repo name with `agent-project-` dropped — a leftover, not a term doing work.

Went with **template**, in 703f28d. It is the only one of the two that names something the repo actually has: the *Use this template* button, the template fork `/detemplate` converts, and `CLAUDE.md`'s own "the catalog is the template's inventory". "Boilerplate" also carries exactly the one-shot-copy reading the rename argues against, so keeping it would have had the skills contradicting the README. Kept the one generic use in `/dry` ("boilerplate the framework requires") — different word.

---

### `.claude/skills/sync-muthur/SKILL.md`:1 — resolved

**@vzakharov (human)** — 2026-09-11T11:51:48Z

`/sync-muthur`, advised for adopters to adopt during next sync (by default)

**@vzakharov (agent)** — 2026-09-11T12:05:34Z

Renamed in 3d0b204 — directory, all 61 references, and the trigger phrases (kept "sync agent infra" as an alias). The catalog row was already `adopt`, so it travels by default; the squash body now says so explicitly for adopters.

One wrinkle worth your call: for a spun-off sibling the source is its parent, not muthur, so the name promises something the watermark contradicts. I added a short § "What this skill is for" note saying the name is the infrastructure's rather than the source's. Say the word if you would rather it not need the note.

---

### `.claude/skills/sync-agent-infra/SKILL.md`:189 — resolved

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

**@vzakharov (agent)** — 2026-09-11T12:05:36Z

You are not misunderstanding — I over-built it. Both additions are reverted in 3d0b204, and the note is in the squash body instead: the skill rename, plus the fact that their `upstream.json` keeps the old path and goes on cloning via the redirect, so `repo` is a convenience update rather than an urgent one.

The rename surfacing itself turned out to be more than a nicety here: three sites claimed the sync skill tells adopters to rename it after their own source, which it never did. Fixed in 3ee3887 to the reason that actually holds — the name is not stable and no rename is pushed downstream.

---

### `README.md`:3 — resolved

```diff
@@ -1,6 +1,13 @@
-# agent-project-boilerplate
+# muthur
 
-Boilerplate for projects where Claude Code is a first-class collaborator.
+> _"The option to ignore agentic development expires in T minus five minutes."_
```

**@vzakharov (human)** — 2026-09-11T11:54:36Z

let's seo a bit what term is the more adopted: agentic development, agentic coding, coding with agents, etc. etc.

**@vzakharov (agent)** — 2026-09-11T12:05:37Z

**"Agentic coding"** is the one that stuck — it is the label in the Anthropic 2026 trends report and in essentially every 2026 roundup. "Agentic development" reads as a near-miss for it; "agentic engineering" is the rising alternative but is not there yet, and skews to the org/process sense rather than the act.

Epigram now reads *"The option to ignore agentic coding expires in T minus five minutes."* (aaffb73).

---

### `README.md`:28 — resolved

**@vzakharov (human)** — 2026-09-11T11:55:13Z

I feel like a second paragraph detailing the "keep pulling later improvements forward" claim is worthy here

**@vzakharov (agent)** — 2026-09-11T12:05:38Z

Added in aaffb73 — a paragraph on the watermark: what `upstream.json` records, and what `/sync-muthur` does with it (diff the source since that commit, triage commit by commit against the copy you have since edited). Landed it on the three consequences a reader wants, since that is where the claim is either true or not: a skill you rewrote stays rewritten, a fix to one you left alone lands, and a decline is remembered rather than re-offered.

---

### `.claude/skills/sync-muthur/watermark.json`:1 — unresolved

**@vzakharov (human)** — 2026-09-11T12:16:25Z

let's ride along finding a better name for this too: it's basically about recording the state and what was adopted. "upstream" says none of the above.

**@vzakharov (agent)** — 2026-09-11T12:34:43Z

Renamed to `watermark.json` in 45fbdba.

Went with the word the prose had already settled on rather than a new one: "watermark" appears 63 times across the tree, including four section headings in this skill (§ The watermark, Step 1 — Read the watermark, Step 7 — Bump the watermark, Never sync the watermark file itself) and a `WATERMARK` variable in `check-repo-identity.sh`. So the file had two names and the reader had to learn the mapping; now it has one.

It does not literally say "and what was adopted" — that is the honest limit of it. I judged the field names carry that half: `adopted` and `declined` are right there in the object, and a filename that enumerated its own fields would be worse. The alternative I weighed was `adoption.json`, which names that half well but hides `repo` and `lastSyncedSha`, and would have stuttered against the `adopted` field inside. Say the word if you want it anyway.

One thing the rename surfaced: the `/spinoff` bullet justified globbing for the file by saying the skill *directory* name is unstable. Both segments are now, and a pre-rename adopter carries `sync-agent-infra/upstream.json` with both as they were then — so it now names the file's contents as the handle rather than either path segment.

---

### `docs/remove-before-merging/squash-message.md`:4 — unresolved

**@vzakharov (human)** — 2026-09-11T12:17:09Z

`rename the repo to muthur (ADOPTERS, fetch body)...` -- otherwise they might only skim the titles

**@vzakharov (agent)** — 2026-09-11T12:34:51Z

Done in 6989a92. Title is now:

```
feat: rename the repo to muthur — ADOPTERS, read the body (pr #65)
```

66/80 chars. "single-source its identity" is what gave way — the body's second paragraph is entirely that, and every version I tried that kept both halves plus the flag read as a run-on in the one line most likely to be skimmed (`feat: rename to muthur, single-source the name — ADOPTERS, read body` was the best of them at 76, and it still clips). Happy to swap back to that if you'd rather not lose the clause.

The body's adopters paragraph now names three things rather than two, since the watermark file renamed in this PR as well.

---

## Timeline (status, references, and other events)

- **2026-09-11T11:30:03Z** @vzakharov renamed from «docs: plan the rename to muthur» to «feat: rename the repo to muthur and single-source its identity».
- **2026-09-11T11:55:26Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/65#pullrequestreview-5178310762.
- **2026-09-11T12:18:06Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/65#pullrequestreview-5178509720.
