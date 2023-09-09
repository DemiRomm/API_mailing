import os

from celery import Celery
from celery.schedules import crontab

# from ..notifications.tasks import mailing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NotificationServiceApi.settings')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notificationserviceapi.settings')
app = Celery('NotificationServiceApi')
# app = Celery('notificationserviceapi')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {'mailing-every-12-hours': {'task': 'notifications.tasks.mailing_start',
                                                  'schedule': crontab(hour='*/12'), }, }

# @app.task()
# def test_task():
#     print('Test 1 OK')
