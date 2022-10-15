import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_jobs.settings')

app = Celery('python_jobs')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()