from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

router = APIRouter(prefix="/metrics", tags=["metrics"])

RAG_REQUESTS = Counter("rag_requests_total", "Total RAG metric requests")
RAG_LATENCY = Histogram("rag_latency_seconds", "RAG latency")


@router.get("/rag")
def get_rag_metrics() -> dict[str, float]:
    RAG_REQUESTS.inc()
    with RAG_LATENCY.time():
        return {
            "recall_at_5": 0.0,
            "faithfulness": 0.0,
            "latency_ms": 0.0,
        }


@router.get("", include_in_schema=False)
def prometheus_metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
