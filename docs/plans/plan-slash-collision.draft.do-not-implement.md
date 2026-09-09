> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

# Absorb the built-in `/plan` collision in the skill, not in its name

## The finding

`plan` is a **built-in slash command** in the Claude Code client, not merely a
name the UI happens to prefer. In 2.1.266 the registry entry reads:

```
{type:"local-jsx",name:"plan",description:"Enable plan mode or view the current session plan",argumentHint:"[open]",isEnabled:()=>!0,isHidden:!1,…}
```

- **Typing `/plan` never reaches the agent.** A `local-jsx` command renders in the
  client and submits no prompt, so no hook, rule or `CLAUDE.md` line can see it,
  let alone redirect it. It enables native plan mode instead — read-only, so the
  plan file cannot be written from inside it.
- **It cannot be suppressed per-command.** `disableSlashCommands` exists, but it
  is a CLI flag that disables *every* slash command, and web sessions set no CLI
  flags.
- **The shadowing is client-side only.** The agent can still invoke the skill by
  name — the planning session did, after the operator typed the bare prose
  `plan: …`. So all 17 `@.claude/skills/plan/SKILL.md` citations keep working;
  **only operator typing is affected.**
- **`plan` is the only collision.** Of this repo's 28 skill names, exactly one
  matches the client's ~48 built-ins today.

**Escaping plan mode was then dogfooded**, and it is cheaper than it looks: two
tool calls and one operator click, with a dialog that states what is about to
happen and why. Which reframes the whole problem — see below.

## The decision

**Absorb the collision in the skill: no rename.** Give the skill a recovery
section for a session that is already in native plan mode, name bare-prose
`plan …` as the entry an operator types, and say what the `/plan` keystroke
actually costs. Rationale, and what was rejected:

