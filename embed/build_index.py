import json
import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Path constants
DATA_FILE = "app/clauses.jsonl"
INDEX_FILE = "embed/faiss_index.index"
STORE_FILE = "embed/faiss_store.pkl"

# Load embedding model
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_clauses():
    documents = []
    with open(DATA_FILE, "r") as f:
        for line in f:
            item = json.loads(line)
            metadata = {
                "doc_id": item.get("doc_id"),
                "clause_id": item.get("clause_id"),
            }
            documents.append(Document(page_content=item["text"], metadata=metadata))
    return documents

def build_index():
    print("Loading documents...")
    documents = load_clauses()

    print("Building FAISS index...")
    vectorstore = FAISS.from_documents(documents, embedding=EMBEDDING_MODEL)

    print(f"Saving index to {INDEX_FILE} and docstore to {STORE_FILE}")
    vectorstore.save_local(folder_path="embed", index_name="faiss_index")
    print("Index built and saved successfully.")

def load_vectorstore():
    print("Loading FAISS index...")
    return FAISS.load_local(
        folder_path="embed",
        index_name="faiss_index",
        embeddings=EMBEDDING_MODEL,
        allow_dangerous_deserialization=True
    )

if __name__ == "__main__":
    build_index()
