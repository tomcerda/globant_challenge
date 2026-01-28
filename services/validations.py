import json
from typing import Tuple, List
from sqlalchemy.engine import Connection
from app.crud.departments import department_exists
from app.crud.jobs import job_exists
from app.models import employees_rejected
from sqlalchemy import insert
from datetime import datetime

def validate_employee_record(conn: Connection, record: dict) -> Tuple[bool, List[str]]:
    errors = []

    if not record.get("name"):
        errors.append("Missing or empty name")

    if record.get("datetime") is None:
        errors.append("Missing or invalid datetime")

    if not record.get("department_id"):
        errors.append("Missing department_id")
    elif not department_exists(conn, record["department_id"]):
        errors.append("Invalid department_id (FK violation)")

    if not record.get("job_id"):
        errors.append("Missing job_id")
    elif not job_exists(conn, record["job_id"]):
        errors.append("Invalid job_id (FK violation)")

    return (len(errors) == 0, errors)

def log_rejected_records(conn: Connection, source: str, records_with_errors: list[tuple[dict, list[str]]]):
    if not records_with_errors:
        return
    payloads = []
    for record, errors in records_with_errors:
        payloads.append({
            "source": source,
            "raw_payload": json.dumps(record, default=str),
            "reject_reason": "; ".join(errors),
        })
    stmt = insert(employees_rejected)
    conn.execute(stmt, payloads)
