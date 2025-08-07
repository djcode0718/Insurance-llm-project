import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.inference import get_decision
import json

if __name__ == "__main__":
    sample_query = "My father had a knee surgery after 3 months of taking the policy. Can we claim?"
    result = get_decision(sample_query)
    print("\n🧪 Test LLM Response:\n", json.dumps(result, indent=2))
