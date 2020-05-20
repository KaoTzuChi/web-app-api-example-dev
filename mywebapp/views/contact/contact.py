from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib import messages
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

create_data = {'subject':'','content':'','receiver':'jessie.kao.tc@gmail.com','sender':'jessie.kao.tc@gmail.com','cclist':'None'}
create_msg = ''
create_tag =''

def contact_create(request):    
    global create_data, create_msg, create_tag
    return render(request, 'contact_create.html', { 'create_data':create_data, 'create_msg':create_msg, 'create_tag':create_tag, })

def contact_sendmail(request):
    global create_data, create_msg, create_tag
    if request.method == 'POST':
        posteddata = dict(request.POST)    
        print('contact_sendmail posteddata : ',posteddata)

        model_data = { 
            'subject' : posteddata['subject'][0],
            'content' : posteddata['content'][0],
            'receiver' : posteddata['receiver'][0],
            'sender' : posteddata['sender'][0],
            'cclist' : posteddata['cclist'][0]
        }
        requests.post( settings.BASE_URL + 'oauth2_gmail/', json=json.dumps(model_data))
        #response = requests.post( settings.BASE_URL + 'oauth2_gmail/', json=json.dumps(model_data)  )
        #print('contact_sendmail response service : %s' %( response ))
     
    else:
        print('contact_sendmail not post method')    
    return redirect('/contact/create/',{ 'create_data': create_data, 'create_msg':create_msg, 'create_tag':create_tag, })

