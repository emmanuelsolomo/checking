from rest_framework import serializers
from netsoul.models import NsLog, O365User
import datetime


class O365UserSerializer(serializers.Serializer):
    userType = serializers.CharField(required=True)
    avatar = serializers.ImageField(required=True)
    name = serializers.CharField(required=True)
    group = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    country = serializers.CharField(required=True)
    flag = serializers.CharField(required=True)
    promotion = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    active = serializers.BooleanField(required=True)   
    last_activity = serializers.DateTimeField(required=False)  
    last_seen = serializers.DateTimeField(required=False)   

    class Meta:
        model = O365User
        fields = ('name', 'group', 'avatar','email', 'country', 'flag', 'promotion', 'location', 'active', 'userType',  'last_activity', 'last_seen')

    def create(self, validated_data):
        """
        Create and return a new `O365User` instance, given the validated data.
        """
        return O365User.objects.create(**validated_data)

class NsLogSerializer(serializers.Serializer):    
    user = serializers.EmailField(required=True)
    date = serializers.DateField(default=datetime.date.today())
    timestamp = serializers.DateTimeField(required=True)
    last_signin = serializers.DateTimeField(required=False)
    ip = serializers.CharField(required=False)
    active = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `O365User` instance, given the validated data.
        """
        return NsLog.objects.create(**validated_data)

    class Meta:
        model = NsLog
        fields = ('user', 'last_signin', 'timestamp', 'last_logoff')




