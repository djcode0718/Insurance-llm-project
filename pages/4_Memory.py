import streamlit as st
from auth.db import get_db_session
from auth.models import MemorySummary
from sqlalchemy.exc import SQLAlchemyError

st.set_page_config(page_title="🧠 Your Memory", layout="centered")

st.sidebar.page_link("pages/4_Memory.py", label="🧠 View/Edit Memory")

st.title("🧠 Memory Summary")
st.markdown("View, edit, or delete your personalized memory used by the assistant.")

# Check login
if "user_id" not in st.session_state:
    st.warning("Please log in to access this page.")
    st.switch_page("pages/1_Login.py")

user_id = st.session_state["user_id"]

db = get_db_session()


memories = db.query(MemorySummary).filter_by(user_id=user_id).order_by(MemorySummary.created_at.desc()).all()

if memories:
    for memory in memories:
        with st.expander(f"🕓 {memory.created_at.strftime('%Y-%m-%d %H:%M:%S')}"):
            edited = st.text_area(f"Summary ID {memory.id}", value=memory.summary, height=150, key=f"edit_{memory.id}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save", key=f"save_{memory.id}"):
                    memory.summary = edited
                    try:
                        db.commit()
                        st.success("Memory updated.")
                        st.rerun()
                    except SQLAlchemyError:
                        db.rollback()
                        st.error("Update failed.")

            with col2:
                if st.button("🗑️ Delete", key=f"delete_{memory.id}"):
                    try:
                        db.delete(memory)
                        db.commit()
                        st.success("Memory deleted.")
                        st.rerun()
                    except SQLAlchemyError:
                        db.rollback()
                        st.error("Delete failed.")
else:
    st.info("No memory has been saved yet for your account.")


db.close()
