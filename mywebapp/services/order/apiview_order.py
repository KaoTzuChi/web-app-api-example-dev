from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bson.objectid import ObjectId
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import authentication_classes, permission_classes

from services.mongodb import utilities as dbutilities
from . import models
from . import serializers as api_ser



''' e.g. http://localhost:5678/read_order_all '''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_order_all(request):   
    if request.method == 'GET':
        #print('read_order_all is_authenticated',request.user.is_authenticated)
        #print('read_order_all is_authenticated',request.user.id)
        data_list = []
        db_obj = dbutilities.db_util('ordercollection')
        db_data = db_obj.read_documents_all('_id') if request.user.is_staff else db_obj.read_document_byfield('memberid', request.user.get_username())

        for doc in db_data:  
            formated_doc= models.orderModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'memberid'),
                dbutilities.getFieldDecimal( doc, 'totalprice'),
                dbutilities.getFieldDecimal( doc, 'totaldiscount'),
                dbutilities.getFieldString( doc, 'payment'),
                dbutilities.getFieldInteger( doc, 'status'),
                dbutilities.getFieldDatetime( doc, 'lastupdate')
            )
            data_list.append(formated_doc)            
        serializedList = api_ser.orderSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status':'read_order_all fail'})


''' e.g. 
http://localhost:5678/read_order_byid/5ebc06f3b5c79873acd292c8 
http://localhost:5678/read_order_byid/5ebc1a7986969a974183393c
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_order_byid(request, id):   
    if request.method == 'GET':
        formated_doc = None
        db_obj = dbutilities.db_util('ordercollection')
        #doc = db_obj.read_document(id)
        doc = db_obj.read_document(id) if request.user.is_staff else db_obj.read_document_bytwofield( '_id', ObjectId(id), 'memberid', request.user.get_username() )

        if doc is None:
            return Response({'status':'read_order_byid no document'})
        else:      
            formated_doc= models.orderModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'memberid'),
                dbutilities.getFieldDecimal( doc, 'totalprice'),
                dbutilities.getFieldDecimal( doc, 'totaldiscount'),
                dbutilities.getFieldString( doc, 'payment'),
                dbutilities.getFieldInteger( doc, 'status'),
                dbutilities.getFieldDatetime( doc, 'lastupdate')
            )       
            serializedList = api_ser.orderSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response({'status':'read_order_byid fail'})


''' 
http://localhost:5678/read_order_byfield/payment/payment1 
http://localhost:5678/read_order_byfield/status/1
http://localhost:5678/read_order_byfield/memberid/user2/
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_order_byfield(request, field, value):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('ordercollection')
        #========== find string field: EQUAL ==========
        if field.strip()=='price':
            value = float(value)
        elif field.strip()=='discount':
            value = float(value)
        elif field.strip()=='status':
            value = int(value)
        else:
            value = value.strip()

        #db_data = db_obj.read_document_byfield(field, value)   
        db_data = db_obj.read_document_byfield(field, value)  if request.user.is_staff else db_obj.read_documents_bytwofield( field, value, 'memberid', request.user.get_username() )

        #========== find string field: LIKE ==========
        ##regx = re.compile('^[\w]*'+value+'[\w]*', re.IGNORECASE)
        #regx = re.compile(value, re.IGNORECASE)
        #regobj = {'$regex':regx }
        #db_data = db_obj.read_document_byfield(field, regobj)    
        
        #========== find number field ==========
        #db_data = db_obj.read_document_byfield('field14', {'$gt':5}) 
        
        #========== find datetime field ==========
        #start = datetime.datetime(2015, 2, 2, 6, 35, 6, 764)
        #end = datetime.datetime(2099, 2, 2, 6, 55, 3, 381)
        #db_data = db_obj.read_document_byfield('field13', {'$gte': start, '$lt': end} ) 

        #========== find array field : EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, ["a", "b"])  
        #========== find array field : CONTAINS ========== equivalent to using find string field: LIKE ==========
        #db_data = db_obj.read_document_byfield(field, { '$all': ["a", "b"] }) 

        #========== find nested field ==========
        #db_data = db_obj.read_document_byfield('field12.item1', regobj )
        #db_data = db_obj.read_document_byfield('field12.item1', {'$gt':5} )
        #db_data = db_obj.read_document_byfield('field12.item1', {'$gte': start, '$lt': end} )

        for doc in db_data:  
            formated_doc= models.orderModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'memberid'),
                dbutilities.getFieldDecimal( doc, 'totalprice'),
                dbutilities.getFieldDecimal( doc, 'totaldiscount'),
                dbutilities.getFieldString( doc, 'payment'),
                dbutilities.getFieldInteger( doc, 'status'),
                dbutilities.getFieldDatetime( doc, 'lastupdate')
            )
            #print(doc)  
            data_list.append(formated_doc)            
        serializedList = api_ser.orderSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status":"read_order_byfield fail'})


