#!/usr/bin/env python3
"""Export a GitHub issue or pull request to Markdown plus downloaded attachments.

Usage:
  python3 scripts/export-github-item.py <number|issue-url|pr-url> [--repo OWNER/REPO]

Issues land in docs/issue/<n>/issue.md, pull requests in docs/pr/<n>/pr.md; both
put downloaded attachments under <out-dir>/attachments/. A bare number works for
either — the type comes from the API, not from the argument. A PR export also
carries its review threads: review bodies, inline comments grouped into reply
chains, and the diff hunk each chain hangs off.

Exit status is non-zero when any attachment fails to download; the Markdown is
still written, with the failed attachments still linked remotely.

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
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, NamedTuple

from lib.github import (
    GITHUB_API_VERSION,
    AllRoutesFailed,
    detect_origin_repo,
    die,
    fetch,
    format_route_statuses,
    format_route_statuses_and_bodies,
    gh_token,
)

ATTACHMENT_URL_RE = re.compile(
    r"https://(?:"
    r"private-user-images\.githubusercontent\.com/[^\s\"'\)<>]+|"
    r"user-images\.githubusercontent\.com/[^\s\"'\)<>]+|"
    r"github\.com/user-attachments/assets/[^\s\"'\)<>]+|"
    r"github\.com/user-attachments/files/[^\s\"'\)<>]+"
    r")",
    re.IGNORECASE,
)

DOCS_ISSUE_ROOT = Path("docs") / "issue"
DOCS_PR_ROOT = Path("docs") / "pr"
USER_AGENT = "export-github-item.py"


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
            r"^https://github\.com/([^/]+)/([^/]+)/(?:issues|pull)/(\d+)/?$",
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
            "Usage: python3 scripts/export-github-item.py "
            "<number|https://github.com/OWNER/REPO/issues/N"
            "|https://github.com/OWNER/REPO/pull/N> [--repo OWNER/REPO]"
        )

    if repo_flag is None:
        repo_flag = detect_origin_repo()
        if repo_flag is None:
            die(
                "Could not determine OWNER/REPO. Pass --repo OWNER/REPO, give a full "
                "issue or PR URL, or run from a checkout whose `origin` is a "
                "github.com repo."
            )

    parts = repo_flag.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        die("--repo and item URLs must use OWNER/REPO (e.g. octocat/hello-world).")

    return nums[0], repo_flag


def _request(url: str, token: str, accept: str) -> tuple[bytes, dict[str, str]]:
    return fetch(
        lambda: urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": accept,
                "X-GitHub-Api-Version": GITHUB_API_VERSION,
                "User-Agent": USER_AGENT,
            },
        )
    )


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
    """Paginate with an explicit `page=` rather than the Link header's URL:
    GitHub phrases those as `repositories/{id}/…`, which the agent proxy in
    Claude Code web sessions rejects with 403.
    """
    items: list[Any] = []
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        url = f"{path}{sep}per_page=100&page={page}"
        data, headers = api_json(url, token)
        if not isinstance(data, list):
            raise RuntimeError(
                f"Expected JSON array from {url}, got {type(data).__name__}"
            )
        items.extend(data)
        if not has_next_page(headers.get("link")):
            return items
        page += 1


def has_next_page(link_header: str | None) -> bool:
    if not link_header:
        return False
    return any(
        re.match(r'\s*<[^>]+>;\s*rel="next"', part) for part in link_header.split(",")
    )


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


class AttachmentDownloadError(Exception):
    """Every opener failed for one attachment.

    The message carries each attempt's status line and nothing else: S3's
    rejection body echoes the offending header value — i.e. the bearer token in
    full — so no response body ever reaches it.
    """


def download_asset(url: str, dest: Path, token: str) -> str:
    try:
        buf, headers = _request(url, token, "application/octet-stream")
    except AllRoutesFailed as exc:
        raise AttachmentDownloadError(
            format_route_statuses(exc.failures)
        ) from exc

    ext = extension_for_bytes(buf, headers.get("content-type"))
    write_path = dest if dest.suffix else (Path(str(dest) + ext) if ext else dest)
    write_path.write_bytes(buf)
    return f"./attachments/{write_path.name}"


class AttachmentDownloads(NamedTuple):
    """One thread's attachment URLs split by outcome, both halves keyed by URL."""

    url_to_relative: dict[str, str]
    failures: dict[str, str]


