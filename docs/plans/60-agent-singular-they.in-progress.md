# #60 — refer to the agent as singular they, not it

Issue: https://github.com/vzakharov/agent-project-boilerplate/issues/60 · export: `docs/issue/60/issue.md`

Sweep the loop's prose for agent-as-"it" and repoint each hit to singular **they**
(or to second person where that reads better), leaving every non-agent "it"
alone. No standing rule is added — the issue rules that out explicitly.

## The boundary — decided once, applied per site

The grep is cheap; the judgement is the work. Three rules settle every site below.

1. **Only the actor is "they".** The agent, an agent, a prior agent, a parallel
   session's agent, a fanned-out subagent or analyst — all take **they**.
2. **Everything else in the loop's vocabulary stays "it".** A session, a run, a
   skill, a script, a check, the harness, the backend, a thread, a branch, a
   plan file, an export, the proxy, and **Claude Code the product** are not
   actors: they keep "it". The convention is about who acts, not about every
   noun nearby.
3. **Second person wins where "they" reads awkwardly.** The skills already
   address the agent as "you"; a rewrite to "you" is the fix, not a dodge. None
   of the seven in-scope sites below needs it — each takes "they"/"their"
   cleanly — so no site is rewritten into second person on this pass.

Three structural cues that keep the sweep honest:

- **A sentence can hold both.** `scripts/vet.sh` has "the agent … the step **it**
  could not load" (the agent → they) two clauses before "which is where **it** was
  when it went unrun" (the check → stays). Fixing one line means reading its
  whole sentence, not substituting on a match.
- **The verb has to move with the pronoun.** "it has no GitHub access" becomes
  "they have no GitHub access"; "itself" becomes "themselves".
- **`agent` is also a noun in compounds that are not the actor** — "agent
  infrastructure", "agent loop", "agent proxy", "user agents",
  `/sync-agent-infra`, `agent-project-boilerplate`. Those generated most of the
  grep noise and none of the hits.

## Sites

Line numbers are as of `f526fd9`; the quoted text is the stable anchor. Each row
is a single-pronoun edit — no sentence is restructured.

**In scope per the issue** (`CLAUDE.md`, `.claude/skills/**`, `.claude/rules/**`, comments in `scripts/**`):

| # | Site | Now | After |
|---|---|---|---|
| 1 | `CLAUDE.md:204` § "Adding or renaming a skill" | the agent follows the surviving prose and skips the step **it** couldn't load | …the step **they** couldn't load |
| 2 | `.claude/skills/sync-agent-infra/catalog.md:302` § "Closure is not optional" | the agent reads the surviving prose and skips the step **it** could not load | …the step **they** could not load |
| 3 | `scripts/check-skill-catalog.sh:7` (header comment, assertion 1) | the agent follows the surviving prose and skips the step **it** could not load | …the step **they** could not load |
| 4 | `scripts/vet.sh:25` (header comment, `check-skill-catalog.sh` rationale) | the agent follows the surviving prose past the step **it** could not load | …past the step **they** could not load |
| 5 | `scripts/check-squash-message.sh:5` (header comment) | The skill's Step 3 is an agent reading **its** own output | …an agent reading **their** own output |
| 6 | `.claude/skills/preview/SKILL.md:26` § "Related" | what lets the agent close some of that gap **itself** | …close some of that gap **themselves** |
| 7 | `.claude/skills/audit-github-backlog/SKILL.md:142` § "Feed findings back down" | `SendMessage` it to that agent rather than letting **it** rediscover the fact or miss it | …rather than letting **them** rediscover the fact or miss it |

Row 7 is the one site with three "it"s in a sentence: the first is the evidence,
the third is the fact, and only the middle one is the agent.

