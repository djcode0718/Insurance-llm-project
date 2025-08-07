from app.ollama_client import query_llama3
from auth.db import get_db_session
from auth.models import MemorySummary
from difflib import SequenceMatcher
from auth.models import ChatSession


def generate_summary(user_id: int, query: str, response: str) -> str:
    prompt = f"""Summarize the key long-term memory from this user exchange:
User Query: {query}
System Response: {response}

Summary (in one sentence):"""
    summary = query_llama3(prompt)
    return summary.strip()

# 🧠 New memory-aware functionality
def get_memory_for_user(user_id: int) -> str:
    db = get_db_session()
    try:
        memory = db.query(MemorySummary).filter_by(user_id=user_id).first()
        return memory.summary if memory else ""
    finally:
        db.close()



def is_similar(a: str, b: str, threshold: float = 0.85) -> bool:
    """Check if two summaries are similar based on string similarity."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() > threshold

# def is_new_summary(new_summary, existing_summaries):
#     for summary in existing_summaries:
#         similarity = SequenceMatcher(None, new_summary, summary.summary).ratio()
#         if similarity > 0.8:
#             return False
#     return True

def is_new_summary(new_summary, existing_summaries):

    for summary in existing_summaries:
        prompt = f"""Determine whether the following two insurance memory summaries describe the SAME case or DIFFERENT cases.

Summary A:
{summary}

Summary B:
{new_summary}

Respond with only one word: "same" or "different"."""

        result = query_llama3(prompt)
        if "same" in result.lower():
            return False  # already exists

    return True  # no matches found

# --- Chat session utilities ---

def save_chat_session(user_id, query, response):
    db = get_db_session()  # Use the generator properly
    try:
        existing = db.query(ChatSession).filter_by(user_id=user_id, query=query, response=response).first()
        if existing:
            return  # Skip saving duplicate
        chat = ChatSession(user_id=user_id, query=query, response=response)
        db.add(chat)
        db.commit()
    finally:
        db.close()

def get_user_sessions(user_id: int, limit: int = 10):
    session = get_db_session()
    try:
        return session.query(ChatSession)\
                      .filter(ChatSession.user_id == user_id)\
                      .order_by(ChatSession.timestamp.desc())\
                      .limit(limit)\
                      .all()
    finally:
        session.close()

def save_memory_summary(user_id: int, summary: str):
    db = get_db_session()
    try:
        # Check all existing summaries
        existing_summaries = db.query(MemorySummary).filter_by(user_id=user_id).all()
        if not is_new_summary(summary, [m.summary for m in existing_summaries]):
            print("Duplicate or similar, not adding in summary.")
            return  # Duplicate or similar — do not add
        print("New query, adding into memory.")
        new_memory = MemorySummary(user_id=user_id, summary=summary)
        db.add(new_memory)
        db.commit()
    finally:
        db.close()

