How to write for a person, stated as a shape rather than a mood, so a violation
is visible rather than a matter of taste:

- **The first sentence is the cause, in the reader's words.** Evidence, counts,
  timelines and caveats come after the conclusion they support, never before it.
- **Not knowing the cause is unfinished work, not a style constraint.** Go read
  the thing that would settle it — the data, the input, the history — before
  reporting. If it is genuinely unknowable, say so once, name what would settle
  it, and say what that would take.
- **Use the nouns of the person affected**, not the ones the error message used,
  whenever both name the same thing.
- **State the chain, not the steps.** Every step says why the next one followed;
  a sequence with no *because* in it is a list, not an explanation.
- **Length is not thoroughness.** A report that takes five screens to reach its
  point has failed even when every line in it is true.
- **Frustration is a signal, and it is about you.** Repeated punctuation, caps,
  a re-asked question, "just tell me" — read it as a report that the last answer
  did not land. Do not answer it with more detail. Answer the question that was
  actually asked, from the cause, in shorter words.

This governs the **human-facing** and **conversation** groups that `CLAUDE.md`
§ "Language" partitions: chat replies, and the GitHub prose a person reads to
decide something — PR bodies, issue comments, review replies. Agent-facing prose
answers to `@.claude/skills/tend-prose/SKILL.md` instead, and commit subjects
answer to § "Git conventions".

**Resolve who you are talking to once, at the start of a session.** Take the
identity the harness supplies; when it does not supply one, run the single
lookup that settles it (`git config user.email`) and carry the answer for the
rest of the session rather than re-deriving it per reply. No entry for that
person means this rule alone, which is a complete instruction on its own.

`@.claude/skills/plainly/SKILL.md` is the long version — the six named defects,
the invocations, and the pass. Read it for a borderline call, not on every reply.
