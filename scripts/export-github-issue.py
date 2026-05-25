#!/usr/bin/env python3
"""Export a GitHub issue to docs/issue/<n>/issue.md plus downloaded attachments.

Usage:
  python3 scripts/export-github-issue.py <issue-number|issue-url> [--repo OWNER/REPO]

Auth: uses $GH_TOKEN (or $GITHUB_TOKEN) if set, otherwise falls back to
`gh auth token`. A token is required to download GitHub's private user-image
attachment URLs (private-user-images.githubusercontent.com), which auth-gate
even when the issue itself is public.

Stdlib only — no third-party deps. Python 3.9+.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ATTACHMENT_URL_RE = re.compile(
    r"https://(?:"
    r"private-user-images\.githubusercontent\.com/[^\s\"'\)<>]+|"
    r"user-images\.githubusercontent\.com/[^\s\"'\)<>]+|"
    r"github\.com/user-attachments/assets/[^\s\"'\)<>]+"
    r")",
    re.IGNORECASE,
)

DOCS_ISSUE_ROOT = Path("docs") / "issue"
USER_AGENT = "export-github-issue.py"


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def gh_token() -> str:
    env = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if env:
        return env.strip()
    try:
        out = subprocess.check_output(["gh", "auth", "token"], text=True)
    except FileNotFoundError:
        die("No GitHub token: set $GH_TOKEN or install `gh` and run `gh auth login`.")
    except subprocess.CalledProcessError:
        die("`gh auth token` failed; run `gh auth login` or set $GH_TOKEN.")
    token = out.strip()
    if not token:
        die("Empty token from `gh auth token`; run `gh auth login`.")
    return token


def detect_origin_repo() -> str | None:
    try:
        url = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], text=True
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    m = re.match(
        r"^(?:https://github\.com/|git@github\.com:)([^/]+)/([^/]+?)(?:\.git)?/?$",
        url,
    )
    return f"{m.group(1)}/{m.group(2)}" if m else None


def parse_args(argv: list[str]) -> tuple[int, str]:
    rest = [a for a in argv[1:] if a != "--"]
    repo_flag: str | None = None
    nums: list[int] = []
    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--repo" and i + 1 < len(rest):
            repo_flag = rest[i + 1]
            i += 2
            continue
        m_url = re.match(
            r"^https://github\.com/([^/]+)/([^/]+)/issues/(\d+)/?$",
            arg.strip(),
            re.IGNORECASE,
        )
        if m_url:
            repo_flag = f"{m_url.group(1)}/{m_url.group(2)}"
            nums.append(int(m_url.group(3)))
            i += 1
            continue
        m_num = re.match(r"^#?(\d+)$", arg)
        if m_num:
            nums.append(int(m_num.group(1)))
        i += 1

    if len(nums) != 1:
        die(
            "Usage: python3 scripts/export-github-issue.py "
            "<issue-number|https://github.com/OWNER/REPO/issues/N> [--repo OWNER/REPO]"
        )

    if repo_flag is None:
        repo_flag = detect_origin_repo()
        if repo_flag is None:
            die(
                "Could not determine OWNER/REPO. Pass --repo OWNER/REPO, give a full "
                "issue URL, or run from a checkout whose `origin` is a github.com repo."
            )

    parts = repo_flag.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        die("--repo and issue URLs must use OWNER/REPO (e.g. octocat/hello-world).")

    return nums[0], repo_flag


def _request(url: str, token: str, accept: str) -> tuple[bytes, dict[str, str]]:
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": accept,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        },
    )
    with urllib.request.urlopen(req) as resp:
        return resp.read(), {k.lower(): v for k, v in resp.headers.items()}


def api_json(path_or_url: str, token: str) -> tuple[Any, dict[str, str]]:
    url = (
        path_or_url
        if path_or_url.startswith("http")
        else f"https://api.github.com/{path_or_url.lstrip('/')}"
    )
    body, headers = _request(url, token, "application/vnd.github+json")
    return json.loads(body), headers


def api_get(path: str, token: str) -> Any:
    data, _ = api_json(path, token)
    return data


def api_paginated(path: str, token: str) -> list[Any]:
    items: list[Any] = []
    url: str | None = path
    while url:
        data, headers = api_json(url, token)
        if not isinstance(data, list):
            raise RuntimeError(
                f"Expected JSON array from {url}, got {type(data).__name__}"
            )
        items.extend(data)
        url = parse_next_link(headers.get("link"))
    return items


def parse_next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for part in link_header.split(","):
        m = re.match(r'\s*<([^>]+)>;\s*rel="next"', part)
        if m:
            return m.group(1)
    return None


def collect_attachment_urls(text: str) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for m in ATTACHMENT_URL_RE.finditer(text):
        url = re.sub(r"[),.;]+$", "", m.group(0))
        if url not in seen:
            seen.add(url)
            ordered.append(url)
    return ordered


def slug_from_url(url: str, index: int) -> str:
    try:
        parsed = urllib.parse.urlparse(url)
        base = os.path.basename(parsed.path) or f"asset-{index}"
        safe = re.sub(r"[^\w.-]+", "_", base)[:180]
        return safe or f"asset-{index}"
    except Exception:
        return f"asset-{index}"


def extension_for_bytes(buf: bytes, content_type: str | None) -> str:
    ct = (content_type or "").split(";")[0].strip().lower()
    if ct == "image/png":
        return ".png"
    if ct in ("image/jpeg", "image/jpg"):
        return ".jpg"
    if ct == "image/gif":
        return ".gif"
    if ct == "image/webp":
        return ".webp"
    if ct == "image/svg+xml":
        return ".svg"
    if len(buf) >= 4 and buf[:4] == b"\x89PNG":
        return ".png"
    if len(buf) >= 3 and buf[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if len(buf) >= 3 and buf[:3] == b"GIF":
        return ".gif"
    if len(buf) >= 4 and buf[:4] == b"RIFF":
        return ".webp"
    return ""


def download_asset(url: str, dest: Path, token: str) -> str | None:
    try:
        buf, headers = _request(url, token, "application/octet-stream")
    except urllib.error.HTTPError as exc:
        print(f"Failed to download {url}: {exc.code} {exc.reason}", file=sys.stderr)
        return None
    except urllib.error.URLError as exc:
        print(f"Failed to download {url}: {exc}", file=sys.stderr)
        return None

    ext = extension_for_bytes(buf, headers.get("content-type"))
    write_path = dest if dest.suffix else (Path(str(dest) + ext) if ext else dest)
    write_path.write_bytes(buf)
    return f"./attachments/{write_path.name}"


_TIMELINE_FORMATTERS: dict[str, Any] = {}


def _fmt(kind: str):
    def decorator(fn):
        _TIMELINE_FORMATTERS[kind] = fn
        return fn

    return decorator


@_fmt("closed")
def _closed(ev, who, when):
    reason = ev.get("state_reason")
    suffix = f" ({reason})" if reason else ""
    return f"- **{when}** @{who} closed this issue{suffix}."


@_fmt("reopened")
def _reopened(ev, who, when):
    return f"- **{when}** @{who} reopened this issue."


@_fmt("renamed")
def _renamed(ev, who, when):
    r = ev.get("rename") or {}
    return f"- **{when}** @{who} renamed from «{r.get('from', '?')}» to «{r.get('to', '?')}»."


@_fmt("labeled")
def _labeled(ev, who, when):
    return f"- **{when}** @{who} added label `{(ev.get('label') or {}).get('name', '?')}`."


@_fmt("unlabeled")
def _unlabeled(ev, who, when):
    return f"- **{when}** @{who} removed label `{(ev.get('label') or {}).get('name', '?')}`."


@_fmt("assigned")
def _assigned(ev, who, when):
    return f"- **{when}** @{who} assigned @{(ev.get('assignee') or {}).get('login', '?')}."


@_fmt("unassigned")
def _unassigned(ev, who, when):
    return f"- **{when}** @{who} unassigned @{(ev.get('assignee') or {}).get('login', '?')}."


@_fmt("milestoned")
def _milestoned(ev, who, when):
    return f"- **{when}** @{who} added milestone «{(ev.get('milestone') or {}).get('title', '?')}»."


@_fmt("demilestoned")
def _demilestoned(ev, who, when):
    return f"- **{when}** @{who} removed milestone «{(ev.get('milestone') or {}).get('title', '?')}»."


@_fmt("locked")
def _locked(ev, who, when):
    return f"- **{when}** @{who} locked this issue."


@_fmt("unlocked")
def _unlocked(ev, who, when):
    return f"- **{when}** @{who} unlocked this issue."


@_fmt("pinned")
def _pinned(ev, who, when):
    return f"- **{when}** @{who} pinned this issue."


@_fmt("unpinned")
def _unpinned(ev, who, when):
    return f"- **{when}** @{who} unpinned this issue."


@_fmt("referenced")
def _referenced(ev, who, when):
    commit = ev.get("commit_url") or ev.get("commit_id") or ""
    note = f": {commit}" if commit else ""
    return f"- **{when}** @{who} referenced this issue in a commit{note}."


@_fmt("cross-referenced")
def _crossref(ev, who, when):
    src = (ev.get("source") or {}).get("issue") or {}
    href = src.get("html_url")
    if href:
        link = f"[#{src.get('number', '?')} {src.get('title', '')}]({href})"
    else:
        link = "(source issue unavailable)"
    return f"- **{when}** @{who} cross-referenced this issue from {link}."


@_fmt("connected")
def _connected(ev, who, when):
    return f"- **{when}** @{who} connected this issue (integration)."


@_fmt("disconnected")
def _disconnected(ev, who, when):
    return f"- **{when}** @{who} disconnected this issue (integration)."


@_fmt("transferred")
def _transferred(ev, who, when):
    return f"- **{when}** @{who} transferred this issue."


@_fmt("head_ref_deleted")
def _head_deleted(ev, who, when):
    return f"- **{when}** @{who} deleted the head ref."


@_fmt("head_ref_restored")
def _head_restored(ev, who, when):
    return f"- **{when}** @{who} restored the head ref."


def format_timeline_line(ev: dict[str, Any]) -> str:
    kind = ev.get("event") or ""
    if kind in ("committed", "commented"):
        return ""
    who = ((ev.get("actor") or {}).get("login")) or "unknown"
    when = ev.get("created_at") or ""
    fn = _TIMELINE_FORMATTERS.get(kind)
    if fn:
        return fn(ev, who, when)
    return f"- **{when}** @{who} — _{kind}_"


def timeline_section(events: list[dict[str, Any]]) -> str:
    lines = [
        line
        for ev in events
        if (line := format_timeline_line(ev))
    ]
    if not lines:
        return ""
    return "\n".join(
        ["## Timeline (status, references, and other events)", "", *lines, ""]
    )


def rewrite_attachment_refs(text: str, url_to_relative: dict[str, str]) -> str:
    for url, rel in url_to_relative.items():
        text = text.replace(url, rel)
    return text


def main() -> None:
    issue_num, repo = parse_args(sys.argv)
    token = gh_token()
    base = f"repos/{repo}/issues/{issue_num}"

    issue = api_get(base, token)
    comments = api_paginated(f"{base}/comments", token)
    timeline = api_paginated(f"{base}/timeline", token)

    issue_dir = DOCS_ISSUE_ROOT / str(issue_num)
    attachments_dir = issue_dir / "attachments"
    md_path = issue_dir / "issue.md"

    body_md = issue.get("body") or "_No description._"
    comment_bodies = [c.get("body") or "" for c in comments]
    all_text = "\n\n".join([body_md, *comment_bodies])
    urls = collect_attachment_urls(all_text)

    url_to_relative: dict[str, str] = {}
    if urls:
        attachments_dir.mkdir(parents=True, exist_ok=True)
        used: set[str] = set()
        for idx, url in enumerate(urls, start=1):
            base_name = slug_from_url(url, idx)
            if base_name in used:
                stem, ext = os.path.splitext(base_name)
                n = 2
                while f"{stem}-{n}{ext}" in used:
                    n += 1
                base_name = f"{stem}-{n}{ext}"
            rel = download_asset(url, attachments_dir / base_name, token)
            if rel is not None:
                used.add(os.path.basename(rel))
                url_to_relative[url] = rel

    body_md = rewrite_attachment_refs(body_md, url_to_relative)

    labels = issue.get("labels") or []
    labels_md = (
        ", ".join(f"`{(l.get('name') or '')}`" for l in labels) if labels else "_none_"
    )
    state_reason = issue.get("state_reason") or ""
    state_suffix = f" ({state_reason})" if state_reason else ""

    header = "\n".join(
        [
            f"# Issue #{issue['number']}: {issue['title']}",
            "",
            f"- **State:** {issue['state']}{state_suffix}",
            f"- **URL:** {issue['html_url']}",
            f"- **Author:** @{(issue.get('user') or {}).get('login') or '?'}",
            f"- **Created:** {issue['created_at']}",
            f"- **Updated:** {issue['updated_at']}",
            f"- **Closed:** {issue.get('closed_at') or '_not closed_'}",
            f"- **Labels:** {labels_md}",
            "",
            "---",
            "",
            "## Body",
            "",
        ]
    )

    if comments:
        chunks = ["## Comments", ""]
        for c in comments:
            text = rewrite_attachment_refs(c.get("body") or "_empty_", url_to_relative)
            chunks.extend(
                [
                    f"### Comment by @{(c.get('user') or {}).get('login') or '?'} on {c.get('created_at', '')}",
                    "",
                    f"[{c.get('html_url', '')}]({c.get('html_url', '')})",
                    "",
                    text,
                    "",
                    "---",
                    "",
                ]
            )
        comments_md = "\n".join(chunks)
    else:
        comments_md = ""

    full_md = "\n".join(
        [header, body_md, "", "---", "", comments_md, timeline_section(timeline)]
    )

    issue_dir.mkdir(parents=True, exist_ok=True)
    md_path.write_text(full_md, encoding="utf-8")

    print(f"Wrote {md_path}")
    if url_to_relative:
        print(
            f"Downloaded {len(url_to_relative)} attachment(s) under {attachments_dir}"
        )


if __name__ == "__main__":
    main()
