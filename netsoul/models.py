from django.db import models
from django.utils import timezone
import datetime


# Create your models here.



class O365User(models.Model):
    STAFF = 'Staff'
    STUDENT = 'Student'
    USER_TYPE = [
        ('STAFF', 'Staff'),
        ('STUDENT', 'Student'),
        ('AER', 'Assitant education'),
        ('APE', 'Assitant Pedagogique'),
        ('ADM', 'Administration'),
        ]
    userType = models.CharField(
        max_length=50,
        choices=USER_TYPE,
        default=STUDENT,
    )
    avatar = models.ImageField(upload_to = 'img/avatars', default = 'img/avatars/1.jpg')
    name = models.CharField(max_length=70,blank=True)
    email = models.EmailField(max_length=70,blank=True)
    country = models.CharField(max_length=70,blank=False,default='BENIN')
    promotion = models.CharField(max_length=70,blank=False,default='2023')
    location = models.CharField(max_length=70,blank=False,default='Seme City')
    flag = models.CharField(max_length=70,blank=False,default='bj')
    active = models.BooleanField(blank=False, null=False,default=False)    
    last_activity = models.DateTimeField(blank=True, null=True) 
    last_seen = models.CharField(max_length=70,blank=True,default="Never been online")    


    class Meta:
        ordering = ('name', 'avatar','email', 'country', 'promotion', 'location','active', 'userType', 'last_activity')

def __str__(self):
    return self.name

class NsLog(models.Model):
    user = models.EmailField(max_length=70,blank=False) #models.ForeignKey(O365User, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    last_signin = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.datetime.now, blank=False)
    last_logoff = models.DateTimeField(blank=True, null=True)
    ip = models.CharField(max_length=70, blank=False)
    active = models.BooleanField(default=True, blank=False)

    class Meta:
        ordering = ('user', 'date', 'timestamp', 'active')

def __str__(self):
    return self.user + " " + self.last_signin
