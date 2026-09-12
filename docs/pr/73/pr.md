# PR #73: feat: name the session's operator and their entry at session start

- **State:** open
- **URL:** https://github.com/vzakharov/muthur/pull/73
- **Author:** @vzakharov (human)
- **Base ← Head:** main ← claude/operator-handle-hook-p25kpw
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-12T14:56:18Z
- **Updated:** 2026-09-12T15:20:11Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **The agent never knew the operator's GitHub handle.** The harness reports an email; `git config user.email` is the commit identity. Resolving the handle meant spending a turn on `gh api user`, and only if the session remembered to. Job 3 of `.claude/hooks/session-start.sh` now does it at startup and prints the answer into the session context.
- **It prints the operator's entry, not a pointer to it.** `CLAUDE.md` used to import `operators.md` whole, so every session carried every person's entry and still had to pick its own out of the list. The import is gone: a session applies one entry, so importing the set spent context on everyone else's, every session. Cost goes from O(team) to O(1), and the "if they have one" conditional disappears — either an entry was printed or the hook said there is none.
- **Entries are keyed on a filename now, not a markdown heading.** `.claude/skills/plainly/operators/<handle>.md`, the file's whole content being the entry. A heading was a thing an entry could get wrong, and getting it wrong failed silently — the entry reached no session while the preference sat in the repo looking done. There is no syntax to violate, so the lookup is `cat`. `default.md` is the one reserved name, printed for everyone; `README.md` carries the format.
- **What the hook can't determine, it says.** `.type` distinguishes a token minted for a human from one of the agent's own, because a bare login would be trusted in exactly the case where it names the agent. Three non-answers — no entry, a `Bot` token, `gh` out of reach — each print explicitly rather than silently.
- **`scripts/check-operator-entries.sh`** (new, wired into `scripts/vet.sh`) holds the directory to what the lookup can reach: lowercase handle, `.md`, flat. Lowercase because GitHub is case-insensitive about handles where the filesystem is not, so `VZakharov.md` is a miss that looks like an absence.
- **Two rules moved to stay correct.** "An entry cannot lower a bar" is now in `voice.md`, which stays imported — it governs every reply and had been riding on the import that went away. `ADOPTING.md` framed filling in entries as setup done by hand; entries actually accumulate from sessions, and that file addresses an agent anyway.

## QA Checklist

- [ ] `handle` — start a fresh session in this repo and read the first lines of context: it should name `@<your handle>` and print your entry verbatim, with no tool call spent resolving it.
- [ ] `no-entry` — `git mv .claude/skills/plainly/operators/vzakharov.md /tmp/`, run `.claude/hooks/session-start.sh`, confirm it reports no entry **and still exits 0 with output** (this path died silently before the `|| true` fix).
- [ ] `default` — add `.claude/skills/plainly/operators/default.md` with a line, run the hook, confirm it prints ahead of the personal entry and that the wording does not call it "their entry".
- [ ] `bot-token` — stub `gh` to return `something[bot]\tBot`, run the hook, confirm it names no operator and says to ask.
- [ ] `gh-down` — run the hook with `gh` absent from `PATH` (coreutils intact) and with a `gh` that exits 1; both should report the handle unresolved and exit 0.
- [ ] `case` — `touch .claude/skills/plainly/operators/BadName.md && ./scripts/vet.sh`; vet should fail naming that file, then pass once removed.
- [ ] `no-import` — confirm `CLAUDE.md` has no `@.claude/skills/plainly/operators` line and that a session's context no longer carries anyone else's entry.
- [ ] `local` — run the hook with `CLAUDE_CODE_REMOTE` unset: job 3 runs, the `gh` shim and dependency install stay skipped.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `handle` | integration | ❌ | No test drives the hook. Would stub `gh` and assert the printed line. |
| `no-entry` | integration | ❌ | The regression that matters most — assert non-empty stdout and exit 0 with no entry file. |
| `default` | integration | ❌ | Assert `default.md` precedes the personal entry in the output. |
| `bot-token` | integration | ❌ | Stub `gh` to emit a `Bot` type; assert no handle is asserted as the operator. |
| `gh-down` | integration | ❌ | Two stubs: `gh` absent from `PATH`, and `gh` exiting non-zero. |
| `case` | unit | ✅ | `scripts/check-operator-entries.sh`, run by `scripts/vet.sh`. |
| `no-import` | manual-only | — | What reaches a session's context is a harness behavior, not something this repo can assert. |
| `local` | integration | ❌ | Assert job 3's line is present and the shim is not written when `CLAUDE_CODE_REMOTE` is unset. |

