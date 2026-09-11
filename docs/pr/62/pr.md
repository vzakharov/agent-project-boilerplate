# PR #62: fix: #60 refer to the agent as singular they, not it

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/pull/62
- **Author:** @vzakharov
- **Base ← Head:** main ← claude/60-agent-singular-they-1yx9vu
- **Draft:** yes
- **Merged:** _not merged_
- **Created:** 2026-09-11T00:03:56Z
- **Updated:** 2026-09-11T00:22:19Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## Summary

- **Repoints the nine agent-as-"it" references the loop's prose still carried** to singular **they**, the convention `#59` landed in `CLAUDE.md` § "Language". Four of the nine are the *same sentence* — "a dangling `@`-reference fails silently; the agent follows the surviving prose and skips the step it could not load" — carried independently by `CLAUDE.md`, `/sync-agent-infra`'s catalog, `check-skill-catalog.sh` and `vet.sh`. The rest are `/preview`'s gap-closing note, `/audit-github-backlog`'s feed-findings-down rule, `check-squash-message.sh`'s header, and one straggler each in `README.md` and `ADOPTING.md`.
- **The boundary is the actual work, and most of what the grep turns up is deliberately untouched.** Only the actor takes "they"; a session, a run, a skill, a script, a check, the harness and Claude Code the product are not actors and keep "it". Fifty-four candidate hits survive the sweep for that reason, and the plan lists each one site by site so a later reader re-running the grep does not "finish the job" on the harness's quoted "fix **it** now" or the branch `/finalize` resumes.
- **No standing rule, and no mechanical check** — the issue rules both out explicitly, and the plan's DRY notes agree: stating the boundary takes more room than the sweep and misfires on the "it" cases more often than it helps. The bet is that consistent prose carries the convention into adopting repos the way the rest of the loop's voice already does.
- **`.claude/rules/**` needed nothing.** Its single `agent` mention pronominalizes the *conventions* ("so conventions reach the agent at the moment **they're** relevant") and was already correct.
- Three lines rewrap because the longer pronoun pushes them past the column their neighbours keep. No sentence is restructured beyond pronoun-verb agreement.

## QA Checklist

- [ ] `grep-clean` — re-run the plan's two grep families over `CLAUDE.md .claude scripts README.md ADOPTING.md` and read each surviving hit: every one should be a non-agent "it" (a session, script, check, thread, ref, or the repo itself).
- [ ] `four-copies` — confirm all four copies of the dangling-`@`-reference sentence now read "the step **they** could not load" (`CLAUDE.md:204`, `catalog.md:301`, `check-skill-catalog.sh:7`, `vet.sh:25`). One left behind makes the pronoun read as per-file taste.
- [ ] `left-alone` — spot-check sites the plan names as deliberately untouched and confirm they still say "it": `CLAUDE.md:41` (the setup script), `from-branch/SKILL.md:52` (the harness's quoted rule), `finalize/SKILL.md:32` (the branch).
- [ ] `agreement` — read each changed sentence whole, not just the pronoun: "would conclude **they have** no GitHub access", "close some of that gap **themselves**", and in `/audit-github-backlog` the sentence's other two "it"s (the evidence, the fact) are correctly left alone.
- [ ] `no-rule` — confirm the diff adds no entry to `CLAUDE.md` or `.claude/rules/` codifying singular they, and nothing to `check-skill-catalog.sh`'s assertions.
- [ ] `wrap` — confirm the three rewrapped lines (`vet.sh:25-26`, `audit-github-backlog/SKILL.md:142-143`, `README.md:85-86`) sit within the column their neighbours keep.
- [ ] `vet` — `bash scripts/vet.sh` exits 0. Two of the three scripts edited *are* the vet suite, so this is the direct check on them.

| Item | Automatable | Covered? | Notes |
|------|-------------|----------|-------|
| `grep-clean` | manual-only | — | The boundary is judgement — which nouns are actors. A grep that encoded it would misfire on the "it" cases more often than it would catch a regression, which is why the plan declines to add one. |
| `four-copies` | unit | — | Mechanically checkable (assert the four files agree on the sentence), but the issue rules out adding the check; it would also only ever fire on this one sentence. |
| `left-alone` | manual-only | — | Asserting a negative here means encoding the same boundary, per `grep-clean`. |
| `agreement` | manual-only | — | Subject-verb agreement across a rewritten clause needs a reader. |
| `no-rule` | unit | — | A diff assertion, but a check that forbids a future rule would outlive the reason for it. |
| `wrap` | unit | — | A line-length check over the touched files; the repo wraps by local convention rather than a global column, so a global rule would flag long-standing lines. |
| `vet` | integration | ✅ | `scripts/vet.sh` — ran green on `af52628` (`check-skill-catalog: OK`, `check-squash-message: ok`). |

Fixes #60

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_011ernDJoAGrF4zQgKif9YpV


---
_Generated by [Claude Code](https://claude.ai/code)_

---

## Comments

### Comment by @vzakharov on 2026-09-11T00:04:27Z

[https://github.com/vzakharov/agent-project-boilerplate/pull/62#issuecomment-5627214264](https://github.com/vzakharov/agent-project-boilerplate/pull/62#issuecomment-5627214264)

Proposed squash title/body:

```
fix: #60 refer to the agent as singular they, not it (pr #62)
```

```
The house convention writes about the agent as singular they, and the
tree still had stragglers: the loop's own prose called the agent "it" in
seven places across CLAUDE.md, the skills and the scripts' header
comments.

Repoint each of them. Four are the same sentence about a dangling
`@`-reference failing silently, carried independently by CLAUDE.md,
`sync-agent-infra`'s catalog, `check-skill-catalog.sh` and `vet.sh`
because those surfaces are copied apart from one another; the rest are
`/preview`'s gap-closing note, `/audit-github-backlog`'s
feed-findings-down rule and `check-squash-message.sh`'s header.
`README.md` and `ADOPTING.md` carry one each and travel with them.

Only the actor takes "they". A session, a run, a skill, a script, a
check, the harness and Claude Code the product are not actors and keep
"it", so most of what the grep turns up is deliberately untouched. No
entry in CLAUDE.md or `.claude/rules/` codifies this: stating the
boundary takes more room than the sweep and misfires on the "it" cases
more often than it helps, so consistent prose carries the convention
into adopting repos the way the rest of the loop's voice already does.

Fixes #60

Co-authored-by: Claude <noreply@anthropic.com>
```

---

_Generated by [Claude Code](https://claude.ai/code)_


---

## Review threads

### `.claude/skills/preview/SKILL.md`:26 — unresolved

```diff
@@ -23,4 +23,4 @@ The failure mode this exists to prevent is specific and common: reasoning about
 
 ## Related
 
-`/qa-checklist` classifies some verification steps as `manual-only` precisely because they need a human's eye on pixels; a hydrated `/preview` is what lets the agent close some of that gap itself.
+`/qa-checklist` classifies some verification steps as `manual-only` precisely because they need a human's eye on pixels; a hydrated `/preview` is what lets the agent close some of that gap themselves.
```

**@vzakharov** — 2026-09-11T00:21:50Z

isn't it "themself" for the singular they?

---

## Timeline (status, references, and other events)

- **2026-09-11T00:22:19Z** @vzakharov reviewed (COMMENTED): https://github.com/vzakharov/agent-project-boilerplate/pull/62#pullrequestreview-5173657163.
