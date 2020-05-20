from rest_framework import serializers
from datetime import date, time, datetime, tzinfo
import datetime
from . import models

class productSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    brief = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, default=0.00)
    contact = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    lastupdate = serializers.DateTimeField(required=False,default=datetime.datetime.now())  
    tags = serializers.ListField(child=serializers.CharField(required=False), required=False)

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.title = attrs.get('title', instance.title)
            instance.brief = attrs.get('brief', instance.brief)
            instance.price = attrs.get('price', instance.price)
            instance.contact = attrs.get('contact', instance.contact)
            instance.location = attrs.get('location', instance.location)
            instance.lastupdate = attrs.get('lastupdate', instance.lastupdate)
            instance.tags = attrs.get('tags', instance.tags)
            return instance
        return models.productModel(attrs.get('objectid'), attrs.get('title'), attrs.get('brief')
        , attrs.get('price'), attrs.get('contact'), attrs.get('location'), attrs.get('lastupdate'), attrs.get('tags'))
