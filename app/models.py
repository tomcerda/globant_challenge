from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from .database import metadata

departments = Table(
    "departments", metadata,
    Column("id", Integer, primary_key=True),
    Column("department", String, nullable=False, unique=True)
)

jobs = Table(
    "jobs", metadata,
    Column("id", Integer, primary_key=True),
    Column("job", String, nullable=False, unique=True)
)

employees = Table(
    "employees", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("datetime", DateTime(timezone=True), nullable=False),
    Column("department_id", Integer, ForeignKey("departments.id"), nullable=False),
    Column("job_id", Integer, ForeignKey("jobs.id"), nullable=False),
    UniqueConstraint("name", "datetime", "department_id", "job_id", name="uq_employee_business_key")
)

employees_rejected = Table(
    "employees_rejected", metadata,
    Column("id", Integer, primary_key=True),
    Column("source", String, nullable=False),
    Column("raw_payload", String, nullable=False),
    Column("reject_reason", String, nullable=False),
)
