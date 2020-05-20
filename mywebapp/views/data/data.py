from django.shortcuts import render, redirect
from django.http import HttpResponse
#from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import requests, datetime, json
import mywebapp.settings as settings
from bson.objectid import ObjectId

from views.utility import dict_key
from services.dataaccess import models
from services.dataaccess import serializers as api_ser

#chkoptions = ['a','b','c','d','e','f','g','h']
chkoptions = ['a','b','c','d']
rdooptions = [1.11,2.22,3.33,4.44]
seloptions = [
    datetime.date.today().strftime('%Y-%m-%dT%H:%M:%SZ'),
    (datetime.date.today()+ datetime.timedelta(weeks=1)).strftime('%Y-%m-%dT%H:%M:%SZ'),
    (datetime.date.today()+ datetime.timedelta(weeks=2)).strftime('%Y-%m-%dT%H:%M:%SZ'),
    (datetime.date.today()+ datetime.timedelta(weeks=3)).strftime('%Y-%m-%dT%H:%M:%SZ'),
]
#dictkeyvaluess = {'item1':'1', 'item2':'2','item3':'3','item4':'4','item5':'5'}
dictkeyvaluess = dict(item1='', item2='',item3='',item4='',item5='')

def data_query(request):
    response = requests.get( settings.BASE_URL + 'read_mycollectionone_all/')
    receiveddata = None
    if response:
        receiveddata = response.json()

    return render(request, 'data_query.html', {
        'receiveddata': receiveddata,
        'chkoptions' : chkoptions,
        'rdooptions' : rdooptions,
        'seloptions' : seloptions,
        'dictkeyvaluess' : dictkeyvaluess,
    })

def data_search(request, field, value):
    print('data_search field=',field,' value=',value)

    response = requests.get( settings.BASE_URL + 'read_mycollectionone_byfield/'+field+'/'+value+'/')
    receiveddata = None
    if response:
        receiveddata = response.json()

    return render(request, 'data_query.html', {
        'receiveddata': receiveddata,
        'chkoptions' : chkoptions,
        'rdooptions' : rdooptions,
        'seloptions' : seloptions,
        'dictkeyvaluess' : dictkeyvaluess,
    })

def data_create(request):
    receiveddata = models.mycollectiononeModel( 
                ObjectId('5eb7f31938a5fd5d85ccf595'),
                'field1test',
                dictkeyvaluess,
                datetime.date.today(),
                3.33,
                ['c','a']
        )
    return render(request, 'data_create.html', {
        'chkoptions' : chkoptions,
        'rdooptions' : rdooptions,
        'seloptions' : seloptions,
        'dictkeyvaluess' : dictkeyvaluess,
        'receiveddata':receiveddata,
    })

def data_detail(request, id):
    response = requests.get( settings.BASE_URL + 'read_mycollectionone_byid/'+id+'/')
    receiveddata = None
    if response:
        receiveddata = response.json()
        receiveddata['field14'] = float(receiveddata['field14'] )
    return render(request, 'data_detail.html', {
        'chkoptions' : chkoptions,
        'rdooptions' : rdooptions,
        'seloptions' : seloptions,
        'dictkeyvaluess' : dictkeyvaluess,
        'receiveddata':receiveddata,
    })

def data_update(request, id):
    response = requests.get( settings.BASE_URL + 'read_mycollectionone_byid/'+id+'/')
    receiveddata = None
    if response:
        receiveddata = response.json()
        receiveddata['field14'] = float(receiveddata['field14'] )
    return render(request, 'data_update.html', {
        'chkoptions' : chkoptions,
        'rdooptions' : rdooptions,
        'seloptions' : seloptions,
        'dictkeyvaluess' : dictkeyvaluess,
        'receiveddata':receiveddata,
    })


def data_create_action(request):
    if request.method == 'POST':
        posteddata = dict(request.POST)
        field12dict = dict()
        for k in dictkeyvaluess:
            if len(posteddata['field12.'+k][0].strip())>0:
                field12dict.update({ k : posteddata['field12.'+k][0].strip()})

        model_data = { 
            'objectid' : posteddata['objectid'][0],
            'field11' : posteddata['field11'][0].strip(),
            'field12' : field12dict,
            'field13' : posteddata['field13'][0],
            'field14' : float(posteddata['field14'][0]),
            'field15' : posteddata['field15']
        }
        response = requests.post( settings.BASE_URL + 'create_doc_in_mycollectionone_return_newone/', json=json.dumps(model_data)  )
        #postedform = DataForm(request.POST)
        #if form.is_valid():
            #book_inst.due_back = form.cleaned_data['renewal_date']
            #book_inst.save()
            #return HttpResponseRedirect(reverse('all-borrowed') )
    else:
        pass

    return redirect('/data/query/')

def data_update_action(request):
    if request.method == 'POST':
        posteddata = dict(request.POST)
        field12dict = dict()
        for k in dictkeyvaluess:
            if len(posteddata['field12.'+k][0].strip())>0:
                field12dict.update({ k : posteddata['field12.'+k][0].strip()})

        model_data = { 
            'objectid' : posteddata['objectid'][0],
            'field11' : posteddata['field11'][0].strip(),
            'field12' : field12dict,
            'field13' : posteddata['field13'][0],
            'field14' : float(posteddata['field14'][0]),
            'field15' : posteddata['field15']
        }
        response = requests.post( settings.BASE_URL + 'replace_doc_in_mycollectionone_return_newone/', json=json.dumps(model_data)  )
    else:
        pass

    return redirect('/data/query/')

def data_delete_action(request):

    if request.method == 'POST':
        posteddata = dict(request.POST)
        model_data = { 
            'objectid' : posteddata['objectid'][0],
        }
        response = requests.post( settings.BASE_URL + 'delete_doc_in_mycollectionone_return_count/', json=json.dumps(model_data)  )
    else:
        pass

    return redirect('/data/query/')



'''
class DataForm(forms.Form):
    field11 = forms.CharField(help_text="Enter a date for field11.")
    #field12 = forms.MultiValueField(help_text="Enter a date for field12.")
    field12 = forms.MultipleChoiceField(help_text="Enter a date for field12.")
    #field13 = forms.DateTimeField(help_text="Enter a date for field13.")
    field13 = forms.ChoiceField(help_text="Enter a date for field13.")
    #field14 = forms.DecimalField(help_text="Enter a date for field14.")
    field14 = forms.ChoiceField(help_text="Enter a date for field14.")
    field15 = forms.MultipleChoiceField(help_text="Enter a date for field15.")

    def clean_field11(self):
        check = self.cleaned_data['field11']
        if len(check) < 5:
            raise ValidationError(_('Invalid data - <5'))
        if len(check) > 12:
            raise ValidationError(_('Invalid data - >12'))
        return check

BooleanField, CharField, ChoiceField, TypedChoiceField, DateField, DateTimeField, 
DecimalField, DurationField, EmailField, FileField, FilePathField, FloatField, ImageField, 
IntegerField, GenericIPAddressField, MultipleChoiceField, TypedMultipleChoiceField, NullBooleanField, 
RegexField, SlugField, TimeField, URLField, UUIDField, ComboField, MultiValueField, 
SplitDateTimeField, ModelMultipleChoiceField, ModelChoiceField​​​​.
'''