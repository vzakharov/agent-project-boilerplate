# PR #25: fix: route the stdlib scripts' API calls around a proxy that refuses api.github.com

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/25
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/agent-proxy-github-api-gmeg1f
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-01T23:00:47Z
- **Updated:** 2026-09-01T23:12:01Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **`export-github-item.py` and `pr-body.py` were dead in any session whose egress proxy refuses `api.github.com`.** Both reached the API through a bare `urlopen`, which honors `HTTPS_PROXY`, so Claude Code's remote-session proxy killed them on their first API call with its own synthetic 403 — independent of the URL shape, the token, and the User-Agent. The export of issue #24 on this branch was only obtainable by running the exporter under `env -u HTTPS_PROXY`.
- **The proxy-then-direct ladder already existed, scoped to attachment downloads.** It moves into `scripts/lib/github.py` (where #18 put the shared plumbing) and now serves all three call sites — the exporter's API reads, its attachment downloads, and `pr-body.py`'s REST calls — through one `fetch` helper that owns both the walk and the per-rung failure accumulation. `#22`'s accumulate discipline existed in exactly one of the three places, which is the drift already having happened once.
- **`fetch` takes a request *factory*, not a `Request`.** `ProxyHandler.proxy_open` calls `req.set_proxy(...)`, which rewrites the request's host **in place** — so a single `Request` reused across the ladder aims at the proxy on every rung, and each later route fails identically to the first. Building one per rung is what structurally keeps the direct rung direct.
- **Failure reporting splits by what the remote echoes back.** `format_route_statuses` renders statuses only, for the attachment path — S3 rejects a download by quoting the offending header, i.e. the bearer token in full. `format_route_statuses_and_bodies` adds the bodies for the API paths, where they *are* the diagnostic: the proxy's `403 "GitHub access is not enabled for this session"` followed by a real `404` reads very differently from either half alone.
- **Order is unchanged and the change is additive**: the proxy-honoring opener is still rung one, so a session where the proxy is the only route out keeps working. The cost accepted is that a genuine error now makes each request twice before reporting — already the attachment path's behavior, and only on the failure path.

## QA Checklist

- [ ] `proxied-export` — with `HTTPS_PROXY` set (no `env -u` prefix), run `python3 scripts/export-github-item.py 24`; it writes `docs/issue/24/issue.md` and exits `0`. On `main` this dies with an `HTTPError 403` traceback and writes nothing.
- [ ] `ladder-report` — run `python3 scripts/export-github-item.py 999999`; it exits non-zero and prints **both** rungs in ladder order, each with its body: the proxy's `403 … "GitHub access is not enabled for this session"`, then a real `404 … "Not Found"`.
- [ ] `attachments` — from a scratch directory, export an issue that has attachments (`python3 ../../scripts/export-github-item.py 17 --repo vzakharov/agent-project-boilerplate`); the attachment lands under `docs/issue/17/attachments/` and it exits `0`.
- [ ] `attachment-failure-safe` — force an attachment failure (call `download_asset` with a non-existent `user-attachments` URL and a dummy token); the message is statuses only — `403 Forbidden; then 404 Not Found` — with no response body and no token anywhere in it.
- [ ] `pr-body-roundtrip` — with the proxy in force, run `python3 scripts/pr-body.py pull <this PR>` then `push`; the body round-trips unchanged and both exit `0`.
- [ ] `direct-only` — `env -u HTTPS_PROXY -u https_proxy python3 scripts/export-github-item.py 24` still writes the export and exits `0`, so a proxy-free environment is unaffected.
- [ ] `static` — `ruff check scripts/` and `mypy` over `scripts/` are both clean.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `proxied-export` | integration | ❌ | Mock at the HTTP boundary: proxy rung 403, direct rung 200 → assert the export is written |
| `ladder-report` | integration | ❌ | Both rungs refuse → assert the message carries each status *and* body, in ladder order |
| `attachments` | integration | ❌ | Attachment URL 302s to a signed URL → assert the file is written and `Authorization` is dropped on the redirect |
| `attachment-failure-safe` | unit | ❌ | `AllRoutesFailed` with bodies → assert `format_route_statuses` emits no body and no token. Security-relevant: this is the token-echo guard |
| `pr-body-roundtrip` | integration | ❌ | Proxy rung refuses the PATCH, direct rung accepts → assert one PATCH lands and the body matches |
| `direct-only` | integration | ❌ | No proxy env → assert only one request is made and it goes direct |
| `static` | unit | ❌ | No `scripts/vet.sh` yet — `ruff` + `mypy` are run by hand today |

**Coverage gap:** every row is `❌`. This repo has no test suite and `scripts/vet.sh` is still the boilerplate stub that exits `1`, so nothing here is protected at merge — the checks above were run by hand in the session that wrote this branch, and all seven pass. `attachment-failure-safe` is the row worth automating first: it guards against leaking the bearer token into an error message. Hydrating `vet.sh` for Python is out of this issue's scope; `/finalize` will stop loudly on the stub.

Closes #24

https://claude.ai/code/session_01G8d4RcyYH12dkA1CRxZvRV


---

## Comments

### Comment by @vzakharov on 2026-09-01T23:01:40Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/25#issuecomment-5501599677](https://github.com/vzakharov/agent-project-boilerplate/pull/25#issuecomment-5501599677)

Proposed squash title/body:

```
fix: #24 route the stdlib scripts around a proxy that refuses api.github.com (pr #25)
```

```
`export-github-item.py` and `pr-body.py` reached the GitHub API through
a bare `urlopen`, which honors `HTTPS_PROXY`. A Claude Code remote
session's egress proxy refuses `api.github.com` with its own 403, so the
first API call killed both scripts outright and the only way to run
either was under `env -u HTTPS_PROXY`.

The proxy-then-direct ladder that works around this already existed in
the exporter, scoped to attachment downloads. It moves into
`scripts/lib/github.py` and now serves all three call sites through one
`fetch`. The proxy rung is still first, so a session where the proxy is
the only route out is unaffected; the cost is a second request per rung,
on the failure path only.

Two shapes are load bearing. `fetch` takes a request *factory* because
`ProxyHandler.proxy_open` rewrites a request's host in place — reuse one
`Request` and every rung aims at the proxy. And the failure renderings
are two functions rather than one with a flag: `format_route_statuses`
omits bodies for the attachment path, where S3 quotes the offending
header back — the bearer token in full — while
`format_route_statuses_and_bodies` keeps them for the API paths, where
the proxy's 403 names itself as the refuser.

Fixes #24

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `docs/remove-before-merging/squash-message.md`:1

**@vzakharov** — 2026-09-01T23:04:15Z

cut by 40-50%

**@vzakharov** — 2026-09-01T23:12:00Z

Cut to 188 words from 312 — 40%. What went: the 403's independence from URL shape/token/User-Agent, the per-rung accumulation, and the "two functions rather than one with a flag" framing spelled out at length. What stayed: the two traps a future editor actually needs (why `fetch` takes a factory, why the attachment path must not print bodies). d1ce11e

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `docs/remove-before-merging/squash-message.md`:4

```diff
@@ -0,0 +1,50 @@
+Proposed squash title/body:
+
+```
+feat: #24 route the stdlib scripts around a proxy that refuses api.github.com (pr #25)
```

**@vzakharov** — 2026-09-01T23:04:26Z

arguably a `fix:`?

**@vzakharov** — 2026-09-01T23:12:02Z

Agreed, and #24 is labelled `bug` — the user-visible outcome is two dead scripts running again, with the restructuring in service of that rather than a new capability. Squash title is now `fix:` and the trailer `Fixes #24`; PR title updated to match. d1ce11e

---
_Generated by [Claude Code](https://claude.ai/code)_


---

### `.claude/skills/override-gh/SKILL.md`:9

```diff
@@ -6,4 +6,6 @@ This skill is a no-op marker. Its sole purpose is the description above — surf
 
 **`gh` already bypasses the egress proxy.** In remote/web sessions the SessionStart hook (`.claude/hooks/session-start.sh`) installs a `gh` shim at `$HOME/.local/bin/gh` (first on `PATH`) that runs the real binary under `env -u HTTPS_PROXY -u https_proxy`. The agent proxy's egress policy blocks some `api.github.com` operations — notably long-polling ones like `gh run watch` — so without this, simple actions (watching a CI run, the `/watch-ci` and `/finalize` flows, `scripts/ci-watch-tick.sh`) stall. With the shim, just call `gh` normally — no `env -u …` prefix needed, the unproxying is transparent and applies to every `gh` invocation (scripts, skills, ad-hoc). git keeps the proxy.
 
+**The stdlib Python scripts carry their own way around it.** `scripts/export-github-item.py` and `scripts/pr-body.py` route every request through `lib.github.fetch`, which tries the proxy first and falls back to a direct connection — so they need no shim and no `env -u` prefix either.
```

**@vzakharov** — 2026-09-01T23:05:23Z

is it something we should mention in ADOPTING.md wrt "The only credential-adjacent thing", or is it a different beast? (Not insisting, and I'd rather keep docs lean, but I felt like I should ask.)

**@vzakharov** — 2026-09-01T23:12:03Z

Same mechanism, but it doesn't belong in that paragraph — that warning is scoped to what the *procedure* asks of the reader, and the ladder asks nothing: it's behavior of a file being copied, not a step to consent to.

It does belong one section down, though, because it makes a claim there false. The case for the shim says "git keeps the proxy. Everything else keeps the proxy." — and once `lib/github.py` ships the ladder, everything else doesn't: the stdlib scripts carry the token past the proxy per request whether or not the shim is adopted. An agent weighing "decide knowingly" shouldn't have to find that in the code, so that bullet now names the one exception. Four words longer, no new section. d1ce11e

Unrelated but adjacent: `docs/catalog.md`'s row for `scripts/lib/github.py` still described the module as it stood before the ladder moved in, so I refreshed it in the same commit.

---
_Generated by [Claude Code](https://claude.ai/code)_


---

## Timeline (status, references, and other events)

- **2026-09-01T23:06:53Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/25#pullrequestreview-5083904889.
- **2026-09-01T23:11:41Z** @vzakharov renamed from «feat: route the stdlib scripts' API calls around a proxy that refuses api.github.com» to «fix: route the stdlib scripts' API calls around a proxy that refuses api.github.com».
