# OmniAgent

OmniAgent is an end-to-end **production-style AI agent system template** that includes orchestration, retrieval, API + UI surfaces, async worker wiring, observability hooks, deployment config, and CI.

## Delivered components

### Agent core
- Multi-agent orchestration pipeline: planner → researcher → analyst → writer → scheduler.
- Shared typed runtime state and deterministic plan execution.
- MCP-style tool abstraction (`MCPClient`) and local MCP server stub (`OmniMCPServer`).

### RAG stack
- Document loading and chunking utilities.
- Hybrid retrieval utility (BM25 + overlap scoring).
- Lightweight GraphRAG utility via co-occurrence graph.
- In-memory vector store fallback abstraction.

### Backend + async
- FastAPI routes:
  - `GET /health`
  - `POST /tasks/run`
  - `POST /tasks/submit`
  - `GET /tasks/{task_id}`
  - `GET /metrics/rag`
- Celery + Redis wiring for worker execution path.
- Evaluation metrics for faithfulness/context relevance.
- Simple tracing helper for timing spans.

### Frontend
- Streamlit dashboard for task submission, report rendering, metrics, and tool results.

### MLOps / project operations
- Fine-tuning dataset scaffolding and JSONL export helper.
- Adapter merge placeholder script.
- Dockerfiles + Docker Compose stack.
- Render deployment manifest (`render.yaml`).
- GitHub Actions CI workflow.
- Makefile commands for run/test/ingest/evaluate/fine-tune export.

---

## Repository structure

```text
backend/
  api/routes/
  core/
  rag/
  observability/
  workers/
  finetuning/
frontend/
scripts/
docs/
.github/workflows/ci.yml
Dockerfile
Dockerfile.frontend
docker-compose.yml
render.yaml
```

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

## Example request

```bash
curl -X POST http://localhost:8000/tasks/run \
  -H "Content-Type: application/json" \
  -d '{"user_goal":"Research RAG 2.0 and remind me in two weeks"}'
```
