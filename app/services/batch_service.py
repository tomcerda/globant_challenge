import pandas as pd
from sqlalchemy.orm import Session
from app.crud.employees import insert_employees
from app.services.validations import validate_employee_record, log_rejected_records
from app.config import MAX_BATCH_SIZE


def process_batch_employees(db: Session, items: list[dict]):
    # Validate batch size
    if not 1 <= len(items) <= MAX_BATCH_SIZE:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Batch size must be between 1 and {MAX_BATCH_SIZE}")

    valid_records = []
    rejected_records = []

    with db.begin():
        conn = db.connection()

        for r in items:

            # ----------------------------------------------------
            # DATA NORMALIZATION (same logic as CSV ingestion)
            # ----------------------------------------------------

            # Normalize department_id
            try:
                r["department_id"] = int(r["department_id"])
            except:
                r["department_id"] = None

            # Normalize job_id
            try:
                r["job_id"] = int(r["job_id"])
            except:
                r["job_id"] = None

            # Normalize datetime
            try:
                r["datetime"] = pd.to_datetime(r["datetime"], errors="coerce")
                if pd.isna(r["datetime"]):
                    r["datetime"] = None
                else:
                    r["datetime"] = r["datetime"].to_pydatetime()
            except:
                r["datetime"] = None

            # ----------------------------------------------------
            # VALIDATION
            # ----------------------------------------------------
            is_valid, errors = validate_employee_record(conn, r)

            if is_valid:
                valid_records.append(r)
            else:
                rejected_records.append((r, errors))

        # ----------------------------------------------------
        # INSERT VALID RECORDS
        # ----------------------------------------------------
        inserted = insert_employees(conn, valid_records)

        # ----------------------------------------------------
        # LOG REJECTED RECORDS
        # ----------------------------------------------------
        log_rejected_records(conn, source="batch", records_with_errors=rejected_records)

    return {
        "total": len(items),
        "inserted": inserted,
        "rejected": len(rejected_records)
    }
