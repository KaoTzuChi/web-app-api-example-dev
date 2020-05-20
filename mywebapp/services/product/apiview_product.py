from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime

from services.mongodb import utilities as dbutilities
from . import models
from . import serializers as api_ser

'''
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class read_product_all(APIView):
    def get(self, request, format=None):
        print('****** read_product_all****** request : ', request )
        print('****** read_product_all****** request.method : ', request.method )
        if request.method == 'GET':
            data_list = []
            db_obj = dbutilities.db_util('productcollection')
            db_data = db_obj.read_documents_all('_id')       
            for doc in db_data:  
                formated_doc= models.productModel( 
                    dbutilities.getIdString( doc, '_id'),
                    dbutilities.getFieldString( doc, 'title'),
                    dbutilities.getFieldString( doc, 'brief' ),
                    dbutilities.getFieldDecimal( doc, 'price'),
                    dbutilities.getFieldString( doc, 'contact'),
                    dbutilities.getFieldString( doc, 'location'),
                    dbutilities.getFieldDatetime( doc, 'lastupdate'),
                    dbutilities.getFieldList( doc, 'tags')
                )
                data_list.append(formated_doc)            
            serializedList = api_ser.productSerializer(data_list, many=True)
            return Response(serializedList.data)
        else:
            return Response({'status':'read_product_all fail'})
'''

''' e.g. http://localhost:5678/read_product_all '''
#@csrf_exempt
@api_view(['GET'])
def read_product_all(request):   
    print('****** read_product_all****** request : ', request )
    print('****** read_product_all****** request.method : ', request.method )
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('productcollection')
        db_data = db_obj.read_documents_all('_id')       
        for doc in db_data:  
            formated_doc= models.productModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'title'),
                dbutilities.getFieldString( doc, 'brief' ),
                dbutilities.getFieldDecimal( doc, 'price'),
                dbutilities.getFieldString( doc, 'contact'),
                dbutilities.getFieldString( doc, 'location'),
                dbutilities.getFieldDatetime( doc, 'lastupdate'),
                dbutilities.getFieldList( doc, 'tags')
            )
            data_list.append(formated_doc)            
        serializedList = api_ser.productSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status':'read_product_all fail'})

''' e.g. http://localhost:5678/read_product_byid/5ebc06f3b5c79873acd292bf '''
@api_view(['GET'])
def read_product_byid(request, id):   
    if request.method == 'GET':
        formated_doc = None
        db_obj = dbutilities.db_util('productcollection')
        doc = db_obj.read_document(id)
        if doc is None:
            return Response({'status':'read_product_byid no document'})
        else:      
            formated_doc= models.productModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'title'),
                dbutilities.getFieldString( doc, 'brief' ),
                dbutilities.getFieldDecimal( doc, 'price'),
                dbutilities.getFieldString( doc, 'contact'),
                dbutilities.getFieldString( doc, 'location'),
                dbutilities.getFieldDatetime( doc, 'lastupdate'),
                dbutilities.getFieldList( doc, 'tags')
            )       
            serializedList = api_ser.productSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response({'status':'read_product_byid fail'})


''' e.g. http://localhost:5678/read_product_byfield/title/two '''
@api_view(['GET'])
def read_product_byfield(request, field, value):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('productcollection')
        #========== find string field: EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, value)   

        #========== find string field: LIKE ==========
        ##regx = re.compile('^[\w]*'+value+'[\w]*', re.IGNORECASE)
        regx = re.compile(value, re.IGNORECASE)
        regobj = {'$regex':regx }
        db_data = db_obj.read_document_byfield(field, regobj)    
        
        #========== find number field ==========
        #db_data = db_obj.read_document_byfield('price', {'$gt':5}) 
        
        #========== find datetime field ==========
        #start = datetime.datetime(2015, 2, 2, 6, 35, 6, 764)
        #end = datetime.datetime(2099, 2, 2, 6, 55, 3, 381)
        #db_data = db_obj.read_document_byfield('lastupdate', {'$gte': start, '$lt': end} ) 

        #========== find array field : EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, ["a", "b"])  
        #========== find array field : CONTAINS ========== equivalent to using find string field: LIKE ==========
        #db_data = db_obj.read_document_byfield(field, { '$all': ["a", "b"] }) 

        #========== find nested field ==========
        #db_data = db_obj.read_document_byfield('field12.item1', regobj )
        #db_data = db_obj.read_document_byfield('field12.item1', {'$gt':5} )
        #db_data = db_obj.read_document_byfield('field12.item1', {'$gte': start, '$lt': end} )

        for doc in db_data:  
            formated_doc= models.productModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'title'),
                dbutilities.getFieldString( doc, 'brief' ),
                dbutilities.getFieldDecimal( doc, 'price'),
                dbutilities.getFieldString( doc, 'contact'),
                dbutilities.getFieldString( doc, 'location'),
                dbutilities.getFieldDatetime( doc, 'lastupdate'),
                dbutilities.getFieldList( doc, 'tags')
            )
            print(doc)  
            data_list.append(formated_doc)            
        serializedList = api_ser.productSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status":"read_product_byfield fail'})


