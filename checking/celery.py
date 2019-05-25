from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checking.settings')

app = Celery('checking')
app.config_from_object('django.conf:settings', namespace='CELERY')
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


@app.task(bind=True)
def debug_task(self):
    print('Hello World *** Request: {0!r}'.format(self.request))

@app.task(bind=True)
def update_users_list(self):
    print('Hello World Add *** Request: {0!r}'.format(self.request))


@app.task(bind=True)
def add(self):
    print('New Add *** Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'add-every-5-seconds': {
        'task': 'tasks.add',
        'schedule': 5.0,
        'args': (16, 16)
    },
    'add-every-15-seconds': {
        'task': 'tasks.update_users_list',
        'schedule': 15.0,
        'args': (16, 16)
    },
}


@app.task(bind=True)
def update_user_list(self):
    
