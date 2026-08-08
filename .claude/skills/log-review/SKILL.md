---
description: "STUB — not yet hydrated for this project. Read the deployed application's logs since the last review, report what they say about how it's actually being used, and triage what looks broken. Hydrate this file against the project's logging and hosting setup before invoking it."
---

> ⚠️ **STUB.** This skill has no working procedure yet. Before it can be invoked, fill in: where logs live and how to query them, how the review window is determined, and where triaged findings go. Delete this banner once you have.

## What this skill is for

Two different jobs that share one input:

- **A qualitative readout** — what are people actually doing with this thing? Which paths are hot, which features nobody touches, where do sessions end. This is the part that can't be replaced by an alert.
- **Health triage** — what's erroring, how often, and is it new.

Both come from the same log sweep, which is why they're one skill rather than two.

## Concerns that hold regardless of stack

| Concern | What a hydrated version must handle |
|---|---|
| **A window since the last run** | Reviews cover a period, and the period has to start where the previous one ended. Decide how that boundary is recorded (a timestamp in a tracked file, the last review's issue, a cursor) — without it, every run either re-reports the same week or silently skips days. |
| **Two outputs, kept apart** | Don't fold the usage readout into the error list. They have different readers and different half-lives: the readout informs product decisions, the triage produces work items. |
| **Dedupe into tracked issues** | A recurring error should attach to the existing issue for it, not generate a new report every review. Say how a finding is matched to an existing issue and what happens when it doesn't match (`/propose-issue` is the natural chain here). |
| **Interactive vs. unattended** | Run by hand, the skill can ask the operator to judge an ambiguous pattern. Run on a schedule, it can't — it must decide, or file something the operator can decide from later. Say which mode is which and what changes between them. |
| **PII when quoting** | Logs contain user data. Quoting a raw line into an issue or a PR comment republishes it somewhere with different access rules. Decide what may be quoted verbatim, what must be redacted, and where the redaction happens. |

## Related

`/propose-issue` is the natural sink for triaged findings — it dedupes against existing open issues rather than filing another copy.
