#!/bin/bash
# Assert that `.claude/skills/plainly/operators.md` stays machine-readable.
#
# `.claude/hooks/session-start.sh` selects one entry out of this file by exact
# heading match and prints it into the session. Nothing imports the file, so a
# malformed heading does not degrade — the entry reaches nobody, silently, and
# the operator is talked to under the house default while their stated
# preference sits in the repo. That is the failure this script exists to make
# loud.
#
#   1. Every `###` line outside a fenced block is `### @<handle>` — `###`, one
#      space, `@`, then a GitHub handle and nothing else. This is also what
#      catches a stray `###` inside an entry body, which would end that entry
#      early and take the rest of it with it.
#   2. No handle appears twice. The hook prints the first match and stops, so a
#      second entry for the same person is dead text.
#   3. No fenced block opens below the first entry. The hook skips fences, so
#      one inside an entry swallows the rest of it. The template block sits
#      above the entries, which is why "below the first entry" is the test.
#
# Passes quietly when the file is absent: an adopting project that keeps no
# operator entries has nothing to check.
#
# Reports every failure rather than stopping at the first.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

OPERATORS=".claude/skills/plainly/operators.md"
failures=0

fail() {
  printf '  ✗ %s\n' "$*" >&2
  failures=$((failures + 1))
}

if [ ! -f "$OPERATORS" ]; then
  echo "check-operator-entries: no $OPERATORS — nothing to check."
  exit 0
fi

echo "1. Entry headings are \`### @<handle>\`"
echo "2. No handle has two entries"
echo "3. No fenced block inside an entry"

# Structural `###` lines only, mirroring the hook's fence handling so that a
# specimen heading in the template block is skipped here exactly as there.
headings="$(awk '
  /^```/ { fence = !fence; next }
  fence  { next }
  /^###/ { print NR "\t" $0 }
' "$OPERATORS")"

seen=""
while IFS=$'\t' read -r lineno text; do
  [ -n "$lineno" ] || continue

  if [[ ! "$text" =~ ^###\ @[A-Za-z0-9](-?[A-Za-z0-9])*$ ]]; then
    fail "$OPERATORS:$lineno: heading is not \`### @<handle>\`: $text"
    continue
  fi

  handle="${text#\#\#\# @}"
  case " $seen " in
    *" $handle "*) fail "$OPERATORS:$lineno: @$handle has more than one entry; the hook prints only the first" ;;
    *)             seen="$seen $handle" ;;
  esac
done <<< "$headings"

# From the fence-aware pass, not a raw grep: the template block's specimen
# heading is also `### @…`, so a grep would anchor on it and call the block's
# own closing fence a violation.
first_entry="$(printf '%s' "$headings" | head -1 | cut -f1)"
if [ -n "$first_entry" ]; then
  while IFS=: read -r lineno _; do
    [ -n "$lineno" ] && [ "$lineno" -gt "$first_entry" ] &&
      fail "$OPERATORS:$lineno: fenced block inside an entry; the hook stops reading there"
  done < <(grep -n '^```' "$OPERATORS")
fi

echo
if [ "$failures" -gt 0 ]; then
  echo "check-operator-entries: $failures problem(s)" >&2
  exit 1
fi

echo "check-operator-entries: OK"
