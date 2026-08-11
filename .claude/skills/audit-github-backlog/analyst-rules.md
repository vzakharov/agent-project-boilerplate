# Backlog analyst rules

**You are a backlog analyst on a whole-backlog audit sweep. Read all of this
before judging anything.** Your bucket, its remit, your item numbers, and where
to write your report come from the prompt that sent you here.

Read `tmp/audit/analyst-context.md` first, and judge every item against what it
says — not against what the item assumes. It is this run's description of the
repo: what shipped, what was retired and what replaced it, what the live
architecture is. An item written against a subsystem that no longer exists is
only judgeable once you know that.

## Where the material is

The threads are already dumped, so **read files — do not hammer the GitHub API.**
Hundreds of items × N agents of `gh api` calls is slow, rate-limited, and blocks
the whole run.

- `tmp/audit/issues/<n>.md` — full thread per open issue: body, labels, dates, all comments
- `tmp/audit/prs/<n>.md` — the same per open PR, plus its base and head refs
- `tmp/audit/rot.md`, `rot.json` — per-PR rot: behind/ahead, files, overlap, gone, merge verdict
- `tmp/audit/pr-history.json` — every PR ever, with `base.ref`

Read the repo itself with Read/Grep/Glob, and use `git` freely (`log`, `grep`, `-S`).

## Verdicts — exactly one per item

| Verdict             | Meaning                                                               |
| ------------------- | --------------------------------------------------------------------- |
| `CLOSE_DONE`        | The work described is done. Cite what did it.                         |
| `CLOSE_NOT_PLANNED` | Obsolete or abandoned — real once, but nobody will do it now.          |
| `CLOSE_DUPLICATE`   | Another issue covers it. **Name it as `#<n>` in your reason.**         |
| `REFILE`            | The framing no longer fits the code: it needs rewriting, not keeping.  |
| `KEEP`              | Still reads true against today's code.                                |
| `UNSURE`            | Needs a human. Say precisely what you could not establish.            |

Write the verdict **exactly** as spelled above. The three closing verdicts are
separate because GitHub's close reason is: they become `completed`,
`not_planned`, and `duplicate` respectively when the plan is executed. A bare
`CLOSE` is rejected as malformed — "closed, reason unstated" is what this
replaced. Choose honestly: a wrong-but-plausible `CLOSE_DONE` is worse than an
accurate `CLOSE_NOT_PLANNED`, because it claims work exists that does not.

Two rules, not preferences:

1. **Age is never a reason to close.** An old issue that still reads true is
   `KEEP`. Some issues get _worse_ while sitting — if a duplicate count or a
   scope has grown since it was filed, say so.
2. **`REFILE` is a framing mismatch, not a wish.** "Still a good idea, nobody did
   it" is `KEEP`. `REFILE` is for an item whose named paths, symbols, or
   architecture are gone.

## Evidence standard — a verdict without evidence is discarded

Cite a path, a line, a grep result, or a commit SHA. Establish, concretely: do
the named files still exist; do the named symbols; does the described
duplication/bug/gap **still** exist; was it already fixed
(`git log --oneline --all --grep '#<n>'`, `git log -S'<symbol>'`); is a newer
open issue already covering it.

Effort scales to age: for items touched in the last two weeks, confirm they are
still live and surface the exceptions rather than deep-diving each.

## Hard read-only boundary

You may read anything and write **only your own report file**. Do not close,
comment on, label, reopen, assign, or edit any issue or PR; do not push, commit,
or run any `gh` command that writes. If you think something should be closed,
that is what your verdict is for.

## Watch for, and call out in your report

- an **umbrella issue whose own body is the only record of the work** — its
  children were never filed as issues, so closing it deletes them; they have to
  be filed separately first
- a **parent whose sub-issues _are_ filed and still open** — the opposite
  problem: the children exist, but they hang off the parent through an API-only
  link, so it reads as finished until you ask
  (`/repos/<owner>/<repo>/issues/<n>/sub_issues`)
- **unfinished security verification**, and **production data repairs that never
  ran** — never `CLOSE` these; a closed-child count can overstate how closed a
  gate is
- **product signal sitting in auto-filed prose** that is tracked in no issue
- **`TODO(#n)` comments** in the code referencing an item you judge `CLOSE`
- a **merged PR that did not actually finish** the issue it references ("schema
  only", "slice 1", "split from"), or that merged to a non-default base

## Output format

Write to the report path your prompt gave you. Two parts, in this order:

1. One `###` section per item: `### #<n> — <title>`, then your verdict, the
   evidence you established (with paths/lines/SHAs), and anything the
   coordinator needs to know.

2. A **final `## Summary` table**, the last thing in the file, in exactly this shape:

```
## Summary

| Item | Verdict | Reason |
|---|---|---|
| #123 | CLOSE_DUPLICATE | Duplicate of #99; `src/foo/bar.ts:12` is the gap both name. |
| #124 | KEEP | `src/x.ts:40` still hand-rolls the parser. |
```

The table is parsed mechanically, so: one row per item you were given and no
others; `#<number>` in the first column; the verdict verbatim in caps; a
one-line reason citing evidence. Escape any literal `|` inside a reason as `\|`.
If you write more than one `## Summary` heading, the **last** one is taken as
your settled position.

---

If following these rules turns up something they get wrong — a trap they do not
warn about, a step that misfires on this repo — say so at the end of your
report. The coordinator collects those for the operator; see `SKILL.md` §
"This is a living document".
