from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.observability.evaluator import evaluate_response


if __name__ == "__main__":
    result = evaluate_response(
        query="What is OmniAgent?",
        context=["OmniAgent is a production-aware multi-agent starter."],
        answer="OmniAgent is a production-aware multi-agent starter.",
    )
    print(result)
