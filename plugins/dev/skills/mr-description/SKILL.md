---
name: mr-description
description: Generates or updates the title and description of a GitLab merge request (MR) or GitHub pull request (PR), in French, with a fixed title pattern and a structured description (Description, Contexte, Changements, Tests). The platform is detected from the URL or the git remote. Use whenever the user wants to write, rewrite, improve or fill in an MR/PR title or description, or gives a GitLab merge request or GitHub pull request link, even if they don't mention the format.
argument-hint: "[MR/PR URL | number]"
allowed-tools: Bash(git status:*), Bash(git branch:*), Bash(git log:*), Bash(git diff:*), Bash(git remote:*), Bash(git rev-parse:*), Bash(gh pr view:*), Bash(gh pr list:*), Bash(gh pr diff:*), Bash(glab mr view:*), Bash(glab mr list:*), Bash(glab mr diff:*)
---

# MR / PR title and description

Everything written into the MR/PR (title, description) and every question asked
to the user is in **French**. Say « MR » for GitLab and « PR » for GitHub.

## Arguments (optional)

Received content: `$ARGUMENTS`

| Argument | Target |
|---|---|
| `https://github.com/<owner>/<repo>/pull/<n>` | GitHub PR |
| `https://<host>/<group>/<repo>/-/merge_requests/<iid>` | GitLab MR |
| `#<n>` / `<n>` alone | MR or PR of the current repo: infer the platform from `git remote -v` |
| nothing | MR or PR of the current branch: infer the platform from `git remote -v` |

If the platform cannot be inferred (self-hosted host, several remotes), ask.

## Hard rules

- **Never modify the MR/PR without explicit confirmation** of the title and of
  the description, then a separate explicit authorization to send.
- Never invent facts (card number, context, tests). Ask or leave out.
- No mention of Claude in the MR/PR content.

## Steps

### 1. Identify and fetch the MR/PR

Resolve the target from the arguments (table above), then read the matching
reference **before running any command**:

- `references/sources/gitlab.md`
- `references/sources/github.md`

If the CLI (`glab` / `gh`) is missing or unauthenticated, tell the user
(suggest `! glab auth login` / `! gh auth login`) rather than guessing.

Retrieve: current title, current description, source/target branches, and the
changes (diff and commit list), following the reference. Read the diff to
understand the real content of the MR/PR.

Determine:
- **Repo name**: last segment of the project path, in UPPERCASE.
- **Card number**: look in the existing title, branch name, commits and
  description (e.g. `ABC-123`, `#123`). If none is found, ask once; if the
  user says there is none, omit the brackets entirely.

### 2. Title

Pattern (same on both platforms):

```
[<card number>] <REPO NAME> - <sujet> - courte description
```

- Brackets and card number only if a card exists.
- `<REPO NAME>`: repo name in uppercase.
- `<sujet>`: **always ask the user** for it (propose a suggestion inferred
  from the diff as a default option, but don't decide alone). If the current
  title already contains a subject, propose to keep it.
- Short description: succinct, in French, lowercase start, no trailing period.
- If an existing title is already well-formed and still fits the MR/PR content,
  keep it and say so. If it no longer fits, propose a modified one and show
  the before/after.

### 3. Description

Structure (Markdown, in French):

```markdown
# Description

<One or two sentences summarizing the goal of the MR/PR.>

## Contexte

<Current state of the code if it's a modification; expected result: constraints,
goals, architecture, strategy.>

## Changements

- <High-level change>
- ...

## Tests

- <Tests written, or manual tests done>
```

Section guidance:

- **Description**: 1–2 sentences on the goal. Propose a draft and ask the
  user to validate or correct it.
- **Contexte**: describes the state before (for a modification) and the
  expected outcome (constraints, objectives, architecture, strategy). Go
  **point by point**: submit each point to the user for validation and ask a
  question whenever a point could be clarified (why this choice, which
  constraint, which alternative rejected). Don't move on with unvalidated
  assumptions.
- **Changements**: high-level list only. Go into detail only when the change
  is precisely about that detail or when it is essential to understand the
  MR/PR as a whole.
- **Tests**: broad strokes of the automated tests written (files/areas
  covered) and the manual tests done. If unknown, ask; never claim tests that
  were not performed.

Prefer batching related questions with `AskUserQuestion` (subject, card
number, context points) instead of many round-trips.

### 4. Existing description (update case)

If the MR/PR already has a description:
- Show what would change, section by section (added / modified / removed),
  not just the new text.
- Preserve useful content the user wrote (links, screenshots, checklists,
  template sections, closing keywords such as `Closes #12`); mention it if
  something would be dropped.
- Ask for confirmation of the changes before going further.

### 5. Confirm, then send

1. Present the final **title**, the **target MR/PR** (URL, branches) and the
   full **description**, and ask for confirmation of all three.
2. Only after that, ask a separate question: authorization to send the
   modifications to the platform.
3. On approval, write the description to a scratchpad/temp file and update the
   MR/PR with the command from the platform reference. These commands are not
   in `allowed-tools` on purpose so the user gets a permission prompt.
4. Report the outcome and the MR/PR URL. If it fails, show the error; don't
   retry silently.
