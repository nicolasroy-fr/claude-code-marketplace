---
name: sqlalchemy-query
description: Write SQLAlchemy 2.x database queries as explicit statements (select, insert, update, delete) run with session.execute, instead of ORM-style access (session.query, session.add, entity loading, lazy relationships). Use when the user asks to write, add or refactor a database query, a repository or a data-access function with SQLAlchemy (« écris une requête SQLAlchemy », « ajoute une fonction d'accès aux données », « crée le repository »), even if they don't mention session.execute.
---

# SQLAlchemy queries with session.execute

Write data-access code as explicit SQLAlchemy 2.x statements run with `session.execute`. Follow every rule below. Code, names and docstrings are in **English**.

## 1. Template

Start from `templates/queries.py` (read it first). It covers get by id, filtered and paginated list, count, insert, bulk insert, update and delete. Replace the placeholders, keep only the functions the request needs, and rename them after what they do (`rename___entity__` is an example of a targeted update):

| Placeholder | Meaning | Example |
|---|---|---|
| `__entity__` | Singular, snake_case | `user` |
| `__entities__` | Plural, snake_case; also the `Table` object | `users` |
| `__Entity__` | Read model class, PascalCase | `User` |
| `__ENTITY__` | Constant prefix, UPPER_CASE | `USER` |
| `__tables_module__` | Module that defines the `Table` (or the model) | `app.db.tables` |

Columns of the template (`id`, `name`, `is_active`) are examples: use the real ones.

## 2. Where it goes

- Put the functions in the project's existing data-access module (`repositories/`, `queries/`, `dal/`, `crud.py`…), one module per table or aggregate. Ask if it is ambiguous.
- Match the project's existing style (free functions vs. a repository class taking the session in `__init__`) when it already has one.

## 3. Statements, not ORM

- Build every query with `select`, `insert`, `update`, `delete` (and `func`, `and_`, `or_`, `case`…) from `sqlalchemy`, and run it with `session.execute(statement)`.
- Target the `Table` object and its columns (`users.c.email`). If the project only has ORM models, use `Model.__table__` or the mapped columns (`User.email`) in the statement, but still select **columns**, never the entity.
- **Forbidden**: `session.query(...)`, `session.add` / `add_all` / `delete` / `merge` / `get`, `select(Model)` returning entities, relationship access, `session.scalars(select(Model))`.
- Select **only the columns needed**, listed in a module-level tuple (`USER_COLUMNS`) when several functions share them.
- Joins are explicit: `select(...).select_from(users.join(orders, orders.c.user_id == users.c.id))`, with the `onclause` always given.
- Aggregations: `func.count()`, `func.sum(...)`, `group_by`, `having`; label computed columns (`.label("total_amount")`).

## 4. Results

Pick the result method that states the expected cardinality:

| Expected | Call |
|---|---|
| Exactly one row | `.mappings().one()` |
| Zero or one row | `.mappings().one_or_none()` |
| Many rows | `.mappings().all()` |
| One scalar | `.scalar_one()` / `.scalar_one_or_none()` |
| A list of scalars | `.scalars().all()` |
| Affected row count | `result.rowcount` |

- Convert rows into a typed read model (frozen `dataclass`, Pydantic model or the project's DTO) before returning; never return `Row` / `RowMapping` / `Result` objects out of the module.
- Use `.returning(...)` on insert/update/delete to get the written row back instead of re-selecting it (PostgreSQL, SQLite ≥ 3.35, MariaDB ≥ 10.5 for insert/delete; not MySQL: re-select there).
- Bulk insert/update: `session.execute(insert(table), [dict, ...])` (executemany), not a loop of single inserts. Return early on an empty list.

## 5. Parameters and safety

- Values always go through the expression API (`column == value`, `.values(...)`, `.in_(...)`), so they are bound parameters.
- **Never** build SQL with f-strings, `%` or `+`. Use `text()` only when the construct is impossible otherwise, with `:name` bind parameters and `.bindparams(...)` or a params dict.
- Dynamic column or order selection comes from an explicit whitelist mapping, never from a raw user string.

## 6. Transactions

- Query functions receive the session as their first parameter and **never** call `commit`, `rollback`, `begin` or `close`: the caller (service, unit of work, request scope) owns the transaction.
- `flush` is not needed: statements are sent to the database by `execute`.

## 7. Async

If the project uses `AsyncSession`: `async def`, `await session.execute(statement)`, then the same result methods. Do not mix sync and async sessions in one module.

## 8. Style

- Type every parameter and return value; filters and options after the session are **keyword-only** (`*`).
- Public functions first, private statement builders (`_filter_users`) after, as in the template.
- Shared filter logic goes into a private builder reused by `list_*` and `count_*`, so both stay consistent.
- No magic values: page sizes and statuses are named constants or enums.
- Google style docstrings on public functions (the `python-docstring` agent can write them).

## Workflow

1. Read the table definition (or model) and the existing data-access code; note its conventions.
2. Read `templates/queries.py` and copy the functions the request needs into the target module.
3. Replace placeholders and example columns, write the specific `where` / `join` / `order_by`.
4. Check: no ORM call from rule 3, explicit columns, right result method, no commit.
5. Run the project's tests and type checker if available; offer to generate tests with `python-test-generator` (tests on a real database or SQLite in memory rather than mocking `session.execute`).
6. Summarize: functions written, their signatures, and any database-specific feature used (`RETURNING`, `ON CONFLICT`…).
