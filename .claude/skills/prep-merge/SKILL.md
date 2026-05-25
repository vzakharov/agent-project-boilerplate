---
description: Land prep — verify there's a draft PR, run the local gates, merge main, mark ready for review, propose a squash title/body, then watch CI.
---

**Pre-check**:

- If `HEAD` is detached, create a branch with a meaningful name derived from the work (e.g., task id or topic) and check it out.
- Run `gh pr view --json isDraft,number,url` on the current branch.
  - No PR → push the branch and create a **draft** PR (`gh pr create --draft`).
  - PR exists but is non-draft → convert it back to draft (`gh pr ready --undo`).
  - Draft PR exists → continue.

**Two-shot rule**: on any failure, try up to two rounds of fixing, then stop and ask the user. Commit after each round of fixes.

If your project distinguishes a lighter check for doc-only changes (e.g. a separate `format:fix` or doc-lint target), swap accordingly throughout the steps below.

Steps (stop on first unresolved failure):

1. **Local gates**: `./scripts/gates.sh`. Fix and rerun until green. (See `CLAUDE.md` → Local gates for what this should cover — implement the script for your stack if it's still a stub.)
2. **Merge main**: `git fetch origin && git merge origin/main`. Resolve conflicts; if you can't, ask.
3. **Issue export cleanup**: If `docs/issue/<n>/` exists on the branch, delete that tree and include the deletion in the **last** pushed commit before step 4. The export was committed earlier by `@.claude/skills/issue/SKILL.md` on purpose — while the branch is in flight, any agent that resumes it (post-compaction handoff, parallel session) reads the full thread from there instead of re-fetching. Deleting it now is intentional: paired with the earlier add, it cancels out in the squash to `main`, so the issue export rides the branch but never lands. Do **not** skip this step — leaving the folder in means it ships to `main`.
4. **Ready for review**: `gh pr ready`.
5. **Suggest squash message**: read `git log origin/main..HEAD` and the PR description, propose a descriptive title + body explaining what & why. Print for the user to approve.
   - Title must follow conventional commit format: `<type>: <subject>` (`feat`, `fix`, `refactor`, `docs`, `chore`, `style`, `test`, `ci`, `perf`). No scope or extra words between the prefix and the colon.
   - If the PR or any part of the diff references a GitHub issue, end the body with `Closes #N` (for `feat`/`refactor`/etc.) or `Fixes #N` (for `fix`).
   - Print the title and the body as two **separate** fenced code blocks (so the UI offers a copy button on each).
6. **Watch CI**: monitor the run on the head commit until it finalizes (`gh run watch <run-id>` is the simplest path; use `gh run list --branch <branch>` to find the latest run id).
   - On success:
     - `git fetch origin` and check whether `origin/main` advanced past the merge base since the CI run started. If it didn't, report the green run and **stop**.
     - If it did, the green CI no longer reflects what would actually land. A clean merge (no conflicts) does **not** mean the code is compatible — semantic incompatibilities (renamed exports used elsewhere, changed function signatures, altered runtime invariants) merge cleanly and still break. Re-run step 2 (`git merge origin/main`), then step 1 (gates), push, and re-watch CI. Repeat until CI finishes green with `origin/main` unchanged during the run. The two-shot rule does not apply to these main-advanced re-runs — they're not failures, they're keeping the test target current.
     - Exception: if `origin/main`'s advance is **clearly inert to CI** — touches only paths that no CI job exercises, like `/docs/`, top-level markdown, or read-only reference data — merge, push, and **stop** — no re-CI needed. The bar is "no test/lint/typecheck job can possibly read this", not "I think it looks safe": if you'd have to read the file to be sure, it doesn't qualify.
   - On failure:
     - if the failure analysis suggests flakes (timeouts, network, known-flaky tests, infra hiccups — not a real code defect), `gh run rerun <run-id> --failed` and re-watch instead of patching code
     - otherwise: re-run step 2 if `origin/main` advanced, then re-run step 1 (gates), then re-watch CI (two-shot rule still applies)
     - exception: same as the success-path exception — if the new conflicts touch only paths CI cannot exercise (docs, top-level markdown, read-only reference data), resolve conflicts, push, and **stop** — no re-CI needed
   - Do NOT merge the PR — the user controls the final title/body and merge.
