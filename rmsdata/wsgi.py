"""
WSGI config for rmsdata project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys
import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
#为了解决wsgi的问题, 导入了sys库,并将BASE_DIR加入sys.path
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rmsdata.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'rmsdata.settings'

#application = get_wsgi_application()
application = django.core.handlers.wsgi.WSGIHandler()
