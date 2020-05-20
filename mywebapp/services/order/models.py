from django.db import models

class orderModel(object):
    def __init__(self, objectid, memberid, totalprice, totaldiscount, payment, status, lastupdate):
        self.objectid = objectid
        self.memberid = memberid
        self.totalprice = totalprice
        self.totaldiscount = totaldiscount
        self.payment = payment
        self.status = status
        self.lastupdate = lastupdate
