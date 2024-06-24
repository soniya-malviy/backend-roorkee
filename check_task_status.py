import os
import django
from celery.result import AsyncResult


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


task_id = 'fb798dfc-3c03-4d5d-9927-e1d0949bed60'
result = AsyncResult(task_id)

print("Task Status:", result.status) 
print("Task Result:", result.result)
