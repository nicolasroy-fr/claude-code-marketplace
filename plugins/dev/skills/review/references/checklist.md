# General review checklist

Language-agnostic. Apply in this order; stop digging a category once nothing
looks off. Project conventions (`CLAUDE.md`, `CONTRIBUTING.md`, linter config)
override anything here.

## 1. Correctness

- Does the code do what the title / description / ticket says?
- Edge cases: empty input, `None` / `null` / `undefined`, zero, negative, very
  large, unicode, timezones, off-by-one, first / last element.
- Control flow: unreachable branches, missing `else`, early returns that skip
  cleanup, inverted conditions.
- Concurrency: shared mutable state, race conditions, missing awaits, unawaited
  promises / coroutines, non-atomic read-modify-write.
- Resources: files, connections, locks and subscriptions released on every path.
- State: stale closures / caches, mutations of arguments, hidden global state.

## 2. Security

- Untrusted input reaching: SQL / shell / template / path / URL / regex /
  deserialization sinks (injection, path traversal, SSRF, ReDoS).
- Authentication and authorization: new endpoints / actions without checks,
  checks done client-side only, IDOR (object ids not scoped to the caller).
- Secrets: credentials, tokens, keys in code, config, logs, test fixtures.
- Sensitive data in logs, error messages, responses or URLs.
- Weak crypto, home-made crypto, predictable randomness for security purposes.
- New dependencies: necessary, maintained, pinned, from the expected source.

## 3. Contracts and compatibility

- Public API / schema / event / CLI / config changes: backward compatible?
  Versioned? Callers updated?
- Database migrations: reversible, safe on large tables (locks, backfills),
  deployed in an order compatible with running code.
- Removed or renamed symbols still referenced elsewhere.

## 4. Error handling

- Errors swallowed (`except: pass`, empty `catch`), or caught too broadly.
- Failure paths leave the system in a consistent state (partial writes).
- Error messages actionable; no sensitive data leaked.
- Retries / timeouts on I/O, with bounds (no infinite loops, no unbounded
  retries).

## 5. Tests

- New or changed behaviour is covered, including failure paths and edge cases.
- Tests would fail if the code were wrong (no assertion-free tests, no tests
  that only mirror the implementation, no over-mocking of the thing under test).
- Deterministic: no dependence on time, order, network, random without a seed.
- Removed / skipped tests are justified.

## 6. Performance

Only flag what is plausibly a problem at the real scale of the code.

- N+1 queries, queries or I/O inside loops, missing pagination / limits.
- Accidental quadratic behaviour on large collections.
- Repeated expensive work that could be hoisted or cached.
- Unbounded memory growth (accumulating lists, caches without eviction).

## 7. Readability and maintainability

- Names say what things are; functions do one thing; no dead code or commented-out
  code; no duplicated logic that should be shared (and no premature abstraction).
- Comments explain *why*, not *what*; outdated comments fixed.
- Change is cohesive: unrelated edits belong in another PR / MR.
- Public functions / modules documented the way the project does it.

## 8. Operability

- Logging / metrics / alerts for new failure modes, without noise or sensitive data.
- Configuration via the project's mechanism, with safe defaults; feature flags
  where the project uses them.
- Docs / changelog / README updated when behaviour or usage changes.
