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
  Under Step 4's ordering the vet run inside `/finalize` is what gates the
  rename, and the remote cannot agree with the tree until that rename has
  happened — so a failing comparison deadlocks the one run that unlocks it. A
  warning still catches what matters, a half-finished rename noticed later.

Wire it into `scripts/vet.sh` beside the other two non-stack checks, extend that
file's comment block to say what it protects, and add its catalog row (the
catalog carries one row per script; `check-skill-catalog.sh` asserts coverage).

## Step 2 — The README

### Title and epigram

```markdown
# muthur

> _"The option to ignore agentic development expires in T minus five minutes."_
>
> — Alien (well, almost)
```

The line is the ship's computer's countdown, bent one clause so it points at the
reader instead of at a self-destruct. No gloss, no link, and no note explaining
what was changed — the attribution's own parenthesis is the whole disclosure.

**Attribute to the film, never to the character.** Naming the speaker would be
the one place the README explains where the repo's name came from, which is the
thing this whole treatment exists not to do. Attributing an adapted line to the
work is also the ordinary convention for one — `— after Alien`, `— with
apologies to Alien`, and this parenthetical form are all standard, and the
parenthetical is the one that sounds like the rest of the README.

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

Settled: the epigram is the countdown line, bent to point at the reader and
attributed to the film with `(well, almost)`; the agent performs the rename
between green CI and the squash-merge; the identity check warns on a remote
mismatch rather than failing; the tagline leads on surviving adaptation. Rejected
along the way: five other quotes, all unbent and all attributable only to a
speaker (which would half-explain the repo's name); an operator-run rename after
the merge (leaves `main` pointing at a 404); a failing remote comparison
(deadlocks the finalize run that gates the rename); and a "standing orders"
tagline (a nod where the differentiator should be).

One wording call stays open, and the plan is written with (a) in force, so
silence ships it.

1. **The bent clause.** The distinctive half — *"expires in T minus five
   minutes"* — is preserved exactly in all three; only the object moves.
   - (a) *"The option to ignore agentic development…"* **In force.** Plainest
     reading, and "ignore" is the natural verb for a trend where the original's
     "override" wants a procedure.
   - (b) *"The option to keep writing it yourself…"* Funnier and concrete, and it
     names what the reader would actually be giving up rather than a category.
   - (c) *"The option to override agentic development…"* One word from the
     original, so the bend is unmistakable — at the cost of a verb that doesn't
     quite fit its new object.

   **The durability question under all three:** *agentic* is a word of this
   moment, and a README that leads with it may read in two years the way
   `late-stage-agentic` already does. (b) is the variant with no shelf life,
   which is the argument for it over (a).
