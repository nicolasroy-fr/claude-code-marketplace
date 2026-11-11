---
name: commit
description: Writes and creates a git commit with a custom emoji (gitmoji style) and a structured message (short sentence + small paragraph), always in English. Use whenever the user asks to commit, to write a commit message, or says "commit this", even if they don't mention the format explicitly.
argument-hint: "[emoji nature] [items to include in the message]"
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git add:*), Bash(git commit:*)
---

# Commit with emoji and fixed format

## Arguments (optional)

Received content: `$ARGUMENTS`

- If the first word matches a nature from the table below (or is directly an
  emoji), it dictates the emoji.
- The rest of the text is a list of items to include in the message
  (preferably in the details paragraph).
- With no argument, infer the nature from the diff.

Examples: `/commit fix migration forgotten in the deployment` or `/commit` alone.

## Steps

1. Read `git status` and `git diff --staged`. If nothing is staged, look at
   `git diff` and suggest what to add before running `git add`.
2. Look at `git log -5 --oneline` for context on the repository's style.
3. Pick the emoji: the one dictated by the arguments, otherwise the dominant
   nature of the diff. One emoji per commit.
4. Write the message following the format below, then run `git commit`.

## Language

**Commit messages are always written in English**, regardless of the language
of the arguments, the conversation, or the existing git history. If the
arguments are in another language, translate them.

## Message format

```
<emoji> <Concise sentence describing what is done>

<Short paragraph with useful details.>
```

- **First line**: emoji, space, one sentence in the imperative mood, 72
  characters maximum, no trailing period.
- **Blank line** required, then **a single paragraph** of 1 to 3 sentences:
  the why, notable choices, side effects. No bullet lists.
- Work in the items provided as arguments without copying them word for word.
- Don't describe the diff line by line: it's already in git.
- No mention of Claude or "Co-authored-by".

## Emoji table

Based on [gitmoji.dev](https://gitmoji.dev). The first block holds the most
common natures; the rest covers the full gitmoji list.

### Core

| Nature | Emoji | When |
|---|---|---|
| feat | ✨ | New feature |
| fix | 🐛 | Bug fix |
| refactor | ♻️ | Restructuring without behavior change |
| perf | ⚡ | Performance improvement |
| test | 🧪 | Adding or changing tests |
| docs | 📝 | Documentation |
| style | 💄 | UI and style files |
| chore | 🔧 | Config, dependencies, tooling |
| infra | 🏗️ | AWS, CI/CD, deployment |
| remove | 🔥 | Removing code or files |
| wip | 🚧 | Work in progress |

### Code quality

| Nature | Emoji | When |
|---|---|---|
| format | 🎨 | Improve structure / format of the code |
| lint | 🚨 | Fix compiler / linter warnings |
| types | 🏷️ | Add or update types |
| typo | ✏️ | Fix typos |
| comments | 💡 | Add or update comments in source code |
| validation | 🦺 | Add or update code related to validation |
| errors | 🥅 | Catch errors |
| business-logic | 👔 | Add or update business logic |
| dead-code | ⚰️ | Remove dead code |
| deprecate | 🗑️ | Deprecate code that needs to be cleaned up |
| compat | 🦖 | Code that adds backwards compatibility |
| concurrency | 🧵 | Add or update code related to multithreading or concurrency |
| bad-code | 💩 | Write bad code that needs to be improved |

### Fixes and security

| Nature | Emoji | When |
|---|---|---|
| hotfix | 🚑 | Critical hotfix |
| small-fix | 🩹 | Simple fix for a non-critical issue |
| security | 🔒 | Fix security or privacy issues |
| secrets | 🔐 | Add or update secrets |
| auth | 🛂 | Authorization, roles and permissions |
| ci-fix | 💚 | Fix CI build |
| revert | ⏪ | Revert changes |
| breaking | 💥 | Introduce breaking changes |

### Dependencies, build and release

| Nature | Emoji | When |
|---|---|---|
| dep-add | ➕ | Add a dependency |
| dep-remove | ➖ | Remove a dependency |
| dep-upgrade | ⬆️ | Upgrade dependencies |
| dep-downgrade | ⬇️ | Downgrade dependencies |
| dep-pin | 📌 | Pin dependencies to specific versions |
| ci | 👷 | Add or update CI build system |
| deploy | 🚀 | Deploy stuff |
| release | 🔖 | Release / version tags |
| package | 📦 | Add or update compiled files or packages |
| scripts | 🔨 | Add or update development scripts |
| external-api | 👽 | Update code due to external API changes |
| init | 🎉 | Begin a project |
| merge | 🔀 | Merge branches |
| move | 🚚 | Move or rename resources (files, paths, routes) |
| license | 📄 | Add or update license |
| gitignore | 🙈 | Add or update a .gitignore file |
| contributors | 👥 | Add or update contributor(s) |
| sponsors | 💸 | Add sponsorships or money related infrastructure |
| dx | 🧑‍💻 | Improve developer experience |

### UI, UX and content

| Nature | Emoji | When |
|---|---|---|
| ux | 🚸 | Improve user experience / usability |
| a11y | ♿ | Improve accessibility |
| responsive | 📱 | Work on responsive design |
| animation | 💫 | Add or update animations and transitions |
| assets | 🍱 | Add or update assets |
| text | 💬 | Add or update text and literals |
| i18n | 🌐 | Internationalization and localization |
| seo | 🔍 | Improve SEO |
| offline | ✈️ | Improve offline support |

### Data, ops and experiments

| Nature | Emoji | When |
|---|---|---|
| db | 🗃️ | Perform database related changes |
| seed | 🌱 | Add or update seed files |
| logs-add | 🔊 | Add or update logs |
| logs-remove | 🔇 | Remove logs |
| analytics | 📈 | Add or update analytics or track code |
| healthcheck | 🩺 | Add or update healthcheck |
| feature-flag | 🚩 | Add, update, or remove feature flags |
| test-pass | ✅ | Make tests pass (🧪 stays the default for adding or changing tests) |
| snapshot | 📸 | Add or update snapshots |
| mock | 🤡 | Mock things |
| experiment | ⚗️ | Perform experiments |
| explore | 🧐 | Data exploration / inspection |
| easter-egg | 🥚 | Add or update an easter egg |

If no nature matches, pick the closest one and don't create a new emoji.
