from fastapi import APIRouter

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/rag")
def get_rag_metrics() -> dict[str, float]:
    # Placeholder metrics; wire this to evaluation history storage in production.
    return {
        "recall_at_5": 0.0,
        "faithfulness": 0.0,
        "latency_ms": 0.0,
    }
