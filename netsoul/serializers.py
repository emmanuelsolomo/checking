from rest_framework import serializers
from netsoul.models import NsLog, O365User
import datetime


class O365UserSerializer(serializers.Serializer):    
    class Meta:
        model = O365User
        fields = ('email')

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

