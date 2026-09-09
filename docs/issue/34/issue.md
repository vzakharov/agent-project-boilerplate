# Issue #34: Step 3 asks squash bodies for editing traps, and never says a re-run rewrites

- **State:** open
- **URL:** https://github.com/vzakharov/agent-project-boilerplate/issues/34
- **Author:** @vzakharov
- **Created:** 2026-09-09T01:42:46Z
- **Updated:** 2026-09-09T01:42:46Z
- **Closed:** _not closed_
- **Labels:** _none_

---

## Body

## What happened

A review round on a downstream branch (`vzakharov/vovazakharov.com` PR #31) caught a squash body that had grown a **"Four things to know when editing here"** paragraph — which files a PDF render step hashes, that a card's link is an overlay because anchors can't nest, the shape the type gate can read, which slices a lint exemption covers. Every item true, every item something a person about to break it needs, and none of it what a commit body is read for.

The operator cut it in one line — *"it doesn't belong to a squash message (no one will be accidentally looking into it to figure out how pdfs work)"* — and in the same breath named the second half: *"going forward make sure the message doesn't bloat following our future edits (cut&replace, don't just append)"*.

Both were fixed downstream, in `.claude/skills/squash-message/SKILL.md`: [b5f4bf2](https://github.com/vzakharov/vovazakharov.com/commit/b5f4bf2) adds the two rules, [fa18122](https://github.com/vzakharov/vovazakharov.com/commit/fa18122) works the first one's consequence. This issue proposes adopting them here, since the skill came from this repo and neither cause is downstream-specific.

## Where the first one came from

Step 3's own target sentence asks for it. Current text, `.claude/skills/squash-message/SKILL.md` § "Step 3 — Tighten it in the file":

> The target is **three paragraphs of prose, four at the outside**, inside the measured caps above […] the rest say what it does about it, named at the level of the behavior, contract or module affected, **plus anything that would trip someone editing that area later**.

So the pass that exists to cut the paragraph is the same pass that licensed it. Lens A would have caught a maintenance manual in a commit body on sight; it never got the chance, because the step had asked for one. That is why this isn't model error to prompt around — the agent followed the step and the step was wrong.

`scripts/check-squash-message.sh` doesn't close it either: the paragraph fits inside 50 lines at 72 wide as easily as anything else, so the measured caps pass a body whose content doesn't belong.

## Where the second one came from

Step 2 hands the run a **live file** — the working proposal, already carrying the last refresh's text. Nothing says what to do with it, and the cheapest thing to do with a file that already says most of what you need is append the new scope and leave the rest standing. Two costs, both observed on that branch:

- **The body walks past the cap one push at a time.** No single refresh looks like it overran; several rounds in, it has.
- **Superseded wording stays beside its replacement.** The clearest instance: an earlier round had inverted which CV address is canonical, and the body still carried the old sentence (*"declares `/cv` canonical"* — by then it was the other way round) next to the new one. The record contradicted itself, and nothing in the pass was looking for that.

The size half is the half `check-squash-message.sh` eventually catches, after the fact. The self-contradiction half nothing catches.

## Suggested shape

Two paragraphs, both in Step 3, plus one deletion. The downstream wording, for reference — worth re-tightening against this repo's copy, which has since moved:

**1. Drop the licensing clause** — `plus anything that would trip someone editing that area later` — from the target sentence, and add to the list of what stays out of a body:

> **A trap for whoever edits the area next is not part of the record either.** The log answers what changed and why; nobody opens a squash message to learn which files a render step hashes. A constraint that has to be obeyed goes where the person about to break it is already looking — a `.claude/rules/` file, or a docstring on the thing itself — unless the change _is_ that the constraint now exists. A "things to know when editing here" paragraph is the tell.

**2. Say that a re-run rewrites**, after the scope paragraph:

> **A re-run rewrites; it never accretes.** Step 2 starts from what the file already says, so the temptation on a refresh is to append the new scope and leave the rest — which walks the body past the cap one push at a time and leaves superseded wording beside what replaced it. Cut and replace, and re-apply the cap to the whole body on every run. A proposal that grew every time the branch did is the tell.

## One thing the fix taught, worth carrying with it

Cutting such a paragraph is a **move, not a deletion**, and the assertion that each item already has a home has to be run rather than assumed. Downstream, the agent justified the cut by saying exactly that — and when a later round made it check, three of the four items did have a home and the fourth had none: `scripts/type-overlap-check.README.md` § "Known gaps" listed three positions where an inline shape is invisible to the gate and not the one route params actually sit in, a generic's type argument. The squash body was the only place that constraint had ever been written down, so the tidy cut would have deleted it.

Whether that belongs in the rule's own text or is left as an issue-thread note is this repo's call. The one-line version: *name the home for each item as you cut it; an item with no home gets one first.*

## Not proposed here

The downstream copy of this skill predates several changes on this side (the measured caps, `check-squash-message.sh`, the Lens A subsections). Nothing above depends on that gap, and no part of it should be read as a suggestion to revert them — the two paragraphs slot into the current text as it stands.

---
_Generated by [Claude Code](https://claude.ai/code)_


---


