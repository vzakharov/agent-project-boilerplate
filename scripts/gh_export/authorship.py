"""Who wrote a post: the login, and whether the post is the agent's or a
human's.

`$GH_TOKEN` is the operator's own identity, so an agent's reply and a human's
guidance reach GitHub under one login and the Claude Code attribution footer is
the only thing separating them. That is why the footer stays **mandatory** on
every agent-authored post: it is read here as a signal, not carried as a
courtesy, and a post that omits it exports as a human's.
"""

from __future__ import annotations

import re
from typing import Any

# Both link targets, both verbs, the optional rule above and session link below
# — the footer's forms across this repo's comment rule and the harness's own
# PR-description block.
_ATTRIBUTION_FOOTER = re.compile(
    r"(?:\A|\n)\s*"  # the whole body, or a break from the prose above
    r"(?:-{3,}[ \t]*\n\s*)?"  # optional horizontal rule
    r"(?:🤖[ \t]*)?"
    r"_?Generated (?:by|with) "
    r"\[Claude Code\]\(https://claude\.(?:ai/code|com/claude-code)/?\)_?"
    r"(?:\s*https://claude\.ai/code/session_[A-Za-z0-9_-]+)?"
    r"\s*\Z"
)


def login_of(holder: Any, default: str = "?") -> str:
    """Login of a `user`/`actor`/`requested_reviewer`-shaped nested object."""
    return (holder or {}).get("login") or default


def split_agent_footer(body: str) -> tuple[bool, str]:
    """Whether the body ends in an attribution footer, and the body without it.

    Anchored at the end of the body, so a footer quoted or discussed mid-post
    stays prose — the export must not read one as a signature.
    """
    match = _ATTRIBUTION_FOOTER.search(body)
    if not match:
        return False, body.rstrip()
    return True, body[: match.start()].rstrip()


def attribution(holder: Any, by_agent: bool) -> str:
    """`@login (agent)` / `@login (human)`, annotating the login rather than
    replacing it. `(human)` and not `(operator)`, because a third-party reviewer
    is neither the agent nor the operator.
    """
    return f"@{login_of(holder)} ({'agent' if by_agent else 'human'})"
