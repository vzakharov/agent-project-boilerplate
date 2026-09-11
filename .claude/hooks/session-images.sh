#!/bin/bash
# UserPromptSubmit hook: copy operator-attached images out of the session
# transcript into the working tree, and name the new ones in the turn's context.
#
# An attached image exists only as base64 inside the transcript on this machine,
# so it dies with the session. Extraction is a hook rather than an instruction
# because the agent forgetting is the failure it exists to remove.
#
# Nothing here commits, and the extracted file is untracked: an image worth
# keeping rides the next commit the agent makes anyway, which is the decision
# CLAUDE.md § "Writing things down" states. A hook that committed on its own
# would commit to whatever branch HEAD happened to be on, and would restore the
# tree `/finalize` had just swept — the manifest it dedupes against is inside
# that tree, so a sweep is indistinguishable from a first run.
#
# One event carries this, and measurement rather than assumption says which:
# when UserPromptSubmit fires the prompt being submitted is not in the
# transcript yet — the last record is the `queue-operation` carrying its text
# and never its image data. So an image lands at the start of the following
# turn, ahead of anything that could act on the file or commit it. A `Stop`
# firing would write it one moment sooner, with nothing in between to read it.
#
# Never fails the turn: a hook that breaks a session over a screenshot is worse
# than a lost screenshot, so every failure path is stderr plus exit 0.

set -euo pipefail

payload="$(cat)"

say() { echo "session-images: $*" >&2; }

if ! command -v jq >/dev/null; then
  say "jq not found; skipping image extraction."
  exit 0
fi
if ! command -v python3 >/dev/null; then
  say "python3 not found; skipping image extraction."
  exit 0
fi

field() { jq -r --arg k "$1" '.[$k] // empty' <<<"$payload"; }

transcript="$(field transcript_path)"
project="${CLAUDE_PROJECT_DIR:-$(field cwd)}"

[ -n "$transcript" ] && [ -f "$transcript" ] || exit 0
[ -n "$project" ] && [ -d "$project" ] || exit 0

rel_dir="docs/remove-before-merging/session-images"
out="$project/$rel_dir"

if ! written="$(python3 "$project/scripts/extract-session-images.py" "$transcript" --out "$out")"; then
  say "extraction failed; continuing without it."
  exit 0
fi

[ -n "$written" ] || exit 0

names="$(sed "s|^$out/|$rel_dir/|" <<<"$written")"
jq -n --arg names "$names" '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: ("Images the operator attached earlier in this session are on disk as untracked files:\n" + $names + "\nThey sit under a tree `/finalize` sweeps, so one worth keeping moves to a permanent home with `git mv` and is committed with the work that references it. Leave the rest where they are.")
  }
}'
