import datetime
import dateutil.parser
import pandas as pd
import pendulum
from datetime import timedelta
from .models import NsLog, O365User
from .serializers import NsLogSerializer, O365UserSerializer
from .dashboard import DashBoardManager
import pytz

class ControlManager(object):
    def __init__(self, email, ip=None):
        self.email = email
        self.UserActivity = O365User.objects.get(email=email)
        self.timezone = pytz.timezone("Africa/Porto-Novo")
        self.dshLogs = DashBoardManager(email, ip)
        self.dshLogs.dashboardData


    def getDailyLogs(self, day):
        today = datetime.date.today()
        activityArray = []
        data = NsLog.objects.filter(user=self.email,date=day)
        self.nslogs = NsLogSerializer(data, many=True)
        #for log in self.dshLogs.dashboardData:
        for log in self.nslogs.data:
            if log['active'] == True:
                activityArray.append(log)
        prev = 0
        duration = timedelta(minutes=0)
        for log in activityArray:
            if prev == 0:
                last_timestamp = log['timestamp']
                prev = 1
            else:
                timestamp = datetime.datetime.strptime(str(log['timestamp']).replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')
                prev_timestamp = datetime.datetime.strptime(last_timestamp.replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')  
                timeDiff =  timestamp - prev_timestamp
                if timeDiff < timedelta(minutes=8):
                    duration = duration + timeDiff
                last_timestamp = log['timestamp']
        return duration
            
    def getWeeklyLogs(self, day):
        dt = pendulum.from_format(day, 'YYYY-MM-DD')
        #today = pendulum.now()
        start = dt.start_of('week')
        end = dt.end_of('week')
        #date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
        date_generated = [start + datetime.timedelta(days=x) for x in range(0, 7)]
        self.weekly_logs = []
        for date in date_generated:
            #duration = self.getDailyLogs(date.strftime("%Y-%m-%d"))
            duration = self.getDailyLogs(date.strftime("%Y-%m-%d"))
            self.weekly_logs.append(str(duration.total_seconds()))
            #self.weekly_logs.append(dict(duration=str(duration), date=date.date()))

    def getMontlyLogs(self):
         print("In DailyLogs")