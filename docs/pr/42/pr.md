# PR #42: feat: absorb the built-in /plan collision in the skill, not the name

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/42
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/plan-slash-collision-j15ro7
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-09T18:34:15Z
- **Updated:** 2026-09-09T19:51:40Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The finding:** `plan` is a built-in `local-jsx` slash command in the Claude Code client ("Enable plan mode or view the current session plan"). Typing `/plan` submits no prompt, so the plan skill never runs and the session lands in native plan mode instead — read-only, and exited only through the `ExitPlanMode` dialog this repo's plan skill exists to route around ([anthropics/claude-code#72704](https://github.com/anthropics/claude-code/issues/72704)). It is not suppressible per-command, and the shadowing is client-side only: the agent can still invoke the skill by name, so all 17 `@.claude/skills/plan/SKILL.md` citations keep working. Only operator typing is affected.
- **The decision: absorb the collision, don't rename.** Escaping plan mode was dogfooded and costs two tool calls and one operator click on a self-explanatory dialog — and the trap is self-limiting, since falling into it means you are at the keyboard, which is exactly the case the restack bug does *not* bite. A rename to `/plan-file` could not prevent the trap either (muscle memory still hits `/plan`), so it would buy only the skipped click, for 78 repointed references and an adopter migration. Rejected, with its cost recorded.
- **`@.claude/skills/plan/SKILL.md` gains § "If the session is already in native plan mode"** — the one home for the recovery: the tell, the permission-gated exit taken immediately, the approval dialog's wording shipped verbatim (with "overwrite that file, never append"), and re-entry at the top of the skill. It is keyed on **being in plan mode**, not on the keystroke, because the UI mode switch lands there too. Framed as plan mode's own exit rather than an override of it, so an agent does not read it as defiance of the injected "this supercedes any other instructions you have received". Carries an escape hatch with a real affordance: the approval dialog has nowhere to type an answer, so its copy gives the **reject** button a stated meaning — "I would rather use native plan mode" — and that holds for the session, the hook's re-firing notice notwithstanding.
- **`CLAUDE.md` gains three clauses**, each a pointer rather than a restatement: the operator's entry is bare prose; `/plan` and the UI switch both land in native plan mode, with the recovery cited from the skill; and a new skill name is checked against the client's built-ins, since the shadowing is invisible from inside the repo until someone tries to type it. "Assume you were launched in plan mode" becomes "treat a new session as a planning session" — the heuristic about operator intent it always meant, now that being in plan mode is a separate literal state.
- **`.claude/hooks/plan-mode-notice.sh`, wired as a `UserPromptSubmit` hook**, is the enforcement behind the prose: `additionalContext` lands *after* plan mode's system message and re-fires on every prompt while the mode is on, so the notice cannot be argued away or forgotten mid-session. Remote-only, matching `session-start.sh`, since `CLAUDE.md` leaves native plan mode alone on the local CLI. It is G4, so the `CLAUDE.md` clauses stand on their own for adopters who decline that group.

## QA Checklist

