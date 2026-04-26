from backend.core.agent_graph import agent_graph
from backend.workers.celery_app import celery_app


@celery_app.task(name="run_omni_task")
def run_omni_task(user_goal: str) -> dict:
    return agent_graph.invoke({"user_goal": user_goal})
