# Source: GitHub pull request

Requires `gh` (authenticated). With a URL, pass it directly or use
`-R <owner>/<repo>`; with a bare number, run inside the repo.

## Fetch

| Need | Command |
|---|---|
| Metadata | `gh pr view <n|url> --json title,body,author,baseRefName,headRefName,isDraft,labels,commits,reviewDecision,statusCheckRollup,url` |
| Diff | `gh pr diff <n|url>` |
| Files list (large PRs) | `gh pr view <n|url> --json files` |
| CI status | `gh pr checks <n|url>` |
| Existing comments / reviews | `gh pr view <n|url> --comments` |
| Current branch's PR | `gh pr view` (no argument) |
| Find PR of a branch | `gh pr list --head <branch>` |

## GitHub specifics

- Closing keywords in the body (`Closes #12`) reveal the linked issue: use it
  to understand the intent.
- Draft PRs: review anyway, but mention it; be more lenient on unfinished work.
- `statusCheckRollup` failing: report it under "Non vérifié" or as a blocker
  if it points to a real defect; don't guess the cause without the logs.
- Review comments already resolved or outdated must not be repeated.
- A PR can touch generated files (lockfiles, snapshots): skip them, say so.

## Posting (only after explicit confirmation, step 8)

- Summary comment: `gh pr comment <n> --body-file <file>`.
- A formal review: `gh pr review <n> --comment|--request-changes|--approve --body-file <file>`.
  **Never approve or request changes on the user's behalf unless they ask for
  that exact action**; default to a plain comment.
- Inline comments on specific lines require the API (`gh api`, with `commit_id`,
  `path`, `line`, `side`). Prefer one summary comment listing `path:line` unless
  the user explicitly wants inline comments.
- Write the body to a scratchpad/temp file first, never inline long text in the
  shell command.
