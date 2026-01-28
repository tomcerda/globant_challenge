import os
import pandas as pd
from fastapi import HTTPException
from sqlalchemy import insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.config import settings
from app.database import engine
from app.models import departments, jobs
from app.crud.employees import insert_employees
from app.services.validations import log_rejected_records


def _load_csv(filename: str, columns: list[str]) -> list[dict]:
    path = os.path.join(settings.DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    df = pd.read_csv(path, header=None)
    df.columns = columns
    return df.to_dict(orient="records")


def ingest_all_from_csv():
    # 1. Load all CSVs
    departments_data = _load_csv("departments.csv", ["id", "department"])
    jobs_data = _load_csv("jobs.csv", ["id", "job"])
    employees_data = _load_csv(
        "hired_employees.csv",
        ["id", "name", "datetime", "department_id", "job_id"]
    )

    # 2. Build in-memory FK sets (O(1) lookup)
    existing_departments = {d["id"] for d in departments_data}
    existing_jobs = {j["id"] for j in jobs_data}

    valid_records = []
    rejected_records = []

    with engine.begin() as conn:
        # 3. Insert departments (idempotent)
        dept_stmt = (
            pg_insert(departments)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        conn.execute(dept_stmt, departments_data)

        # 4. Insert jobs (idempotent)
        job_stmt = (
            pg_insert(jobs)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        conn.execute(job_stmt, jobs_data)

        # 5. Validate employees using in-memory sets
        for r in employees_data:
            errors = []

            # Normalize types
            try:
                r["department_id"] = int(r["department_id"])
            except:
                r["department_id"] = None

            try:
                r["job_id"] = int(r["job_id"])
            except:
                r["job_id"] = None

            try:
                r["datetime"] = pd.to_datetime(r["datetime"], errors="coerce")
                if pd.isna(r["datetime"]):
                    r["datetime"] = None
                else:
                    r["datetime"] = r["datetime"].to_pydatetime()
            except:
                r["datetime"] = None

            # Validate fields
            if not r.get("name"):
                errors.append("Missing or empty name")

            if r.get("datetime") is None:
                errors.append("Missing or invalid datetime")

            if r.get("department_id") not in existing_departments:
                errors.append("Invalid department_id (FK violation)")

            if r.get("job_id") not in existing_jobs:
                errors.append("Invalid job_id (FK violation)")

            if errors:
                rejected_records.append((r, errors))
            else:
                valid_records.append(r)

        # 6. Insert valid employees
        inserted = insert_employees(conn, valid_records)

        # 7. Log rejected
        log_rejected_records(conn, "csv", rejected_records)

    return {
        "departments_inserted": len(departments_data),
        "jobs_inserted": len(jobs_data),
        "employees_total": len(employees_data),
        "employees_inserted": inserted,
        "employees_rejected": len(rejected_records)
    }
