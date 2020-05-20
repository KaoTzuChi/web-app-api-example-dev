from django.db import models

class productModel(object):
    def __init__(self, objectid, title, brief, price, contact, location, lastupdate, tags):
        self.objectid = objectid
        self.title = title
        self.brief = brief
        self.price = price
        self.contact = contact
        self.location = location
        self.lastupdate = lastupdate
        self.tags = tags


