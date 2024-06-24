# myapp/tasks.py

from celery import shared_task
from django.core.management import call_command

@shared_task
def load_schemes():
    call_command('load_schemes_from_json')
