"""The sections every export carries: the header block and the conversation
comments, plus the login helper the review and timeline renderers share.
"""

from __future__ import annotations

from typing import Any

from gh_export.attachments import rewrite_attachment_refs


def login_of(holder: Any, default: str = "?") -> str:
    """Login of a `user`/`actor`/`requested_reviewer`-shaped nested object."""
    return (holder or {}).get("login") or default


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
        head = (head_ref.get("label") if cross_repo else head_ref.get("ref")) or "?"
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
