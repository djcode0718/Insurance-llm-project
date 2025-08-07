from auth.models import Base
from auth.db import engine

if __name__ == "__main__":
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
