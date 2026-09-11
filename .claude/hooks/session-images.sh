#!/bin/bash
# UserPromptSubmit + Stop hook: copy operator-attached images out of the session
# transcript onto the branch, and in a remote session commit what was copied.
#
# An attached image exists only as base64 inside the transcript on this machine,
# so it dies with the session. Extraction is a hook rather than an instruction
# because the agent forgetting is the failure it exists to remove.
#
# The two events split the job, and measurement rather than assumption puts the
# split where it is: when UserPromptSubmit fires the prompt being submitted is
# not in the transcript yet — the last record is the `queue-operation` carrying
# its text and never its image data. So Stop is what persists an image, at the
# end of the turn it arrived in, and UserPromptSubmit is what names the ones
# already on disk at the start of the next.
#
# The commit is remote-only, matching CLAUDE.md § "Git conventions", which scopes
# proactive committing to the sessions where the operator reviews from another
# machine. Locally they are looking at the tree itself, so the file in
# `git status` is the whole signal. It never pushes: a push publishes whatever
# else the branch has committed, at a moment nobody chose. And it carries no
# session trailer — the payload names the transcript's session uuid, not the
# `session_01…` id the attribution link needs, and a fabricated link is worse.
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
event="$(field hook_event_name)"
project="${CLAUDE_PROJECT_DIR:-$(field cwd)}"

[ -n "$transcript" ] && [ -f "$transcript" ] || exit 0
[ -n "$project" ] && [ -d "$project" ] || exit 0

rel_dir="docs/remove-before-merging/session-images"
out="$project/$rel_dir"

if ! written="$(python3 "$project/scripts/extract-session-images.py" "$transcript" --out "$out")"; then
  say "extraction failed; continuing without it."
  exit 0
fi

if [ "$event" = "UserPromptSubmit" ]; then
  [ -n "$written" ] || exit 0
  names="$(sed "s|^$out/|$rel_dir/|" <<<"$written")"
  jq -n --arg names "$names" '{
    hookSpecificOutput: {
      hookEventName: "UserPromptSubmit",
      additionalContext: ("Images the operator attached earlier in this session are on the branch as files:\n" + $names + "\nThey are working artifacts under a tree /finalize sweeps; `git mv` one worth keeping to a permanent home.")
    }
  }'
  exit 0
fi

# Stop: commit, in a remote session only.
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0

git_dir="$(git -C "$project" rev-parse --git-dir 2>/dev/null)" || exit 0
case "$git_dir" in /*) ;; *) git_dir="$project/$git_dir" ;; esac

if [ "$(git -C "$project" rev-parse --abbrev-ref HEAD 2>/dev/null)" = "HEAD" ]; then
  say "HEAD is detached; leaving $rel_dir uncommitted."
  exit 0
fi
if [ -e "$git_dir/MERGE_HEAD" ] || [ -d "$git_dir/rebase-merge" ] || [ -d "$git_dir/rebase-apply" ]; then
  say "a merge or rebase is in progress; leaving $rel_dir uncommitted."
  exit 0
fi

git -C "$project" add -- "$rel_dir" 2>/dev/null || { say "git add failed."; exit 0; }
files="$(git -C "$project" diff --cached --name-only -- "$rel_dir")"
[ -n "$files" ] || exit 0

if ! git -C "$project" commit --quiet --only \
  -m "chore: capture operator-attached session images" -m "$files" \
  -- "$rel_dir" 2>/dev/null; then
  say "commit failed; $rel_dir is staged and left for the agent."
fi
exit 0
