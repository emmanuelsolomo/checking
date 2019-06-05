import datetime
import dateutil.parser
import pandas as pd
from datetime import timedelta
from .models import NsLog, O365User
from .serializers import NsLogSerializer, O365UserSerializer
import pytz



class LogManager(object):
    """Log and Activity Manager """
    def __init__(self, email, ip=None):
        self.UserActivity = O365User.objects.get(email=email)
        self.timezone = pytz.timezone("Africa/Porto-Novo")
        self.today = datetime.date.today()
        self.now = datetime.datetime.now()
        self.nslogs = NsLog.objects.filter(user=email,date=self.today)
        self.nbLog = len(self.nslogs)
        self.logtime = self.timezone.localize(self.now)
        self.TzStrLogtime = self.logtime.strftime('%Y-%m-%dT%H:%M:%S%z')
        self.StrLogtime = self.logtime.strftime('%Y-%m-%dT%H:%M:%S')
        self.timeShift = self.getTimeDiff()
        self.email = email
        self.ip = ip

    def updateActivity(self, last_signin=None):
        self.UserActivity.active = True
        self.UserActivity.last_activity = self.logtime
        self.UserActivity.last_seen = str(round(self.timeShift)) + " minutes ago"
        if self.ip == "137.255.10.29" or self.ip == "41.85.161.132":
            self.UserActivity.location = "[EPITECHxSemeCity]"
        elif self.ip == "137.255.8.213":
            self.UserActivity.location = "[EPITECHxSemeCity]"
        else:
            self.UserActivity.location = "[SomewherexWorld]"
        self.UserActivity.save()

    def updateNsLog(self,last_signin='None', originWeb=True):
        data = dict(user=self.email,timestamp=self.TzStrLogtime, ip=self.ip,active=True)
        print(data)
        print(self.timeShift)
        serializer = NsLogSerializer(data=data)
        if serializer.is_valid() and self.timeShift >= 5 and originWeb:
            serializer.save()
        elif serializer.is_valid() and not originWeb :
            serializer.save()   
        elif serializer.is_valid():
            print("Need more conditions to save logs")

    def getTimeDiff(self):
        if self.nbLog > 0:
            time_difference = self.logtime - self.nslogs[self.nbLog - 1].timestamp
            time_difference_in_minutes = time_difference / timedelta(minutes=1)
            return time_difference_in_minutes
        return 0

