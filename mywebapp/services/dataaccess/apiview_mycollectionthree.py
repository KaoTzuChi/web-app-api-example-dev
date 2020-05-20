from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime

from services.mongodb import utilities as dbutilities
from . import models
from . import serializers as api_ser

''' e.g. http://localhost:5678/read_mycollectionthree_all '''
#@csrf_exempt
@api_view(['GET'])
def read_mycollectionthree_all(request):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('mycollectionthree')
        db_data = db_obj.read_documents_all('_id')       
        for doc in db_data:  
            formated_doc= models.mycollectionthreeModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'field31'),
                dbutilities.getFieldInteger( doc, 'field32'),
                dbutilities.getFieldInteger( doc, 'field33'),
                dbutilities.getFieldDecimal( doc, 'field34'),
                dbutilities.getFieldList( doc, 'field35')
            )
            data_list.append(formated_doc)            
        serializedList = api_ser.mycollectionthreeSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status':'read_mycollectionthree_all fail'})

''' e.g. http://localhost:5678/read_mycollectionthree_byid/5eb7d4b2338af773dd96f6fc '''
@api_view(['GET'])
def read_mycollectionthree_byid(request, id):   
    if request.method == 'GET':
        formated_doc = None
        db_obj = dbutilities.db_util('mycollectionthree')
        doc = db_obj.read_document(id)
        if doc is None:
            return Response({'status':'read_mycollectionthree_byid no document'})
        else:      
            formated_doc= models.mycollectionthreeModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'field31'),
                dbutilities.getFieldInteger( doc, 'field32'),
                dbutilities.getFieldInteger( doc, 'field33'),
                dbutilities.getFieldDecimal( doc, 'field34'),
                dbutilities.getFieldList( doc, 'field35')
            )       
            serializedList = api_ser.mycollectionthreeSerializer(formated_doc, many=False)
            return Response(serializedList.data)   
    else:
        return Response({'status':'read_mycollectionthree_byid fail'})

''' e.g. http://localhost:5678/read_mycollectionthree_byfield/field31/valueof-doc1-field31 '''
@api_view(['GET'])
def read_mycollectionthree_byfield(request, field, value):   
    if request.method == 'GET':
        data_list = []
        db_obj = dbutilities.db_util('mycollectionthree')
        #========== find string field: EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, value)   

        #========== find string field: LIKE ==========
        ##regx = re.compile('^[\w]*'+value+'[\w]*', re.IGNORECASE)
        regx = re.compile(value, re.IGNORECASE)
        regobj = {'$regex':regx }
        db_data = db_obj.read_document_byfield(field, regobj)    
        
        #========== find number field ==========
        #db_data = db_obj.read_document_byfield('field34', {'$gt':5}) 
        
        #========== find datetime field ==========
        #start = datetime.datetime(2015, 2, 2, 6, 35, 6, 764)
        #end = datetime.datetime(2099, 2, 2, 6, 55, 3, 381)
        #db_data = db_obj.read_document_byfield('field33', {'$gte': start, '$lt': end} ) 

        #========== find array field : EQUAL ==========
        #db_data = db_obj.read_document_byfield(field, ["a", "b"])  
        #========== find array field : CONTAINS ========== equivalent to using find string field: LIKE ==========
        #db_data = db_obj.read_document_byfield(field, { '$all': ["a", "b"] }) 

        #========== find nested field ==========
        #db_data = db_obj.read_document_byfield('field32.item1', regobj )
        #db_data = db_obj.read_document_byfield('field32.item1', {'$gt':5} )
        #db_data = db_obj.read_document_byfield('field32.item1', {'$gte': start, '$lt': end} )

        for doc in db_data:  
            formated_doc= models.mycollectionthreeModel( 
                dbutilities.getIdString( doc, '_id'),
                dbutilities.getFieldString( doc, 'field31'),
                dbutilities.getFieldInteger( doc, 'field32'),
                dbutilities.getFieldInteger( doc, 'field33'),
                dbutilities.getFieldDecimal( doc, 'field34'),
                dbutilities.getFieldList( doc, 'field35')
            )
            print(doc)  
            data_list.append(formated_doc)            
        serializedList = api_ser.mycollectionthreeSerializer(data_list, many=True)
        return Response(serializedList.data)
    else:
        return Response({'status":"read_mycollectionthree_byfield fail'})

