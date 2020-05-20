"""
WSGI config for mywebapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/

"""

import os, sys
from django.core.wsgi import get_wsgi_application

#for exe from manage_dev.py
#sys.path.append('/mywebapp')
#for exe from manage.py
#sys.path.append('/home/www/avlexam/mywebapp/mywebapp')
#for exe from wsgi.ini
#sys.path.append('/home/www/avlexam/mywebapp')

try:
    import mywebapp.globals as gvs
    print('********** in mywebapp.wsgi.py ********** appEntry() = '+ str(gvs.appEntry()))
    if (gvs.appEntry()==0):
        sys.path.append('/mywebapp')
    else:
        sys.path.append('/home/www/avlexam/mywebapp/mywebapp')
        gvs.enableProdWsgi()
    
except ImportError as error:
    print('********** in mywebapp.wsgi.py ********** ImportError : %s'%( error ))
    sys.path.append('/home/www/avlexam/mywebapp')
    #os.environ["PYTHONPATH"] = "/home/www/avlexam/ap2env/bin"
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

except Exception as exception:
    print('********** in mywebapp.wsgi.py ********** Exception : %s'%( exception ))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebapp.settings')
application = get_wsgi_application()
