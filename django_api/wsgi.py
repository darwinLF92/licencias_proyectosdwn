import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings')

try:
    application = get_wsgi_application()
except Exception as e:
    print("Error al iniciar WSGI:", str(e), file=sys.stderr)
    traceback.print_exc()
    raise
