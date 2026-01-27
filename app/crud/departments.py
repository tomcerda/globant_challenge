from sqlalchemy import select
from sqlalchemy.engine import Connection
from ..models import departments

def department_exists(conn: Connection, department_id: int) -> bool:
    stmt = select(departments.c.id).where(departments.c.id == department_id)
    return conn.execute(stmt).first() is not None
