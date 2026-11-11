# Claude Code Skills

Personal collection of [Claude Code](https://claude.com/claude-code) skills.

## Plugins & skills

Skills are grouped by theme, one plugin per theme under `plugins/<theme>/`.

| Plugin | Skill | Description |
|---|---|---|
| `git` | `commit` | Creates a git commit with an emoji and a structured message, always in English. |
| `python` | `python-test-generator` | Generates pytest unit tests following strict conventions (`tests/` folder, `test__<function>__<case>` naming, with/when/then structure, attribute-by-attribute asserts). |
| `python` | `python-docstring` (agent, Haiku) | Writes docstrings for functions, methods and classes in Google style (ruff pydocstyle, `convention = "google"`). |
| `python` | `ruff-format` (hook) | After each `Write`/`Edit`, runs `ruff format` on the edited `.py`/`.pyi` file (uses the project's ruff config). Skipped if `ruff` or `jq` is not installed. |
| `react` | `react-component` | Generates a single React component file (TypeScript, Tailwind) from templates. |
| `react` | `react-hook` | Generates a custom React hook folder (TypeScript, Vitest + Testing Library `renderHook`) from templates. |
| `dev` | `review` | Reviews local changes, a GitHub PR or a GitLab MR and reports prioritized findings in French; loads per-language checks from `references/languages/`. Saves each review to `reviews/` at the repo root. Never posts to a PR/MR without confirmation. |
| `dev` | `mr-description` | Generates or updates a GitLab MR / GitHub PR title and description in French (fixed title pattern, Description/Contexte/Changements/Tests); platform detected from the URL or the git remote. Confirmations before any change. |
| `dev` | `plan-council` | Builds a dev/feature plan with a council of 5 advisors (Architect, Minimalist, Skeptic, Tester, Maintainer) and a chairman, saved to `plans/` in French. Light mode by default (1 Haiku scout reads the code once, 5 Sonnet advisors, 1 Opus chairman); `--full` adds an anonymous peer-review round. |
| `dev` | `plan-scout`, `plan-advisor`, `plan-reviewer`, `plan-chairman` (agents) | Internal agents of `plan-council` (Haiku scout, Sonnet advisors and peer reviewers, Opus chairman). Not meant to be called directly. |
| `dev` | `github` (MCP server) | Official [GitHub MCP server](https://github.com/github/github-mcp-server) (remote, `https://api.githubcopilot.com/mcp/`). Needs `GITHUB_PERSONAL_ACCESS_TOKEN`. |
| `dev` | `gitlab` (MCP server) | Official [GitLab MCP server](https://docs.gitlab.com/user/gitlab_duo/model_context_protocol/mcp_server/) (remote, `/api/v4/mcp`). OAuth via `/mcp`; self-managed: set `GITLAB_MCP_URL`. |
| `terraform` | `terraform-aws` | Creates an AWS Terraform deployment (flat root, one file per resource family, S3 native-lock backend, default tags, fmt + validate). |
| `terraform` | `terraform-fmt` (hook) | After each `Write`/`Edit`, runs `terraform fmt` on the edited `.tf`/`.tfvars` file. Skipped if `terraform` or `jq` is not installed. |

## Install

Add the marketplace (user scope, available in all your projects):

```
/plugin marketplace add nicolasroy-fr/claude-code-marketplace
```

Or with the full URL:

```
/plugin marketplace add https://github.com/nicolasroy-fr/claude-code-marketplace
```

Then install the plugins you need:

```
/plugin install git@nicolas-skills
/plugin install dev@nicolas-skills
/plugin install python@nicolas-skills
/plugin install react@nicolas-skills
/plugin install terraform@nicolas-skills
```

From the shell, the same thing with the CLI:

```
claude plugin marketplace add nicolasroy-fr/claude-code-marketplace
claude plugin install git@nicolas-skills --scope user
```

Update later with `/plugin marketplace update nicolas-skills`.

Or copy a single skill manually:

```
cp -r plugins/git/skills/commit ~/.claude/skills/
```

## MCP servers setup

Both servers ship with the `dev` plugin.

**GitHub**: create a [personal access token](https://github.com/settings/personal-access-tokens/new)
(`repo` scope) and export it in the shell that launches Claude Code:

```
export GITHUB_PERSONAL_ACCESS_TOKEN=<token>
```

**GitLab**: authentication is OAuth, run `/mcp`, select
`plugin:dev:gitlab` and approve in the browser. On GitLab.com nothing else is
needed. For a self-managed instance, point the server at it before launching
Claude Code:

```
export GITLAB_MCP_URL=https://<gitlab.example.com>/api/v4/mcp
```

The instance (or the top-level group on GitLab.com) must allow access to the
MCP server in its settings.

## Usage

```
/git:commit [nature] [details to include]
/dev:mr-description [MR/PR URL | number]
/dev:review [PR/MR URL | number | branch | --staged]
/dev:plan-council <feature | ticket URL | file> [--full]
```

## Validation

Check the marketplace and every plugin before pushing:

```
claude plugin validate --strict .
for p in plugins/*/; do claude plugin validate --strict "$p"; done
```

The `Validate plugins` GitHub Actions workflow runs the same checks (plus
`shellcheck` on hook scripts) on every push to `main` and every pull request.

## Adding a skill

Create `plugins/<theme>/skills/<name>/SKILL.md` with `name` and `description` frontmatter.

For a new theme:
1. Create `plugins/<theme>/.claude-plugin/plugin.json` (`name`, `description`, `version`, `author`).
2. Add an entry to `.claude-plugin/marketplace.json` with `"source": "./plugins/<theme>"`.

When a plugin changes, bump its `version` in `plugin.json` so that
`/plugin marketplace update` picks up the change.
