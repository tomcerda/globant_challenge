from fastapi import APIRouter
from app.services.csv_ingestion import ingest_all_from_csv

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
def upload_all():
    return ingest_all_from_csv()

