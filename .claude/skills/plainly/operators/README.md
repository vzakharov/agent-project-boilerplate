# Operator entries

How individual people want to be talked to. `.claude/hooks/session-start.sh`
resolves the session's operator at startup and prints their entry into the
session, so an entry reaches you already applied to the reply you are writing —
you do not come here to read one. **What an entry may and may not do is
`@.claude/skills/plainly/voice.md`'s**; the short of it is that an entry tunes
manner and never substance.

## The format is the filename

`<handle>.md`, lowercase, and the file's whole content is the entry — no
headings, no front matter, nothing to malform. Bullets are the convention, one
short line per preference:

```markdown
- Return the banter rather than filing it.
```

`default.md` is the one reserved name: where it exists, it is printed for
everyone, before whoever's own entry. Use it for a manner rule that holds across
the team, not as somewhere to put a person who has no entry.

Lowercase because GitHub handles are case-insensitive while filenames here are
not — the hook lowercases the login it resolves, so `VZakharov.md` would be
looked up and missed. `scripts/check-operator-entries.sh` holds the directory to
that.

## Writing one

**When someone states a standing preference about how you talk to them, write it
down here** — that is how a preference outlives the session it was mentioned in.
Ask first only where it is genuinely ambiguous whether they meant this reply or
every reply from now on.
