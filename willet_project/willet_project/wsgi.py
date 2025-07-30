import os
from django.core.wsgi import get_wsgi_application

# Indique à Django d’utiliser la configuration de développemeos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'willet_config')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')


application = get_wsgi_application()
