import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "unblock-pages-every-day": {
        "task": "pages.tasks.unblock_pages",
        "schedule": crontab(minute="*/5"),  # Runs every 5 minutes
    },
}
