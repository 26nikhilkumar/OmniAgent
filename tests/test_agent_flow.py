from backend.core.agent_graph import agent_graph


def test_agent_graph_generates_report_and_analysis():
    state = agent_graph.invoke({"user_goal": "Research hybrid rag and remind me"})
    assert "final_report" in state
    assert "analysis" in state
    assert state["final_report"].startswith("# OmniAgent Report")
    assert len(state.get("tool_results", [])) >= 3
