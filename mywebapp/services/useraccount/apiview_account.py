from django.views.decorators.csrf import csrf_exempt 
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import authentication_classes, permission_classes
import datetime, pytz, json

from bson.objectid import ObjectId
from mywebapp import settings
from . import models
from . import serializers as api_ser


''' e.g. http://localhost:5678/account_read_all '''
@api_view(['GET'])
@permission_classes([IsAdminUser])
def account_read_all(request):  
    if request.method == 'GET':
        try:
            data_list = []
            current_users = User.objects.all()
            # current_users = User.objects.get(is_active=True)
            for tmpuser in current_users:
                #print('--------account_read_all------- tmpuser: ', tmpuser.id )
                #print('--------account_read_all------- byid: ', User.objects.get(id=tmpuser.id).get_username())
                acc = models.accountModel( 
                    tmpuser.get_username(),
                    tmpuser.password,
                    tmpuser.email,
                    tmpuser.first_name,
                    tmpuser.last_name,
                    tmpuser.last_login,
                    tmpuser.date_joined,
                    #tmpuser.token_issued,
                    tmpuser.is_staff,
                    tmpuser.is_superuser,
                    tmpuser.is_active,
                    get_token(tmpuser)
                )
                data_list.append(acc)            
            serializedList = api_ser.accountSerializer(data_list, many=True)
            return Response(serializedList.data)
        except ObjectDoesNotExist:
            return Response({'status':'account_read_all ObjectDoesNotExist'})
    else:
        return Response({'status':'account_read_all fail'})


''' e.g. http://localhost:5678/account_read_one/user1 '''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def account_read_one(request, accountname):   
    if request.method == 'GET':
        #print(request.user.is_staff)
        #print(str(request.user) == accountname.strip())
        if ((request.user.is_staff) | (str(request.user) == accountname)):
            try:
                existing_user = User.objects.get(username=accountname)
                    
                return_user = models.accountModel( 
                    existing_user.get_username(),
                    existing_user.password,
                    existing_user.email,
                    existing_user.first_name,
                    existing_user.last_name,
                    existing_user.last_login,
                    existing_user.date_joined,
                    #existing_user.token_issued,
                    existing_user.is_staff,
                    existing_user.is_superuser,
                    existing_user.is_active,
                    get_token( existing_user )
                )        
                serializedList = api_ser.accountSerializer(return_user, many=False)
                return Response(serializedList.data)
            except ObjectDoesNotExist:
                return Response({'status':'account_read_one ObjectDoesNotExist'})
        else:
            return Response({'status':'account_read_one no permission'})
    else:
        return Response({'status':'account_read_one fail'})


'''
e.g. http://localhost:5678/account_create/
request_data = { 
    "username": "user1", 
    "password" : "user1pwd", 
    "email" : "user1@test.mysite.com",
    "first_name" : "user1 first_name", 
    "last_name" : "user1 last_name", 
    "last_login" : "2020-05-13T00:01:01Z", 
    "date_joined" : "2020-05-13T00:01:01Z", 
    "is_staff" : false,
    "is_superuser" : false,
    "is_active" : false,
    "auth_token" : "none"
}
'''
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def account_create(request):
    request_data=request.data
    print(request_data)
    print(type(request_data))

    if type(request_data)==str:
        request_data = json.loads(request_data)

    print(request_data)
    print(type(request_data))

    serialized = api_ser.accountSerializer(data = request_data)

    print(serialized.is_valid())

    if serialized.is_valid():
        return_user = None
        try:
            existing_user = User.objects.get( username = request_data.get("username") )
            return Response({'status':'account_create user already exists'})

        except ObjectDoesNotExist:
            new_user = User.objects.create_user(
                request_data.get("username"), 
                password=request_data.get("password")
            )
            new_user.set_password( request_data.get("password") )
            new_user.email = request_data.get("email")     
            new_user.first_name = request_data.get("first_name") 
            new_user.last_name = request_data.get("last_name") 
            new_user.last_login = None
            new_user.date_joined = datetime.datetime.now()
            #new_user.token_issued = request_data.get("token_issued")           
            new_user.is_superuser = chk_bool( request_data.get("is_superuser") )
            new_user.is_staff = chk_bool( request_data.get("is_staff") )
            new_user.is_active = False
            new_user.save()
            new_token, created = Token.objects.get_or_create( user=new_user )

            return_user = models.accountModel( 
                new_user.get_username(),
                new_user.password,
                new_user.email,
                new_user.first_name,
                new_user.last_name,
                new_user.last_login,
                new_user.date_joined,
                #new_user.token_issued,
                new_user.is_staff,
                new_user.is_superuser,
                new_user.is_active,
                #get_token( new_user ),
                new_token.key
            )
            print('%saccount_activate/%s/%s/' % (settings.BASE_URL,new_user.get_username(), str(new_token.key)))

        serializedList = api_ser.accountSerializer(return_user, many=False)
        return Response(serializedList.data)   
    else:
        return Response(serialized._errors)


