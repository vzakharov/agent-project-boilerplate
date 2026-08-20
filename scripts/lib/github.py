"""Shared GitHub plumbing for the stdlib-only scripts in `scripts/`.

Imported as `from lib.github import detect_origin_repo, die, gh_token`. Running a
script as `python3 scripts/<name>.py` puts `scripts/` on `sys.path[0]`, so
`lib.github` resolves as a PEP 420 namespace package from any working directory —
no `__init__.py`, no `sys.path` manipulation. Both callers write output relative
to the caller's cwd while living elsewhere, so that cwd-independence matters.

Deliberately excluded: each script's `USER_AGENT` (they differ, which is how the
two are told apart server-side) and the `DOCS_*_ROOT` output paths.

Stdlib only — no third-party deps. Python 3.9+.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from typing import NoReturn


def die(msg: str, code: int = 1) -> NoReturn:
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
