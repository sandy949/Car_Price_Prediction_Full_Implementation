from celery import Celery

# Create a Celery app instance with Redis as broker and backend.
celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Update Celery configuration to use UTC timezone.
celery.conf.update(
    timezone='UTC',
    enable_utc=True
)

# Define periodic task schedule using Celery Beat.
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'transfer-daily-active-tasks': {
        'task': 'backend.task_sync.transfer_active_tasks',  # Module path to your task
        'schedule': crontab(hour=0, minute=0),  # Run daily at midnight UTC
    },
}