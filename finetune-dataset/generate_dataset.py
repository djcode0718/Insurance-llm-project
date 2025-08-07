import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import os
from tqdm import tqdm
from app.inference import get_decision
from embed.build_index import load_vectorstore

QUERY_FILE = "finetune-dataset/ins_queries3.txt"
OUTPUT_FILE = "finetune-dataset/fine_data3.jsonl"

def load_queries() -> list:
    with open(QUERY_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def save_record(record: dict, file_path: str):
    with open(file_path, "a") as f:
        f.write(json.dumps(record) + "\n")

def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    queries = load_queries()
    print(f"🔍 Processing {len(queries)} queries...")

    for query in tqdm(queries):
        result = get_decision(query)
        record = {
            "query": query,
            "approval": result.get("approval"),
            "amount": result.get("amount"),
            "justification": result.get("justification"),
            "clause_ids": result.get("clause_ids")
        }
        save_record(record, OUTPUT_FILE)

    print(f"\n✅ Dataset saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
