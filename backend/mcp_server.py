from backend.core.tools import run_python_calculation, schedule_reminder, search_web


class OmniMCPServer:
    """Minimal MCP-like tool registry server for local development."""

    def list_tools(self) -> list[dict]:
        return [
            {"name": "search_web", "description": "Search public web content"},
            {"name": "schedule_reminder", "description": "Schedule follow up reminder"},
            {"name": "python_calc", "description": "Run safe arithmetic expression"},
        ]

    def call_tool(self, name: str, arguments: dict):
        if name == "search_web":
            return search_web(arguments.get("query", ""))
        if name == "schedule_reminder":
            return schedule_reminder(arguments.get("event", ""), arguments.get("days_from_now", 14))
        if name == "python_calc":
            return run_python_calculation(arguments.get("expression", "0"))
        raise ValueError(f"Unknown tool: {name}")