'''
e.g. http://localhost:5678/account_update/
request_data = { 
    "username": "user3", 
    "password" : "user3pwd", 
    "email" : "user33@test.mysite.com",
    "first_name" : "user33 first_name", 
    "last_name" : "user33 last_name", 
    "last_login" : "2020-05-12T00:01:01Z", 
    "date_joined" : "2020-05-12T00:01:01Z", 
    "is_staff" : true,
    "is_superuser" : true,
    "is_active" : true,
    "auth_token" : "none"
}
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_update(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.accountSerializer(data = request_data)
    if serialized.is_valid():
        return_user = None
        try:
            existing_user = User.objects.get( username = request_data.get("username") )
            #existing_user.set_password( request_data.get("password") )
            existing_user.email = request_data.get("email")  
            existing_user.first_name = request_data.get("first_name") 
            existing_user.last_name = request_data.get("last_name") 
            existing_user.last_login = request_data.get("last_login") 
            existing_user.date_joined = request_data.get("date_joined") 
           # existing_user.token_issued = request_data.get("token_issued")                        
            existing_user.is_superuser = chk_bool( request_data.get("is_superuser") )
            existing_user.is_staff = chk_bool( request_data.get("is_staff") )
            existing_user.save()

            return_user = models.accountModel( 
                existing_user.get_username(),
                existing_user.password,
                existing_user.email,
                existing_user.first_name,
                existing_user.last_name,
                existing_user.last_login,
                existing_user.date_joined,
                #existing_user.token_issued,
                existing_user.is_staff,
                existing_user.is_superuser,
                existing_user.is_active,
                get_token( existing_user )
            )
            serializedList = api_ser.accountSerializer(return_user, many=False)
            return Response(serializedList.data) 

        except ObjectDoesNotExist:
            return Response({'status':'account_update: the user does not exist'})
    else:
        return Response(serialized._errors)


''' 
e.g. http://localhost:5678/account_deactivate/
request_data = { "username": "user3" } 
'''
@api_view(['POST'])
@permission_classes([IsAdminUser])
def account_deactivate(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.accountSerializer(data = request_data)
    if serialized.is_valid():
        return_user = None
        try:
            existing_user = User.objects.get( username = request_data.get("username") )
            existing_user.is_active = False
            existing_user.save()
            return_user = models.accountModel( 
                existing_user.get_username(),
                existing_user.password,
                existing_user.email,
                existing_user.first_name,
                existing_user.last_name,
                existing_user.last_login,
                existing_user.date_joined,
                #existing_user.token_issued,
                existing_user.is_staff,
                existing_user.is_superuser,
                existing_user.is_active,
                get_token( existing_user )
            )
            serializedList = api_ser.accountSerializer(return_user, many=False)
            return Response(serializedList.data) 

        except ObjectDoesNotExist:
            return Response({'status':'account_deactivate: the user does not exist'})
    else:
        return Response(serialized._errors)


''' 
e.g. http://localhost:5678/account_activate/user16/c233e30f62e2c19f2dab94f3bf794bcbdc56af08/
account_activate/user1cccc/515c5a8a515ded9dd1d5d74521a9749c4b843374

