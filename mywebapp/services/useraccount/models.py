from django.db import models

class accountModel(object):
    def __init__(self, username, password, email
    , first_name, last_name, last_login, date_joined
    , is_staff, is_superuser, is_active, auth_token):
       self.username =username
       self.password = password
       self.email = email
       self.first_name = first_name
       self.last_name = last_name
       self.last_login = last_login
       self.date_joined = date_joined
       #self.token_issued = token_issued
       self.is_staff = is_staff
       self.is_superuser = is_superuser
       self.is_active = is_active
       self.auth_token = auth_token
