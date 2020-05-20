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
from email.mime.text import MIMEText


'''
get : http://localhost:5678/oauth2_gmail/
post : 
{ 
    "subject" : "test subject 1",
    "content" : "test content 1",
    "receiver" : "jessie.kao.tc@gmail.com",
    "sender" : "jessie.kao.tc@gmail.com",
    "cclist" : "None"
}
'''
#import os 
#os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
#from __future__ import print_function
import pickle
import os.path
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SCOPES = [
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/spreadsheets'
]
SECRETS_FILE = ('/home/www/avlexam/mywebapp/services/googleapi/'+settings.FILENAME_PREFIX+'credentials.json') if (gvs.appEntry()>0) else ('services/googleapi/'+settings.FILENAME_PREFIX+'credentials.json')

#@csrf_exempt
@api_view(['GET','POST'])
def oauth2_gmail(request):
    CALLBACK_PATH = (settings.BASE_URL+'oauth2_gmail')
    print('oauth2_gmail gvs.getOauthState start : %s'%( gvs.getOauthState() ))

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            STATE = gvs.getOauthState()
            if STATE:
                print('oauth2_gmail GOT STATE : %s'%( STATE ))
                flow = InstalledAppFlow.from_client_secrets_file( SECRETS_FILE, scopes=SCOPES, state=STATE)
                flow.redirect_uri = CALLBACK_PATH
                authorization_response = request.build_absolute_uri()
                flow.fetch_token(authorization_response=authorization_response)
                creds = flow.credentials
                #flow = InstalledAppFlow.from_client_secrets_file( SECRETS_FILE, SCOPES)
                #flow.redirect_uri = CALLBACK_PATH
                #creds = flow.run_local_server()
                print('oauth2_gmail creds : %s'%( creds ))
            else:
                print('oauth2_gmail NO STATE : %s'%( STATE ))
                flow = InstalledAppFlow.from_client_secrets_file( SECRETS_FILE, SCOPES)
                flow.redirect_uri = CALLBACK_PATH
                authorization_url, _state = flow.authorization_url( access_type='offline', include_granted_scopes='true')
                #creds = flow.run_local_server(port=0)
                gvs.setOauthState(_state)
                print('oauth2_gmail gvs.getOauthState setted : %s'%( gvs.getOauthState() ))
                print('oauth2_gmail authorization_url : %s'%( authorization_url ))
                return HttpResponseRedirect( authorization_url )
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    print('oauth2_gmail request.method : %s'%( request.method ))

    if request.method == 'GET':
        # Call the Gmail API
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])
        return Response({ 'status':'oauth2_gmail done', 'data' : labels })

    else:
        request_data=request.data
        if type(request_data)==str: request_data = json.loads(request_data)
        print('oauth2_gmail request_data : %s'%( request_data ))
        if( request_data.get("subject") and request_data.get("content")):
            message = MIMEText( request_data.get("content") )
            message['to'] = request_data.get("receiver")
            message['from'] = request_data.get("sender")
            message['subject'] = request_data.get("subject")
            #_body = {'raw': base64.urlsafe_b64encode(message.as_string())}
            #_body = {'raw': base64.b64encode(message.as_bytes())}
            raw = base64.urlsafe_b64encode(message.as_bytes())
            raw = raw.decode()
            _body = {'raw': raw}
            try:
                user_id = 'me'
                message = (service.users().messages().send(userId=user_id, body=_body).execute())
                print('oauth2_gmail Message Id : %s'%( message['id'] ))
                #return message
                return Response({'status':'oauth2_gmail mail sent successfully'})

            except errors.HttpError as error:
                print('oauth2_gmail An error occurred : %s'%( error ))
                return Response({'status': ('oauth2_gmail An error occurred: %s'% error) })
        else:
            return Response({'status':'oauth2_gmail no request data' })



@api_view(['GET','POST'])
def oauth2_sheets(request):
    CALLBACK_PATH = (settings.BASE_URL+'oauth2_sheets')
    print('oauth2_sheets gvs.getOauthState start : %s'%( gvs.getOauthState() ))
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            STATE = gvs.getOauthState()
            if STATE:
                print('oauth2_sheets GOT STATE : %s'%( STATE ))
                flow = InstalledAppFlow.from_client_secrets_file( SECRETS_FILE, scopes=SCOPES, state=STATE)
                flow.redirect_uri = CALLBACK_PATH
                authorization_response = request.build_absolute_uri()
                flow.fetch_token(authorization_response=authorization_response)
                creds = flow.credentials
                #flow = InstalledAppFlow.from_client_secrets_file( SECRETS_FILE, SCOPES)
                #flow.redirect_uri = CALLBACK_PATH
                #creds = flow.run_local_server()
                print('oauth2_sheets creds : %s'%( creds ))
            else:
                print('oauth2_sheets NO STATE : %s'%( STATE ))
                flow = InstalledAppFlow.from_client_secrets_file( SECRETS_FILE, SCOPES)
                flow.redirect_uri = CALLBACK_PATH
                authorization_url, _state = flow.authorization_url( access_type='offline', include_granted_scopes='true')
                #creds = flow.run_local_server(port=0)
                gvs.setOauthState(_state)
                print('oauth2_sheets gvs.getOauthState setted : %s'%( gvs.getOauthState() ))
                print('oauth2_sheets authorization_url : %s'%( authorization_url ))
                return HttpResponseRedirect( authorization_url )
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    print('oauth2_sheets request.method : %s'%( request.method ))

    if request.method == 'GET':
        #https://docs.google.com/spreadsheets/d/1J0kEf5DUTlNmQpvhtOqM5XMN89bA9HFCf8vd1ZRCYn0/edit?usp=sharing
        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1J0kEf5DUTlNmQpvhtOqM5XMN89bA9HFCf8vd1ZRCYn0'
        SAMPLE_RANGE_NAME = 'sheet1!A2:E'

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('oauth2_sheets No data found.')
        else:
            print('oauth2_sheets Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('oauth2_sheets row in values : %s, %s' % (row[0], row[4]))

        return Response({ 'status':'oauth2_sheets done', 'data' : values })

    else:
        request_data=request.data
        if type(request_data)==str: request_data = json.loads(request_data)
        print('oauth2_sheets request_data : %s'%( request_data ))

        if( request_data.get("subject") and request_data.get("content")):
            return Response({ 'status':'oauth2_sheets done', 'data' : request_data })
        else:
            return Response({'status':'oauth2_sheets no request data' })