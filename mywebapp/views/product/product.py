from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime, json
import requests

import mywebapp.settings as settings
from bson.objectid import ObjectId

from views.utility import dict_key
from services.product import models
from services.product import serializers as api_ser

#chkoptions = ['a','b','c','d','e','f','g','h']
chkoptions = ['a','b','c','d']

def product_query(request):
    tmpurl = settings.BASE_URL + 'read_product_all/'
    print('****** product_query****** tmpurl : ', tmpurl )
    response = requests.get( tmpurl)
    print('****** product_query****** response : ',response)
    receiveddata = None
    if response:
        receiveddata = response.json()
    return render(request, 'product_query.html', {
        'receiveddata': receiveddata,
        'chkoptions' : chkoptions,
    })

def product_detail(request, id):
    response = requests.get( settings.BASE_URL + 'read_product_byid/'+id+'/')
    receiveddata = None
    if response:
        receiveddata = response.json()
    receiveddata['lastupdate'] = datetime.datetime.strptime(receiveddata['lastupdate'],'%Y-%m-%dT%H:%M:%SZ')
    receiveddata['price'] = float(receiveddata['price'] )
    return render(request, 'product_detail.html', {
        'chkoptions' : chkoptions,
        'receiveddata':receiveddata,
    })

def product_search(request, field, value):
    response = requests.get( settings.BASE_URL + 'read_product_byfield/'+field+'/'+value+'/')
    receiveddata = None
    if response:
        receiveddata = response.json()
    return render(request, 'product_query.html', {
        'receiveddata': receiveddata,
        'chkoptions' : chkoptions,
    })

def product_addtocart(request):
    pagename = 'query'
    if (request.method == 'POST') and (request.user) and (request.user.is_authenticated):
        posteddata = dict(request.POST)   
        model_data = { 
            'productid' : posteddata['objectid'][0], 'productname' : posteddata['productname'][0],
            'orderid' : 'None', 'memberid' : request.user.get_username(),
            'price' : posteddata['price'][0], 'discount' : 1.00, 'count' : 1,
            'lastupdate' : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        pagename = posteddata['pagename'][0]
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }

        response = requests.post( settings.BASE_URL + 'create_doc_in_shoppingcart_return_newone/', json=json.dumps(model_data) , headers= http_option )
        response_data = None
        if response:
            response_data = dict(response.json())    

        print('product_addtocart',response_data)
        if response_data.get('productid'):            
            print('add to cart OK!')
        else:
            print('add to cart fail!')
    else:
        pass
    return redirect('/product/'+pagename)
    