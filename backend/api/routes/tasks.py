from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.agent_graph import agent_graph
from backend.observability.evaluator import evaluate_response

router = APIRouter(prefix="/tasks", tags=["tasks"])
_TASKS: dict[str, dict] = {}


class TaskRequest(BaseModel):
    user_goal: str


def _run(user_goal: str, thread_id: str) -> dict:
    state = agent_graph.invoke({"user_goal": user_goal}, thread_id=thread_id)
    metrics = evaluate_response(
        query=user_goal,
        context=state.get("retrieved_context", []),
        answer=state.get("final_report", ""),
    )
    return {"result": state, "metrics": metrics, "thread_id": thread_id}


@router.post("/run")
def run_task(payload: TaskRequest) -> dict:
    return _run(payload.user_goal, thread_id=str(uuid4()))


@router.post("/submit")
def submit_task(payload: TaskRequest) -> dict:
    task_id = str(uuid4())
    _TASKS[task_id] = {"status": "running", "logs": ["task received", "planning", "executing"]}
    _TASKS[task_id] = {"status": "completed", **_run(payload.user_goal, thread_id=task_id), "logs": ["completed"]}
    return {"task_id": task_id, "status": _TASKS[task_id]["status"]}


@router.get("/{task_id}")
def get_task(task_id: str) -> dict:
    task = _TASKS.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    return task
