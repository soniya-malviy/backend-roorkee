from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'load-scheme-data-every-day': {  
        'task': 'myapp.tasks.load_schemes', 
        'schedule': crontab(hour=0, minute=0), 
    },
}

app.conf.timezone = 'UTC'

