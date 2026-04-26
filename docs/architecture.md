# OmniAgent Architecture

## Runtime flow
1. User submits task via Streamlit or API.
2. FastAPI route invokes orchestrator.
3. Planner builds step plan.
4. Researcher calls MCP-dispatched tools.
5. Analyst computes derived insights.
6. Writer synthesizes final report.
7. Scheduler optionally sets follow-up reminder.
8. Evaluator computes quality metrics.

## Components
- `backend/core`: orchestration, agent state, MCP client, tools
- `backend/rag`: ingestion, hybrid retrieval, graph rag, vector store
- `backend/observability`: evaluator and tracing helpers
- `backend/workers`: Celery worker glue
- `frontend`: Streamlit dashboard
