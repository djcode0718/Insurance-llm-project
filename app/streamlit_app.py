import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.inference import get_decision

st.set_page_config(page_title="Insurance LLM Assistant", layout="centered")

st.title("🧠 Insurance LLM Assistant")
st.markdown("Enter a query like: `46-year-old male, knee surgery in Pune, 3-month-old insurance policy`")

user_input = st.text_area("📝 Your insurance case query:", height=150)

if st.button("🔍 Get Decision"):
    with st.spinner("Processing your query..."):
        result = get_decision(user_input)

    # Display structured result
    st.markdown("---")
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

    st.markdown("---")
    st.success("✅ Decision complete.")
