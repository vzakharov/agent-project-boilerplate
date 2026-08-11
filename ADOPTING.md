# Adopting this agent infrastructure

**You are probably an agent, reading this from a temporary clone.** This file is
the acquisition procedure. It is read once, over the network, and is **never
copied into the adopting repo** — nothing here describes how to work in your
project, only how to get the infrastructure into it.

The inventory lives in [`docs/catalog.md`](docs/catalog.md): one row per skill,
script and file, with the criteria for deciding whether you need it. This file
does not restate what any skill does; it cites catalog rows. Read them together.

Two ways in. Pick the one that matches how you got here:

- **[Adopt into an existing repo](#adopt-into-an-existing-repo)** — the repo
  already exists and has its own history and conventions. You select a subset
  and merge it in.
- **[Template fork](#template-fork)** — you used GitHub's *"Use this template"*,
  so every file is already present. Your work is pruning and hydration, not
  selection.

Both converge on the [shared tail](#shared-tail-both-modes), which is where the
four steps they have in common are written once.

## Adopt into an existing repo

### Step 1 — Clone this repo somewhere temporary

```bash
git clone --depth 1 https://github.com/vzakharov/agent-project-boilerplate \
  <scratchpad>/boilerplate
```

Into your session's scratchpad or `tmp/` — **not** anywhere that will be
committed.

Plain `git clone`, never `gh repo clone`. This repo is public and git transport
is not gated on your session's repository scope, so this is the one step that
cannot fail on session configuration — verified working unauthenticated and
against a repo outside the session's scope.

`--depth 1` is right here and **wrong for `/sync-upstream`**, which needs full
history to resolve its watermark SHA. Don't carry this flag over to that skill;
it has its own clone recipe and its own warning about `--depth`.

### Step 2 — Profile the target repo; don't interrogate the human

Most adoption criteria are decidable by inspection. Answer what you can from the
repo itself, and only ask about what it genuinely cannot tell you.

**Use only proxy-safe probes.** You are running in a repo with no `gh` shim
installed — the shim is part of what you are adopting — so this step must work in
a vanilla session. Every command below is verified to work in exactly that
condition.

```bash
# Is this a GitHub repo, and which one?
git remote -v

# Script prerequisites (G2/G3 need these).
python3 -V; command -v jq; command -v gh

# Does CI run here?
ls .github/workflows 2>/dev/null

# Existing agent config to merge with rather than overwrite.
ls -a .claude 2>/dev/null; ls CLAUDE.md 2>/dev/null
```

For anything needing the API, use the **REST form** — `gh api repos/{owner}/{repo}/…`:

```bash
R=<owner>/<repo>

gh api "repos/$R" --jq .visibility            # capability probe — see below
gh api "repos/$R" --jq .allow_squash_merge    # does the squash discipline apply?
gh api "repos/$R" --jq .default_branch        # the trunk G2 assumes
gh api "repos/$R/issues?per_page=1" --jq length         # is work tracked as issues? (G3)
gh api "repos/$R/actions/workflows" --jq .total_count   # is there CI? (G5)
```

**No `gh <noun> <verb> --json` forms at this step.** `gh repo view --json`, `gh pr
list` and `gh issue list` are GraphQL, and in a proxied web session they fail:

```
HTTP 403: This GraphQL query is not enabled for this session — only the pinned
set of PR-review operations is served. Use REST via `gh api repos/{owner}/{repo}/...`
instead.
```

That 403 is **not a blocker — it is a finding.** It is the diagnostic signature
of a proxied web session, which is positive evidence that G4 is needed. The error
text names its own workaround.

> **Never use `gh auth status` to decide whether `gh` works.** In a session where
> `gh api` works fine it reports *"Failed to log in to github.com using token
> (GH_TOKEN) … The token in GH_TOKEN is invalid"* alongside *"Active account:
> true"*. An agent trusting that would conclude it has no GitHub access and
> abandon or downgrade the adoption for no reason. The honest probe is
> `gh api repos/{owner}/{repo} --jq .visibility` — if it prints a visibility,
> `gh` works.

**What the repo cannot answer — ask, briefly:** whether sessions run on Claude
Code web/remote (this decides G4), and whether the project has a deploy path, a
visual surface, deployed logs, a production datastore, or sequential numbered
migrations (these decide the individual G6 stubs).

### Step 3 — If this is a web/remote session, settle G4 before copying anything

Do this **first**, not last. An adopter who leaves it to the end finishes the
whole procedure and then discovers that `/pr` 403s on first use.

The adopted skills call GraphQL-flavored `gh` freely (`gh pr view --json`, `gh pr
list`, `gh issue list`). Without the shim, those fail exactly as Step 2 showed.
So on the web, G4 is a **prerequisite of G2, G3 and G5** — not a nicety.

**To adopt it**, copy `.claude/hooks/session-start.sh` and merge
`.claude/settings.json` (see the [G4 catalog
rows](docs/catalog.md#g4--remote-session-plumbing)), then install the shim for
the *current* session so the remaining steps and the newly-adopted skills have a
working `gh`.

#### What the shim does, and why you may object to it

The shim at `$HOME/.local/bin/gh` runs the real `gh` binary under
`env -u HTTPS_PROXY -u https_proxy`.

**Your own default guidance probably tells you never to unset `HTTPS_PROXY`.**
That conflict is real and worth naming rather than hoping you don't notice it:
from where you sit, this looks like being asked to defeat an egress control. The
case for it:

- The proxy's egress policy blocks long-polling calls and most of `gh`'s GraphQL
  surface, which is what breaks the skills — not a security property you would
  want to preserve.
- The shim scopes the unproxying to `gh`, which talks only to GitHub hosts. git
  keeps the proxy. Everything else keeps the proxy.
- It is checked-in, reviewable configuration owned by the repo, not a runtime
  argument you are being talked into.

**Decide knowingly.** If you are not satisfied, decline it — the procedure is
built to finish without it.

#### If you decline G4

Adoption **never hard-depends on the shim**. This file's own steps are
proxy-safe REST throughout, so declining costs you nothing here. What it costs
downstream is scoped and stated:

- The `gh`-heavy skills need their GraphQL-flavored calls rewritten into the REST
  forms that work through the proxy (`gh api repos/{owner}/{repo}/…`).
- `gh run watch`-style long-polling does not work at all, so `/watch-ci` (G5) is
  unavailable rather than degraded.

Making those skills proxy-safe at the source — which would remove this dependency
and this decision entirely — is tracked separately; see
[Known gaps](#known-gaps).

**Record the decision either way** in `upstream.json`'s `declined` map with the
reason, so re-sync stops re-offering it. Then finish the procedure and **say what
you skipped** in your report.

### Step 4 — Pick groups from the catalog, resolve the closure, copy

Read [`docs/catalog.md`](docs/catalog.md) and decide group by group, using the
Step 2 profile. Then, before copying, resolve each chosen group's **Pulls in**
column — a skill copied without the siblings it `@`-references leaves a pointer
to a file that isn't there, and that failure is silent: the agent follows the
surviving prose and skips the step it could not load.

The catalog's [Closure is not
optional](docs/catalog.md#closure-is-not-optional) section lists the four
counter-intuitive cases. Don't re-derive them.

Copy the resolved set from the clone into your repo. Then continue to the shared
tail.

## Template fork

*"Use this template"* already gave you every file, so there is nothing to select
and nothing to clone — your work is removing what doesn't apply and hydrating
what does.

1. **Delete the `never` rows.** `README.md` (replace it with your project's),
   `ADOPTING.md`, `docs/catalog.md`, and anything under `docs/plans/` or
   `docs/remove-before-merging/` — see the [Never
   rows](docs/catalog.md#never). They describe or maintain the template.
2. **Prune the groups you don't need**, using the catalog exactly as the
   subset-adoption path does — the criteria are the same, you are just deleting
   instead of copying. Resolve the closure in reverse: if you delete a group,
   strip the `@`-references pointing into it.
3. **Fill in the "About this project" stub** at the top of `CLAUDE.md`.
4. **Implement dep-install in `.claude/hooks/session-start.sh`** so remote
   sessions start with a current `node_modules` / `venv` / equivalent. The `gh`
   shim half already works.

Then continue to the shared tail.

## Shared tail (both modes)

### Reconcile `CLAUDE.md` rather than overwrite it

Your repo already has conventions, or will. The boilerplate's `CLAUDE.md` is a
**seed upstream and a donor downstream**: take its sections, merge them into
yours, and keep your stack-specific content. Overwriting is the one way to make
adoption a regression.

Replace the remaining stubs — repository layout, testing — as those conventions
stabilize, and add `.claude/rules/` files as area-specific conventions emerge
(the mechanism ships with a README and no rules).

### Implement `scripts/vet.sh`

Point it at lint/type-check/test commands your repo already has:

```bash
pnpm lint && pnpm typecheck && pnpm test:unit             # Node / pnpm
cargo clippy --all-targets -- -D warnings && cargo test   # Rust
ruff check . && mypy . && pytest -q                       # Python
go vet ./... && go test -short ./...                      # Go
```

The shipped stub **exits `1` by design**, and six skills invoke it —
`/finalize` stops loudly until you do this. It is a
[`rewrite`](docs/catalog.md#three-dispositions-not-two), not a choice: there is
no version of the PR loop that does not run your checks.

### Hydrate or delete the G6 stubs

Go through the [G6 rows](docs/catalog.md#g6--stack-stubs). Hydrating one means
writing your project's real commands in and **deleting the banner** at the top.

**An unhydrated stub is worse than a missing skill** — half-following one against
a project it was never written for beats not having it only in appearance. Delete
the ones that don't apply; three of them tell you when deleting is the right
answer outright (no visual surface, no CI-only tests, no numbered migrations).

### Repoint the sync watermark

`.claude/skills/sync-upstream/upstream.json` is a
[`rewrite`](docs/catalog.md#three-dispositions-not-two). Write it for **your**
repo — inheriting the clone's copy points your sync at a repo you cannot read and
sets `lastSyncedSha` to a foreign history, which surfaces one sync later as an
unresolvable SHA.

```json
{
  "repo": "vzakharov/agent-project-boilerplate",
  "lastSyncedSha": "<this repo's HEAD at the moment you cloned it>",
  "lastSyncedAt": "<YYYY-MM-DD>",
  "adopted": ["CLAUDE.md", ".claude/skills/pr/", "scripts/check-merge.sh"],
  "declined": { ".claude/skills/issue/": "we track work in Linear, not GitHub issues" }
}
```

- `repo` is where you took this from — this repo, for a first-generation adopter.
- `lastSyncedSha` is the HEAD you cloned (`git -C <scratchpad>/boilerplate rev-parse HEAD`).
  Recording it now is what makes the *next* sync a small diff instead of a
  re-triage of everything.
- `adopted` lists what you actually took, at whatever granularity is true —
  directories or files.
- `declined` maps path → why-not. Fill this in as you go; it is what keeps
  re-sync quiet, and it records the *reason* so a later sync can notice when the
  reason has stopped being true.

From here on, pulling later changes forward is just `/sync-upstream` — the same
command this repo uses to track *its* own source. Nothing further to install.

### Verify

Run these before reporting done. Each one corresponds to a way adoption fails
silently:

1. **No reference dangles**: `bash scripts/check-skill-catalog.sh` exits `0`.
   Downstream it runs its first assertion only (there is no `docs/catalog.md` in
   your tree, by design) — and that assertion is the whole point here.
2. **The skills are actually loaded**: confirm the copied skills appear in the
   session's skill list. A skill in the wrong directory is invisible rather than
   broken.
3. **No unhydrated stub came along silently**: every remaining G6 skill either
   has your commands in it and no banner, or is gone.
4. **The watermark names your source**: `upstream.json` points at the repo you
   adopted from, with a `lastSyncedSha` that resolves there.
5. **If you adopted G4**: confirm one GraphQL-flavored call now succeeds — e.g.
   `gh pr list -R <owner>/<repo>`. That is the assertion the shim exists to make
   true, and it either works or the hook isn't installed.
6. **If you declined G4**: state that in your report, with what it cost (above).

## Known gaps

**The `gh`-heavy skills are not proxy-safe.** They call GraphQL-flavored `gh`, so
in a web session they need G4's shim. Rewriting those call sites into REST form
would make G4 genuinely optional and remove the one step where you may
reasonably refuse — but it touches roughly ten skills and changes behavior at the
source as much as downstream, so it is judged on its own merits rather than as a
rider on this entry point. If you hit the G4 refusal and want the tracking
thread, look for the open issue titled around *"make the gh-heavy skills
proxy-safe"* in this repo's issues.

## The line a human pastes

To start this in another repo's agent session:

```
Adopt the agent infrastructure from https://github.com/vzakharov/agent-project-boilerplate
into this repo: clone it somewhere temporary, read ADOPTING.md, and follow it.
```

Prose rather than a shell one-liner on purpose: it names the repo and the file
and lets the agent pick its own fetch mechanism, which survives an environment
where any particular one is blocked.
