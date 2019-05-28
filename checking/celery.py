from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import datetime
import pandas as pd
from datetime import timedelta
#from .load_env import load_env

#load_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checking.settings')

app = Celery('checking')
app.config_from_object('django.conf:settings', namespace='CELERY')
#app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
app.conf.timezone = 'UTC'

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


app.conf.beat_schedule = {
    'add-every-15-seconds': {
        'task': 'netsoul.tasks.update_user_list',
        'schedule': 15.0
    },
}



