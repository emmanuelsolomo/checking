import datetime
import dateutil.parser
import pandas as pd
from datetime import timedelta
from .models import NsLog, O365User
from .serializers import NsLogSerializer, O365UserSerializer
import pytz



class DashBoardManager(object):
    """Log and Activity Manager """
    def __init__(self, email, ip=None):
        self.UserActivity = O365User.objects.get(email=email)
        self.timezone = pytz.timezone("Africa/Porto-Novo")
        self.now = datetime.datetime.now()
        self.logtime = self.timezone.localize(self.now)
        self.TzStrLogtime = self.logtime.strftime('%Y-%m-%dT%H:%M:%S%z')
        self.StrLogtime = self.logtime.strftime('%Y-%m-%dT%H:%M:%S')
        self.today = datetime.date.today()
        self.day = datetime.date.today()
        self.fullDay = self.day.strftime('%Y-%m-%dT%H:%M:%S')
        self.date = datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S%z')
        self.simpleDate=datetime.date.today().strftime('%Y-%m-%d')
        self.nslogs = NsLog.objects.filter(user=email,date=self.day)
        self.nbLog = len(self.nslogs)
        self.serializer = NsLogSerializer(self.nslogs, many=True)
        self.TzStart=str(self.day) + '+01:00'
        self.start=str(self.day)
        self.TzfullDayStart=str(self.fullDay) + '+01:00'
        self.end=self.serializer.data[0]['timestamp']
        self.lastLog=self.serializer.data[self.nbLog - 1]['timestamp']
        self.strLastlog=self.serializer.data[self.nbLog - 1]['timestamp']
        self.ip = ip
        self.email = email
        self.setNoActivityLogs()
        self.find_inactivy()
        self.timeShift = self.getTimeDiff()
        self.dashboardData = self.noActivityLogs +  self.dataUpdate
        self.setLogOffActivityLogs()

    def setNoActivityLogs(self):
        stamps = pd.date_range(start=self.TzfullDayStart, end=self.end,freq='0H10T')
        serie = pd.Series('timestamp', index=stamps.strftime('%Y-%m-%dT%H:%M:%S%z'))
        data = dict(zip(serie.index.format(), serie))
        self.noActivityLogs = [ dict(user=self.email,date=self.simpleDate,timestamp=timestamp,last_signin=None,ip=None,active=False)  for  timestamp, key in  data.items()]

    def setLogOffActivityLogs(self):
        endTime = datetime.datetime.strptime(self.StrLogtime, '%Y-%m-%dT%H:%M:%S')
        lastLogTime = datetime.datetime.strptime(self.strLastlog.replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')
        time_difference =  endTime - lastLogTime
        time_difference_in_minutes = time_difference / timedelta(minutes=1)
        if time_difference_in_minutes > 15:
            start=self.strLastlog
            end=self.TzStrLogtime
            stamps = pd.date_range(start=start, end=end,freq='0H10T')
            serie = pd.Series('timestamp', index=stamps.strftime('%Y-%m-%dT%H:%M:%S%z'))
            data = dict(zip(serie.index.format(), serie))
            logout_inactivity_logs = [ dict(user=self.email,date=self.simpleDate,timestamp=timestamp,last_signin=None,ip=None,active=False)  for  timestamp, key in  data.items()]
            self.dashboardData  = self.dashboardData  + logout_inactivity_logs

    def findLogOffTime(self):
        stamps = pd.date_range(start=self.TzfullDayStart, end=self.end,freq='0H10T')
        serie = pd.Series('timestamp', index=stamps.strftime('%Y-%m-%dT%H:%M:%S%z'))
        data = dict(zip(serie.index.format(), serie))
        self.noActivityLogs = [ dict(user=self.email,date=self.simpleDate,timestamp=self.date,last_signin=None,ip=None,active=False)  for  date, key in  data.items()]

    def getTimeDiff(self):
        if self.nbLog > 0:
            time_difference = self.logtime - self.nslogs[self.nbLog - 1].timestamp
            time_difference_in_minutes = time_difference / timedelta(minutes=1)
            return time_difference_in_minutes
        return 0

    def check_timedelta(self, time1, time2):  
        date_time2_obj = datetime.datetime.strptime(time2.replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')
        date_time1_obj = datetime.datetime.strptime(time1.replace("+01:00", ""), '%Y-%m-%dT%H:%M:%S')  
        time_difference =  date_time1_obj - date_time2_obj

        time_difference_in_minutes = time_difference / timedelta(minutes=1)
        shift_array = []
        if (time_difference_in_minutes > 15):    
            shift = 1
            new_row = date_time2_obj
            while shift < (time_difference_in_minutes / 5):      
                new_row = new_row + timedelta(minutes=5)
                log = dict(user=self.email,date=self.day,timestamp=new_row.strftime('%Y-%m-%dT%H:%M:%S%z'),last_signin=None,ip=None,active=False)
                shift_array.append(log)
                shift = shift + 1
        return shift_array

    def find_inactivy(self):
        current = 0
        self.dataUpdate = self.serializer.data
        while current < len(self.dataUpdate):
            if current > 0:
                shift_array = self.check_timedelta(self.dataUpdate [current]['timestamp'], self.dataUpdate [current - 1]['timestamp'])
                if (len(shift_array) > 0):
                    cpt = 0 
                    index = current
                    while(cpt < len(shift_array)):
                        self.dataUpdate.insert(index, shift_array[cpt])
                        cpt = cpt + 1
                        index = index + 1          
            current += 1
