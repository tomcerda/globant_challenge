from fastapi import FastAPI
from app.routers import upload, employees, metrics

app = FastAPI(title="Globant Challenge API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
