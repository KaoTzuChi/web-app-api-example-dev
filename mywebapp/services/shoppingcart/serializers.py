from rest_framework import serializers
from datetime import date, time, datetime, tzinfo
import datetime
from . import models

class shoppingcartSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    memberid = serializers.CharField(required=False)
    orderid = serializers.CharField(required=False)
    productid = serializers.CharField(required=False)
    productname = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default=0.00)
    discount = serializers.DecimalField(max_digits= 4, decimal_places=2, required=False, default=0.00)
    count = serializers.IntegerField(required=False,default=0)
    lastupdate = serializers.DateTimeField(required=False,default=datetime.datetime.now())  

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.memberid = attrs.get('memberid', instance.memberid)
            instance.orderid = attrs.get('orderid', instance.orderid)
            instance.productid = attrs.get('productid', instance.productid)
            instance.productname = attrs.get('productname', instance.productname)
            instance.price = attrs.get('price', instance.price)
            instance.discount = attrs.get('discount', instance.discount)
            instance.count = attrs.get('count', instance.count)
            instance.lastupdate = attrs.get('lastupdate', instance.lastupdate)
            return instance
        return models.shoppingcartModel(attrs.get('objectid'), attrs.get('memberid'), attrs.get('orderid')
        , attrs.get('productid'), attrs.get('productname'), attrs.get('price')
        , attrs.get('discount'), attrs.get('count'), attrs.get('lastupdate'))
