from datetime import datetime, timedelta, timezone


def search_web(query: str) -> list[dict[str, str]]:
    return [
        {
            "title": f"Result for: {query}",
            "url": "https://example.com/search",
            "snippet": "Placeholder result. Integrate Tavily/SerpAPI/MCP server for live data.",
        }
    ]


def run_python_calculation(expression: str) -> dict[str, str]:
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expression).issubset(allowed_chars):
        return {"error": "Unsafe expression"}
    try:
        return {"result": str(eval(expression, {"__builtins__": {}}, {}))}
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


def schedule_reminder(event: str, days_from_now: int = 14) -> dict[str, str]:
    reminder_time = datetime.now(timezone.utc) + timedelta(days=days_from_now)
    return {
        "event": event,
        "scheduled_for": reminder_time.isoformat(),
        "status": "scheduled",
    }
