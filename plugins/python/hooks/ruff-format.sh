#!/usr/bin/env bash
# PostToolUse hook: run `ruff format` on the Python file Claude just wrote or edited.
# Silently does nothing when jq or ruff is missing, or when the file is not Python.
set -u

command -v jq >/dev/null 2>&1 || exit 0
command -v ruff >/dev/null 2>&1 || exit 0

file_path=$(jq -r '.tool_input.file_path // empty')
case "$file_path" in
  *.py | *.pyi) ;;
  *) exit 0 ;;
esac
[ -f "$file_path" ] || exit 0

# Uses the project's ruff config (pyproject.toml / ruff.toml) when there is one.
if ! output=$(ruff format --quiet "$file_path" 2>&1); then
  echo "ruff format failed on $file_path: $output" >&2
fi
exit 0
