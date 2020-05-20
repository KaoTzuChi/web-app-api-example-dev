from rest_framework import viewsets
#from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime, base64
#import logging
#from services.mongodb import utilities as dbutilities
#from . import models
#from . import serializers as api_ser
import mywebapp.settings as settings
import mywebapp.globals as gvs

import stripe as stripe

Publishable_key = 'pk_test_7O6XurM2uVIasrfBmfjsgJlH000XXU3c6G'
Secret_key = 'sk_test_9vvspzu93NEpzVJDSuN1CetH00Q7pE8mBX'

@api_view(['GET','POST'])
def stripe_test(request):
    stripe.api_key = Secret_key

    response = stripe.PaymentIntent.create(
            amount=1000,
            currency='usd',
            payment_method_types=['card'],
            receipt_email='jenny.rosen@example.com',
        )

    return Response({'status':'stripe_test','data':response })