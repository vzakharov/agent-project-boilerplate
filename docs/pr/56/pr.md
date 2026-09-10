# PR #56: feat: #55 label agent-authored comments in the export

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/56
- **Author:** @vzakharov (agent)
- **Base ← Head:** main ← claude/55-label-agent-comments-quhi8e
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-10T21:11:54Z
- **Updated:** 2026-09-10T21:16:24Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **Plan only — no implementation yet.** This PR carries the issue export (`docs/issue/55/`) and the plan (`docs/plans/55-label-agent-comments.draft.do-not-implement.md`) so the approach can be reviewed as a diff before any code is written.
- **The work:** move the agent-vs-operator discrimination out of `/handle`'s prose and into `scripts/export-github-item.py` — detect the Claude Code attribution footer on a comment body, label the comment in the export, strip the matched footer, and cut the string-test paragraph from `.claude/skills/handle/SKILL.md` § "Step 2".
- **The plan corrects the issue's proposed seam.** #55 suggests hanging the label off `markdown.py`'s `login_of()`; that function receives the nested *user* object, not the comment, so it cannot see the body the footer lives in. The label hangs off a new body-level helper (`gh_export/authorship.py`) instead, called at the sites that actually hold a body — which is also why the timeline needs no change (its events carry no bodies).
- **Two decisions worth a reviewer's attention:** the label reads `(agent)` / `(human)` rather than the issue's literal `(agent)` / `(operator)`, because `(operator)` is a false claim on a third-party reviewer's comment; and the repo has no Python test hook today, so the plan adds a stdlib `unittest` suite plus a `vet.sh` line to assert the acceptance criteria.
- **Rider folded in:** a bare `<issue title> #<N>` session prompt routes to `/issue`, the same as a literal invocation. Sectioned separately in the plan so it can be rejected independently.

## QA Checklist

- [ ] `plan-approach` — read `docs/plans/55-label-agent-comments.draft.do-not-implement.md` and confirm the module seam (`authorship.py` holding a body-level footer test, `login_of` left alone) is the one you want.
- [ ] `label-vocabulary` — decide open question 1: `(agent)`/`(human)` as planned, `(agent)`/`(operator)` per the issue's literal acceptance criterion, or `(agent)`-only with absence meaning human.
- [ ] `test-hook` — decide open question 2: whether the exporter gets the repo's first `unittest` suite plus a `vet.sh` line, or the criteria are verified by hand and nothing is committed.
- [ ] `rider-scope` — decide open question 3: whether the `<title> #<N>` routing rule ships here or separately.
- [ ] `dry-notes` — confirm the `## DRY notes` section's calls, in particular that the four call sites interpolate a shared `@login (label)` fragment rather than a shared header builder.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `plan-approach` | No | n/a | Design review; the point of publishing the plan as a diff. |
| `label-vocabulary` | No | n/a | Operator decision. Plan is written with `(agent)`/`(human)` in force, so silence resolves it. |
| `test-hook` | No | n/a | Operator decision. Recommendation in force; declining leaves the issue's "nothing asserts the footer survives" complaint standing. |
| `rider-scope` | No | n/a | Operator decision; rejecting it leaves the rest of the plan unchanged. |
| `dry-notes` | No | n/a | Required by CLAUDE.md; reviewable as prose only. |

Closes #55

---

## Comments

### Comment by @vzakharov (agent) on 2026-09-10T21:12:27Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/56#issuecomment-5625507660](https://github.com/vzakharov/agent-project-boilerplate/pull/56#issuecomment-5625507660)

Proposed squash title/body:

```
feat: #55 label agent-authored comments in the export (pr #56)
```

```
`$GH_TOKEN` is the operator's own identity, so an agent's reply and
the operator's guidance reach GitHub under one `@login`. Only the
Claude Code attribution footer separates them, and `/handle`'s review
lane — whose tail test asks whether a thread's newest comment is
guidance nobody has answered — was reading for it by eye, as prose
instructing the agent to notice a string. That fails in the expensive
direction either way: a missed footer re-works an answered thread, an
imagined one skips guidance addressed to the agent.

The export now decides it. A body-level footer test labels every
rendered comment `(agent)` or `(human)` beside its raw login, strips
the matched footer, and matches only a trailing one, so a quoted
footer mid-body reads as human. The label sits on a new
`gh_export/authorship.py` rather than on `login_of()`, which receives
a nested user object and so cannot see the body the footer lives in;
the timeline needs no label, its events carrying no bodies. `(human)`
rather than `(operator)` because a third-party reviewer is neither the
agent nor the operator. The footer stays mandatory on every
agent-authored post, now as the machine-read signal rather than a
courtesy, and `authorship.py` is where that is written down.

`/handle` § "Step 2" cites the label instead of explaining the test.
Asserting any of this needed a Python test hook the repo did not have,
so the exporter gets a stdlib `unittest` file and `scripts/vet.sh`
gains the line that runs it. A session prompt that is a bare
issue title ending in `#<N>` now invokes `/issue`, which is what the
operator means by it.

Closes #55

Co-authored-by: Claude <noreply@anthropic.com>
```

---

