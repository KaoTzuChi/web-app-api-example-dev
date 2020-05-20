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
import requests, datetime, json
import mywebapp.settings as settings
from bson.objectid import ObjectId

from views.utility import dict_key
from services.order import models as ordermodels
from services.shoppingcart import models as cartmodels
from services.order import serializers as order_ser
from services.shoppingcart import serializers as cart_ser

#order_status = {'0':'created','1':'paided','2':'delivering','3':'delivered','4':'processing','5':'finished'}
order_status = {0:'created',1:'paided',2:'delivering',3:'delivered',4:'processing',5:'finished'}

def cart_query(request):
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        response = requests.get( settings.BASE_URL + 'read_shoppingcart_unpaid/', headers= http_option)
        receiveddata = None
        if response:
            receiveddata = response.json()
        return render(request, 'cart_query.html', {
            'receiveddata': receiveddata,
        })
    else:
        print('cart_query not authenticated')

def cart_update(request):
    if (request.method == 'POST') and (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        posteddata = dict(request.POST)
        model_data = { 
            'objectid' : posteddata['objectid'][0], 'productid' : posteddata['productid'][0], 'productname' : posteddata['productname'][0], 
            'orderid' : "None", 'memberid' : request.user.get_username(),
            'price' : posteddata['price'][0], 'discount' : 1.00, 'count' :  posteddata['count'][0],
            'lastupdate' : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        print(model_data)
        response = requests.post( settings.BASE_URL + 'replace_doc_in_shoppingcart_return_newone/', json=json.dumps(model_data), headers= http_option  )
    else:
        pass
    return redirect('/cart/query/')

def cart_delete(request, id):
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        model_data = { 
            'objectid' : id,
        }
        response = requests.post( settings.BASE_URL + 'delete_doc_in_shoppingcart_return_count/', json=json.dumps(model_data), headers= http_option  )
    else:
        pass
    return redirect('/cart/query/')

def cart_checkout(request):
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        response = requests.get( settings.BASE_URL + 'read_shoppingcart_unpaid/', headers= http_option)
        receiveddata = None
        if response:
            receiveddata = response.json()
        totalprice=0.00
        totaldiscount=0.00
        for dataitem in receiveddata:
            print(dataitem.get('price'), dataitem.get('count'))
            tmpp = float(dataitem.get('price')) * float(dataitem.get('count'))
            tmpd = tmpp - (tmpp * float(dataitem.get('discount'))) 
            totalprice = totalprice + tmpp
            totaldiscount = totaldiscount + tmpd

        return render(request, 'cart_checkout.html', {
            'receiveddata': receiveddata,
            'totalprice' : totalprice,
            'totaldiscount' : totaldiscount,
            'user_first' : request.user.first_name,
            'user_last' : request.user.last_name,
            'user_name' : request.user.get_username(),
            'user_email' : request.user.email,
        })
    else:
        print('cart_checkout not authenticated')

def order_create(request):
    if (request.method == 'POST') and (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        posteddata = dict(request.POST)
        model_data = {  
            "memberid": request.user.get_username(), 
            "totalprice":posteddata['totalprice'][0], 
            "totaldiscount": posteddata['totaldiscount'][0], 
            "payment": posteddata['payment'][0], 
            "status": 0, 
            "lastupdate":datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        
        response = requests.post( settings.BASE_URL + 'create_doc_in_order_return_newone/', json=json.dumps(model_data), headers= http_option  )
        response_data = None
        if response:
            response_data = dict(response.json())     
        print('order_create response_data: ',response_data)
        if response_data.get('objectid'):
            neworderid = { "orderid": response_data.get('objectid') }
            response2 = requests.post( settings.BASE_URL + 'replace_orderid_in_shoppingcart_return_count/', json=json.dumps(neworderid), headers= http_option  )
            response_data2 = None
            if response:
                response2 = dict(response2.json())     
            print('order_create response_data2: ',response_data2)
        else:
            print('order_create fail')
    else:
        print('order_create not authenticated')
    return redirect('/cart/query/')

def order_query(request):
    global order_status
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        response = requests.get( settings.BASE_URL + 'read_order_all/', headers= http_option)
        receiveddata = None
        if response:
            receiveddata = response.json()
        return render(request, 'order_query.html', {
            'receiveddata': receiveddata,
            'order_status':order_status,
        })
    else:
        print('order_query not authenticated')

def order_detail(request, id):
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        response = requests.get( settings.BASE_URL + 'read_shoppingcart_byfield/orderid/'+id+'/', headers= http_option)
        receiveddata = None
        if response:
            receiveddata = response.json()
        return render(request, 'order_detail.html', {
            'receiveddata': receiveddata,
        })
    else:
        print('order_detail not authenticated')

