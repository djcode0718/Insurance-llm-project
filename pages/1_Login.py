import streamlit as st
from auth.db import get_db_session
from auth.auth_handler import authenticate_user

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    db = get_db_session()
    result = authenticate_user(db, username, password)
    db.close()

    if result["success"]:
        st.session_state["user_id"] = result["user_id"]
        st.success("Login successful! Redirecting...")
        st.switch_page("pages/3_Insurance_LLM_Assistant.py")
    else:
        st.error(result["error"])

if st.button("Don't have an account? Sign Up"):
    st.switch_page("pages/2_Signup.py")
