## Operator entries

How individual people want to be talked to, applied on every reply to that
person. **What an entry may and may not do is
`@.claude/skills/plainly/voice.md`'s** — read it before writing one; the short of
it is that an entry tunes manner and never substance.

`.claude/hooks/session-start.sh` reads this file at startup and prints the
current operator's entry into the session, which is why nothing imports the
whole file: one session needs one entry. So the headings are load-bearing —
`### @<handle>`, exactly, or the entry under it reaches nobody.
`scripts/check-operator-entries.sh` holds them to that.

**When someone states a standing preference about how you talk to them, write it
down here** — that is how a preference outlives the session it was mentioned in.
Ask first only where it is genuinely ambiguous whether they meant this reply or
every reply from now on.

```markdown
### @<github handle>

- <one line per preference — manner only>
```

### @vzakharov

- Return the banter rather than filing it. A joke gets a joke back, or gets
  passed by — never a paragraph about the joke.
