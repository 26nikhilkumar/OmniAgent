from contextlib import contextmanager
from time import perf_counter


@contextmanager
def trace_span(name: str):
    start = perf_counter()
    yield
    elapsed_ms = (perf_counter() - start) * 1000
    # Replace with LangSmith / OpenTelemetry exporters in production.
    print(f"[trace] span={name} elapsed_ms={elapsed_ms:.2f}")
