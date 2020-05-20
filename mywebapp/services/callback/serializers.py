from rest_framework import serializers
from datetime import date, time, datetime, tzinfo
import datetime
from . import models

class callbackSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    sender = serializers.CharField(required=False)
    data = serializers.DictField(serializers.CharField(required=False, default=''))
    statuscode = serializers.IntegerField(required=False,default=0)  
    lastupdate = serializers.DateTimeField(required=False,default=datetime.datetime.now())  

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.sender = attrs.get('sender', instance.sender)
            instance.data = attrs.get('data', instance.data)
            instance.statuscode = attrs.get('statuscode', instance.statuscode)
            instance.lastupdate = attrs.get('lastupdate', instance.lastupdate)

            return instance
        return models.callbackModel(attrs.get('objectid'), attrs.get('sender'), attrs.get('data')
        , attrs.get('statuscode'), attrs.get('lastupdate') )
