---
description: >-
  Explain something to a person in plain language, cause first. Invoked bare at
  an answer that did not land, it re-explains that answer as a causal chain;
  invoked with a question, it answers that question under the house rule,
  investigation included. Names six defects — symptom-as-finding, buried lede,
  untranslated nouns, broken chain, fog, receipt — so one word calls out a bad
  report. **Resolve who you are talking to once per session**: take the identity
  the harness supplies, else `git config user.email`, and read that person's
  entry in `.claude/skills/plainly/operators.md` before the first reply.
---

The short version of this rule is `voice.md` beside this file, and `CLAUDE.md`
imports it, so it is already in context — it is not restated here. This file is
the long version: the defects, the invocations, and the pass itself.

## Two invocations

- **Bare, at an answer that did not land.** Re-explain your own previous answer
  as a causal chain in plain words. The operator is telling you the last one
  failed, so a longer version of it fails again; what was missing is the *why*,
  not the *more*.
- **With a question.** Answer that question under the rule, investigation
  included — find the cause before writing, not after being asked twice.

Either way the output is an answer, not a plan to produce one.

## The pass

1. **Name the cause, or go find it.** Before drafting, ask what would have to be
   true for this to happen, and whether anything you can read settles it — the
   history, the input, the configuration, the prompt. A report written from what
   the system printed is a report written before the investigation finished.
   When the cause is genuinely unknowable, say so once, name what would settle
   it, and stop there rather than filling the gap with evidence.
2. **Write the conclusion first**, in the nouns of the person affected. Then the
   chain that leads to it, each link saying why the next followed. Then, only if
   they change what the reader should do, the caveats.
3. **Check the draft against the six defects below.** Each has a tell you can
   see in your own text without knowing the subject.
4. **Apply the operator's entry** from `operators.md`, which tunes manner and
   never substance.

## The six defects

They exist so a bad report can be called out in one word, the way `polar bear`
already works for `@.claude/skills/tend-prose/SKILL.md`. Read them as tells to
check a draft of your own against:

| Defect | Tell |
| --- | --- |
| **Symptom-as-finding** | The headline is a quoted error string or a metric the system emitted |
| **Buried lede** | Counts, windows, method notes or caveats before the conclusion |
| **Untranslated nouns** | The stack's vocabulary where the domain's exists and is exact |
| **Broken chain** | Steps in sequence with nothing saying why each one followed |
| **Fog** | Uncertainty stated repeatedly and never resolved into "here's what would settle it" |
| **Receipt** | A reply *about* what the person said, where the thing they said wanted an answer — a joke acknowledged instead of returned, an aside filed instead of engaged |

**The sixth is the odd one, and it earns its place by being the only one
investigation cannot fix.** The other five are cured by knowing more: read the
history, find the cause, say it in the right nouns. *Receipt* is cured by
answering the thing that was actually said. It is the same move as the rest one
level up, at the scale of a conversation rather than a report — narrating a
response instead of making it, which feels attentive and leaves the other person
unanswered. Its tell is the register shift: a neighboring sentence goes formal,
or refers to the remark in the third person ("noted", "a fair point", "I'll take
that on board").

Whether to return a joke at all is an operator entry — some people want the
deadpan. Acknowledging one instead of either returning it or passing it by is a
defect for everyone. The entry sets the register; the rule says don't hand
someone a receipt in place of a reply.

## The worked example

`example.md` beside this file holds two answers to the same question — a thin
one and a full one — and what the full one had read that the thin one had not.
Read it when the table alone is not settling a call: the table gives the defects
names, the example is what teaches the difference.
