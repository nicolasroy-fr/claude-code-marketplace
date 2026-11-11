#!/usr/bin/env bash
# PostToolUse hook: run `terraform fmt` on the Terraform file Claude just wrote or edited.
# Silently does nothing when jq or terraform is missing, or when the file is not Terraform.
set -u

command -v jq >/dev/null 2>&1 || exit 0
command -v terraform >/dev/null 2>&1 || exit 0

file_path=$(jq -r '.tool_input.file_path // empty')
case "$file_path" in
  *.tf | *.tfvars) ;;
  *) exit 0 ;;
esac
[ -f "$file_path" ] || exit 0

if ! output=$(terraform fmt "$file_path" 2>&1); then
  echo "terraform fmt failed on $file_path: $output" >&2
fi
exit 0
