# backend/tasks/__init__.py
from celery import Celery
from datetime import date
from backend.db import SessionLocal
from backend.db_models import TaskManager, TaskLogger

celery = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

@celery.task
def transfer_active_tasks():
    """
    Logs all 'active' tasks from TaskManager into TaskLogger once per day.
    Prevents duplicate entries by checking if a task was already logged today.
    """
    session = SessionLocal()
    today = date.today()

    active_tasks = session.query(TaskManager).filter(TaskManager.status == "active").all()

    for task in active_tasks:
        already_logged = session.query(TaskLogger).filter(
            TaskLogger.task_id == task.id,
            TaskLogger.changed_at.cast(date) == today
        ).first()

        if not already_logged:
            log = TaskLogger(
                task_id=task.id,
                old_status="active",
                new_status="active",
                changed_by="system"
            )
            session.add(log)

    session.commit()
    session.close()
