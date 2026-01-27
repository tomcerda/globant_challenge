from fastapi import FastAPI

app = FastAPI(title="Globant Challenge API")

@app.get("/health")
def health():
    return {"status": "ok"}