**`.claude/rules/**` has no hits.** Its single `agent` mention pronominalizes the
*conventions* ("so conventions reach the agent at the moment **they're**
relevant"), which is already correct and unrelated.

**Adjacent, pending question 1** — the same straggler outside the four named surfaces:

| # | Site | Now | After |
|---|---|---|---|
| 8 | `README.md:85` | The agent selects a subset … expect **it** to ask only about your session type | …expect **them** to ask… |
| 9 | `ADOPTING.md:114` | An agent trusting that would conclude **it** has no GitHub access | …would conclude **they have** no GitHub access |

## Sites deliberately left alone

Named here because a later reader re-running the grep will hit them and should
not "finish the job":

- `CLAUDE.md:41` "no agent can move **it**" — *it* is the environment setup script.
- `CLAUDE.md:66` / `CLAUDE.md:130` / `CLAUDE.md:124` — "it" is the heredoc's effect, the pushed work, and the loop respectively.
- `.claude/skills/finalize/SKILL.md:32,55` — "any agent that resumes **it**" (the branch), "anything else an agent parked there goes with **it**" (the tree).
- `.claude/skills/from-branch/SKILL.md:52` — the harness's quoted "fix **it** now" rule.
- `.claude/skills/handle/SKILL.md:34` — "one without **it**" is the attribution footer.
- `.claude/skills/plan/SKILL.md:71` — "an answer to **it**" is the question.
- `.claude/skills/log-review/SKILL.md:28` — "can't read **it**" is the ref.
- `.claude/skills/watch-ci/SKILL.md:81` — "name what made **it** non-actionable" is the run.
- `.claude/skills/audit-github-backlog/SKILL.md:55,91,352` — the thread dump, the shared rules file, the transcript.
- `scripts/ci-watch-tick.sh`, `scripts/lib/watch-tick-common.sh`, `scripts/lib/gh-repo.sh`, `scripts/check-merge.sh`, `scripts/pr-body.py`, `scripts/gh_export/api.py`, `.claude/hooks/session-start.sh` — every `agent` mention is attributive ("the agent's tick loop", "the agent egress proxy", "agents don't reconstruct the whole body") with no pronoun pointing back at it.

## Steps

1. Flip the plan file to `*.in-progress.md`, quoting the go-ahead.
2. Re-run the grep families against the tree as it then stands, and reconcile
   against the table above before editing — `#59` is open and adds `CLAUDE.md`
   § "Language", so a straggler may have arrived or moved:
   ```
   rg -nU -oe '\bagents?(\x27s)?\b[^.!?]{0,220}?\b(it|its|itself)\b' -g '*.md' -g '*.sh' -g '*.py' CLAUDE.md .claude scripts README.md ADOPTING.md
   rg -nU -oe '\b(analysts?|subagents?)\b[^.!?]{0,160}?\b(it|its|itself)\b' -g '*.md' CLAUDE.md .claude
   ```
   The first family is the sweep; the second catches a fanned-out agent referred
   to by role rather than as "agent". Both stop at sentence punctuation, so also
   read two lines past each `agent` hit for a pronoun that opens the next
   sentence.
3. Apply rows 1–7 (and 8–9 unless question 1 comes back "stated scope only").
   One `Edit` per site; no sentence restructured beyond pronoun-verb agreement.
4. Run `bash scripts/vet.sh`.
5. `/dry`, `/tighten-docs`, then hand the PR to `/pr` — per `@.claude/skills/go/SKILL.md`.

## Open questions

Both are written with the recommended answer already in force above, so silence
is a valid resolution and the plan is implementable as it stands.

1. **Do `README.md` and `ADOPTING.md` travel with the sweep?** The issue names
   four surfaces and `README.md`/`ADOPTING.md` are not among them, but each
   carries exactly one straggler (rows 8–9), and both are prose an adopter reads
   *before* anything in `.claude/`.
   - **(a) Include them — recommended, and in force above.** Two one-word edits
     close the convention across everything a reader meets, and leaving a
     visible "it" in the front door is the inconsistency the issue exists to
     remove.
   - (b) Stated scope only — keep the acceptance criterion's four surfaces
     exactly, and file rows 8–9 as a follow-up.
2. **Commit prefix.** `CLAUDE.md` § "Git conventions" says a change to
   `.claude/skills/**`, this file's conventions, or the `scripts/` the skills
   call is `feat:`/`fix:` and never `docs:` "however Markdown-shaped the diff" —
   yet the issue itself is titled `docs:`, and `README.md` is named there as a
   `docs:` surface.
   - **(a) `fix:` — recommended, and in force above.** The bulk of the diff is
     executed prose, and the convention's carve-out for `docs:` is prose *about*
     the repo that no session runs.
   - (b) `docs:`, matching the issue's own title.
   - (c) `style:`, on the reading that a pronoun sweep changes no instruction.

## DRY notes

Nothing is added, extracted, or moved — the change is seven (or nine) pronouns in
place. The one reuse call the diff raises:

- **Rows 1–4 are the same sentence in four files** ("a dangling `@`-reference
  fails silently — the agent follows the surviving prose and skips the step it
  could not load"), and that duplication is **correct as it stands; do not
  extract it.** The four surfaces are copied independently: an adopter can take
  `scripts/check-skill-catalog.sh` without `CLAUDE.md`, `scripts/vet.sh` names
  the same fact to argue against deleting the line that calls the script, and
  `catalog.md` is read from a fresh clone during a sync with nothing else of the
  repo loaded. A pointer would fail in exactly the case each copy exists to
  cover. What the sweep owes them is **consistency**: all four move together, or
  the tree reads as though the pronoun choice were per-file taste.
- No shared vocabulary file, glossary, or lint rule is introduced. The issue
  rules out a standing rule in `CLAUDE.md` or `.claude/rules/`, and a
  grep-based check would have to encode the boundary above — which misfires on
  the "it" cases more often than it would catch a regression.

## Deliberately out of scope

- **No standing rule.** No entry in `CLAUDE.md` or `.claude/rules/` codifying
  singular they; the issue argues the boundary is too slippery to state in less
  space than the sweep itself, and bets on consistent prose carrying the voice.
- **No mechanical check.** Same reasoning: nothing added to
  `scripts/check-skill-catalog.sh` or `scripts/vet.sh`.
- **`docs/`** — `docs/issue/60/` is a working artifact `/finalize` sweeps, and
  the issue text quoted in it is the reporter's, not the loop's prose.
- **No rewording beyond the pronoun.** Every other tightening these sentences
  might invite belongs to `/tighten-docs` on its own pass, not to a diff whose
  whole claim is "this is a pronoun sweep".

## Acceptance

- No agent-as-"it" left in `CLAUDE.md`, `.claude/skills/**`, `.claude/rules/**`,
  or comments in `scripts/**` (plus `README.md`/`ADOPTING.md` under question 1a).
- Every "it" named under § "Sites deliberately left alone" is untouched.
- `bash scripts/vet.sh` green.
