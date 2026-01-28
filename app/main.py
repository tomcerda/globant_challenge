from fastapi import FastAPI
from app.routers import upload, employees, metrics
import subprocess

app = FastAPI(title="Globant Challenge API")


@app.on_event("startup")
def run_migrations():
    subprocess.run(
        ["alembic", "upgrade", "head"],
        check=True
    )


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
