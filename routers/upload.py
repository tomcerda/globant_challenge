from fastapi import APIRouter
from ..services.csv_ingestion import ingest_employees_from_csv

router = APIRouter()

@router.post("/employees")
def upload_employees_from_csv():
    """
    Ingest employees from a CSV file and return a summary of the operation.
    """
    return ingest_employees_from_csv()
