from app.database import engine, metadata
from app import models  # ← IMPORTANTE: esto registra las tablas en metadata
from app.config import settings

print("Using DATABASE_URL:", settings.DATABASE_URL)

metadata.create_all(engine)
print("Tables created successfully")


