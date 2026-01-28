from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_session
from app.schemas import EmployeeBatchItem, BatchResult
from ..services.batch_service import process_batch_employees

router = APIRouter()

@router.post("/batch", response_model=BatchResult)
def batch_employees(
    items: list[EmployeeBatchItem],
    db: Session = Depends(get_session),
):
    return process_batch_employees(db, [item.dict() for item in items])
