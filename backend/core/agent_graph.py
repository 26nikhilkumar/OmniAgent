from backend.core.agents import analyst_node, planner_node, researcher_node, scheduler_node, writer_node
from backend.core.state import AgentState


class OmniAgentGraph:
    """Deterministic graph runner with step routing.

    Designed to mirror a LangGraph state machine; easy to swap with real LangGraph.
    """

    def invoke(self, state: AgentState) -> AgentState:
        state = planner_node(state)

        while state["current_step"] < len(state["plan"]):
            agent = state["plan"][state["current_step"]]["agent"]
            if agent == "researcher":
                state = researcher_node(state)
            elif agent == "analyst":
                state = analyst_node(state)
            elif agent == "writer":
                state = writer_node(state)
            elif agent == "scheduler":
                state = scheduler_node(state)
            else:
                state.setdefault("errors", []).append(f"Unknown agent: {agent}")
                state["current_step"] += 1

        return state


agent_graph = OmniAgentGraph()
