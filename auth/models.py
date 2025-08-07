from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
# from auth.db import get_db_session
# from app.memory_utils import is_new_summary

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("ChatSession", back_populates="user")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")

# # --- Chat session utilities ---

# def save_chat_session(user_id, query, response):
#     db = get_db_session()  # Use the generator properly
#     try:
#         existing = db.query(ChatSession).filter_by(user_id=user_id, query=query, response=response).first()
#         if existing:
#             return  # Skip saving duplicate
#         chat = ChatSession(user_id=user_id, query=query, response=response)
#         db.add(chat)
#         db.commit()
#     finally:
#         db.close()

# def get_user_sessions(user_id: int, limit: int = 10):
#     session = get_db_session()
#     try:
#         return session.query(ChatSession)\
#                       .filter(ChatSession.user_id == user_id)\
#                       .order_by(ChatSession.timestamp.desc())\
#                       .limit(limit)\
#                       .all()
#     finally:
#         session.close()
    

class MemorySummary(Base):
    __tablename__ = "memory_summaries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="memories")

User.memories = relationship("MemorySummary", back_populates="user", cascade="all, delete-orphan")


# def save_memory_summary(user_id: int, summary: str):
#     db = get_db_session()
#     try:
#         # Check all existing summaries
#         existing_summaries = db.query(MemorySummary).filter_by(user_id=user_id).all()
#         if not is_new_summary(summary, [m.summary for m in existing_summaries]):
#             return  # Duplicate or similar — do not add

#         new_memory = MemorySummary(user_id=user_id, summary=summary)
#         db.add(new_memory)
#         db.commit()
#     finally:
#         db.close()

