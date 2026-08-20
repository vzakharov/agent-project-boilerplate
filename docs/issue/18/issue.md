# Issue #18: export-github-item.py and pr-body.py duplicate their GitHub plumbing byte-for-byte

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/issues/18
- **Author:** @vzakharov
- **Created:** 2026-08-20T23:22:53Z
- **Updated:** 2026-08-20T23:22:53Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

`scripts/export-github-item.py` and `scripts/pr-body.py` each carry their own copy of `die`, `gh_token` and `detect_origin_repo`. All three are **byte-identical** between the two files — 26 lines total.

Each encodes a rule that has to change in both places to stay correct:

- `gh_token` — the resolution order (`$GH_TOKEN` → `$GITHUB_TOKEN` → `gh auth token`) and the three distinct failure messages.
- `detect_origin_repo` — the regex for which `origin` URL shapes count as GitHub (`https://` and `git@`, optional `.git`, optional trailing slash).
- `die` — trivial on its own, but it is what the other two call.

That makes this real coupling rather than incidental resemblance: a token lane added in one script and not the other is a silent inconsistency, and the shapes `detect_origin_repo` accepts are exactly the kind of thing that gets extended once and forgotten.

## Suggested shape

A `scripts/lib/github.py` holding the three functions, imported as:

```python
from lib.github import detect_origin_repo, die, gh_token
```

The import mechanism is worth being deliberate about: a script run as `python3 scripts/<name>.py` puts `scripts/` on `sys.path[0]`, so `lib.github` resolves as a PEP 420 namespace package **from any working directory**. That property is load-bearing here — both scripts write output relative to the caller's cwd while living elsewhere, and `export-github-item.py` is routinely run against a checkout other than the one it sits in (`--repo`). No `__init__.py` and no `sys.path` manipulation needed.

`scripts/lib/` already exists for the shell equivalent (`watch-tick-common.sh`), so this follows the convention rather than inventing one.

Worth leaving *out* of the shared module: each script's `USER_AGENT` (they differ, deliberately — it is how the two are told apart server-side) and the `DOCS_*_ROOT` constants (`DOCS_ISSUE_ROOT` is single-use, and splitting the pair so one comes from a shared module while its sibling stays local costs a reader more than the one duplicated line saves).

## Why I'm filing rather than just carrying it

Done downstream in [vzakharov/vovazakharov.com#5](https://github.com/vzakharov/vovazakharov.com/pull/5) — 73 lines removed, 4 added, with both scripts exercised afterward (issue export with attachments, PR export, `pull`/`push` round-trip, the token-less and usage failure paths, and a run from a foreign cwd to confirm the import resolves).

But it forks both files from this repo, so every future `/sync-upstream` on either turns from a clean copy into a manual merge. Applying it here instead converges them again. Happy to open a PR with the patch.

Note this repo's copies also still have the attachment-download bug in #17 — worth fixing that first or together, since both touch `export-github-item.py`.

---


