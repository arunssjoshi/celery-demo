from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celerydemoapp.settings")

# Create the Celery app instance
app = Celery("my_celery_app_for_celerydemoapp")

# Load task modules from all registered Django apps.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["celerydemoapp.mytasks"])


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
