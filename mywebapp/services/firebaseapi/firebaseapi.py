from rest_framework import viewsets
#from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime, base64
import mywebapp.settings as settings
import mywebapp.globals as gvs


import os 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'services/firebaseapi/cloud-credentials.json'

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import firestore


SECRETS_FILE = ('services/firebaseapi/serviceAccountKey.json')
REALTIME_DB = 'https://avlexam-d6f56.firebaseio.com/'

@api_view(['GET','POST'])
def firebase_update(request):
    db = firestore.Client()
    print('firebase_update db : %s'%( db ))

    doc_ref = db.collection(u'testcollection').document(u'yg0GqsKuByzZNgKwuhwL')
    print('firebase_update doc_ref : %s'%( doc_ref ))

    doc_ref.set({
        u'firstxxx': u'Ada',
        u'lastxxx': u'Lovelace',
        u'bornxxx': 1815
    })

    # Then query for documents
    users_ref = db.collection(u'testcollection')
    print('firebase_update users_ref : %s'%( users_ref ))

    returndata = {}
    for doc in users_ref.stream():
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        returndata.update( { str(doc.id) : doc.to_dict() } )
        
    return Response({'status':'firebase_update responsed','data':returndata })

@api_view(['GET','POST'])
def firebase_retrieve(request):
    db = firestore.Client()
    print('firebase_retrieve db : %s'%( db ))

    doc_ref = db.collection(u'testcollection')
    print('firebase_retrieve doc_ref : %s'%( doc_ref ))

    returndata = {}
    for doc in doc_ref.stream():
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        returndata.update( { str(doc.id) : doc.to_dict() } )
        
    return Response({'status':'firebase_retrieve responsed','data':returndata })


@api_view(['GET','POST'])
def firebase_insert(request):
    db = firestore.Client()
    print('firebase_insert db : %s'%( db ))

    doc_ref = db.collection(u'testcollection')
    print('firebase_insert doc_ref : %s'%( doc_ref ))

    data = {
        u'name': u'Los Angeles',
        u'state': u'CA',
        u'country': u'USA'
    }

    # Add a new doc in collection 'cities' with ID 'LA'
    db.collection(u'testcollection').document(u'inserted').set(data)


    # Then query for documents
    result_ref = db.collection(u'testcollection')
    print('firebase_insert users_ref : %s'%( result_ref ))

    returndata = {}
    for doc in result_ref.stream():
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        returndata.update( { str(doc.id) : doc.to_dict() } )
        
    return Response({'status':'firebase_insert responsed','data':returndata })


@api_view(['GET','POST'])
def firebase_delete(request):
    return Response({'status':'firebase_delete no request data' })

