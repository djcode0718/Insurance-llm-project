# create_tables.py
from auth.db import engine
from auth.models import Base
# from auth import models  # this is important to import MemorySummary

Base.metadata.create_all(bind=engine)
print("✅ Tables created.")
