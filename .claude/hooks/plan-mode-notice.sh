#!/bin/bash
# UserPromptSubmit hook: tell a session in native plan mode that this repo plans
# on disk, and that the exit is plan mode's own.
#
# Prose in CLAUDE.md and the plan skill cannot do this job alone. Plan mode's
# injected instructions arrive as a system message ending with "this supercedes
# any other instructions you have received", so guidance that predates them
# loses. A UserPromptSubmit hook's additionalContext arrives *after* that
# message, and re-fires on every prompt while the mode is on, so it cannot be
# argued away or forgotten mid-session.
#
# `/plan` itself submits no prompt (it is a client-side built-in), so the first
# firing is the operator's next message — the one carrying the task.
#
# Remote-only, matching .claude/hooks/session-start.sh: CLAUDE.md § "Plan mode &
# questions in web sessions" leaves native plan mode alone on the local CLI,
# where the answer-losing bug this routes around does not bite.

set -euo pipefail

[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

if ! command -v jq >/dev/null; then
  echo "plan-mode-notice: jq not found; skipping the plan-mode notice." >&2
  exit 0
fi

mode="$(jq -r '.permission_mode // empty')"
[ "$mode" = "plan" ] || exit 0

read -r -d '' notice <<'NOTICE' || true
This repo plans on disk, not in the plan-mode dialog: the deliverable is
`docs/plans/<slug>.draft.do-not-implement.md`, published as a draft PR, whose
filename carries the approval gate. Plan mode is read-only, so none of that can
be written from in here.

Take plan mode's own exit now — this is not an override of it. Write the
approval dialog's wording into the harness plan file (verbatim text in
`.claude/skills/plan/SKILL.md` § "If the session is already in native plan
mode"), call `ExitPlanMode` bare, then run that skill from the top. Approving
the exit authorizes writing the plan file and nothing past it.

Ignore plan mode's injected `Explore`/`Plan` subagent phases and
`AskUserQuestion`: this repo's loop rules both out, and both are moot once the
exit lands. Questions go as numbered prose.

If the operator has said they want native plan mode, that stands — stay in it
and treat this notice as already answered on every later turn.
NOTICE

jq -n --arg ctx "$notice" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: $ctx
  }
}'