'''
e.g. http://localhost:5678/create_doc_in_order_return_newone/
request_data = 
{  "memberid": "user1", "totalprice":111.11, "totaldiscount": 111, 
"payment": "payment1", "status": 1, "lastupdate":"2022-01-01T00:01:01Z" }
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_doc_in_order_return_newone(request):
    
    #print('create_doc_in_order_return_newone request',request)
    #print('create_doc_in_order_return_newone request.data ',request.data)
    #print('create_doc_in_order_return_newone request.data ',type(request.data))
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    request_data['memberid'] =  request_data['memberid'] if request.user.is_staff else request.user.get_username()
    #print('create_doc_in_order_return_newone request_data',request_data)
    #print('create_doc_in_order_return_newone request_data',type(request_data))

    serialized = api_ser.orderSerializer(data = request_data)
    #print('create_doc_in_order_return_newone serialized.is_valid()',serialized.is_valid())
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        if reqId != None:
            tempdict = request_data.pop('objectid')  
        db_obj = dbutilities.db_util('ordercollection')     
        inserted_ids = db_obj.create_documents([request_data])

        #print('create_doc_in_order_return_newone request_data',request_data)
        #print('create_doc_in_order_return_newone inserted_ids',inserted_ids)
        
        newdoc = None
        if(len(inserted_ids) > 0):
            newdoc = db_obj.read_document(inserted_ids[0])

        if newdoc is None:
            return Response({'status':'create_doc_in_order_return_newone no doc is created'})
        else:                  
            formated_doc= models.orderModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'memberid'),
                dbutilities.getFieldDecimal( newdoc, 'totalprice'),
                dbutilities.getFieldDecimal( newdoc, 'totaldiscount'),
                dbutilities.getFieldString( newdoc, 'payment'),
                dbutilities.getFieldInteger( newdoc, 'status'),
                dbutilities.getFieldDatetime( newdoc, 'lastupdate')
            )       
            serializedList = api_ser.orderSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)


'''
e.g. http://localhost:5678/replace_doc_in_order_return_newone/
request_data = 
{ "objectid": "5ebc1a7986969a974183393a", "memberid": "user111", "totalprice":111.11, "totaldiscount": 111, 
"payment": "payment1", "status": 1, "lastupdate":"2022-01-01T00:01:01Z" }
{ "objectid": "5ebc1a7986969a9741833942", "memberid": "user333", "totalprice":111.11, "totaldiscount": 111, 
"payment": "payment1", "status": 1, "lastupdate":"2022-01-01T00:01:01Z" }
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def replace_doc_in_order_return_newone(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)
    request_data['memberid'] =  request_data['memberid'] if request.user.is_staff else request.user.get_username()

    serialized = api_ser.orderSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        if reqId != None:
            tempdict = request_data.pop('objectid')
        replacedata = request_data
        db_obj = dbutilities.db_util('ordercollection')   

        chk_doc = db_obj.read_document(reqId)
        doc_owner = dbutilities.getFieldString( chk_doc, 'memberid') if chk_doc else ''

        #print('replace_doc_in_order_return_newone  reqId:',reqId)
        #print('replace_doc_in_order_return_newone  chk_doc:',chk_doc)
        #print('replace_doc_in_order_return_newone  is_staff:',request.user.is_staff)
        #print('replace_doc_in_order_return_newone  get_username:',request.user.get_username())
        #print('replace_doc_in_order_return_newone  memberid:', dbutilities.getFieldString( chk_doc, 'memberid') )
        #print('replace_doc_in_order_return_newone  doc_owner:',doc_owner)
        #print('replace_doc_in_order_return_newone  doc_owner:',(doc_owner== request.user.get_username()))

        if ( (request.user.is_staff) | (doc_owner== request.user.get_username()) ):
            modified_count = db_obj.replace_document(filterId, replacedata)
            newdoc = None
            if(modified_count > 0):
                newdoc = db_obj.read_document(reqId)                
            if newdoc is None:
                return Response({'status':'replace_doc_in_order_return_newone no doc id replaced'})
            else:      
                formated_doc= models.orderModel( 
                    dbutilities.getIdString( newdoc, '_id'),
                    dbutilities.getFieldString( newdoc, 'memberid'),
                    dbutilities.getFieldDecimal( newdoc, 'totalprice'),
                    dbutilities.getFieldDecimal( newdoc, 'totaldiscount'),
                    dbutilities.getFieldString( newdoc, 'payment'),
                    dbutilities.getFieldInteger( newdoc, 'status'),
                    dbutilities.getFieldDatetime( newdoc, 'lastupdate')
                )       
                serializedList = api_ser.orderSerializer(formated_doc, many=False)
                return Response(serializedList.data)   
        else:
            return Response({'status':'replace_doc_in_order_return_newone not data owner'})
    else:
        return Response(serialized._errors)

