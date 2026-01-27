from sqlalchemy import select
from sqlalchemy.engine import Connection
from ..models import jobs

def job_exists(conn: Connection, job_id: int) -> bool:
    stmt = select(jobs.c.job_id).where(jobs.c.job_id == job_id)
    return conn.execute(stmt).first() is not None

def job_exists_by_name(conn: Connection, job_name: str) -> bool:
    stmt = select(jobs.c.job_id).where(jobs.c.job == job_name)
    return conn.execute(stmt).first() is not None
