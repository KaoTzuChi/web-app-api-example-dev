#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
import logging.handlers
import mywebapp.globals as gvs

#os.environ["PYTHONPATH"] = "/home/www/avlexam/ap2env/bin"
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

gvs.enableProdManage()
gvs.setOauthState('')
print('********** in manage.py ********** appEntry() = '+ str(gvs.appEntry()))
print('********** in manage.py ********** getOauthState() = '+ str(gvs.getOauthState()))

def main():
    #sys.path.append('/home/www/pinkgarden/django/djsite')
    sys.path.append('/home/www/avlexam/mywebapp/mywebapp')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mywebapp.settings')

    '''
    # Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
    logging.getLogger().setLevel(logging.NOTSET)

    # Add stdout handler, with level INFO
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    formater = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
    console.setFormatter(formater)
    logging.getLogger().addHandler(console)

    # Add file rotating handler, with level DEBUG
    rotatingHandler = logging.handlers.RotatingFileHandler(filename='rotating.log', maxBytes=1000, backupCount=5)
    rotatingHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotatingHandler.setFormatter(formatter)
    logging.getLogger().addHandler(rotatingHandler)

    log = logging.getLogger("app." + __name__)
    log.debug('Debug message, should only appear in the file.')
    log.info('Info message, should appear in file and stdout.')
    log.warning('Warning message, should appear in file and stdout.')
    log.error('Error message, should appear in file and stdout.')
    '''

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
