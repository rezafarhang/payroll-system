from __future__ import absolute_import, unicode_literals
import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('payroll', broker='redis://redis:6379/0', include=['payrollsystem.payroll.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'calculate_weekly_incomes': {
        'task': 'payroll.tasks.calculate_weekly_incomes',
        'schedule': crontab(minute=1),
    }
}
