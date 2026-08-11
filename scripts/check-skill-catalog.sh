#!/bin/bash
# Assert the skill cross-reference and catalog invariants.
#
#   1. Every `@.claude/skills/<name>/SKILL.md` reference resolves to a file that
#      exists. This is the check that makes subset-copying safe: a skill copied
#      without its closure leaves a pointer that fails *silently* — the agent
#      follows the surviving prose and skips the step it could not load.
#   2. Every `.claude/skills/*/` directory has exactly one row in
#      `docs/catalog.md`.
#   3. Every path named in a catalog row's first column exists.
#
# Assertions 2-3 skip when `docs/catalog.md` is absent, which is the normal
# downstream case — the catalog describes the source repo and is never vendored.
# So the same script is useful at every link in the adoption chain.
#
# Run it when adding, renaming or removing a skill. Exits non-zero on any
# failure, listing every one rather than stopping at the first.

set -uo pipefail

cd "$(dirname "$0")/.." || exit 1

CATALOG="docs/catalog.md"
failures=0

fail() {
  printf '  ✗ %s\n' "$*" >&2
  failures=$((failures + 1))
}

# The search surface is the durable agent infrastructure: the skills and their
# config, the always-loaded conventions, the acquisition docs, the scripts.
# Working artifacts (`docs/plans/`, `docs/issue/`, `docs/pr/`) are deliberately
# outside it — they discuss references as examples rather than making them, so a
# plan quoting a placeholder skill path is not a broken link. Keep illustrative
# reference syntax out of this file too, for the same reason: it scans itself.
mapfile -t sources < <(
  {
    [ -d .claude ] && find .claude -type f \
      \( -name '*.md' -o -name '*.sh' -o -name '*.json' \) -print
    for f in CLAUDE.md README.md ADOPTING.md docs/catalog.md; do
      [ -f "$f" ] && printf '%s\n' "$f"
    done
    [ -d scripts ] && find scripts -type f \( -name '*.sh' -o -name '*.py' \) -print
  } 2>/dev/null
)

if [ ${#sources[@]} -eq 0 ]; then
  echo "check-skill-catalog: found no files to scan — wrong directory?" >&2
  exit 1
fi

# --- Assertion 1: no dangling skill reference ------------------------------

echo "1. Skill @-references resolve"

# Emit "file:referenced-skill" for every @-reference, then test each target.
while IFS= read -r hit; do
  [ -n "$hit" ] || continue
  src=${hit%%:*}
  name=${hit#*:}
  if [ ! -f ".claude/skills/$name/SKILL.md" ]; then
    fail "$src references @.claude/skills/$name/SKILL.md — no such file"
  fi
done < <(
  grep -oHE '@\.claude/skills/[a-z0-9-]+/SKILL\.md' "${sources[@]}" 2>/dev/null |
    sed -E 's|@\.claude/skills/([a-z0-9-]+)/SKILL\.md|\1|' |
    sort -u
)

# --- Assertions 2 and 3: the catalog covers the inventory -----------------

if [ ! -f "$CATALOG" ]; then
  echo "2-3. Skipped — no $CATALOG (expected downstream)"
else
  # A catalog row is a table line whose first cell is a single backticked
  # token: `/skill-name` for a skill, a repo-relative path for anything else.
  mapfile -t row_items < <(
    grep -E '^\|' "$CATALOG" |
      sed -E 's/^\| *`([^`]+)` *\|.*/\1/;t;d' |
      sort
  )

  echo "2. Every skill directory has exactly one catalog row"
  for dir in .claude/skills/*/; do
    name=$(basename "$dir")
    count=0
    for item in "${row_items[@]}"; do
      [ "$item" = "/$name" ] && count=$((count + 1))
    done
    case $count in
      1) ;;
      0) fail "/$name has no row in $CATALOG" ;;
      *) fail "/$name has $count rows in $CATALOG — groups must partition the inventory" ;;
    esac
  done

  echo "3. Every path in a catalog row exists"
  for item in "${row_items[@]}"; do
    # Globs stand for a whole tree ("docs/plans/*"); check the parent instead.
    case "$item" in
      */\*) item=${item%/\*} ;;
      *\**) continue ;;
    esac
    case "$item" in
      /*) path=".claude/skills/${item#/}" ;;  # `/skill-name`
      *) path="$item" ;;
    esac
    if [ ! -e "$path" ] && [ ! -e "${path%/}" ]; then
      fail "$CATALOG names \`$item\` — $path does not exist"
    fi
  done
fi

# --- Report ---------------------------------------------------------------

echo
if [ "$failures" -eq 0 ]; then
  echo "check-skill-catalog: OK"
  exit 0
fi
echo "check-skill-catalog: $failures failure(s)" >&2
exit 1