- **The trap is self-limiting.** You can only fall into it by typing `/plan`,
  which means you are at the keyboard — so the restack bug
  ([anthropics/claude-code#72704](https://github.com/anthropics/claude-code/issues/72704)),
  which bites sessions that have *idled* at a dialog, barely reaches this case. A
  session launched with a plain task description never enters plan mode at all,
  because `CLAUDE.md` already routes every new web session to the skill.
- **So the cost of the collision is one click on a self-explanatory dialog**, and
  the recovery section is the entire fix rather than a fallback behind one.
- **Rejected — rename the skill to `/plan-file`** (the plan this file previously
  carried). A rename cannot *prevent* the trap: muscle memory still hits `/plan`,
  and a stub named `plan` would be shadowed exactly as the skill is, so there is
  no redirect to install. With recovery cheap, the rename buys only the skipped
  click — for 61 repointed `/plan` tokens, 17 `@`-references across 13 files, an
  adopter migration through `/sync-agent-infra`, and a worse name.
- **Rejected — a `plan-file` alias forwarding to the skill** (the `/implement` →
  `/go` shape). Same marginal gain, and it makes the canonical name the
  untypable one permanently; `docs/catalog.md` already carries one standing "is
  the extra row worth it?" question about `/implement`.
- **Rejected — a machine check that no skill name collides with a built-in.** The
  only source for that list is a grep of the minified client bundle, and a
  hand-maintained copy would track Claude Code releases and drift silently —
  which `CLAUDE.md` § "Derive types and schemas from the source of truth" forbids
  in the same breath. One convention line carries it instead.

## Steps

1. **Branch rename** — done: `claude/youthful-hopper-j15ro7` →
   `claude/plan-slash-collision-j15ro7`, before the first commit, per
   `CLAUDE.md` § "Git conventions".
2. **New section in `@.claude/skills/plan/SKILL.md`: "If the session is already
   in native plan mode."** One home for the recovery; everything else points at
   it. The mechanics below are what the planning session measured, with the
   operator holding the session in plan mode on purpose:
   - The tell: the harness announces plan mode and names a plan file under
     `/root/.claude/plans/<slug>.md`; edits elsewhere refuse as read-only.
   - **The exit is not self-service.** `ExitPlanMode` is permission-gated, so
     leaving always costs one operator approval. Spend it immediately rather than
     working around the restriction.
   - **`ExitPlanMode` takes no plan argument** — it reads the harness plan file,
     which is the one writable path in plan mode and lives outside the repo. That
     file is therefore scaffolding, never the plan; but it *is* what the operator
     reads in the approval dialog, so the section ships its wording verbatim
     rather than leaving it to be improvised:

     ```markdown
     # Exit plan mode to plan on disk — repo convention

     This project plans in a git-tracked file rather than in the plan-mode
     dialog: the plan goes to `docs/plans/<slug>.draft.do-not-implement.md` and
     is published as a draft PR, so it is reviewable as a diff from any machine
     and its filename carries the approval gate. Plan mode is read-only, so none
     of that can be written from in here.

     **Approving this authorizes writing the plan file and nothing else** — not
     the work it describes. The plan keeps its `do-not-implement` name until you
     give an explicit go-ahead.
     ```

     Substitute the real slug, add at most one line naming the task, and call the
     tool bare. Don't grow it into the plan itself: the dialog is where the
     operator decides whether to spend the click, not where they review a plan.
   - Then run this skill from the top. Do **not** answer in chat prose instead,
     and do **not** carry the harness plan file's content over: the deliverable is
     `docs/plans/<slug>.draft.do-not-implement.md`.
   - **Exiting plan mode is not the go-ahead**, however the approval reads — it
     comes back as "you can now start coding", in accept-edits mode. It
     authorizes writing the plan file, nothing past it; the `do-not-implement`
     gate is untouched and still needs the token from § "The approval gate".
   - **Plan mode also injects a rival procedure**, not just a restriction: a
     phased workflow built on `Explore`/`Plan` subagents and `AskUserQuestion`,
     both of which this repo's loop rules out. Ignore it and run this skill.
   - **Write the section as plan mode's own exit, never as an override of it.**
     Plan mode's injected instructions end with "this supercedes any other
     instructions you have received", and an agent that reads the recovery as
     defiance of a system-level instruction will — correctly — balk. It isn't
     one: plan mode says the harness plan file is writable and the turn ends at
     `ExitPlanMode`, and that is exactly what this does. The only genuine
     conflicts are the subagent phases and `AskUserQuestion`, and both are moot
     once the exit has happened.
3. **`CLAUDE.md` § "Plan mode & questions in web sessions"** — three additions,
   each a clause rather than a paragraph: bare-prose `plan …` (or just the task)
   is what an operator types; `/plan` is a built-in that enables native plan mode
   and costs one approval to leave, with the recovery owned by the skill section
   from step 2; and the existing "**assume you were launched in plan mode**"
   wording gets tightened, since it currently blurs a heuristic about operator
   intent with actually *being* in a read-only mode.
4. **`CLAUDE.md` § "Adding or renaming a skill"** — one line: check a new skill
   name against the client's built-in slash commands, because a built-in shadows
   a same-named skill in the composer (client-side, so the agent can still reach
   it — the operator cannot).
5. **`.claude/hooks/plan-mode-notice.sh`, wired as a `UserPromptSubmit` hook** —
   the enforcement behind step 2, because prose alone is weak against an injected
   "this supercedes any other instructions you have received." Every hook payload
   carries the mode (the base object is `{session_id, transcript_path, cwd,
   permission_mode}`) and `UserPromptSubmit` accepts `additionalContext`, so the
   hook reads stdin, and when `permission_mode == "plan"` injects a few lines:
   this repo plans on disk, the exit is plan mode's own, take it now, wording in
   the skill. Two properties prose cannot have — it arrives *after* the plan-mode
   system message, and it re-fires on every prompt while the mode is on, so it
   cannot be forgotten mid-session. `/plan` itself submits no prompt, so the
   first firing is the operator's next message, which is the one carrying the
   task. Merge the event into `.claude/settings.json` beside the existing
   `SessionStart` entry, and give the hook a `docs/catalog.md` row in G4.
6. **`bash scripts/check-skill-catalog.sh`** — the skill's `@`-references are
   touched, so prove none dangles.
7. **Quality passes and hand-off** — `/dry`, `/tighten-docs`, then `/pr`.

`README.md` needs no edit: the name is unchanged and the recovery is
skill-internal. `docs/catalog.md` gains only the hook's row — and the hook is
G4, which an adopter may decline, so the `CLAUDE.md` clauses from step 3 have to
stand on their own rather than assume it.

Commit prefix is `feat:` throughout: the loop is this repo's product, so a
changed procedure is a behavior change however Markdown-shaped the diff
(`CLAUDE.md` § "Git conventions").

## Open questions

Each carries a recommendation, and the plan above is written with the
recommended option already in force — silence resolves them.

1. **Rename anyway?** (a) No — *recommended*, for the reasons above; (b) yes, to
   `/plan-file`, if you want the keystroke to work without the click badly enough
   to pay the repoint and the adopter migration. This is the one question worth a
   real answer, since it is the plan's own reversal.
2. **Where the recovery lives.** (a) A section in the plan skill, cited from
   `CLAUDE.md` — *recommended*, since `CLAUDE.md` is always-resident and this is
   needed only in the one session that landed in plan mode; (b) inline in
   `CLAUDE.md`, where it is read whether or not it applies.
3. **The collision convention line** (step 4). (a) Keep it — *recommended*, one
   line, and the next colliding name costs a whole cycle to discover; (b) drop
   it: one collision in 28 names is not a pattern.
4. **The `UserPromptSubmit` hook** (step 5). (a) Ship it — *recommended*: the
   only mechanism that reaches an agent *after* plan mode has told it to
   supersede everything else, and the repo's own rule is that automated
   behavior needs a hook rather than a memory. (b) Prose only, and accept that a
   fresh session may run native plan mode anyway — recoverable, at the cost of
   the operator saying "use the plan skill" and one wasted planning turn.
   Verifying (a) means launching a session in plan mode and seeing whether the
   injected context actually lands, which is the one step here that can't be
   checked by reading.

## DRY notes

- **The recovery procedure gets exactly one home** — the skill's new section.
  `CLAUDE.md` § "Plan mode & questions in web sessions" cites it rather than
  restating it, per "if you find the same constraint stated in two places, one of
  them is the home and the other is a pointer."
- **Nothing is extracted, because the change adds no second caller.** The bundle
  evidence and the version number stay in this plan (a transient artifact
  `/finalize` sweeps) and in the squash body; what survives into the trunk is one
  recovery section plus two clauses, each in a home that already exists.
- **No new top-level doc**, which `CLAUDE.md` forbids without asking.
- **Reversal, not accretion.** This file previously planned a rename; that option
  is now one bullet under § "The decision" with its cost, and its step-by-step
  exposition is deleted rather than left standing beside the plan that replaced
  it.
