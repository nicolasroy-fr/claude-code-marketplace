---
name: clean-code
description: Language-agnostic clean code conventions to follow when writing or modifying code, and to check when reviewing it (top-down function order, explicit names, no magic values, guard clauses...). Use whenever writing, editing or refactoring code in any language, even if the user doesn't mention conventions.
---

# Clean code

Readability conventions that apply to every language. When writing code,
follow them. When reviewing code, report violations as **Suggestion**, or
**Important** when the pattern is widespread in the change.

Order of precedence, highest first: the project's own conventions (`CLAUDE.md`,
`CONTRIBUTING.md`, linter / formatter config), then the language-specific
plugins and references (python, react, terraform), then this skill.

## Top-down code

The order of the functions follows the logical execution flow: the entry point
comes first, then the functions it calls, in the order they are called. A reader
should be able to read the file from top to bottom like the program runs.

- Flag helpers defined before the code that uses them when it makes the flow
  harder to follow.
- Flag a file whose function order bears no relation to the call order.

## No abbreviated names

Always spell out variable names (and parameters, attributes, fields). Short
names are accepted only when they are the norm in the context, for example `x`,
`y`, `z` for positions or coordinates.

```python
# Avoid
usr_cfg = load(p)
for i, tmp in enumerate(res): ...

# Prefer
user_configuration = load(file_path)
for result_index, result in enumerate(results): ...
```

## Explicit names for free functions

A free function (not a method, so it has no class or object to give it context)
must have a name that says what it does on its own. A bare verb without context
is not enough: include what goes in and what comes out, or what it applies to.

```text
# Avoid
convert(value)
process(data)
parse(text)

# Prefer
convertFromCelsiusToFahrenheit(value)
processPendingInvoices(invoices)
parseIsoDate(text)
```

Use the casing of the language (`convert_from_celsius_to_fahrenheit` in Python,
`convertFromCelsiusToFahrenheit` in TypeScript).

## No magic values

Numbers and strings that carry meaning go in named constants, not inline.

```python
# Avoid
if retry_count > 3: ...

# Prefer
MAX_RETRY_COUNT = 3
if retry_count > MAX_RETRY_COUNT: ...
```

Obvious values (`0`, `1`, `""`, an index in a trivial loop) are fine.

## Units in names

When a value has a unit, put it in the name: `timeoutSeconds`, `sizeInBytes`,
`priceInCents`. Skip it when the type already carries the unit (for example a
`timedelta` or a `Duration`).

## Guard clauses, little nesting

Handle invalid or special cases first with an early return (or `continue`,
`raise`), so the main path stays at the lowest indentation. Flag nesting deeper
than 2 or 3 levels when guard clauses or an extracted function would flatten it.

```python
# Avoid
if user:
    if user.is_active:
        do_something(user)

# Prefer
if not user or not user.is_active:
    return
do_something(user)
```

## No boolean flag parameters

A boolean parameter that switches behavior is unreadable at the call site
(`render(true)`). Prefer two explicit functions, or an enum / named option.

```text
# Avoid
render(true)

# Prefer
renderWithHeader()   or   render(mode=Mode.WITH_HEADER)
```

## Boolean names

Name booleans positively, with a prefix that reads as a question: `isEnabled`,
`hasPermission`, `shouldRetry`, `canEdit`. Avoid negative names (`isNotEnabled`,
`disableCache = false`) and bare names (`flag`, `status`).

## One word per concept

Use the same word for the same idea across the code: don't mix `fetch`, `get`
and `load` (or `remove`, `delete` and `destroy`) for the same kind of operation.
Follow the vocabulary already used in the codebase.
