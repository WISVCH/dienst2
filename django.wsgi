import os
import sys

path = '/home/markj/dienst2'
if path not in sys.path:
    sys.path.append(path)
    sys.path.append(os.path.normpath(path+"/.."))

os.environ['DJANGO_SETTINGS_MODULE'] = 'dienst2.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
