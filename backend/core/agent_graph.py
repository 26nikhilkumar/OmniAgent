from typing import Literal

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from backend.core.agents import analyst_node, planner_node, researcher_node, scheduler_node, writer_node
from backend.core.state import AgentState


def router(state: AgentState) -> Literal["researcher", "analyst", "writer", "scheduler", "end"]:
    plan = state.get("plan", [])
    step = state.get("current_step", 0)
    if step >= len(plan):
        return "end"
    agent = plan[step]["agent"]
    if agent in {"researcher", "analyst", "writer", "scheduler"}:
        return agent
    state.setdefault("errors", []).append(f"Unknown agent: {agent}")
    state["current_step"] = step + 1
    return router(state)


class OmniAgentGraph:
    def __init__(self) -> None:
        workflow = StateGraph(AgentState)
        workflow.add_node("planner", planner_node)
        workflow.add_node("researcher", researcher_node)
        workflow.add_node("analyst", analyst_node)
        workflow.add_node("writer", writer_node)
        workflow.add_node("scheduler", scheduler_node)

        workflow.set_entry_point("planner")
        workflow.add_conditional_edges(
            "planner",
            router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "scheduler": "scheduler",
                "end": END,
            },
        )
        workflow.add_conditional_edges(
            "researcher",
            router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "scheduler": "scheduler",
                "end": END,
            },
        )
        workflow.add_conditional_edges(
            "analyst",
            router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "scheduler": "scheduler",
                "end": END,
            },
        )
        workflow.add_conditional_edges(
            "writer",
            router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "scheduler": "scheduler",
                "end": END,
            },
        )
        workflow.add_conditional_edges(
            "scheduler",
            router,
            {
                "researcher": "researcher",
                "analyst": "analyst",
                "writer": "writer",
                "scheduler": "scheduler",
                "end": END,
            },
        )

        self.app = workflow.compile(checkpointer=MemorySaver())

    def invoke(self, state: AgentState, thread_id: str = "default") -> AgentState:
        config = {"configurable": {"thread_id": thread_id}}
        return self.app.invoke(state, config=config)

    def mermaid(self) -> str:
        return """
flowchart TD
    planner --> researcher
    planner --> analyst
    planner --> writer
    planner --> scheduler
    researcher --> analyst
    analyst --> writer
    writer --> scheduler
    scheduler --> END
""".strip()


agent_graph = OmniAgentGraph()