def download_attachments(
    urls: list[str], attachments_dir: Path, token: str
) -> AttachmentDownloads:
    if not urls:
        return AttachmentDownloads({}, {})
    attachments_dir.mkdir(parents=True, exist_ok=True)
    url_to_relative: dict[str, str] = {}
    failures: dict[str, str] = {}
    used: set[str] = set()
    for idx, url in enumerate(urls, start=1):
        base_name = slug_from_url(url, idx)
        if base_name in used:
            stem, ext = os.path.splitext(base_name)
            n = 2
            while f"{stem}-{n}{ext}" in used:
                n += 1
            base_name = f"{stem}-{n}{ext}"
        try:
            rel = download_asset(url, attachments_dir / base_name, token)
        except AttachmentDownloadError as exc:
            failures[url] = str(exc)
            continue
        used.add(os.path.basename(rel))
        url_to_relative[url] = rel
    return AttachmentDownloads(url_to_relative, failures)


def login_of(holder: Any, default: str = "?") -> str:
    """Login of a `user`/`actor`/`requested_reviewer`-shaped nested object."""
    return (holder or {}).get("login") or default


_STATIC_TIMELINE_SUFFIXES = {
    "reopened": "reopened {noun}.",
    "locked": "locked {noun}.",
    "unlocked": "unlocked {noun}.",
    "pinned": "pinned {noun}.",
    "unpinned": "unpinned {noun}.",
    "transferred": "transferred {noun}.",
    "connected": "connected {noun} (integration).",
    "disconnected": "disconnected {noun} (integration).",
    "head_ref_deleted": "deleted the head ref.",
    "head_ref_restored": "restored the head ref.",
    "merged": "merged {noun}.",
    "ready_for_review": "marked {noun} ready for review.",
    "convert_to_draft": "converted {noun} to a draft.",
}

_TIMELINE_SKIP = frozenset({"committed", "commented"})


def _reviewer_name(ev: dict[str, Any]) -> str:
    reviewer = login_of(ev.get("requested_reviewer"), "")
    if reviewer:
        return f"@{reviewer}"
    team = (ev.get("requested_team") or {}).get("name")
    return f"team «{team}»" if team else "?"


def _timeline_suffix(ev: dict[str, Any], noun: str) -> str:
    """Return the phrase after `@{who} ` for a timeline event."""
    kind = ev.get("event") or ""
    if kind in _STATIC_TIMELINE_SUFFIXES:
        return _STATIC_TIMELINE_SUFFIXES[kind].format(noun=noun)

    label = (ev.get("label") or {}).get("name", "?")
    assignee = (ev.get("assignee") or {}).get("login", "?")
    milestone = (ev.get("milestone") or {}).get("title", "?")

    if kind == "closed":
        reason = ev.get("state_reason")
        return f"closed {noun} ({reason})." if reason else f"closed {noun}."
    if kind == "renamed":
        r = ev.get("rename") or {}
        return f"renamed from «{r.get('from', '?')}» to «{r.get('to', '?')}»."
    if kind == "labeled":
        return f"added label `{label}`."
    if kind == "unlabeled":
        return f"removed label `{label}`."
    if kind == "assigned":
        return f"assigned @{assignee}."
    if kind == "unassigned":
        return f"unassigned @{assignee}."
    if kind == "milestoned":
        return f"added milestone «{milestone}»."
    if kind == "demilestoned":
        return f"removed milestone «{milestone}»."
    if kind == "referenced":
        commit = ev.get("commit_url") or ev.get("commit_id") or ""
        note = f": {commit}" if commit else ""
        return f"referenced {noun} in a commit{note}."
    if kind == "cross-referenced":
        src = (ev.get("source") or {}).get("issue") or {}
        href = src.get("html_url")
        link = (
            f"[#{src.get('number', '?')} {src.get('title', '')}]({href})"
            if href
            else "(source issue unavailable)"
        )
        return f"cross-referenced {noun} from {link}."
    if kind == "reviewed":
        state = (ev.get("state") or "reviewed").upper()
        href = ev.get("html_url") or ""
        link = f": {href}" if href else ""
        return f"reviewed ({state}){link}."
    if kind == "review_requested":
        return f"requested a review from {_reviewer_name(ev)}."
    if kind == "review_request_removed":
        return f"removed the review request for {_reviewer_name(ev)}."
    return f"— _{kind}_"


