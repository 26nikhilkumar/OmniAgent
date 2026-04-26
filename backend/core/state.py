from typing import Any, Literal, TypedDict

AgentName = Literal["planner", "researcher", "analyst", "writer", "scheduler"]


class PlanStep(TypedDict):
    agent: AgentName
    instruction: str


class AgentState(TypedDict, total=False):
    user_goal: str
    plan: list[PlanStep]
    current_step: int
    retrieved_context: list[str]
    analysis: str
    final_report: str
    tool_results: list[dict[str, Any]]
    errors: list[str]
    metadata: dict[str, Any]
