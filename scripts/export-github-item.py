#!/usr/bin/env python3
"""Export a GitHub issue or pull request to Markdown plus downloaded attachments.

Usage:
  python3 scripts/export-github-item.py <number|issue-url|pr-url> [--repo OWNER/REPO]

Issues land in docs/issue/<n>/issue.md, pull requests in docs/pr/<n>/pr.md; both
put downloaded attachments under <out-dir>/attachments/. A bare number works for
either — the type comes from the API, not from the argument. A PR export also
carries its review threads: review bodies, inline comments grouped into reply
chains, the diff hunk each chain hangs off, and whether the reviewer resolved it.

Exit status is non-zero when any attachment fails to download; the Markdown is
still written, with the failed attachments still linked remotely.

Auth: uses $GH_TOKEN (or $GITHUB_TOKEN) if set, otherwise falls back to
`gh auth token`. A token is required to download GitHub's private user-image
attachment URLs (private-user-images.githubusercontent.com), which auth-gate
even when the issue itself is public.

The pieces live in `scripts/gh_export/`; running this file as
`python3 scripts/export-github-item.py` puts `scripts/` on `sys.path[0]`, so
both `gh_export` and `lib` resolve as PEP 420 namespace packages from any
working directory — no `__init__.py`, no `sys.path` manipulation.

Stdlib only — no third-party deps, here or under `gh_export/`. Python 3.9+.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from gh_export.api import (
    GraphqlError,
    api_get,
    api_paginated,
    fetch_thread_resolution,
)
from gh_export.attachments import (
    collect_attachment_urls,
    download_attachments,
    rewrite_attachment_refs,
)
from gh_export.cli import parse_args
from gh_export.markdown import comments_section, header_section
from gh_export.reviews import review_section
from gh_export.timeline import timeline_section
from lib.github import (
    AllRoutesFailed,
    die,
    format_route_statuses_and_bodies,
    gh_token,
)

DOCS_ISSUE_ROOT = Path("docs") / "issue"
DOCS_PR_ROOT = Path("docs") / "pr"


def main() -> None:
    number, repo = parse_args(sys.argv)
    token = gh_token()
    base = f"repos/{repo}/issues/{number}"

    pr: dict[str, Any] | None = None
    reviews: list[dict[str, Any]] = []
    review_comments: list[dict[str, Any]] = []
    resolved_by_comment_id: dict[int, bool] = {}
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
            resolved_by_comment_id = fetch_thread_resolution(repo, number, token)
    except AllRoutesFailed as exc:
        die(
            f"GitHub API request for #{number} failed on every route:\n"
            f"{format_route_statuses_and_bodies(exc.failures)}"
        )
    except GraphqlError as exc:
        die(f"GitHub GraphQL query for #{number}'s review threads failed: {exc}")

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
        *filter(
            None,
            [
                review_section(
                    reviews, review_comments, url_to_relative, resolved_by_comment_id
                )
            ],
        ),
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
