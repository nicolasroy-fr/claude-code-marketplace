# Source: local changes

No remote involved: everything comes from `git`.

## Choosing what to review

| Situation | Command |
|---|---|
| `--staged` | `git diff --cached` |
| a branch name `<b>` | `git diff $(git merge-base <default> <b>)...<b>` |
| no argument, uncommitted changes exist | `git diff HEAD` (staged + unstaged) |
| no argument, working tree clean, branch ≠ default | `git diff $(git merge-base <default> HEAD)...HEAD` |
| no argument, nothing to review | tell the user and ask what to review |

Find the default branch with `git symbolic-ref --short refs/remotes/origin/HEAD`
(fallback: `main`, then `master`).

If both uncommitted changes **and** commits ahead of the default branch exist,
ask which one to review (or both) instead of choosing.

## Context

- `git status --short` to see untracked files: `git diff` does not show them.
  Read new untracked files directly and include them in the review.
- `git log --oneline <default>..HEAD` for the commit messages (intent).
- There is no title / description / ticket: infer the intent from the commits
  and the branch name (often contains a ticket id), and say it is inferred.
- No CI status and no review threads.

## Output

Findings are displayed in the terminal and saved to `reviews/` (step 7). Nothing to post.
