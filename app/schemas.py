from datetime import datetime
from pydantic import BaseModel, Field

class EmployeeBase(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int


class EmployeeBatchItem(EmployeeBase):
    pass

class BatchResult(BaseModel):
    total: int
    inserted: int
    rejected: int
