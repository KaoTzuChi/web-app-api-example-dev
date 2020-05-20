from django.shortcuts import render
from django.http import HttpResponse
#from datetime import date, time, datetime, tzinfo
from bson.objectid import ObjectId
import datetime
import sys
import django
from services.useraccount import models as usermodels
from django.contrib.auth.models import User
import mywebapp.settings as settings

def index(request):
    #print(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'))
    #print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC+00:00'))
    #post_list = [] #Post.objects.all()
    return render(request, 'home.html',{
        'baseurl':settings.BASE_URL,
        'appentry':settings.APP_ENTRY
    })
'''
    showtext = '<h1> Welcome to the Django APP! </h1>'    
    try:        
        test_db = utilities.db_util('mycollectionone')
        test_db_data = test_db.read_documents_all('_id')
        showtext = showtext + '<h2> Data of mycollectionone in mydatabase </h2><ul>'
        data_count = 0
        for doc in test_db_data:
            showtext = showtext + '<li> document[%s] = %s </li>' % (data_count, doc)
            data_count +=1
        showtext = showtext + '</ul>'
        showtext = showtext + '<p> <b>Current time</b> = %s </p>' % datetime.datetime.now()
        showtext = showtext + '<p> <b>Version of python</b> = %s </p>' % sys.version
        showtext = showtext + '<p> <b>Version of django</b> = %s </p>' % django.get_version()
        showtext = showtext + '<p> <b>Version of rest_framework</b> = %s </p>' % rest_framework.VERSION
        showtext = showtext + '<p> <b>Version of pymongo</b> = %s </p>' % pymongo.version
        # Insert multiple documents:
        # tempdata = [ {'field1': 'a'}, {'field1': 'b', 'field4': 2.22 }, {'field1': 'c', 'field3': '20200202'}]
        # result = test_db.create_documents(tempdata)
    except Exception as e:
        showtext = showtext + '<p> exception=%s </p>' % e
    return HttpResponse('<div>' + showtext + '</div>')

'''    