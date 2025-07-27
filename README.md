# 🧠 Insurance LLM Assistant

A smart assistant that uses a fine-tuned LLM to decide insurance claim approvals based on user queries and insurance policy clauses.

## 🔍 Overview

This tool helps automate insurance claim decisions. Just enter a natural language query like:

> *"46-year-old male, knee surgery in Pune, 3-month-old insurance policy"*

The assistant will:
- Search relevant clauses using vector similarity
- Use a local LLM (LLaMA 3 via Ollama) to reason over them
- Return a structured decision including approval, amount, justification, and clause references.

---

## 🏗️ Project Structure

INSURANCE_LLM-PROJECT/
├── app/
│ ├── clauses.jsonl # Insurance policy clauses
│ ├── inference.py # Main logic: query → retrieval → LLM → output
│ ├── ollama_client.py # Calls to LLaMA 3 via Ollama
│ ├── streamlit_app.py # Frontend using Streamlit
│ └── init.py
│
├── embed/
│ └── build_index.py # Embeds clauses using MiniLM and builds FAISS index
│
├── requirements.txt # Dependencies
└── README.md # This file

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### 1. 🐍 Create & Activate Virtual Environment

```bash
conda create -n ins-env python=3.11 -y
conda activate ins-env
2. 💾 Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
If using Ollama, also install it from https://ollama.com and run:

bash
Copy
Edit
ollama run llama3
3. 📦 Build the Clause Index
Make sure clauses.jsonl exists, then:

bash
Copy
Edit
python embed/build_index.py
4. 🧠 Run the Assistant
bash
Copy
Edit
streamlit run app/streamlit_app.py
🧪 Example Output
Input:

hello guys I am ill

Output:

yaml
Copy
Edit
Approval: No
Amount: ₹0
Justification: Query is irrelevant or too vague.
Clause IDs Used: []
🛠️ Technologies Used
LLM: LLaMA 3 via Ollama

Embeddings: MiniLM (via sentence-transformers)

Vector Search: FAISS

UI: Streamlit

Backend Logic: Python

📘 Notes
Queries that are vague or irrelevant are automatically rejected.

You can fine-tune or swap the embedding or LLM model based on compute constraints.
