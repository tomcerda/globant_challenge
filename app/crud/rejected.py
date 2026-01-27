from sqlalchemy import insert
from sqlalchemy.engine import Connection
from ..models import employees_rejected

def insert_rejected(conn: Connection, row: dict, reason: str):
    stmt = insert(employees_rejected).values(
        name=row.get("name"),
        datetime=row.get("datetime"),
        department=row.get("department"),
        job=row.get("job"),
        reason=reason
    )
    conn.execute(stmt)
