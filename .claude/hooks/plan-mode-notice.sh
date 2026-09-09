#!/bin/bash
# UserPromptSubmit hook: tell a session in native plan mode that this repo plans
# on disk, and that the exit is plan mode's own.
#
# This has to be a hook rather than prose. Plan mode's injected instructions end
# with "this supercedes any other instructions you have received", so anything
# already in CLAUDE.md or the skill loses to them; additionalContext lands after
# that message and re-fires every prompt, so it cannot be argued away or
# forgotten mid-session. (The first firing is the operator's task message —
# `/plan` is client-side and submits no prompt of its own.)
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
This repo plans on disk: the deliverable is a git-tracked
`docs/plans/<slug>.draft.do-not-implement.md` on a draft PR, and plan mode is
read-only, so it cannot be written from in here.

Take plan mode's own exit now — this is not an override of it. Write the
approval dialog's wording into the harness plan file (verbatim text in
`.claude/skills/plan/SKILL.md` § "If the session is already in native plan
mode"), call `ExitPlanMode` bare, then run that skill from the top.

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
