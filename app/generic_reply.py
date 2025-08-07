# app/generic_reply.py

from app.ollama_client import query_llama3

def generate_generic_reply(query: str) -> str:
    prompt = f"""
You are a friendly chatbot designed to help with health insurance claims. However, the user has asked a question unrelated to insurance.

Reply warmly to the user's question in a helpful or conversational tone. Then, gently remind the user that you specialize in insurance queries and ask them to provide one.

Example:

User: "I have a doubt"
Bot: "Sure! I'm here to help. What's your doubt? Just a heads-up — I specialize in insurance-related topics. Let me know if your question is about a claim, policy, or coverage!"

User: "{query}"
Bot:"""
    
    try:
        response = query_llama3(prompt).strip()
        return response
    except Exception:
        return "I'm happy to help! Just a reminder that I specialize in insurance-related queries. Let me know if you have a question about a policy, claim, or treatment."
