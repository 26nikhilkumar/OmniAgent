from backend.core.mcp_client import MCPClient
from backend.core.state import AgentState, PlanStep
from backend.core.tools import run_python_calculation, schedule_reminder, search_web

mcp = MCPClient()
mcp.register("search_web", search_web)
mcp.register("schedule_reminder", schedule_reminder)
mcp.register("python_calc", run_python_calculation)


def planner_node(state: AgentState) -> AgentState:
    goal = state["user_goal"].strip()
    plan: list[PlanStep] = [
        {"agent": "researcher", "instruction": f"Gather external context for: {goal}"},
        {"agent": "analyst", "instruction": "Evaluate retrieved context and extract key claims."},
        {"agent": "writer", "instruction": "Compose concise markdown report with next actions."},
    ]
    if "remind" in goal.lower() or "reminder" in goal.lower() or "follow up" in goal.lower():
        plan.append({"agent": "scheduler", "instruction": "Schedule reminder in 14 days."})

    state["plan"] = plan
    state["current_step"] = 0
    state["tool_results"] = []
    state["errors"] = []
    state["metadata"] = {"planner": "deterministic"}
    return state


def researcher_node(state: AgentState) -> AgentState:
    instruction = state["plan"][state["current_step"]]["instruction"]
    results = mcp.call("search_web", query=instruction)
    state["tool_results"].append({"research": results})
    state["retrieved_context"] = [r["snippet"] for r in results]
    state["current_step"] += 1
    return state


def analyst_node(state: AgentState) -> AgentState:
    context = state.get("retrieved_context", [])
    token_count = sum(len(c.split()) for c in context)
    calc = mcp.call("python_calc", expression=f"{token_count}/10")
    state["analysis"] = (
        f"Found {len(context)} context item(s). "
        f"Approx complexity score: {calc.get('result', calc.get('error', 'n/a'))}."
    )
    state["tool_results"].append({"analysis": state["analysis"]})
    state["current_step"] += 1
    return state


def writer_node(state: AgentState) -> AgentState:
    context = "\n".join(state.get("retrieved_context", [])) or "No context available."
    analysis = state.get("analysis", "No analysis generated.")
    state["final_report"] = (
        "# OmniAgent Report\n\n"
        f"## Goal\n{state['user_goal']}\n\n"
        f"## Analysis\n{analysis}\n\n"
        f"## Evidence\n{context}\n\n"
        "## Recommended Next Steps\n"
        "1. Validate claims with live provider data.\n"
        "2. Add domain-specific tools and retries."
    )
    state["current_step"] += 1
    return state


def scheduler_node(state: AgentState) -> AgentState:
    result = mcp.call("schedule_reminder", event=state["user_goal"], days_from_now=14)
    state["tool_results"].append({"scheduler": result})
    state["current_step"] += 1
    return state
