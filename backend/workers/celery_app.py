from celery import Celery

from backend.config import get_settings

settings = get_settings()
celery_app = Celery("omniagent", broker=settings.redis_url, backend=settings.redis_url)