'''
e.g. http://localhost:5678/replace_doc_in_order_return_newone/
request_data = 
{ "objectid": "5ebc1a7986969a974183393a", "status": 5  }
{ "objectid": "5ebd2ef1f0572b28ea1b0ca2", "status": 5 }

{ "orderid": "5ebd2ef1f0572b28ea1b0ca1", "status": 3 }
'''
#@api_view(['POST'])
#@permission_classes([IsAuthenticated])
#def replace_status_in_order_return_newone(request):
@api_view(['GET','POST'])
def paymentcallback(request):    
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.orderSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid") if request_data.get("objectid") else request_data.get("orderid")
        filterId = {'_id': ObjectId(reqId)}
        db_obj = dbutilities.db_util('ordercollection')   
        chk_doc = db_obj.read_document(reqId)
        doc_owner = dbutilities.getFieldString( chk_doc, 'memberid') if chk_doc else ''

        if ( (request.user.is_staff) | (doc_owner== request.user.get_username()) ) and chk_doc:
            
            replacedata = { "objectid": reqId, 
            "memberid": dbutilities.getFieldString( chk_doc, 'memberid'), 
            "totalprice": dbutilities.getFieldString( chk_doc, 'totalprice'), 
            "totaldiscount": dbutilities.getFieldString( chk_doc, 'totaldiscount'), 
            "payment": dbutilities.getFieldString( chk_doc, 'payment'), 
            "status": request_data.get("status"), 
            "lastupdate": datetime.datetime.now() 
            }

            modified_count = db_obj.replace_document(filterId, replacedata)
            newdoc = None
            if(modified_count > 0):
                newdoc = db_obj.read_document(reqId)                
            if newdoc is None:
                return Response({'status':'replace_status_in_order_return_newone no doc id replaced'})
            else:  
                '''    
                formated_doc= models.orderModel( 
                    dbutilities.getIdString( newdoc, '_id'),
                    dbutilities.getFieldString( newdoc, 'memberid'),
                    dbutilities.getFieldDecimal( newdoc, 'totalprice'),
                    dbutilities.getFieldDecimal( newdoc, 'totaldiscount'),
                    dbutilities.getFieldString( newdoc, 'payment'),
                    dbutilities.getFieldInteger( newdoc, 'status'),
                    dbutilities.getFieldDatetime( newdoc, 'lastupdate')
                )       
                serializedList = api_ser.orderSerializer(formated_doc, many=False)
                return Response(serializedList.data)   
                '''
                return Response({
                    'status':'replace_status_in_order_return_newone success',
                    'data' : 1
                })
        else:
            return Response({'status':'replace_status_in_order_return_newone not data owner'})
    else:
        return Response(serialized._errors)


''' 
e.g. http://localhost:5678/delete_doc_in_order_return_count/
request_data = {"objectid": "5ebc1a7986969a974183393d"} 
request_data = {"objectid": "5ebc3766848dd6278bc142e1"} 
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_doc_in_order_return_count(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.orderSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        db_obj = dbutilities.db_util('ordercollection')      

        chk_doc = db_obj.read_document(reqId)
        doc_owner = dbutilities.getFieldString( chk_doc, 'memberid') if chk_doc else ''

        if ( (request.user.is_staff) | (doc_owner== request.user.get_username()) ):
            deleted_count = db_obj.delete_documents(filterId)
            if deleted_count is None:
                return Response({'status':'delete_doc_in_order_return_count no doc is deleted'})
            else:
                return Response({
                    'status':'delete_doc_in_order_return_count success',
                    'data' : deleted_count
                })
        else:
            return Response({'status':'delete_doc_in_order_return_count not data owner'})
    else:
        return Response(serialized._errors)