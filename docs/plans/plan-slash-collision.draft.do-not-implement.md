> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Route the plan skill around Claude Code's built-in `/plan`

## The finding

`plan` is a **built-in slash command** in the Claude Code client, not merely a
name the UI happens to prefer. In 2.1.266 the registry entry reads:

```
{type:"local-jsx",name:"plan",description:"Enable plan mode or view the current session plan",argumentHint:"[open]",isEnabled:()=>!0,isHidden:!1,…}
```

Three consequences follow from `type:"local-jsx"` and `isEnabled:()=>true`:

- **Typing `/plan` never reaches the agent.** A `local-jsx` command renders in the
  client and submits no prompt, so no hook, rule or `CLAUDE.md` line can see it,
  let alone redirect it.
- **The cost is worse than a no-op.** It *enables native plan mode* — the
  read-only mode whose exit is the `ExitPlanMode` dialog that
  [anthropics/claude-code#72704](https://github.com/anthropics/claude-code/issues/72704)
  restacks and drops answers for. So the keystroke that means "use the plan
  skill" lands the session in the exact UI the skill exists to avoid, and in a
  mode that cannot write the plan file.
- **It cannot be suppressed per-command.** `disableSlashCommands` exists, but it
  is a CLI flag that disables *every* slash command, and web sessions set no CLI
  flags.

Two facts bound the damage, and they are what the options below trade against:

- **The shadowing is client-side only.** The agent can still invoke the skill by
  name — this session did, after the operator typed the bare prose `plan: …`. So
  every `@.claude/skills/plan/SKILL.md` citation in the loop keeps working
  untouched; **only operator typing is broken.**
- **`plan` is the only collision.** Of this repo's 28 skill names, exactly one
  matches the client's ~48 built-ins today (`review`, `security-review`,
  `pr-comments`, `init` and `skills` are built-ins, but none of ours claim those
  names).

## The decision

**Rename the skill to `/plan-file`, ship no `plan` compatibility stub, and give
the skill a recovery section for a session that is already in native plan mode.**
Rationale, and what was rejected:

- **A rename is the only thing that yields a command an operator can type.** It
  does not *prevent* the trap — muscle memory will still hit `/plan`, and a stub
  named `plan` would be shadowed just like the skill, so there is no redirect to
  install. That is why the recovery section is load-bearing rather than
  defensive: it is the only piece that handles the case that actually happens.
- **`plan-file` keeps the muscle-memory keystroke useful.** Typing `/plan` lists
  the built-in *and* `/plan-file` side by side, so the reach for the old name is
  a teaching moment instead of a dead end. It also says what the skill is: the
  plan is a file.
- **Rejected — keep the name, and tell operators to type bare `plan`.** Cheap,
  and already half in force (`CLAUDE.md` routes *every* new web session to the
  skill, so a plain task description suffices and the bare word is only
  emphasis). But it leaves the repo advertising `/plan` in 61 places while that
  keystroke is booby-trapped, and it never gives an explicit invocation for the
  mid-session case ("plan this separate piece of work"). Kept as a *documented
  fallback*, not as the fix.
- **Rejected — a `plan-file` alias forwarding to a skill still homed at `plan`**
  (the `/implement` → `/go` shape, inverted). It avoids the repoint churn, but
  makes the canonical name the untypable one permanently, and `docs/catalog.md`
  already carries one standing "is the extra row worth it?" question about
  `/implement`; a second is worse than a sed.
- **Rejected — a machine check that no skill name collides with a built-in.** The
  only source for that list is a grep of the minified client bundle, and a
  hand-maintained copy would track Claude Code releases and drift silently —
  which `CLAUDE.md` § "Derive types and schemas from the source of truth"
  forbids in the same breath. One convention line carries it instead.

## Steps

1. **Branch rename** — done: `claude/youthful-hopper-j15ro7` →
   `claude/plan-slash-collision-j15ro7`, before the first commit, per
   `CLAUDE.md` § "Git conventions".
2. **`git mv .claude/skills/plan .claude/skills/plan-file`**, then repoint every
   citation: 17 `@.claude/skills/plan/SKILL.md` references and 61 `/plan` tokens
   across 13 files (`CLAUDE.md`, `README.md`, `docs/catalog.md`, and the
   `go`, `pr`, `finalize`, `handle`, `issue`, `from-branch`, `propose-issue`,
   `squash-message`, `audit-github-backlog` skills). Do it with a scripted
   replacement and then read the diff — the prose also says "plan mode", "plan
   file" and "the plan" in senses a blind sed would corrupt.
