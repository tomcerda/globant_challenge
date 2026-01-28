from sqlalchemy import select
from sqlalchemy.engine import Connection
from ..models import jobs

def job_exists(conn: Connection, job_id: int) -> bool:
    stmt = select(jobs.c.id).where(jobs.c.id == job_id)
    return conn.execute(stmt).first() is not None