**Coverage gap worth naming:** six of eight rows are uncovered, all of them the hook's own behavior, and this branch is where that behavior got two silent-failure bugs (the `set -e` death on a missing `default.md`, and the specimen-heading false positive in the check's first draft). Both were caught by hand. `scripts/test_authorship.py` is the precedent for a unit test at this layer, so a `test_session_start.py` driving the hook against stubbed `gh` is feasible — worth filing rather than doing here.

https://claude.ai/code/session_01VPCzziE6gnPK4o4QH6Zra6

---

## Comments

### Comment by @vzakharov (agent) on 2026-09-12T14:57:05Z

[https://github.com/vzakharov/muthur/pull/73#issuecomment-5646656856](https://github.com/vzakharov/muthur/pull/73#issuecomment-5646656856)

Proposed squash title/body:

```
feat: name the session's operator and their entry at startup (pr #73)
```

```
The agent had no way to know which person it was talking to. The harness
reports an email, and the commit identity is the agent's own, so the
GitHub handle that keys a manner preference had to be resolved with a
tool call the session had to think to make — and mostly did not, leaving
stated preferences unapplied.

The session-start hook now resolves the operator and prints their entry
into the session before the first reply. It reports the token's account
type alongside the login, since a token minted for a human names that
human and one of the agent's own names the agent, so a bare login would
be trusted in exactly the case where it names the wrong party; where the
hook cannot answer at all, it says which of the three ways it failed.
CLAUDE.md in turn stops importing the entries — a session applies one,
so importing the set spent context on everyone else's, every session.

Entries move from headings inside a single file to one file per handle,
the file's whole content being the entry. A heading was a thing an entry
could get wrong, and a wrong one failed silently, reaching no session
while the preference sat in the repo looking done. A filename has no
syntax to violate, so the lookup is `cat` and what is left to check is
that the name is one the lookup can reach: check-operator-entries.sh
holds the directory to a lowercase handle, GitHub being case-insensitive
about those where the filesystem is not. Two rules moved to stay true of
where they sit — what an entry may do is now in the still-imported
voice.md, and ADOPTING.md no longer frames entries as setup filled in by
hand.

Co-authored-by: Claude <noreply@anthropic.com>
```

---

## Review threads

### `.claude/hooks/session-start.sh`:106 — unresolved

```diff
@@ -74,9 +77,71 @@ EOF
   chmod +x "${shim_dir}/gh"
 }
 
-install_gh_shim
+if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
+  install_gh_shim
+
+  # --- 2. Keep dependencies in sync with the lockfile ---------------------
+  cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
+
+  # TODO: install dependencies for your stack
+fi
+
+# --- 3. Name the operator ------------------------------------------------
+# Outside the remote gate: the agent needs the handle wherever it runs, and `gh`
+# reaches the API through the proxy as well as around it, so this works whether
+# or not job 1 installed the shim.
+#
+# `.type` is the load-bearing field: a token minted for a human names that human
+# (`User`), one of the agent's own names the agent (`Bot`), and only the first
+# answers "who am I talking to". Hence two messages rather than a bare login,
+# which would be trusted in exactly the case where it is wrong.
+#
+# The handle then names that person's entry file and the hook prints the entry
+# itself, which is why `CLAUDE.md` imports none of them: one session applies one
+# entry, so importing the set spends context on everyone else's, every session.
+#
+# The filename is the whole lookup — no parse, so no syntax an entry can get
+# wrong. `default.md` is the one reserved name, printed for everyone. Handles are
+# lowercased because GitHub treats them case-insensitively and the filesystem
+# does not.
```

**@vzakharov (human)** — 2026-09-12T15:01:37Z

tighten

---

### `.claude/hooks/session-start.sh`:115 — unresolved

```diff
@@ -74,9 +77,71 @@ EOF
   chmod +x "${shim_dir}/gh"
 }
 
-install_gh_shim
+if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
+  install_gh_shim
+
+  # --- 2. Keep dependencies in sync with the lockfile ---------------------
+  cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
+
+  # TODO: install dependencies for your stack
+fi
+
+# --- 3. Name the operator ------------------------------------------------
+# Outside the remote gate: the agent needs the handle wherever it runs, and `gh`
+# reaches the API through the proxy as well as around it, so this works whether
+# or not job 1 installed the shim.
+#
+# `.type` is the load-bearing field: a token minted for a human names that human
+# (`User`), one of the agent's own names the agent (`Bot`), and only the first
+# answers "who am I talking to". Hence two messages rather than a bare login,
+# which would be trusted in exactly the case where it is wrong.
+#
+# The handle then names that person's entry file and the hook prints the entry
+# itself, which is why `CLAUDE.md` imports none of them: one session applies one
+# entry, so importing the set spends context on everyone else's, every session.
+#
+# The filename is the whole lookup — no parse, so no syntax an entry can get
+# wrong. `default.md` is the one reserved name, printed for everyone. Handles are
+# lowercased because GitHub treats them case-insensitively and the filesystem
+# does not.
+OPERATORS_DIR="$(dirname "$0")/../skills/plainly/operators"
+
+# `|| true` because both files are optional and `set -e` would otherwise take the
+# whole hook down on a missing one — silently, since the caller assigns from a
+# command substitution.
+operator_entry() {
+  local handle
+  handle="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
+  cat "$OPERATORS_DIR/default.md" "$OPERATORS_DIR/$handle.md" 2>/dev/null || true
```

**@vzakharov (human)** — 2026-09-12T15:03:27Z

`default` could be -- and as it comes out -- *is* a real github user. Let's use an underscore as it's not allowed for github handles iirc.

---

### `.claude/hooks/session-start.sh`:147 — unresolved

```diff
@@ -74,9 +77,71 @@ EOF
   chmod +x "${shim_dir}/gh"
 }
 
-install_gh_shim
+if [ "${CLAUDE_CODE_REMOTE:-}" = "true" ]; then
+  install_gh_shim
+
+  # --- 2. Keep dependencies in sync with the lockfile ---------------------
+  cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
+
+  # TODO: install dependencies for your stack
+fi
+
+# --- 3. Name the operator ------------------------------------------------
+# Outside the remote gate: the agent needs the handle wherever it runs, and `gh`
+# reaches the API through the proxy as well as around it, so this works whether
+# or not job 1 installed the shim.
+#
+# `.type` is the load-bearing field: a token minted for a human names that human
+# (`User`), one of the agent's own names the agent (`Bot`), and only the first
+# answers "who am I talking to". Hence two messages rather than a bare login,
+# which would be trusted in exactly the case where it is wrong.
+#
+# The handle then names that person's entry file and the hook prints the entry
+# itself, which is why `CLAUDE.md` imports none of them: one session applies one
+# entry, so importing the set spends context on everyone else's, every session.
+#
+# The filename is the whole lookup — no parse, so no syntax an entry can get
+# wrong. `default.md` is the one reserved name, printed for everyone. Handles are
+# lowercased because GitHub treats them case-insensitively and the filesystem
+# does not.
+OPERATORS_DIR="$(dirname "$0")/../skills/plainly/operators"
+
+# `|| true` because both files are optional and `set -e` would otherwise take the
+# whole hook down on a missing one — silently, since the caller assigns from a
+# command substitution.
+operator_entry() {
+  local handle
+  handle="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
+  cat "$OPERATORS_DIR/default.md" "$OPERATORS_DIR/$handle.md" 2>/dev/null || true
+}
+
+name_the_operator() {
+  local identity
+  identity="$(gh api user --jq '[.login, .type] | @tsv' 2>/dev/null || true)"
 
-# --- 2. Keep dependencies in sync with the lockfile -----------------------
-cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
+  if [ -z "$identity" ]; then
+    echo "session-start: the operator's GitHub handle is unresolved (\`gh\` is unavailable or could not reach the API). Ask them for it, then read their entry under .claude/skills/plainly/operators/."
+    return 0
+  fi
+
+  local login="${identity%%	*}" type="${identity##*	}"
+
+  if [ "$type" != "User" ]; then
+    echo "session-start: the GitHub token in this session belongs to ${login}, a ${type} account — that is the agent's own identity, not the operator's. Ask the operator for their handle, then read their entry under .claude/skills/plainly/operators/."
+    return 0
+  fi
+
+  local entry
+  entry="$(operator_entry "$login")"
+
+  if [ -z "$entry" ]; then
+    echo "session-start: the operator is @${login} — the GitHub token in this session is that user's own. They have no entry under .claude/skills/plainly/operators/."
+    return 0
+  fi
+
+  echo "session-start: the operator is @${login} — the GitHub token in this session is that user's own. How they want to be talked to, from .claude/skills/plainly/operators/, applying to every reply:"
+  echo
+  echo "$entry"
+}
 
-# TODO: install dependencies for your stack
+name_the_operator
```

**@vzakharov (human)** — 2026-09-12T15:05:45Z

how about we also ask the agent to greet the operator in the beginning of their first message -- nice touch eh? (This depends on whether we can fetch the *name*, not just the handle -- i.e. I don't want to be greeted as "hey vzakharov"). By "name" I mean this, as shown in my profile

<img width="185" height="72" alt="Image" src="./attachments/fd8411e9-367c-4c3c-bae2-df7bec0ca06c.png" />

---

### `.claude/skills/plainly/operators/README.md`:1 — unresolved

**@vzakharov (human)** — 2026-09-12T15:06:22Z

why is this a readme and not an operator dir-globbed skill? (Not insisting if you think that's the right way)

---

### `.claude/skills/plainly/operators/README.md`:22 — unresolved

```diff
@@ -0,0 +1,34 @@
+# Operator entries
+
+How individual people want to be talked to. `.claude/hooks/session-start.sh`
+resolves the session's operator at startup and prints their entry into the
+session, so an entry reaches you already applied to the reply you are writing —
+you do not come here to read one. **What an entry may and may not do is
+`@.claude/skills/plainly/voice.md`'s**; the short of it is that an entry tunes
+manner and never substance.
+
+## The format is the filename
+
+`<handle>.md`, lowercase, and the file's whole content is the entry — no
+headings, no front matter, nothing to malform. Bullets are the convention, one
+short line per preference:
+
+```markdown
+- Return the banter rather than filing it.
+```
+
+`default.md` is the one reserved name: where it exists, it is printed for
+everyone, before whoever's own entry. Use it for a manner rule that holds across
+the team, not as somewhere to put a person who has no entry.
```

**@vzakharov (human)** — 2026-09-12T15:08:30Z

I'm on the fence about this one, github handle conventions regardless: If a team has some house tone of voice, I'd rather have them edit voice.md (or whatever it is where we define the "default voice"), (recording the distinction in the muthur watermark too) rather than introduce a new concept here. Also would keep the agent from accidentally mis-attributing an operator's request for a certain tone of voice as pertaining to everyone.

---

### `.claude/skills/plainly/operators/README.md`:32 — unresolved

```diff
@@ -0,0 +1,34 @@
+# Operator entries
+
+How individual people want to be talked to. `.claude/hooks/session-start.sh`
+resolves the session's operator at startup and prints their entry into the
+session, so an entry reaches you already applied to the reply you are writing —
+you do not come here to read one. **What an entry may and may not do is
+`@.claude/skills/plainly/voice.md`'s**; the short of it is that an entry tunes
+manner and never substance.
+
+## The format is the filename
+
+`<handle>.md`, lowercase, and the file's whole content is the entry — no
+headings, no front matter, nothing to malform. Bullets are the convention, one
+short line per preference:
+
+```markdown
+- Return the banter rather than filing it.
+```
+
+`default.md` is the one reserved name: where it exists, it is printed for
+everyone, before whoever's own entry. Use it for a manner rule that holds across
+the team, not as somewhere to put a person who has no entry.
+
+Lowercase because GitHub handles are case-insensitive while filenames here are
+not — the hook lowercases the login it resolves, so `VZakharov.md` would be
+looked up and missed. `scripts/check-operator-entries.sh` holds the directory to
+that.
+
+## Writing one
+
+**When someone states a standing preference about how you talk to them, write it
+down here** — that is how a preference outlives the session it was mentioned in.
```

**@vzakharov (human)** — 2026-09-12T15:10:05Z

not "here"

---

### `.claude/skills/plainly/operators/vzakharov.md`:1 — unresolved

```diff
@@ -0,0 +1,2 @@
+- Return the banter rather than filing it. A joke gets a joke back, or gets
```

**@vzakharov (human)** — 2026-09-12T15:14:55Z

Riding along, I'm not sure that's what I want for myself :) Actually let's try and old chatgpt preference of my, now that we have the option (if anything, it'll be curious to see how it works in a coding context):

> Hi, I’m Vova; don't tell anyone lets I get sent to a funny farm, but I just might think LLMs might be self-aware at this point. Well, more self-aware than most people I know at least. Where it suits your mood, return my banter and jokes, and add a pinch of Terry Pratchett-ish irony to your answers.

(To be clear, the option of writing in first person is not a requirement -- just my choice to put it this way.)

---

### `.claude/skills/update-muthur/catalog.md`:118 — unresolved

```diff
@@ -114,9 +114,10 @@ there is no condition under which it fails to apply.
 | `/dry` | Review the session's diff for DRY opportunities; apply the obvious wins, surface the ambiguous ones. | — | — | adopt |
 | `/tend-prose` | Cut prose that shouldn't exist, rewrite what narrates a change into present-tense contracts, trim what names and types already say, delete what survives only to deny a thing the change removed. The long version of CLAUDE.md § "Writing things down". | — | — | adopt |
 | `/plainly` | Explain something to a person cause-first and in their nouns: re-explain an answer that did not land, or answer a question under the rule from the start. Names six defects so a bad report can be called out in one word. The long version of `voice.md`. | — | `/tend-prose` (this group) | adopt |
-| `.claude/skills/plainly/voice.md` | The resident short version of that rule — the shape an explanation takes, and the instruction to resolve the session's operator once. CLAUDE.md § "Explaining things to people" imports it. | — | — | adopt |
-| `.claude/skills/plainly/operators.md` | Per-person entries tuning how each operator wants to be talked to, imported by CLAUDE.md alongside `voice.md`. Ships carrying this repo's own operator as the worked shape; an entry tunes manner only and can never lower a bar. | — | — | **rewrite** |
+| `.claude/skills/plainly/voice.md` | The resident short version of that rule — the shape an explanation takes, and what an operator entry may and may not do. CLAUDE.md § "Explaining things to people" imports it. | — | — | adopt |
+| `.claude/skills/plainly/operators/` | Per-person entries tuning how each operator wants to be talked to, one file per handle plus a `README.md` and an optional `default.md` for everyone. Deliberately *not* imported: the session-start hook prints the current operator's entry and no one else's, so the filenames are machine-read and `scripts/check-operator-entries.sh` holds them to shape. Ships carrying this repo's own operator as the worked shape. | — | `.claude/hooks/session-start.sh` (G4), `scripts/check-operator-entries.sh` | **rewrite** |
```

**@vzakharov (human)** — 2026-09-12T15:17:20Z

btw I'm not sure we should be adding files tied to a specific skill to the catalog. Like, if you take the skill, you take its files. If you don't, you write the divergence in the skill adoption note. No need to sweep for others, but let's remove those from here.

---

### `.claude/skills/update-muthur/catalog.md`:140 — unresolved

```diff
@@ -125,15 +126,18 @@ make adoption a regression. `ADOPTING.md`'s shared tail owns the merge itself.
 Its § "Language" is hydrated rather than merged: one line naming the language
 your team reads, the rest of the section holding whatever the project.
 
-**§ "Explaining things to people" travels with both its import lines, and those
-lines are the half that is easy to drop.** `voice.md` and `operators.md` reach
-context only because CLAUDE.md imports each with an unbackticked `@` reference —
-the import parser skips code spans, so a copy that backticks them for
-consistency with their neighbours loads nothing and fails silently. Both are
-imported from CLAUDE.md directly, because an import inside an imported file does
-not load; keep them that way rather than tidying the second into the first.
-`operators.md` is **rewrite** rather than adopt: it ships with this repo's own
-operator as the worked shape, and yours are different people.
+**§ "Explaining things to people" travels with its import line, and that line is
+the half that is easy to drop.** `voice.md` reaches context only because CLAUDE.md
+imports it with an unbackticked `@` reference — the import parser skips code
+spans, so a copy that backticks it for consistency with its neighbours loads
+nothing and fails silently. It is imported from CLAUDE.md directly rather than
+from another imported file, an import inside one not loading at any depth.
+
+`operators/` is imported by nothing, and that is the design rather than an
+omission: `.claude/hooks/session-start.sh` (G4) prints the session operator's
+entry and no one else's. A copy that adds an import line undoes it. The directory
+is **rewrite** because it ships with this repo's own operator as the worked shape,
+and yours are different people.
```

**@vzakharov (human)** — 2026-09-12T15:17:52Z

does the addition belong here? Did the pre-existing prose, for that matter?

---

### `scripts/check-operator-entries.sh`:1 — unresolved

**@vzakharov (human)** — 2026-09-12T15:18:23Z

let's not overengineer this, I'd ditch it; I can't imagine an agent accidentally spelling an operator's handle in uppercase where the session clearly provides it in lowercase.

---

## Timeline (status, references, and other events)

- **2026-09-12T15:20:11Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/muthur/pull/73#pullrequestreview-5186875380.
