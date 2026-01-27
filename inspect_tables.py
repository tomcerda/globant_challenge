from sqlalchemy import inspect
from app.database import engine

inspector = inspect(engine)
print("Tables:", inspector.get_table_names())
