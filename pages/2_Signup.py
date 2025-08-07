import streamlit as st
from auth.db import get_db_session
from auth.auth_handler import register_user

st.set_page_config(page_title="Sign Up", layout="centered")
st.title("📝 Create Account")

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    db = get_db_session()
    result = register_user(db, username, email, password)
    db.close()

    if result["success"]:
        st.success("Account created! You can now log in.")
        st.switch_page("pages/1_Login.py")
    else:
        st.error(result["error"])

if st.button("Already have an account? Login"):
    st.switch_page("pages/1_Login.py")
