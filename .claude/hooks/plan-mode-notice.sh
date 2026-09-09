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
`docs/plans/<slug>.draft.do-not-implement.md` on a draft PR, and plan mode holds
the session to read-only work, so writing it means leaving first.

Take plan mode's own exit now — this is not an override of it. Copy
`.claude/skills/plan/exit-dialog.md` over the harness plan file (creating its
directory, which does not exist yet), so the approval dialog carries this repo's
wording, call `ExitPlanMode` bare, then run `.claude/skills/plan/SKILL.md` from
the top.

The read-only restriction gates `Edit`/`Write` and not Bash, so that plan file
is writable from in here. Writing it anyway takes the operator's approval rather
than asking for it — the exit above is how to ask.

Ignore plan mode's injected `Explore`/`Plan` subagent phases and
`AskUserQuestion`: this repo's loop rules both out, and both are moot once the
exit lands. Questions go as numbered prose.

Rejecting that approval is how the operator says they want native plan mode
after all — the dialog copy tells them so. If they reject it, or say as much in
chat, stay in the mode, run its own workflow, and treat this notice as already
answered on every later turn.
NOTICE

jq -n --arg ctx "$notice" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: $ctx
  }
}'
