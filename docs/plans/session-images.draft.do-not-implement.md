> ⛔ **DRAFT — DO NOT IMPLEMENT.** This plan is not approved. Do not edit source while this file is named `*.draft.do-not-implement.md` — prep and spikes go in `tmp/`. On an explicit operator go-ahead, `git mv` it to `*.in-progress.md` and delete this banner (quoting the go-ahead in the commit) *before* touching code.

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
   and on `Stop`, so extraction needs no agent discipline.
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
   - On `Stop`, also commit what the script wrote, restricted to the output
     directory: `git add -- <dir> && git commit -- <dir>`. Guards: skip when `HEAD`
     is detached, when a merge or rebase is in progress, or when the directory has
     no changes.
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

6. **Guard the dangling reference.** `/finalize` sweeps
   `docs/remove-before-merging/` wholesale, so prose that lands while pointing into
   `session-images/` ships a broken link. Add one clause to `/finalize` step 6,
   before the sweep: grep the tree for references into the directory and promote or
   repoint what is still needed.

7. **Catalog rows** in `.claude/skills/sync-agent-infra/catalog.md`: the script and
   the hook into G4 (remote-session plumbing), `scripts/lib/media.py` into G2
   alongside `scripts/lib/github.py`, and the `docs/remove-before-merging/*` row
   under "Never" updated to name session images beside the squash-message draft.
   Update the `.claude/settings.json` row, which currently names only the
   SessionStart and UserPromptSubmit hooks.

8. **Vet and finalize** — `./scripts/vet.sh` covers the catalog assertion, so a
   missing row fails there rather than downstream.

## Open questions

Each carries a recommendation, and the plan above is written with the
recommendation already in force — so silence is a valid answer and the work is
implementable as written.

**1. What commits the extracted files?** They only survive the VM once they are
committed and pushed.

- **(a) — recommended.** Extract on `UserPromptSubmit` (for the in-turn context)
  and extract-plus-commit on `Stop`, the commit restricted to the output directory.
  The turn cannot end with the image uncommitted. Residual: the commit is local
  until the agent's next push, so a session that dies between the two still loses
  it — narrow, and the existing "commit and push proactively" convention closes it
  in practice.
- **(b)** Hooks extract only; the agent commits as part of its normal flow. Simpler,
  but it reintroduces the agent discipline this exists to remove — a turn that
  makes no commit (a pure question, like the one that raised this) leaves the file
  to die with the VM.
- **(c)** The `Stop` hook commits *and* pushes. Closes the residual window, but a
  hook that pushes publishes whatever else the branch has committed, at a moment
  nobody chose. Recommend against.

**2. Does this run on the local CLI too, or only in remote sessions?** The other
two hooks no-op unless `$CLAUDE_CODE_REMOTE` is set.

- **(a) — recommended.** Run everywhere. The loss is a property of the transcript,
  not of the agent proxy, and a local session attaches images the same way. The
  cost on a laptop is one `jq` and one short file scan per prompt.
- **(b)** Gate it remote-only for consistency with the neighbours. Consistent, but
  it withholds the feature from the sessions where the operator could most easily
  have used it.

**3. Should anything mechanical catch a reference into `session-images/` that
outlives the sweep?**

- **(a) — recommended.** Prose only: the `/finalize` clause in step 6, plus the
  CLAUDE.md convention. The sweep already has a human-shaped step around it.
- **(b)** A check in `scripts/vet.sh` that fails when a file outside
  `docs/remove-before-merging/` references a path inside it. Catches it earlier, but
  vet runs long before the sweep, when the reference is legitimate — it would fire
  on every branch that is using the mechanism correctly.

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
