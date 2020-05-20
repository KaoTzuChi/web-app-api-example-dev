from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

from services.mongodb import utilities as dbutilities
from . import models
from . import serializers as api_ser

''' e.g. http://localhost:5678/read_mycollectiontwo_all '''
#@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_mycollectiontwo_all(request):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('mycollectiontwo')
        db_data = db_obj.read_documents_all('_id')       
        for doc in db_data:  
            formated_doc= models.mycollectiontwoModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'field21'),
                dbutilities.getFieldDict( doc, 'field22', ['item1','item2'] ),
                dbutilities.getFieldDatetime( doc, 'field23'),
                dbutilities.getFieldDecimal( doc, 'field24'),
                dbutilities.getFieldList( doc, 'field25')
            )
            data_list.append(formated_doc)            
        serializedList = api_ser.mycollectiontwoSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status':'read_mycollectiontwo_all fail'})

''' e.g. http://localhost:5678/read_mycollectiontwo_byid/5eb7d4b2338af773dd96f6fc '''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_mycollectiontwo_byid(request, id):   
    if request.method == 'GET':
        formated_doc = None
        db_obj = dbutilities.db_util('mycollectiontwo')
        doc = db_obj.read_document(id)
        if doc is None:
            return Response({'status':'read_mycollectiontwo_byid no document'})
        else:      
            formated_doc= models.mycollectiontwoModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'field21'),
                dbutilities.getFieldDict( doc, 'field22', ['item1','item2'] ),
                dbutilities.getFieldDatetime( doc, 'field23'),
                dbutilities.getFieldDecimal( doc, 'field24'),
                dbutilities.getFieldList( doc, 'field25')
            )       
            serializedList = api_ser.mycollectiontwoSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response({'status':'read_mycollectiontwo_byid fail'})

''' e.g. http://localhost:5678/read_mycollectiontwo_byfield/field21/valueof-doc1-field21 '''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def read_mycollectiontwo_byfield(request, field, value):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('mycollectiontwo')
        #========== find string field: EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, value)   

        #========== find string field: LIKE ==========
        ##regx = re.compile('^[\w]*'+value+'[\w]*', re.IGNORECASE)
        regx = re.compile(value, re.IGNORECASE)
        regobj = {'$regex':regx }
        db_data = db_obj.read_document_byfield(field, regobj)    
        
        #========== find number field ==========
        #db_data = db_obj.read_document_byfield('field24', {'$gt':5}) 
        
        #========== find datetime field ==========
        #start = datetime.datetime(2015, 2, 2, 6, 35, 6, 764)
        #end = datetime.datetime(2099, 2, 2, 6, 55, 3, 381)
        #db_data = db_obj.read_document_byfield('field23', {'$gte': start, '$lt': end} ) 

        #========== find array field : EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, ["a", "b"])  
        #========== find array field : CONTAINS ========== equivalent to using find string field: LIKE ==========
        #db_data = db_obj.read_document_byfield(field, { '$all': ["a", "b"] }) 

        #========== find nested field ==========
        #db_data = db_obj.read_document_byfield('field22.item1', regobj )
        #db_data = db_obj.read_document_byfield('field22.item1', {'$gt':5} )
        #db_data = db_obj.read_document_byfield('field22.item1', {'$gte': start, '$lt': end} )

        for doc in db_data:  
            formated_doc= models.mycollectiontwoModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'field21'),
                dbutilities.getFieldDict( doc, 'field22', ['item1','item2'] ),
                dbutilities.getFieldDatetime( doc, 'field23'),
                dbutilities.getFieldDecimal( doc, 'field24'),
                dbutilities.getFieldList( doc, 'field25')
            )
            print(doc)  
            data_list.append(formated_doc)            
        serializedList = api_ser.mycollectiontwoSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status":"read_mycollectiontwo_byfield fail'})


'''
e.g. http://localhost:5678/create_doc_in_mycollectiontwo_return_newone/
request_data = { 
    "_id": "5d53ca1d72be9fe767779e70", 
    "field21" : "test value 1", 
    "field22" : {"item1":"test value 2", "item2":"test value 3" },
    "field23" : "2020-01-01T00:00:00Z",
    "field24" : 2.34
}
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_doc_in_mycollectiontwo_return_newone(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.mycollectiontwoSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        if reqId != None:
            tempdict = request_data.pop('objectid')  
        db_obj = dbutilities.db_util('mycollectiontwo')     
        inserted_ids = db_obj.create_documents([request_data])
        
        newdoc = None
        if(len(inserted_ids) > 0):
            newdoc = db_obj.read_document(inserted_ids[0])

        if newdoc is None:
            return Response({'status':'create_doc_in_mycollectiontwo_return_newone no doc is created'})
        else:      
            formated_doc= models.mycollectiontwoModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'field21'),
                dbutilities.getFieldDict( newdoc, 'field22', ['item1','item2'] ),
                dbutilities.getFieldDatetime( newdoc, 'field23'),
                dbutilities.getFieldDecimal( newdoc, 'field24'),
                dbutilities.getFieldList( newdoc, 'field25')
            )       
            serializedList = api_ser.mycollectiontwoSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)


'''
e.g. http://localhost:5678/replace_doc_in_mycollectiontwo_return_newone/
request_data = { 
    "_id": "5eb7f31938a5fd5d85ccf595", 
    "field21": "test value 5", 
    "field22":{"item1":"test value 6", "item2":"test value 7" },
    "field23": "2020-08-01T00:00:00Z",
    "field24": 4.56
}
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def replace_doc_in_mycollectiontwo_return_newone(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.mycollectiontwoSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        if reqId != None:
            tempdict = request_data.pop('objectid')
        replacedata = request_data
        db_obj = dbutilities.db_util('mycollectiontwo')      
        modified_count = db_obj.replace_document(filterId, replacedata)
        newdoc = None
        if(modified_count > 0):
            newdoc = db_obj.read_document(reqId)
        if newdoc is None:
            return Response({'status':'replace_doc_in_mycollectiontwo_return_newone no doc id replaced'})
        else:      
            formated_doc= models.mycollectiontwoModel( 
                dbutilities.getIdString( newdoc, '_id'),
                dbutilities.getFieldString( newdoc, 'field21'),
                dbutilities.getFieldDict( newdoc, 'field22', ['item1','item2'] ),
                dbutilities.getFieldDatetime( newdoc, 'field23'),
                dbutilities.getFieldDecimal( newdoc, 'field24'),
                dbutilities.getFieldList( newdoc, 'field25')
            )       
            serializedList = api_ser.mycollectiontwoSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response(serialized._errors)

''' 
e.g. http://localhost:5678/delete_doc_in_mycollectiontwo_return_count/
request_data = {"_id": "5eb7f31938a5fd5d85ccf595"} 
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_doc_in_mycollectiontwo_return_count(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.mycollectiontwoSerializer(data = request_data)
    if serialized.is_valid():
        reqId = request_data.get("objectid")
        filterId = {'_id': ObjectId(reqId)}
        db_obj = dbutilities.db_util('mycollectiontwo')        
        deleted_count = db_obj.delete_documents(filterId)
        if deleted_count is None:
            return Response({'status':'delete_doc_in_mycollectiontwo_return_count no doc is deleted'})
        else:
            return Response({
                'status':'delete_doc_in_mycollectiontwo_return_count success',
                'data' : deleted_count
            })
    else:
        return Response(serialized._errors)