# Persist operator-attached images from the session transcript

## The problem

An image the operator attaches to a session reaches the agent as base64 inside the
message — no file is written. It lives in exactly one place on the VM: the session
transcript at the `transcript_path` every hook is handed. The VM is ephemeral, so
when the session ends the image is gone, and the next session has no way to see
what the operator pointed at.

The workarounds in use today both route the image out of the session and back in:
attach it to a PR comment so `scripts/export-github-item.py` can pull it down, or
commit it from a local machine. Both need the operator to do the round trip by
hand, in a different tool, for something they already sent.

## What lands

An image the operator attaches is on the branch as a file, with enough context
recorded that a later session knows what it was. Nothing that costs the operator
an extra step.

1. **`scripts/extract-session-images.py`** — reads a transcript, writes every
   operator-attached image it has not already written to
   `docs/remove-before-merging/session-images/`, and appends a row per image to
   `index.md` there. Idempotent: re-running writes nothing new.
2. **`.claude/hooks/session-images.sh`** — runs that script on `UserPromptSubmit`
   and on `Stop`, so extraction needs no agent discipline, and in a remote
   session commits what it wrote.
3. **A CLAUDE.md convention** saying what the extracted files are for and what
   the agent does with one worth keeping.
4. **Catalog rows** so the mechanism reaches adopters intact.

## What the transcript actually holds

Established by reading this session's own transcript; recorded so it is not
re-derived.

An operator attachment is a record with `type: "user"` and `origin.kind: "human"`,
whose `message.content` is a list carrying a top-level
`{"type": "image", "source": {"type": "base64", "media_type": …, "data": …}}`
block alongside the prompt text.

Three things look like it and are not:

- **The agent's own `Read` of an image file** also lands under `type: "user"`, but
  the image block is nested inside a `tool_result` and the record has no
  `origin` key. Extracting these would re-commit files the repo already has.
- **Subagent turns** carry `isSidechain: true`.
- **`queue-operation` records** carry the prompt text but never the image data, so
  they are not a second source to reconcile against.

So the filter is `type == "user"` and `origin.kind == "human"` and
`isSidechain` falsy, over top-level `image` blocks only.

Each such record also carries `uuid`, `timestamp`, `sessionId`, `promptId` and
`gitBranch` — enough for a deterministic filename and a manifest row, with no
separate state file to keep in sync.

## Steps

1. **Move `extension_for_bytes` to `scripts/lib/media.py`** and repoint
   `scripts/gh_export/attachments.py` at it. It maps a content type to a file
   extension and sniffs magic bytes when the type is missing or wrong — the same
   job on both sides. See DRY notes for why it moves rather than being imported
   where it sits.

2. **Write `scripts/extract-session-images.py`** (stdlib only, Python 3.9+, matching
   the other scripts):

   - Usage: `python3 scripts/extract-session-images.py <transcript.jsonl> [--out <dir>]`,
     defaulting to `docs/remove-before-merging/session-images/`.
   - Parse line by line, skipping unparseable lines rather than failing — a
     transcript is appended to while the script reads it.
   - Filter as above. Name each file `<UTC timestamp>-<first 8 of uuid><ext>`, e.g.
     `20260911T124355Z-cb565b80.jpg`, so the name is derived from the record and a
     re-run recomputes the same one.
   - Skip an image whose SHA-256 is already in the manifest, so the same screenshot
     sent twice is one file.
   - Append to `index.md`: filename, UTC timestamp, size, the branch the record
     names, and the first ~200 characters of the prompt text that accompanied it.
     The text is what makes the image legible to a session that was not there.
   - Print one line per newly written file and nothing when there is nothing new,
     so the hook's output is silent in the common case.
   - Exit non-zero only on an unreadable transcript or an unwritable output
     directory. A transcript with no images is success.

3. **Write `.claude/hooks/session-images.sh`**, wired in `.claude/settings.json` on
   both `UserPromptSubmit` and `Stop`:

   - Read `transcript_path` and `cwd` from the hook's stdin JSON with `jq`, matching
     `.claude/hooks/plan-mode-notice.sh`.
   - Run the script. On `UserPromptSubmit`, when files were written, emit
     `hookSpecificOutput.additionalContext` naming them, so the agent can reference
     the path in the same turn.
   - On `Stop`, **in a remote session only** (`$CLAUDE_CODE_REMOTE`), also commit
     what the script wrote, restricted to the output directory:
     `git add -- <dir> && git commit -- <dir>`. Guards: skip when `HEAD` is
     detached, when a merge or rebase is in progress, or when the directory has no
     changes.
   - Never fail the turn. A hook that breaks a session over a screenshot is worse
     than a lost screenshot, so every failure path is a message on stderr and
     `exit 0`.

