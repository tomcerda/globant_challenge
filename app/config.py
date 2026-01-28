import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # app/
        self.BASE_DIR = Path(__file__).resolve().parent

        # app/data por defecto
        self.DATA_DIR = Path(os.getenv("DATA_DIR", self.BASE_DIR / "data"))

        # DB
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://user:password@localhost:5432/challenge"
        )

settings = Settings()

print("BASE_DIR:", settings.BASE_DIR)
print("DATA_DIR:", settings.DATA_DIR)
