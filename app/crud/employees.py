from sqlalchemy import insert
from sqlalchemy.engine import Connection
from ..models import employees

def insert_employee(conn: Connection, name: str, date, department_id: int, job_id: int):
    stmt = insert(employees).values(
        name=name,
        datetime=date,
        department_id=department_id,
        job_id=job_id
    )
    conn.execute(stmt)
