from django.shortcuts import render
from django.http import HttpResponse
import requests, datetime, json

import mywebapp.settings as settings

def dashboard_main(request):
    response = requests.get( settings.BASE_URL + 'read_mycollectionthree_all/')
    receiveddata = None
    if response:
        receiveddata = response.json()
    print(receiveddata)
    return render(request, 'dashboard.html', {
        'receiveddata': receiveddata,
    })
