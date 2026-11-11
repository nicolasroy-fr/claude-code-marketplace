# Python review points

Complements `checklist.md`; project config (`pyproject.toml`, ruff, mypy)
takes precedence. Add your own conventions below.

## Common pitfalls

- Mutable default arguments (`def f(x=[])`).
- Bare `except:` / `except Exception: pass`; missing `raise ... from err`.
- `is` for value comparison; `== None`; truthiness checks that conflate `0`,
  `""`, `[]` and `None`.
- Late-binding closures in loops; modifying a collection while iterating it.
- Resources opened without `with`.
- Blocking calls inside `async def`; coroutines never awaited.
- `datetime.now()` / `utcnow()` naive datetimes where timezone matters.
- `subprocess` with `shell=True` on non-constant input; `pickle` / `yaml.load`
  on untrusted data; f-string SQL.

## Typing and API

- Public functions annotated; `Any` and `# type: ignore` justified.
- Return types consistent (no `str | None` that callers never handle).

## Tests

- <!-- your pytest conventions: location, naming, structure, assertions -->

## Docstrings

- <!-- your docstring convention (e.g. Google style) -->

## Project conventions

- <!-- add yours -->
