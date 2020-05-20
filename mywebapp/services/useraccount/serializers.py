from rest_framework import serializers
from datetime import date, time, datetime, tzinfo
import datetime
from . import models

class accountSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    #email = EmailField(max_length=None, min_length=None, allow_blank=True)
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')
    last_login = serializers.DateTimeField(required=False,default=datetime.datetime.now())  
    date_joined = serializers.DateTimeField(required=False,default=datetime.datetime.now())  
    #token_issued = serializers.DateTimeField(required=False,default=datetime.datetime.now())  
    #groups = serializers.ListField(serializers.CharField(required=False, default=''))
    #user_permissions = serializers.ListField(serializers.CharField(required=False, default=''))
    #is_authenticated = serializers.BooleanField(default=False)
    is_staff = serializers.BooleanField(required=False)
    is_superuser = serializers.BooleanField(required=False)    
    is_active = serializers.BooleanField(required=False)
    auth_token = serializers.CharField(required=False)

    def create(self, attrs, instance=None):
        if instance:
            instance.username = attrs.get('username', instance.username)
            instance.password = attrs.get('password', instance.password)
            instance.email = attrs.get('email', instance.email)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            instance.last_login = attrs.get('last_login', instance.last_login)
            instance.date_joined = attrs.get('date_joined', instance.date_joined)
            #instance.token_issued = attrs.get('token_issued', instance.token_issued)
            instance.is_staff = attrs.get('is_staff', instance.is_staff)
            instance.is_superuser = attrs.get('is_superuser', instance.is_superuser)
            instance.is_active = attrs.get('is_active', instance.is_active)
            instance.auth_token = attrs.get('auth_token', instance.auth_token)
            return instance
        return models.accountModel(attrs.get('username'), attrs.get('password'), attrs.get('email')
        , attrs.get('first_name'), attrs.get('last_name'), attrs.get('last_login'), attrs.get('date_joined')
        , attrs.get('is_staff'), attrs.get('is_superuser'), attrs.get('is_active'), attrs.get('auth_token') )
