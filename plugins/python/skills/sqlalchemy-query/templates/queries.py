"""Queries on the __entities__ table, executed with ``session.execute``."""

from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy import Select, delete, func, insert, select, update
from sqlalchemy.orm import Session

from __tables_module__ import __entities__

DEFAULT_PAGE_SIZE = 50


@dataclass(frozen=True, slots=True)
class __Entity__:
    """Read model of a __entity__ row."""

    id: int
    name: str
    is_active: bool


__ENTITY___COLUMNS = (
    __entities__.c.id,
    __entities__.c.name,
    __entities__.c.is_active,
)


def get___entity__(session: Session, __entity___id: int) -> __Entity__ | None:
    """Fetches one __entity__ by id.

    Args:
        session: Session the query runs in.
        __entity___id: Id of the __entity__ to fetch.

    Returns:
        The __entity__, or None when no row has this id.
    """
    statement = select(*__ENTITY___COLUMNS).where(__entities__.c.id == __entity___id)
    row = session.execute(statement).mappings().one_or_none()
    if row is None:
        return None
    return __Entity__(**row)


def list___entities__(
    session: Session,
    *,
    is_active: bool | None = None,
    limit: int = DEFAULT_PAGE_SIZE,
    offset: int = 0,
) -> list[__Entity__]:
    """Lists __entities__, optionally filtered, ordered by id.

    Args:
        session: Session the query runs in.
        is_active: Keeps only __entities__ with this status when given.
        limit: Maximum number of rows returned.
        offset: Number of rows skipped.

    Returns:
        The matching __entities__, possibly empty.
    """
    statement = (
        _filter___entities__(select(*__ENTITY___COLUMNS), is_active=is_active)
        .order_by(__entities__.c.id)
        .limit(limit)
        .offset(offset)
    )
    rows = session.execute(statement).mappings().all()
    return [__Entity__(**row) for row in rows]


def count___entities__(session: Session, *, is_active: bool | None = None) -> int:
    """Counts __entities__, with the same filters as ``list___entities__``.

    Args:
        session: Session the query runs in.
        is_active: Counts only __entities__ with this status when given.

    Returns:
        The number of matching __entities__.
    """
    statement = _filter___entities__(
        select(func.count()).select_from(__entities__), is_active=is_active
    )
    return session.execute(statement).scalar_one()


def create___entity__(session: Session, *, name: str, is_active: bool = True) -> __Entity__:
    """Inserts one __entity__ and returns it as stored.

    Args:
        session: Session the query runs in.
        name: Name of the new __entity__.
        is_active: Initial status of the new __entity__.

    Returns:
        The created __entity__, with its generated id.
    """
    statement = (
        insert(__entities__)
        .values(name=name, is_active=is_active)
        .returning(*__ENTITY___COLUMNS)
    )
    row = session.execute(statement).mappings().one()
    return __Entity__(**row)


def create___entities__(session: Session, names: Sequence[str]) -> None:
    """Inserts several active __entities__ in one round trip.

    Args:
        session: Session the query runs in.
        names: Names of the __entities__ to create.
    """
    if not names:
        return
    session.execute(
        insert(__entities__),
        [{"name": name, "is_active": True} for name in names],
    )


def rename___entity__(session: Session, __entity___id: int, name: str) -> __Entity__ | None:
    """Renames one __entity__.

    Args:
        session: Session the query runs in.
        __entity___id: Id of the __entity__ to rename.
        name: New name.

    Returns:
        The updated __entity__, or None when no row has this id.
    """
    statement = (
        update(__entities__)
        .where(__entities__.c.id == __entity___id)
        .values(name=name)
        .returning(*__ENTITY___COLUMNS)
    )
    row = session.execute(statement).mappings().one_or_none()
    if row is None:
        return None
    return __Entity__(**row)


def delete___entity__(session: Session, __entity___id: int) -> bool:
    """Deletes one __entity__.

    Args:
        session: Session the query runs in.
        __entity___id: Id of the __entity__ to delete.

    Returns:
        True when a row was deleted, False when no row has this id.
    """
    statement = delete(__entities__).where(__entities__.c.id == __entity___id)
    result = session.execute(statement)
    return result.rowcount > 0


def _filter___entities__(statement: Select, *, is_active: bool | None) -> Select:
    if is_active is not None:
        statement = statement.where(__entities__.c.is_active == is_active)
    return statement