'''
e.g. http://localhost:5678/create_doc_in_product_return_newone/
request_data = 
{ "title": "product xx", "brief": "brief xxx", "price":999, "contact": "+886-2-4445-1111", 
"location": "location xx", "lastupdate":"2022-01-01T00:01:01Z", "tags":["a","c","d"] }
'''
@api_view(['POST'])
def create_doc_in_product_return_newone(request):
    
    #print('create_doc_in_product_return_newone request',request)
    #print('create_doc_in_product_return_newone request.data ',request.data)
    #print('create_doc_in_product_return_newone request.data ',type(request.data))
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    #print('create_doc_in_product_return_newone request_data',request_data)
    #print('create_doc_in_product_return_newone request_data',type(request_data))

    serialized = api_ser.productSerializer(data = request_data)
    #print('create_doc_in_product_return_newone serialized.is_valid()',serialized.is_valid())
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        if reqId != None:
            tempdict = request_data.pop('objectid')  
        db_obj = dbutilities.db_util('productcollection')     
        inserted_ids = db_obj.create_documents([request_data])

        #print('create_doc_in_product_return_newone request_data',request_data)
        #print('create_doc_in_product_return_newone inserted_ids',inserted_ids)
        
        newdoc = None
        if(len(inserted_ids) > 0):
            newdoc = db_obj.read_document(inserted_ids[0])

        if newdoc is None:
            return Response({'status':'create_doc_in_product_return_newone no doc is created'})
        else:      
            formated_doc= models.productModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'title'),
                dbutilities.getFieldString( newdoc, 'brief' ),
                dbutilities.getFieldDecimal( newdoc, 'price'),
                dbutilities.getFieldString( newdoc, 'contact'),
                dbutilities.getFieldString( newdoc, 'location'),
                dbutilities.getFieldDatetime( newdoc, 'lastupdate'),
                dbutilities.getFieldList( newdoc, 'tags')
            )       
            serializedList = api_ser.productSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)


'''
e.g. http://localhost:5678/replace_doc_in_product_return_newone/
request_data = 
{ "objectid": "5ebc06f3b5c79873acd292c0",
"title": "product bbb", "brief": "brief fff", "price":666, "contact": "+886-2-7777-1111", 
"location": "location bbb", "lastupdate":"2012-01-01T00:01:01Z", "tags":["a","d"] }
'''
@api_view(['POST'])
def replace_doc_in_product_return_newone(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.productSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        if reqId != None:
            tempdict = request_data.pop('objectid')
        replacedata = request_data
        db_obj = dbutilities.db_util('productcollection')      
        modified_count = db_obj.replace_document(filterId, replacedata)
        newdoc = None
        if(modified_count > 0):
            newdoc = db_obj.read_document(reqId)
        if newdoc is None:
            return Response({'status':'replace_doc_in_product_return_newone no doc id replaced'})
        else:      
            formated_doc= models.productModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'title'),
                dbutilities.getFieldString( newdoc, 'brief' ),
                dbutilities.getFieldDecimal( newdoc, 'price'),
                dbutilities.getFieldString( newdoc, 'contact'),
                dbutilities.getFieldString( newdoc, 'location'),
                dbutilities.getFieldDatetime( newdoc, 'lastupdate'),
                dbutilities.getFieldList( newdoc, 'tags')
            )       
            serializedList = api_ser.productSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)

''' 
e.g. http://localhost:5678/delete_doc_in_product_return_count/
request_data = {"objectid": "5ebc06f3b5c79873acd292be"} 
'''
@api_view(['POST'])
def delete_doc_in_product_return_count(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.productSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        db_obj = dbutilities.db_util('productcollection')        
        deleted_count = db_obj.delete_documents(filterId)
        if deleted_count is None:
            return Response({'status':'delete_doc_in_product_return_count no doc is deleted'})
        else:
            return Response({
                'status':'delete_doc_in_product_return_count success',
                'data' : deleted_count
            })
    else:
        return Response(serialized._errors)