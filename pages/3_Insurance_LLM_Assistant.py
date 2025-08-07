import streamlit as st
from app.inference import get_decision
from app.memory_utils import generate_summary
from app.memory_utils import save_chat_session, save_memory_summary
from auth.db import get_db_session  # ✅ Import get_db

import time
import threading

# Check login
if "user_id" not in st.session_state:
    st.warning("Please log in to access this page.")
    st.switch_page("pages/1_Login.py")

st.sidebar.title("🔐 Account")
st.sidebar.markdown(f"👋 Logged in as **{st.session_state.get('username', 'User')}**")
if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.success("You have been logged out.")
    st.rerun()

# Page setup
st.set_page_config(page_title="Insurance LLM Assistant", layout="centered")

st.sidebar.page_link("pages/4_Memory.py", label="🧠 View/Edit Memory")

st.title("🧠 Insurance LLM Assistant")
st.markdown("Enter a query like: `46-year-old male, knee surgery in Pune, 3-month-old insurance policy`")

# User input
user_input = st.text_area("📝 Your insurance case query:", height=150)

# Action button
if st.button("🔍 Get Decision") and user_input.strip():
    # with st.spinner("Processing your query..."):
    #     result = get_decision(user_input)

    # Start dynamic progress loader
    progress_bar = st.progress(0)
    status_text = st.empty()

    def animate_progress(stop_event):
        progress = 0
        while not stop_event.is_set():
            progress = (progress + 1) % 100
            progress_bar.progress(progress)
            time.sleep(0.05)

    stop_event = threading.Event()
    progress_thread = threading.Thread(target=animate_progress, args=(stop_event,))
    progress_thread.start()

    status_text.markdown("🧠 **Talking to LLaMA... Please wait.**")

    # Measure response time
    start_time = time.time()
    result = get_decision(user_input)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    stop_event.set()
    progress_thread.join()
    progress_bar.progress(100)
    status_text.markdown(f"✅ **Response received in {elapsed_time} seconds.**")

    # ✅ Use an actual session instance from generator
    db = get_db_session()

    user_id = st.session_state["user_id"]
    summary = generate_summary(user_id, user_input, str(result))
    save_memory_summary(user_id, summary)

    save_chat_session(
        # db=db,  # Pass the session explicitly
        user_id=st.session_state["user_id"],
        query=user_input,
        response=str(result)
    )

    # # Show results
    # st.markdown("---")
    # st.subheader("🧾 Decision Summary")

    # col1, col2 = st.columns(2)
    # with col1:
    #     st.markdown(f"**🟢 Approval:** `{result.get('approval', 'N/A')}`")
    # with col2:
    #     st.markdown(f"**💰 Amount:** `{result.get('amount', '₹0')}`")

    # st.markdown("**🧠 Justification:**")
    # st.info(result.get("justification", "No justification provided."), icon="💡")

    # clause_ids = result.get("clause_ids", [])
    # if clause_ids:
    #     st.markdown("**📄 Clause IDs Used:**")
    #     st.code(", ".join(clause_ids), language="text")
    # else:
    #     st.warning("No relevant clauses matched.", icon="⚠️")

    # st.markdown("---")
    # st.success("✅ Decision complete.")


    # Show results
    st.markdown("---")

    if isinstance(result, dict):
        st.subheader("🧾 Decision Summary")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**🟢 Approval:** `{result.get('approval', 'N/A')}`")
        with col2:
            st.markdown(f"**💰 Amount:** `{result.get('amount', '₹0')}`")

        st.markdown("**🧠 Justification:**")
        st.info(result.get("justification", "No justification provided."), icon="💡")

        clause_ids = result.get("clause_ids", [])
        if clause_ids:
            st.markdown("**📄 Clause IDs Used:**")
            st.code(", ".join(clause_ids), language="text")
        else:
            st.warning("No relevant clauses matched.", icon="⚠️")

        st.success("✅ Decision complete.")

    else:
        # It's a generic LLM reply (string)
        st.subheader("🤖 Assistant")
        st.info(result, icon="💬")
        st.markdown("Feel free to ask me an insurance-related query when you're ready!")