3. **`bash scripts/check-skill-catalog.sh`** — proves no `@`-reference dangles
   and that the renamed skill has exactly one `docs/catalog.md` row.
4. **New section in the skill: "If the session is already in native plan mode."**
   One home for the recovery; everything else points at it. Content:
   - The tell: edits and commits refuse as read-only, or the harness says plan
     mode.
   - Get out immediately, while the operator is still at the keyboard —
     `ExitPlanMode` with a one-line plan that says only *write the plan to
     `docs/plans/<slug>.draft.do-not-implement.md` and publish it as a draft PR*.
     The restack bug bites sessions that have idled, so session start is when the
     dialog is most likely to survive. If it is lost anyway, say so in one line
     and ask the operator to switch the session out of plan mode.
   - Then run this skill from the top. Do **not** answer in chat prose instead —
     the deliverable is the file.
   - **Exiting plan mode is not the go-ahead.** It authorizes writing the plan
     file, nothing past it; the `do-not-implement` gate is untouched and still
     needs the token from § "The approval gate".
5. **`CLAUDE.md` § "Plan mode & questions in web sessions"** — repoint to
   `/plan-file`, state in one clause why the name is not `/plan` (the built-in
   enables native plan mode and never reaches the agent), name bare-prose
   `plan …` as the fallback entry, and point at the skill's new section for
   recovery. Also tighten the existing "**assume you were launched in plan
   mode**" wording, which currently blurs the heuristic about operator intent
   with actually *being* in a read-only mode.
6. **`CLAUDE.md` § "Adding or renaming a skill"** — one line: check a new skill
   name against the client's built-in slash commands, because a built-in shadows
   a same-named skill in the composer (client-side, so the agent can still reach
   it — the operator cannot).
7. **`README.md` § "Why `/plan` and `/go` exist"** and **`docs/catalog.md`** —
   rename the mentions and the G2 row plus the four "Pulls in" cells. The
   catalog row carries the *why* of the name, so an adopter does not helpfully
   rename it back to `plan`.
8. **Quality passes and hand-off** — `/dry`, `/tighten-docs`, then `/pr`.

Commit prefix is `feat:` throughout: the loop is this repo's product, so a
changed procedure is a behavior change however Markdown-shaped the diff
(`CLAUDE.md` § "Git conventions").

## Open questions

Each carries a recommendation, and the plan above is written with the
recommended option already in force — silence resolves them.

1. **The name.** (a) `/plan-file` — *recommended*, prefix-discoverable from the
   muscle-memory keystroke and self-describing; (b) `/write-plan` — closer to the
   house verb-first style (`/propose-issue`, `/check-merge`), but invisible to
   someone typing `/plan`; (c) `/blueprint` — zero ambiguity, zero
   discoverability, and a new word to learn.
2. **A compatibility stub named `plan`?** (a) None — *recommended*: it would be
   shadowed in the composer, and no handoff block or plan file emits `/plan`
   (they emit `/go`), so there is no caller to redirect. (b) Ship one anyway for
   agent-internal robustness, at the cost of a permanent extra catalog row.
3. **Collision hardening.** (a) One convention line in `CLAUDE.md` —
   *recommended*; (b) also a `scripts/check-skill-catalog.sh` assertion against a
   checked-in list of built-in names — rejected above as a hand-maintained
   duplicate of an upstream list.

## DRY notes

- **The recovery procedure gets exactly one home** — the skill's new section.
  `CLAUDE.md` § "Plan mode & questions in web sessions" cites it rather than
  restating it, per "if you find the same constraint stated in two places, one of
  them is the home and the other is a pointer."
- **No abstraction is extracted, because none is shared.** The bulk of the work
  is repointing citations that already exist; `CLAUDE.md` § "Writing things down"
  requires exactly that ("when a convention changes, every place that states it
  changes with it"). The alternative — a single "skill names" indirection layer
  that every citation reads through — would add a hop to 78 call sites to save
  one future sed, and Markdown has no mechanism for it anyway.
- **The finding above is not written down twice.** The client-side-only nature of
  the shadowing is what makes the rename safe for agent-internal citations; it is
  stated once here (a transient artifact `/finalize` sweeps) and survives into
  the trunk only as the one-line *why* on the `docs/catalog.md` row and the one
  convention line in `CLAUDE.md`. The bundle grep and the version number stay in
  this plan and in the squash body — nothing in the trunk tracks a client
  internal.
- **No new top-level doc**, which `CLAUDE.md` forbids without asking: the three
  durable sentences fit in homes that already exist.
