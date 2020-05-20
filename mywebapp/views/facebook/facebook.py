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
#from services.useraccount import models
#from services.useraccount import serializers as api_ser

def facebook_login(request):    
    return render(request, 'facebook_login.html', {})

