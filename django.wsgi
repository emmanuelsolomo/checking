import os
import sys
import os
from django.core.wsgi import get_wsgi_application

path='/apps/checking'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'checking.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'checking.settings')

application = get_wsgi_application()


#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
