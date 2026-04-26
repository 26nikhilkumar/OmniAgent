# OmniAgent

OmniAgent is an end-to-end **production-style AI agent system template** that includes LangGraph orchestration, hybrid retrieval, GraphRAG, API + UI surfaces, async worker wiring, observability hooks, deployment config, and CI.

## Why this project is different
- ✅ Real **LangGraph** state machine with conditional routing and checkpointing.
- ✅ **Hybrid retrieval** path with dense + sparse scoring and optional cross-encoder reranking.
- ✅ **Neo4j GraphRAG** backend for entity graph traversal.
- ✅ **MCP-style tool interfaces** with discoverable/callable server methods.
- ✅ **Observability hooks** (quality evaluator + tracing + Prometheus metrics endpoint).

## Architecture

```mermaid
flowchart TD
    UI[Streamlit UI] --> API[FastAPI]
    API --> CELERY[Celery Worker]
    API --> LG[LangGraph Orchestrator]
    LG --> RAG[Hybrid Retriever]
    LG --> GRAPH[Neo4j GraphRAG]
    LG --> MCP[MCP Server/Tools]
    API --> METRICS[/metrics + /metrics/rag]
```

## Delivered components

### Agent core
- Multi-agent orchestration pipeline: planner → researcher → analyst → writer → scheduler.
- Shared typed runtime state and conditional routing.
- LangGraph `StateGraph` with memory checkpointer.

### Retrieval stack
- Document loading and chunking.
- Hybrid retrieval (`BM25 + dense embeddings`) with fallback mode.
- Optional cross-encoder reranking.
- Neo4j-backed GraphRAG entity relationships.

### Backend + observability
- FastAPI routes:
  - `GET /health`
  - `POST /tasks/run`
  - `POST /tasks/submit`
  - `GET /tasks/{task_id}`
  - `GET /metrics/rag`
  - `GET /metrics` (Prometheus format)
- Evaluation metrics for faithfulness/context relevance.
- Tracing helper for span timings.

### Frontend + ops
- Streamlit dashboard for task submission and result inspection.
- Dockerfiles + Docker Compose stack (redis + neo4j + backend + worker + frontend).
- Render deployment manifest.
- GitHub Actions CI workflow.

---

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
make run-api
```

In another terminal:

```bash
make run-ui
```

## Run docker stack

```bash
docker compose up --build
```

## Useful commands

```bash
make test
make ingest
make evaluate
make export-finetune
```

## Performance (placeholder baseline)

| Metric | Current |
|---|---:|
| Recall@5 | 0.00 |
| Faithfulness | 0.00 |
| Latency | 0 ms |

## Testimonial (placeholder)

> "OmniAgent helped me automate recurring research workflows." — _Future user testimonial_
