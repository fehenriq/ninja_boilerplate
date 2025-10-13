import os
import platform

from celery import Celery
from django.conf import settings

import core.celery_signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings", namespace="CELERY")
if settings.CELERY_BROKER_URL.startswith("rediss://"):
    app.conf.broker_use_ssl = settings.CELERY_BROKER_USE_SSL
app.autodiscover_tasks()

if platform.system() == "Windows":
    app.conf.worker_pool = "solo"
