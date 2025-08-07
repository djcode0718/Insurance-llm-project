from embed.build_index import load_vectorstore
from app.ollama_client import query_llama3

from app.memory_utils import get_memory_for_user
# from auth.models import MemorySummary

from app.intent_classifier import is_insurance_related
from app.generic_reply import generate_generic_reply  # <-- new

SYSTEM_PROMPT = """You are an insurance claim decision assistant. 
You are given a query and a few relevant clauses from an insurance policy.
Your job is to:

1. Decide if the claim should be approved or rejected.
2. Provide the amount to be approved (estimate it from the clauses).
3. Justify your decision using clause references and reasons.
4. Return ONLY the following format:

Approval: Yes/No  
Amount: ₹[amount]  
Justification: [your reasoning here]  
Clause IDs Used: [comma separated clause IDs]

If the query is not related to insurance or health or is too vague, respond exactly as:

Approval: No  
Amount: ₹0  
Justification: Query is irrelevant or too vague.  
Clause IDs Used: []
"""

# Load vectorstore once
vectorstore = load_vectorstore()

def get_decision(query: str) -> dict:
    # # Step 1 – Filter short/irrelevant queries
    # if len(query.strip()) < 10 or query.lower().strip() in ["hello", "hi", "help", "yes", "no"]:
    #     return {
    #         "approval": "No",
    #         "amount": "₹0",
    #         "justification": "Query is irrelevant or too vague.",
    #         "clause_ids": []
    #     }

    # Step 1 – Use LLaMA3-based intent classifier
    if not is_insurance_related(query):
        print("Non insurance related question.")
        return generate_generic_reply(query)  # Smart polite fallback

    # Step 2 – Semantic search for relevant clauses
    docs_and_scores = vectorstore.similarity_search_with_score(query, k=5)

    relevant_clauses = []
    clause_ids_used = []

    for doc, score in docs_and_scores:
        if score < 0.4:
            continue
        relevant_clauses.append(doc.page_content)
        if 'clause_id' in doc.metadata:
            clause_ids_used.append(doc.metadata['clause_id'])

    if not relevant_clauses:
        print("Not relevant query, information not present in the clauses")
        return {
            "approval": "No",
            "amount": "₹0",
            "justification": "Query is irrelevant or does not match any insurance clauses.",
            "clause_ids": []
        }

    # Step 3 – Build single prompt
    context = "\n".join(relevant_clauses)
    prompt = f"""{SYSTEM_PROMPT}

CLAUSES:
{context}

QUERY:
{query}
"""

    # Step 4 – Query LLM
    llm_response = query_llama3(prompt)

    # Step 5 – Parse response
    return {
        "approval": extract_field(llm_response, "Approval"),
        "amount": extract_field(llm_response, "Amount"),
        "justification": extract_field(llm_response, "Justification"),
        "clause_ids": clause_ids_used,
    }

def extract_field(text, field):
    for line in text.splitlines():
        if line.lower().startswith(field.lower() + ":"):
            return line.split(":", 1)[1].strip()
    return ""

# def generate_summary(user_id: int, query: str, response: str) -> str:
#     prompt = f"""Summarize the key long-term memory from this user exchange:
# User Query: {query}
# System Response: {response}

# Summary (in one sentence):"""
#     summary = query_llama3(prompt)  # use your Ollama or GPT endpoint
#     return summary.strip()

# # 🧠 New memory-aware functionality
# def get_memory_for_user(user_id: int) -> str:
#     db = get_db_session()
#     try:
#         memory = db.query(MemorySummary).filter_by(user_id=user_id).first()
#         return memory.summary if memory else ""
#     finally:
#         db.close()

def get_decision_with_memory(query: str, user_id: int) -> dict:
    memory = get_memory_for_user(user_id)
    prompt = f"""
{SYSTEM_PROMPT}

MEMORY:
{memory}

QUERY:
{query}
"""
    llm_response = query_llama3(prompt)

    return {
        "approval": extract_field(llm_response, "Approval"),
        "amount": extract_field(llm_response, "Amount"),
        "justification": extract_field(llm_response, "Justification"),
        "clause_ids": [],  # Optional: You can re-use the vectorstore logic if clause relevance is still required
    }
