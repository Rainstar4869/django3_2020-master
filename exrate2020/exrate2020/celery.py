from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exrate2020.settings')

app = Celery('exrate2020', broker='amqp://celery:password123@rabbitmq:5672/my_vhost',
             backend='amqp://celery:password123@rabbitmq:5672/my_vhost')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
