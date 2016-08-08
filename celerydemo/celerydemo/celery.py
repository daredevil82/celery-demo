from __future__ import absolute_import
import os

from celery import Celery
from django.conf import settings
from celerydemo.settings import CELERY_BROKER, CELERY_BACKEND

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celerydemo.settings')
app = Celery('celerydemo', backend=CELERY_BACKEND, broker=CELERY_BROKER, include=['app.tasks.task_functions',
                                                                                  'app.tasks.task_classes'])
app.config_from_object('django.conf:settings')
app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
