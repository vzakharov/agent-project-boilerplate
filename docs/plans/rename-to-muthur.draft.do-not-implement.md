> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Rename `agent-project-boilerplate` → `muthur`

## What this is

Three changes that ship together, because each is stale without the others:

1. **The GitHub rename**, relying on GitHub's permanent redirect. No pointer repo
   at the old name — the old path only stops redirecting if we ourselves occupy
   it, and nobody else can, since it lives under this account.
2. **Single-sourcing the repo's identity**, so the next rename is one JSON edit
   plus a check, rather than a grep across six files.
3. **A README that carries the name** — epigram, tagline, description — without
   explaining itself.

The name is decided. What is open is in § "Questions".

## Decisions already taken (do not re-litigate)

- **`muthur`**, lowercase, as `vzakharov/muthur`. The handle `github.com/muthur`
  and the bare repo name under other owners are taken; ours is free.
- **No tombstone repo.** The in-tree references mean any adopter who syncs reads
  the new name from the tree itself, and the redirect covers the machinery in the
  meantime.
- **The joke is never explained.** No "named after", no gloss, no footnote. The
  epigram is a bare quote with attribution; the tagline plays the angle without
  naming the source.

## Step 1 — Single-source the repo identity

Today the literal `vzakharov/agent-project-boilerplate` appears **16 times across
6 files**. They are three different kinds of thing, and only one is irreducible.

### 1a. The source of truth

`.claude/skills/sync-agent-infra/upstream.json`'s `repo` field. It already names
this repo, it is already the file an adopter re-targets, and it is already
machine-readable. Nothing new is created to hold the name.

Its semantics in this tree are worth stating plainly, since the field means "the
repo I took this from": in the boilerplate, which has no source above it, the
shipped stub names *itself*. That self-reference is exactly the predicate the
identity checks want — see 1b.

### 1b. The three identity checks become a comparison, not a literal

`/detemplate` and `/spinoff` partition on the same signal ("catalog present; is
`origin` the boilerplate?"), and `CLAUDE.md`'s opening stub carries the same test.
All three currently hardcode the name. Replace each with:

> `origin` equals the `repo` field in `.claude/skills/sync-agent-infra/upstream.json`

This is equivalent in every tree that matters, and self-maintaining:

| Tree | `origin` | `upstream.repo` | Equal? | Correct verdict |
| --- | --- | --- | --- | --- |
| This repo | `vzakharov/muthur` | `vzakharov/muthur` | yes | is the source |
| Undetemplated fork | the fork | `vzakharov/muthur` | no | is a fork |
| Adopter / spinoff | itself | its own parent | no | is a project |

Sites: `.claude/skills/detemplate/SKILL.md:46` and `:267`,
`.claude/skills/spinoff/SKILL.md:38`, `CLAUDE.md:7`.

**Also reword the substring warnings at those sites.** Both currently justify
"match the full `owner/repo`" with the example that an adopter may legitimately
be called `acme-boilerplate`. Under the new name that example is a polar bear —
it defends against a collision the name no longer has. Keep the rule (a full
`owner/repo` match is still the right test), drop the dead example, and state the
reason from the comparison itself rather than from a hazard that has left.

### 1c. The literals that stay, and the check that pins them

These are human copy-paste — clone lines, a filled-in watermark example, a `gh
api` recipe, an issue link — and cannot interpolate:

- `README.md`: the H1, the `--template` line (58), the adopt prompt (81)
- `ADOPTING.md`: 47, 316, 319, 346, 527
- `.claude/skills/detemplate/SKILL.md`: 129, 139
- `.claude/skills/sync-agent-infra/upstream.json`: 2 — the source of truth itself

Plus one that is irreducible by nature: **`/detemplate`'s frontmatter
`description`**, which names the repository so a session can check it against its
own working directory at no round-trip. Frontmatter is read by the client; it
cannot reference a file.

Add **`scripts/check-repo-identity.sh`**, modelled on `check-skill-catalog.sh`:

- Read the canonical `owner/repo` from `upstream.json`.
- Fail if that literal appears anywhere outside the allowlist above.
- Fail if any allowlisted site names a *different* `owner/repo` than the canonical
  one (catching a half-finished rename).
- Compare against `git remote get-url origin` too, but **warn without failing**.
  The window where the two legitimately disagree is not the moment of the rename
  — it opens at the first edit that writes `muthur` into the tree and closes at
  `gh repo rename`, i.e. it spans the whole implementation PR. A failing
  comparison would red the vet run for that entire stretch; a warning still
  catches the case that matters, which is a half-finished rename noticed later.

Wire it into `scripts/vet.sh` beside the other two non-stack checks, extend that
file's comment block to say what it protects, and add its catalog row (the
catalog carries one row per script; `check-skill-catalog.sh` asserts coverage).

## Step 2 — The README

### Title and epigram

```markdown
# muthur

> _"Big things have small beginnings."_
```

The quote stands alone under the H1, italic, attributed or bare (see the open
question), with no gloss and no link. Anyone who knows it, knows it — and anyone
who doesn't reads a plain aphorism about seeds, which is the same thing this
repo is.

### Tagline and description

The two things the opener has to carry are **the agent as a first-class
collaborator** and **infrastructure that keeps syncing after you've changed it**.
Replace the current two-line opener with:

```markdown
Agent-first infrastructure that survives being adapted.

Fork it into any project, change it to fit that project, and keep pulling
later improvements forward — the part a copied skill directory can't do.
Stack-agnostic.
```

"Survives being adapted" is the whole differentiator in four words: everyone
ships skills, nobody keeps them mergeable once you've made them yours. The
second sentence spells out the mechanism, because "another pile of agent skills"
is the wrong first read and the one the name alone invites.

