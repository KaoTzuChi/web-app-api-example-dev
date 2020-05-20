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
from services.useraccount import models
from services.useraccount import serializers as api_ser

create_data = models.accountModel( '','','','','',None,None,False,False,False,'')
create_msg = ''
create_tag =''

def member_create(request):    
    global create_data, create_msg, create_tag
    #print('member_create create_data=',create_data.auth_token)
    #print('member_create create_msg=',create_msg)
    #print('member_create create_tag=',create_tag)

    return render(request, 'member_create.html', { 'create_data':create_data, 'create_msg':create_msg, 'create_tag':create_tag, })

def member_create_action(request):
    global create_data, create_msg, create_tag
    if request.method == 'POST':
        posteddata = dict(request.POST)    
        model_data = { 
            'username' : posteddata['username'][0], 'password' : posteddata['password'][0], 'email' : posteddata['email'][0],
            'first_name' : posteddata['first_name'][0], 'last_name' : posteddata['last_name'][0],
            'last_login' : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'date_joined' : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'is_staff' : 'False', 'is_superuser' : 'False', 'is_active' : 'False', 'auth_token' : 'None'
        }
        response = requests.post( settings.BASE_URL + 'account_create/', json=json.dumps(model_data)  )
        response_data = None
        if response:
            response_data = dict(response.json())      
            if response_data.get('username'):            
                create_data = models.accountModel(
                    response_data.get('username'), response_data.get('password'), response_data.get('email'), response_data.get('first_name'),
                    response_data.get('last_name'), response_data.get('last_login'), response_data.get('date_joined'), response_data.get('is_staff'),
                    response_data.get('is_superuser'), response_data.get('is_active'), response_data.get('auth_token')
                    )
                create_tag='disabled'
                create_msg= 'Create member successfully. Active account here: '+ settings.BASE_URL + 'account_activate/' + response_data.get('username')+'/'+ response_data.get('auth_token')+'/'
            else:
                create_data = models.accountModel(
                    posteddata['username'][0], posteddata['password'][0], posteddata['email'][0], posteddata['first_name'][0],
                    posteddata['last_name'][0], posteddata['last_login'][0], posteddata['date_joined'][0], posteddata['is_staff'][0],
                    posteddata['is_superuser'][0], posteddata['is_active'][0], posteddata['auth_token'][0]
                    )
                create_tag=''
                if response_data.get('status'):
                    create_msg = response_data.get('status')
                else:
                    create_msg='Create member causes unknown error.'
    else:
        pass    
    return redirect('/member/create/',{ 'create_data': create_data, 'create_msg':create_msg, 'create_tag':create_tag, })


login_data = models.accountModel( '','','','','',None,None,False,False,False,'')
login_msg = ''
login_tag =''

def member_login(request):    
    global login_data, login_msg, login_tag
    #print('member_login login_data=',login_data.auth_token)
    #print('member_login login_msg=',login_msg)
    #login_data.username = request.user.get_username() if request.user.get_username() else logout_data.username
    #logout_msg = logout_msg if request.user.get_username() else ''
    login_tag = 'disabled' if request.user.is_authenticated else ''
    
    return render(request, 'member_login.html', { 'login_data':login_data, 'login_msg':login_msg, 'login_tag':login_tag, })

