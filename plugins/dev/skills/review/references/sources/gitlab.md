# Source: GitLab merge request

Requires `glab` (authenticated). URL shape:
`https://<host>/<group>/<repo>/-/merge_requests/<iid>`. Extract host, project
path and `iid`. For a self-hosted instance, use `GITLAB_HOST=<host>`.

## Fetch

| Need | Command |
|---|---|
| Metadata | `glab mr view <iid> -R <project path>` (add `--output json` for fields) |
| Diff | `glab mr diff <iid> -R <project path>` |
| Existing discussions | `glab mr view <iid> -R <project path> --comments` |
| Current branch's MR | `glab mr view` (no argument) |
| Find MR of a branch | `glab mr list --source-branch <branch>` |

If `glab mr view` does not expose what you need (pipeline status, discussion
resolution), `glab api projects/<url-encoded path>/merge_requests/<iid>/...`
can be used, but it is not in `allowed-tools`, so expect a permission prompt.

## GitLab specifics

- MR titles in this setup may follow a `[card] REPO - sujet - description`
  pattern: the card number points to the ticket, use it to understand the
  intent.
- Discussions are **resolvable threads**: do not repeat points from threads
  that are already resolved; mention unresolved ones that the change doesn't
  address.
- Draft / WIP MRs: review anyway, mention it, be lenient on unfinished work.
- Pipeline failing: report under "Non vérifié" or as a blocker if it clearly
  points to a defect; don't guess the cause without the job logs.
- Squash-on-merge projects: commit messages matter less than the MR
  title/description for the intent.

## Posting (only after explicit confirmation, step 8)

- Summary note: `glab mr note <iid> -R <project path> -m "<text>"`, or better
  with the text read from a scratchpad/temp file.
- Inline discussions on specific lines require the API (`position` with
  `base_sha`, `start_sha`, `head_sha`, `new_path`, `new_line`). Prefer one
  summary note listing `path:line` unless the user explicitly wants inline
  discussions.
- **Never approve (`glab mr approve`) on the user's behalf** unless they ask
  for that exact action.
