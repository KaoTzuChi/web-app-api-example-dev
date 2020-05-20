from rest_framework import serializers
from datetime import date, time, datetime, tzinfo
import datetime
from . import models

class mycollectiononeSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    field11 = serializers.CharField(required=False)
    field12 = serializers.DictField(serializers.CharField(required=False, default=''))
    field13 = serializers.DateTimeField(required=False,default=datetime.datetime.now())  
    field14 = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, default=0.00)
    field15 = serializers.ListField(child=serializers.CharField(required=False), required=False)

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.field11 = attrs.get('field11', instance.field11)
            instance.field12 = attrs.get('field12', instance.field12)
            instance.field13 = attrs.get('field13', instance.field13)
            instance.field14 = attrs.get('field14', instance.field14)
            instance.field15 = attrs.get('field15', instance.field15)
            return instance
        return models.collectionOneModel(attrs.get('objectid'), attrs.get('field11'), attrs.get('field12')
        , attrs.get('field13'), attrs.get('field14'), attrs.get('field15'))

class mycollectiontwoSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    field21 = serializers.CharField(required=False)
    field22 = serializers.DictField(serializers.CharField(required=False, default=''))
    field23 = serializers.DateTimeField(required=False,default=datetime.datetime.now())  
    field24 = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, default=0.00)
    field25 = serializers.ListField(child=serializers.CharField(required=False), required=False)

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.field21 = attrs.get('field21', instance.field21)
            instance.field22 = attrs.get('field22', instance.field22)
            instance.field23 = attrs.get('field23', instance.field23)
            instance.field24 = attrs.get('field24', instance.field24)
            instance.field25 = attrs.get('field25', instance.field25)
            return instance
        return models.collectionTwoModel(attrs.get('objectid'), attrs.get('field21'), attrs.get('field22')
        , attrs.get('field23'), attrs.get('field24'), attrs.get('field25'))

class mycollectionthreeSerializer(serializers.Serializer):
    objectid = serializers.CharField(required=False)
    field31 = serializers.CharField(required=False)
    field32 = serializers.IntegerField(required=False,default=0)  
    field33 = serializers.IntegerField(required=False,default=0)  
    field34 = serializers.DecimalField(max_digits=3, decimal_places=2, required=False, default=0.00)
    field35 = serializers.ListField(child=serializers.CharField(required=False), required=False)

    def create(self, attrs, instance=None):
        if instance:
            instance.objectid = attrs.get('objectid', instance.objectid)
            instance.field31 = attrs.get('field31', instance.field31)
            instance.field32 = attrs.get('field32', instance.field32)
            instance.field33 = attrs.get('field33', instance.field33)
            instance.field34 = attrs.get('field34', instance.field34)
            instance.field35 = attrs.get('field35', instance.field35)
            return instance
        return models.collectionTwoModel(attrs.get('objectid'), attrs.get('field31'), attrs.get('field32')
        , attrs.get('field33'), attrs.get('field34'), attrs.get('field35'))
