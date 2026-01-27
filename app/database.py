from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
metadata = MetaData()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
