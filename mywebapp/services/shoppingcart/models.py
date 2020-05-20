from django.db import models

class shoppingcartModel(object):
    def __init__(self, objectid, memberid, orderid, productid,productname, price, discount,count, lastupdate):
        self.objectid = objectid
        self.memberid = memberid
        self.orderid = orderid
        self.productid = productid
        self.productname = productname
        self.price = price
        self.discount = discount
        self.count = count
        self.lastupdate = lastupdate
