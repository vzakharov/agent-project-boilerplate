# CLAUDE.md

## About this project

> _Replace this stub with a short description of what this codebase is and why it exists._

## About this file

This file is intentionally bare. It carries only the conventions that hold true regardless of stack. As the project's actual conventions emerge — directory layout, testing approach, naming patterns, deployment quirks, recurring pitfalls — flesh out the relevant sections below.

**Agent: this is yours to grow.** When you notice a pattern worth codifying, a trap worth warning about, or a tool/command that should be documented, propose the addition. Treat CLAUDE.md as a living artifact you and the human co-author over time — not a fixed doctrine to obey. The principles in "Key principles" below are the seed; everything around them should grow with the project.

## Repository layout

> _Document the top-level directories and what they're for as the layout stabilizes._

## Local gates

Local gates are the fast checks the agent runs *before pushing* to save CI minutes — typically lint, type-check, format-check, and any tests fast enough to run in seconds. Entrypoint: `./scripts/gates.sh`.

**Action required when starting a new project**: implement `scripts/gates.sh` for your stack. Examples:

```bash
pnpm lint && pnpm typecheck && pnpm test:unit       # Node / pnpm
cargo clippy --all-targets -- -D warnings && cargo test   # Rust
ruff check . && mypy . && pytest -q                 # Python
go vet ./... && go test -short ./...                # Go
```

Until it's implemented, skills that depend on it (notably `prep-merge`) will stop loudly.

**Keep it current** as tooling evolves. If a CI job catches something `gates.sh` should have caught, that's a signal to extend it.

**Do not run gates before every commit** on feature branches — it's wasteful, especially in remote/web sessions. Gates run at milestones: before pushing review-ready work, before flipping a PR to ready. `prep-merge` is the canonical caller.

## Key principles

- **No "MVP" mindset.** Aim for production-grade durability from day one. Don't cut corners with "we'll fix it later" reasoning. Design decisions should be durable.
- **Don't replace what already works.** Only swap a tool or service for a concrete problem with it, not on aesthetics or novelty.
- **Never add lint-suppression comments without explicit user confirmation.** This includes `eslint-disable`, `# noqa`, `# type: ignore`, `// nolint`, and equivalents in any language. When a lint rule flags code, fix the code to satisfy the rule. If the rule is genuinely wrong for that case, ask the user before suppressing. **Exception for test files:** file-level suppression is acceptable when the disabled rules relate to mocking mechanics that conflict with test setup. Do not suppress rules that flag real code quality issues even in tests.
- **Linters are signals, not puzzles to game.** Do not contort the architecture solely to silence a rule when a clearer approach exists. Rules exist to keep the codebase consistent and safe — work _with_ them, not around them in a hacky way.
- **Ignore IDE diagnostics until local gates.** Do not react to or try to fix type errors, lint warnings, or other diagnostics that appear in IDE context during implementation. IDE servers can lag behind file changes and produce stale or misleading errors. `./scripts/gates.sh` is the single source of truth for correctness — only fix errors it reports.
- **Don't revert unexpected mid-execution changes.** If new code, comments, or edits appear in files during execution, they're most likely from the user editing concurrently. If the context makes it clear they're user-made, preserve them without asking. If genuinely unclear, ask before touching them — but never silently revert.
- **Don't spin on typing/linting errors.** If a type error or lint issue resists 2–3 straightforward fix attempts, stop. Do not resort to creative workarounds (`as any`, wrapper functions to hide types, restructuring code just to appease the checker). Ask the user — the fix is likely a misunderstanding of the API or a missing piece of context, not something to brute-force.
- **Never silently swallow errors.** On primary code paths, errors must propagate — logging alone isn't enough. A logged-and-continued error is a silent fail with paperwork. Silent fallbacks are acceptable only for secondary fire-and-forget operations where failure demonstrably cannot affect the user-facing result, and only with explicit user approval for the specific call site.
- **Validate at boundaries.** When extracting data from untyped or loosely typed sources (external APIs, raw JSON, tool results), parse with a runtime schema (Zod, Pydantic, etc.) instead of asserting/casting. A cast hides shape mismatches at runtime; a parse surfaces them immediately. Don't re-parse data that's already type-safe inside the program.
- **Keep production files under ~450 lines.** Rule of thumb, not a hard cap. Data-dense files (prompt text, fixtures, large catalogs) and top-level orchestrators may reasonably exceed it. When a logic-heavy file climbs well past ~450 lines, look for natural seams (focused helpers, sub-components) rather than letting it grow indefinitely.
- **Don't run Bash with `run_in_background`.** Always run commands synchronously, even long ones. Background tasks have a tendency to stall without an obvious reason — set a long `timeout` on a normal foreground call instead.

