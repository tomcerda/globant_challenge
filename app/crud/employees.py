from sqlalchemy.engine import Connection
from sqlalchemy.dialects.postgresql import insert as pg_insert
from ..models import employees


def insert_employees(conn: Connection, records: list[dict]):
    if not records:
        return 0

    stmt = (
        pg_insert(employees)
        .on_conflict_do_nothing(index_elements=["id"])
    )

    result = conn.execute(stmt, records)
    return result.rowcount or 0

