import os
from django.core.asgi import get_asgi_application

# Indique à Django d’utiliser le bon fichier de configuratios.environ.setdefault('DJANGO_SETTINGS_MODULE', 'willet_config')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.dev')



application = get_asgi_application()
