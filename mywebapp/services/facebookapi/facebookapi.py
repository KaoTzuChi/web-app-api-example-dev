from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from django.http import HttpResponse, HttpResponseRedirect
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt 
import re, datetime, json, datetime, base64, urllib
import mywebapp.settings as settings
import mywebapp.globals as gvs

import facebook

APP_ID = '331830000000000'
APP_SECRET = 'd6xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
APP_TOKEN = '331830000000000|o3oy-xXxxxxxxxxxxxxxxxxxxxx'
USER_ID = '10157500000000000'
USER_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...'
PAGE_ID = '111580000000000'
PAGE_ACCESS_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx...'

def get_query_token():
    access_token = gvs.getFacebookToken()
    if not access_token:
        #app_id = 'YOUR_APP_ID'
        #app_secret = 'YOUR_APP_SECRET'
        graph = facebook.GraphAPI()
        access_token = graph.get_app_access_token(APP_ID, APP_SECRET) 
        gvs.setFacebookToken(access_token)
        print('oauth_facebook access_token : %s'%( access_token ))
        
    return access_token


@api_view(['GET'])
def get_posts_from_fanspage(request):
    
    graph = facebook.GraphAPI(USER_ACCESS_TOKEN)
    print('get_posts_from_fanspage graph : %s'%( graph ))
    if graph:
        resp = graph.get_object('me/accounts')
        print('get_posts_from_fanspage resp : %s'%( resp ))

        page_access_token = None
        for page in resp['data']:
            if page['id'] == PAGE_ID:
                page_access_token = page['access_token']
        print('get_posts_from_fanspage page_access_token : %s'%( page_access_token ))

        page_graph = facebook.GraphAPI(page_access_token)
        print('get_posts_from_fanspage page_graph : %s'%( page_graph ))
        page_resp = page_graph.get_object('jessiecodingtest', field = 'id')
        print('get_posts_from_fanspage page_resp : %s'%( page_resp ))
        print('get_posts_from_fanspage page_resp : %s'%( page_resp['id'] ))

        posts = page_graph.get_connections(id = PAGE_ID, connection_name = 'posts', summary = True)
        print('get_posts_from_fanspage posts : %s'%( posts ))
            
        return Response({'status':'get_posts_from_fanspage published','data': posts })
    else:
        return Response({'status':'get_posts_from_fanspage facebook.GraphAPI(USER_ACCESS_TOKEN) fail' })