def format_timeline_line(ev: dict[str, Any], noun: str) -> str:
    kind = ev.get("event") or ""
    if kind in _TIMELINE_SKIP:
        return ""
    # `reviewed` events are review payloads: they carry `user`/`submitted_at`
    # where every other event carries `actor`/`created_at`.
    who = login_of(ev.get("actor") or ev.get("user"), "unknown")
    when = ev.get("created_at") or ev.get("submitted_at") or ""
    return f"- **{when}** @{who} {_timeline_suffix(ev, noun)}"


def timeline_section(events: list[dict[str, Any]], noun: str) -> str:
    lines = [
        line
        for ev in events
        if (line := format_timeline_line(ev, noun))
    ]
    if not lines:
        return ""
    return "\n".join(
        ["## Timeline (status, references, and other events)", "", *lines, ""]
    )


def review_threads(comments: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Group inline review comments into reply chains, oldest root first."""
    by_id = {c["id"]: c for c in comments if c.get("id") is not None}

    def root_of(comment: dict[str, Any]) -> dict[str, Any]:
        seen: set[Any] = set()
        current = comment
        while True:
            parent_id = current.get("in_reply_to_id")
            if parent_id is None or parent_id not in by_id or parent_id in seen:
                return current
            seen.add(parent_id)
            current = by_id[parent_id]

    threads: dict[Any, list[dict[str, Any]]] = {}
    for comment in comments:
        threads.setdefault(root_of(comment)["id"], []).append(comment)

    for chain in threads.values():
        chain.sort(key=lambda c: c.get("created_at") or "")

    return sorted(
        threads.values(), key=lambda chain: chain[0].get("created_at") or ""
    )


def review_section(
    reviews: list[dict[str, Any]],
    comments: list[dict[str, Any]],
    url_to_relative: dict[str, str],
) -> str:
    """Render review bodies and inline comment threads, or "" if there are none."""
    bodied = [r for r in reviews if (r.get("body") or "").strip()]
    threads = review_threads(comments)
    if not bodied and not threads:
        return ""

    chunks = ["## Review threads", ""]

    for review in bodied:
        state = (review.get("state") or "COMMENTED").upper()
        who = login_of(review.get("user"))
        chunks.extend(
            [
                f"### Review by @{who} — {state}",
                "",
                f"_{review.get('submitted_at', '')}_",
                "",
                rewrite_attachment_refs(review["body"], url_to_relative),
                "",
            ]
        )

    for chain in threads:
        root = chain[0]
        line = root.get("line") or root.get("original_line") or "?"
        chunks.extend([f"### `{root.get('path', '?')}`:{line}", ""])
        hunk = root.get("diff_hunk")
        if hunk:
            chunks.extend(["```diff", hunk, "```", ""])
        for comment in chain:
            who = login_of(comment.get("user"))
            chunks.extend(
                [
                    f"**@{who}** — {comment.get('created_at', '')}",
                    "",
                    rewrite_attachment_refs(
                        comment.get("body") or "_empty_", url_to_relative
                    ),
                    "",
                ]
            )
        chunks.extend(["---", ""])

    return "\n".join(chunks)


def comments_section(
    comments: list[dict[str, Any]], url_to_relative: dict[str, str]
) -> str:
    if not comments:
        return ""
    chunks = ["## Comments", ""]
    for c in comments:
        text = rewrite_attachment_refs(c.get("body") or "_empty_", url_to_relative)
        chunks.extend(
            [
                f"### Comment by @{login_of(c.get('user'))} on {c.get('created_at', '')}",
                "",
                f"[{c.get('html_url', '')}]({c.get('html_url', '')})",
                "",
                text,
                "",
                "---",
                "",
            ]
        )
    return "\n".join(chunks)


def header_section(item: dict[str, Any], pr: dict[str, Any] | None) -> str:
    labels = item.get("labels") or []
    labels_md = (
        ", ".join(f"`{(lab.get('name') or '')}`" for lab in labels)
        if labels
        else "_none_"
    )
    state_reason = item.get("state_reason") or ""
    state_suffix = f" ({state_reason})" if state_reason else ""

    lines = [
        f"# {'PR' if pr else 'Issue'} #{item['number']}: {item['title']}",
        "",
        f"- **State:** {item['state']}{state_suffix}",
        f"- **URL:** {item['html_url']}",
        f"- **Author:** @{login_of(item.get('user'))}",
    ]
    if pr:
        base_ref = pr.get("base") or {}
        head_ref = pr.get("head") or {}
        base = base_ref.get("ref") or "?"
        # A fork's head needs its `owner:branch` label to be unambiguous.
        cross_repo = (head_ref.get("repo") or {}).get("full_name") != (
            base_ref.get("repo") or {}
        ).get("full_name")
        head = (
            head_ref.get("label") if cross_repo else head_ref.get("ref")
        ) or "?"
        lines.extend(
            [
                f"- **Base ← Head:** {base} ← {head}",
                f"- **Draft:** {'yes' if pr.get('draft') else 'no'}",
                f"- **Merged:** {pr.get('merged_at') or '_not merged_'}",
            ]
        )
    lines.extend(
        [
            f"- **Created:** {item['created_at']}",
            f"- **Updated:** {item['updated_at']}",
            f"- **Closed:** {item.get('closed_at') or '_not closed_'}",
            f"- **Labels:** {labels_md}",
            "",
            "---",
            "",
            "## Body",
            "",
        ]
    )
    return "\n".join(lines)


def rewrite_attachment_refs(text: str, url_to_relative: dict[str, str]) -> str:
    for url, rel in url_to_relative.items():
        text = text.replace(url, rel)
    return text


def main() -> None:
    number, repo = parse_args(sys.argv)
    token = gh_token()
    base = f"repos/{repo}/issues/{number}"

    pr: dict[str, Any] | None = None
    reviews: list[dict[str, Any]] = []
    review_comments: list[dict[str, Any]] = []
    try:
        # The issues endpoint serves PRs too, and is the only one carrying the
        # conversation comments and timeline.
        item = api_get(base, token)
        is_pr = item.get("pull_request") is not None
        comments = api_paginated(f"{base}/comments", token)
        timeline = api_paginated(f"{base}/timeline", token)

        if is_pr:
            pr_base = f"repos/{repo}/pulls/{number}"
            pr = api_get(pr_base, token)
            reviews = api_paginated(f"{pr_base}/reviews", token)
            review_comments = api_paginated(f"{pr_base}/comments", token)
    except AllRoutesFailed as exc:
        die(
            f"GitHub API request for #{number} failed on every route:\n"
            f"{format_route_statuses_and_bodies(exc.failures)}"
        )

    out_dir = (DOCS_PR_ROOT if is_pr else DOCS_ISSUE_ROOT) / str(number)
    attachments_dir = out_dir / "attachments"
    md_path = out_dir / ("pr.md" if is_pr else "issue.md")

    body_md = item.get("body") or "_No description._"
    prose = [
        body_md,
        *(c.get("body") or "" for c in comments),
        *(r.get("body") or "" for r in reviews),
        *(rc.get("body") or "" for rc in review_comments),
    ]
    downloads = download_attachments(
        collect_attachment_urls("\n\n".join(prose)), attachments_dir, token
    )
    url_to_relative = downloads.url_to_relative

    body_md = rewrite_attachment_refs(body_md, url_to_relative)
    noun = "this pull request" if is_pr else "this issue"

    # The review section is dropped rather than joined as "" — an empty element
    # would leave a stray blank line in every issue export.
    sections = [
        header_section(item, pr),
        body_md,
        "",
        "---",
        "",
        comments_section(comments, url_to_relative),
        *filter(None, [review_section(reviews, review_comments, url_to_relative)]),
        timeline_section(timeline, noun),
    ]
    full_md = "\n".join(sections)

    out_dir.mkdir(parents=True, exist_ok=True)
    md_path.write_text(full_md, encoding="utf-8")

    print(f"Wrote {md_path}")
    total = len(url_to_relative) + len(downloads.failures)
    if total:
        print(
            f"Downloaded {len(url_to_relative)}/{total} attachment(s) "
            f"under {attachments_dir}"
        )
    for url, reason in downloads.failures.items():
        print(f"Failed to download {url}: {reason}", file=sys.stderr)
    if downloads.failures:
        # The prose is worth having without its images, so the export stays
        # written and the exit code carries the failure — the Markdown still
        # points at whatever did not download.
        die(
            f"{len(downloads.failures)} of {total} attachment(s) failed; "
            f"{md_path} still links to them remotely."
        )


if __name__ == "__main__":
    main()