## Docstrings

Add a docstring only when the behavioral contract isn't obvious from the function name and types — side effects, runtime constraints, cross-boundary coupling, or "don't change this" traps. If the main reason to document something is that someone might break it while editing, a short inline comment inside the function is enough (the dev will see it while changing the code). Don't document things we're not actively working with — they may change or disappear.

Prefer code clear enough not to need usage examples in docstrings. If an example is the clearest way to convey usage, include one — but a need for examples is often a signal that the API itself could be clearer.

## Derive types and schemas from the source of truth

Never hand-write a type or schema whose shape tracks another declaration — derive it. Hand-written duplicates drift silently and the type checker won't catch it because the duplicate redeclared its own fields.

- Use your ORM/library's derivation utilities (e.g. `drizzle-zod`, Pydantic's `from_orm`, `sqlc`-generated types).
- When a runtime schema exists, infer the type from it rather than declaring a parallel type.
- For enums, define the values as a `const` array and derive the typed schema from it (`z.enum(VALUES)`, equivalents in other stacks). Use the array's element type for dispatch maps so the compiler enforces exhaustiveness.

## Testing

> _Document the chosen testing stack and conventions here as they're decided._

Universal guidance regardless of stack:

- **Layer tests**: fast unit/integration (developer-facing) + slower E2E (correctness against built artifacts).
- **Authorization/permission code must have tests.** Bugs there are security vulnerabilities.
- **Mock at HTTP boundaries**, not at internal functions. Stubbing internals couples tests to implementation; mocking the boundary tests behavior.

## GitHub comments

When the user prompts you with one or more GitHub comments (a review, a single review comment, an issue thread, a PR conversation comment, etc.), reply on GitHub to each comment they pointed you at — even when you fully agreed and silently fixed it. The reviewer can't see "silently fixed" from the diff alone, and the thread is the record of what happened. Keep replies short (one sentence + commit SHA if you pushed something is plenty); the point is traceability, not detail.

## Git conventions

Use semantic commit prefixes:

- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation changes
- `chore:` — maintenance, config, dependencies
- `refactor:` — code restructuring without behavior change
- `style:` — formatting, whitespace (no code change)
- `test:` — adding or updating tests
- `ci:` — CI/CD changes
- `perf:` — performance improvements

Write descriptive commit messages: the subject line summarizes the change, and the body explains what was changed and why in enough detail that someone reading the log understands the commit without looking at the diff.

**On a feature branch in a remote/web environment** (typically signalled by a branch named `<vendor>/<autoname>`), commit and push proactively after each meaningful unit of work — don't wait to be asked. The operator is usually reviewing from a different machine than the VM the agent runs on, so they can only see the work once it's pushed.

**Do not run local gates before every commit on feature branches.** Gates run at milestones via `prep-merge`. See "Local gates" above.

## Keeping docs in sync

- **Plan drift**: When work deviates significantly from your plan docs, update them to reflect actual progress and revised ordering. The plan is a living document, not a stale ideal.
- **Decision-doc consistency**: When revising a decision (e.g., renaming a convention, changing a tool choice), update all docs that reference the old convention.
- **Plan-item voice**: Plan checklist items should read as forward-looking intent (how you'd phrase them _before_ doing the work), not as retrospective reports.

## Working with skills

This project ships a small set of Claude Code skills under `.claude/skills/`. Invoke them as `/<name>` in a session:

- **`/issue`** — take a GitHub issue end-to-end (read, optionally split, implement, open a draft PR).
- **`/prep-merge`** — land prep: run gates, merge main, flip to ready, draft squash message, watch CI.
- **`/from-branch`** — attach the current session to an existing branch or PR, abandoning the auto-created session branch.
- **`/explore`** — investigate the codebase via parallel Explore agents.
- **`/dry`** — review the session's diff for DRY opportunities; applies obvious wins, surfaces ambiguous ones.

Add new skills here as repeated workflows emerge — each as a directory under `.claude/skills/<name>/SKILL.md`. Skills checked into the repo are picked up automatically when Claude Code opens the project.
