---
name: review
description: Reviews code changes and reports prioritized findings in French. Works on local changes (working tree, staged, branch vs main), a GitHub pull request or a GitLab merge request (URL or number), and adapts the checks to the languages found in the diff. Use whenever the user asks to review, relire, "check" or give feedback on code, a diff, a branch, a PR or an MR, even if they don't say "review".
argument-hint: "[PR/MR URL | number | branch | --staged]"
allowed-tools: Bash(git status:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*), Bash(git show:*), Bash(git merge-base:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(gh pr view:*), Bash(gh pr diff:*), Bash(gh pr checks:*), Bash(gh pr list:*), Bash(glab mr view:*), Bash(glab mr diff:*), Bash(glab mr list:*), Edit(reviews/**)
---

# Code review

The review itself (findings, questions asked to the user) is written in
**French**. Code, identifiers and suggested patches stay in their original
language.

## Arguments (optional)

Received content: `$ARGUMENTS`

| Argument | Source |
|---|---|
| `https://github.com/<owner>/<repo>/pull/<n>` | GitHub PR |
| `https://<host>/<group>/<repo>/-/merge_requests/<iid>` | GitLab MR |
| `#<n>` / `<n>` alone | PR or MR of the current repo: infer the platform from `git remote -v` |
| `--staged` | Local, staged changes only |
| a branch name | Local, that branch compared to the default branch |
| nothing | Local: see `references/sources/local.md` for the default behaviour |

If the platform cannot be inferred (self-hosted host, ambiguous remote), ask.

## Hard rules

- **Read-only, with one exception.** The only thing written without asking is
  the review report file in `reviews/` (step 7). Never modify code, the PR/MR,
  or post comments without explicit confirmation (step 8).
- Never run project code (tests, builds, scripts) unless the user asks.
- Only report what you actually see in the diff or in the code you read. No
  speculation presented as fact; mark uncertainty explicitly.
- Never invent a file, a line number or a function. Every finding cites
  `path:line` in the **new** version of the file.
- Don't comment on what a formatter or linter already enforces (whitespace,
  import order, quote style…), unless the project clearly doesn't run one.
- No mention of Claude in anything that would be posted to a PR/MR.

## Steps

### 1. Identify the source

Resolve the target from the arguments (table above), then read the matching
reference **before running any command**:

- `references/sources/local.md`
- `references/sources/github.md`
- `references/sources/gitlab.md`

If the CLI (`gh` / `glab`) is missing or unauthenticated, tell the user
(suggest `! gh auth login` / `! glab auth login`) rather than guessing.

### 2. Fetch the change

Following the source reference, retrieve:
- the **diff**,
- the **metadata**: title, description, source/target branches, linked ticket,
  commit list, CI status when available,
- for a PR/MR: existing review threads, so you don't repeat what has already
  been said or resolved.

Large changes: if the diff is bigger than roughly 1500 changed lines, say so,
ignore generated files, lockfiles and vendored code, and review by groups of
files (by feature or directory) rather than all at once. Tell the user what was
skipped.

### 3. Understand the intent

Before judging, state to yourself what the change is *supposed* to do, from the
title, description, ticket and commits. A finding is only meaningful relative
to the intent. If the intent is unclear and it matters for the verdict, ask the
user one short question, or list it under "Non vérifié".

### 4. Load the checks

1. Always read `references/checklist.md`.
2. Detect the languages from the changed file extensions and read the matching
   file in `references/languages/`:

   | Extensions | Reference |
   |---|---|
   | `.py` | `python.md` |
   | `.ts`, `.tsx`, `.js`, `.jsx` | `react.md` |
   | `.tf`, `.tfvars` | `terraform.md` |

   If a language has no reference file, review it with the general checklist
   and your knowledge of its idioms, and say so in the output.
3. Look at the project's own conventions if present (`CLAUDE.md`,
   `CONTRIBUTING.md`, linter / formatter config) and treat them as higher
   priority than the references.

Several languages in the same change: load each relevant file.

### 5. Analyze

- Read the diff **and the surrounding code**. Open the full file, the callers
  of a changed function, the tests that cover it. A hunk alone is rarely
  enough to judge a change.
- Check in this order: correctness → security → data / API contracts → error
  handling → tests → performance → readability / maintainability.
- Check that the change matches its stated intent, and that nothing unrelated
  slipped in.
- Check that tests exist for new or changed behaviour, and that they would
  actually fail if the code were wrong.
- Prefer few, well-argued findings over an exhaustive list. If you have a
  doubt you cannot resolve by reading the code, put it as a question.

### 6. Report

Print the review in the terminal, in French, with this structure. Omit empty
sections.

```markdown
## Review — <target: PR/MR title and URL, or branch / "changements locaux">

**Résumé** : <2–3 sentences: what the change does and overall impression>
**Verdict** : ✅ Prêt à merger | 💬 Merge possible avec réserves | ❌ Changements requis

### 🔴 Bloquant
- `path/file.py:42` — <problem>. <Why it matters.> **Suggestion** : <fix>

### 🟠 Important
- `path:line` — ...

### 🟡 Suggestions
- `path:line` — ...

### ❓ Questions
- <What you could not determine from the code alone>

### 👍 Points positifs
- <Brief, only if genuine>

### Non vérifié
- <What was not checked: tests not run, files skipped, missing reference for a language…>
```

Severity:
- **Bloquant**: bug, security issue, data loss, broken contract, missing test
  on risky logic. Should not merge as is.
- **Important**: likely future bug, fragile design, error-handling gap,
  convention violation worth fixing in this change.
- **Suggestion**: readability, minor simplification, optional improvement.

For each finding: where, what, why it matters, and a concrete fix (a short code
snippet when it helps). One finding per issue; group identical occurrences
("same pattern in `a.py:10`, `b.py:55`").

### 7. Save the report

After printing the review, save the exact same Markdown to a file:

- **Folder**: `reviews/` at the **root of the repository being reviewed**
  (`git rev-parse --show-toplevel`), created if missing. If the current
  directory is not in a git repository, use `reviews/` in the current directory.
- **File name**: `<YYYY-MM-DD>-<slug>.md` where the date is today's and `<slug>`
  is:
  - PR: `pr-<n>-<short-title>`; MR: `mr-<iid>-<short-title>`
  - branch: `branch-<name>` (replace `/` with `-`)
  - staged / working tree: `local-<current-branch>`
  - lowercase, ASCII, words separated by `-`, 60 characters max.
- If the file already exists, don't overwrite it: append `-2`, `-3`…
- Add a small header before the review content:

  ```markdown
  <!-- source: <URL or "local">, head: <short commit sha>, generated: <ISO date> -->
  ```
- Don't `git add` or commit it, and don't edit `.gitignore`. Just tell the user
  the path, and mention in one line that `reviews/` may be worth ignoring in
  git if it isn't already (check with `git check-ignore reviews` first and stay
  silent if it is).

### 8. Follow-up (only if the user asks)

The review ends at step 7 by default. If the user then asks to post it
(« poste la review », « commente la MR ») on a PR/MR:

1. Show the exact comments that would be posted (inline vs. summary).
2. Ask for explicit confirmation.
3. Post following the platform reference. The posting commands are not in
   `allowed-tools` on purpose, so the user also gets a permission prompt.
4. Report the outcome. If it fails, show the error; don't retry silently.

If the user asks to *fix* the findings, that is a separate task: confirm which
findings to apply before editing.
