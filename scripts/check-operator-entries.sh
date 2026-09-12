#!/bin/bash
# Assert that every file in `.claude/skills/plainly/operators/` is reachable.
#
# `.claude/hooks/session-start.sh` looks an entry up by filename — the resolved
# login, lowercased, plus `.md`. Nothing imports the directory, so a file the
# lookup cannot name does not degrade: it reaches no session, silently, while the
# preference it holds sits in the repo looking done. That is the failure this
# script exists to make loud.
#
# So every `*.md` here is either `default.md` (printed for everyone), `README.md`
# (the format, read by people rather than the hook), or `<handle>.md` where the
# handle is lowercase and otherwise a legal GitHub handle. Uppercase is the one
# that bites without looking wrong, GitHub being case-insensitive about handles
# where the filesystem is not.
#
# There is nothing else to check. An entry's content is its whole file, so it has
# no syntax to violate — which is why this script is short and why the directory
# is shaped this way.
#
# Passes quietly when the directory is absent: a project that keeps no operator
# entries has nothing to check.
#
# Reports every failure rather than stopping at the first.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

OPERATORS=".claude/skills/plainly/operators"
failures=0

fail() {
  printf '  ✗ %s\n' "$*" >&2
  failures=$((failures + 1))
}

if [ ! -d "$OPERATORS" ]; then
  echo "check-operator-entries: no $OPERATORS/ — nothing to check."
  exit 0
fi

echo "1. Every entry filename is a handle the hook can look up"

shopt -s nullglob
for path in "$OPERATORS"/*; do
  name="$(basename "$path")"

  case "$name" in
    README.md|default.md) continue ;;
  esac

  if [ -d "$path" ]; then
    fail "$path: a directory; entries are flat files, and the hook will not find this"
    continue
  fi

  case "$name" in
    *.md) ;;
    *) fail "$path: not a \`.md\` file, so no login will ever name it"; continue ;;
  esac

  handle="${name%.md}"
  if [[ ! "$handle" =~ ^[a-z0-9](-?[a-z0-9])*$ ]]; then
    fail "$path: \`$handle\` is not a lowercase GitHub handle, so the hook's lookup misses it"
  fi
done

echo
if [ "$failures" -gt 0 ]; then
  echo "check-operator-entries: $failures problem(s)" >&2
  exit 1
fi

echo "check-operator-entries: OK"
