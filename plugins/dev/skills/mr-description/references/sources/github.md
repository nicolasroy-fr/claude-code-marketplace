# Platform: GitHub pull request

Requires `gh` (authenticated). URL shape:
`https://github.com/<owner>/<repo>/pull/<n>`. Pass the URL directly or use
`-R <owner>/<repo>`; with a bare number or nothing, run inside the repo.

## Fetch

- Metadata: `gh pr view <n|url> --json title,body,baseRefName,headRefName,isDraft,labels,commits,url`.
- Without URL: `gh pr view` (PR of the current branch) or
  `gh pr list --head <branch>`. If several or none match, ask the user.
- Changes: `gh pr diff <n|url>`.
- Commit list: the `commits` field of the JSON above.

Repo name: the `<repo>` segment of `<owner>/<repo>`.

## GitHub specifics

- Closing keywords in the body (`Closes #12`, `Fixes #12`) link the issue: keep
  them when rewriting the description, and use them to find the card number.
- A `.github/pull_request_template.md` may exist: if the user's description
  has template sections (checklists…), preserve them (step 4).
- Draft PRs: handle normally, don't change the draft state.

## Update (only after step 5 confirmations)

```
gh pr edit <n|url> --title "<title>" --body-file <file>
```

Write the description to a scratchpad/temp file first, never inline it in the
command.