account_activate/user0/3f11ddc7dd4ce895fff1f3319ae9c0e77570a633
request_data = { "username": "user1" } 
'''
@api_view(['GET'])
#@permission_classes([IsAdminUser])
def account_activate(request,accountname,tokenstr):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    print(accountname,tokenstr)
    return_user = None
    try:
        existing_user = User.objects.get( username = accountname )

        us_tz = pytz.timezone('US/Pacific')
        dt_now = datetime.datetime.now().replace(tzinfo=us_tz)
        dt_join = existing_user.date_joined.replace(tzinfo=us_tz)
        dt_expired = ( existing_user.date_joined + datetime.timedelta(hours=1)).replace(tzinfo=us_tz)
        #print( dt_now, dt_join, dt_expired)
        #print( dt_join<dt_now, dt_now < dt_expired)
        #print( get_token(existing_user) )
        #print( get_token(existing_user)==tokenstr )
        
        if ((dt_join<dt_now) and (dt_now < dt_expired)):
            if(str(get_token(existing_user))==tokenstr.strip()):
                existing_user.is_active = True
                existing_user.save()
                return_user = models.accountModel( 
                    existing_user.get_username(),
                    existing_user.password,
                    existing_user.email,
                    existing_user.first_name,
                    existing_user.last_name,
                    existing_user.last_login,
                    existing_user.date_joined,
                    #existing_user.token_issued,
                    existing_user.is_staff,
                    existing_user.is_superuser,
                    existing_user.is_active,
                    get_token( existing_user )
                )
                serializedList = api_ser.accountSerializer(return_user, many=False)
                return Response(serializedList.data) 
            else:
                return Response({'status':'account_activate: token not matched'})
        else:
            return Response({'status':'account_activate: token expired'})
    except ObjectDoesNotExist:
        return Response({'status':'account_activate: the user does not exist'})


'''
e.g. http://localhost:5678/account_login/
request_data = { "username": "admin", "password" : "admin123456" }
request_data = { "username": "user0", "password" : "user0pwd" }
request_data = { "username": "user1", "password" : "user1pwd" }
request_data = { "username": "user2", "password" : "user2pwd" }
request_data = { "username": "user3", "password" : "user3pwd" }
request_data = { "username": "user4", "password" : "user4pwd" }
'''
@api_view(['POST'])
def account_login(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.accountSerializer(data = request_data)
    if serialized.is_valid():
        try:
            existing_user = User.objects.get( username = request_data.get("username"), is_active=True )
            check = existing_user.check_password( request_data.get("password") )
            if check is True:
                if existing_user.is_active:
                    auth_user = auth.authenticate(
                        username= existing_user.get_username(), 
                        password= request_data.get("password")
                    )
                    if auth_user is not None:
                        auth.login(request, auth_user)
                        # print('--------account_login-------',auth_user.is_authenticated)
                        # token, _ = Token.objects.get_or_create(user=user)
                        new_token, created = Token.objects.get_or_create( user=auth_user )
                        return_user = models.accountModel( 
                            existing_user.get_username(),
                            existing_user.password,
                            existing_user.email,
                            existing_user.first_name,
                            existing_user.last_name,
                            existing_user.last_login,
                            existing_user.date_joined,
                            #existing_user.token_issued,
                            existing_user.is_staff,
                            existing_user.is_superuser,
                            existing_user.is_active,
                            new_token.key
                        )
                        serializedList = api_ser.accountSerializer(return_user, many=False)
                        return Response(serializedList.data)
                    else:
                        return Response({'status':'account_login: invalid credentials'})                    
                else:
                    return Response({'status':'account_login: unavailable user'})
            else:
                return Response({'status':'account_login: the password is not correct'})
        except ObjectDoesNotExist:
            return Response({'status':'account_login: the user does not exist or not active'})
    else:
        return Response(serialized._errors)


'''
e.g. http://localhost:5678/account_logout/
request_data = { "username": "user0" }
request_data = { "username": "user1" }
request_data = { "username": "user3" }
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_logout(request):
    request_data=request.data
    if type(request_data)==str:
        request_data = json.loads(request_data)

    serialized = api_ser.accountSerializer(data = request_data)
    if serialized.is_valid():
        if request.user.get_username()== request_data.get("username"):
            try:
                existing_user = User.objects.get( username = request_data.get("username") )
                auth.logout(request)
                existing_user.auth_token.delete()
                return Response({'status':'account_logout: done'})
            except ObjectDoesNotExist:
                return Response({'status':'account_logout: the user does not exist'})
        else:
            return Response({'status':'account_logout: not current user'})
    else:
        return Response(serialized._errors)


def get_token( checking_user):
    return_string = None
    try:
        return_string = checking_user.auth_token
    except:
        return_string = 'not issued yet'
    return return_string

def chk_bool ( data_item ):
    return_value = False
    try:
        if (type(data_item) == bool):
            return_value = data_item
        elif (type(data_item) == str):
            if (data_item.lower() == 'true'):
                return_value = True
    except:
        return_value = False
    return return_value