def member_login_action(request):
    global login_data, login_msg, login_tag
    if request.method == 'POST':
        posteddata = dict(request.POST)    
        model_data = { 'username' : posteddata['username'][0], 'password' : posteddata['password'][0] }
        response = requests.post( settings.BASE_URL + 'account_login/', json=json.dumps(model_data)  )
        response_data = None
        if response:
            response_data = dict(response.json())      
            if response_data.get('username'):            
                login_data = models.accountModel(
                    response_data.get('username'), response_data.get('password'), response_data.get('email'), response_data.get('first_name'),
                    response_data.get('last_name'), response_data.get('last_login'), response_data.get('date_joined'), response_data.get('is_staff'),
                    response_data.get('is_superuser'), response_data.get('is_active'), response_data.get('auth_token')
                    )
                login_tag='disabled'
                login_msg='Member sign-in successfully.'

                #print('member_login login_data.username=',login_data.username )
                #print('member_login login_data.auth_token=',login_data.auth_token )

                auth_user = auth.authenticate( username= posteddata['username'][0], password= posteddata['password'][0] )
                auth.login(request, auth_user)
                #new_token, created = Token.objects.get_or_create( user=auth_user )

                #print('member_login request.user=',request.user )
                #print('member_login request.user=',request.user.auth_token )
                #print('member_login request.user.is_authenticated()=',str(request.user.is_authenticated) )
            else:
                login_data = models.accountModel( posteddata['username'][0], posteddata['password'][0], '','','',None,None,False,False,False,'')
                login_tag=''
                if response_data.get('status'):
                    login_msg = response_data.get('status')
                else:
                    login_msg='Member sign-in causes unknown error.'
    else:
        pass    
    return redirect('/member/login/',{ 'login_data': login_data, 'login_msg':login_msg, 'login_tag':login_tag, })


logout_data = models.accountModel( '','','','','',None,None,False,False,False,'')
logout_msg = ''
logout_tag =''

def member_logout(request):    
    global logout_data, logout_msg, logout_tag
    #print('member_logout logout_data=',logout_data.auth_token)
    #print('member_logout logout_msg=',logout_msg)
    #print('member_logout request.user.is_authenticated()=',str(request.user.is_authenticated) )    
    logout_data.username = request.user.get_username() if request.user.is_authenticated else logout_data.username
    #logout_msg = logout_msg if request.user.get_username() else ''
    logout_tag = '' if request.user.get_username() else 'disabled'
    return render(request, 'member_logout.html', { 'logout_data':logout_data, 'logout_msg':logout_msg, 'logout_tag':logout_tag, })

def member_logout_action(request):
    global logout_data, logout_msg, logout_tag
    if (request.method == 'POST') and (request.user) and (request.user.is_authenticated) :
        posteddata = dict(request.POST)    
        #print('member_logout_action posteddata=',posteddata)
        #print('member_logout_action request.user=',request.user )
        #print('member_logout_action request.user=',request.user.auth_token )
        #print('member_logout_action request.user.is_authenticated()=',str(request.user.is_authenticated) )
        model_data = {  'username' : logout_data.username }
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }

        #logout_data = models.accountModel( posteddata['username'][0], '', '','','',None,None,False,False,False,'')
        response = requests.post( settings.BASE_URL + 'account_logout/', json=json.dumps(model_data), headers= http_option )
        response_data = None
        if response:
            response_data = dict(response.json())   

            if response_data.get('status'):           
                logout_data.username = posteddata['username'][0]
                existing_user = User.objects.get( username = posteddata['username'][0] )
                auth.logout(request)
                #existing_user.auth_token.delete()
                logout_msg = response_data.get('status')
                #logout_msg = 'Member sign-out successfully.'
                logout_tag ='disabled'
            else:
                logout_msg='Member sign-out causes unknown error.'
    else:
        pass    
    return redirect('/member/logout/',{ 'logout_data': logout_data, 'logout_msg':logout_msg, 'logout_tag':logout_tag, })


update_data = models.accountModel( '','','','','',None,None,False,False,False,'')
update_msg = ''
update_tag =''

def member_reload(request):    
    update_data={}
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        #print('member_reload = ', request.user.get_username())
        response = requests.get( settings.BASE_URL + 'account_read_one/'+request.user.get_username()+'/', headers= http_option)
        update_data = None
        if response:  
            update_data = response.json()
        #print('member_reload = ', update_data)
    else:
        pass
        #update_msg = 'Authentication credentials were not provided.'
        #update_tag = 'disabled'
    return render(request, 'member_update.html', { 
        'update_data':update_data, 
        'update_msg':'', 
        'update_tag':'', 
        })
   

