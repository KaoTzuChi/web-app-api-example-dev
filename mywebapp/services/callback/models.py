from django.db import models

class callbackModel(object):
    def __init__(self, objectid, sender, data, statuscode, lastupdate):
        self.objectid = objectid
        self.sender = sender
        self.data = data
        self.statuscode = statuscode
        self.lastupdate = lastupdate


