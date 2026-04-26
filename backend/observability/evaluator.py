def faithfulness_score(answer: str, context: list[str]) -> float:
    if not context:
        return 0.0
    context_blob = " ".join(context).lower()
    answer_tokens = set(answer.lower().split())
    if not answer_tokens:
        return 0.0
    grounded = sum(1 for t in answer_tokens if t in context_blob)
    return grounded / len(answer_tokens)


def context_relevance_score(query: str, context: list[str]) -> float:
    if not context:
        return 0.0
    q_tokens = set(query.lower().split())
    c_tokens = set(" ".join(context).lower().split())
    if not q_tokens:
        return 0.0
    return len(q_tokens.intersection(c_tokens)) / len(q_tokens)


def evaluate_response(query: str, context: list[str], answer: str) -> dict[str, float]:
    return {
        "faithfulness": round(faithfulness_score(answer, context), 3),
        "context_relevance": round(context_relevance_score(query, context), 3),
    }
