import os

# from django.conf import settings

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypizza.settings')

app = Celery('mypizza')

app.config_from_object('django.conf:settings', namespace="CELERY")
# app.config_from_object('django.conf:settings')

# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()  # вариант команды из habr.com
