from fastapi import FastAPI

from backend.api.routes.health import router as health_router
from backend.api.routes.metrics import router as metrics_router
from backend.api.routes.tasks import router as tasks_router
from backend.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(metrics_router)


@app.get("/")
def index() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "docs": "/docs",
    }
