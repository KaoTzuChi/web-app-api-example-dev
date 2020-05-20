"""mywebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from views import app
from views.order import order
from views.product import product
from views.dashboard import dashboard
from views.data import data
from views.member import member
from views.contact import contact
from views.facebook import facebook
from services.dataaccess import apiview_mycollectionone as apiview_one
from services.dataaccess import apiview_mycollectiontwo as apiview_two
from services.dataaccess import apiview_mycollectionthree as apiview_three
from services.useraccount import apiview_account as apiview_acc
from services.callback import apiview_callback as apiview_cb
from services.product import apiview_product as apiview_product
from services.shoppingcart import apiview_shoppingcart as apiview_cart
from services.order import apiview_order as apiview_odr
from services.googleapi import oauthtwo
from services.facebookapi import facebookapi
from services.firebaseapi import firebaseapi
from services.stripeapi import stripeapi

router = DefaultRouter()

urlpatterns = [
    url(r'^$', app.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),  

    url(r'^read_mycollectionone_all/$', apiview_one.read_mycollectionone_all),
    url(r'^read_mycollectionone_byid/(?P<id>[-\w]+)/$', apiview_one.read_mycollectionone_byid),
    url(r'^read_mycollectionone_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_one.read_mycollectionone_byfield),
    url(r'^create_doc_in_mycollectionone_return_newone/$', apiview_one.create_doc_in_mycollectionone_return_newone),
    url(r'^replace_doc_in_mycollectionone_return_newone/$', apiview_one.replace_doc_in_mycollectionone_return_newone),
    url(r'^delete_doc_in_mycollectionone_return_count/$', apiview_one.delete_doc_in_mycollectionone_return_count),
    url(r'^data/query/$', data.data_query, name='data_query'),
    url(r'^data/search/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', data.data_search, name='data_search'),
    url(r'^data/create/$', data.data_create, name='data_create'),
    url(r'^data/detail/(?P<id>[-\w]+)/$', data.data_detail, name='data_detail'),
    url(r'^data/update/(?P<id>[-\w]+)/$', data.data_update, name='data_update'),
    url(r'^data/create_action/$', data.data_create_action, name='data_create_action'),
    url(r'^data/update_action/$', data.data_update_action, name='data_update_action'),
    url(r'^data/delete_action/$', data.data_delete_action, name='data_delete_action'),

    url(r'^read_mycollectiontwo_all/$', apiview_two.read_mycollectiontwo_all),
    url(r'^read_mycollectiontwo_byid/(?P<id>[-\w]+)/$', apiview_two.read_mycollectiontwo_byid),
    url(r'^read_mycollectiontwo_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_two.read_mycollectiontwo_byfield),
    url(r'^create_doc_in_mycollectiontwo_return_newone/$', apiview_two.create_doc_in_mycollectiontwo_return_newone),
    url(r'^replace_doc_in_mycollectiontwo_return_newone/$', apiview_two.replace_doc_in_mycollectiontwo_return_newone),
    url(r'^delete_doc_in_mycollectiontwo_return_count/$', apiview_two.delete_doc_in_mycollectiontwo_return_count),

    url(r'^read_mycollectionthree_all/$', apiview_three.read_mycollectionthree_all),
    url(r'^read_mycollectionthree_byid/(?P<id>[-\w]+)/$', apiview_three.read_mycollectionthree_byid),
    url(r'^read_mycollectionthree_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_three.read_mycollectionthree_byfield),
    url(r'^dashboard/$', dashboard.dashboard_main, name='dashboard_main'),

    url(r'^read_product_all/$', apiview_product.read_product_all),
    url(r'^read_product_byid/(?P<id>[-\w]+)/$', apiview_product.read_product_byid),
    url(r'^read_product_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_product.read_product_byfield),
    url(r'^create_doc_in_product_return_newone/$', apiview_product.create_doc_in_product_return_newone),
    url(r'^replace_doc_in_product_return_newone/$', apiview_product.replace_doc_in_product_return_newone),
    url(r'^delete_doc_in_product_return_count/$', apiview_product.delete_doc_in_product_return_count),
    url(r'^product/query/$', product.product_query, name='product_query'),
    url(r'^product/search/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', product.product_search, name='product_search'),
    url(r'^product/detail/(?P<id>[-\w]+)/$', product.product_detail, name='product_detail'),
    url(r'^product/addtocart/$', product.product_addtocart, name='product_addtocart'),

    url(r'^read_shoppingcart_all/$', apiview_cart.read_shoppingcart_all),
    url(r'^read_shoppingcart_unpaid/$', apiview_cart.read_shoppingcart_unpaid),
    url(r'^read_shoppingcart_byid/(?P<id>[-\w]+)/$', apiview_cart.read_shoppingcart_byid),
    url(r'^read_shoppingcart_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_cart.read_shoppingcart_byfield),
    url(r'^create_doc_in_shoppingcart_return_newone/$', apiview_cart.create_doc_in_shoppingcart_return_newone),
    url(r'^replace_doc_in_shoppingcart_return_newone/$', apiview_cart.replace_doc_in_shoppingcart_return_newone),
    url(r'^replace_orderid_in_shoppingcart_return_count/$', apiview_cart.replace_orderid_in_shoppingcart_return_count),
    url(r'^delete_doc_in_shoppingcart_return_count/$', apiview_cart.delete_doc_in_shoppingcart_return_count),

    url(r'^read_order_all/$', apiview_odr.read_order_all),
    url(r'^read_order_byid/(?P<id>[-\w]+)/$', apiview_odr.read_order_byid),
    url(r'^read_order_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_odr.read_order_byfield),
    url(r'^create_doc_in_order_return_newone/$', apiview_odr.create_doc_in_order_return_newone),
    url(r'^replace_doc_in_order_return_newone/$', apiview_odr.replace_doc_in_order_return_newone),
    url(r'^delete_doc_in_order_return_count/$', apiview_odr.delete_doc_in_order_return_count),
    url(r'^paymentcallback/$', apiview_odr.paymentcallback),

    url(r'^cart/query/$', order.cart_query, name='cart_query'),
    url(r'^cart/update/$', order.cart_update, name='cart_update'),
    url(r'^cart/delete/(?P<id>[-\w]+)/$', order.cart_delete, name='cart_delete'),
    url(r'^cart/checkout/$', order.cart_checkout, name='cart_checkout'),
    url(r'^order/create/$', order.order_create, name='order_create'),
    url(r'^order/query/$', order.order_query, name='order_query'),
    url(r'^order/detail/(?P<id>[-\w]+)/$', order.order_detail, name='order_detail'),

    url(r'^account_read_all/$', apiview_acc.account_read_all),
    url(r'^account_read_one/(?P<accountname>[-\w]+)/$', apiview_acc.account_read_one),
    url(r'^account_create/$', apiview_acc.account_create),
    url(r'^account_update/$', apiview_acc.account_update),
    url(r'^account_deactivate/$', apiview_acc.account_deactivate),
    url(r'^account_activate/(?P<accountname>[-\w]+)/(?P<tokenstr>[-\w]+)/$', apiview_acc.account_activate),
    url(r'^account_login/$', apiview_acc.account_login),
    url(r'^account_logout/$', apiview_acc.account_logout),  
    url(r'^member/create/$', member.member_create, name='member_create'),
    url(r'^member/create_action/$', member.member_create_action, name='member_create_action'),
    url(r'^member/login/$', member.member_login, name='member_login'),
    url(r'^member/login_action/$', member.member_login_action, name='member_login_action'),
    url(r'^member/logout/$', member.member_logout, name='member_logout'),
    url(r'^member/logout_action/$', member.member_logout_action, name='member_logout_action'),
    url(r'^member/update/$', member.member_update, name='member_update'),
    url(r'^member/reload/$', member.member_reload, name='member_reload'),
    url(r'^member/update_action/$', member.member_update_action, name='data_update_action'),

    url(r'^read_callback_all/$', apiview_cb.read_callback_all),
    url(r'^read_callback_byid/(?P<id>[-\w]+)/$', apiview_cb.read_callback_byid),
    url(r'^read_callback_byfield/(?P<field>[-\w]+)/(?P<value>[-\w]+)/$', apiview_cb.read_callback_byfield),
    url(r'^create_doc_in_callback_return_newone/$', apiview_cb.create_doc_in_callback_return_newone),
    url(r'^replace_doc_in_callback_return_newone/$', apiview_cb.replace_doc_in_callback_return_newone),
    url(r'^delete_doc_in_callback_return_count/$', apiview_cb.delete_doc_in_callback_return_count),

    url(r'^oauth2_gmail/$', oauthtwo.oauth2_gmail),
    url(r'^oauth2_sheets/$', oauthtwo.oauth2_sheets),

    url(r'^firebase_insert/$', firebaseapi.firebase_insert),
    url(r'^firebase_retrieve/$', firebaseapi.firebase_retrieve),
    url(r'^firebase_update/$', firebaseapi.firebase_update),
    url(r'^firebase_delete/$', firebaseapi.firebase_delete),

    url(r'^stripe_test/$', stripeapi.stripe_test),
    
    url(r'^contact/create/$', contact.contact_create, name='contact_create'),
    url(r'^contact/sendmail/$', contact.contact_sendmail, name='contact_sendmail'),

    url(r'^facebook/login/$', facebook.facebook_login, name='facebook_login'),
    #url(r'^oauth_facebook/$', facebookapi.oauth_facebook),
    url(r'^get_posts_from_fanspage/$', facebookapi.get_posts_from_fanspage),
]
