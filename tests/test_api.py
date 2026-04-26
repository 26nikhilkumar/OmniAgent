from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_run_task():
    response = client.post("/tasks/run", json={"user_goal": "Research RAG"})
    assert response.status_code == 200
    body = response.json()
    assert "result" in body
    assert "metrics" in body


def test_submit_and_get_task():
    submit = client.post("/tasks/submit", json={"user_goal": "Research agents"})
    assert submit.status_code == 200
    task_id = submit.json()["task_id"]

    fetch = client.get(f"/tasks/{task_id}")
    assert fetch.status_code == 200
    assert fetch.json()["status"] == "completed"


def test_rag_metrics_endpoint():
    response = client.get("/metrics/rag")
    assert response.status_code == 200
    assert "latency_ms" in response.json()