4. **Verify the `UserPromptSubmit` timing.** Whether the current message is in the
   transcript when that hook fires is not settled by reading — the records are
   appended around prompt submission and the ordering is not documented. The `Stop`
   trigger makes the answer not matter for persistence, but it decides whether the
   in-turn context of step 3 names the image just sent or the one before it. Test
   it by logging the transcript's line count and the presence of the current
   `user_input` from inside the hook, then sending one prompt. Record the answer in
   the hook's header comment.

5. **Add the CLAUDE.md convention** — a short paragraph under "Writing things down"
   or its own heading: extracted images are working artifacts under a tree that
   never lands; an image worth keeping is `git mv`'d to a permanent home and
   referenced from the prose that needs it; the rest go with the tree at
   `/finalize`.

6. **Catalog rows** in `.claude/skills/sync-agent-infra/catalog.md`: the script and
   the hook into G4 (remote-session plumbing), `scripts/lib/media.py` into G2
   alongside `scripts/lib/github.py`, and the `docs/remove-before-merging/*` row
   under "Never" updated to name session images beside the squash-message draft.
   Update the `.claude/settings.json` row, which currently names only the
   SessionStart and UserPromptSubmit hooks.

7. **Vet and finalize** — `./scripts/vet.sh` covers the catalog assertion, so a
   missing row fails there rather than downstream.

## Settled decisions

**The `Stop` firing commits, and that is what makes the mechanism work.** The
alternative — hooks extract, the agent commits in its normal flow — reintroduces
exactly the discipline this exists to remove: a turn that makes no commit, a pure
question being the common case, leaves the file to die with the VM. The hook does
not push: a hook that pushes publishes whatever else the branch has committed, at
a moment nobody chose. So the commit is local until the agent's next push, and the
existing "commit and push proactively" convention closes that window.

**Extraction runs everywhere; the commit is gated to remote sessions.** The loss
is a property of the transcript, not of the agent proxy, so a laptop session needs
the extraction as much as a web one — the cost there is one `jq` and one short file
scan per prompt. The commit is a different question, and the answer is where the
repo already commits: CLAUDE.md scopes proactive committing to remote sessions
because that is where the operator watches from another machine. Locally they are
looking at the tree itself, so the file in `git status` is the whole signal, and a
commit appearing unbidden on whatever branch they happen to be standing on is not.

**Nothing mechanical guards a reference that outlives the `/finalize` sweep.**
Prose that lands while pointing into `docs/remove-before-merging/` ships a broken
link, but that is true of everything the tree holds, not of screenshots — so it is
its own problem, handled separately rather than bolted onto this one.

## DRY notes

**`extension_for_bytes` is genuinely shared, and moves.** `scripts/gh_export/attachments.py`
already maps a content type to an extension and falls back to sniffing magic bytes;
the new script needs exactly that, over `media_type` from the transcript instead of
a `Content-Type` header. Importing it where it sits would work — running
`python3 scripts/<file>.py` puts `scripts/` on `sys.path[0]`, so `gh_export`
resolves — but it would make a G4 hook depend on G3's exporter, and an adopter who
takes the hooks without the issue loop would get an `ImportError` on every prompt.
Moving it to `scripts/lib/media.py`, beside the existing `scripts/lib/github.py`,
keeps one copy and leaves each group standing on its own.

**Nothing else is shared with the GitHub exporter, and forcing more would be
net-negative.** `gh_export/attachments.py` discovers URLs in Markdown and fetches
them over an authenticated HTTP ladder; this script decodes base64 out of a local
JSONL. The words "attachment" and "download" are the overlap; the mechanism is not.
A common abstraction over the two would have a URL-or-not branch running through
every function.

**No new skill.** The mechanism is a hook and a script, with the agent-facing
half being one CLAUDE.md convention. A skill would add a catalog row, a `SKILL.md`
to keep in sync, and a slash command nobody has occasion to type — the extraction
is meant to happen without being invoked.

**The manifest is the state file.** Filenames are derived from the record's own
`timestamp` and `uuid`, and dedupe reads the hashes already in `index.md`, so there
is no second file recording what has been extracted and no way for the two to drift.

## Risks

- **A transcript read mid-write** yields a truncated last line. Handled by skipping
  unparseable lines; the record is caught on the next firing.
- **A large attachment** goes onto the branch as a blob. The squash merge means it
  never reaches the trunk, and `/finalize` deletes the tree before that, so the cost
  is branch size during review. The manifest records each file's size so an
  outsized one is visible.
- **The record shape is undocumented** and belongs to the client, not to this repo.
  If it changes, the filter matches nothing and the script exits 0 — the failure is
  silent, the way it was before this existed, rather than noisy. A `--verbose` flag
  that reports what it saw and rejected makes the diagnosis one command.
