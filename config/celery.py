import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-documents-status-every-day (18.00)': {
        'task': 'app.document.tasks.task2.check_document_status',
        'schedule': crontab(),
    },
}