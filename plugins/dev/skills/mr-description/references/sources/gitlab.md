# Platform: GitLab merge request

Requires `glab` (authenticated). URL shape:
`https://<host>/<group>/<repo>/-/merge_requests/<iid>`. Extract host, project
path and `iid`. For a self-hosted instance, use `GITLAB_HOST=<host>` or
`glab api --hostname`.

## Fetch

- With a URL: `glab mr view <iid> -R <project path>` (add `--output json` for
  fields).
- Without URL: `git branch --show-current`, then
  `glab mr list --source-branch <branch>` / `glab mr view <branch>`.
  If several or none match, ask the user.
- Changes: `glab mr diff <iid> -R <project path>`.
- Commit list: `glab mr view <iid> -R <project path> --output json` (commits are
  not always included), or
  `glab api projects/<url-encoded path>/merge_requests/<iid>/commits` (not in
  `allowed-tools`: expect a permission prompt).

Repo name: last segment of the project path.

## Update (only after step 5 confirmations)

```
glab mr update <iid> -R <project path> --title "<title>" --description "$(cat <file>)"
```

or `glab api -X PUT projects/:id/merge_requests/<iid>` with `title` and
`description` fields.