def member_update(request):    
    global update_data, update_msg, update_tag
    if (request.user) and (request.user.is_authenticated):
        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        #print('member_update = ', request.user.get_username())
        response = requests.get( settings.BASE_URL + 'account_read_one/'+request.user.get_username()+'/', headers= http_option)
        update_data = None
        if response:  
            update_data = response.json()
        #print('member_update = ', update_data)
    else:
        pass
        #update_msg = 'Authentication credentials were not provided.'
        #update_tag = 'disabled'
    return render(request, 'member_update.html', { 'update_data':update_data, 'update_msg':update_msg, 'update_tag':update_tag, })

def member_update_action(request):
    global update_data, update_msg, update_tag
    if (request.method == 'POST') and (request.user) and (request.user.is_authenticated):
        posteddata = dict(request.POST)    

        print('member_update_action posteddata=',posteddata)
        print('member_update_action request.user=',request.user )
        print('member_update_action request.user.auth_token=',request.user.auth_token )
        print('member_update_action request.user.is_authenticated=',str(request.user.is_authenticated) )

        model_data = { 
            'username' : posteddata['username'][0], 'password' : posteddata['password'][0], 'email' : posteddata['email'][0],
            'first_name' : posteddata['first_name'][0], 'last_name' : posteddata['last_name'][0],
            'last_login' : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'date_joined' : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'is_staff' : 'False', 'is_superuser' : 'False', 'is_active' : 'False', 'auth_token' : 'None'
        }

        http_option = { 'Content-Type':  'application/json', 'Authorization': 'Token ' + str(request.user.auth_token), }
        response = requests.post( settings.BASE_URL + 'account_update/', json=json.dumps(model_data) , headers= http_option )
        response_data = None
        if response:
            response_data = dict(response.json())       
        
            if response_data.get('username'):            
                update_data = models.accountModel(
                    response_data.get('username'), response_data.get('password'), response_data.get('email'), response_data.get('first_name'),
                    response_data.get('last_name'), response_data.get('last_login'), response_data.get('date_joined'), response_data.get('is_staff'),
                    response_data.get('is_superuser'), response_data.get('is_active'), response_data.get('auth_token')
                    )
                update_tag='disabled'
                update_msg='Update member successfully.'
            else:
                update_data = models.accountModel(
                    posteddata['username'][0], posteddata['password'][0], posteddata['email'][0], posteddata['first_name'][0],
                    posteddata['last_name'][0], posteddata['last_login'][0], posteddata['date_joined'][0], posteddata['is_staff'][0],
                    posteddata['is_superuser'][0], posteddata['is_active'][0], posteddata['auth_token'][0]
                    )
                update_tag=''
                if response_data.get('status'):
                    update_msg = response_data.get('status')
                else:
                    update_msg='Update member causes unknown error.'
    else:
        pass    
    return redirect('/member/update/',{ 'update_data': update_data, 'update_msg':update_msg, 'update_tag':update_tag, })


'''
class DataForm(forms.Form):
    field11 = forms.CharField(help_text="Enter a date for field11.")
    #field12 = forms.MultiValueField(help_text="Enter a date for field12.")
    field12 = forms.MultipleChoiceField(help_text="Enter a date for field12.")
    #field13 = forms.DateTimeField(help_text="Enter a date for field13.")
    field13 = forms.ChoiceField(help_text="Enter a date for field13.")
    #field14 = forms.DecimalField(help_text="Enter a date for field14.")
    field14 = forms.ChoiceField(help_text="Enter a date for field14.")
    field15 = forms.MultipleChoiceField(help_text="Enter a date for field15.")

    def clean_field11(self):
        check = self.cleaned_data['field11']
        if len(check) < 5:
            raise ValidationError(_('Invalid data - <5'))
        if len(check) > 12:
            raise ValidationError(_('Invalid data - >12'))
        return check

BooleanField, CharField, ChoiceField, TypedChoiceField, DateField, DateTimeField, 
DecimalField, DurationField, EmailField, FileField, FilePathField, FloatField, ImageField, 
IntegerField, GenericIPAddressField, MultipleChoiceField, TypedMultipleChoiceField, NullBooleanField, 
RegexField, SlugField, TimeField, URLField, UUIDField, ComboField, MultiValueField, 
SplitDateTimeField, ModelMultipleChoiceField, ModelChoiceField​​​​.
'''