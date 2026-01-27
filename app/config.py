import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://user:password@localhost:5432/challenge"
    )
    DATA_DIR: str = os.getenv("DATA_DIR", "data")

settings = Settings()

# For debugging purposes
print("DATABASE_URL:", settings.DATABASE_URL)