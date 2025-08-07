from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite DB path (you can change this if needed)
DATABASE_URL = "sqlite:///auth_user_data.db"

# SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to get a session
# def get_db_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def get_db_session():
    return SessionLocal()
