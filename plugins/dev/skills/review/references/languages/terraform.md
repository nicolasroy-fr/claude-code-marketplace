# Terraform review points

Complements `checklist.md`; project config and existing module layout take
precedence. Add your own conventions below.

## Safety (highest priority)

- **Destructive changes**: resources that would be replaced or destroyed
  (renamed resource addresses without `moved`, changed immutable arguments),
  stateful resources (databases, buckets, volumes, KMS keys) without
  `prevent_destroy` / backups / deletion protection.
- IAM: wildcard actions or resources (`"*"`), overly broad trust policies,
  inline policies that should be scoped.
- Network exposure: `0.0.0.0/0` ingress, public buckets / databases / endpoints.
- Encryption at rest and in transit disabled or unspecified; public access
  blocks missing on S3.
- Secrets in `.tf`, `.tfvars` or state outputs; sensitive variables / outputs
  not marked `sensitive = true`.

## Structure and quality

- Provider and Terraform versions pinned; lock file updated when providers change.
- Variables: typed, described, validated where it helps; no unused variables or
  outputs.
- No hard-coded account ids, regions or ARNs that should be data sources or
  variables.
- `count` vs `for_each`: `count` over a list that can reorder causes churn.
- Tags / default tags consistent with the project.
- Backend and state configuration unchanged unless that is the intent.

## Tests / validation

- Mention if `terraform fmt` / `validate` / `plan` output was not available to
  you (put under "Non vérifié").

## Project conventions

- <!-- file layout, naming, module usage… -->
