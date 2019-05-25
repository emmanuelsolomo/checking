from .models import NsLog, O365User
from .serializers import NsLogSerializer, O365UserSerializer
from checking.celery import app
import datetime
import pandas as pd
from datetime import timedelta
from django.utils import timezone


@app.task(bind=True)
def debug_task(self):
    print('Hello World *** Request: {0!r}'.format(self.request))


@app.task(bind=True)
def add(self):
    f = open("/tmp/task_add.txt", "a")
    print("Hello stackoverflow!", file=f)
    print("I have a question.", file=f)
    print('New Add *** Request: {0!r}'.format(self.request))

    
@app.task(bind=True)
def update_user_list(self):
    nslogs = NsLog.objects.all()
    serializer = NsLogSerializer(nslogs, many=True)
    activity = O365User.objects.all()
    ActivitySerializer = O365UserSerializer(activity, many=True)
    f = open("/tmp/user_list.txt", "a")
    for user in  ActivitySerializer.data:
        print(user, file=f)
        print("*****************", file=f)
        UserActivity = O365User.objects.get(email=user['email'])
        localUser = NsLog.objects.filter(user=user['email'])
        localSerializer = NsLogSerializer(localUser, many=True)
        if len(localSerializer.data) > 0:
            print(localSerializer.data[1]['timestamp'], file=f)
            log_time = datetime.datetime.now(timezone.utc)
            logtime = log_time.strftime('%Y-%m-%dT%H:%M')
            last_timestamp =  localUser[0].timestamp
            time_difference = log_time - last_timestamp
            last_seen = time_difference / timedelta(minutes=1)
            if last_seen < 60 and last_seen > 20:
                print("Last seen : a few minutes ago", file=f)
                print("Setting status to offline", file=f)
                UserActivity.active = False
                UserActivity.last_seen = str(round(last_seen)) + " minutes ago"
                UserActivity.save()
            if last_seen > 60 and last_seen/60 < 24:
                print("Last seen :  a few hours ago", file=f)
                print("Setting status to offline", file=f)
                UserActivity.active = False
                UserActivity.last_seen = str(round(last_seen/60)) + " hours ago"
                UserActivity.save()
            if last_seen > 60 and last_seen/60 > 24:
                print("Last seen : more than a day", file=f)
                print("Setting status to offline", file=f)
                UserActivity.active = False
                UserActivity.last_seen = "More than a days ago"
                UserActivity.save()
        else:
            print("No logs found for user  with email : " + user['email'], file=f)
            UserActivity.active = False
            UserActivity.last_seen = "A long time ago"            
            print("###################", file=f)
            UserActivity.save()

    f.close()