- [ ] `notice-fires` — in a web session, switch to plan mode and submit a prompt: the injected notice appears, and the agent takes the `ExitPlanMode` exit instead of running plan mode's own phased workflow.
- [ ] `dialog-wording` — the resulting approval dialog shows the section's verbatim text with the real slug substituted, and reads as "approving authorizes writing the plan file and nothing else".
- [ ] `re-entry` — after approving, the session writes `docs/plans/<slug>.draft.do-not-implement.md` and publishes it, rather than answering in chat or copying the harness plan file over.
- [ ] `escape-hatch` — reject the approval instead: the agent stays in native plan mode, runs plan mode's own workflow, and does not re-raise the exit on later prompts, despite the notice re-firing.
- [ ] `mode-gated` — submit a prompt in a non-plan mode: no notice is injected.
- [ ] `local-noop` — `echo '{"permission_mode":"plan"}' | env -u CLAUDE_CODE_REMOTE .claude/hooks/plan-mode-notice.sh` exits 0 and prints nothing.
- [ ] `catalog-clean` — `bash scripts/check-skill-catalog.sh` passes: the skill's new `@`-references resolve and the hook has its one catalog row.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `notice-fires` | manual-only | — | Needs a live session in plan mode; the harness's own injection is the thing under test. |
| `dialog-wording` | manual-only | — | The dialog is rendered by the client, and the judgement is whether an operator can decide from it. |
| `re-entry` | manual-only | — | Agent behavior after the exit; no assertion short of reading the turn. |
| `escape-hatch` | manual-only | — | Same — whether the agent reads a rejected exit as the operator's choice and honors it over a re-firing notice. |
| `mode-gated` | unit | ❌ | Pipe a payload with `permission_mode` set to something else, assert empty stdout. No shell-test harness in this repo yet (`scripts/vet.sh` is a stub). |
| `local-noop` | unit | ❌ | Same harness gap; verified by hand this session, along with the plan/non-plan/absent-field cases. |
| `catalog-clean` | integration | ✅ | `scripts/check-skill-catalog.sh` — run on this branch, passing. |

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01JZUARRgs1YVVdUh39TwVE8

