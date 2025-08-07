# app/intent_classifier.py

from app.ollama_client import query_llama3

def is_insurance_related(query: str) -> bool:
    prompt = f"""
You are an intent classification assistant for a health insurance bot. Your job is to determine if the following user query is related to insurance (even vaguely).

If the query involves coverage, claims, premiums, hospitals, surgery, medical treatment, policy terms, or anything remotely insurance-related — respond with just one word: "yes".

If the query is unrelated to insurance (e.g., general greetings, life issues, tech questions, travel plans, etc.) — respond with just one word: "no".

Query:
\"\"\"{query}\"\"\"
"""
    try:
        response = query_llama3(prompt).strip().lower()
        return "yes" in response
    except Exception:
        # Fallback: assume non-insurance in case of timeout/failure
        return False
