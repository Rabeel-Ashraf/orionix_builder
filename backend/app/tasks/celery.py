from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "orionix_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks.tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
)

# Optional: Configure beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    'refill-free-credits-twice-monthly': {
        'task': 'app.tasks.tasks.refill_free_credits',
        'schedule': 15 * 24 * 60 * 60,  # 15 days in seconds (approx 2x per month)
    },
    'cleanup-temp-files': {
        'task': 'app.tasks.tasks.cleanup_temp_files',
        'schedule': 24 * 60 * 60,  # Daily
    },
}
