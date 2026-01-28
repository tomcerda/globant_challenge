import os
import pandas as pd
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.config import settings
from app.database import engine
from app.crud.employees import insert_employees
from validations import validate_employee_record, log_rejected_records

def _load_csv(filename: str, columns: list[str]) -> list[dict]:
    path = os.path.join(settings.DATA_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"File not found: {path}")
    df = pd.read_csv(path, header=None)
    df.columns = columns
    return df.to_dict(orient="records")

def ingest_employees_from_csv():
    records = _load_csv(
        "hired_employees.csv",
        ["id", "name", "datetime", "department_id", "job_id"]
    )

    valid_records = []
    rejected_records = []

    with engine.begin() as conn:
        for r in records:
            # Types normalization
            try:
                r["department_id"] = int(r["department_id"])
            except Exception:
                r["department_id"] = None

            try:
                r["job_id"] = int(r["job_id"])
            except Exception:
                r["job_id"] = None

            # Pandas datetime parsing
            try:
                r["datetime"] = pd.to_datetime(r["datetime"], errors="coerce")
                if pd.isna(r["datetime"]):
                    r["datetime"] = None
                else:
                    r["datetime"] = r["datetime"].to_pydatetime()
            except Exception:
                r["datetime"] = None

            is_valid, errors = validate_employee_record(conn, r)
            if is_valid:
                valid_records.append(r)
            else:
                rejected_records.append((r, errors))

        inserted = insert_employees(conn, valid_records)
        log_rejected_records(conn, source="csv", records_with_errors=rejected_records)

    return {
        "total": len(records),
        "inserted": inserted,
        "rejected": len(rejected_records)
    }
