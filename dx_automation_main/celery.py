import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dx_automation_main.settings')

app = Celery('dx_automation_main') # Initialize Celery with the name of the main django project

# - namespace='CELERY' means all celery-related configuration keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True) #ignore_result=True means we don't store task results in result backend
def debug_task(self):
    print(f'Request: {self.request!r}')