#!/usr/bin/env python3
"""Pull a PR body to a transient local file, edit it there, push it back.

Usage:
  python3 scripts/pr-body.py pull <pr-number> [--repo OWNER/REPO]
  python3 scripts/pr-body.py push <pr-number> [--repo OWNER/REPO]

`pull` writes docs/pr/<n>/body.md; `push` PATCHes the PR body from that file and
deletes docs/pr/<n>/.

Editing happens on the local file between pull and push — agents don't
reconstruct the whole body inline (cheap on tokens, and the rest of the body is
preserved verbatim because only the edited region of the local file changes).

Uses the REST API directly, which sidesteps the GraphQL "Projects (classic)
deprecation" error (`repository.pullRequest.projectCards`) that can break
`gh pr edit`.

Auth: uses $GH_TOKEN (or $GITHUB_TOKEN) if set, otherwise falls back to
`gh auth token`.

Stdlib only — no third-party deps. Python 3.9+.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DOCS_PR_ROOT = Path("docs") / "pr"
USER_AGENT = "pr-body.py"


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


def parse_args(argv: list[str]) -> tuple[str, int, str]:
    rest = [a for a in argv[1:] if a != "--"]
    repo_flag: str | None = None
    command: str | None = None
    nums: list[int] = []
    i = 0
    while i < len(rest):
        arg = rest[i]
        if arg == "--repo" and i + 1 < len(rest):
            repo_flag = rest[i + 1]
            i += 2
            continue
        if arg in ("pull", "push"):
            command = arg
            i += 1
            continue
        m = re.match(r"^#?(\d+)$", arg)
        if m:
            nums.append(int(m.group(1)))
        i += 1

    if command is None or len(nums) != 1:
        die("Usage: python3 scripts/pr-body.py <pull|push> <pr-number> [--repo OWNER/REPO]")

    if repo_flag is None:
        repo_flag = detect_origin_repo()
        if repo_flag is None:
            die(
                "Could not determine OWNER/REPO. Pass --repo OWNER/REPO, or run from a "
                "checkout whose `origin` is a github.com repo."
            )

    parts = repo_flag.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        die("--repo must be OWNER/REPO (e.g. octocat/hello-world).")

    return command, nums[0], repo_flag


def api(path: str, token: str, method: str = "GET", payload: Any = None) -> Any:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        f"https://api.github.com/{path.lstrip('/')}",
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        die(f"{method} {path} failed: {exc.code} {exc.reason}\n{exc.read().decode(errors='replace')}")


def body_file(pr: int) -> Path:
    return DOCS_PR_ROOT / str(pr) / "body.md"


def pull(pr: int, repo: str, token: str) -> None:
    view = api(f"repos/{repo}/pulls/{pr}", token)
    path = body_file(pr)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(view.get("body") or "", encoding="utf-8")
    print(path)


def push(pr: int, repo: str, token: str) -> None:
    path = body_file(pr)
    if not path.is_file():
        die(f"No local body at {path} — run `python3 scripts/pr-body.py pull {pr}` first.")
    view = api(
        f"repos/{repo}/pulls/{pr}",
        token,
        method="PATCH",
        payload={"body": path.read_text(encoding="utf-8")},
    )
    shutil.rmtree(path.parent, ignore_errors=True)
    print(view.get("html_url") or f"PR #{pr} body updated.")


def main() -> None:
    command, pr, repo = parse_args(sys.argv)
    token = gh_token()
    if command == "pull":
        pull(pr, repo, token)
    else:
        push(pr, repo, token)


if __name__ == "__main__":
    main()