The rest of the README is unchanged apart from the name substitutions in Step 1c
and the § "Getting it" heading text, which keeps working verbatim.

### GitHub repo metadata

Set the repository description to match the tagline (it is what renders in search
results, in the sidebar of every fork, and on the template-picker):

> Agent-first infrastructure that survives being adapted — a plan → go → land loop you fork into any project, change to fit, and keep syncing. Stack-agnostic.

Leave topics as they are unless they name the old slug.

## Step 3 — Teach `/sync-agent-infra` about a renamed source

An adopter's watermark will name `vzakharov/agent-project-boilerplate` until they
next sync, and their clone of it will succeed via the redirect while their
`upstream.json` stays wrong. Add a short step to
`.claude/skills/sync-agent-infra/SKILL.md`: when the clone of `repo` lands on a
repository whose canonical `owner/repo` differs from the watermark, update
`repo` (and any `lineage[].repo` naming the same source) as part of that sync,
and say so in the sync commit.

Write it as the **general** mechanism — a source repo that was renamed — not as a
note about this rename. The general form is durable and covers adopters of
adopters; a note about this specific rename is stale the day everyone has synced.

## Step 4 — The rename itself

```bash
gh repo rename muthur                    # from the repo, requires admin
git remote set-url origin https://github.com/vzakharov/muthur
```

**The order is:** land everything above on this PR → rename on GitHub → squash-merge.
A stale-but-working README on `main` for a few minutes beats a correct README
whose clone lines 404, which is what renaming after the merge would produce.

**Known risk between the rename and the merge:** this session's GitHub scope
names the old slug, so MCP GitHub tools may stop resolving the repo once it is
renamed. The API redirects, so it will likely be fine — but if the merge step
fails afterwards, finish it in the GitHub UI rather than fighting the tooling,
and say so in the report.

## DRY notes

- **The name now has one home** (`upstream.json`'s `repo`) plus an allowlist of
  copy-paste sites that a script pins. That is the whole point of the change; the
  alternative — a new dedicated identity file — was rejected because it adds a
  file to carry one string that an existing, already-authoritative file already
  carries.
- **The three identity checks collapse into one predicate** (`origin ==
  upstream.repo`) stated three times in prose, because they are three different
  skills' entry guards and each needs the sentence in its own flow. What is shared
  is the *value*, which is now genuinely shared; duplicating the one-line
  comparison is cheaper than a fourth file they all `@`-reference for one
  sentence. `/detemplate` and `/spinoff` already cross-reference each other for
  the rationale, and that stays.
- **`check-repo-identity.sh` is a new script, not a branch inside
  `check-skill-catalog.sh`.** The two assert unrelated invariants over different
  file sets, and the catalog checker is already multi-assertion; folding a third
  concern in would make its failure output ambiguous about which invariant broke.
- **No new abstraction over `gh repo rename`.** It runs once.

## Verification

1. `./scripts/vet.sh` passes, with the new check in it.
2. `grep -rI "agent-project-boilerplate" --exclude-dir=.git .` returns only
   allowlisted sites — and after Step 4, returns nothing but genuine history.
3. The new check fails as intended against a deliberate stray literal (test it in
   `tmp/`, not by committing one).
4. Post-rename: `gh repo view vzakharov/muthur` resolves; the old URL redirects
   for both web and `git clone`.
5. README renders with the epigram directly under the H1 and no gloss anywhere.

## Questions

Settled: the agent performs the rename between green CI and the squash-merge; the
identity check warns on a remote mismatch rather than failing; the tagline leads
on surviving adaptation rather than on a nod to the name. Rejected along the way:
an operator-run rename after the merge (leaves `main` pointing at a 404), a
failing remote comparison (reds the vet run for the whole implementation PR), and
a "standing orders" tagline (a nod where the differentiator should be).

One fork stays open. The plan is written with (b) in force, so silence ships it.

1. **Epigram.** All six verified verbatim against transcripts.
   - (a) David, *Prometheus* — _"Sometimes to create, one must first destroy."_
     Reads as `/detemplate`'s whole job.
   - (b) David, *Prometheus* — _"Big things have small beginnings."_ **In force.**
     It is about propagation from a seed, which is the repo's core act, and it is
     the only candidate that works as a plain aphorism for a reader who doesn't
     place it — which is what "never explain the joke" actually requires.
   - (c) Ash, *Alien* — _"I admire its purity. A survivor… unclouded by
     conscience, remorse, or delusions of morality."_ The best prose of the six;
     it admires a relentless process, which is either exactly right or slightly
     grim depending on the day.
   - (d) MU/TH/UR's screen, Special Order 937, *Alien* — _"Priority one — Ensure
     return of organism for analysis. All other considerations secondary. Crew
     expendable."_ The most on-the-nose for the name, and the only one whose
     punchline is that the humans are disposable — which fights "the agent is a
     first-class collaborator, not a replacement."
   - (e) Bishop, *Aliens* — _"That could never happen now with our behavioral
     inhibitors."_ A joke about guardrails; needs its setup line to land, so it
     is the weakest as a bare epigram.
   - (f) MOTHER, *Alien* — _"The option to override automatic detonation expires
     in T minus five minutes."_ Lands on gates that cannot be un-passed, which is
     what the approval tokens are; longest of the six.

   Sub-question: **attribute it or not.** Bare is colder and truer to "don't
   explain"; a `— David, Prometheus (2012)` line under it makes the epigram
   legible as a quotation to a reader who'd otherwise think we wrote it. In force:
   **bare**.
