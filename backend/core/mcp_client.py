from typing import Any


class MCPClient:
    """Lightweight MCP-like dispatcher.

    This is intentionally local and deterministic for offline development.
    Replace with a real MCP SDK client for production.
    """

    def __init__(self) -> None:
        self.tools: dict[str, Any] = {}

    def register(self, name: str, tool_fn: Any) -> None:
        self.tools[name] = tool_fn

    def call(self, name: str, **kwargs: Any) -> Any:
        if name not in self.tools:
            raise ValueError(f"Unknown MCP tool: {name}")
        return self.tools[name](**kwargs)