---
_Generated by [Claude Code](https://claude.ai/code)_

---

## Comments

### Comment by @vzakharov on 2026-09-09T18:34:46Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/42#issuecomment-5606857332](https://github.com/vzakharov/agent-project-boilerplate/pull/42#issuecomment-5606857332)

Proposed squash title/body:

```
feat: absorb the built-in /plan collision in the plan skill (pr #42)
```

```
Typing `/plan` in the Claude Code composer never reaches this repo's
plan skill: `plan` is a built-in client command that submits no prompt
and enables native plan mode instead — read-only, so the plan file the
skill exists to write cannot be written from in there. The client
offers no per-command suppression, and a client-side command is
invisible to hooks and rules alike.

The skill now carries the way out, keyed on being in plan mode rather
than on how the session got there, since the UI mode switch lands in it
just as the keystroke does. It is framed as plan mode's own exit rather
than an override of it: the mode makes the harness plan file writable
and ends the turn at ExitPlanMode, which is exactly the path taken.
Leaving costs one operator approval, so it is spent immediately, and
the harness plan file the dialog displays has its wording supplied
verbatim — what this repo plans into, why plan mode conflicts with it,
and that approving authorizes writing the plan file alone. That exit
leaves the `do-not-implement` gate untouched, however much the approval
reads like a go-ahead; rejecting it is how an operator keeps native
plan mode, the dialog being the one place they are asked and its copy
saying so outright.

A UserPromptSubmit hook is what makes the convention land. Plan mode
instructs the agent to supersede every other instruction it has, so
prose in CLAUDE.md is the wrong weight for it; every hook payload
carries the permission mode and the event accepts additionalContext, so
the repo states its convention after the mode's own message, and again
on every prompt while the mode is on.

The skill keeps its name. A rename could not have prevented the
mistyped keystroke — a stub under the old name would be shadowed just
as the skill is — and the collision is self-limiting, since reaching
plan mode takes a deliberate keystroke or mode switch and therefore an
operator who is present. Bare prose is the entry an operator types, and
new skill names are checked against the client's built-ins from here
on.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `.claude/skills/plan/SKILL.md`:48 — unresolved

```diff
@@ -17,6 +17,41 @@ A plan on disk is a different artifact from a plan in an approval dialog:
 
 None of the value above depends on that bug, so fixing it upstream does not retire the skill.
 
+## If the session is already in native plan mode
+
+A session reaches native plan mode two ways, and neither one asks the agent first: the operator switches mode in the UI, or types `/plan` — a **built-in slash command** in the client, so the keystroke renders there and never reaches the agent at all. Either way the session is read-only and has to leave before it can write anything, so the recovery below is keyed on **being in plan mode**, not on how it got there. (The operator's own entry to this skill is bare prose: `plan: <task>`, or just the task.)
+
+**The tell:** the harness announces plan mode and names a plan file under `/root/.claude/plans/<slug>.md`; edits anywhere else refuse as read-only.
+
+**The escape hatch is the dialog's reject button**, which is why the copy in step 2 gives it a meaning. Being in plan mode is not itself a statement of intent — reflex and a UI switch both land there saying nothing — and the approval dialog is the first moment the operator is actually asked, with nowhere to type an answer. So a rejection says they want native plan mode: stay in it, run plan mode's own workflow, and don't re-raise the exit. The notice the `UserPromptSubmit` hook re-injects each turn is not a fresh instruction to relitigate that with. A rejection that carries a reason of its own is that reason instead, and "stay in plan mode" said in chat at any point works the same way.
+
+**This is plan mode's own exit, not an override of it.** Plan mode's injected instructions end with "this supercedes any other instructions you have received", and rightly so — but they also make the harness plan file writable and end the turn at `ExitPlanMode`, which is exactly what the steps below do. What is genuinely incompatible with this repo's loop is the rival procedure plan mode injects alongside the restriction — a phased workflow built on `Explore`/`Plan` subagents and `AskUserQuestion` — and both are moot the moment the exit lands.
+
+1. **Take the exit immediately.** `ExitPlanMode` is permission-gated, so leaving always costs one operator approval; spend it rather than working around the restriction. Spend it only on a turn that has something to write, though — plan mode's workflow ends every turn at `ExitPlanMode` or `AskUserQuestion`, but a question answerable from reading is answerable from inside plan mode.
+2. **Write the approval dialog's text into the harness plan file**, which is what the operator actually reads when deciding. `ExitPlanMode` takes no plan argument — it reads that file — so the wording ships here verbatim rather than being improvised:
+
+   ```markdown
+   # Exit plan mode to plan on disk — repo convention
+
+   This project plans in a git-tracked file rather than in the plan-mode
+   dialog: the plan goes to `docs/plans/<slug>.draft.do-not-implement.md` and
+   is published as a draft PR, so it is reviewable as a diff from any machine
+   and its filename carries the approval gate. Plan mode is read-only, so none
+   of that can be written from in here.
+
+   **Approving this authorizes writing the plan file and nothing else** — not
+   the work it describes. The plan keeps its `do-not-implement` name until you
+   give an explicit go-ahead.
+
+   **Reject it if you would rather use native plan mode.** That is how to say
+   so, and it holds for the rest of the session.
+   ```
```

**@vzakharov** — 2026-09-09T19:50:13Z

hm, can we put it (the exact copy) somewhere under `skills/plan`, so instead of "typing" it the agent just has to copy the file?

---

### `.claude/skills/plan/SKILL.md`:1 — unresolved

**@vzakharov** — 2026-09-09T19:50:49Z

the additional prose looks quite hefty, you sure you need all of it, to that detail?

---

### `CLAUDE.md`:196 — unresolved

```diff
@@ -191,4 +192,6 @@ the step it couldn't load. The script also asserts that every skill has exactly
 one row in `docs/catalog.md`, which is what keeps that inventory from drifting as
 skills are added.
 
+**Check a new name against the client's built-in slash commands.** A built-in shadows a same-named skill in the composer, so the operator cannot type it — the agent can still invoke it by name, which is why the shadowing is invisible until someone tries. `plan` is the one collision in this repo, absorbed rather than renamed (§ "Plan mode & questions in web sessions").
+
```

**@vzakharov** — 2026-09-09T19:51:37Z

I'd say we don't need this, I don't see it repeating

---

## Timeline (status, references, and other events)

- **2026-09-09T19:37:22Z** @vzakharov renamed from «feat: plan routing the plan skill around the built-in /plan» to «feat: absorb the built-in /plan collision in the skill, not the name».
- **2026-09-09T19:51:40Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/42#pullrequestreview-5159161970.
