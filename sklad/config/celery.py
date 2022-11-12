from celery import Celery
from celery.schedules import crontab

app = Celery('sklad')
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-documents-status': {
        'task': 'app.document.tasks.task2.check_document_status',
        'schedule': crontab(**app.conf.get('CRON_TIME')),
    },
}
