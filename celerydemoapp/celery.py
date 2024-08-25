from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celerydemoapp.settings")

# Create the Celery app instance
app = Celery("my_celery_app_for_celerydemoapp")

# Load task modules from all registered Django apps.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "task-every-10-seconds": {
        "task": "celerydemoapp.tasks.my_periodic_task",
        "schedule": timedelta(seconds=10),  # Run every 20 seconds
        "args": (),  # Arguments to pass to the task, if any
    },
    "send-daily-report-every-morning": {
        "task": "celerydemoapp.tasks.send_daily_report",
        "schedule": crontab(hour=7, minute=0),
        "args": (),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
