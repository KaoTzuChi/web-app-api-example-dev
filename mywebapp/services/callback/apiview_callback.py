from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime

from services.mongodb import utilities as dbutilities
from . import models
from . import serializers as api_ser

''' e.g. http://localhost:5678/read_callback_all '''
#@csrf_exempt
@api_view(['GET'])
def read_callback_all(request):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('callbackcollection')
        db_data = db_obj.read_documents_all('_id')       
        for doc in db_data:  
            formated_doc= models.callbackModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'sender'),
                dbutilities.getFieldDict( doc, 'data', ['data','status'] ),
                dbutilities.getFieldInteger( doc, 'statuscode'),
                dbutilities.getFieldDatetime( doc, 'lastupdate')
            )
            data_list.append(formated_doc)            
        serializedList = api_ser.callbackSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status':'read_callback_all fail'})

''' e.g. http://localhost:5678/read_callback_byid/5eb7d4b2338af773dd96f6fc '''
@api_view(['GET'])
def read_callback_byid(request, id):   
    if request.method == 'GET':
        formated_doc = None
        db_obj = dbutilities.db_util('callbackcollection')
        doc = db_obj.read_document(id)
        if doc is None:
            return Response({'status':'read_callback_byid no document'})
        else:      
            formated_doc= models.callbackModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'sender'),
                dbutilities.getFieldDict( doc, 'data', ['data','status'] ),
                dbutilities.getFieldInteger( doc, 'statuscode'),
                dbutilities.getFieldDatetime( doc, 'lastupdate')
            )       
            serializedList = api_ser.callbackSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response({'status':'read_callback_byid fail'})


''' e.g. http://localhost:5678/read_callback_byfield/sender/oauth/ '''
@api_view(['GET'])
def read_callback_byfield(request, field, value):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('callbackcollection')
        #========== find string field: EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, value)   

        #========== find string field: LIKE ==========
        ##regx = re.compile('^[\w]*'+value+'[\w]*', re.IGNORECASE)
        regx = re.compile(value, re.IGNORECASE)
        regobj = {'$regex':regx }
        db_data = db_obj.read_document_byfield(field, regobj)    
        
        #========== find number field ==========
        #db_data = db_obj.read_document_byfield('statuscode', {'$gt':5}) 
        
        #========== find datetime field ==========
        #start = datetime.datetime(2015, 2, 2, 6, 35, 6, 764)
        #end = datetime.datetime(2099, 2, 2, 6, 55, 3, 381)
        #db_data = db_obj.read_document_byfield('lastupdate', {'$gte': start, '$lt': end} ) 

        #========== find array field : EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, ["a", "b"])  
        #========== find array field : CONTAINS ========== equivalent to using find string field: LIKE ==========
        #db_data = db_obj.read_document_byfield(field, { '$all': ["a", "b"] }) 

        #========== find nested field ==========
        #db_data = db_obj.read_document_byfield('data.item1', regobj )
        #db_data = db_obj.read_document_byfield('data.item1', {'$gt':5} )    'services.dataaccess',

        for doc in db_data:  
            formated_doc= models.callbackModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'sender'),
                dbutilities.getFieldDict( doc, 'data', ['data','status'] ),
                dbutilities.getFieldInteger( doc, 'statuscode'),
                dbutilities.getFieldDatetime( doc, 'lastupdate')
            )
            print(doc)  
            data_list.append(formated_doc)            
        serializedList = api_ser.callbackSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status":"read_callback_byfield fail'})


'''
e.g. http://localhost:5678/create_doc_in_callback_return_newone/
request_data = { "sender": "oauth", 
"data": {"status":"valueofitem1", "data":"valueofitem2"}, 
"statuscode":200, "lastupdate":"2011-01-01T00:01:01Z" }
'''
@api_view(['POST'])
def create_doc_in_callback_return_newone(request):
    
    #print('create_doc_in_callback_return_newone request',request)
    #print('create_doc_in_callback_return_newone request.data ',request.data)
    #print('create_doc_in_callback_return_newone request.data ',type(request.data))
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    #print('create_doc_in_callback_return_newone request_data',request_data)
    #print('create_doc_in_callback_return_newone request_data',type(request_data))

    serialized = api_ser.callbackSerializer(data = request_data)
    #print('create_doc_in_callback_return_newone serialized.is_valid()',serialized.is_valid())
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        if reqId != None:
            tempdict = request_data.pop('objectid')  
        db_obj = dbutilities.db_util('callbackcollection')     
        inserted_ids = db_obj.create_documents([request_data])

        #print('create_doc_in_callback_return_newone request_data',request_data)
        #print('create_doc_in_callback_return_newone inserted_ids',inserted_ids)
        
        newdoc = None
        if(len(inserted_ids) > 0):
            newdoc = db_obj.read_document(inserted_ids[0])

        if newdoc is None:
            return Response({'status':'create_doc_in_callback_return_newone no doc is created'})
        else:      
            formated_doc= models.callbackModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'sender'),
                dbutilities.getFieldDict( newdoc, 'data', ['data','status'] ),
                dbutilities.getFieldInteger( newdoc, 'statuscode'),
                dbutilities.getFieldDatetime( newdoc, 'lastupdate')
            )       
            serializedList = api_ser.callbackSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)


'''
e.g. http://localhost:5678/replace_doc_in_callback_return_newone/
request_data = 
{ "objectid": "5ebc06f4b5c79873acd292de", "sender": "oauthxxb", 
"data": {"c":"ccc", "d":"ddd"}, 
"statuscode":200, "lastupdate":"2022-01-01T00:01:01Z" }
'''
@api_view(['POST'])
def replace_doc_in_callback_return_newone(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.callbackSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        if reqId != None:
            tempdict = request_data.pop('objectid')
        replacedata = request_data
        db_obj = dbutilities.db_util('callbackcollection')      
        modified_count = db_obj.replace_document(filterId, replacedata)
        newdoc = None
        if(modified_count > 0):
            newdoc = db_obj.read_document(reqId)
        if newdoc is None:
            return Response({'status':'replace_doc_in_callback_return_newone no doc id replaced'})
        else:      
            formated_doc= models.callbackModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'sender'),
                dbutilities.getFieldDict( newdoc, 'data', ['data','status'] ),
                dbutilities.getFieldInteger( newdoc, 'statuscode'),
                dbutilities.getFieldDatetime( newdoc, 'lastupdate')
            )       
            serializedList = api_ser.callbackSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)

''' 
e.g. http://localhost:5678/delete_doc_in_callback_return_count/
request_data = {"objectid": "5ebc08a4f3f21f2f7aa78e59"} 
'''
@api_view(['POST'])
def delete_doc_in_callback_return_count(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.callbackSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        db_obj = dbutilities.db_util('callbackcollection')        
        deleted_count = db_obj.delete_documents(filterId)
        if deleted_count is None:
            return Response({'status':'delete_doc_in_callback_return_count no doc is deleted'})
        else:
            return Response({
                'status':'delete_doc_in_callback_return_count success',
                'data' : deleted_count
            })
    else:
        return Response(serialized._errors)