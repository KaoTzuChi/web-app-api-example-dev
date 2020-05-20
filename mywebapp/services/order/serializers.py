from rest_framework import serializers
from datetime import date, time, datetime, tzinfo
import datetime
from . import models

class orderSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    memberid = serializers.CharField(required=False)
    totalprice = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default=0.00)
    totaldiscount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default=0.00)
    payment = serializers.CharField(required=False)
    status = serializers.IntegerField(required=False,default=0)  
    lastupdate = serializers.DateTimeField(required=False,default=datetime.datetime.now())  

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.memberid = attrs.get('memberid', instance.memberid)
            instance.totalprice = attrs.get('totalprice', instance.totalprice)
            instance.totaldiscount = attrs.get('totaldiscount', instance.totaldiscount)
            instance.payment = attrs.get('payment', instance.payment)
            instance.status = attrs.get('status', instance.status)
            instance.lastupdate = attrs.get('lastupdate', instance.lastupdate)
            return instance
        return models.orderModel(attrs.get('objectid'), attrs.get('memberid'), attrs.get('totalprice')
        , attrs.get('totaldiscount'), attrs.get('payment'), attrs.get('status'), attrs.get('lastupdate'))

