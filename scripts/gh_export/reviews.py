"""The PR-only review section: review bodies, inline comment threads grouped
into reply chains, and each thread's resolved state.
"""

from __future__ import annotations

from typing import Any

from gh_export.attachments import rewrite_attachment_refs
from gh_export.authorship import attribution, split_agent_footer


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

    return sorted(threads.values(), key=lambda chain: chain[0].get("created_at") or "")


def resolution_label(
    chain: list[dict[str, Any]], resolved_by_comment_id: dict[int, bool]
) -> str:
    """A thread the resolution query didn't return reads as `resolution unknown`
    rather than silently as open — a reader acts on this word."""
    for comment in chain:
        resolved = resolved_by_comment_id.get(comment.get("id"))
        if resolved is not None:
            return "resolved" if resolved else "unresolved"
    return "resolution unknown"


def review_section(
    reviews: list[dict[str, Any]],
    comments: list[dict[str, Any]],
    url_to_relative: dict[str, str],
    resolved_by_comment_id: dict[int, bool],
) -> str:
    """Render review bodies and inline comment threads, or "" if there are none."""
    bodied = [r for r in reviews if (r.get("body") or "").strip()]
    threads = review_threads(comments)
    if not bodied and not threads:
        return ""

    chunks = ["## Review threads", ""]

    for review in bodied:
        state = (review.get("state") or "COMMENTED").upper()
        by_agent, body = split_agent_footer(review["body"])
        chunks.extend(
            [
                f"### Review by {attribution(review.get('user'), by_agent)}"
                f" — {state}",
                "",
                f"_{review.get('submitted_at', '')}_",
                "",
                rewrite_attachment_refs(body or "_empty_", url_to_relative),
                "",
            ]
        )

    for chain in threads:
        root = chain[0]
        line = root.get("line") or root.get("original_line") or "?"
        label = resolution_label(chain, resolved_by_comment_id)
        chunks.extend([f"### `{root.get('path', '?')}`:{line} — {label}", ""])
        hunk = root.get("diff_hunk")
        if hunk:
            chunks.extend(["```diff", hunk, "```", ""])
        for comment in chain:
            by_agent, body = split_agent_footer(comment.get("body") or "")
            chunks.extend(
                [
                    f"**{attribution(comment.get('user'), by_agent)}**"
                    f" — {comment.get('created_at', '')}",
                    "",
                    rewrite_attachment_refs(body or "_empty_", url_to_relative),
                    "",
                ]
            )
        chunks.extend(["---", ""])

    return "\n".join(chunks)
