from fastapi import APIRouter
from ..services.metrics_service import hires_by_quarter, departments_above_mean

router = APIRouter()

@router.get("/hires-by-quarter")
def get_hires_by_quarter():
    return hires_by_quarter()

@router.get("/departments-above-mean")
def get_departments_above_mean():
    return departments_above_mean()
