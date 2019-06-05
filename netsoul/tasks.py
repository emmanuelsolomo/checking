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
        UserActivity = O365User.objects.get(email=user['email'])
        localUser = NsLog.objects.filter(user=user['email'])
        localSerializer = NsLogSerializer(localUser, many=True)
        if len(localSerializer.data) > 0:
            log_time = datetime.datetime.now(timezone.utc)
            logtime = log_time.strftime('%Y-%m-%dT%H:%M')
            timestamp_index = len(localUser) - 1
            last_timestamp =  localUser[timestamp_index].timestamp
            time_difference = log_time - last_timestamp
            last_seen = time_difference / timedelta(minutes=1)
            last_seen_in_hours = last_seen/60
            if last_seen < 60 and last_seen > 5:
                UserActivity.active = False
                UserActivity.last_seen = str(round(last_seen)) + " minutes ago"
                UserActivity.location = "N/A"                                            
            if last_seen > 60 and last_seen/60 < 24:
                UserActivity.active = False
                UserActivity.last_seen = str(round(last_seen/60)) + " hours ago"
                UserActivity.location = "N/A"                                            
            if last_seen/60 > 24:
                last_seen_in_days = round((last_seen/60)/24)
                UserActivity.location = "N/A"                            
                if last_seen_in_days > 1:
                    UserActivity.last_seen = str(last_seen_in_days) + "days ago"
                else:
                    UserActivity.last_seen = "More than a day ago"
            UserActivity.save()
        else:
            print("No logs found for user  with email : " + user['email'], file=f)
            UserActivity.active = False
            UserActivity.last_seen = "A long time ago"
            UserActivity.location = "N/A"            
            print("###################", file=f)
            UserActivity.save()

    f.close()
